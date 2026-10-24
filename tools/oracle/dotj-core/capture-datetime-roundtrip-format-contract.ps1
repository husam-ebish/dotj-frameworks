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
if([TimeZoneInfo]::Local.Id -ne 'W. Europe Standard Time'){throw 'Selected offset formatting reference requires W. Europe Standard Time.'}
$culture=[Globalization.CultureInfo]::CurrentCulture
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
try{
$provider=[Globalization.CultureInfo]::InvariantCulture;$formats=@('o','O','r','R','u','U');$samples=@();$strings=@();$buffers=@()
foreach($ticks in [long[]]@(0,1,863999999999,621355968000000000,638447204961234567,3155378975999999999)){foreach($kind in @([DateTimeKind]::Utc,[DateTimeKind]::Unspecified)){
 $samples+=@{inputTicks=$ticks;inputKind=$kind.ToString();route='direct';value=[DateTime]::new($ticks,$kind);fullRange=$true;buffer=($kind -eq [DateTimeKind]::Utc -and $ticks -in @([long]0,[long]3155378975999999999))}
}}
foreach($date in @(@(2024,3,31),@(2024,10,27),@(2026,3,29),@(2026,10,25))){foreach($hour in 0..3){
 $plain=[DateTime]::new($date[0],$date[1],$date[2],$hour,30,0)
 foreach($kind in @([DateTimeKind]::Local,[DateTimeKind]::Unspecified)){
  $value=[DateTime]::SpecifyKind($plain,$kind)
  $samples+=@{inputTicks=$plain.Ticks;inputKind=$kind.ToString();route='direct';value=$value;fullRange=$false;buffer=($date[0] -eq 2024 -and $hour -eq 2 -and (($date[1] -eq 3 -and $kind -eq [DateTimeKind]::Local) -or ($date[1] -eq 10 -and $kind -eq [DateTimeKind]::Unspecified)))}
 }
 $utc=[DateTime]::SpecifyKind($plain,[DateTimeKind]::Utc)
 $samples+=@{inputTicks=$utc.Ticks;inputKind='Utc';route='viaLocal';value=$utc.ToLocalTime();fullRange=$false;buffer=($date[0] -eq 2024 -and $date[1] -eq 10 -and $hour -in @(0,1))}
}}
foreach($sample in $samples){foreach($format in $formats){
 if($sample.fullRange -and $sample.inputKind -eq 'Unspecified' -and $format -ceq 'U'){continue}
 $value=$sample.value;$text=$value.ToString($format,$provider)
 $strings+=[ordered]@{inputTicks=$sample.inputTicks.ToString();inputKind=$sample.inputKind;route=$sample.route;format=$format;text=$text;singleText=$value.ToString($format);interfaceText=([IFormattable].GetMethod('ToString').Invoke($value,[object[]]@($format,$provider)))}
 if(!$sample.buffer){continue}
 foreach($capacity in 0..($text.Length+1)){foreach($encoding in @('Char','Utf8')){
  $written=[int[]]@(99)
  if($encoding -eq 'Char'){$buffer=[char[]]('#'*$capacity);$formatter=$charFormatter}else{$buffer=[byte[]]::new($capacity);[Array]::Fill($buffer,[byte]35);$formatter=$byteFormatter}
  $success=$formatter.Invoke($value,$buffer,$written,$format,$provider)
  $row=[ordered]@{inputTicks=$sample.inputTicks.ToString();inputKind=$sample.inputKind;route=$sample.route;format=$format;capacity=$capacity;encoding=$encoding;success=$success;written=$written[0]}
  if($encoding -eq 'Char'){$row.buffer=[string]::new($buffer)}else{$row.bufferHex=[Convert]::ToHexString($buffer)}
  $buffers+=$row
 }}
}}
}finally{[Globalization.CultureInfo]::CurrentCulture=$culture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=[TimeZoneInfo]::Local.Id;javaZoneProfile='Europe/Zurich';strings=$strings;buffers=$buffers;qualification='BOUNDED_INVARIANT_ROUNDTRIP_RFC_UTC_FORMAT_REFERENCE; MODERN_LOCAL_ZONE_PROFILE_ONLY_FULL_CULTURES_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned roundtrip/RFC/UTC formatting: $($strings.Count) strings and $($buffers.Count) buffers"
