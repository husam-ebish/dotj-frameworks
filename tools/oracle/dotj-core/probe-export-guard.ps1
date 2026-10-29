param([string]$Repository,[string]$CasesPath,[string]$OutputPath,[string]$WrapperPath,[string]$OriginalWrapperPath)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
function ExtractGuard([string]$Path,[bool]$Original){
 $s=[IO.File]::ReadAllText($Path).Replace("`r`n","`n")
 $phase=$s.IndexOf('    if ($ExportEvidence) {')
 if($phase -lt 0){throw 'Export phase not found'}
 $marker=if($Original){'        foreach ($relative in $changed) {'}else{'        # Keep native command lines bounded'}
 $start=$s.IndexOf($marker,$phase)
 $end=$s.IndexOf('        foreach ($relative in $changed) { Copy-Item',$start)
 if($start -lt 0 -or $end -le $start){throw 'Evidence guard boundaries not found'}
 return [scriptblock]::Create($s.Substring($start,$end-$start))
}
$script:Guard=ExtractGuard $WrapperPath $false
$script:OriginalGuard=$null
if($OriginalWrapperPath){$script:OriginalGuard=ExtractGuard $OriginalWrapperPath $true}
$cases=Get-Content -LiteralPath $CasesPath -Encoding UTF8 -Raw|ConvertFrom-Json
function Original([string]$repository,[string[]]$changed){& $script:OriginalGuard}
function Batched([string]$repository,[string[]]$changed){& $script:Guard}
$results=[Collections.Generic.List[object]]::new()
foreach($case in $cases){
 $blocked=$false;$message=$null;$clock=[Diagnostics.Stopwatch]::StartNew()
 try{
  if($case.route -eq 'original'){Original $Repository $case.paths}
  else{Batched $Repository $case.paths}
 }catch{$blocked=$true;$message=$_.Exception.Message}
 $clock.Stop()
 $results.Add([ordered]@{name=$case.name;route=$case.route;blocked=$blocked;message=$message;seconds=$clock.Elapsed.TotalSeconds})
}
[IO.File]::WriteAllText($OutputPath,(ConvertTo-Json -InputObject $results.ToArray() -Depth 5),[Text.UTF8Encoding]::new($false))
