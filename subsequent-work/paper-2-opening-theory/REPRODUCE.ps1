param(
    [string]$Python = "python",
    [string]$Lake = "lake",
    [string]$Latexmk = "latexmk"
)
$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot
try {
    & $Python "CODE\verify_manifest.py"
    if ($LASTEXITCODE -ne 0) { throw "Manifest verification failed" }
    & $Python "CODE\verify_paper.py"
    if ($LASTEXITCODE -ne 0) { throw "Exact verification failed" }
    & $Python "CODE\verify_paper.py" --fixture
    if ($LASTEXITCODE -ne 0) { throw "Discrepancy fixture failed" }
    & $Python "CODE\export_tables.py"
    if ($LASTEXITCODE -ne 0) { throw "Table export failed" }
    Push-Location "formalisation"
    try {
        & $Lake build
        if ($LASTEXITCODE -ne 0) { throw "Lean build failed" }
        & $Lake env lean M3AFormalisation.lean
        if ($LASTEXITCODE -ne 0) { throw "Lean root-module check failed" }
    } finally {
        Pop-Location
    }
    Push-Location "paper\source"
    try {
        & $Latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
        if ($LASTEXITCODE -ne 0) { throw "Paper build failed" }
    } finally {
        Pop-Location
    }
} finally {
    Pop-Location
}

