Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$javaRoot = Join-Path $repoRoot 'dotj-core\dotj-core-01'
$classes = Join-Path $javaRoot 'build\test-classes'
New-Item -ItemType Directory -Force -Path $classes | Out-Null

$sources = @(
    'src/main/java/org/dotj/internal/ownership/OwnedResources.java'
    'src/main/java/org/dotj/internal/context/ContextSnapshot.java'
    'src/main/java/org/dotj/internal/context/ContextTransfer.java'
    'src/main/java/org/dotj/internal/types/TypeIdentity.java'
    'src/test/java/org/dotj/internal/ownership/OwnedResourcesTest.java'
    'src/test/java/org/dotj/internal/ownership/CallerOwnershipTest.java'
    'src/test/java/org/dotj/internal/ownership/OwnedResourcesRaceTest.java'
    'src/test/java/org/dotj/internal/ownership/OwnedResourcesReentrancyTest.java'
    'src/test/java/org/dotj/internal/ownership/OwnedResourcesBoundaryTest.java'
    'src/test/java/org/dotj/internal/context/ContextSnapshotTest.java'
    'src/test/java/org/dotj/internal/context/ContextTransferTest.java'
    'src/test/java/org/dotj/internal/context/ContextIsolationTest.java'
    'src/test/java/org/dotj/internal/context/ContextSnapshotBoundaryTest.java'
    'src/test/java/org/dotj/internal/types/LoadableType.java'
    'src/test/java/org/dotj/internal/types/TypeIdentityTest.java'
    'src/test/java/org/dotj/internal/types/TypeIdentityLoaderTest.java'
    'src/test/java/org/dotj/internal/types/TypeIdentityBoundaryTest.java'
) | ForEach-Object { Join-Path $javaRoot $_ }

& javac -d $classes @sources
if ($LASTEXITCODE -ne 0) { throw 'Java fixture compilation failed.' }

$javaTests = @(
    'org.dotj.internal.ownership.OwnedResourcesTest'
    'org.dotj.internal.ownership.CallerOwnershipTest'
    'org.dotj.internal.ownership.OwnedResourcesRaceTest'
    'org.dotj.internal.ownership.OwnedResourcesReentrancyTest'
    'org.dotj.internal.ownership.OwnedResourcesBoundaryTest'
    'org.dotj.internal.context.ContextSnapshotTest'
    'org.dotj.internal.context.ContextTransferTest'
    'org.dotj.internal.context.ContextIsolationTest'
    'org.dotj.internal.context.ContextSnapshotBoundaryTest'
    'org.dotj.internal.types.TypeIdentityTest'
    'org.dotj.internal.types.TypeIdentityLoaderTest'
    'org.dotj.internal.types.TypeIdentityBoundaryTest'
)
foreach ($test in $javaTests) {
    & java -cp $classes $test
    if ($LASTEXITCODE -ne 0) { throw "Java fixture failed: $test" }
}

$dotnetProjects = @(
    'tools/oracle/dotj-core/disposal-metadata/DisposalMetadataOracle.csproj'
    'tools/oracle/dotj-core/disposal-behavior/DisposalBehaviorOracle.csproj'
    'tools/oracle/dotj-core/di-ownership/DiOwnershipOracle.csproj'
    'tools/oracle/dotj-core/context-flow/ContextFlowOracle.csproj'
    'tools/oracle/dotj-core/type-identity/TypeIdentityOracle.csproj'
)
foreach ($project in $dotnetProjects) {
    & dotnet run --project (Join-Path $repoRoot $project) --configuration Release --no-launch-profile
    if ($LASTEXITCODE -ne 0) { throw "Oracle failed: $project" }
}

Write-Output "PASS: $($javaTests.Count) Java fixtures and $($dotnetProjects.Count) .NET oracles"
