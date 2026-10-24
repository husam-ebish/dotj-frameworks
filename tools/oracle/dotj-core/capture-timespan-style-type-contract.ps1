param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Style enum Type oracle requires pinned CoreLib.'}
$type=[Globalization.TimeSpanStyles]
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$metadata=[ordered]@{name=$type.FullName;simpleName=$type.Name;namespace=$type.Namespace;baseType=$type.BaseType.FullName
    isClass=$type.IsClass;isValueType=$type.IsValueType;isEnum=$type.IsEnum;isSealed=$type.IsSealed;isPrimitive=$type.IsPrimitive
    typeCode=[int][Type]::GetTypeCode($type);underlyingType=$type.GetEnumUnderlyingType().FullName;names=$type.GetEnumNames()
    values=@($type.GetEnumValues()|ForEach-Object{[int]$_});underlyingValues=$type.GetEnumValuesAsUnderlyingType()
    omittedInterfaces=@($type.GetInterfaces()|ForEach-Object{$_.FullName})}
$descriptors=@();foreach($value in @([int]::MinValue,-1,0,1,2,3,[int]::MaxValue)){
    $descriptors+=@{kind='int';value=$value;object=$value};$descriptors+=@{kind='style';value=$value;object=[Enum]::ToObject($type,[int]$value)}
}
foreach($text in @('None','none','AssumeNegative','assumenegative','2','None, AssumeNegative')){$descriptors+=@{kind='string';value=$text;object=$text}}
$descriptors+=@{kind='null';value=$null;object=$null}
$queries=@();foreach($item in $descriptors){
    try{$name=[ordered]@{name=$type.GetEnumName($item.object)}}catch{$name=Failure $_}
    try{$defined=[ordered]@{boolean=$type.IsEnumDefined($item.object)}}catch{$defined=Failure $_}
    $queries+=[ordered]@{kind=$item.kind;value=$item.value;nameResult=$name;definedResult=$defined}
}
$targets=@($type,[object],[ValueType],[Enum],[int],[Globalization.NumberStyles])
$assignability=@();foreach($target in $targets){$assignability+=[ordered]@{target=$target.FullName;result=$target.IsAssignableFrom($type)}}
$instances=@();foreach($value in @([int]::MinValue,-1,0,1,2,3,[int]::MaxValue)){foreach($target in $targets){
    $instances+=[ordered]@{value=$value;target=$target.FullName;result=$target.IsInstanceOfType([Enum]::ToObject($type,[int]$value))}
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();metadata=$metadata;queries=$queries;assignability=$assignability;instances=$instances
    qualification='SELECTED_STYLE_ENUM_TYPE_NAMES_VALUES_AND_QUERIES_REFERENCE; OMITTED_INTERFACES_DISPATCH_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned style enum Type reference: $($queries.Count) name/defined query pairs and $($instances.Count) instance cases"
