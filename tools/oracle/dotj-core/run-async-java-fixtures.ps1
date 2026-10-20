Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$javaRoot = Join-Path $repoRoot 'dotj-core\dotj-core-01'
$main = Join-Path $javaRoot 'src\main\java\org\dotj\internal\async'
$tests = Join-Path $javaRoot 'src\test\java\org\dotj\internal\async'
$classes = Join-Path $javaRoot 'build\async-test-classes'
New-Item -ItemType Directory -Force -Path $classes | Out-Null

$sources = @((Get-ChildItem -LiteralPath $main -Filter '*.java').FullName) +
    @((Get-ChildItem -LiteralPath $tests -Filter '*.java').FullName)
& javac --release 21 -d $classes @sources
if ($LASTEXITCODE -ne 0) { throw 'Internal async Java compilation failed.' }
& java -cp $classes 'org.dotj.internal.async.AsyncStateTest'
if ($LASTEXITCODE -ne 0) { throw 'Internal async Java fixture failed.' }
& java -cp $classes 'org.dotj.internal.async.AsyncCompletionRaceTest'
if ($LASTEXITCODE -ne 0) { throw 'Internal async race fixture failed.' }
& java -cp $classes 'org.dotj.internal.async.AsyncWaitTest'
if ($LASTEXITCODE -ne 0) { throw 'Internal async wait fixture failed.' }
