[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string] $FilePath,

    [Parameter()]
    [string[]] $ArgumentList = @(),

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string] $WorkingDirectory,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string] $ReceiptPath,

    [Parameter()]
    [ValidateRange(10, 5000)]
    [int] $PollMilliseconds = 100,

    [Parameter()]
    [ValidateRange(1, 86400)]
    [int] $TimeoutSeconds = 3600
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not ('BuildShortPaths.Native' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.ComponentModel;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

namespace BuildShortPaths
{
    public static class Native
    {
        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        private static extern UInt32 GetShortPathNameW(String path, StringBuilder buffer, UInt32 length);

        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        private static extern UInt32 GetLongPathNameW(String path, StringBuilder buffer, UInt32 length);

        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        private static extern UInt32 GetFullPathNameW(
            String path, UInt32 length, StringBuilder buffer, IntPtr filePart);

        public static String NormalizeNative(String path)
        {
            StringBuilder buffer = new StringBuilder(32768);
            UInt32 length = GetFullPathNameW(path, (UInt32)buffer.Capacity, buffer, IntPtr.Zero);
            if (length == 0)
            {
                throw new Win32Exception(Marshal.GetLastWin32Error(), "GetFullPathNameW failed");
            }
            if (length >= buffer.Capacity)
            {
                throw new InvalidOperationException("The native path exceeds the bounded path buffer.");
            }
            return buffer.ToString();
        }

        private static String ReadExistingPath(String path, Boolean shorten)
        {
            String fullPath = Path.GetFullPath(path);
            String extendedPath = fullPath.StartsWith(@"\\?\", StringComparison.Ordinal)
                ? fullPath
                : (fullPath.StartsWith(@"\\", StringComparison.Ordinal)
                    ? @"\\?\UNC\" + fullPath.Substring(2)
                    : @"\\?\" + fullPath);
            StringBuilder buffer = new StringBuilder(32768);
            UInt32 length = shorten
                ? GetShortPathNameW(extendedPath, buffer, (UInt32)buffer.Capacity)
                : GetLongPathNameW(extendedPath, buffer, (UInt32)buffer.Capacity);
            if (length == 0)
            {
                throw new Win32Exception(
                    Marshal.GetLastWin32Error(),
                    shorten ? "GetShortPathNameW failed" : "GetLongPathNameW failed");
            }
            if (length >= buffer.Capacity)
            {
                throw new InvalidOperationException("The verified path exceeds the bounded path buffer.");
            }
            String result = buffer.ToString();
            if (result.StartsWith(@"\\?\UNC\", StringComparison.OrdinalIgnoreCase))
            {
                result = @"\\" + result.Substring(8);
            }
            else if (result.StartsWith(@"\\?\", StringComparison.Ordinal))
            {
                result = result.Substring(4);
            }
            // .NET GetFullPath expands existing 8.3 names; preserve them for native launch paths.
            return shorten ? result : Path.GetFullPath(result);
        }

        public static String ExpandExisting(String path)
        {
            return ReadExistingPath(path, false);
        }

        public static String ShortenVerified(String path)
        {
            String canonical = ExpandExisting(path);
            String shortened = ReadExistingPath(canonical, true);
            if (!String.Equals(canonical, ExpandExisting(shortened), StringComparison.OrdinalIgnoreCase))
            {
                throw new InvalidOperationException("The existing short path does not roundtrip to its authority path.");
            }
            return shortened;
        }
    }
}
'@ -Language CSharp -ErrorAction Stop
}

$MemoryLimitBytes = [UInt64] 3221225472
$RequiredLimitFlags = [UInt32] 0x00002200
$BreakawayLimitFlags = [UInt32] 0x00001800
$TerminationExitCode = [UInt32] 3758096385
$blockedProcessNames = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
foreach ($blockedName in @(
    'pdflatex', 'pdftex', 'bibtex', 'bibtex8', 'latex', 'latexmk',
    'xelatex', 'lualatex', 'miktex-pdftex', 'miktex-bibtex', 'texify',
    'mktexpk', 'mktextfm'
)) {
    [void] $blockedProcessNames.Add($blockedName)
}

function Get-FullPath {
    param([Parameter(Mandatory = $true)][string] $Path)
    return [System.IO.Path]::GetFullPath($Path)
}

function Test-PathWithin {
    param(
        [Parameter(Mandatory = $true)][string] $ChildPath,
        [Parameter(Mandatory = $true)][string] $ParentPath
    )

    $child = (Get-FullPath -Path $ChildPath).TrimEnd(
        [System.IO.Path]::DirectorySeparatorChar,
        [System.IO.Path]::AltDirectorySeparatorChar
    )
    $parent = (Get-FullPath -Path $ParentPath).TrimEnd(
        [System.IO.Path]::DirectorySeparatorChar,
        [System.IO.Path]::AltDirectorySeparatorChar
    )
    if ($child.Equals($parent, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $true
    }

    $prefix = $parent + [System.IO.Path]::DirectorySeparatorChar
    return $child.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)
}


function Convert-ToCanonicalTaskPath {
    param([Parameter(Mandatory = $true)][string] $Path)

    $nativeNormalized = [BuildShortPaths.Native]::NormalizeNative($Path)
    if (
        $nativeNormalized.Equals($nativePhaseRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
        $nativeNormalized.StartsWith(
            $nativePhaseRoot + [System.IO.Path]::DirectorySeparatorChar,
            [System.StringComparison]::OrdinalIgnoreCase
        )
    ) {
        return Get-FullPath -Path ($phaseRoot + $nativeNormalized.Substring($nativePhaseRoot.Length))
    }
    return Get-FullPath -Path $nativeNormalized
}

function Convert-ToNativeTaskPath {
    param([Parameter(Mandatory = $true)][string] $Path)

    $canonicalPath = Convert-ToCanonicalTaskPath -Path $Path
    if (-not (Test-PathWithin -ChildPath $canonicalPath -ParentPath $phaseRoot)) {
        throw "Native task-path conversion escapes the exact phase root: $canonicalPath"
    }
    $nativePath = $nativePhaseRoot + $canonicalPath.Substring($phaseRoot.Length)
    if ($nativePath.Length -ge 260) {
        throw "Verified short native path still reaches MAX_PATH: $nativePath"
    }
    $expandedPath = [BuildShortPaths.Native]::ExpandExisting($nativePath)
    if (-not $expandedPath.Equals($canonicalPath, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Native task path did not roundtrip to its exact authority path: $canonicalPath"
    }
    return $nativePath
}

if ([IntPtr]::Size -ne 8) {
    throw 'The guarded launcher requires 64-bit PowerShell so the exact 3,221,225,472-byte limit cannot overflow.'
}

$canonicalScriptPath = [BuildShortPaths.Native]::ExpandExisting($PSCommandPath)
$controlsRoot = Get-FullPath -Path ([System.IO.Path]::GetDirectoryName($canonicalScriptPath))
$assignmentRoot = Get-FullPath -Path ([System.IO.Path]::GetDirectoryName($controlsRoot))
$phaseRoot = Get-FullPath -Path ([System.IO.Path]::GetDirectoryName($assignmentRoot))
$nativePhaseRoot = [BuildShortPaths.Native]::ShortenVerified($phaseRoot)
$resolvedExecutable = Convert-ToCanonicalTaskPath -Path $FilePath
$resolvedWorkingDirectory = Convert-ToCanonicalTaskPath -Path $WorkingDirectory
$resolvedReceiptPath = Convert-ToCanonicalTaskPath -Path $ReceiptPath

if (-not (Test-Path -LiteralPath $resolvedExecutable -PathType Leaf)) {
    throw "Guarded executable does not exist: $resolvedExecutable"
}
if (-not (Test-Path -LiteralPath $resolvedWorkingDirectory -PathType Container)) {
    throw "Guarded working directory does not exist: $resolvedWorkingDirectory"
}
if (-not (Test-PathWithin -ChildPath $resolvedWorkingDirectory -ParentPath $assignmentRoot)) {
    throw "Working directory escapes the build root: $resolvedWorkingDirectory"
}
if (-not (Test-PathWithin -ChildPath $resolvedReceiptPath -ParentPath $resolvedWorkingDirectory)) {
    throw "Receipt path must stay inside the guarded working directory: $resolvedReceiptPath"
}

$receiptParent = [System.IO.Path]::GetDirectoryName($resolvedReceiptPath)
if (-not (Test-Path -LiteralPath $receiptParent -PathType Container)) {
    throw "Receipt directory does not exist: $receiptParent"
}
if (Test-Path -LiteralPath $resolvedReceiptPath) {
    throw "Guarded-process receipts are immutable and must not already exist: $resolvedReceiptPath"
}

$temporaryEnvironment = [ordered]@{}
$nativeTemporaryEnvironment = [ordered]@{}
foreach ($temporaryVariable in @('TEMP', 'TMP')) {
    $temporaryValue = [System.Environment]::GetEnvironmentVariable(
        $temporaryVariable,
        [System.EnvironmentVariableTarget]::Process
    )
    if ([string]::IsNullOrWhiteSpace($temporaryValue)) {
        throw "$temporaryVariable must be set to a task-private directory before the guard is loaded."
    }
    $canonicalTemporaryValue = Convert-ToCanonicalTaskPath -Path $temporaryValue
    if (-not (Test-PathWithin -ChildPath $canonicalTemporaryValue -ParentPath $assignmentRoot)) {
        throw "$temporaryVariable escapes the build root: $temporaryValue"
    }
    $temporaryEnvironment[$temporaryVariable] = $temporaryValue
    $nativeTemporaryEnvironment[$temporaryVariable] = Convert-ToNativeTaskPath -Path $canonicalTemporaryValue
}

$nativeWorkingDirectory = Convert-ToNativeTaskPath -Path $resolvedWorkingDirectory
$nativeExecutable = $resolvedExecutable
if (Test-PathWithin -ChildPath $resolvedExecutable -ParentPath $phaseRoot) {
    $nativeExecutable = Convert-ToNativeTaskPath -Path $resolvedExecutable
}
$nativeArguments = [System.Collections.Generic.List[string]]::new()
foreach ($argument in $ArgumentList) {
    if ([System.IO.Path]::IsPathFullyQualified($argument)) {
        $canonicalArgument = Convert-ToCanonicalTaskPath -Path $argument
        if (Test-PathWithin -ChildPath $canonicalArgument -ParentPath $phaseRoot) {
            $nativeArguments.Add((Convert-ToNativeTaskPath -Path $canonicalArgument))
            continue
        }
    }
    $nativeArguments.Add($argument)
}

if (-not ('B04JobGuard.Native' -as [type])) {
    $nativeSource = @'
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;

namespace B04JobGuard
{
    public sealed class JobLimitSnapshot
    {
        public UInt32 LimitFlags { get; set; }
        public UInt64 JobMemoryLimit { get; set; }
        public UInt64 PeakJobMemoryUsed { get; set; }
    }

    public sealed class PrivateMemorySample
    {
        public UInt64 TotalPrivateBytes { get; set; }
        public Int32 ReportedProcessIds { get; set; }
        public Int32 SampledProcesses { get; set; }
        public Int64[] ProcessIds { get; set; }
    }

    public sealed class ChildProcessHandles : IDisposable
    {
        public IntPtr ProcessHandle { get; private set; }
        public IntPtr ThreadHandle { get; private set; }
        public UInt32 ProcessId { get; private set; }

        internal ChildProcessHandles(IntPtr processHandle, IntPtr threadHandle, UInt32 processId)
        {
            ProcessHandle = processHandle;
            ThreadHandle = threadHandle;
            ProcessId = processId;
        }

        public void Dispose()
        {
            if (ThreadHandle != IntPtr.Zero)
            {
                Native.CloseHandle(ThreadHandle);
                ThreadHandle = IntPtr.Zero;
            }
            if (ProcessHandle != IntPtr.Zero)
            {
                Native.CloseHandle(ProcessHandle);
                ProcessHandle = IntPtr.Zero;
            }
            GC.SuppressFinalize(this);
        }
    }

    public static class Native
    {
        private const UInt32 JOB_OBJECT_LIMIT_JOB_MEMORY = 0x00000200;
        private const UInt32 JOB_OBJECT_LIMIT_BREAKAWAY_OK = 0x00000800;
        private const UInt32 JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK = 0x00001000;
        private const UInt32 JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000;
        private const UInt32 REQUIRED_LIMIT_FLAGS =
            JOB_OBJECT_LIMIT_JOB_MEMORY | JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE;
        private const UInt32 BREAKAWAY_LIMIT_FLAGS =
            JOB_OBJECT_LIMIT_BREAKAWAY_OK | JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK;

        private const UInt32 CREATE_SUSPENDED = 0x00000004;
        private const UInt32 CREATE_NO_WINDOW = 0x08000000;
        private const UInt32 CREATE_UNICODE_ENVIRONMENT = 0x00000400;
        private const UInt32 WAIT_OBJECT_0 = 0x00000000;
        private const UInt32 WAIT_TIMEOUT = 0x00000102;
        private const UInt32 PRIVATE_MEMORY_EXIT_RACE_WAIT_MILLISECONDS = 250;
        private const UInt32 PROCESS_QUERY_LIMITED_INFORMATION = 0x00001000;
        private const UInt32 SYNCHRONIZE = 0x00100000;
        private const Int32 ERROR_INVALID_PARAMETER = 87;
        private const Int32 ERROR_MORE_DATA = 234;

        private enum JOBOBJECTINFOCLASS
        {
            JobObjectBasicProcessIdList = 3,
            JobObjectExtendedLimitInformation = 9
        }

        [StructLayout(LayoutKind.Sequential)]
        private struct JOBOBJECT_BASIC_LIMIT_INFORMATION
        {
            public Int64 PerProcessUserTimeLimit;
            public Int64 PerJobUserTimeLimit;
            public UInt32 LimitFlags;
            public UIntPtr MinimumWorkingSetSize;
            public UIntPtr MaximumWorkingSetSize;
            public UInt32 ActiveProcessLimit;
            public UIntPtr Affinity;
            public UInt32 PriorityClass;
            public UInt32 SchedulingClass;
        }

        [StructLayout(LayoutKind.Sequential)]
        private struct IO_COUNTERS
        {
            public UInt64 ReadOperationCount;
            public UInt64 WriteOperationCount;
            public UInt64 OtherOperationCount;
            public UInt64 ReadTransferCount;
            public UInt64 WriteTransferCount;
            public UInt64 OtherTransferCount;
        }

        [StructLayout(LayoutKind.Sequential)]
        private struct JOBOBJECT_EXTENDED_LIMIT_INFORMATION
        {
            public JOBOBJECT_BASIC_LIMIT_INFORMATION BasicLimitInformation;
            public IO_COUNTERS IoInfo;
            public UIntPtr ProcessMemoryLimit;
            public UIntPtr JobMemoryLimit;
            public UIntPtr PeakProcessMemoryUsed;
            public UIntPtr PeakJobMemoryUsed;
        }

        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
        private struct STARTUPINFO
        {
            public UInt32 cb;
            public String lpReserved;
            public String lpDesktop;
            public String lpTitle;
            public UInt32 dwX;
            public UInt32 dwY;
            public UInt32 dwXSize;
            public UInt32 dwYSize;
            public UInt32 dwXCountChars;
            public UInt32 dwYCountChars;
            public UInt32 dwFillAttribute;
            public UInt32 dwFlags;
            public UInt16 wShowWindow;
            public UInt16 cbReserved2;
            public IntPtr lpReserved2;
            public IntPtr hStdInput;
            public IntPtr hStdOutput;
            public IntPtr hStdError;
        }

        [StructLayout(LayoutKind.Sequential)]
        private struct PROCESS_INFORMATION
        {
            public IntPtr hProcess;
            public IntPtr hThread;
            public UInt32 dwProcessId;
            public UInt32 dwThreadId;
        }

        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        private static extern IntPtr CreateJobObjectW(IntPtr jobAttributes, String name);

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern Boolean SetInformationJobObject(
            IntPtr job,
            JOBOBJECTINFOCLASS informationClass,
            ref JOBOBJECT_EXTENDED_LIMIT_INFORMATION information,
            UInt32 informationLength);

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern Boolean QueryInformationJobObject(
            IntPtr job,
            JOBOBJECTINFOCLASS informationClass,
            out JOBOBJECT_EXTENDED_LIMIT_INFORMATION information,
            UInt32 informationLength,
            out UInt32 returnLength);

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern Boolean QueryInformationJobObject(
            IntPtr job,
            JOBOBJECTINFOCLASS informationClass,
            IntPtr information,
            UInt32 informationLength,
            out UInt32 returnLength);

        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern Boolean CreateProcessW(
            String applicationName,
            StringBuilder commandLine,
            IntPtr processAttributes,
            IntPtr threadAttributes,
            Boolean inheritHandles,
            UInt32 creationFlags,
            IntPtr environment,
            String currentDirectory,
            ref STARTUPINFO startupInfo,
            out PROCESS_INFORMATION processInformation);

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern Boolean AssignProcessToJobObject(IntPtr job, IntPtr process);

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern Boolean IsProcessInJob(
            IntPtr process,
            IntPtr job,
            [MarshalAs(UnmanagedType.Bool)] out Boolean result);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern IntPtr OpenProcess(
            UInt32 desiredAccess,
            [MarshalAs(UnmanagedType.Bool)] Boolean inheritHandle,
            UInt32 processId);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern UInt32 ResumeThread(IntPtr thread);

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern Boolean TerminateProcess(IntPtr process, UInt32 exitCode);

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern Boolean TerminateJobObject(IntPtr job, UInt32 exitCode);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern UInt32 WaitForSingleObject(IntPtr handle, UInt32 milliseconds);

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern Boolean GetExitCodeProcess(IntPtr process, out UInt32 exitCode);

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        internal static extern Boolean CloseHandle(IntPtr handle);

        private static Exception LastWin32Exception(String operation)
        {
            return new Win32Exception(Marshal.GetLastWin32Error(), operation);
        }

        private static UInt64 UIntPtrToUInt64(UIntPtr value)
        {
            return value.ToUInt64();
        }

        private static String QuoteArgument(String value)
        {
            if (value == null)
            {
                value = String.Empty;
            }
            if (value.Length > 0 && value.IndexOfAny(new Char[] { ' ', '\t', '\n', '\v', '"' }) < 0)
            {
                return value;
            }

            StringBuilder quoted = new StringBuilder();
            quoted.Append('"');
            Int32 backslashes = 0;
            foreach (Char character in value)
            {
                if (character == '\\')
                {
                    backslashes++;
                    continue;
                }
                if (character == '"')
                {
                    quoted.Append('\\', backslashes * 2 + 1);
                    quoted.Append('"');
                    backslashes = 0;
                    continue;
                }
                quoted.Append('\\', backslashes);
                backslashes = 0;
                quoted.Append(character);
            }
            quoted.Append('\\', backslashes * 2);
            quoted.Append('"');
            return quoted.ToString();
        }

        private static String BuildCommandLine(String applicationPath, String[] arguments)
        {
            StringBuilder commandLine = new StringBuilder(QuoteArgument(applicationPath));
            if (arguments != null)
            {
                foreach (String argument in arguments)
                {
                    commandLine.Append(' ');
                    commandLine.Append(QuoteArgument(argument));
                }
            }
            return commandLine.ToString();
        }

        public static IntPtr CreateVerifiedJob(UInt64 memoryLimitBytes)
        {
            if (IntPtr.Size != 8)
            {
                throw new PlatformNotSupportedException("A 64-bit process is required.");
            }
            if (memoryLimitBytes != 3221225472UL)
            {
                throw new ArgumentOutOfRangeException(
                    "memoryLimitBytes",
                    "The B04 guard accepts only the exact 3,221,225,472-byte cap.");
            }

            Int32 extendedSize = Marshal.SizeOf(
                typeof(JOBOBJECT_EXTENDED_LIMIT_INFORMATION));
            Int32 jobMemoryOffset = Marshal.OffsetOf(
                typeof(JOBOBJECT_EXTENDED_LIMIT_INFORMATION),
                "JobMemoryLimit").ToInt32();
            if (extendedSize != 144 || jobMemoryOffset != 120)
            {
                throw new InvalidOperationException(
                    String.Format(
                        "Unexpected x64 Job Object layout: size={0}, JobMemoryLimitOffset={1}.",
                        extendedSize,
                        jobMemoryOffset));
            }

            IntPtr job = CreateJobObjectW(IntPtr.Zero, null);
            if (job == IntPtr.Zero)
            {
                throw LastWin32Exception("CreateJobObjectW failed");
            }

            try
            {
                JOBOBJECT_EXTENDED_LIMIT_INFORMATION information =
                    new JOBOBJECT_EXTENDED_LIMIT_INFORMATION();
                information.BasicLimitInformation.LimitFlags = REQUIRED_LIMIT_FLAGS;
                information.JobMemoryLimit = new UIntPtr(memoryLimitBytes);
                UInt32 structureSize = (UInt32)Marshal.SizeOf(
                    typeof(JOBOBJECT_EXTENDED_LIMIT_INFORMATION));

                if (!SetInformationJobObject(
                    job,
                    JOBOBJECTINFOCLASS.JobObjectExtendedLimitInformation,
                    ref information,
                    structureSize))
                {
                    throw LastWin32Exception("SetInformationJobObject failed");
                }

                JobLimitSnapshot snapshot = ReadLimits(job);
                if (snapshot.LimitFlags != REQUIRED_LIMIT_FLAGS)
                {
                    throw new InvalidOperationException(
                        String.Format(
                            "Job limit flag readback mismatch: expected 0x{0:X8}, received 0x{1:X8}.",
                            REQUIRED_LIMIT_FLAGS,
                            snapshot.LimitFlags));
                }
                if ((snapshot.LimitFlags & BREAKAWAY_LIMIT_FLAGS) != 0)
                {
                    throw new InvalidOperationException("Job readback unexpectedly permits breakaway.");
                }
                if (snapshot.JobMemoryLimit != memoryLimitBytes)
                {
                    throw new InvalidOperationException(
                        String.Format(
                            "Job memory readback mismatch: expected {0}, received {1}.",
                            memoryLimitBytes,
                            snapshot.JobMemoryLimit));
                }
                return job;
            }
            catch
            {
                CloseHandle(job);
                throw;
            }
        }

        public static JobLimitSnapshot ReadLimits(IntPtr job)
        {
            JOBOBJECT_EXTENDED_LIMIT_INFORMATION information;
            UInt32 returnLength;
            UInt32 structureSize = (UInt32)Marshal.SizeOf(
                typeof(JOBOBJECT_EXTENDED_LIMIT_INFORMATION));
            if (!QueryInformationJobObject(
                job,
                JOBOBJECTINFOCLASS.JobObjectExtendedLimitInformation,
                out information,
                structureSize,
                out returnLength))
            {
                throw LastWin32Exception("QueryInformationJobObject limit readback failed");
            }

            return new JobLimitSnapshot
            {
                LimitFlags = information.BasicLimitInformation.LimitFlags,
                JobMemoryLimit = UIntPtrToUInt64(information.JobMemoryLimit),
                PeakJobMemoryUsed = UIntPtrToUInt64(information.PeakJobMemoryUsed)
            };
        }

        public static ChildProcessHandles CreateAssignedAndResume(
            IntPtr job,
            String applicationPath,
            String[] arguments,
            String workingDirectory)
        {
            STARTUPINFO startupInfo = new STARTUPINFO();
            startupInfo.cb = (UInt32)Marshal.SizeOf(typeof(STARTUPINFO));
            PROCESS_INFORMATION processInformation;
            StringBuilder commandLine = new StringBuilder(
                BuildCommandLine(applicationPath, arguments));
            UInt32 creationFlags =
                CREATE_SUSPENDED | CREATE_NO_WINDOW | CREATE_UNICODE_ENVIRONMENT;

            if (!CreateProcessW(
                applicationPath,
                commandLine,
                IntPtr.Zero,
                IntPtr.Zero,
                false,
                creationFlags,
                IntPtr.Zero,
                workingDirectory,
                ref startupInfo,
                out processInformation))
            {
                throw LastWin32Exception("CreateProcessW failed");
            }

            Boolean assignedToJob = false;
            try
            {
                if (!AssignProcessToJobObject(job, processInformation.hProcess))
                {
                    throw LastWin32Exception(
                        "AssignProcessToJobObject failed before child resume");
                }
                assignedToJob = true;

                Boolean isInJob;
                if (!IsProcessInJob(processInformation.hProcess, job, out isInJob))
                {
                    throw LastWin32Exception("IsProcessInJob verification failed");
                }
                if (!isInJob)
                {
                    throw new InvalidOperationException(
                        "The suspended child was not a member of the configured job.");
                }

                UInt32 resumeResult = ResumeThread(processInformation.hThread);
                if (resumeResult == UInt32.MaxValue)
                {
                    throw LastWin32Exception("ResumeThread failed");
                }
                if (resumeResult != 1U)
                {
                    throw new InvalidOperationException(
                        String.Format(
                            "ResumeThread returned an unexpected prior suspend count of {0}.",
                            resumeResult));
                }

                return new ChildProcessHandles(
                    processInformation.hProcess,
                    processInformation.hThread,
                    processInformation.dwProcessId);
            }
            catch
            {
                Boolean terminationSucceeded = assignedToJob
                    ? TerminateJobObject(job, 0xE0000001U)
                    : TerminateProcess(processInformation.hProcess, 0xE0000001U);
                if (!terminationSucceeded)
                {
                    throw LastWin32Exception(
                        assignedToJob
                            ? "TerminateJobObject failed after launch-path failure"
                            : "TerminateProcess failed for the unassigned suspended child");
                }
                UInt32 terminationWait = WaitForSingleObject(
                    processInformation.hProcess,
                    5000);
                if (terminationWait != WAIT_OBJECT_0)
                {
                    throw new InvalidOperationException(
                        String.Format(
                            "The failed launch did not terminate within the bounded wait; wait result 0x{0:X8}.",
                            terminationWait));
                }
                Boolean threadClosed = CloseHandle(processInformation.hThread);
                Boolean processClosed = CloseHandle(processInformation.hProcess);
                if (!threadClosed || !processClosed)
                {
                    throw LastWin32Exception("Closing failed-launch process handles failed");
                }
                throw;
            }
        }

        private static Int64[] GetJobProcessIds(IntPtr job)
        {
            Int32 capacity = 32;
            for (Int32 attempt = 0; attempt < 8; attempt++)
            {
                Int32 bufferSize = checked(8 + capacity * IntPtr.Size);
                IntPtr buffer = Marshal.AllocHGlobal(bufferSize);
                try
                {
                    for (Int32 offset = 0; offset < bufferSize; offset += 4)
                    {
                        Marshal.WriteInt32(buffer, offset, 0);
                    }

                    UInt32 returnLength;
                    Boolean succeeded = QueryInformationJobObject(
                        job,
                        JOBOBJECTINFOCLASS.JobObjectBasicProcessIdList,
                        buffer,
                        (UInt32)bufferSize,
                        out returnLength);
                    Int32 assigned = Marshal.ReadInt32(buffer, 0);
                    Int32 inList = Marshal.ReadInt32(buffer, 4);
                    if (assigned < 0 || inList < 0 || assigned > 4096 || inList > 4096)
                    {
                        throw new InvalidOperationException(
                            String.Format(
                                "Job process-list accounting is outside the bounded range: assigned={0}, listed={1}.",
                                assigned,
                                inList));
                    }
                    if (succeeded)
                    {
                        if (assigned != inList)
                        {
                            capacity = Math.Max(capacity * 2, assigned + 8);
                            continue;
                        }
                        Int64[] processIds = new Int64[inList];
                        HashSet<Int64> uniqueProcessIds = new HashSet<Int64>();
                        for (Int32 index = 0; index < inList; index++)
                        {
                            processIds[index] = Marshal.ReadIntPtr(
                                buffer,
                                8 + index * IntPtr.Size).ToInt64();
                            if (!uniqueProcessIds.Add(processIds[index]))
                            {
                                throw new InvalidOperationException(
                                    "The Job Object returned a duplicate process identifier.");
                            }
                        }
                        return processIds;
                    }

                    Int32 error = Marshal.GetLastWin32Error();
                    if (error != ERROR_MORE_DATA)
                    {
                        throw new Win32Exception(
                            error,
                            "QueryInformationJobObject process-list sampling failed");
                    }
                    capacity = Math.Max(capacity * 2, Math.Max(assigned, inList) + 8);
                }
                finally
                {
                    Marshal.FreeHGlobal(buffer);
                }
            }
            throw new InvalidOperationException("Job process list did not stabilize within eight bounded reads.");
        }

        public static PrivateMemorySample SampleAggregatePrivateBytes(IntPtr job)
        {
            Int64[] processIds = GetJobProcessIds(job);
            UInt64 total = 0;
            Int32 sampled = 0;
            foreach (Int64 processIdValue in processIds)
            {
                if (processIdValue <= 0 || processIdValue > Int32.MaxValue)
                {
                    throw new InvalidOperationException(
                        "Job reported a process identifier outside the supported range.");
                }

                try
                {
                    using (Process process = Process.GetProcessById((Int32)processIdValue))
                    {
                        process.Refresh();
                        Boolean isInJob;
                        if (!IsProcessInJob(process.Handle, job, out isInJob))
                        {
                            throw LastWin32Exception(
                                "IsProcessInJob failed during private-byte sampling");
                        }
                        if (!isInJob)
                        {
                            throw new InvalidOperationException(
                                "A sampled process identifier was not a member of the guarded job.");
                        }
                        Int64 privateBytes = process.PrivateMemorySize64;
                        if (privateBytes < 0)
                        {
                            throw new InvalidOperationException(
                                "A process reported negative private memory usage.");
                        }
                        total = checked(total + (UInt64)privateBytes);
                        sampled++;
                    }
                }
                catch (ArgumentException)
                {
                    if (IsProcessIdentifierLive((Int32)processIdValue))
                    {
                        throw;
                    }
                }
                catch (InvalidOperationException)
                {
                    if (IsProcessIdentifierLive((Int32)processIdValue))
                    {
                        throw;
                    }
                }
                catch (Win32Exception)
                {
                    if (IsProcessIdentifierLive((Int32)processIdValue))
                    {
                        throw;
                    }
                }
            }

            return new PrivateMemorySample
            {
                TotalPrivateBytes = total,
                ReportedProcessIds = processIds.Length,
                SampledProcesses = sampled,
                ProcessIds = processIds
            };
        }

        public static Int32 GetActiveProcessCount(IntPtr job)
        {
            return GetJobProcessIds(job).Length;
        }

        private static Boolean IsProcessIdentifierLive(Int32 processId)
        {
            IntPtr process = OpenProcess(
                PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE,
                false,
                (UInt32)processId);
            if (process == IntPtr.Zero)
            {
                Int32 error = Marshal.GetLastWin32Error();
                if (error == ERROR_INVALID_PARAMETER)
                {
                    return false;
                }
                throw new Win32Exception(
                    error,
                    "OpenProcess failed while resolving a private-byte sampling race");
            }

            try
            {
                UInt32 waitResult = WaitForSingleObject(
                    process,
                    PRIVATE_MEMORY_EXIT_RACE_WAIT_MILLISECONDS);
                if (waitResult == WAIT_OBJECT_0)
                {
                    return false;
                }
                if (waitResult == WAIT_TIMEOUT)
                {
                    return true;
                }
                throw LastWin32Exception(
                    "WaitForSingleObject failed while resolving a private-byte sampling race");
            }
            finally
            {
                if (!CloseHandle(process))
                {
                    throw LastWin32Exception(
                        "CloseHandle failed while resolving a private-byte sampling race");
                }
            }
        }

        public static Boolean IsForeignLiveProcess(IntPtr job, Int32 processId)
        {
            if (processId <= 0)
            {
                throw new ArgumentOutOfRangeException("processId");
            }

            IntPtr process = OpenProcess(
                PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE,
                false,
                (UInt32)processId);
            if (process == IntPtr.Zero)
            {
                Int32 error = Marshal.GetLastWin32Error();
                if (error == ERROR_INVALID_PARAMETER)
                {
                    // The enumerated process exited before its handle could be opened.
                    return false;
                }
                throw new Win32Exception(
                    error,
                    "OpenProcess failed during foreign-process membership verification");
            }

            try
            {
                if (IsProcessSignaled(process))
                {
                    return false;
                }

                Boolean isInJob;
                if (!IsProcessInJob(process, job, out isInJob))
                {
                    throw LastWin32Exception(
                        "IsProcessInJob failed during foreign-process membership verification");
                }

                // Query the opened process object, never a historical PID membership cache.
                return !isInJob && !IsProcessSignaled(process);
            }
            finally
            {
                if (!CloseHandle(process))
                {
                    throw LastWin32Exception(
                        "CloseHandle failed after foreign-process membership verification");
                }
            }
        }

        public static Boolean IsProcessSignaled(IntPtr process)
        {
            UInt32 waitResult = WaitForSingleObject(process, 0);
            if (waitResult == WAIT_OBJECT_0)
            {
                return true;
            }
            if (waitResult == WAIT_TIMEOUT)
            {
                return false;
            }
            throw LastWin32Exception("WaitForSingleObject failed");
        }

        public static UInt32 GetProcessExitCode(IntPtr process)
        {
            UInt32 exitCode;
            if (!GetExitCodeProcess(process, out exitCode))
            {
                throw LastWin32Exception("GetExitCodeProcess failed");
            }
            return exitCode;
        }

        public static void TerminateCapturedJob(IntPtr job, UInt32 exitCode)
        {
            if (!TerminateJobObject(job, exitCode))
            {
                throw LastWin32Exception("TerminateJobObject failed");
            }
        }

        public static void WaitAfterTermination(IntPtr process, UInt32 milliseconds)
        {
            UInt32 waitResult = WaitForSingleObject(process, milliseconds);
            if (waitResult == WAIT_TIMEOUT)
            {
                throw new InvalidOperationException(
                    "The guarded root did not terminate within the bounded wait.");
            }
            if (waitResult != WAIT_OBJECT_0)
            {
                throw LastWin32Exception("Post-termination wait failed");
            }
        }

        public static void CloseJob(IntPtr job)
        {
            if (job != IntPtr.Zero && !CloseHandle(job))
            {
                throw LastWin32Exception("CloseHandle(job) failed");
            }
        }
    }
}
'@

    Add-Type -TypeDefinition $nativeSource -Language CSharp -ErrorAction Stop
}

$startedUtc = [DateTimeOffset]::UtcNow
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$job = [IntPtr]::Zero
$child = $null
$processId = $null
$exitCode = $null
$sampledPeakPrivateBytes = [UInt64] 0
$jobPeakMemoryUsedBytes = [UInt64] 0
$readbackFlags = $null
$readbackMemoryLimitBytes = $null
$capTriggered = $false
$treeTerminated = $false
$foreignProcessEvidence = @()
$finalActiveProcessCount = $null
$status = 'GUARD_INITIALIZATION_FAILED'
$terminalError = $null
$cleanupErrors = [System.Collections.Generic.List[string]]::new()

try {
    foreach ($temporaryVariable in $nativeTemporaryEnvironment.Keys) {
        [System.Environment]::SetEnvironmentVariable(
            $temporaryVariable,
            $nativeTemporaryEnvironment[$temporaryVariable],
            [System.EnvironmentVariableTarget]::Process
        )
    }
    $preexistingTexProcesses = @(
        Get-Process -ErrorAction Stop |
            Where-Object { $blockedProcessNames.Contains($_.ProcessName) } |
            ForEach-Object {
                [pscustomobject]@{
                    process_name = $_.ProcessName
                    process_id = $_.Id
                }
            }
    )
    if ($preexistingTexProcesses.Count -ne 0) {
        $foreignProcessEvidence = $preexistingTexProcesses
        $status = 'OVERLAPPING_TEX_PROCESS_REJECTED'
        throw 'A TeX/BibTeX process already exists; refusing to create a guarded child.'
    }

    $job = [B04JobGuard.Native]::CreateVerifiedJob($MemoryLimitBytes)
    $initialSnapshot = [B04JobGuard.Native]::ReadLimits($job)
    $readbackFlags = [UInt32] $initialSnapshot.LimitFlags
    $readbackMemoryLimitBytes = [UInt64] $initialSnapshot.JobMemoryLimit

    if ($readbackFlags -ne $RequiredLimitFlags) {
        throw "PowerShell readback rejected limit flags 0x$($readbackFlags.ToString('X8'))."
    }
    if (($readbackFlags -band $BreakawayLimitFlags) -ne 0) {
        throw 'PowerShell readback detected a prohibited breakaway flag.'
    }
    if ($readbackMemoryLimitBytes -ne $MemoryLimitBytes) {
        throw "PowerShell readback rejected job memory limit $readbackMemoryLimitBytes."
    }

    $child = [B04JobGuard.Native]::CreateAssignedAndResume(
        $job,
        $nativeExecutable,
        $nativeArguments.ToArray(),
        $nativeWorkingDirectory
    )
    $processId = [UInt32] $child.ProcessId
    $status = 'RUNNING'

    while ($true) {
        try {
            $sample = [B04JobGuard.Native]::SampleAggregatePrivateBytes($job)
            $aggregatePrivateBytes = [UInt64] $sample.TotalPrivateBytes
            if ($aggregatePrivateBytes -gt $sampledPeakPrivateBytes) {
                $sampledPeakPrivateBytes = $aggregatePrivateBytes
            }

            $foreignProcesses = @(
                Get-Process -ErrorAction Stop |
                    Where-Object {
                        $blockedProcessNames.Contains($_.ProcessName) -and
                        [B04JobGuard.Native]::IsForeignLiveProcess($job, $_.Id)
                    } |
                    ForEach-Object {
                        [pscustomobject]@{
                            process_name = $_.ProcessName
                            process_id = $_.Id
                        }
                    }
            )
            if ($foreignProcesses.Count -ne 0) {
                $foreignProcessEvidence = $foreignProcesses
                $status = 'FOREIGN_TEX_PROCESS_DETECTED'
                throw 'A TeX/BibTeX process outside the captured Job Object appeared during the guarded command.'
            }

            $snapshot = [B04JobGuard.Native]::ReadLimits($job)
            $observedJobPeak = [UInt64] $snapshot.PeakJobMemoryUsed
            if ($observedJobPeak -gt $jobPeakMemoryUsedBytes) {
                $jobPeakMemoryUsedBytes = $observedJobPeak
            }

            if (
                $aggregatePrivateBytes -ge $MemoryLimitBytes -or
                $observedJobPeak -ge $MemoryLimitBytes
            ) {
                $capTriggered = $true
                $status = 'MEMORY_LIMIT_TRIGGERED'
                throw "Aggregate private-byte cap reached: sampled=$aggregatePrivateBytes, job_peak=$observedJobPeak, cap=$MemoryLimitBytes."
            }

            $rootExited = [B04JobGuard.Native]::IsProcessSignaled($child.ProcessHandle)
            if (-not $rootExited -and $sample.ReportedProcessIds -eq 0) {
                $status = 'ACCOUNTING_FAILURE'
                throw 'The root process is live but the job reports no captured process identifiers.'
            }

            if ($rootExited -and $null -eq $exitCode) {
                $exitCode = [UInt32] [B04JobGuard.Native]::GetProcessExitCode(
                    $child.ProcessHandle
                )
                if ($exitCode -ne 0) {
                    $status = 'PROCESS_EXIT_NONZERO'
                    throw "Guarded root process exited with code $exitCode."
                }
            }

            if ($rootExited -and $sample.ReportedProcessIds -eq 0) {
                break
            }

            if ($stopwatch.Elapsed.TotalSeconds -ge $TimeoutSeconds) {
                $status = 'TIMEOUT'
                throw "Guarded process tree exceeded the bounded timeout of $TimeoutSeconds seconds."
            }
        }
        catch {
            if ($status -eq 'RUNNING') {
                $status = 'SAMPLING_OR_WATCHER_FAILURE'
            }
            throw
        }

        Start-Sleep -Milliseconds $PollMilliseconds
    }

    if ($exitCode -eq 0) {
        $status = 'SUCCEEDED'
    }
    else {
        $status = 'PROCESS_EXIT_NONZERO'
        $terminalError = "Guarded process exited with code $exitCode."
    }
}
catch {
    $terminalError = $_.Exception.Message
    if ($job -ne [IntPtr]::Zero) {
        try {
            [B04JobGuard.Native]::TerminateCapturedJob($job, $TerminationExitCode)
        }
        catch {
            $cleanupErrors.Add($_.Exception.Message)
        }
        if ($null -ne $child) {
            try {
                [B04JobGuard.Native]::WaitAfterTermination($child.ProcessHandle, 5000)
            }
            catch {
                $cleanupErrors.Add($_.Exception.Message)
            }
        }
        try {
            for ($terminationPoll = 0; $terminationPoll -lt 50; $terminationPoll++) {
                $finalActiveProcessCount = [B04JobGuard.Native]::GetActiveProcessCount($job)
                if ($finalActiveProcessCount -eq 0) {
                    break
                }
                Start-Sleep -Milliseconds 100
            }
            if ($finalActiveProcessCount -ne 0) {
                throw "Captured Job Object still reports $finalActiveProcessCount active processes after termination."
            }
            $treeTerminated = $true
        }
        catch {
            $cleanupErrors.Add($_.Exception.Message)
        }
    }
}
finally {
    $stopwatch.Stop()
    if ($job -ne [IntPtr]::Zero) {
        try {
            $finalSnapshot = [B04JobGuard.Native]::ReadLimits($job)
            $finalActiveProcessCount = [B04JobGuard.Native]::GetActiveProcessCount($job)
            $finalJobPeak = [UInt64] $finalSnapshot.PeakJobMemoryUsed
            if ($finalJobPeak -gt $jobPeakMemoryUsedBytes) {
                $jobPeakMemoryUsedBytes = $finalJobPeak
            }
            if ($finalActiveProcessCount -ne 0 -and $null -eq $terminalError) {
                throw "Guard completion left $finalActiveProcessCount active captured processes."
            }
        }
        catch {
            $cleanupErrors.Add($_.Exception.Message)
            if ($null -eq $terminalError) {
                $status = 'FINAL_ACCOUNTING_FAILURE'
                $terminalError = $_.Exception.Message
                try {
                    [B04JobGuard.Native]::TerminateCapturedJob($job, $TerminationExitCode)
                    $treeTerminated = $true
                }
                catch {
                    $cleanupErrors.Add($_.Exception.Message)
                }
            }
        }
    }

    if ($null -ne $child) {
        $child.Dispose()
    }
    if ($job -ne [IntPtr]::Zero) {
        try {
            [B04JobGuard.Native]::CloseJob($job)
        }
        catch {
            $cleanupErrors.Add($_.Exception.Message)
            if ($null -eq $terminalError) {
                $status = 'JOB_CLOSE_FAILURE'
                $terminalError = $_.Exception.Message
            }
        }
    }
    foreach ($temporaryVariable in $temporaryEnvironment.Keys) {
        [System.Environment]::SetEnvironmentVariable(
            $temporaryVariable,
            $temporaryEnvironment[$temporaryVariable],
            [System.EnvironmentVariableTarget]::Process
        )
    }
}

$finishedUtc = [DateTimeOffset]::UtcNow
$receipt = [ordered]@{
    schema = 'ega_iii_1_vi_b04_guarded_process_v1'
    started_utc = $startedUtc.ToString('o')
    finished_utc = $finishedUtc.ToString('o')
    duration_milliseconds = [Int64] [Math]::Round($stopwatch.Elapsed.TotalMilliseconds)
    status = $status
    executable = $resolvedExecutable
    arguments = [string[]] $ArgumentList
    working_directory = $resolvedWorkingDirectory
    native_working_directory = $nativeWorkingDirectory
    native_executable = $nativeExecutable
    native_arguments = $nativeArguments.ToArray()
    path_mode = 'verified_existing_ntfs_short_names'
    canonical_phase_root = $phaseRoot
    native_phase_root = $nativePhaseRoot
    process_id = $processId
    exit_code = $exitCode
    memory_limit_bytes = $MemoryLimitBytes
    memory_limit_hex = '0x00000000C0000000'
    required_limit_flags_hex = '0x00002200'
    readback_limit_flags_hex = if ($null -eq $readbackFlags) {
        $null
    }
    else {
        '0x{0:X8}' -f $readbackFlags
    }
    readback_memory_limit_bytes = $readbackMemoryLimitBytes
    sampled_peak_private_bytes = $sampledPeakPrivateBytes
    peak_job_memory_used_bytes = $jobPeakMemoryUsedBytes
    cap_triggered = $capTriggered
    captured_tree_terminated = $treeTerminated
    final_active_processes = $finalActiveProcessCount
    foreign_tex_processes = @($foreignProcessEvidence)
    timeout_seconds = $TimeoutSeconds
    poll_milliseconds = $PollMilliseconds
    error = $terminalError
    cleanup_errors = [string[]] $cleanupErrors
}

$receiptJson = $receipt | ConvertTo-Json -Depth 6
$utf8WithoutBom = [System.Text.UTF8Encoding]::new($false)
$receiptTemporaryPath = $resolvedReceiptPath + '.tmp-' + $PID
try {
    if (Test-Path -LiteralPath $receiptTemporaryPath) {
        throw "Receipt temporary path unexpectedly exists: $receiptTemporaryPath"
    }
    [byte[]] $receiptBytes = $utf8WithoutBom.GetBytes(
        $receiptJson + [Environment]::NewLine
    )
    $receiptStream = [System.IO.FileStream]::new(
        $receiptTemporaryPath,
        [System.IO.FileMode]::CreateNew,
        [System.IO.FileAccess]::Write,
        [System.IO.FileShare]::None
    )
    try {
        $receiptStream.Write($receiptBytes, 0, $receiptBytes.Length)
        $receiptStream.Flush($true)
    }
    finally {
        $receiptStream.Dispose()
    }
    [System.IO.File]::Move($receiptTemporaryPath, $resolvedReceiptPath)
    [void] (
        Get-Content -LiteralPath $resolvedReceiptPath -Raw -ErrorAction Stop |
            ConvertFrom-Json -ErrorAction Stop
    )
}
catch {
    if (Test-Path -LiteralPath $receiptTemporaryPath) {
        [System.IO.File]::Delete($receiptTemporaryPath)
    }
    throw "Unable to write the guarded-process receipt '$resolvedReceiptPath': $($_.Exception.Message)"
}

if ($null -ne $terminalError) {
    throw $terminalError
}
if ($cleanupErrors.Count -ne 0) {
    throw "Guard cleanup reported errors; inspect $resolvedReceiptPath."
}

[pscustomobject] $receipt

