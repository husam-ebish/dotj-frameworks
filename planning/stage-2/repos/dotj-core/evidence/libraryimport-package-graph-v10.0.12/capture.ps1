param(
    [Parameter(Mandatory = $true)]
    [string] $SourceRoot,
    [Parameter(Mandatory = $true)]
    [string] $PackageRoot
)

$ErrorActionPreference = 'Stop'
$evidenceRoot = $PSScriptRoot
$assetsPath = Join-Path $SourceRoot 'artifacts/obj/LibraryImportGenerator/project.assets.json'
$assets = Get-Content -LiteralPath $assetsPath -Raw | ConvertFrom-Json
$targetName = 'netstandard2.0'
$target = $assets.targets.PSObject.Properties[$targetName].Value
if ($null -eq $target) { throw "Missing $targetName target" }
$utf8 = New-Object System.Text.UTF8Encoding($false)
$snapshotPath = Join-Path $evidenceRoot 'project.assets.json.raw'
Copy-Item -LiteralPath $assetsPath -Destination $snapshotPath -Force

$packages = @()
$projects = @()
foreach ($entry in $target.PSObject.Properties) {
    if ($entry.Value.type -eq 'project') {
        $projects += $entry.Name
        continue
    }
    if ($entry.Value.type -ne 'package') { continue }
    $parts = $entry.Name.Split('/')
    $id = $parts[0]
    $version = $parts[1]
    $cachePath = Join-Path $PackageRoot ($id.ToLowerInvariant() + '/' + $version)
    if (!(Test-Path -LiteralPath $cachePath)) { throw "Package cache missing: $($entry.Name)" }
    $nuspec = @(Get-ChildItem -LiteralPath $cachePath -Filter '*.nuspec' -File)
    if ($nuspec.Count -ne 1) { throw "Expected one nuspec: $($entry.Name)" }
    $packageSnapshotRoot = Join-Path $evidenceRoot ('packages/' + $id.ToLowerInvariant() + '/' + $version)
    New-Item -ItemType Directory -Path $packageSnapshotRoot -Force | Out-Null
    Copy-Item -LiteralPath $nuspec[0].FullName -Destination (Join-Path $packageSnapshotRoot $nuspec[0].Name) -Force
    [xml] $nuspecXml = Get-Content -LiteralPath $nuspec[0].FullName -Raw
    $metadata = $nuspecXml.package.metadata
    $noticeFiles = @()
    $candidates = @(Get-ChildItem -LiteralPath $cachePath -Recurse -File | Where-Object { $_.Name -match '(?i)(license|licence|notice|third.?party|copyright|credits)' } | Sort-Object FullName)
    foreach ($candidate in $candidates) {
        $relative = $candidate.FullName.Substring($cachePath.Length).TrimStart([char] 92, [char] 47).Replace([char] 92, [char] 47)
        $destination = Join-Path $packageSnapshotRoot $relative
        New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $candidate.FullName -Destination $destination -Force
        $noticeFiles += [ordered]@{
            path = 'packages/' + $id.ToLowerInvariant() + '/' + $version + '/' + $relative
            bytes = $candidate.Length
            sha256 = (Get-FileHash -LiteralPath $candidate.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    }
    $dependencies = @()
    if ($entry.Value.dependencies) {
        foreach ($dependency in $entry.Value.dependencies.PSObject.Properties) {
            $dependencies += [ordered]@{ id = $dependency.Name; versionRange = [string] $dependency.Value }
        }
    }
    $packages += [ordered]@{
        id = $id
        version = $version
        sha512FromAssets = $assets.libraries.PSObject.Properties[$entry.Name].Value.sha512
        dependencies = $dependencies
        nuspec = [ordered]@{
            path = 'packages/' + $id.ToLowerInvariant() + '/' + $version + '/' + $nuspec[0].Name
            sha256 = (Get-FileHash -LiteralPath $nuspec[0].FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            licenseType = if ($metadata.license) { [string] $metadata.license.type } else { $null }
            licenseValue = if ($metadata.license) { [string] $metadata.license.'#text' } else { $null }
            licenseUrl = if ($metadata.licenseUrl) { [string] $metadata.licenseUrl } else { $null }
        }
        noticeLikeFiles = $noticeFiles
    }
}
$manifest = [ordered]@{
    schemaVersion = 1
    recordedDate = '2026-10-20'
    scope = 'LibraryImportGenerator resolved netstandard2.0 build-time package graph from pinned dotnet/runtime v10.0.12 source extraction'
    status = 'INVENTORY ONLY; notice applicability and redistribution rights unresolved'
    sourceTag = 'v10.0.12'
    sourceCommit = '4271d88e0aebf3d04f188f1334c2220d80555ef6'
    sourceProject = 'src/libraries/System.Runtime.InteropServices/gen/LibraryImportGenerator/LibraryImportGenerator.csproj'
    targetFramework = $targetName
    assetsSnapshot = [ordered]@{
        path = 'project.assets.json.raw'
        bytes = (Get-Item -LiteralPath $assetsPath).Length
        sha256 = (Get-FileHash -LiteralPath $assetsPath -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    packageFolderFromAssets = @($assets.packageFolders.PSObject.Properties.Name)
    projectFileDependencyGroup = @($assets.projectFileDependencyGroups.PSObject.Properties[$targetName].Value)
    projectReferencesInTarget = $projects
    resolvedPackageCount = $packages.Count
    noticeLikeFileCount = @($packages | ForEach-Object { $_.noticeLikeFiles }).Count
    packages = $packages
    limits = @(
        'The filename scan selects files containing license, licence, notice, third-party, copyright or credits in the extracted package cache. Embedded notices and other filenames were not assessed.',
        'Nuspec declarations and extracted files are evidence of package contents, not a legal determination or file-to-notice mapping.',
        'This is the restored LibraryImportGenerator target graph. It does not establish the complete upstream runtime build graph or official release build provenance.'
    )
}
[System.IO.File]::WriteAllText((Join-Path $evidenceRoot 'manifest.json'), ($manifest | ConvertTo-Json -Depth 30), $utf8)
Write-Output "Packages: $($packages.Count); notice-like files: $($manifest.noticeLikeFileCount); project references: $($projects.Count)"
