param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
function New-Utf8Formatter(){
 $span=[type]'System.Span[byte]';$bridge=[Reflection.Emit.DynamicMethod]::new('ByteUtf8TryFormat',[bool],[type[]]@([object],[byte[]],[int[]],[string],[IFormatProvider]));$il=$bridge.GetILGenerator()
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Castclass,[IUtf8SpanFormattable]);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Call,$span.GetMethod('op_Implicit',[type[]]@([byte[]])))
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_2);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0);$il.Emit([Reflection.Emit.OpCodes]::Ldelema,[int]);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3);$il.Emit([Reflection.Emit.OpCodes]::Call,[MemoryExtensions].GetMethod('AsSpan',[type[]]@([string])));$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4);$il.Emit([Reflection.Emit.OpCodes]::Callvirt,[IUtf8SpanFormattable].GetMethod('TryFormat'));$il.Emit([Reflection.Emit.OpCodes]::Ret)
 return $bridge.CreateDelegate([Func[object,byte[],int[],string,IFormatProvider,bool]])
}
$custom=[Globalization.NumberFormatInfo]::InvariantInfo.Clone();$custom.NegativeSign=[string][char]0x2212;$custom.PositiveSign=[string][char]0x2197;$custom.NumberDecimalSeparator=[string][char]0x00b7;$custom.NumberGroupSeparator='_'
$profiles=@(@{name='Invariant';value=[Globalization.NumberFormatInfo]::InvariantInfo},@{name='Unicode';value=$custom})
$values=[int[]]@(0,1,2,7,9,10,42,99,100,127,128,200,254,255);$formats=@($null,'','G','G2','D','d','D4','X','x2','X4','B','B12','R','F2','N2','E2','Q');$format=New-Utf8Formatter;$single=[byte].GetMethod('ToString',[type[]]@([string],[IFormatProvider]));$rows=@()
foreach($numericProfile in $profiles){foreach($number in $values){foreach($specifier in $formats){
 $boxed=[byte]$number;$arguments=[object[]]::new(2);$arguments[0]=$specifier;$arguments[1]=$numericProfile.value
 try{$text=$single.Invoke($boxed,$arguments);$length=[Text.Encoding]::UTF8.GetByteCount($text);$capacities=@(0,1,[Math]::Max(0,$length-2),[Math]::Max(0,$length-1),$length,($length+1))|Sort-Object -Unique}catch{$capacities=@(0,1,3,7,32,256)}
 foreach($capacity in $capacities){$buffer=[byte[]]::new($capacity);[Array]::Fill($buffer,[byte]35);$written=[int[]]@(99)
  try{$success=$format.Invoke($boxed,$buffer,$written,$specifier,$numericProfile.value);$result=[ordered]@{boolean=$success}}catch{$result=Failure $_}
  $rows+=[ordered]@{value=$number;provider=$numericProfile.name;format=$specifier;capacity=$capacity;written=$written[0];bufferUnits=[int[]]$buffer;result=$result}
 }
}}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();typeName='System.Byte';interfaces=@([byte].GetInterfaces()|ForEach-Object FullName);valueCount=$values.Count;providerCount=$profiles.Count;buffers=$rows;qualification='BOUNDED_BYTE_UTF8_REFERENCE; OTHER_FORMATS_CULTURES_BYREF_LIFETIMES_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned Byte UTF-8: $($rows.Count) buffer cases"
