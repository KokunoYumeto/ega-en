$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceRoot = Join-Path $repoRoot 'source'
$outputRoot = Join-Path $PSScriptRoot 'out'
$readerRoot = Join-Path $repoRoot 'reader'

$env:SOURCE_DATE_EPOCH = '1787356800'
$env:FORCE_SOURCE_DATE = '1'
$env:TZ = 'UTC'
$env:BIBINPUTS = "$sourceRoot;"

$readers = @(
    [pscustomobject]@{ Driver = 'EGA_English_Global_0_IV'; PublicName = '00_EGA_EN_COMPLETE_LINKED_READER.pdf' },
    [pscustomobject]@{ Driver = 'EGA_III2_EN'; PublicName = 'EGA_III2_English_Standalone_Reader.pdf' },
    [pscustomobject]@{ Driver = 'EGA_IV1_EN'; PublicName = 'EGA_IV1_English_Standalone_Reader.pdf' },
    [pscustomobject]@{ Driver = 'EGA_IV3_EN'; PublicName = 'EGA_IV3_English_Standalone_Reader.pdf' },
    [pscustomobject]@{ Driver = 'EGA_IV4_EN'; PublicName = 'EGA_IV4_English_Standalone_Reader.pdf' }
)

New-Item -ItemType Directory -Force -Path $outputRoot, $readerRoot | Out-Null
$outputRootFull = [IO.Path]::GetFullPath($outputRoot).TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar

function Invoke-EGAReaderBuild {
    param(
        [Parameter(Mandatory = $true)][string]$Driver,
        [Parameter(Mandatory = $true)][string]$PublicName
    )

    $driverPath = Join-Path $sourceRoot "$Driver.tex"
    if (-not (Test-Path -LiteralPath $driverPath)) {
        throw "Missing reader driver: $driverPath"
    }

    $jobRoot = Join-Path $outputRoot $Driver
    $jobRootFull = [IO.Path]::GetFullPath($jobRoot).TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    if (-not $jobRootFull.StartsWith($outputRootFull, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to clear build path outside the repository output directory: $jobRootFull"
    }
    if (Test-Path -LiteralPath $jobRoot) {
        Remove-Item -LiteralPath $jobRoot -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path $jobRoot | Out-Null

    Push-Location $sourceRoot
    try {
        & pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory $jobRoot "$Driver.tex"
        if ($LASTEXITCODE -ne 0) { throw "$Driver initial pdfLaTeX pass failed with exit code $LASTEXITCODE" }
        Push-Location $jobRoot
        try {
            & bibtex $Driver
            if ($LASTEXITCODE -ne 0) { throw "$Driver BibTeX pass failed with exit code $LASTEXITCODE" }
        } finally {
            Pop-Location
        }
        2..5 | ForEach-Object {
            & pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory $jobRoot "$Driver.tex"
            if ($LASTEXITCODE -ne 0) { throw "$Driver pdfLaTeX pass $_ failed with exit code $LASTEXITCODE" }
        }
    } finally {
        Pop-Location
    }

    $builtPdf = Join-Path $jobRoot "$Driver.pdf"
    if (-not (Test-Path -LiteralPath $builtPdf)) {
        throw "Expected reader PDF was not produced: $builtPdf"
    }
    $publicPdf = Join-Path $readerRoot $PublicName
    Copy-Item -LiteralPath $builtPdf -Destination $publicPdf -Force
    $item = Get-Item -LiteralPath $publicPdf
    $hash = Get-FileHash -Algorithm SHA256 -LiteralPath $publicPdf
    [pscustomobject]@{
        Path = $item.FullName
        Bytes = $item.Length
        SHA256 = $hash.Hash
    }
}

$readers | ForEach-Object {
    Invoke-EGAReaderBuild -Driver $_.Driver -PublicName $_.PublicName
}
