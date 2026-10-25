param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum formatter requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
$provider=[Globalization.NumberFormatInfo]::InvariantInfo;$enumType=[sbyte]
function New-EnumFormatter(){
 $span=[type]'System.Span[char]';$readOnly=[type]'System.ReadOnlySpan[char]';$bridge=[Reflection.Emit.DynamicMethod]::new('EnumCharTryFormat',[bool],[type[]]@([object],[char[]],[int[]],[string],[IFormatProvider]));$il=$bridge.GetILGenerator()
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Castclass,[ISpanFormattable]);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Call,$span.GetMethod('op_Implicit',[type[]]@([char[]])))
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_2);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0);$il.Emit([Reflection.Emit.OpCodes]::Ldelema,[int]);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3);$il.Emit([Reflection.Emit.OpCodes]::Call,[MemoryExtensions].GetMethod('AsSpan',[type[]]@([string])));$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4);$il.Emit([Reflection.Emit.OpCodes]::Callvirt,[ISpanFormattable].GetMethod('TryFormat'));$il.Emit([Reflection.Emit.OpCodes]::Ret)
 return $bridge.CreateDelegate([Func[object,char[],int[],string,IFormatProvider,bool]])
}
function New-SpanText([type]$Element,[bool]$ReadOnly){
 $array=$Element.MakeArrayType();$definition=if($ReadOnly){[type]'System.ReadOnlySpan`1'}else{[type]'System.Span`1'};$span=$definition.MakeGenericType([type[]]@($Element));$bridge=[Reflection.Emit.DynamicMethod]::new('SelectedSpanText',[string],[type[]]@($array,[int],[int]));$il=$bridge.GetILGenerator();$local=$il.DeclareLocal($span)
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_2);$il.Emit([Reflection.Emit.OpCodes]::Newobj,$span.GetConstructor([type[]]@($array,[int],[int])));$il.Emit([Reflection.Emit.OpCodes]::Stloc,$local);$il.Emit([Reflection.Emit.OpCodes]::Ldloca,$local);$il.Emit([Reflection.Emit.OpCodes]::Call,$span.GetMethod('ToString',[type[]]@()));$il.Emit([Reflection.Emit.OpCodes]::Ret)
 $delegate=[type]'System.Func`4';return $bridge.CreateDelegate($delegate.MakeGenericType([type[]]@($array,[int],[int],[string])))
}
function Units([Array]$values){return ,([int[]]@(foreach($value in $values){[int]$value}))}
$formatter=New-EnumFormatter;$single=[sbyte].GetMethod('ToString',[type[]]@([string]));$rows=@()
$values=[int[]]@(-128,-127,-100,-42,-1,0,1,9,10,42,99,100,126,127)
foreach($number in $values){
 $boxed=[sbyte]$number
 foreach($format in @($null,'','G','G2','D','d','D4','X','x2','X4','B','B12','R','F2','N2','E2','Q')){
  $arguments=[object[]]::new(1);$arguments[0]=$format
  try{$text=$single.Invoke($boxed,$arguments);$length=$text.Length;$capacities=@(0,1,[Math]::Max(0,$length-2),[Math]::Max(0,$length-1),$length,($length+1))|Sort-Object -Unique;if($number -eq 255 -and $format -ceq 'G'){$capacities=0..($length+1)}}catch{$capacities=@(0,1,3,7,32,256)}
  foreach($capacity in $capacities){$buffer=[char[]]('#'*$capacity);$written=[int[]]@(99)
   try{$success=$formatter.Invoke($boxed,$buffer,$written,$format,$provider);$result=[ordered]@{boolean=$success}}catch{$result=Failure $_}
   $rows+=[ordered]@{value=$number;format=$format;capacity=$capacity;written=$written[0];buffer=[string]::new($buffer);result=$result}
  }
 }
}
$seeds=[ordered]@{Char=[int[]]@(65,98,0,55357,56898,9731,65535,42,13,10,90,255);Byte=[int[]]@(0,1,127,128,255,42,13,10,64,65,254,3)};$texts=@()
foreach($encoding in @('Char','Byte')){foreach($readOnly in @($false,$true)){
 $element=if($encoding -eq 'Char'){[char]}else{[byte]};$getter=New-SpanText $element $readOnly
 if($encoding -eq 'Char'){$source=[char[]]$seeds.Char}else{$source=[byte[]]$seeds.Byte}
 foreach($offset in @(0,1,4,8,12)){foreach($length in @(0,1,3,4,8,12)){if($offset+$length -gt 12){continue}
  $text=$getter.Invoke($source,$offset,$length);$texts+=[ordered]@{encoding=$encoding;readOnly=$readOnly;offset=$offset;length=$length;textUnits=(Units ($text.ToCharArray()))}
 }}
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();enumType=$enumType.FullName;interfaces=@($enumType.GetInterfaces()|ForEach-Object FullName);providerThrowsIfQueried=$false;providerProfile='Invariant';utf8Assignable=[IUtf8SpanFormattable].IsAssignableFrom($enumType);utf8Instance=[IUtf8SpanFormattable].IsInstanceOfType([sbyte]0);valueCount=$values.Count;seeds=$seeds;texts=$texts;buffers=$rows;qualification='BOUNDED_SBYTE_CHAR_FORMAT_AND_SPAN_TEXT_REFERENCE; BYREF_LIFETIME_OTHER_ENUM_METHODS_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned SByte Char formatting: $($rows.Count) buffers; $($texts.Count) span texts"
