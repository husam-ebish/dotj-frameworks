param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum formatter requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$assembly=[Reflection.Emit.AssemblyBuilder]::DefineDynamicAssembly([Reflection.AssemblyName]::new('IgnoredEnumProvider'),[Reflection.Emit.AssemblyBuilderAccess]::Run)
$builder=$assembly.DefineDynamicModule('Main').DefineType('IgnoredProvider',[Reflection.TypeAttributes]'Public,Sealed');$builder.AddInterfaceImplementation([IFormatProvider]);$builder.DefineDefaultConstructor([Reflection.MethodAttributes]::Public)|Out-Null
$method=$builder.DefineMethod('GetFormat',[Reflection.MethodAttributes]'Public,Virtual,Final,HideBySig,NewSlot',[object],[type[]]@([type]));$il=$method.GetILGenerator();$il.Emit([Reflection.Emit.OpCodes]::Ldstr,'Provider must be ignored');$il.Emit([Reflection.Emit.OpCodes]::Newobj,[InvalidOperationException].GetConstructor([type[]]@([string])));$il.Emit([Reflection.Emit.OpCodes]::Throw);$builder.DefineMethodOverride($method,[IFormatProvider].GetMethod('GetFormat'))
$provider=[Activator]::CreateInstance($builder.CreateType());$enumType=[Globalization.TimeSpanStyles]
$plain=[Enum].GetMethod('ToString',[type[]]@());$defaultProvider=[Enum].GetMethod('ToString',[type[]]@([IFormatProvider]));$single=[Enum].GetMethod('ToString',[type[]]@([string]));$withProvider=[Enum].GetMethod('ToString',[type[]]@([string],[IFormatProvider]));$interface=[IFormattable].GetMethod('ToString')
$values=@([int]::MinValue,-1)+(0..255)+@(256,257,511,65535,[int]::MaxValue)
$formats=@($null,'','G','g','F','f','D','d','X','x','?','GG',' G','G ',[string][char]0)
$defaults=@();$rows=@()
foreach($number in $values){
 $boxed=[Enum]::ToObject($enumType,[int]$number);$defaults+=[ordered]@{value=$number;text=$plain.Invoke($boxed,[object[]]@());providerText=$defaultProvider.Invoke($boxed,[object[]]@($provider))}
 foreach($format in $formats){
  $arguments=[object[]]::new(2);$arguments[0]=$format;$arguments[1]=$provider;$singleArguments=[object[]]::new(1);$singleArguments[0]=$format
  try{$singleResult=[ordered]@{text=$single.Invoke($boxed,$singleArguments)}}catch{$singleResult=Failure $_}
  try{$providerResult=[ordered]@{text=$withProvider.Invoke($boxed,$arguments)}}catch{$providerResult=Failure $_}
  try{$interfaceResult=[ordered]@{text=$interface.Invoke($boxed,$arguments)}}catch{$interfaceResult=Failure $_}
  $rows+=[ordered]@{value=$number;format=$format;single=$singleResult;provider=$providerResult;interface=$interfaceResult}
 }
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();enumType=$enumType.FullName;underlyingType=[Enum]::GetUnderlyingType($enumType).FullName;flags=$enumType.IsDefined([FlagsAttribute],$false);interfaces=@($enumType.GetInterfaces()|ForEach-Object FullName);formatDeclaringType=$single.DeclaringType.FullName;providerThrowsIfQueried=$true;defaults=$defaults;cases=$rows;qualification='BOUNDED_INT32_TIMESPAN_STYLE_ENUM_FORMAT_REFERENCE; OTHER_ENUM_INTERFACES_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned TimeSpanStyles formatting: $($defaults.Count) defaults; $($rows.Count) formatted cases"
