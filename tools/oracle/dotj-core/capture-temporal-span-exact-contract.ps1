param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Exact span oracle requires pinned CoreLib.'}
function New-ExactParser([type]$ValueType,[bool]$Try){
    $span=[type]'System.ReadOnlySpan[char]';$array=$ValueType.MakeArrayType()
    $styles=[type]('System.Globalization.'+$ValueType.Name+'Styles')
    $parameters=[Collections.Generic.List[type]]::new()
    foreach($type in @([char[]],[int],[int],[char[]],[int],[int],[IFormatProvider])){$parameters.Add($type)}
    if($Try){$parameters.Add($array)}
    $return=if($Try){[bool]}else{$ValueType}
    $bridge=[Reflection.Emit.DynamicMethod]::new('TemporalSpanExact',$return,$parameters.ToArray());$il=$bridge.GetILGenerator()
    $ctor=$span.GetConstructor([type[]]@([char[]],[int],[int]))
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_2)
    $il.Emit([Reflection.Emit.OpCodes]::Newobj,$ctor)
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_3);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]5)
    $il.Emit([Reflection.Emit.OpCodes]::Newobj,$ctor)
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]6);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0)
    if($Try){
        $il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]7);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0);$il.Emit([Reflection.Emit.OpCodes]::Ldelema,$ValueType)
        $target=$ValueType.GetMethod('TryParseExact',[type[]]@($span,$span,[IFormatProvider],$styles,$ValueType.MakeByRefType()))
        $definition=[type]'System.Func`9';$parameters.Add([bool])
    }else{
        $target=$ValueType.GetMethod('ParseExact',[type[]]@($span,$span,[IFormatProvider],$styles))
        $definition=[type]'System.Func`8';$parameters.Add($ValueType)
    }
    if($null -eq $target){throw 'Expected style-bearing CLR span signature missing.'}
    $il.Emit([Reflection.Emit.OpCodes]::Call,$target);$il.Emit([Reflection.Emit.OpCodes]::Ret)
    return $bridge.CreateDelegate($definition.MakeGenericType($parameters.ToArray()))
}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult}}
$rows=@();$savedCulture=[Globalization.CultureInfo]::CurrentCulture
try{
    [Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
    foreach($name in @('DateTime','TimeSpan')){
        $type=[type]('System.'+$name);$parse=New-ExactParser $type $false;$tryParse=New-ExactParser $type $true
        $inputs=if($name -eq 'DateTime'){@('','0001-01-01','2024-02-29','2024-02-29T12:34:56.1234567','0000-01-01','garbage')}
            else{@('','0','1:2','1.02:03:04.0000005','-10675199.02:48:05.4775808','garbage')}
        $formats=if($name -eq 'DateTime'){@('','yyyy-MM-dd','yyyy-MM-ddTHH:mm:ss.fffffff','?')}else{@('','c','t','T','?')}
        foreach($text in $inputs){foreach($format in $formats){foreach($offset in @(0,3,7)){
            $formatOffset=if($offset -eq 0){0}else{2}
            $buffer=[char[]](('#'*$offset)+$text+'####');$formatBuffer=[char[]](('X'*$formatOffset)+$format+'YYYY')
            try{$value=$parse.Invoke($buffer,$offset,$text.Length,$formatBuffer,$formatOffset,$format.Length,$null);$result=[ordered]@{ticks=$value.Ticks};if($name -eq 'DateTime'){$result.kind=$value.Kind.ToString()}}
            catch{$result=Failure $_}
            $output=[Array]::CreateInstance($type,1);$seed=if($name -eq 'DateTime'){[DateTime]::new(2000,1,1)}else{[TimeSpan]::FromTicks(99)};$output.SetValue($seed,0)
            try{$success=$tryParse.Invoke($buffer,$offset,$text.Length,$formatBuffer,$formatOffset,$format.Length,$null,$output);$tryResult=[ordered]@{boolean=$success}}
            catch{$success=$null;$tryResult=Failure $_}
            $value=$output.GetValue(0)
            $row=[ordered]@{type=$name;input=$text;format=$format;offset=$offset;formatOffset=$formatOffset;styleValue=0
                result=$result;tryResult=$tryResult;trySuccess=$success;tryTicks=$value.Ticks}
            if($name -eq 'DateTime'){$row.tryKind=$value.Kind.ToString()};$rows+=$row
        }}}
    }
}finally{[Globalization.CultureInfo]::CurrentCulture=$savedCulture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();cases=$rows
    qualification='SELECTED_CHAR_SPAN_EXACT_REFERENCE; NONE_STYLE_ADAPTER_ONLY; FULL_STYLES_AND_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned exact Char-span oracle: $($rows.Count) cases"
