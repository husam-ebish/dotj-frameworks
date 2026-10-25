param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$coreHash = (Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if ([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678') {
    throw 'DateTime oracle requires the pinned .NET 10.0.12 CoreLib.'
}
function Failure($ErrorRecord) {
    $value = $ErrorRecord.Exception.GetBaseException()
    [ordered]@{ exception = $value.GetType().FullName; paramName = $(if ($value -is [ArgumentException]) { $value.ParamName } else { $null }); hResult = $value.HResult }
}
function New-DateTimeBufferFormatter([type]$ElementType) {
    $arrayType = $ElementType.MakeArrayType()
    $spanDefinition = [type]'System.Span`1'
    $spanType = $spanDefinition.MakeGenericType($ElementType)
    $bridge = [Reflection.Emit.DynamicMethod]::new('DateTimeBufferTryFormat',[bool],
        [type[]]@([DateTime],$arrayType,[int[]],[string],[IFormatProvider]))
    $il = $bridge.GetILGenerator()
    $target = [DateTime].GetMethod('TryFormat',[type[]]@($spanType,[int].MakeByRefType(),[type]'System.ReadOnlySpan[char]',[IFormatProvider]))
    $il.Emit([Reflection.Emit.OpCodes]::Ldarga_S,[byte]0)
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_1)
    $il.Emit([Reflection.Emit.OpCodes]::Call,$spanType.GetMethod('op_Implicit',[type[]]@($arrayType)))
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_2)
    $il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0)
    $il.Emit([Reflection.Emit.OpCodes]::Ldelema,[int])
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_3)
    $il.Emit([Reflection.Emit.OpCodes]::Call,[MemoryExtensions].GetMethod('AsSpan',[type[]]@([string])))
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4)
    $il.Emit([Reflection.Emit.OpCodes]::Call,$target)
    $il.Emit([Reflection.Emit.OpCodes]::Ret)
    $delegateDefinition = [type]'System.Func`6'
    $delegateType = $delegateDefinition.MakeGenericType([type[]]@([DateTime],$arrayType,[int[]],[string],[IFormatProvider],[bool]))
    return $bridge.CreateDelegate($delegateType)
}
$charFormatter=New-DateTimeBufferFormatter ([char]);$byteFormatter=New-DateTimeBufferFormatter ([byte])
$formats=@('%y','yy','yyy','yyyy','yyyyy','yyyyyyyyyyyy','%M','MM','MMM','MMMM','MMMMM','%d','dd','ddd','dddd','ddddd','%H','HH','HHHH','%h','hh','hhhh','%m','mm','mmmm','%s','ss','ssss','%t','tt','tttt','%g','gggg','%f','ff','fffffff','%F','FF','FFFFFFF','ss.FFFFFFF','ss.FFF','%z','zz','zzz','zzzz','%K','KK','yyyy/MM/dd HH:mm:ss.fffffff K','yyyy-MM-ddTHH:mm:ss.FFFFFFFK',"'hello' yyyy",'"hello" MM',"'a\'b' dd",'\y\y','%/','%:','%x','abc','yyyy qqq',"yyyy 'a\'b'",'yyyy \','yyyy %','%%','%','ffffffff','FFFFFFFF',"yyyy 'unclosed",'yyyy "unclosed','HH:mm:ss.fffffff','HH:mm:ss.FFFFFFF','日yyyy月MM')
$samples=@(@{ticks=[long]0;kind=[DateTimeKind]::Utc},@{ticks=[long]638447204961234567;kind=[DateTimeKind]::Unspecified},@{ticks=[long]638447204960000000;kind=[DateTimeKind]::Local},@{ticks=[long]3155378975999999999;kind=[DateTimeKind]::Utc})
$rows=@();$culture=[Globalization.CultureInfo]::CurrentCulture
try{
 [Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
 foreach($sample in $samples){foreach($format in $formats){
  if(($format.Contains('z') -or $format.Contains('K')) -and $sample.ticks -lt 864000000000){continue}
  $value=[DateTime]::new($sample.ticks,$sample.kind)
  foreach($encoding in @('Char','Utf8')){
   try{$text=$value.ToString($format,[Globalization.CultureInfo]::InvariantCulture);$length=if($encoding -eq 'Char'){$text.Length}else{[Text.Encoding]::UTF8.GetByteCount($text)};$capacities=0..($length+2)}catch{$capacities=@(0,1,3,5,8,16,40)}
   foreach($capacity in $capacities){
    $written=[int[]]@(99)
    if($encoding -eq 'Char'){$buffer=[char[]]('#'*$capacity);$formatter=$charFormatter}else{$buffer=[byte[]]::new($capacity);[Array]::Fill($buffer,[byte]35);$formatter=$byteFormatter}
    try{$success=$formatter.Invoke($value,$buffer,$written,$format,[Globalization.CultureInfo]::InvariantCulture);$result=[ordered]@{boolean=$success}}catch{$result=Failure $_}
    $row=[ordered]@{ticks=$sample.ticks.ToString();kind=$sample.kind.ToString();format=$format;encoding=$encoding;capacity=$capacity;written=$written[0];result=$result}
    if($encoding -eq 'Char'){$row.buffer=[string]::new($buffer)}else{$row.bufferHex=[Convert]::ToHexString($buffer)}
    $rows+=$row
   }
  }
 }}
}finally{[Globalization.CultureInfo]::CurrentCulture=$culture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=[TimeZoneInfo]::Local.Id;javaZoneProfile='Europe/Zurich';buffers=$rows;qualification='BOUNDED_INVARIANT_CUSTOM_DATETIME_BUFFER_REFERENCE; PROVIDER_HISTORICAL_ZONES_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned custom DateTime buffers: $($rows.Count) cases"
