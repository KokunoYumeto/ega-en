$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceRoot = Join-Path $repoRoot 'source'
$outputRoot = Join-Path $PSScriptRoot 'out'
$env:SOURCE_DATE_EPOCH = '1787356800'
$env:FORCE_SOURCE_DATE = '1'
$env:TZ = 'UTC'
$env:BIBINPUTS = "$sourceRoot;"
New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

Push-Location $sourceRoot
try {
    & pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory $outputRoot EGA_English_Global_0_IV.tex
    if ($LASTEXITCODE -ne 0) { throw "Initial pdfLaTeX pass failed with exit code $LASTEXITCODE" }
    Push-Location $outputRoot
    try {
        & bibtex EGA_English_Global_0_IV
        if ($LASTEXITCODE -ne 0) { throw "BibTeX failed with exit code $LASTEXITCODE" }
    } finally {
        Pop-Location
    }
    2..5 | ForEach-Object {
        & pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory $outputRoot EGA_English_Global_0_IV.tex
        if ($LASTEXITCODE -ne 0) { throw "pdfLaTeX pass $_ failed with exit code $LASTEXITCODE" }
    }
} finally {
    Pop-Location
}

$pdf = Join-Path $outputRoot 'EGA_English_Global_0_IV.pdf'
if (-not (Test-Path -LiteralPath $pdf)) { throw 'Expected English reader PDF was not produced.' }
Get-Item -LiteralPath $pdf | Select-Object FullName,Length
Get-FileHash -Algorithm SHA256 -LiteralPath $pdf
