param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum query oracle requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$from=@();$to=@();$values=[Collections.Generic.HashSet[long]]::new()
foreach($value in @([double]::NaN,[double]::NegativeInfinity,[double]::PositiveInfinity,[double]::MinValue,[double]::MaxValue,-657435.0,-657434.99999999,-657434.0,-2.75,-2.5,-2.25,-2.0,-1.75,-1.5,-1.25,-1.0,-0.75,-0.5,-0.25,-0.0,0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0,2.25,2.5,2.75,2958465.0,2958465.99999999,2958466.0)){
 foreach($sample in @($value,[Math]::BitDecrement($value),[Math]::BitIncrement($value))){[void]$values.Add([BitConverter]::DoubleToInt64Bits($sample))}
}
foreach($millis in @(-86400001,-86400000,-86399999,-2,-1,0,1,2,86399999,86400000,86400001)){
 foreach($delta in @(-0.500000001,-0.5,-0.499999999,0.499999999,0.5,0.500000001)){
  [void]$values.Add([BitConverter]::DoubleToInt64Bits(($millis+$delta)/86400000.0))
 }
}
foreach($bits in ($values|Sort-Object)){
 try{
  $date=[DateTime]::FromOADate([BitConverter]::Int64BitsToDouble($bits))
  try{$roundTrip=[ordered]@{bits=[BitConverter]::DoubleToInt64Bits($date.ToOADate()).ToString()}}catch{$roundTrip=Failure $_}
  $result=[ordered]@{ticks=$date.Ticks.ToString();kind=$date.Kind.ToString();roundTrip=$roundTrip}
 }catch{$result=Failure $_}
 $from+=[ordered]@{bits=$bits.ToString();result=$result}
}
$ticks=[Collections.Generic.HashSet[long]]::new()
foreach($point in [long[]]@(0,1,9999,10000,863999999999,864000000000,31241376000000000,599264352000000000,3155378975999999999)){
 foreach($delta in [long[]]@(-10001,-10000,-9999,-1,0,1,9999,10000,10001)){
  if($point+$delta -ge 0 -and $point+$delta -le 3155378975999999999){[void]$ticks.Add($point+$delta)}
 }
}
foreach($value in ($ticks|Sort-Object)){foreach($kind in [Enum]::GetValues([DateTimeKind])){
 try{
  $date=[DateTime]::new($value,$kind);$oa=$date.ToOADate()
  try{$roundTrip=[ordered]@{ticks=[DateTime]::FromOADate($oa).Ticks.ToString()}}catch{$roundTrip=Failure $_}
  $result=[ordered]@{bits=[BitConverter]::DoubleToInt64Bits($oa).ToString();roundTrip=$roundTrip}
 }catch{$result=Failure $_}
 $to+=[ordered]@{ticks=$value.ToString();kind=$kind.ToString();result=$result}
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();fromOADate=$from;toOADate=$to;qualification='BOUNDED_OLE_AUTOMATION_REFERENCE; FULL_INTEROP_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned OLE Automation conversion reference: $($from.Count) imports and $($to.Count) exports"
