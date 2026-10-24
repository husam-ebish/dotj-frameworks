<# Acquire and verify only the selected foundation toolchain; no global installation. #>
[CmdletBinding()]
param(
    [string]$StorageRoot = 'D:\AI\Implementation\dotj Frameworks',
    [switch]$VerifyOnly,
    [switch]$Extract
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$storage = [IO.Path]::GetFullPath($StorageRoot)
if ([IO.Path]::GetPathRoot($storage) -ine 'D:\') { throw 'Bootstrap storage must be on D:.' }
if ($VerifyOnly -and $Extract) { throw 'VerifyOnly cannot be combined with Extract.' }
$manifestPath = Join-Path $PSScriptRoot 'dependency-downloads-v1.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$toolchains = Join-Path $storage 'toolchains'
$downloads = Join-Path $toolchains 'downloads'
if (-not $VerifyOnly) { New-Item -ItemType Directory -Force -Path $downloads | Out-Null }
$verified = @()
foreach ($package in $manifest.packages) {
    if ([IO.Path]::GetFileName($package.file) -ne $package.file) { throw 'Manifest filename must be a single component.' }
    $archive = Join-Path $downloads $package.file
    $valid = $false
    if (Test-Path -LiteralPath $archive) {
        $valid = (Get-FileHash -LiteralPath $archive -Algorithm $package.hashAlgorithm).Hash -ieq $package.hash
    }
    if (-not $valid) {
        if ($VerifyOnly) { throw "Missing or mismatched archive: $archive" }
        $partial = $archive + '.partial'
        & curl.exe --fail --location --silent --show-error --retry 2 --max-time 300 $package.url --output $partial
        if ($LASTEXITCODE -ne 0) { throw "Download failed: $($package.id)" }
        if ((Get-FileHash -LiteralPath $partial -Algorithm $package.hashAlgorithm).Hash -ine $package.hash) {
            throw "Downloaded archive hash mismatch: $($package.id); retained .partial for inspection"
        }
        Move-Item -LiteralPath $partial -Destination $archive -Force
    }
    if ($Extract -and $package.extractTo) {
        if ([IO.Path]::GetFileName($package.extractTo) -ne $package.extractTo) { throw 'Extraction target must be a single component.' }
        $destination = Join-Path $toolchains $package.extractTo
        New-Item -ItemType Directory -Force -Path $destination | Out-Null
        & tar.exe -xf $archive -C $destination
        if ($LASTEXITCODE -ne 0) { throw "Extraction failed: $($package.id)" }
    }
    $verified += [ordered]@{
        id = $package.id; version = $package.version; role = $package.role
        url = $package.url; path = $archive; bytes = (Get-Item -LiteralPath $archive).Length
        hashAlgorithm = $package.hashAlgorithm; hash = $package.hash; hashMatched = $true
    }
    Write-Output "PASS verified $($package.id) $($package.version)"
}
if ($Extract) {
    & (Join-Path $PSScriptRoot 'run-isolated-foundation-gate.ps1') -StorageRoot $storage -PreflightOnly
}
$record = [ordered]@{
    schemaVersion = 1; scope = $manifest.scope
    manifestSha256 = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
    archives = $verified
    productRuntime = 'JDK APIs only; no third-party Java library dependency. Maven and Gradle are not required.'
    broaderProject = $manifest.broaderProject
}
$root = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$output = Join-Path $root 'planning/stage-2/repos/dotj-core/evidence/dependency-download-verification-v1.json'
[IO.File]::WriteAllText($output, ($record | ConvertTo-Json -Depth 8) + "`n", (New-Object Text.UTF8Encoding($false)))
Write-Output 'PASS selected foundation archive verification; no product library or public .j SDK installed'
