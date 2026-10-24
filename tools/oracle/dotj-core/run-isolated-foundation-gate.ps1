<# Run the existing candidate gate in a detached worktree stored on D:. #>
[CmdletBinding()]
param(
    [string]$StorageRoot = 'D:\AI\Implementation\dotj Frameworks',
    [string]$PythonHome,
    [string]$DotnetHome,
    [string]$JdkHome,
    [string]$RunName,
    [ValidateRange(64,1024)][int]$JavaHeapMiB = 256,
    [ValidateRange(1,3)][int]$CheckWorkers = 3,
    [switch]$ExportEvidence,
    [switch]$PreflightOnly
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$repository = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$storage = [IO.Path]::GetFullPath($StorageRoot)
if ([IO.Path]::GetPathRoot($storage) -ine 'D:\') { throw 'Validation storage must be on D:.' }
if ($RunName -and $RunName -notmatch '^[a-zA-Z0-9_-]+$') { throw 'RunName must be a single directory name.' }
if (-not $PythonHome) { $PythonHome = Join-Path $storage 'toolchains/python-3.13.9' }
if (-not $DotnetHome) { $DotnetHome = Join-Path $storage 'toolchains/dotnet' }
if (-not $JdkHome) {
    $matches = @(Get-ChildItem -LiteralPath (Join-Path $storage 'toolchains/jdk-qualified') -Directory)
    if ($matches.Count -ne 1) { throw 'Specify one pinned JDK with -JdkHome.' }
    $JdkHome = $matches[0].FullName
}
foreach ($homePath in @($PythonHome, $DotnetHome, $JdkHome)) {
    if (-not ([IO.Path]::GetFullPath($homePath)).StartsWith($storage.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "Toolchain must be stored under StorageRoot: $homePath"
    }
}
$baseline = Get-Content -LiteralPath (Join-Path $repository 'planning/stage-2/repos/dotj-core/evidence/baseline-lock.json') -Raw | ConvertFrom-Json
function Check-Binary([string]$Path, [string]$Expected) {
    $actual = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $Expected) { throw "Pinned binary hash mismatch: $Path" }
    [ordered]@{ path = $Path; sha256 = $actual }
}
$binaryChecks = @()
foreach ($entry in $baseline.localJavaToolchain.binaryHashesSha256.PSObject.Properties) {
    $binaryChecks += Check-Binary (Join-Path $JdkHome $entry.Name) $entry.Value
}
foreach ($entry in $baseline.localOracleCandidate.binaryHashesSha256.PSObject.Properties) {
    $relative = $entry.Name.Substring($entry.Name.IndexOf('/dotnet/') + 8)
    $binaryChecks += Check-Binary (Join-Path $DotnetHome $relative) $entry.Value
}
$python = Join-Path $PythonHome 'python.exe'
& $python -c 'import sys, zipfile, hashlib, subprocess; print(sys.version)'
if ($LASTEXITCODE -ne 0) { throw 'Python standard-library preflight failed.' }
if ($PreflightOnly) { $binaryChecks | ConvertTo-Json -Depth 4; return }

$revision = (& git -C $repository rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Cannot resolve source revision.' }
$sourceChanges = @(& git -C $repository status --porcelain)
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect source checkout.' }
if ($sourceChanges.Count -ne 0) { throw 'Commit or resolve source checkout changes before validating HEAD.' }
if (-not $RunName) { $RunName = $revision.Substring(0, 12) }
$runRoot = Join-Path $storage ('validation/' + $RunName)
if (Test-Path -LiteralPath $runRoot) { throw "Run directory already exists; preserve it and select another RunName: $runRoot" }
New-Item -ItemType Directory -Force -Path $runRoot | Out-Null
$worktree = Join-Path $runRoot 'source'
& git -c core.longpaths=true -C $repository worktree add --quiet --detach $worktree $revision
if ($LASTEXITCODE -ne 0) { throw 'Cannot create isolated source worktree.' }
$variables = @('PATH', 'TEMP', 'TMP', 'DOTNET_ROOT', 'DOTNET_CLI_HOME', 'NUGET_PACKAGES',
    'DOTNET_SKIP_FIRST_TIME_EXPERIENCE', 'DOTNET_CLI_TELEMETRY_OPTOUT', 'DOTNET_MULTILEVEL_LOOKUP',
    'PYTHONPYCACHEPREFIX', 'JAVA_HOME', 'JAVA_TOOL_OPTIONS', 'MSBUILDDISABLENODEREUSE')
$saved = @{}
foreach ($name in $variables) { $saved[$name] = [Environment]::GetEnvironmentVariable($name, 'Process') }
try {
    $env:PATH = "$PythonHome;$DotnetHome;$(Join-Path $JdkHome 'bin');$env:PATH"
    $env:TEMP = Join-Path $runRoot 'tmp'; $env:TMP = $env:TEMP
    $env:DOTNET_ROOT = $DotnetHome
    $env:DOTNET_CLI_HOME = Join-Path $storage 'cache/dotnet-home'
    $env:NUGET_PACKAGES = Join-Path $storage 'cache/nuget'
    $env:PYTHONPYCACHEPREFIX = Join-Path $storage 'cache/python'
    $env:JAVA_HOME = $JdkHome
    # Default ergonomics can reserve a large initial heap for every concurrent consumer JVM.
    $env:JAVA_TOOL_OPTIONS = ("$($saved['JAVA_TOOL_OPTIONS']) -Xms16m -Xmx${JavaHeapMiB}m").Trim()
    $env:DOTNET_SKIP_FIRST_TIME_EXPERIENCE = '1'; $env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
    $env:DOTNET_MULTILEVEL_LOOKUP = '0'; $env:MSBUILDDISABLENODEREUSE = '1'
    New-Item -ItemType Directory -Force -Path $env:TEMP, $env:DOTNET_CLI_HOME, $env:NUGET_PACKAGES, $env:PYTHONPYCACHEPREFIX | Out-Null
    $oracle = Join-Path $worktree 'tools/oracle/dotj-core'
    # This prerequisite was implicit in the old machine's existing build folder.
    $ErrorActionPreference = 'Continue'
    & $python (Join-Path $oracle 'run-captured-python.py') --log (Join-Path $runRoot 'candidate-bootstrap.log') -- (Join-Path $oracle 'build-idisposable-candidate.py')
    $ErrorActionPreference = 'Stop'
    if ($LASTEXITCODE -ne 0) { throw 'Compile-only candidate bootstrap failed.' }
    $ErrorActionPreference = 'Continue'
    & $python (Join-Path $oracle 'run-captured-python.py') --log (Join-Path $runRoot 'foundation-gate.log') -- (Join-Path $oracle 'run-foundation-public-candidate-gate.py') --check-workers $CheckWorkers
    $ErrorActionPreference = 'Stop'
    if ($LASTEXITCODE -ne 0) { throw 'Foundation gate failed; see retained run logs.' }
    $changed = @(& git -C $worktree diff --name-only)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inventory generated evidence changes.' }
    $newEvidence = @(& git -C $worktree ls-files --others --exclude-standard)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inventory newly generated evidence.' }
    $changed = @(@($changed) + @($newEvidence) | Sort-Object -Unique)
    foreach ($relative in $changed) {
        if ($relative -notmatch '^planning/stage-2/repos/dotj-core/evidence/[^/]+\.json$') {
            throw "Unexpected tracked output from gate: $relative"
        }
    }
    $record = [ordered]@{
        schemaVersion = 1; sourceRevision = $revision; runRoot = $runRoot
        pinnedBinaryChecks = $binaryChecks; gatePassed = $true
        javaValidationOptions = $env:JAVA_TOOL_OPTIONS
        independentCheckWorkers = $CheckWorkers
        changedEvidencePaths = $changed; evidenceExportRequested = [bool]$ExportEvidence; evidenceExported = $false
        qualification = 'BOUNDED_CANDIDATE_ONLY; E01/E02/E03/N01/Q01_OPEN'
    }
    [IO.File]::WriteAllText((Join-Path $runRoot 'isolated-validation.json'), ($record | ConvertTo-Json -Depth 8) + "`n", (New-Object Text.UTF8Encoding($false)))
    if ($ExportEvidence) {
        if ((& git -C $repository rev-parse HEAD).Trim() -ne $revision) { throw 'Source HEAD changed during validation; evidence not exported.' }
        foreach ($relative in $changed) {
            $destination = Join-Path $repository $relative
            if (@(& git -C $repository status --porcelain -- $relative).Count -ne 0) { throw "Refusing to overwrite modified evidence: $relative" }
        }
        foreach ($relative in $changed) { Copy-Item -LiteralPath (Join-Path $worktree $relative) -Destination (Join-Path $repository $relative) }
        $record.evidenceExported = $true
        [IO.File]::WriteAllText((Join-Path $runRoot 'isolated-validation.json'), ($record | ConvertTo-Json -Depth 8) + "`n", (New-Object Text.UTF8Encoding($false)))
    }
    Write-Output "PASS isolated foundation validation: $revision; builds, caches and logs on D:"
} finally {
    foreach ($name in $variables) { [Environment]::SetEnvironmentVariable($name, $saved[$name], 'Process') }
}
