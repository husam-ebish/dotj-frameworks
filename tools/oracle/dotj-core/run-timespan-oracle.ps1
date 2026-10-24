<# Backward-compatible entry point for the selected TimeSpan reference capture. #>
[CmdletBinding()]
param([string]$StorageRoot = 'D:\AI\Implementation\dotj Frameworks')
$ErrorActionPreference = 'Stop'
& (Join-Path $PSScriptRoot 'run-pinned-contract-oracle.ps1') -Contract timespan -StorageRoot $StorageRoot
