param(
    [Parameter(Mandatory = $true)]
    [string] $SourceRoot,
    [string] $OutputDirectory = (Join-Path $env:TEMP 'dotj-wp02-upstream-results')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$mapping = Get-Content -LiteralPath (Join-Path $repoRoot 'planning\stage-2\repos\dotj-core\evidence\wp02-upstream-test-map-v10.0.12.json') -Raw | ConvertFrom-Json
$source = (Resolve-Path -LiteralPath $SourceRoot).Path
$testSource = Join-Path $source $mapping.sourcePath
$project = Join-Path $source $mapping.projectPath
if ((Get-FileHash -LiteralPath $testSource -Algorithm SHA256).Hash.ToLowerInvariant() -ne $mapping.sourceSha256) {
    throw 'Pinned cancellation test source hash mismatch.'
}
if ((Get-FileHash -LiteralPath $project -Algorithm SHA256).Hash.ToLowerInvariant() -ne $mapping.projectSha256) {
    throw 'Pinned cancellation test project hash mismatch.'
}

$dotnetHost = (Get-Command dotnet -ErrorAction Stop).Source
$sdkVersion = (& $dotnetHost --version | Select-Object -First 1).Trim()
$sdkRoot = (Join-Path (Split-Path $dotnetHost -Parent) "sdk/$sdkVersion").Replace('\', '/')
if (-not ((& $dotnetHost --list-runtimes) | Where-Object { $_ -match '^Microsoft\.NETCore\.App 10\.0\.12 ' })) {
    throw 'Pinned runtime 10.0.12 is unavailable.'
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$resultFile = Join-Path $OutputDirectory 'cancellation.trx'
if (Test-Path -LiteralPath $resultFile) {
    Remove-Item -LiteralPath $resultFile
}
$class = $mapping.class
$filter = (@($mapping.cases | ForEach-Object { "FullyQualifiedName=$class.$($_.upstreamMethod)" })) -join '|'
$settings = @(
    '-p:UseLocalTargetingRuntimePack=false',
    '-p:UseDefaultTestHost=true',
    "-p:RunSettingsDotNetHostPath=$dotnetHost",
    "-p:NetCoreSdkRoot=$sdkRoot"
)
$arguments = @('test', $project, '--framework', 'net10.0', '--filter', $filter,
    '--verbosity', 'minimal', '-m:1', '--logger', 'trx;LogFileName=cancellation.trx',
    '--results-directory', $OutputDirectory) + $settings
Push-Location $source
try {
    & $dotnetHost @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Selected upstream cancellation tests failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}

[xml] $trx = Get-Content -LiteralPath $resultFile
$results = @($trx.TestRun.Results.UnitTestResult)
$summary = @()
foreach ($case in $mapping.cases) {
    $name = [regex]::Escape($case.upstreamMethod)
    $matches = @($results | Where-Object { $_.testName -match "\.$name(\(|$)" })
    if ($matches.Count -ne 1 -or $matches[0].outcome -ne 'Passed') {
        throw "Unexpected upstream result for $($case.upstreamMethod): $($matches.Count)."
    }
    $summary += [ordered]@{ oracleCase = $case.oracleCase; upstreamMethod = $case.upstreamMethod; outcome = 'Passed' }
}
if ($results.Count -ne $mapping.cases.Count) {
    throw "Unexpected selected test count $($results.Count)."
}
$manifest = [ordered]@{
    sourceCommit = $mapping.sourceCommit
    sdkVersion = $sdkVersion
    runtimeVersion = '10.0.12'
    testSourceSha256 = $mapping.sourceSha256
    projectSha256 = $mapping.projectSha256
    passed = $results.Count
    cases = $summary
    trxPath = $resultFile
}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'summary.json') -Encoding UTF8
$manifest | ConvertTo-Json -Depth 5
