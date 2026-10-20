Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$main = Join-Path $repoRoot 'dotj-core\dotj-core-01\src\main\java'
$build = Join-Path $repoRoot 'dotj-core\dotj-core-01\build'
$classes = Join-Path $build 'internal-core-classes-v1'
$jarPath = Join-Path $build 'dotj-core-internal-v1.jar'
$manifestPath = Join-Path $repoRoot 'planning\stage-2\repos\dotj-core\evidence\internal-core-jar-v1.json'
$publicJar = Join-Path $repoRoot 'dotj-core\dotj-core-public\build\idisposable-v1\dotj-core-idisposable-v1.jar'
& python (Join-Path $repoRoot 'tools\oracle\dotj-core\build-idisposable-product.py')
if ($LASTEXITCODE -ne 0) { throw 'Public IDisposable dependency build failed.' }
New-Item -ItemType Directory -Force -Path $classes | Out-Null

$sources = @(Get-ChildItem -LiteralPath $main -Recurse -Filter '*.java' | Sort-Object FullName)
if ($sources.Count -ne 14) { throw "Expected fourteen internal Java source files, found $($sources.Count)." }
& javac --release 21 -classpath $publicJar -d $classes @($sources | ForEach-Object FullName)
if ($LASTEXITCODE -ne 0) { throw 'Internal Java compilation failed.' }

$classFiles = @(Get-ChildItem -LiteralPath $classes -Recurse -Filter '*.class')
if ($classFiles.Count -ne 15) { throw "Expected fifteen internal class files, found $($classFiles.Count)." }
& jar --create --file $jarPath --date=2026-10-20T00:00:00Z -C $classes .
if ($LASTEXITCODE -ne 0) { throw 'Internal JAR creation failed.' }
$entries = @(& jar --list --file $jarPath)
if ($LASTEXITCODE -ne 0) { throw 'Internal JAR listing failed.' }
if (@($entries | Where-Object { $_ -like 'System/*' -or $_ -like '*Test.class' }).Count -ne 0) {
    throw 'Internal JAR contains a public-name probe or test class.'
}
$result = [ordered]@{
    schemaVersion = 1
    purpose = 'Internal development bootstrap artifact; not a public .j product package'
    jdkVersion = (& javac -version 2>&1 | Select-Object -First 1).ToString()
    sourceCount = $sources.Count
    classCount = $classFiles.Count
    jarSha256 = (Get-FileHash -LiteralPath $jarPath -Algorithm SHA256).Hash.ToLowerInvariant()
    entries = $entries
    sourceHashes = @($sources | ForEach-Object {
        [ordered]@{
            path = $_.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
            sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    })
}
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
Write-Output "PASS: $($sources.Count) internal sources and $($classFiles.Count) classes in JDK-only JAR"
