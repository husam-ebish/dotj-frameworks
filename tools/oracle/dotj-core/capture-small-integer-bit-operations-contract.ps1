param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
$offsets=[int[]]@(-2147483648,-65,-64,-33,-32,-31,-17,-16,-15,-9,-8,-7,-1,0,1,7,8,9,15,16,17,31,32,33,64,65,2147483647);$types=@()
foreach($numericType in @([sbyte],[byte],[uint16],[uint32])){
 if($numericType -eq [sbyte]){$values=[long[]](-128..127)}elseif($numericType -eq [byte]){$values=[long[]](0..255)}else{
  $bits=if($numericType -eq [uint16]){16}else{32};$max=([long]1 -shl $bits)-1;$set=[Collections.Generic.HashSet[long]]::new();[void]$set.Add(0);[void]$set.Add($max)
  foreach($bit in 0..($bits-1)){$power=[long]1 -shl $bit;foreach($value in @(($power-1),$power,($power+1))){if($value -ge 0 -and $value -le $max){[void]$set.Add($value)}}};$values=[long[]]@($set|Sort-Object)
 }
 $single=@{};foreach($name in @('LeadingZeroCount','TrailingZeroCount','PopCount','IsPow2','IsEvenInteger','IsOddInteger')){$single[$name]=$numericType.GetMethod($name,[type[]]@($numericType))}
 $left=$numericType.GetMethod('RotateLeft',[type[]]@($numericType,[int]));$right=$numericType.GetMethod('RotateRight',[type[]]@($numericType,[int]));$rows=@();$rotations=@()
 foreach($value in $values){
  $boxed=[Convert]::ChangeType($value,$numericType);$arguments=[object[]]@($boxed);$row=[ordered]@{value=$value}
  foreach($name in @('LeadingZeroCount','TrailingZeroCount','PopCount')){$row[$name]=[long]$single[$name].Invoke($null,$arguments)}
  foreach($name in @('IsPow2','IsEvenInteger','IsOddInteger')){$row[$name]=[bool]$single[$name].Invoke($null,$arguments)}
  $rows+=$row
  foreach($offset in $offsets){$arguments=[object[]]@($boxed,$offset);$rotations+=[ordered]@{value=$value;offset=$offset;left=[long]$left.Invoke($null,$arguments);right=[long]$right.Invoke($null,$arguments)}}
 }
 $types+=[ordered]@{fullName=$numericType.FullName;values=$rows;rotations=$rotations}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();offsets=$offsets;types=$types;qualification='BOUNDED_SMALL_INTEGER_BITS; OTHER_APIS_GENERIC_INTERFACES_AND_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 14)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned bit operations: $($types.Count) types"
