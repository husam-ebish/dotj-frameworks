param(
    [Parameter(Mandatory = $true)]
    [string] $SourceRoot,
    [string] $OutputDirectory = (Join-Path $env:TEMP 'dotj-wp01-upstream-results')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$source = (Resolve-Path -LiteralPath $SourceRoot).Path
$expected = @{
    'src/libraries/System.Threading/tests/System.Threading.Tests.csproj' = '5dcea5725804cfb93c1e4683fb8c9ec64818919eae365231e0097a3e0c2b1ca3'
    'src/libraries/System.Threading/tests/AsyncLocalTests.cs' = 'acf6f236c142e98a38c6a2f237585e6718deba5568d6593e543c6a1c7136c119'
    'src/libraries/System.Threading/tests/ExecutionContextTests.cs' = '6b3a4c92779fcadfdbea667d76a8cd380d60b896cac01fe65fa16445afb59477'
    'src/libraries/Microsoft.Extensions.DependencyInjection/tests/DI.Tests/Microsoft.Extensions.DependencyInjection.Tests.csproj' = '5aa0a1a77db15d3086866e97802b532b5a33b7297986e979d1566d187835d98c'
    'src/libraries/Microsoft.Extensions.DependencyInjection/tests/DI.Tests/ServiceProviderContainerTests.cs' = '43883d7686636dcb84c4fa5a74386a67d29499f5b915033918bc55de2125968f'
    'src/libraries/Microsoft.Extensions.DependencyInjection.Specification.Tests/src/DependencyInjectionSpecificationTests.cs' = 'b600356d3641e29e2e9a3a0dad9f63fecb8395ced022dc39df4f0c7d29a2b306'
}
$dotnetHost = (Get-Command dotnet -ErrorAction Stop).Source
$sdkVersion = (& $dotnetHost --version | Select-Object -First 1).Trim()
$sdkRoot = (Join-Path (Split-Path $dotnetHost -Parent) "sdk/$sdkVersion").Replace('\', '/')
if (-not (Test-Path -LiteralPath $sdkRoot)) {
    throw "SDK root missing: $sdkRoot"
}
$runtimes = & $dotnetHost --list-runtimes
if (-not ($runtimes | Where-Object { $_ -match '^Microsoft\.NETCore\.App 10\.0\.12 ' })) {
    throw 'The pinned installed runtime Microsoft.NETCore.App 10.0.12 is missing.'
}

$drive = $null
foreach ($letter in @('R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')) {
    if (-not (Get-PSDrive -Name $letter -ErrorAction SilentlyContinue)) {
        $drive = "${letter}:"
        break
    }
}
if ($null -eq $drive) {
    throw 'No free drive letter R-Z is available for the short source path.'
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
& subst $drive $source
if ($LASTEXITCODE -ne 0) {
    throw "Could not map $drive to the pinned source."
}

try {
    $mappedRoot = "$drive\"
    foreach ($entry in $expected.GetEnumerator()) {
        $path = Join-Path $mappedRoot $entry.Key
        $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actual -ne $entry.Value) {
            throw "Pinned source hash mismatch: $($entry.Key)"
        }
    }
    $settings = @(
        '-p:UseLocalTargetingRuntimePack=false',
        '-p:UseDefaultTestHost=true',
        "-p:RunSettingsDotNetHostPath=$dotnetHost",
        "-p:NetCoreSdkRoot=$sdkRoot"
    )
    $suites = @(
        @{
            Name = 'context'
            Project = 'src/libraries/System.Threading/tests/System.Threading.Tests.csproj'
            Filter = 'FullyQualifiedName=System.Threading.Tests.AsyncLocalTests.CaptureAndRestore|FullyQualifiedName=System.Threading.Tests.ExecutionContextTests.FlowTest'
            Expected = @{
                'CaptureAndRestore' = 1
                'FlowTest' = 1
            }
        },
        @{
            Name = 'ownership'
            Project = 'src/libraries/Microsoft.Extensions.DependencyInjection/tests/DI.Tests/Microsoft.Extensions.DependencyInjection.Tests.csproj'
            Filter = (@(
                'SingletonServiceCreatedFromInstanceIsNotDisposedWhenContainerIsDisposed',
                'ProviderDisposeThrowsWhenOnlyDisposeAsyncImplemented',
                'DoesNotDisposeSingletonInstances',
                'SingletonServiceCreatedFromFactoryIsDisposedWhenContainerIsDisposed',
                'ProviderScopeDisposeAsyncCallsDisposeAsyncOnServices',
                'ProviderScopeDisposePrefersServiceDispose',
                'DisposesInReverseOrderOfCreation',
                'ProviderScopeDisposeThrowsWhenOnlyDisposeAsyncImplemented',
                'ProviderAsyncScopeDisposeThrowsWhenOnlyDisposeAsyncImplemented'
            ) | ForEach-Object { "FullyQualifiedName~$_" }) -join '|'
            Expected = @{
                'SingletonServiceCreatedFromInstanceIsNotDisposedWhenContainerIsDisposed' = 4
                'ProviderDisposeThrowsWhenOnlyDisposeAsyncImplemented' = 4
                'DoesNotDisposeSingletonInstances' = 4
                'SingletonServiceCreatedFromFactoryIsDisposedWhenContainerIsDisposed' = 4
                'ProviderScopeDisposeAsyncCallsDisposeAsyncOnServices' = 4
                'ProviderScopeDisposePrefersServiceDispose' = 4
                'DisposesInReverseOrderOfCreation' = 5
                'ProviderScopeDisposeThrowsWhenOnlyDisposeAsyncImplemented' = 4
                'ProviderAsyncScopeDisposeThrowsWhenOnlyDisposeAsyncImplemented' = 4
            }
        }
    )

    $summaries = @()
    Push-Location $mappedRoot
    try {
        foreach ($suite in $suites) {
            $resultFile = Join-Path $OutputDirectory "$($suite.Name).trx"
            if (Test-Path -LiteralPath $resultFile) {
                Remove-Item -LiteralPath $resultFile
            }
            $project = Join-Path $mappedRoot $suite.Project
            $arguments = @('test', $project, '--framework', 'net10.0', '--filter', $suite.Filter,
                '--verbosity', 'minimal', '-m:1', '--logger', "trx;LogFileName=$($suite.Name).trx",
                '--results-directory', $OutputDirectory) + $settings
            & $dotnetHost @arguments
            if ($LASTEXITCODE -ne 0) {
                throw "Upstream $($suite.Name) test run failed with exit code $LASTEXITCODE."
            }
            [xml] $trx = Get-Content -LiteralPath $resultFile
            $results = @($trx.TestRun.Results.UnitTestResult)
            foreach ($method in $suite.Expected.Keys) {
                $matches = @($results | Where-Object { $_.testName -match "\.$method(\(|$)" })
                if ($matches.Count -ne $suite.Expected[$method] -or @($matches | Where-Object { $_.outcome -ne 'Passed' }).Count -gt 0) {
                    throw "Unexpected result count or outcome for ${method}: $($matches.Count)."
                }
            }
            $expectedCount = ($suite.Expected.Values | Measure-Object -Sum).Sum
            if ($results.Count -ne $expectedCount) {
                throw "Unexpected $($suite.Name) total: $($results.Count), expected $expectedCount."
            }
            $summaries += [ordered]@{
                suite = $suite.Name
                project = $suite.Project
                expected = $expectedCount
                passed = @($results | Where-Object { $_.outcome -eq 'Passed' }).Count
                failed = @($results | Where-Object { $_.outcome -eq 'Failed' }).Count
                resultFile = $resultFile
            }
        }
    }
    finally {
        Pop-Location
    }

    $report = [ordered]@{
        sourceCommit = '4271d88e0aebf3d04f188f1334c2220d80555ef6'
        runtime = 'Microsoft.NETCore.App 10.0.12'
        sdk = $sdkVersion
        suites = $summaries
        totalPassed = ($summaries | ForEach-Object { $_['passed'] } | Measure-Object -Sum).Sum
    }
    $report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'summary.json') -Encoding UTF8
    $report | ConvertTo-Json -Depth 8
}
finally {
    & subst $drive /D | Out-Null
}
