param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$owner=[uint];$compare=$owner.GetMethod('CompareTo',[type[]]@([object]));$typedCompare=$owner.GetMethod('CompareTo',[type[]]@([uint]));$interface=[IComparable].GetMethod('CompareTo');$equals=$owner.GetMethod('Equals',[type[]]@([object]));$typedEquals=$owner.GetMethod('Equals',[type[]]@([uint]));$hash=$owner.GetMethod('GetHashCode',[type[]]@())
$values=[long[]]@(0,1,2,7,8,9,10,15,16,31,32,42,255,256,65535,65536,2147483646,2147483647,2147483648,2147483649,4294967293,4294967294,4294967295);$hashValues=[long[]]@((0..255)+@(256,257,511,65535,65536,2147483647,2147483648,2147483649,4294967294,4294967295))
$targets=@(foreach($number in $values){@{kind='uint32';value=$number}})
$targets+=@(@{kind='null'},@{kind='int32';value=0},@{kind='int32';value=255},@{kind='sbyte';value=0},@{kind='sbyte';value=127},@{kind='sbyte';value=-1},@{kind='int16';value=0},@{kind='int16';value=255},@{kind='byte';value=0},@{kind='byte';value=255},@{kind='int64';value=0},@{kind='uint16';value=0},@{kind='boolean';value=$false},@{kind='string';value='0'},@{kind='string';value=''},@{kind='object'},@{kind='char';value=0},@{kind='double';value=0},@{kind='enum';type='System.DayOfWeek';name='Sunday';value=0},@{kind='enum';type='System.Reflection.BindingFlags';name='Default';value=0})
$hashes=@(foreach($number in $hashValues){$boxed=[uint]$number;[ordered]@{value=$number;hash=$hash.Invoke($boxed,[object[]]@())}});$rows=@()
foreach($number in $values){$boxed=[uint]$number;foreach($target in $targets){
 $other=$null
 switch($target.kind){
  'uint32'{$other=[uint]$target.value};'int32'{$other=[int]$target.value};'sbyte'{$other=[sbyte]$target.value};'int16'{$other=[short]$target.value};'byte'{$other=[byte]$target.value};'int64'{$other=[long]$target.value};'uint16'{$other=[ushort]$target.value};'boolean'{$other=[bool]$target.value};'string'{$other=[string]$target.value};'object'{$other=[object]::new()};'char'{$other=[char]$target.value};'double'{$other=[double]$target.value};'enum'{$other=[Enum]::ToObject([Type]::GetType($target.type,$true),[int]$target.value)}
 }
 $arguments=[object[]]::new(1);$arguments[0]=$other
 try{$comparison=[ordered]@{value=$compare.Invoke($boxed,$arguments)}}catch{$comparison=Failure $_}
 try{$interfaceResult=[ordered]@{value=$interface.Invoke($boxed,$arguments)}}catch{$interfaceResult=Failure $_}
 $typedComparison=$null;$typedEquality=$null
 if($target.kind -eq 'uint32'){$typedComparison=$typedCompare.Invoke($boxed,$arguments);$typedEquality=$typedEquals.Invoke($boxed,$arguments)}
 $rows+=[ordered]@{value=$number;target=$target;comparison=$comparison;interfaceComparison=$interfaceResult;equal=$equals.Invoke($boxed,$arguments);typedComparison=$typedComparison;typedEquality=$typedEquality}
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();typeName=$owner.FullName;interfaces=@($owner.GetInterfaces()|ForEach-Object FullName);valueCount=$values.Count;hashes=$hashes;cases=$rows;qualification='BOUNDED_UINT32_COMPARISON_REFERENCE; GENERIC_INTERFACE_ARITY_OTHER_NUMERIC_API_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned UInt32 comparison: $($hashes.Count) hashes; $($rows.Count) target pairs"
