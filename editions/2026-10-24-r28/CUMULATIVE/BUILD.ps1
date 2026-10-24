param(
 [Parameter(Mandatory=$true)][string]$PdfLatex,
 [Parameter(Mandatory=$true)][string]$BibTeX,
 [ValidateSet('native','direct')][string]$SourceForm='native',
 [string]$OutputDirectory=(Join-Path $PSScriptRoot 'build_output')
)
$ErrorActionPreference='Stop'
$utf8=[Text.UTF8Encoding]::new($false)
$packageRoot=[IO.Path]::GetFullPath($PSScriptRoot)
$outputRoot=[IO.Path]::GetFullPath($OutputDirectory)
if(Test-Path -LiteralPath $outputRoot){throw 'Use a new output directory; prior results are not overwritten.'}
$engine=(Get-Item -LiteralPath $PdfLatex).FullName
$bib=(Get-Item -LiteralPath $BibTeX).FullName
$manifest=Get-Content -LiteralPath (Join-Path $packageRoot 'MANIFEST.json') -Raw|ConvertFrom-Json
foreach($entry in $manifest.files){
 $path=Join-Path $packageRoot $entry.path
 $item=Get-Item -LiteralPath $path
 if($item.Length -ne $entry.bytes -or (Get-FileHash -LiteralPath $path).Hash -ne $entry.sha256){throw "Source identity mismatch: $($entry.path)"}
}
$guard=Join-Path $packageRoot 'build_support/run_guarded_process.ps1'
$job='EGA_English_Global_0_IV'
$body=if($SourceForm -eq 'native'){'EGA_English_Global_0_IV.tex'}else{'00_EGA_EN_CUMULATIVE.tex'}
$owned=$false;$abandoned=$false;$failure=$null;$passes=@();$saved=@{}
$mutex=[Threading.Mutex]::new($false,'Global\InterlanguageTeXSlotV1')
foreach($v in 'TEMP','TMP','SOURCE_DATE_EPOCH','FORCE_SOURCE_DATE','TZ','MIKTEX_ENABLE_INSTALLER'){$saved[$v]=[Environment]::GetEnvironmentVariable($v,'Process')}
[IO.Directory]::CreateDirectory($outputRoot)|Out-Null
$tempDir=Join-Path $outputRoot 'tmp'
[IO.Directory]::CreateDirectory($tempDir)|Out-Null
$env:TEMP=$tempDir;$env:TMP=$tempDir;$env:SOURCE_DATE_EPOCH='1790294400';$env:FORCE_SOURCE_DATE='1';$env:TZ='UTC';$env:MIKTEX_ENABLE_INSTALLER='0'
try{
 try{$owned=$mutex.WaitOne(1000)}catch [Threading.AbandonedMutexException]{$owned=$true;$abandoned=$true}
 if(-not $owned){throw 'TeX mutex unavailable; no engine launched.'}
 foreach($edition in 'primary','replay'){
  $work=Join-Path $outputRoot $edition
  foreach($entry in $manifest.files|Where-Object{$_.path.StartsWith("$SourceForm/")}){
   $relative=$entry.path.Substring($SourceForm.Length+1)
   $destination=Join-Path $work $relative
   [IO.Directory]::CreateDirectory((Split-Path -Parent $destination))|Out-Null
   [IO.File]::Copy((Join-Path $packageRoot $entry.path),$destination,$false)
  }
  $wrapper="\pdfinfoomitdate=1`n\pdftrailerid{}`n\pdfsuppressptexinfo=15`n\input{$body}`n"
  [IO.File]::WriteAllText((Join-Path $work 'build_entry.tex'),$wrapper,$utf8)
  foreach($pass in 1..6){
   $receipt=Join-Path $work "pass$pass.guard.json"
   & $guard -FilePath $engine -ArgumentList @('-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder',"-jobname=$job",'build_entry.tex') -WorkingDirectory $work -ReceiptPath $receipt -TimeoutSeconds 1200|Out-Null
   $g=Get-Content -LiteralPath $receipt -Raw|ConvertFrom-Json
   if($g.status -ne 'SUCCEEDED' -or $g.cap_triggered -or $g.final_active_processes -ne 0 -or $g.memory_limit_bytes -ne 3221225472){throw 'Captured-process guard failure'}
   $passes+=@{edition=$edition;pass=$pass;peak_bytes=$g.peak_job_memory_used_bytes}
   if($pass -eq 1){
    $receipt=Join-Path $work 'bibtex.guard.json'
    & $guard -FilePath $bib -ArgumentList @($job) -WorkingDirectory $work -ReceiptPath $receipt -TimeoutSeconds 300|Out-Null
    $g=Get-Content -LiteralPath $receipt -Raw|ConvertFrom-Json
    if($g.status -ne 'SUCCEEDED' -or $g.cap_triggered -or $g.final_active_processes -ne 0 -or $g.memory_limit_bytes -ne 3221225472){throw 'Captured BibTeX guard failure'}
    $passes+=@{edition=$edition;pass='bibtex';peak_bytes=$g.peak_job_memory_used_bytes}
   }
   if($pass -eq 5){[IO.File]::Copy((Join-Path $work "$job.pdf"),(Join-Path $work 'pass5.pdf'),$false)}
  }
  $log=[IO.File]::ReadAllText((Join-Path $work "$job.log"))
  if($log -match '(?im)^Missing character:|undefined references|Reference .+ undefined|Citation .+ undefined|Rerun to get cross-references right|multiply[- ]defined labels|^!'){throw "Terminal log failure: $edition"}
  if((Get-FileHash -LiteralPath (Join-Path $work "$job.pdf")).Hash -ne (Get-FileHash -LiteralPath (Join-Path $work 'pass5.pdf')).Hash){throw "Pass 5/6 instability: $edition"}
 }
 if((Get-FileHash -LiteralPath (Join-Path $outputRoot "primary/$job.pdf")).Hash -ne (Get-FileHash -LiteralPath (Join-Path $outputRoot "replay/$job.pdf")).Hash){throw 'Replay bytes differ'}
}catch{$failure=$_.Exception.Message}
finally{
 if($owned){$mutex.ReleaseMutex()};$mutex.Dispose()
 foreach($v in $saved.Keys){[Environment]::SetEnvironmentVariable($v,$saved[$v],'Process')}
 $result=@{source_form=$SourceForm;acquired=$owned;abandoned=$abandoned;passes=$passes;error=$failure;reader_qa='REQUIRES_SEPARATE_CONTENT_LINK_AND_VISUAL_CHECKS'}
 [IO.File]::WriteAllText((Join-Path $outputRoot 'BUILD_RESULT.json'),($result|ConvertTo-Json -Depth 6)+"`n",$utf8)
}
if($failure){throw $failure}
Write-Output 'Deterministic build passed; content/link/visual release checks remain separate.'
