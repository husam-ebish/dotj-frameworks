param([Parameter(Mandatory)][string]$OutputPath,[string]$InputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
if(-not $InputPath){$InputPath=Join-Path ([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))) 'planning/stage-2/repos/dotj-core/evidence/integer-string-parsing-contract-v10.0.12.json'}
$inputData=Get-Content -LiteralPath $InputPath -Raw | ConvertFrom-Json
if($inputData.runtimeVersion -ne '10.0.12' -or $inputData.coreLibSha256 -ne $coreHash){throw 'Pinned String corpus required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
function Failure($record){$e=$record.Exception.GetBaseException();return ,([object[]]@('E',$e.GetType().FullName,$e.HResult,$(if($e -is [ArgumentException]){$e.ParamName}else{$null})))}
function Parse-Result([Reflection.MethodInfo]$Method,[object[]]$Arguments){try{return ,([object[]]@('V',[long]$Method.Invoke($null,$Arguments)))}catch{return ,(Failure $_)}}
function Try-Result([Reflection.MethodInfo]$Method,[object[]]$Arguments){try{$ok=$Method.Invoke($null,$Arguments);return ,([object[]]@('T',[bool]$ok,[long]$Arguments[$Arguments.Length-1]))}catch{$failure=Failure $_;return ,([object[]]@($failure[0],$failure[1],$failure[2],$failure[3],[long]$Arguments[$Arguments.Length-1]))}}
$texts=[Collections.Generic.List[object]]::new();$seen=[Collections.Generic.HashSet[object]]::new()
[void]$seen.Add($null);$texts.Add($null)
foreach($row in $inputData.types[0].cases){if($row.provider -eq 'Invariant' -and $seen.Add($row.text)){$texts.Add($row.text)}}
$extras=@('1.0','1.1','0.1','1e1','1e-1','100e-2','1e9999999999999','1e-9999999999999','0e9999999999999','(1)','(0)','1-','1+','1~','1p','~ 1','- 1','1,2,3','1,,','1_000','1:00','kr 1','1 kr','kr1,00','1.00kr','1e~1','1ep1','FF','80','10000000','11111111','FFFF','FFFFFFFF','00FF','0xFF',([string][char]0xa4+'1'),('1'+[char]0xa4),('-'+[char]0xa4+'1'),([string][char]0xa4+' - 1'),('('+[char]0xa4+'1)'),('1'+[char]0xa0+'000'),('1 000'),([string][char]0x20ac+'1,00'),([string][char]0x2212+'1'),([string][char]0x2197+'1'))
foreach($text in $extras){if($seen.Add($text)){$texts.Add($text)}}
$custom=[Globalization.NumberFormatInfo]::InvariantInfo.Clone();$custom.NegativeSign='~';$custom.PositiveSign='p';$custom.NumberDecimalSeparator=':';$custom.NumberGroupSeparator='_';$custom.CurrencySymbol='kr';$custom.CurrencyDecimalSeparator=',';$custom.CurrencyGroupSeparator='.';$custom.NumberNegativePattern=2
$unicode=[Globalization.NumberFormatInfo]::InvariantInfo.Clone();$unicode.NegativeSign=[string][char]0x2212;$unicode.PositiveSign=[string][char]0x2197;$unicode.NumberGroupSeparator=[string][char]0xa0;$unicode.CurrencySymbol=[string][char]0x20ac;$unicode.CurrencyDecimalSeparator=',';$unicode.CurrencyGroupSeparator=[string][char]0x202f
$profiles=@([Globalization.NumberFormatInfo]::InvariantInfo,$custom,$unicode)
$named=[int[]]@(0,3,4,8,16,32,64,96,128,256,7,111,167,383,511,515,1027)
$invalid=[int[]]@(-2147483648,-1,2048,65535,1536,516,519,1028,1539,520)
$focusTexts=@($null,'','0','-1','1.0','1.1','1e1','(1)','1,000',' - 1 ','FF','80','10000000','1-','1 000',([string][char]0xa4+'1'),('1'+[char]0))
$focus=[Collections.Generic.List[int]]::new();foreach($text in $focusTexts){if($seen.Add($text)){$texts.Add($text)};$focus.Add($texts.IndexOf($text))}
$types=@([sbyte],[byte],[uint16],[uint32]);$rows=[Collections.Generic.List[object]]::new()
for($typeIndex=0;$typeIndex -lt $types.Count;$typeIndex++){
 $owner=$types[$typeIndex];$parse=$owner.GetMethod('Parse',[type[]]@([string],[Globalization.NumberStyles],[IFormatProvider]));$simple=$owner.GetMethod('Parse',[type[]]@([string],[Globalization.NumberStyles]));$try=$owner.GetMethod('TryParse',[type[]]@([string],[Globalization.NumberStyles],[IFormatProvider],$owner.MakeByRefType()));$keys=[Collections.Generic.HashSet[object]]::new()
 $plans=[Collections.Generic.List[object]]::new()
 foreach($flags in $named){for($profile=0;$profile -lt $profiles.Count;$profile++){for($textIndex=0;$textIndex -lt $texts.Count;$textIndex++){$plans.Add([int[]]@($flags,$profile,$textIndex))}}}
 foreach($flags in 0..511){foreach($textIndex in $focus){$plans.Add([int[]]@($flags,0,$textIndex))}}
 foreach($flags in $invalid){foreach($textIndex in $focus){$plans.Add([int[]]@($flags,0,$textIndex))}}
 foreach($plan in $plans){$flags=$plan[0];$profile=$plan[1];$textIndex=$plan[2];if(-not $keys.Add("$flags/$profile/$textIndex")){continue};$style=[Enum]::ToObject([Globalization.NumberStyles],$flags)
  $arguments=[object[]]::new(3);$arguments[0]=$texts[$textIndex];$arguments[1]=$style;$arguments[2]=$profiles[$profile];$provided=Parse-Result $parse $arguments
  $arguments=[object[]]::new(4);$arguments[0]=$texts[$textIndex];$arguments[1]=$style;$arguments[2]=$profiles[$profile];$arguments[3]=[Convert]::ChangeType(99,$owner);$tried=Try-Result $try $arguments
  $defaultResult=$null;if($profile -eq 0){$arguments=[object[]]::new(2);$arguments[0]=$texts[$textIndex];$arguments[1]=$style;$defaultResult=Parse-Result $simple $arguments}
  $rows.Add([object[]]@($typeIndex,$textIndex,$flags,$profile,$provided,$tried,$defaultResult))
 }
}
function New-StyleSpanParser([type]$Owner,[type]$Element,[bool]$TryParse){
 $array=$Element.MakeArrayType();$outputArray=$Owner.MakeArrayType();$definition=[type]'System.ReadOnlySpan`1';$span=$definition.MakeGenericType([type[]]@($Element))
 if($TryParse){$parameters=[type[]]@($array,[int],[int],[Globalization.NumberStyles],[IFormatProvider],$outputArray);$returnType=[bool];$method=$Owner.GetMethod('TryParse',[type[]]@($span,[Globalization.NumberStyles],[IFormatProvider],$Owner.MakeByRefType()));$functionType=[type]'System.Func`7';$delegate=$functionType.MakeGenericType([type[]]@($array,[int],[int],[Globalization.NumberStyles],[IFormatProvider],$outputArray,[bool]))}else{$parameters=[type[]]@($array,[int],[int],[Globalization.NumberStyles],[IFormatProvider]);$returnType=[object];$method=$Owner.GetMethod('Parse',[type[]]@($span,[Globalization.NumberStyles],[IFormatProvider]));$functionType=[type]'System.Func`6';$delegate=$functionType.MakeGenericType([type[]]@($array,[int],[int],[Globalization.NumberStyles],[IFormatProvider],[object]))}
 $bridge=[Reflection.Emit.DynamicMethod]::new('IntegerStyleSpan',$returnType,$parameters);$il=$bridge.GetILGenerator();$il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_2);$il.Emit([Reflection.Emit.OpCodes]::Newobj,$span.GetConstructor([type[]]@($array,[int],[int])));$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4)
 if($TryParse){$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]5);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0);$il.Emit([Reflection.Emit.OpCodes]::Ldelema,$Owner)}
 $il.Emit([Reflection.Emit.OpCodes]::Call,$method);if(-not $TryParse){$il.Emit([Reflection.Emit.OpCodes]::Box,$Owner)};$il.Emit([Reflection.Emit.OpCodes]::Ret);return $bridge.CreateDelegate($delegate)
}
$spanRows=[Collections.Generic.List[object]]::new();$spanIndices=[Collections.Generic.HashSet[int]]::new();foreach($index in $focus){[void]$spanIndices.Add($index)};foreach($text in $extras){[void]$spanIndices.Add($texts.IndexOf($text))}
for($typeIndex=0;$typeIndex -lt $types.Count;$typeIndex++){$owner=$types[$typeIndex]
 for($encoding=0;$encoding -lt 2;$encoding++){
  $element=if($encoding -eq 0){[char]}else{[byte]};$parseBridge=New-StyleSpanParser $owner $element $false;$tryBridge=New-StyleSpanParser $owner $element $true
  foreach($flags in @($named)+@($invalid)){for($profile=0;$profile -lt $profiles.Count;$profile++){foreach($textIndex in $spanIndices){
   $text=[string]$texts[$textIndex];if($encoding -eq 0){$core=$text.ToCharArray()}else{$core=[Text.Encoding]::UTF8.GetBytes($text)}
   $backing=[Array]::CreateInstance($element,$core.Length+5);for($index=0;$index -lt $backing.Length;$index++){$backing.SetValue([Convert]::ChangeType(35,$element),$index)};[Array]::Copy($core,0,$backing,3,$core.Length);$style=[Enum]::ToObject([Globalization.NumberStyles],$flags)
   try{$parsed=[object[]]@('V',[long]$parseBridge.Invoke($backing,3,$core.Length,$style,$profiles[$profile]))}catch{$parsed=Failure $_}
   $written=[Array]::CreateInstance($owner,1);$written.SetValue([Convert]::ChangeType(99,$owner),0)
   try{$ok=$tryBridge.Invoke($backing,3,$core.Length,$style,$profiles[$profile],$written);$tried=[object[]]@('T',[bool]$ok,[long]$written.GetValue(0))}catch{$failure=Failure $_;$tried=[object[]]@($failure[0],$failure[1],$failure[2],$failure[3],[long]$written.GetValue(0))}
   $spanRows.Add([object[]]@($typeIndex,$textIndex,$flags,$profile,$encoding,$parsed,$tried))
  }}}
 }
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

$queryProviders=@(@{kind='Format';value=(New-QueryProvider 'Format')},@{kind='Overflow';value=(New-QueryProvider 'Overflow')},@{kind='Null';value=(New-QueryProvider 'Null')});$queries=[Collections.Generic.List[object]]::new()
for($typeIndex=0;$typeIndex -lt $types.Count;$typeIndex++){$owner=$types[$typeIndex];$parse=$owner.GetMethod('Parse',[type[]]@([string],[Globalization.NumberStyles],[IFormatProvider]));$try=$owner.GetMethod('TryParse',[type[]]@([string],[Globalization.NumberStyles],[IFormatProvider],$owner.MakeByRefType()))
 foreach($queryProvider in $queryProviders){foreach($flags in @(0,7,511,515,1027,1536,2048)){foreach($text in @($null,'','1','bad','4294967296')){
  $providerType=$queryProvider.value.GetType();$style=[Enum]::ToObject([Globalization.NumberStyles],$flags);$providerType.GetField('Calls').SetValue($null,0);$providerType.GetField('Requested').SetValue($null,$null)
  $arguments=[object[]]::new(3);$arguments[0]=$text;$arguments[1]=$style;$arguments[2]=$queryProvider.value;$parsed=Parse-Result $parse $arguments;$parseCalls=[int]$providerType.GetField('Calls').GetValue($null);$requested=$providerType.GetField('Requested').GetValue($null);$parseType=if($null -eq $requested){$null}else{$requested.FullName}
  $providerType.GetField('Calls').SetValue($null,0);$providerType.GetField('Requested').SetValue($null,$null)
  $arguments=[object[]]::new(4);$arguments[0]=$text;$arguments[1]=$style;$arguments[2]=$queryProvider.value;$arguments[3]=[Convert]::ChangeType(99,$owner);$tried=Try-Result $try $arguments;$tryCalls=[int]$providerType.GetField('Calls').GetValue($null);$requested=$providerType.GetField('Requested').GetValue($null);$tryType=if($null -eq $requested){$null}else{$requested.FullName}
  $queries.Add([object[]]@($typeIndex,$text,$flags,$queryProvider.kind,$parsed,$tried,$parseCalls,$parseType,$tryCalls,$tryType))
 }}}
}

for($typeIndex=0;$typeIndex -lt $types.Count;$typeIndex++){$owner=$types[$typeIndex]
 for($encoding=0;$encoding -lt 2;$encoding++){
  $element=if($encoding -eq 0){[char]}else{[byte]};$parseBridge=New-StyleSpanParser $owner $element $false;$tryBridge=New-StyleSpanParser $owner $element $true
  foreach($queryProvider in $queryProviders){foreach($flags in @(7,515,1027,1536)){foreach($sourceText in @($null,'1')){
   $text=[string]$sourceText;if($encoding -eq 0){$core=$text.ToCharArray()}else{$core=[Text.Encoding]::UTF8.GetBytes($text)};$backing=[Array]::CreateInstance($element,$core.Length+5);for($index=0;$index -lt $backing.Length;$index++){$backing.SetValue([Convert]::ChangeType(35,$element),$index)};[Array]::Copy($core,0,$backing,3,$core.Length);$style=[Enum]::ToObject([Globalization.NumberStyles],$flags)
   $providerType=$queryProvider.value.GetType();$providerType.GetField('Calls').SetValue($null,0);$providerType.GetField('Requested').SetValue($null,$null)
   try{$parsed=[object[]]@('V',[long]$parseBridge.Invoke($backing,3,$core.Length,$style,$queryProvider.value))}catch{$parsed=Failure $_}
   $parseCalls=[int]$providerType.GetField('Calls').GetValue($null);$requested=$providerType.GetField('Requested').GetValue($null);$parseType=if($null -eq $requested){$null}else{$requested.FullName}
   $providerType.GetField('Calls').SetValue($null,0);$providerType.GetField('Requested').SetValue($null,$null);$written=[Array]::CreateInstance($owner,1);$written.SetValue([Convert]::ChangeType(99,$owner),0)
   try{$ok=$tryBridge.Invoke($backing,3,$core.Length,$style,$queryProvider.value,$written);$tried=[object[]]@('T',[bool]$ok,[long]$written.GetValue(0))}catch{$failure=Failure $_;$tried=[object[]]@($failure[0],$failure[1],$failure[2],$failure[3],[long]$written.GetValue(0))}
   $tryCalls=[int]$providerType.GetField('Calls').GetValue($null);$requested=$providerType.GetField('Requested').GetValue($null);$tryType=if($null -eq $requested){$null}else{$requested.FullName}
   $queries.Add([object[]]@($typeIndex,$sourceText,$flags,$queryProvider.kind,$parsed,$tried,$parseCalls,$parseType,$tryCalls,$tryType,$encoding))
  }}}
 }
}

$providerRecords=@(foreach($info in $profiles){[ordered]@{negativeSign=$info.NegativeSign;positiveSign=$info.PositiveSign;numberDecimal=$info.NumberDecimalSeparator;numberGroup=$info.NumberGroupSeparator;currencySymbol=$info.CurrencySymbol;currencyDecimal=$info.CurrencyDecimalSeparator;currencyGroup=$info.CurrencyGroupSeparator;numberNegativePattern=$info.NumberNegativePattern}})
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();inputEvidence='integer-string-parsing-contract-v10.0.12.json';inputSha256=(Get-FileHash -LiteralPath $InputPath -Algorithm SHA256).Hash.ToLowerInvariant();types=@($types|ForEach-Object FullName);texts=$texts;providers=$providerRecords;namedStyles=$named;invalidStyles=$invalid;rows=$rows;spanRows=$spanRows;providerQueries=$queries;qualification='BOUNDED_INTEGER_STYLE_REFERENCE; ADDITIONAL_PROVIDER_AND_RELEASE_QUALIFICATION_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 14 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned integer String styles: $($rows.Count) rows, $($texts.Count) texts, three providers"
