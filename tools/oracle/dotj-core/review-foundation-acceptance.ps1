<##
Read-only acceptance and evidence audit; does not run or qualify the candidate.
Run from any directory with Windows PowerShell 5.1 or PowerShell 7.
Use -OutputPath to save a machine-readable review. Temporary output belongs under
D:\AI\Implementation\dotj Frameworks, outside the repository.
##>
[CmdletBinding()]
param(
    [string]$RepositoryRoot,
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $RepositoryRoot) { $RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path }
function Read-Record([string]$Path) {
    Get-Content -LiteralPath (Join-Path $RepositoryRoot $Path) -Raw | ConvertFrom-Json
}
function Require([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}
function Check-Hash([string]$Path, [string]$Expected) {
    $actual = (Get-FileHash -LiteralPath (Join-Path $RepositoryRoot $Path) -Algorithm SHA256).Hash.ToLowerInvariant()
    Require ($actual -eq $Expected) "Evidence hash mismatch: $Path"
}

$progress = Read-Record 'planning/stage-2/IMPLEMENTATION-PROGRESS.json'
$prefix = 'planning/stage-2/repos/dotj-core/evidence/'
$gate = Read-Record ($prefix + 'foundation-public-candidate-gate-v1.json')
$packet = Read-Record ($prefix + 'foundation-e01-review-packet-v1.json')
$candidate = Read-Record ($prefix + 'foundation-product-candidate-v1.json')
$baseline = Read-Record ($prefix + 'baseline-lock.json')
$sdk = (Read-Record 'tools/oracle/dotj-core/global.json').sdk.version

# Recompute counts from task and gate records; never infer acceptance from batches.
$tasks = @($progress.frameworks | ForEach-Object { $_.tasks })
$implementation = @($tasks | Where-Object { $_.classification -ne 'prerequisite' })
$naming = @($tasks | Where-Object { $_.classification -eq 'prerequisite' })
$acceptedStatuses = @('COMPLETE', 'COMPLETED', 'ACCEPTED')
$accepted = @($implementation | Where-Object { $_.status -in $acceptedStatuses })
$gates = @($progress.frameworks | ForEach-Object { $_.outstandingPreparationAndQualificationGates.PSObject.Properties.Value })
$openItems = @($tasks | Where-Object { $_.status -notin $acceptedStatuses }).Count +
    @($gates | Where-Object { $_ -notin $acceptedStatuses }).Count
$qualified = @($progress.frameworks | Where-Object {
    $_.completedImplementationTaskCount -eq $_.totalBaselinedImplementationTaskCount -and
    @($_.outstandingPreparationAndQualificationGates.PSObject.Properties.Value |
        Where-Object { $_ -notin $acceptedStatuses }).Count -eq 0
})
Require ($progress.frameworks.Count -eq $progress.overall.frameworkCount) 'Framework count drift'
Require (@($tasks.id | Sort-Object -Unique).Count -eq $tasks.Count) 'Duplicate task IDs'
Require ($implementation.Count -eq $progress.overall.totalBaselinedImplementationTaskCount) 'Implementation denominator drift'
Require ($accepted.Count -eq $progress.overall.completedImplementationTaskCount) 'Accepted task count drift'
$percent = [Math]::Round(100.0 * $accepted.Count / $implementation.Count, 2)
Require ($percent -eq $progress.overall.implementedPercent) 'Implementation percentage drift'
Require ($qualified.Count -eq $progress.overall.frameworksFullyImplementedAndQualified) 'Framework qualification count drift'
Require ($openItems -eq $progress.batchPlan.outstandingAcceptanceItems) 'Open acceptance item count drift'
Require ($progress.completedBatches.Count -eq $progress.batchPlan.completedBatches) 'Batch count drift'
Require (@($progress.completedBatches | Sort-Object -Unique).Count -eq $progress.completedBatches.Count) 'Duplicate batch IDs'

# Check exact bytes from the historical gate, then check source freshness separately.
foreach ($entry in $gate.evidenceSha256.PSObject.Properties) {
    Check-Hash ($prefix + $entry.Name) $entry.Value
}
foreach ($source in $candidate.productSources) { Check-Hash $source.path $source.sha256 }
Require ($gate.candidateJarSha256 -eq $candidate.jarSha256) 'Candidate/gate identity drift'
Require ($packet.candidateJarSha256 -eq $candidate.jarSha256) 'Review/candidate identity drift'
Require ($gate.productSourceCount -eq $candidate.productSources.Count) 'Candidate source count drift'
Require ($gate.releaseQualified -eq $false) 'Review logic needs updating for a qualified release'
$openDecisions = @($packet.openDecisions | Where-Object { $_.status -eq 'OPEN' })
Require ($openDecisions.Count -eq $gate.openE01DecisionCount) 'E01 decision count drift'
$localJar = Join-Path $RepositoryRoot $candidate.jarPath
if (Test-Path -LiteralPath $localJar) { Check-Hash $candidate.jarPath $candidate.jarSha256 }

# Capture availability without installing tools, building, or writing caches.
$toolchain = @()
foreach ($tool in @('python', 'java', 'javac', 'jar', 'javap')) {
    $command = Get-Command $tool -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    $available = $null -ne $command
    # WindowsApps python is a Store launcher, not an installed interpreter.
    if ($available -and $tool -eq 'python' -and $command.Source -like '*\Microsoft\WindowsApps\*') { $available = $false }
    $toolchain += [ordered]@{ tool = $tool; available = $available; path = $(if ($command) { $command.Source } else { $null }) }
}
$dotnet = Get-Command dotnet -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
$sdks = @(); $runtimes = @()
if ($dotnet) {
    $sdks = @(& $dotnet.Source --list-sdks)
    Require ($LASTEXITCODE -eq 0) 'Cannot inventory .NET SDKs'
    $runtimes = @(& $dotnet.Source --list-runtimes)
    Require ($LASTEXITCODE -eq 0) 'Cannot inventory .NET runtimes'
}
$sdkAvailable = @($sdks | Where-Object { $_.StartsWith($sdk + ' ') }).Count -eq 1
$runtimeVersion = $baseline.localOracleCandidate.runtimeVersion
$runtimeAvailable = @($runtimes | Where-Object { $_.StartsWith('Microsoft.NETCore.App ' + $runtimeVersion + ' ') }).Count -eq 1
$core = @($progress.frameworks | Where-Object { $_.repository -eq 'dotj-core' })
Require ($core.Count -eq 1) 'Expected one dotj-core framework'
$review = [ordered]@{
    schemaVersion = 1
    scope = 'Foundation acceptance review; historical evidence integrity and local prerequisites only'
    status = 'REVIEW_PASS; PUBLIC_QUALIFICATION_OPEN'
    implementation = [ordered]@{ accepted = $accepted.Count; total = $implementation.Count; percent = $percent }
    namingPrerequisites = $naming.Count
    openAcceptanceItems = $openItems
    qualifiedFrameworks = $qualified.Count
    frameworkCount = $progress.frameworks.Count
    completedBatches = $progress.completedBatches.Count
    plannedProjectBatches = $progress.batchPlan.plannedTotalBatches
    remainingProjectBatches = $progress.batchPlan.remainingPlannedBatches
    foundationGates = $core[0].outstandingPreparationAndQualificationGates
    openE01Decisions = $openDecisions
    historicalGate = [ordered]@{
        checksRecorded = $gate.checks.Count
        evidenceFilesHashVerified = @($gate.evidenceSha256.PSObject.Properties).Count
        productSourcesHashVerified = $candidate.productSources.Count
        candidateJarSha256 = $candidate.jarSha256
        localJarPresent = (Test-Path -LiteralPath $localJar)
        rerunThisReview = $false
    }
    localPrerequisites = [ordered]@{
        commands = $toolchain
        requiredSdk = $sdk
        sdkAvailable = $sdkAvailable
        installedSdks = $sdks
        requiredRuntime = $runtimeVersion
        runtimeAvailable = $runtimeAvailable
        installedRuntimes = $runtimes
        pinnedToolchainHashesVerified = $false
        requiredCommandsAndVersionsAvailable = ($sdkAvailable -and $runtimeAvailable -and @($toolchain | Where-Object { -not $_.available }).Count -eq 0)
    }
    nextTask = 'Restore isolated Python, pinned SDK/runtime and JDK under D:\AI\Implementation\dotj Frameworks; verify baseline hashes, redirect gate build/cache output off C:, then rerun the packaged consumers and 20-check gate.'
    acceptanceDisposition = 'No tasks or gates accepted; E01 decisions require the recorded reviews. Batch counts are not implementation completion.'
}
$json = $review | ConvertTo-Json -Depth 15
if ($OutputPath) {
    [IO.File]::WriteAllText($OutputPath, $json + "`n", (New-Object Text.UTF8Encoding($false)))
}
$json
