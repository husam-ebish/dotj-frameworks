Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$javaRoot = Join-Path $repoRoot 'dotj-core\dotj-core-01'
$main = Join-Path $javaRoot 'src\main\java\org\dotj\internal\cancellation'
$tests = Join-Path $javaRoot 'src\test\java\org\dotj\internal\cancellation'
$classes = Join-Path $javaRoot 'build\test-classes'
New-Item -ItemType Directory -Force -Path $classes | Out-Null

$sources = @((Get-ChildItem -LiteralPath $main -Filter '*.java').FullName) +
    @((Get-ChildItem -LiteralPath $tests -Filter '*.java').FullName)
& javac -d $classes @sources
if ($LASTEXITCODE -ne 0) { throw 'WP-02 Java compilation failed.' }

$testNames = @(
    'CancellationStateTest',
    'CancellationOrderTest',
    'CancellationLateRegistrationTest',
    'CancellationStopFirstTest',
    'CancellationAggregateTest',
    'CancellationUnregisterTest',
    'CancellationCloseWaitTest',
    'CancellationSelfCloseTest',
    'CancellationAsyncTest',
    'CancellationResetTest',
    'CancellationLinkedTest',
    'CancellationTimerTest'
)
foreach ($name in $testNames) {
    & java -cp $classes "org.dotj.internal.cancellation.$name"
    if ($LASTEXITCODE -ne 0) { throw "WP-02 Java fixture failed: $name" }
}
Write-Output "PASS: $($testNames.Count) internal WP-02 Java fixtures"
