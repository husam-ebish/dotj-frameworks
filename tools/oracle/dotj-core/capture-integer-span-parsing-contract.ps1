param([Parameter(Mandatory)][string]$OutputPath,[string]$InputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
if(-not $InputPath){$InputPath=Join-Path ([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))) 'planning/stage-2/repos/dotj-core/evidence/integer-string-parsing-contract-v10.0.12.json'}
$inputs=Get-Content -LiteralPath $InputPath -Raw | ConvertFrom-Json
if($inputs.runtimeVersion -ne '10.0.12' -or $inputs.coreLibSha256 -ne $coreHash -or $inputs.textCount -ne 398){throw 'Pinned String input corpus required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
function New-SpanParser([type]$Owner,[type]$Element,[string]$Operation,[bool]$WithProvider){
 $array=$Element.MakeArrayType();$outputArray=$Owner.MakeArrayType();$definition=[type]'System.ReadOnlySpan`1';$span=$definition.MakeGenericType([type[]]@($Element))
 if($Operation -eq 'Parse'){
  $parameters=[type[]]@($array,[int],[int],[IFormatProvider]);$resultType=[object];$method=$Owner.GetMethod('Parse',[type[]]@($span,[IFormatProvider]));$functionType=[type]'System.Func`5';$delegate=$functionType.MakeGenericType([type[]]@($array,[int],[int],[IFormatProvider],[object]))
 }else{
  $parameters=[type[]]@($array,[int],[int],[IFormatProvider],$outputArray);$resultType=[bool]
  [type[]]$signature=if($WithProvider){[type[]]@($span,[IFormatProvider],$Owner.MakeByRefType())}else{[type[]]@($span,$Owner.MakeByRefType())};$method=$Owner.GetMethod('TryParse',$signature);$functionType=[type]'System.Func`6';$delegate=$functionType.MakeGenericType([type[]]@($array,[int],[int],[IFormatProvider],$outputArray,[bool]))
 }
 if($null -eq $method){throw 'Missing native span method'}
 $bridge=[Reflection.Emit.DynamicMethod]::new('SelectedIntegerSpan'+$Operation,$resultType,$parameters);$il=$bridge.GetILGenerator()
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_2);$il.Emit([Reflection.Emit.OpCodes]::Newobj,$span.GetConstructor([type[]]@($array,[int],[int])))
 if($Operation -eq 'Parse'){
  $il.Emit([Reflection.Emit.OpCodes]::Ldarg_3);$il.Emit([Reflection.Emit.OpCodes]::Call,$method);$il.Emit([Reflection.Emit.OpCodes]::Box,$Owner)
 }else{
  if($WithProvider){$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3)}
  $il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0);$il.Emit([Reflection.Emit.OpCodes]::Ldelema,$Owner);$il.Emit([Reflection.Emit.OpCodes]::Call,$method)
 }
 $il.Emit([Reflection.Emit.OpCodes]::Ret);return $bridge.CreateDelegate($delegate)
}
function New-Backing([type]$Element,[int[]]$Units){
 $array=[Array]::CreateInstance($Element,$Units.Length+5)
 for($index=0;$index -lt $array.Length;$index++){$array.SetValue([Convert]::ChangeType(35,$Element),$index)}
 for($index=0;$index -lt $Units.Length;$index++){$array.SetValue([Convert]::ChangeType($Units[$index],$Element),$index+3)}
 return ,$array
}
$sources=@()
foreach($row in $inputs.types[0].cases){if($row.provider -ne 'Invariant'){continue};$text=[string]$row.text
 $sources+=[ordered]@{encoding='Char';units=[int[]]@($text.ToCharArray()|ForEach-Object {[int]$_})}
 $sources+=[ordered]@{encoding='Byte';units=[int[]][Text.Encoding]::UTF8.GetBytes($text)}
}
$malformed=@(@(255),@(128),@(192,175),@(49,255),@(239,187,191,49),@(49,0,0),@(49,0,32),@(32,49,0),@(239,191,189),@(237,160,128),@(240,159,153,130),@(49,194))
foreach($units in $malformed){$sources+=[ordered]@{encoding='Byte';units=[int[]]$units}}
$custom=[Globalization.NumberFormatInfo]::InvariantInfo.Clone();$custom.NegativeSign='~';$custom.PositiveSign='p';$profiles=@(@{name='Invariant';value=[Globalization.NumberFormatInfo]::InvariantInfo},@{name='Custom';value=$custom});
$unicode=[Globalization.NumberFormatInfo]::InvariantInfo.Clone();$unicode.NegativeSign=[string][char]0x2212;$unicode.PositiveSign=[string][char]0x2197;$profiles+=@{name='Unicode';value=$unicode}
foreach($text in @(([string][char]0x2212+'0'),([string][char]0x2212+'128'),([string][char]0x2212+'129'),([string][char]0x2212+'65535'),([string][char]0x2212+'4294967296'),([string][char]0x2197+'1'),([string][char]0x2197+'65535'),([string][char]0x2197+'4294967295'))){
 $sources+=[ordered]@{encoding='Char';units=[int[]]@($text.ToCharArray()|ForEach-Object {[int]$_})};$sources+=[ordered]@{encoding='Byte';units=[int[]][Text.Encoding]::UTF8.GetBytes($text)}
}
$variants=@()
foreach($codePoint in @(0x2012,0x207b,0x208b,0x2212,0x2796,0xfe63,0xff0d,0x2010,0x2013,0x2014,0x006d)){
 $symbols=[Globalization.NumberFormatInfo]::InvariantInfo.Clone();$symbols.NegativeSign=[string][char]$codePoint;$profile=[ordered]@{name=('Sign'+$codePoint.ToString('X4'));value=$symbols};$variants+=$profile
 foreach($text in @('-1',($symbols.NegativeSign+'1'))){$sources+=[ordered]@{encoding='Char';units=[int[]]@($text.ToCharArray()|ForEach-Object {[int]$_});profile=$profile.name};$sources+=[ordered]@{encoding='Byte';units=[int[]][Text.Encoding]::UTF8.GetBytes($text);profile=$profile.name}}
}
$allProfiles=@($profiles)+@($variants);$providerIndex=@{};foreach($entry in $allProfiles){$providerIndex[$entry.name]=$entry}

$types=@()
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
foreach($owner in @([sbyte],[byte],[uint16],[uint32])){
 $bridges=@{};foreach($encoding in @('Char','Byte')){$element=if($encoding -eq 'Char'){[char]}else{[byte]};$bridges[$encoding]=@{parse=(New-SpanParser $owner $element 'Parse' $true);tryParse=(New-SpanParser $owner $element 'TryParse' $true);tryDefault=(New-SpanParser $owner $element 'TryParse' $false)}}
 $rows=@()
 foreach($source in $sources){$element=if($source.encoding -eq 'Char'){[char]}else{[byte]};$backing=New-Backing $element $source.units;$bridge=$bridges[$source.encoding]
  $activeProfiles=@($profiles);if($source.Contains('profile')){$activeProfiles=@($providerIndex[$source.profile])}
  foreach($numericProfile in $activeProfiles){
   try{$parse=[ordered]@{value=[long]$bridge.parse.Invoke($backing,3,$source.units.Length,$numericProfile.value)}}catch{$parse=Failure $_}
   $written=[Array]::CreateInstance($owner,1);$written.SetValue([Convert]::ChangeType(99,$owner),0)
   try{$ok=$bridge.tryParse.Invoke($backing,3,$source.units.Length,$numericProfile.value,$written);$try=[ordered]@{boolean=[bool]$ok;value=[long]$written.GetValue(0)}}catch{$try=Failure $_;$try.value=[long]$written.GetValue(0)}
   $row=[ordered]@{encoding=$source.encoding;units=$source.units;provider=$numericProfile.name;parse=$parse;tryParse=$try}
   if($numericProfile.name -eq 'Invariant'){
    $written=[Array]::CreateInstance($owner,1);$written.SetValue([Convert]::ChangeType(99,$owner),0)
    try{$ok=$bridge.tryDefault.Invoke($backing,3,$source.units.Length,$null,$written);$row.tryDefault=[ordered]@{boolean=[bool]$ok;value=[long]$written.GetValue(0)}}catch{$result=Failure $_;$result.value=[long]$written.GetValue(0);$row.tryDefault=$result}
   }
   $rows+=$row
  }
 }
 foreach($encoding in @('Char','Byte')){foreach($queryProvider in $queryProviders){foreach($sourceText in @($null,'1','bad')){foreach($operation in @('Parse','TryParse')){
  $text=[string]$sourceText
  if($encoding -eq 'Char'){$element=[char];$units=[int[]]@($text.ToCharArray()|ForEach-Object {[int]$_})}else{$element=[byte];$units=[int[]][Text.Encoding]::UTF8.GetBytes($text)}
  $backing=New-Backing $element $units;$bridge=$bridges[$encoding];$providerType=$queryProvider.value.GetType();$providerType.GetField('Calls').SetValue($null,0);$providerType.GetField('Requested').SetValue($null,$null)
  if($operation -eq 'Parse'){
   try{$result=[ordered]@{value=[long]$bridge.parse.Invoke($backing,3,$units.Length,$queryProvider.value)}}catch{$result=Failure $_}
  }else{
   $written=[Array]::CreateInstance($owner,1);$written.SetValue([Convert]::ChangeType(99,$owner),0)
   try{$ok=$bridge.tryParse.Invoke($backing,3,$units.Length,$queryProvider.value,$written);$result=[ordered]@{boolean=[bool]$ok;value=[long]$written.GetValue(0)}}catch{$result=Failure $_;$result.value=[long]$written.GetValue(0)}
  }
  $requested=$providerType.GetField('Requested').GetValue($null)
  $queries+=[ordered]@{fullName=$owner.FullName;encoding=$encoding;units=$units;kind=$queryProvider.kind;operation=$operation;calls=[int]$providerType.GetField('Calls').GetValue($null);requestedType=$(if($null -eq $requested){$null}else{$requested.FullName});result=$result}
 }}}}
 $types+=[ordered]@{fullName=$owner.FullName;cases=$rows}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();inputEvidence='integer-string-parsing-contract-v10.0.12.json';inputSha256=(Get-FileHash -LiteralPath $InputPath -Algorithm SHA256).Hash.ToLowerInvariant();sourceCount=$sources.Count;providers=@(foreach($entry in $allProfiles){[ordered]@{name=$entry.name;negativeSign=$entry.value.NegativeSign;positiveSign=$entry.value.PositiveSign}});types=$types;providerQueries=$queries;qualification='BOUNDED_INTEGER_CHAR_UTF8_SPAN_PARSE; OTHER_STYLES_PROVIDERS_BYREF_LIFETIMES_AND_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 14)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned integer span parsing: $($sources.Count) sources across four carriers"
