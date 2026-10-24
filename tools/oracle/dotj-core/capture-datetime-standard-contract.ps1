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
$charFormatter = New-DateTimeBufferFormatter ([char])
$byteFormatter = New-DateTimeBufferFormatter ([byte])
$culture=[Globalization.CultureInfo]::CurrentCulture
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
try{
$provider=[Globalization.CultureInfo]::InvariantCulture;$formats=@('d','D','f','F','g','G','m','M','t','T','y','Y')
$ticksList=[long[]]@(0,1,863999999999,864000000000,31241376000000000,621355968000000000,638447204961234567,638636327981234567,3155378975999999999)
$strings=@();$buffers=@()
foreach($ticks in $ticksList){foreach($kind in [Enum]::GetValues([DateTimeKind])){foreach($format in $formats){
 $value=[DateTime]::new($ticks,$kind);$text=$value.ToString($format,$provider)
 $strings+=[ordered]@{ticks=$ticks.ToString();kind=$kind.ToString();format=$format;text=$text;singleText=$value.ToString($format);interfaceText=([IFormattable].GetMethod('ToString').Invoke($value,[object[]]@($format,$provider)))}
}}}
foreach($ticks in [long[]]@(0,638447204961234567,3155378975999999999)){foreach($format in $formats){
 $value=[DateTime]::new($ticks,[DateTimeKind]::Unspecified);$text=$value.ToString($format,$provider)
 foreach($capacity in 0..($text.Length+1)){foreach($encoding in @('Char','Utf8')){
  $written=[int[]]@(99)
  if($encoding -eq 'Char'){$buffer=[char[]]('#'*$capacity);$formatter=$charFormatter}else{$buffer=[byte[]]::new($capacity);[Array]::Fill($buffer,[byte]35);$formatter=$byteFormatter}
  $success=$formatter.Invoke($value,$buffer,$written,$format,$provider)
  $row=[ordered]@{ticks=$ticks.ToString();format=$format;capacity=$capacity;encoding=$encoding;success=$success;written=$written[0]}
  if($encoding -eq 'Char'){$row.buffer=[string]::new($buffer)}else{$row.bufferHex=[Convert]::ToHexString($buffer)}
  $buffers+=$row
 }}
}}
}finally{[Globalization.CultureInfo]::CurrentCulture=$culture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();strings=$strings;buffers=$buffers;qualification='BOUNDED_INVARIANT_DATE_AND_TIME_STANDARD_FORMAT_REFERENCE; OFFSET_ROUNDTRIP_CULTURES_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned invariant standard date/time formats: $($strings.Count) strings and $($buffers.Count) buffers"
