param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum query oracle requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$rows=@()
foreach($type in @([object],[string],[int],[void],[Enum],[ValueType],[DayOfWeek].MakeArrayType(),[DayOfWeek].MakePointerType(),[DayOfWeek].MakeByRefType())){
 foreach($op in @('GetEnumNames','GetEnumValues','GetEnumValuesAsUnderlyingType','GetEnumUnderlyingType','GetEnumName','IsEnumDefined')){
  foreach($value in @($null,1,'None',[double]1,$true,[DayOfWeek]::Monday,[long]1)){
   if($op -notin @('GetEnumName','IsEnumDefined') -and $null -ne $value){continue}
   try{$result=switch($op){GetEnumNames {$type.GetEnumNames()};GetEnumValues {$type.GetEnumValues()};GetEnumValuesAsUnderlyingType {$type.GetEnumValuesAsUnderlyingType()};GetEnumUnderlyingType {$type.GetEnumUnderlyingType()};GetEnumName {$type.GetEnumName($value)};IsEnumDefined {$type.IsEnumDefined($value)}};throw 'unexpected success'}catch{$e=$_.Exception.GetBaseException();$rows+=@{type=$type.FullName;operation=$op;value=$value;kind=$(if($null -eq $value){'null'}elseif($value -is [double]){'double'}elseif($value -is [long]){'long'}elseif($value -is [DayOfWeek]){'day'}else{'other'});exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
  }
 }
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();queries=$rows;qualification='BOUNDED_NON_ENUM_RECEIVER_ERROR_PRECEDENCE_REFERENCE'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned non-enum receivers: $($rows.Count) failures"
