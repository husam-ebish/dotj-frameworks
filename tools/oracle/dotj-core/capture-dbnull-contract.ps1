param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'DBNull reference requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
function Result($output){
 if([object]::ReferenceEquals($output,[DBNull]::Value)){return [ordered]@{singleton=$true}}
 if($output -is [TypeCode]){return [ordered]@{typeCode=[int]$output}}
 if($output -is [bool]){return [ordered]@{boolean=$output}}
 return [ordered]@{text=$output}
}
$value=[DBNull]::Value;$type=[DBNull];$rows=@()
foreach($op in @('GetTypeCode','ToDateTime','ToString','ToBoolean','ToChar','ToSByte','ToByte','ToInt16','ToUInt16','ToInt32','ToUInt32','ToInt64','ToUInt64','ToSingle','ToDouble','ToDecimal')){
 if($op -eq 'GetTypeCode'){$arguments=[object[]]@()}else{$arguments=[object[]]@($null)}
 try{$result=Result ([IConvertible].GetMethod($op).Invoke($value,$arguments))}catch{$result=Failure $_}
 $rows+=[ordered]@{operation=$op;result=$result}
}
foreach($name in @('System.Boolean','System.Char','System.SByte','System.Byte','System.Int16','System.UInt16','System.Int32','System.UInt32','System.Int64','System.UInt64','System.Single','System.Double','System.Decimal','System.String','System.Object','System.DateTime','System.DBNull','System.Enum','System.ValueType','System.IConvertible','System.TimeSpan','System.Int32[]',$null)){
 $target=if($null -eq $name){$null}else{[Type]::GetType($name,$true)}
 try{$result=Result ([IConvertible].GetMethod('ToType').Invoke($value,[object[]]@($target,$null)))}catch{$result=Failure $_}
 $rows+=[ordered]@{operation='ToType';target=$name;result=$result}
}
$rows+=[ordered]@{operation='ToStringNoProvider';result=(Result ($value.ToString()))}
foreach($entry in @(@{name='null';value=$null},@{name='self';value=$value},@{name='string';value=''},@{name='object';value=[object]::new()})){
 $rows+=[ordered]@{operation='Equals';argument=$entry.name;result=(Result ($value.Equals($entry.value)))}
}
foreach($state in @(0,255)){
 $context=[Runtime.Serialization.StreamingContext]::new([Runtime.Serialization.StreamingContextStates]$state)
 try{$output=$type.GetMethod('GetObjectData').Invoke($value,[object[]]@($null,$context));throw 'Unexpected serialization success'}catch{$result=Failure $_}
 $rows+=[ordered]@{operation='NullSerializationInfo';state=$state;result=$result}
}
$metadata=[ordered]@{name=$type.FullName;baseType=$type.BaseType.FullName;isClass=$type.IsClass;isSealed=$type.IsSealed;isValueType=$type.IsValueType;isSerializable=$type.IsSerializable;typeCode=[int][Type]::GetTypeCode($type);interfaces=@($type.GetInterfaces()|ForEach-Object{$_.FullName}|Sort-Object)}
$relations=@();foreach($target in @([object],[DBNull],[IConvertible],[Runtime.Serialization.ISerializable],[string],[ValueType],[Enum],[int])){
 $relations+=[ordered]@{target=$target.FullName;assignable=$target.IsAssignableFrom($type);instance=$target.IsInstanceOfType($value)}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();queries=$rows;metadata=$metadata;relations=$relations;qualification='BOUNDED_DBNULL_SINGLETON_CONVERSION_AND_NULL_SERIALIZATION_REFERENCE; NONNULL_SERIALIZATION_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned DBNull reference: $($rows.Count) calls and $($relations.Count) relation pairs"
