param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$coreHash = (Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if ([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678') {
    throw 'DateTime oracle requires the pinned .NET 10.0.12 CoreLib.'
}
function Failure($ErrorRecord) {
    $value = $ErrorRecord.Exception.GetBaseException()
    [ordered]@{ exception = $value.GetType().FullName; paramName = $(if ($value -is [ArgumentException]) { $value.ParamName } else { $null }); hResult = $value.HResult; actualValue = $(if($value -is [ArgumentOutOfRangeException]){$value.ActualValue}else{$null}) }
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
function Units([string]$text){return ,([int[]]@(foreach($c in $text.ToCharArray()){[int]$c}))}
$pair=[char]::ConvertFromUtf32(0x1F642);$high=[string][char]0xD83D;$low=[string][char]0xDE42
$formats=@(("'"+$pair+"'"),($pair+' yyyy'),("'αβ' yyyy"),('日yyyy月MM'),($high+' yyyy'),($low+' yyyy'),("'"+$high+"' yyyy"),("'"+$low+"' yyyy"),('\'+$pair+' yyyy'),("'a"+$pair+"b' yyyy"),($pair+$pair+' yy'),($high+'x'+$low+' yy'),('%'+$pair+' yy'),("'"+$pair+"' %"),("'"+$high+"' %"),('yyyy \'+$high),('yyyy \'+$low),('yyyy \'+$pair),('yyyy '+$high+$high+$low),('yyyy '+$low+$high),('yyyy '+$pair+$low),('yyyy '+$high+$pair),("'é日' MMMM"),("'a\'"+$pair+"' MM"))
$formats+=@('\? yyyy','\? yyyy','\? yyyy',"'\?' yyyy",'\? yyyy',('\'+([string][char]0x100)+' yyyy'))
$samples=@(@{ticks=[long]638447204961234567;kind=[DateTimeKind]::Unspecified},@{ticks=[long]3155378975999999999;kind=[DateTimeKind]::Utc})
$strings=@();$rows=@();$culture=[Globalization.CultureInfo]::CurrentCulture
try{
 [Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
 foreach($sample in $samples){foreach($format in $formats){
  $value=[DateTime]::new($sample.ticks,$sample.kind)
  $stringRow=[ordered]@{ticks=$sample.ticks.ToString();kind=$sample.kind.ToString();formatUnits=(Units $format)}
  try{$stringRow.result=[ordered]@{units=(Units ($value.ToString($format,[Globalization.CultureInfo]::InvariantCulture)));singleUnits=(Units ($value.ToString($format)));interfaceUnits=(Units ([IFormattable].GetMethod('ToString').Invoke($value,[object[]]@($format,[Globalization.CultureInfo]::InvariantCulture))))}}catch{$stringRow.result=Failure $_}
  $strings+=$stringRow
  foreach($encoding in @('Char','Utf8')){
   $capacities=0..32
   foreach($capacity in $capacities){
    $written=[int[]]@(99)
    if($encoding -eq 'Char'){$buffer=[char[]]('#'*$capacity);$formatter=$charFormatter}else{$buffer=[byte[]]::new($capacity);[Array]::Fill($buffer,[byte]35);$formatter=$byteFormatter}
    try{$success=$formatter.Invoke($value,$buffer,$written,$format,[Globalization.CultureInfo]::InvariantCulture);$result=[ordered]@{boolean=$success}}catch{$result=Failure $_}
    $row=[ordered]@{ticks=$sample.ticks.ToString();kind=$sample.kind.ToString();formatUnits=(Units $format);encoding=$encoding;capacity=$capacity;written=$written[0];result=$result}
    if($encoding -eq 'Char'){$row.bufferUnits=(Units ([string]::new($buffer)))}else{$row.bufferHex=[Convert]::ToHexString($buffer)}
    $rows+=$row
   }
  }
 }}
}finally{[Globalization.CultureInfo]::CurrentCulture=$culture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=[TimeZoneInfo]::Local.Id;javaZoneProfile='Europe/Zurich';strings=$strings;buffers=$rows;qualification='BOUNDED_INVARIANT_CUSTOM_DATETIME_UNICODE_REFERENCE; PROVIDER_HISTORICAL_ZONES_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned custom DateTime Unicode buffers: $($rows.Count) cases"
