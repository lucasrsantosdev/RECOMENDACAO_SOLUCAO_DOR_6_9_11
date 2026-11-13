$ErrorActionPreference = "Stop"
 Set-Location $PSScriptRoot
 py -3 .\main.py --modo ambos
 if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
 py -3 -m unittest discover -s tests -v
 if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
