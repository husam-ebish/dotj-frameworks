param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$profiles=@(@{type=[sbyte];values=[long[]]@(-128,-127,-100,-42,-1,0,1,9,10,42,99,100,126,127)},@{type=[byte];values=[long[]]@(0,1,2,7,9,10,42,99,100,127,128,200,254,255)},@{type=[uint16];values=[long[]]@(0,1,7,9,10,42,99,100,127,255,256,32767,65534,65535)},@{type=[uint32];values=[long[]]@(0,1,9,10,42,99,100,255,65535,65536,2147483647,2147483648,4294967294,4294967295)})
$types=@()
foreach($numericProfile in $profiles){
 $numericType=$numericProfile.type;$values=$numericProfile.values;$bounds=@($values[0],$values[1],$values[4],$values[7],$values[10],$values[12],$values[13]);$pairs=@();$clamps=@()
 $min=$numericType.GetMethod('Min',[type[]]@($numericType,$numericType));$max=$numericType.GetMethod('Max',[type[]]@($numericType,$numericType));$clamp=$numericType.GetMethod('Clamp',[type[]]@($numericType,$numericType,$numericType))
 foreach($x in $values){foreach($y in $values){
  $arguments=[object[]]@([Convert]::ChangeType($x,$numericType),[Convert]::ChangeType($y,$numericType))
  $pairs+=[ordered]@{x=$x;y=$y;min=[long]$min.Invoke($null,$arguments);max=[long]$max.Invoke($null,$arguments)}
 }}
 foreach($value in $values){foreach($lower in $bounds){foreach($upper in $bounds){
  $arguments=[object[]]@([Convert]::ChangeType($value,$numericType),[Convert]::ChangeType($lower,$numericType),[Convert]::ChangeType($upper,$numericType))
  try{$result=[ordered]@{value=[long]$clamp.Invoke($null,$arguments)}}catch{$result=Failure $_}
  $clamps+=[ordered]@{value=$value;lower=$lower;upper=$upper;result=$result}
 }}}
 $types+=[ordered]@{fullName=$numericType.FullName;pairs=$pairs;clamps=$clamps}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();types=$types;qualification='BOUNDED_SMALL_INTEGER_MIN_MAX_CLAMP; OTHER_ARITHMETIC_GENERIC_INTERFACES_AND_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 14)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned Min/Max/Clamp: $($types.Count) types, 3528 pair/clamp groups"
