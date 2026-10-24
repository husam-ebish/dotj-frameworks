<##
Read-only acceptance and evidence audit; does not run or qualify the candidate.
Run from any directory with Windows PowerShell 5.1 or PowerShell 7.
Use -OutputPath to save a machine-readable review. Temporary output belongs under
D:\AI\Implementation\dotj Frameworks, outside the repository.
##>
[CmdletBinding()]
param(
    [string]$RepositoryRoot,
    [string]$OutputPath,
    [string]$StorageRoot = 'D:\AI\Implementation\dotj Frameworks'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $RepositoryRoot) { $RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path }
$StorageRoot = [IO.Path]::GetFullPath($StorageRoot)
if ([IO.Path]::GetPathRoot($StorageRoot) -ine 'D:\') { throw 'Audit command storage must be on D:.' }
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
function Pinned-File([string]$Path, [string]$Expected) {
    $exists = Test-Path -LiteralPath $Path -PathType Leaf
    $actual = $null; $errorText = $null
    if ($exists) {
        try { $actual = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
        catch { $errorText = $_.Exception.Message }
    }
    [ordered]@{ path = $Path; exists = $exists; expectedSha256 = $Expected
        actualSha256 = $actual; hashMatched = ($exists -and $actual -eq $Expected); error = $errorText }
}
function Native-Output([string]$Executable, [string]$Arguments) {
    if (-not $Executable -or -not (Test-Path -LiteralPath $Executable -PathType Leaf)) {
        return [ordered]@{ path = $Executable; arguments = $Arguments; exitCode = $null
            stdout = ''; stderr = 'No verified executable available'; timedOut = $false }
    }
    $temporary = Join-Path $StorageRoot 'tmp'
    New-Item -ItemType Directory -Force -Path $temporary | Out-Null
    $process = New-Object Diagnostics.Process
    $process.StartInfo.FileName = $Executable
    $process.StartInfo.Arguments = $Arguments
    $process.StartInfo.UseShellExecute = $false
    $process.StartInfo.CreateNoWindow = $true
    $process.StartInfo.RedirectStandardOutput = $true
    $process.StartInfo.RedirectStandardError = $true
    $process.StartInfo.EnvironmentVariables['TEMP'] = $temporary
    $process.StartInfo.EnvironmentVariables['TMP'] = $temporary
    $process.StartInfo.EnvironmentVariables['PYTHONPYCACHEPREFIX'] = Join-Path $StorageRoot 'cache/python'
    $process.StartInfo.EnvironmentVariables['DOTNET_CLI_HOME'] = Join-Path $StorageRoot 'cache/dotnet-home'
    $process.StartInfo.EnvironmentVariables['DOTNET_ROOT'] = Join-Path $StorageRoot 'toolchains/dotnet'
    $process.StartInfo.EnvironmentVariables['DOTNET_CLI_TELEMETRY_OPTOUT'] = '1'
    try {
        [void]$process.Start()
        $stdout = $process.StandardOutput.ReadToEndAsync()
        $stderr = $process.StandardError.ReadToEndAsync()
        $timedOut = -not $process.WaitForExit(10000)
        if ($timedOut) { $process.Kill(); $process.WaitForExit() }
        return [ordered]@{ path = $Executable; arguments = $Arguments; exitCode = $process.ExitCode
            stdout = $stdout.GetAwaiter().GetResult().TrimEnd(); stderr = $stderr.GetAwaiter().GetResult().TrimEnd()
            timedOut = $timedOut }
    } catch {
        return [ordered]@{ path = $Executable; arguments = $Arguments; exitCode = $null
            stdout = ''; stderr = $_.Exception.Message; timedOut = $false }
    } finally { $process.Dispose() }
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
# Discover the isolated profile by current file hashes, never by old-PC paths.
$toolRoot = Join-Path $StorageRoot 'toolchains'
$jdkRoot = Join-Path $toolRoot 'jdk-qualified'
$profiles = @()
if (Test-Path -LiteralPath $jdkRoot -PathType Container) {
    foreach ($directory in @(Get-ChildItem -LiteralPath $jdkRoot -Directory | Sort-Object FullName)) {
        $files = @($packet.jdkToolchain.binaryHashesSha256.PSObject.Properties | ForEach-Object {
            Pinned-File (Join-Path $directory.FullName $_.Name) $_.Value
        })
        $profiles += [ordered]@{ root = $directory.FullName; files = $files
            hashMatched = ($files.Count -eq 3 -and @($files | Where-Object { -not $_.hashMatched }).Count -eq 0) }
    }
}
$selectedJdk = @($profiles | Where-Object { $_.hashMatched } | Select-Object -First 1)
$dotnetRoot = Join-Path $toolRoot 'dotnet'
$dotnetFiles = @()
foreach ($relative in @('dotnet.exe', "sdk/$sdk/dotnet.dll", "shared/Microsoft.NETCore.App/$runtimeVersion/System.Private.CoreLib.dll")) {
    $pin = @($baseline.localOracleCandidate.binaryHashesSha256.PSObject.Properties | Where-Object {
        $_.Name.Replace('\', '/').EndsWith('/' + $relative)
    })
    Require ($pin.Count -eq 1) "Missing or ambiguous baseline binary pin: $relative"
    $dotnetFiles += Pinned-File (Join-Path $dotnetRoot $relative) $pin[0].Value
}
$dotnetMatched = @($dotnetFiles | Where-Object { -not $_.hashMatched }).Count -eq 0
$pythonPath = $null
$downloadManifestPath = Join-Path $RepositoryRoot 'tools/oracle/dotj-core/dependency-downloads-v1.json'
if (Test-Path -LiteralPath $downloadManifestPath) {
    $downloads = Get-Content -LiteralPath $downloadManifestPath -Raw | ConvertFrom-Json
    $pythonPackage = @($downloads.packages | Where-Object { $_.id -eq 'python' })
    if ($pythonPackage.Count -eq 1) { $pythonPath = Join-Path (Join-Path $toolRoot $pythonPackage[0].extractTo) 'python.exe' }
}
$javaHome = if ($selectedJdk.Count -eq 1) { $selectedJdk[0].root } else { $null }
$verifiedDotnet = if ($dotnetMatched) { Join-Path $dotnetRoot 'dotnet.exe' } else { $null }
$commands = [ordered]@{
    pythonVersion = Native-Output $pythonPath '--version'
    pythonStandardLibrary = Native-Output $pythonPath '-c "import sys, json, hashlib, subprocess; print(sys.version)"'
    javaVersion = Native-Output $(if ($javaHome) { Join-Path $javaHome 'bin/java.exe' }) '-version'
    javacVersion = Native-Output $(if ($javaHome) { Join-Path $javaHome 'bin/javac.exe' }) '-version'
    jarVersion = Native-Output $(if ($javaHome) { Join-Path $javaHome 'bin/jar.exe' }) '--version'
    sdkList = Native-Output $verifiedDotnet '--list-sdks'
    runtimeList = Native-Output $verifiedDotnet '--list-runtimes'
}
$isolatedReady = ($selectedJdk.Count -eq 1 -and $dotnetMatched -and
    @($commands.Values | Where-Object { $_.exitCode -ne 0 -or $_.timedOut }).Count -eq 0 -and
    $commands.pythonVersion.stdout -match '^Python [0-9]+\.[0-9]+' -and
    $commands.sdkList.stdout -match ('(?m)^' + [regex]::Escape($sdk) + ' ') -and
    $commands.runtimeList.stdout -match ('(?m)^Microsoft.NETCore.App ' + [regex]::Escape($runtimeVersion) + ' '))
$core = @($progress.frameworks | Where-Object { $_.repository -eq 'dotj-core' })
Require ($core.Count -eq 1) 'Expected one dotj-core framework'
$review = [ordered]@{
    schemaVersion = 2
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
        commandResolution = 'DEFAULT PATH ONLY; isolated tools are reported separately'
        commands = $toolchain
        requiredSdk = $sdk
        sdkAvailable = $sdkAvailable
        installedSdks = $sdks
        requiredRuntime = $runtimeVersion
        runtimeAvailable = $runtimeAvailable
        installedRuntimes = $runtimes
        pinnedToolchainHashesVerified = $false
        requiredCommandNamesAndDotnetVersionsAvailable = ($sdkAvailable -and $runtimeAvailable -and @($toolchain | Where-Object { -not $_.available }).Count -eq 0)
    }
    isolatedPrerequisites = [ordered]@{
        storageRoot = $StorageRoot; jdkProfiles = $profiles; dotnetBinaryChecks = $dotnetFiles
        commandResults = $commands; readyForPinnedValidation = $isolatedReady
        qualification = 'Tool availability and binary identity only; not product or release acceptance'
    }
    dependencyScopes = [ordered]@{
        currentProduct = 'JDK APIs only, targeting Java 21; no third-party Java runtime libraries; Maven/Gradle not required'
        development = 'Python and pinned .NET SDK/runtime are validation tools, excluded from the Java product JAR'
        broaderProject = 'Resolved 66-framework graph remains open; no released public .j SDK installer/feed documented'
    }
    nextTask = $progress.nextProposedBatch.outcome
    acceptanceDisposition = 'No tasks or gates accepted; E01 decisions require the recorded reviews. Batch counts are not implementation completion.'
}
$json = $review | ConvertTo-Json -Depth 15
if ($OutputPath) {
    [IO.File]::WriteAllText($OutputPath, $json + "`n", (New-Object Text.UTF8Encoding($false)))
}
$json
