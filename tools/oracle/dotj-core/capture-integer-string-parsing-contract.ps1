param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
function Parse-Result([Reflection.MethodInfo]$Method,[object[]]$Arguments){try{[ordered]@{value=[long]$Method.Invoke($null,$Arguments)}}catch{Failure $_}}
function Try-Result([Reflection.MethodInfo]$Method,[object[]]$Arguments){try{$ok=$Method.Invoke($null,$Arguments);[ordered]@{boolean=[bool]$ok;value=[long]$Arguments[$Arguments.Length-1]}}catch{$result=Failure $_;$result.value=[long]$Arguments[$Arguments.Length-1];$result}}
$texts=[Collections.Generic.List[string]]::new();$set=[Collections.Generic.HashSet[string]]::new()
foreach($text in @($null,'',' ','+','-','p','~','0','-0','+0','p0','~0','0001','-0001','1.0','1e0','1,000','0x10','FF','NaN','Infinity','++1','--1','+-1','1-','1+','p-1','~+1',('1'+[char]0),('1'+[char]0+' '),('1 '+[char]0),([string][char]0),('1'+[char]0+'2'),([string][char]0+'1'),([string][char]0xa0+'1'),('1'+[char]0xa0),([string][char]0x2000+'1'),('1'+[char]0x2000),([string][char]0x0661),([string][char]0xff11),([string][char]0x2212+'1'),('9'*100),('0'*100))){if($set.Add($text)){$texts.Add($text)}}
$anchors=[long[]]@(-4294967296,-2147483649,-2147483648,-65536,-32769,-256,-129,-128,-127,-100,-42,-10,-1,0,1,9,10,42,99,100,126,127,128,129,254,255,256,257,32767,32768,65534,65535,65536,65537,2147483647,2147483648,4294967294,4294967295,4294967296)
foreach($value in $anchors){$text=$value.ToString([Globalization.CultureInfo]::InvariantCulture);foreach($form in @($text,(' '+$text+' '),([string][char]9+$text+[char]13),($text+[char]0),($text+' '+[char]0),($text+[char]0+' '),('0'+$text),$text.Replace('-','~'),('p'+$text),('+'+$text))){if($set.Add($form)){$texts.Add($form)}}}
$custom=[Globalization.NumberFormatInfo]::InvariantInfo.Clone();$custom.NegativeSign='~';$custom.PositiveSign='p';$profiles=@(@{name='Invariant';value=[Globalization.NumberFormatInfo]::InvariantInfo},@{name='Custom';value=$custom});$types=@()
foreach($numericType in @([sbyte],[byte],[uint16],[uint32])){
 $parse=$numericType.GetMethod('Parse',[type[]]@([string],[IFormatProvider]));$try=$numericType.GetMethod('TryParse',[type[]]@([string],[IFormatProvider],$numericType.MakeByRefType()));$simple=$numericType.GetMethod('Parse',[type[]]@([string]));$trySimple=$numericType.GetMethod('TryParse',[type[]]@([string],$numericType.MakeByRefType()));$rows=@()
 foreach($numericProfile in $profiles){foreach($text in $texts){
  $arguments=[object[]]::new(2);$arguments[0]=$text;$arguments[1]=$numericProfile.value;$parseResult=Parse-Result $parse $arguments
  $arguments=[object[]]::new(3);$arguments[0]=$text;$arguments[1]=$numericProfile.value;$arguments[2]=[Convert]::ChangeType(99,$numericType);$tryResult=Try-Result $try $arguments
  $row=[ordered]@{text=$text;provider=$numericProfile.name;parse=$parseResult;tryParse=$tryResult}
  if($numericProfile.name -eq 'Invariant'){
   $arguments=[object[]]::new(1);$arguments[0]=$text;$row.parseDefault=Parse-Result $simple $arguments
   $arguments=[object[]]::new(2);$arguments[0]=$text;$arguments[1]=[Convert]::ChangeType(99,$numericType);$row.tryDefault=Try-Result $trySimple $arguments
  }
  $rows+=$row
 }}
 $types+=[ordered]@{fullName=$numericType.FullName;cases=$rows}
}
function New-QueryProvider([string]$Kind){
 $assembly=[Reflection.Emit.AssemblyBuilder]::DefineDynamicAssembly([Reflection.AssemblyName]::new('IntegerStringProvider'+$Kind),[Reflection.Emit.AssemblyBuilderAccess]::Run)
 $module=$assembly.DefineDynamicModule('main');$builder=$module.DefineType('IntegerStringProvider'+$Kind,[Reflection.TypeAttributes]'Public,Class',[object],[type[]]@([IFormatProvider]))
 $calls=$builder.DefineField('Calls',[int],[Reflection.FieldAttributes]'Public,Static');$requested=$builder.DefineField('Requested',[type],[Reflection.FieldAttributes]'Public,Static');[void]$builder.DefineDefaultConstructor([Reflection.MethodAttributes]::Public)
 $method=$builder.DefineMethod('GetFormat',[Reflection.MethodAttributes]'Public,Virtual,HideBySig',[object],[type[]]@([type]));$il=$method.GetILGenerator()
 $il.Emit([Reflection.Emit.OpCodes]::Ldsfld,$calls);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_1);$il.Emit([Reflection.Emit.OpCodes]::Add);$il.Emit([Reflection.Emit.OpCodes]::Stsfld,$calls);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Stsfld,$requested)
 if($Kind -eq 'Null'){$il.Emit([Reflection.Emit.OpCodes]::Ldnull);$il.Emit([Reflection.Emit.OpCodes]::Ret)}else{
  $exception=if($Kind -eq 'Format'){[FormatException]}else{[OverflowException]};$il.Emit([Reflection.Emit.OpCodes]::Ldstr,'provider failure');$il.Emit([Reflection.Emit.OpCodes]::Newobj,$exception.GetConstructor([type[]]@([string])));$il.Emit([Reflection.Emit.OpCodes]::Throw)
 }
 $builder.DefineMethodOverride($method,[IFormatProvider].GetMethod('GetFormat'));$type=$builder.CreateType();return [Activator]::CreateInstance($type)
}
$queryProviders=@(@{kind='Format';value=(New-QueryProvider 'Format')},@{kind='Overflow';value=(New-QueryProvider 'Overflow')},@{kind='Null';value=(New-QueryProvider 'Null')});$queries=@()
foreach($numericType in @([sbyte],[byte],[uint16],[uint32])){foreach($queryProvider in $queryProviders){foreach($text in @($null,'','1','bad','4294967296')){foreach($operation in @('Parse','TryParse')){
 $type=$queryProvider.value.GetType();$type.GetField('Calls').SetValue($null,0);$type.GetField('Requested').SetValue($null,$null)
 if($operation -eq 'Parse'){$method=$numericType.GetMethod('Parse',[type[]]@([string],[IFormatProvider]));$arguments=[object[]]::new(2);$arguments[0]=$text;$arguments[1]=$queryProvider.value;$result=Parse-Result $method $arguments}else{$method=$numericType.GetMethod('TryParse',[type[]]@([string],[IFormatProvider],$numericType.MakeByRefType()));$arguments=[object[]]::new(3);$arguments[0]=$text;$arguments[1]=$queryProvider.value;$arguments[2]=[Convert]::ChangeType(99,$numericType);$result=Try-Result $method $arguments}
 $requested=$type.GetField('Requested').GetValue($null)
 $queries+=[ordered]@{fullName=$numericType.FullName;kind=$queryProvider.kind;text=$text;operation=$operation;calls=[int]$type.GetField('Calls').GetValue($null);requestedType=$(if($null -eq $requested){$null}else{$requested.FullName});result=$result}
}}}}

$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();textCount=$texts.Count;types=$types;providerQueries=$queries;qualification='BOUNDED_INTEGER_STRING_PARSE; OTHER_STYLES_SPANS_PROVIDERS_GENERIC_INTERFACES_AND_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 14)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned integer String parsing: $($texts.Count) texts, four carriers, two providers"
