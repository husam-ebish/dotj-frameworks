param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum formatter requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$assembly=[Reflection.Emit.AssemblyBuilder]::DefineDynamicAssembly([Reflection.AssemblyName]::new('IgnoredEnumProvider'),[Reflection.Emit.AssemblyBuilderAccess]::Run)
$builder=$assembly.DefineDynamicModule('Main').DefineType('IgnoredProvider',[Reflection.TypeAttributes]'Public,Sealed');$builder.AddInterfaceImplementation([IFormatProvider]);$builder.DefineDefaultConstructor([Reflection.MethodAttributes]::Public)|Out-Null
$method=$builder.DefineMethod('GetFormat',[Reflection.MethodAttributes]'Public,Virtual,Final,HideBySig,NewSlot',[object],[type[]]@([type]));$il=$method.GetILGenerator();$il.Emit([Reflection.Emit.OpCodes]::Ldstr,'Provider must be ignored');$il.Emit([Reflection.Emit.OpCodes]::Newobj,[InvalidOperationException].GetConstructor([type[]]@([string])));$il.Emit([Reflection.Emit.OpCodes]::Throw);$builder.DefineMethodOverride($method,[IFormatProvider].GetMethod('GetFormat'))
$provider=[Activator]::CreateInstance($builder.CreateType());$enumType=[Reflection.MethodImplAttributes]
$plain=[Enum].GetMethod('ToString',[type[]]@());$defaultProvider=[Enum].GetMethod('ToString',[type[]]@([IFormatProvider]));$single=[Enum].GetMethod('ToString',[type[]]@([string]));$withProvider=[Enum].GetMethod('ToString',[type[]]@([string],[IFormatProvider]));$interface=[IFormattable].GetMethod('ToString')
function Converted($output){
 $result=[ordered]@{type=$output.GetType().FullName}
 if($output -is [bool]){$result.boolean=$output}
 elseif($output -is [char]){$result.character=[int]$output}
 elseif($output -is [single]){$result.singleBits=[BitConverter]::SingleToInt32Bits($output).ToString()}
 elseif($output -is [double]){$result.doubleBits=[BitConverter]::DoubleToInt64Bits($output).ToString()}
 elseif($output -is [Enum]){$result.enumValue=[Convert]::ToInt32($output,[Globalization.CultureInfo]::InvariantCulture);$result.text=$output.ToString()}
 else{$result.text=[Convert]::ToString($output,[Globalization.CultureInfo]::InvariantCulture)}
 if($output -is [decimal]){$result.decimalBits=[decimal]::GetBits($output)}
 return $result
}
$anchors=[int[]]@([int]::MinValue,-16777217,-65536,-32769,-32768,-129,-128,-1,0,1,3,7,15,16,32,64,127,128,255,256,32767,32768,65535,65536,16777215,16777216,16777217,[int]::MaxValue)
$values=[int[]]@((@($anchors)+@([Enum]::GetValues($enumType)|ForEach-Object {[Convert]::ToInt32($_,[Globalization.CultureInfo]::InvariantCulture)}))|Sort-Object -Unique)
$targets=@('System.Boolean','System.Char','System.SByte','System.Byte','System.Int16','System.UInt16','System.Int32','System.UInt32','System.Int64','System.UInt64','System.Single','System.Double','System.Decimal','System.String','System.Object','System.DateTime','System.DBNull','System.Enum','System.ValueType','System.IConvertible','System.TimeSpan','System.Int32[]','System.Reflection.MethodImplAttributes','System.Globalization.TimeSpanStyles',$null)
$methods=@('GetTypeCode','ToBoolean','ToChar','ToSByte','ToByte','ToInt16','ToUInt16','ToInt32','ToUInt32','ToInt64','ToUInt64','ToSingle','ToDouble','ToDecimal','ToDateTime','ToString');$direct=@();$queries=@();$toType=[IConvertible].GetMethod('ToType')
foreach($number in $values){
 $boxed=[Enum]::ToObject($enumType,$number)
 foreach($name in $methods){
  $method=[IConvertible].GetMethod($name);$arguments=if($name -eq 'GetTypeCode'){[object[]]@()}else{[object[]]@($provider)}
  try{$output=$method.Invoke($boxed,[object[]]$arguments);$result=Converted $output}catch{$result=Failure $_}
  $direct+=[ordered]@{value=$number;method=$name;result=$result}
 }
 foreach($name in $targets){
  $type=if($null -eq $name){$null}else{[Type]::GetType($name,$true)}
  try{$output=$toType.Invoke($boxed,[object[]]@($type,$provider));$result=Converted $output;$result.sameBox=[object]::ReferenceEquals($boxed,$output)}catch{$result=Failure $_}
  $queries+=[ordered]@{value=$number;target=$name;result=$result}
 }
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();enumType=$enumType.FullName;providerThrowsIfQueried=$true;interfaces=@($enumType.GetInterfaces()|ForEach-Object FullName);valueCount=$values.Count;direct=$direct;queries=$queries;qualification='BOUNDED_METHOD_IMPL_ATTRIBUTES_CONVERTIBLE_REFERENCE; OTHER_ENUM_CONTRACTS_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned MethodImplAttributes conversions: $($direct.Count) direct; $($queries.Count) target cases"
