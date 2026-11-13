$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
py -3 .\solucao_definitiva\executar.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
