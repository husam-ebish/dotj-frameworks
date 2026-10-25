param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum formatter requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$enumType=[Reflection.CallingConventions];$method=[Enum].GetMethod('HasFlag',[type[]]@([Enum]));$targets=@()
$flagValues=[int[]]@((@([int]::MinValue,-1)+(0..255)+@(256,257,65535,[int]::MaxValue)+@([Enum]::GetValues($enumType)|ForEach-Object {[Convert]::ToInt32($_,[Globalization.CultureInfo]::InvariantCulture)}))|Sort-Object -Unique)
foreach($number in $flagValues){$targets+=@{kind='style';value=[int]$number}}
$targets+=@{kind='null'}
foreach($typeName in @('System.Globalization.TimeSpanStyles','System.Globalization.DateTimeStyles','System.DateTimeKind','System.DayOfWeek','System.TypeCode','System.Globalization.NumberStyles','System.Reflection.BindingFlags','System.Reflection.MemberTypes','System.Reflection.MethodImplAttributes','System.Reflection.GenericParameterAttributes','System.Reflection.ParameterAttributes','System.Runtime.Serialization.StreamingContextStates')){
 $type=[Type]::GetType($typeName,$true);$value=[Enum]::GetValues($type).GetValue(0);$targets+=@{kind='foreign';type=$typeName;name=[Enum]::GetName($type,$value);value=[Convert]::ToInt32($value,[Globalization.CultureInfo]::InvariantCulture)}
}
$rows=@();$anchors=[int[]]@([int]::MinValue,-1,0,1,7,15,16,32,64,128,255,256,257,[int]::MaxValue);$values=[int[]]@((@($anchors)+@([Enum]::GetValues($enumType)|ForEach-Object {[Convert]::ToInt32($_,[Globalization.CultureInfo]::InvariantCulture)}))|Sort-Object -Unique)
foreach($number in $values){
 $boxed=[Enum]::ToObject($enumType,$number)
 foreach($target in $targets){
  $flag=$null
  if($target.kind -eq 'style'){$flag=[Enum]::ToObject($enumType,$target.value)}elseif($target.kind -eq 'foreign'){$flag=[Enum]::ToObject([Type]::GetType($target.type,$true),$target.value)}
  $arguments=[object[]]::new(1);$arguments[0]=$flag
  try{$result=[ordered]@{boolean=$method.Invoke($boxed,$arguments)}}catch{$result=Failure $_}
  $rows+=[ordered]@{value=$number;flag=$target;result=$result}
 }
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();enumType=$enumType.FullName;declaringType=$method.DeclaringType.FullName;flagParameterType=$method.GetParameters()[0].ParameterType.FullName;valueCount=$values.Count;flagValueCount=$flagValues.Count;cases=$rows;qualification='BOUNDED_CALLING_CONVENTIONS_HASFLAG_REFERENCE; PHYSICAL_ENUM_PARAMETER_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned CallingConventions HasFlag: $($rows.Count) cases"
