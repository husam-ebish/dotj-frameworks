param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum query oracle requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
if([TimeZoneInfo]::Local.Id -ne 'W. Europe Standard Time'){throw 'Selected conversion overlap reference requires W. Europe Standard Time.'}
$originalCulture=[Globalization.CultureInfo]::CurrentCulture
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
try{
$samples=@();$rows=@();$iface=[IConvertible]
foreach($ticks in [long[]]@(0,1,863999999999,864000000000,599264352000000000,621355968000000000,638447616000000000,3155378975999999999)){foreach($kind in [Enum]::GetValues([DateTimeKind])){
 $samples+=@{inputTicks=$ticks;inputKind=$kind.ToString();route='direct';value=[DateTime]::new($ticks,$kind)}
}}
foreach($date in @(@(2024,3,31),@(2024,10,27),@(2026,3,29),@(2026,10,25))){foreach($hour in 0..2){
 $utc=[DateTime]::new($date[0],$date[1],$date[2],$hour,30,0,[DateTimeKind]::Utc)
 $samples+=@{inputTicks=$utc.Ticks;inputKind='Utc';route='viaLocal';value=$utc.ToLocalTime()}
}}
$operations=@('GetTypeCode','ToDateTime','ToString','ToBoolean','ToChar','ToSByte','ToByte','ToInt16','ToUInt16','ToInt32','ToUInt32','ToInt64','ToUInt64','ToSingle','ToDouble','ToDecimal')
$targets=@('System.DateTime','System.String','System.Object','System.ValueType','System.Enum','System.Boolean','System.Char','System.SByte','System.Byte','System.Int16','System.UInt16','System.Int32','System.UInt32','System.Int64','System.UInt64','System.Single','System.Double','System.Decimal','System.DBNull','System.TimeSpan',$null)
foreach($sample in $samples){
 foreach($op in $operations){
  $method=$iface.GetMethod($op)
  if($op -eq 'GetTypeCode'){$arguments=[object[]]@()}else{$arguments=[object[]]@($null)}
  try{
   $output=$method.Invoke($sample.value,$arguments)
   if($output -is [DateTime]){
    $result=[ordered]@{ticks=$output.Ticks.ToString();kind=$output.Kind.ToString()}
    if($sample.route -eq 'viaLocal'){$result.binary=$output.ToBinary().ToString();$result.utcTicks=$output.ToUniversalTime().Ticks.ToString()}
   }elseif($output -is [TypeCode]){$result=[ordered]@{typeCode=[int]$output}}else{$result=[ordered]@{text=$output}}
  }catch{$result=Failure $_}
  $rows+=[ordered]@{inputTicks=$sample.inputTicks.ToString();inputKind=$sample.inputKind;route=$sample.route;operation=$op;result=$result}
 }
 foreach($targetName in $targets){
  $target=if($null -eq $targetName){$null}else{[Type]::GetType($targetName,$true)}
  try{
   $output=$iface.GetMethod('ToType').Invoke($sample.value,[object[]]@($target,$null))
   if($output -is [DateTime]){
    $result=[ordered]@{ticks=$output.Ticks.ToString();kind=$output.Kind.ToString()}
    if($sample.route -eq 'viaLocal'){$result.binary=$output.ToBinary().ToString();$result.utcTicks=$output.ToUniversalTime().Ticks.ToString()}
   }else{$result=[ordered]@{text=$output}}
  }catch{$result=Failure $_}
  $rows+=[ordered]@{inputTicks=$sample.inputTicks.ToString();inputKind=$sample.inputKind;route=$sample.route;operation='ToType';target=$targetName;result=$result}
 }
}
}finally{[Globalization.CultureInfo]::CurrentCulture=$originalCulture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=[TimeZoneInfo]::Local.Id;javaZoneProfile='Europe/Zurich';cultureProfile='Invariant';queries=$rows;qualification='BOUNDED_DATETIME_CONVERTIBLE_REFERENCE; HISTORICAL_ZONE_FULL_PROVIDER_AND_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned DateTime IConvertible: $($rows.Count) cases"
