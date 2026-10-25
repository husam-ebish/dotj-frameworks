param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum formatter requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$enumType=[Reflection.MemberTypes];$compare=[Enum].GetMethod('CompareTo',[type[]]@([object]));$interface=[IComparable].GetMethod('CompareTo');$equals=[Enum].GetMethod('Equals',[type[]]@([object]));$hash=[Enum].GetMethod('GetHashCode',[type[]]@())
$anchors=[int[]]@([int]::MinValue,-65536,-129,-1,0,1,2,3,7,8,15,16,32,64,127,128,255,256,65535,65536,16777217,[int]::MaxValue)
$values=[int[]]@((@($anchors)+@([Enum]::GetValues($enumType)|ForEach-Object {[Convert]::ToInt32($_,[Globalization.CultureInfo]::InvariantCulture)}))|Sort-Object -Unique)
$targets=@(foreach($number in $values){@{kind='style';value=$number}})
$targets+=@(@{kind='null'},@{kind='int32';value=0},@{kind='int32';value=3},@{kind='int64';value=0},@{kind='byte';value=0},@{kind='boolean';value=$false},@{kind='string';value='0'},@{kind='string';value=''},@{kind='object'},@{kind='enum';type='System.Globalization.TimeSpanStyles';value=3},@{kind='enum';type='System.Globalization.DateTimeStyles';value=1},@{kind='enum';type='System.DateTimeKind';value=1},@{kind='enum';type='System.DayOfWeek';value=3},@{kind='enum';type='System.TypeCode';value=9})
$rows=@();$hashes=@()
foreach($number in $values){
 $boxed=[Enum]::ToObject($enumType,$number);$hashes+=[ordered]@{value=$number;hash=$hash.Invoke($boxed,[object[]]@())}
 foreach($target in $targets){
  $other=$null
  switch($target.kind){
   'style'{$other=[Enum]::ToObject($enumType,[int]$target.value)}
   'int32'{$other=[int]$target.value}
   'int64'{$other=[long]$target.value}
   'byte'{$other=[byte]$target.value}
   'boolean'{$other=[bool]$target.value}
   'string'{$other=[string]$target.value}
   'object'{$other=[object]::new()}
   'enum'{$other=[Enum]::ToObject([Type]::GetType($target.type,$true),[int]$target.value)}
  }
  $arguments=[object[]]::new(1);$arguments[0]=$other
  try{$comparison=[ordered]@{value=$compare.Invoke($boxed,$arguments)}}catch{$comparison=Failure $_}
  try{$interfaceResult=[ordered]@{value=$interface.Invoke($boxed,$arguments)}}catch{$interfaceResult=Failure $_}
  $equal=$equals.Invoke($boxed,$arguments)
  $rows+=[ordered]@{value=$number;target=$target;comparison=$comparison;interfaceComparison=$interfaceResult;equal=$equal}
 }
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();enumType=$enumType.FullName;interfaces=@($enumType.GetInterfaces()|ForEach-Object FullName);valueCount=$values.Count;hashes=$hashes;cases=$rows;qualification='BOUNDED_MEMBER_TYPES_ENUM_COMPARISON_REFERENCE; OTHER_ENUM_CONTRACTS_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned MemberTypes comparison: $($hashes.Count) hashes; $($rows.Count) comparisons"
