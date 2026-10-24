param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if ([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678') {
    throw 'Temporal span oracle requires pinned CoreLib.'
}
function New-Formatter([type]$ValueType,[type]$ElementType) {
    $array=$ElementType.MakeArrayType()
    $definition=[type]'System.Span`1'; $span=$definition.MakeGenericType($ElementType)
    $method=[Reflection.Emit.DynamicMethod]::new('TemporalOffsetTryFormat',[bool],
        [type[]]@($ValueType,$array,[int[]],[string],[IFormatProvider],[int],[int]))
    $il=$method.GetILGenerator()
    $target=$ValueType.GetMethod('TryFormat',[type[]]@($span,[int].MakeByRefType(),[type]'System.ReadOnlySpan[char]',[IFormatProvider]))
    $ctor=$span.GetConstructor([type[]]@($array,[int],[int]))
    $il.Emit([Reflection.Emit.OpCodes]::Ldarga_S,[byte]0)
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_1)
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]5)
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]6)
    $il.Emit([Reflection.Emit.OpCodes]::Newobj,$ctor)
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_2)
    $il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0)
    $il.Emit([Reflection.Emit.OpCodes]::Ldelema,[int])
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_3)
    $il.Emit([Reflection.Emit.OpCodes]::Call,[MemoryExtensions].GetMethod('AsSpan',[type[]]@([string])))
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4)
    $il.Emit([Reflection.Emit.OpCodes]::Call,$target)
    $il.Emit([Reflection.Emit.OpCodes]::Ret)
    $definition=[type]'System.Func`8'
    $delegate=$definition.MakeGenericType([type[]]@($ValueType,$array,[int[]],[string],[IFormatProvider],[int],[int],[bool]))
    return $method.CreateDelegate($delegate)
}
$rows=@()
$savedCulture=[Globalization.CultureInfo]::CurrentCulture
try {
    [Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
    foreach ($name in @('TimeSpan')) {
        $type=[type]('System.'+$name)
        $charFormatter=New-Formatter $type ([char]); $byteFormatter=New-Formatter $type ([byte])
        $ticksList=@([long]::MinValue,[long]-123456789012345,[long]-10000000,[long]-10000,[long]-1,[long]0,[long]1,[long]10000,[long]10000000,[long]123456789012345,[long]::MaxValue)
        $formats=@('g','G')
        foreach ($ticks in $ticksList) {
            if ($name -eq 'TimeSpan') {$kinds=@($null)}
            else {$kinds=@([DateTimeKind]::Unspecified,[DateTimeKind]::Utc,[DateTimeKind]::Local)}
            foreach ($kind in $kinds) {
                $value=if ($name -eq 'TimeSpan') {[TimeSpan]::FromTicks($ticks)} else {[DateTime]::new($ticks,$kind)}
                foreach ($format in $formats) {
                    $text=$value.ToString($format,[Globalization.CultureInfo]::InvariantCulture);$required=$text.Length
                    foreach ($offset in @(0,3)) {
                        foreach ($capacity in @(0,1,($required-1),$required,($required+1))) {
                            foreach ($encoding in @('Char','Utf8')) {
                                $length=$offset+$capacity+4
                                if ($encoding -eq 'Char') {$buffer=[char[]]('#'*$length); $formatter=$charFormatter}
                                else {$buffer=[byte[]]::new($length); [Array]::Fill($buffer,[byte]35); $formatter=$byteFormatter}
                                $written=[int[]]@(99)
                                try {$result=[ordered]@{boolean=$formatter.Invoke($value,$buffer,$written,$format,$null,$offset,$capacity)}}
                                catch {$e=$_.Exception.GetBaseException(); $result=[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
                                $row=[ordered]@{type=$name;ticks=$ticks;kind=$(if($null -eq $kind){$null}else{$kind.ToString()});format=$format
                                    text=$text;offset=$offset;capacity=$capacity;encoding=$encoding;result=$result;written=$written[0]}
                                if ($encoding -eq 'Char') {$row.buffer=[string]::new($buffer)} else {$row.bufferHex=[Convert]::ToHexString($buffer)}
                                $rows+=$row
                            }
                        }
                    }
                }
            }
        }
    }
} finally {[Globalization.CultureInfo]::CurrentCulture=$savedCulture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();cases=$rows
    qualification='SELECTED_INVARIANT_GENERAL_FORMAT_REFERENCE; NULL_PROVIDER_ONLY; CULTURE_BYREF_LIFETIME_AND_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned temporal span oracle: $($rows.Count) cases"
