param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if ([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678') {throw 'Temporal span parsing oracle requires pinned CoreLib.'}
function New-Parser([type]$ValueType,[bool]$Try) {
    $span=[type]'System.ReadOnlySpan[char]'
    $array=$ValueType.MakeArrayType()
    $parameters=if($Try){[type[]]@([char[]],[int],[int],[IFormatProvider],$array)}else{[type[]]@([char[]],[int],[int],[IFormatProvider])}
    $return=if($Try){[bool]}else{$ValueType}
    $bridge=[Reflection.Emit.DynamicMethod]::new('TemporalSpanParse',$return,$parameters)
    $il=$bridge.GetILGenerator()
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0)
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_1)
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_2)
    $il.Emit([Reflection.Emit.OpCodes]::Newobj,$span.GetConstructor([type[]]@([char[]],[int],[int])))
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_3)
    if($Try){
        $il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4)
        $il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0)
        $il.Emit([Reflection.Emit.OpCodes]::Ldelema,$ValueType)
        $target=$ValueType.GetMethod('TryParse',[type[]]@($span,[IFormatProvider],$ValueType.MakeByRefType()))
        $definition=[type]'System.Func`6';$delegate=$definition.MakeGenericType([type[]]@([char[]],[int],[int],[IFormatProvider],$array,[bool]))
    }else{
        $target=$ValueType.GetMethod('Parse',[type[]]@($span,[IFormatProvider]))
        $definition=[type]'System.Func`5';$delegate=$definition.MakeGenericType([type[]]@([char[]],[int],[int],[IFormatProvider],$ValueType))
    }
    if($null -eq $target){throw 'Pinned public Char-span parse signature missing.'}
    $il.Emit([Reflection.Emit.OpCodes]::Call,$target);$il.Emit([Reflection.Emit.OpCodes]::Ret)
    return $bridge.CreateDelegate($delegate)
}
$rows=@();$savedCulture=[Globalization.CultureInfo]::CurrentCulture
try{
    [Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
    foreach($name in @('DateTime','TimeSpan')){
        $type=[type]('System.'+$name);$parse=New-Parser $type $false;$tryParse=New-Parser $type $true
        $inputs=if($name -eq 'DateTime'){@('','0001-01-01','9999-12-31','2024-02-29','1900-02-29','0000-01-01','garbage',
            '2024-02-29T12:34:56.12345675','9999-12-31T23:59:59.99999995','2024-02-29 12:34:56',' 2024-02-29 ')}else{
            @('','0','1:2','1:2:3','1.02:03:04.0000005','-10675199.02:48:05.4775808','10675199.02:48:05.4775808',
                'garbage','1:61:0','00:00:00.00000005',' 1:2:3 ')}
        foreach($text in $inputs){foreach($offset in @(0,3,7)){
            $buffer=[char[]](('#'*$offset)+$text+'####')
            try{$value=$parse.Invoke($buffer,$offset,$text.Length,$null);$result=[ordered]@{ticks=$value.Ticks}}
            catch{$e=$_.Exception.GetBaseException();$result=[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult}}
            if($name -eq 'DateTime' -and $result.Contains('ticks')){$result.kind=$value.Kind.ToString()}
            $output=[Array]::CreateInstance($type,1)
            $seed=if($name -eq 'DateTime'){[DateTime]::new(2000,1,1)}else{[TimeSpan]::FromTicks(99)}
            $output.SetValue($seed,0)
            $success=$tryParse.Invoke($buffer,$offset,$text.Length,$null,$output)
            $value=$output.GetValue(0)
            $row=[ordered]@{type=$name;input=$text;offset=$offset;result=$result;trySuccess=$success;tryTicks=$value.Ticks}
            if($name -eq 'DateTime'){$row.tryKind=$value.Kind.ToString()}
            $rows+=$row
        }}
    }
}finally{[Globalization.CultureInfo]::CurrentCulture=$savedCulture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();cases=$rows
    qualification='SELECTED_CHAR_SPAN_PARSE_REFERENCE; PROVIDERS_STYLES_AND_LANGUAGE_MAPPING_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned Char-span parsing oracle: $($rows.Count) cases"
