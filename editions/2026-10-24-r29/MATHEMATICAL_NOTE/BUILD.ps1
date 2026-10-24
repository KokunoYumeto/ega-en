param(
 [Parameter(Mandatory=$true)][string]$PdfLatex,
 [Parameter(Mandatory=$true)][string]$BibTeX,
 [ValidateSet('native','direct')][string]$SourceForm='native',
 [string]$OutputDirectory=(Join-Path $PSScriptRoot 'build_output'),
 [string]$ReusePrimaryDirectory='' 
)
$ErrorActionPreference='Stop'
$utf8=[Text.UTF8Encoding]::new($false)
$packageRoot=[IO.Path]::GetFullPath($PSScriptRoot)
$outputRoot=[IO.Path]::GetFullPath($OutputDirectory)
if(Test-Path -LiteralPath $outputRoot){throw 'Use a new output directory; prior results are not overwritten.'}
$engine=(Get-Item -LiteralPath $PdfLatex).FullName
$bib=(Get-Item -LiteralPath $BibTeX).FullName
$manifest=Get-Content -LiteralPath (Join-Path $packageRoot 'MANIFEST.json') -Raw|ConvertFrom-Json
$config=Get-Content -LiteralPath (Join-Path $packageRoot 'BUILD_CONFIG.json') -Raw|ConvertFrom-Json
if($config.private_bytes_cap -ne 3221225472 -or $config.tex_mutex -ne 'Global\InterlanguageTeXSlotV1'){throw 'Invalid safety configuration'}
foreach($entry in $manifest.files){
 $path=Join-Path $packageRoot $entry.path
 if((Get-Item -LiteralPath $path).Length -ne $entry.bytes -or (Get-FileHash -LiteralPath $path).Hash -ne $entry.sha256){throw "Source identity mismatch: $($entry.path)"}
}
$guard=Join-Path $packageRoot 'build_support/run_guarded_process.ps1'
$job=$config.job_name
$body=if($SourceForm -eq 'native'){$config.native_master}else{$config.direct_master}
$owned=$false;$abandoned=$false;$failure=$null;$passes=@();$saved=@{}
$mutex=[Threading.Mutex]::new($false,'Global\InterlanguageTeXSlotV1')
foreach($v in 'TEMP','TMP','SOURCE_DATE_EPOCH','FORCE_SOURCE_DATE','TZ','MIKTEX_ENABLE_INSTALLER'){$saved[$v]=[Environment]::GetEnvironmentVariable($v,'Process')}
[IO.Directory]::CreateDirectory($outputRoot)|Out-Null
$tempDir=Join-Path $outputRoot 'tmp';[IO.Directory]::CreateDirectory($tempDir)|Out-Null
$env:TEMP=$tempDir;$env:TMP=$tempDir;$env:SOURCE_DATE_EPOCH=[string]$config.source_date_epoch;$env:FORCE_SOURCE_DATE='1';$env:TZ='UTC';$env:MIKTEX_ENABLE_INSTALLER='0'
try{
 try{$owned=$mutex.WaitOne(1000)}catch [Threading.AbandonedMutexException]{$owned=$true;$abandoned=$true}
 if(-not $owned){throw 'TeX mutex unavailable; no engine launched.'}

 $editions=@('primary','replay')
 if($ReusePrimaryDirectory){
  $prior=[IO.Path]::GetFullPath($ReusePrimaryDirectory)
  if(-not (Test-Path -LiteralPath $prior -PathType Container)){throw 'Missing reusable primary'}
  $priorResult=Get-Content -LiteralPath (Join-Path (Split-Path -Parent $prior) 'BUILD_RESULT.json') -Raw|ConvertFrom-Json
  if($priorResult.source_form -ne $SourceForm -or $priorResult.job_name -ne $job -or -not $priorResult.acquired){throw 'Reusable build scope mismatch'}
  foreach($entry in $manifest.files|Where-Object{$_.path.StartsWith("$SourceForm/")}){
   $p=Join-Path $prior $entry.path.Substring($SourceForm.Length+1)
   if((Get-Item -LiteralPath $p).Length -ne $entry.bytes -or (Get-FileHash -LiteralPath $p).Hash -ne $entry.sha256){throw 'Reusable source mismatch'}
  }
  $expectedWrapper="\pdfinfoomitdate=1`n\pdftrailerid{}`n\pdfsuppressptexinfo=15`n\input{$body}`n"
  if([IO.File]::ReadAllText((Join-Path $prior 'build_entry.tex')) -cne $expectedWrapper){throw 'Reusable wrapper mismatch'}
  $expectedArguments=@('-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder',"-jobname=$job",'build_entry.tex')
  $copyNames=@("$job.pdf","$job.log",'pass5.pdf')
  foreach($pass in 1..6){
   $gp=Join-Path $prior "pass$pass.guard.json"
   $g=Get-Content -LiteralPath $gp -Raw|ConvertFrom-Json
   if($g.status -ne 'SUCCEEDED' -or $g.exit_code -ne 0 -or $g.cap_triggered -or $g.final_active_processes -ne 0 -or $g.memory_limit_bytes -ne 3221225472 -or $g.executable -ne $engine -or $g.working_directory -ne $prior -or ($g.arguments -join "`n") -cne ($expectedArguments -join "`n")){throw 'Reusable guarded pass mismatch'}
   $passes+=@{edition='primary';pass=$pass;peak_bytes=$g.peak_job_memory_used_bytes;adopted=$true;receipt=$gp}
   $copyNames+="pass$pass.guard.json"
  }
  if([IO.File]::ReadAllText((Join-Path $prior "$job.aux")).Contains('\bibdata')){
   $g=Get-Content -LiteralPath (Join-Path $prior 'bibtex.guard.json') -Raw|ConvertFrom-Json
   if($g.status -ne 'SUCCEEDED' -or $g.exit_code -ne 0 -or $g.cap_triggered -or $g.final_active_processes -ne 0 -or $g.memory_limit_bytes -ne 3221225472 -or $g.executable -ne $bib -or $g.working_directory -ne $prior -or ($g.arguments -join '') -cne $job){throw 'Reusable BibTeX mismatch'}
   $copyNames+='bibtex.guard.json'
  }
  $oldLog=[IO.File]::ReadAllText((Join-Path $prior "$job.log"))
  if($oldLog -match '(?im)pdfTeX warning \(dest\)|^Missing character:|undefined references|Reference .+ undefined|Citation .+ undefined|Rerun to get cross-references right|multiply[- ]defined labels|^![ \t]*\S' -or $oldLog -notmatch 'Output written on'){throw 'Reusable log failure'}
  if((Get-FileHash -LiteralPath (Join-Path $prior "$job.pdf")).Hash -ne (Get-FileHash -LiteralPath (Join-Path $prior 'pass5.pdf')).Hash){throw 'Reusable pass 5/6 instability'}
  $destination=Join-Path $outputRoot 'primary';[IO.Directory]::CreateDirectory($destination)|Out-Null
  $adopted=@()
  foreach($name in $copyNames){
   $p=Join-Path $prior $name;$h=(Get-FileHash -LiteralPath $p).Hash;$target=Join-Path $destination $name
   [IO.File]::Copy($p,$target,$false)
   if((Get-FileHash -LiteralPath $target).Hash -ne $h -or (Get-FileHash -LiteralPath $p).Hash -ne $h){throw 'Reusable artifact changed'}
   $adopted+=@{name=$name;bytes=(Get-Item -LiteralPath $target).Length;sha256=$h}
  }
  [IO.File]::WriteAllText((Join-Path $destination 'ADOPTED_PRIMARY.json'),(@{source=$prior;artifacts=$adopted;independent_replay_pending=$true}|ConvertTo-Json -Depth 6)+"`n",$utf8)
  $editions=@('replay')
 }
 foreach($edition in $editions){
  $work=Join-Path $outputRoot $edition
  foreach($entry in $manifest.files|Where-Object{$_.path.StartsWith("$SourceForm/")}){
   $relative=$entry.path.Substring($SourceForm.Length+1);$destination=Join-Path $work $relative
   [IO.Directory]::CreateDirectory((Split-Path -Parent $destination))|Out-Null
   [IO.File]::Copy((Join-Path $packageRoot $entry.path),$destination,$false)
  }
  $wrapper="\pdfinfoomitdate=1`n\pdftrailerid{}`n\pdfsuppressptexinfo=15`n\input{$body}`n"
  [IO.File]::WriteAllText((Join-Path $work 'build_entry.tex'),$wrapper,$utf8)
  foreach($pass in 1..6){
   $receipt=Join-Path $work "pass$pass.guard.json"
   & $guard -FilePath $engine -ArgumentList @('-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder',"-jobname=$job",'build_entry.tex') -WorkingDirectory $work -TaskRoot $outputRoot -ReceiptPath $receipt -TimeoutSeconds 1200|Out-Null
   $g=Get-Content -LiteralPath $receipt -Raw|ConvertFrom-Json
   if($g.status -ne 'SUCCEEDED' -or $g.cap_triggered -or $g.final_active_processes -ne 0 -or $g.memory_limit_bytes -ne 3221225472){throw 'Captured-process guard failure'}
   $passes+=@{edition=$edition;pass=$pass;peak_bytes=$g.peak_job_memory_used_bytes}
   if($pass -eq 1 -and [IO.File]::ReadAllText((Join-Path $work "$job.aux")).Contains('\bibdata')){
    $receipt=Join-Path $work 'bibtex.guard.json'
    & $guard -FilePath $bib -ArgumentList @($job) -WorkingDirectory $work -TaskRoot $outputRoot -ReceiptPath $receipt -TimeoutSeconds 300|Out-Null
    $g=Get-Content -LiteralPath $receipt -Raw|ConvertFrom-Json
    if($g.status -ne 'SUCCEEDED' -or $g.cap_triggered -or $g.final_active_processes -ne 0 -or $g.memory_limit_bytes -ne 3221225472){throw 'Captured BibTeX guard failure'}
    $passes+=@{edition=$edition;pass='bibtex';peak_bytes=$g.peak_job_memory_used_bytes}
   }
   if($pass -eq 5){[IO.File]::Copy((Join-Path $work "$job.pdf"),(Join-Path $work 'pass5.pdf'),$false)}
  }
  $log=[IO.File]::ReadAllText((Join-Path $work "$job.log"))
  if($log -match '(?im)pdfTeX warning \(dest\)|^Missing character:|undefined references|Reference .+ undefined|Citation .+ undefined|Rerun to get cross-references right|multiply[- ]defined labels|^![ \t]*\S'){throw "Terminal log failure: $edition"}
  if((Get-FileHash -LiteralPath (Join-Path $work "$job.pdf")).Hash -ne (Get-FileHash -LiteralPath (Join-Path $work 'pass5.pdf')).Hash){throw "Pass 5/6 instability: $edition"}
 }
 if((Get-FileHash -LiteralPath (Join-Path $outputRoot "primary/$job.pdf")).Hash -ne (Get-FileHash -LiteralPath (Join-Path $outputRoot "replay/$job.pdf")).Hash){throw 'Replay bytes differ'}
}catch{$failure=$_.Exception.Message}
finally{
 if($owned){$mutex.ReleaseMutex()};$mutex.Dispose()
 foreach($v in $saved.Keys){[Environment]::SetEnvironmentVariable($v,$saved[$v],'Process')}
 $result=@{source_form=$SourceForm;job_name=$job;acquired=$owned;abandoned=$abandoned;passes=$passes;error=$failure;reader_qa='REQUIRES_SEPARATE_CONTENT_LINK_AND_VISUAL_CHECKS'}
 [IO.File]::WriteAllText((Join-Path $outputRoot 'BUILD_RESULT.json'),($result|ConvertTo-Json -Depth 6)+"`n",$utf8)
}
if($failure){throw $failure}
Write-Output 'Deterministic build passed; content/link/visual release checks remain separate.'
