param(
 [Parameter(Mandatory=$true)][ValidateSet('baseline-compile','baseline-runtime')][string]$Operation,
 [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$SourceLockSha256,
 [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ReviewSha256
)
# Invoke only through the reviewed Windows PowerShell executable. This minimum
# interpreter bootstrap is measured separately from the Python-owned900 scope.
$ErrorActionPreference='Stop'
$watch=[Diagnostics.Stopwatch]::StartNew()
$base='D:\AI\Implementation\dotj Frameworks'
$profile=Join-Path $base 'worktrees\dotj-build-ordering-conditions-v1\tools\oracle\dotj-build\condition-ordering-jdk-v1'
$work=Join-Path $base 'agents\batch2518-build-ordering-preparation-v1\baseline-red-jdk-v1'
$pythonRoot=Join-Path $base 'toolchains\python-3.13.9'
$hostPath='C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
function Assert-Regular([string]$Path) {
 $item=Get-Item -LiteralPath $Path -Force
 if($item.PSIsContainer){throw 'regular file required'}
 $cursor=$item
 while($null -ne $cursor){
  if(($cursor.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0){throw 'reparse path forbidden'}
  if($cursor -is [IO.FileInfo]){$cursor=$cursor.Directory}else{$cursor=$cursor.Parent}
 }
 return $item
}
function Assert-Pin($d) {
 $item=Assert-Regular $d.path
 if($item.Length -ne $d.sizeBytes -or (Get-FileHash -LiteralPath $d.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $d.sha256){throw ('descriptor mismatch '+$d.path)}
}
if([Diagnostics.Process]::GetCurrentProcess().MainModule.FileName -ne $hostPath){throw 'reviewed Windows PowerShell host required'}
$sourcePath=Join-Path $profile 'source-lock.json'
$null=Assert-Regular $sourcePath
if((Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $SourceLockSha256){throw 'external source lock identity'}
$lock=Get-Content -Raw -LiteralPath $sourcePath|ConvertFrom-Json
Assert-Pin $lock.externalBootstrapHost
$actual=@(Get-ChildItem -LiteralPath $profile -Recurse -Force)
if(@($actual|Where-Object {($_.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0}).Count){throw 'profile reparse'}
$actualFiles=@($actual|Where-Object {-not $_.PSIsContainer}|ForEach-Object {$_.FullName}|Sort-Object)
$expectedFiles=@(@($lock.files|ForEach-Object {$_.path})+$sourcePath|Sort-Object)
if(Compare-Object $actualFiles $expectedFiles){throw 'exact launcher profile inventory'}
# Close every imported helper/bootstrap/manifest before any selected Python.
foreach($d in $lock.files){Assert-Pin $d}
Assert-Pin $lock.guard
$manifest=Get-Content -Raw -LiteralPath (Join-Path $profile 'python-bootstrap-inputs.json')|ConvertFrom-Json
if($manifest.root -ne $pythonRoot -or $manifest.files.Count -ne 34 -or $manifest.siteEnabled -ne $false){throw 'exact selected Python manifest'}
$payload=@(Get-ChildItem -LiteralPath $pythonRoot -Recurse -Force)
if(@($payload|Where-Object {($_.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0}).Count){throw 'Python reparse'}
$actualFiles=@($payload|Where-Object {-not $_.PSIsContainer}|ForEach-Object {$_.FullName}|Sort-Object)
$expectedFiles=@($manifest.files|ForEach-Object {$_.path}|Sort-Object)
if($actualFiles.Count -ne 34 -or (Compare-Object $actualFiles $expectedFiles)){throw 'exact selected Python membership'}
foreach($d in $manifest.files){Assert-Pin $d}
$active=@(Get-Content -LiteralPath (Join-Path $pythonRoot 'python313._pth')|Where-Object {$_.Trim() -and -not $_.Trim().StartsWith('#')}|ForEach-Object {$_.Trim()})
if(($active -join '|') -ne 'python313.zip|.'){throw 'active Python paths and site disabled'}
$reviewPath=Join-Path $base ('orchestration\two-frameworks\batch2518-jdk-'+$Operation+'-attempt01-review-v1.json')
$null=Assert-Regular $reviewPath
if((Get-FileHash -LiteralPath $reviewPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ReviewSha256){throw 'exact independent operation review'}
$review=Get-Content -Raw -LiteralPath $reviewPath|ConvertFrom-Json
if($review.sourceLockSha256 -ne $SourceLockSha256 -or $review.operation -ne $Operation -or $review.jdkInvocationApproved -ne $true -or $review.invocationCountApproved -ne 1){throw 'separate actual operation approval required'}
$bootRoot=Join-Path $work 'bootstrap'
New-Item -ItemType Directory -Path $bootRoot -Force|Out-Null
$recordPath=Join-Path $bootRoot ($Operation+'-attempt01.json')
if(Test-Path -LiteralPath $recordPath){throw 'fresh single-use bootstrap; no automatic retry'}
$record=[ordered]@{schemaVersion=1;status='EXTERNAL_PYTHON_BOOTSTRAP_VERIFIED';sourceLockSha256=$SourceLockSha256;reviewSha256=$ReviewSha256;operation=$Operation;pythonFiles=34;activePth=$active;siteEnabled=$false;seconds=$watch.Elapsed.TotalSeconds;ownershipTimingIncludesBootstrap=$false;host=$lock.externalBootstrapHost;osBoundary='Windows System32 APIs; no Windows payload scan'}
[IO.File]::WriteAllText($recordPath,($record|ConvertTo-Json -Depth 6),[Text.UTF8Encoding]::new($false))
$bootstrapSha=(Get-FileHash -LiteralPath $recordPath -Algorithm SHA256).Hash.ToLowerInvariant()
$operationHomePath=Join-Path $work ($Operation+'-attempt01\home')
$env:HOME=$operationHomePath;$env:USERPROFILE=$operationHomePath;$env:HOMEDRIVE=[IO.Path]::GetPathRoot($operationHomePath).TrimEnd('\');$env:HOMEPATH=$operationHomePath.Substring($env:HOMEDRIVE.Length)
$env:TEMP=Join-Path $work ($Operation+'-attempt01\tmp');$env:TMP=$env:TEMP
$env:PYTHONDONTWRITEBYTECODE='1';$env:PYTHONNOUSERSITE='1';$env:PYTHONUTF8='1'
$env:APPDATA=Join-Path $operationHomePath 'AppData\Roaming';$env:LOCALAPPDATA=Join-Path $operationHomePath 'AppData\Local'
# The fixed Python outer validates the complete review and obtains owned Job
# authority before full stage checks. No caller argv/deadline reaches a JDK.
& (Join-Path $pythonRoot 'python.exe') -B (Join-Path $profile 'jdk_runner.py') ('--operation='+$Operation) ('--source-lock-sha256='+$SourceLockSha256) ('--review-sha256='+$ReviewSha256) ('--bootstrap-sha256='+$bootstrapSha)
exit $LASTEXITCODE
