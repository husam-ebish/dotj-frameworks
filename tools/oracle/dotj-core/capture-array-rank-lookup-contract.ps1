param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum query oracle requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$rows=@()
$bases=@('System.Int32','System.String','System.TimeSpan','System.Globalization.TimeSpanStyles')
foreach($base in $bases){foreach($rank in 2..33){foreach($shape in @('array','pointerArray','arrayVector')){
 $suffix='['+(','*($rank-1))+']'
 $canonical=switch($shape){array {$base+$suffix};pointerArray {$base+'*'+$suffix};arrayVector {$base+$suffix+'[]'}}
 foreach($variant in @('canonical','lower')){foreach($ignoreCase in @($false,$true)){foreach($throwOnError in @($false,$true)){
  $query=if($variant -eq 'lower'){$canonical.ToLowerInvariant()}else{$canonical}
  try{$type=[Type]::GetType($query,$throwOnError,$ignoreCase)
   if($null -eq $type){$result=[ordered]@{name=$null}}
   else{$result=[ordered]@{name=$type.FullName;simpleName=$type.Name;arrayRank=$type.GetArrayRank();isSZArray=$type.IsSZArray;elementName=$type.GetElementType().FullName}}
  }catch{$result=Failure $_}
  $rows+=[ordered]@{base=$base;rank=$rank;shape=$shape;query=$query;ignoreCase=$ignoreCase;throwOnError=$throwOnError;result=$result}
 }}}
}}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();queries=$rows;qualification='BOUNDED_ARRAY_RANK_NAME_LOOKUP_REFERENCE; ALLOCATION_AND_GENERAL_GRAMMAR_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned array-rank name lookup: $($rows.Count) cases"
