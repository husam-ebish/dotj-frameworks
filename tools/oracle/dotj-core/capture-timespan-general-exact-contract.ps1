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
$parse=New-ExactParser ([TimeSpan]) $false;$tryParse=New-ExactParser ([TimeSpan]) $true
$inputs=@('','0','1','-1','1:2','-1:2','1:2:3','24:00:00','1.2:3','1:2:3:4','1:02:03:04.0000000',
    '1:2:3:4.5','0:00:00:00','0:00:00:00.0','0:0:0:0.0000000','0:00:00:00.00000000',
    '00:00:00.00000005','00:00:00.00000000','1:2:.3','1:2:3.',' 1:2:3 ',"`n1:2:3`n",'+01:02:03',
    '1.02:03:04.0000000','1:02:03:04.','1:02:03:04.12345678','1:02:03:04.00000005',
    '1:24:00:00.0000000','0:00:60:00.0000000','0:00:00:60.0000000',
    '10675199:02:48:05.4775807','10675199:02:48:05.4775808','-10675199:02:48:05.4775808',
    '-10675199:02:48:05.4775809','10675200:00:00:00.0000000','268435456','268435456:00:00:00.0000000',
    '99999999999999999999999999','0000000000000000000000000000',
    ([string][char]160+'1:2:3'+[char]160),([string][char]133+'1:2:3'+[char]133))
$rows=@();$savedCulture=[Globalization.CultureInfo]::CurrentCulture
try{
    [Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
    foreach($ticks in @([long]0,[long]1,[long]-1,[long]9999,[long]10000000,[long]123456789012345,[long]::MinValue,[long]::MaxValue)){
        foreach($format in @('g','G')){$inputs+=[TimeSpan]::FromTicks($ticks).ToString($format,[Globalization.CultureInfo]::InvariantCulture)}
    }
    foreach($text in $inputs){foreach($format in @('g','G')){foreach($offset in @(0,3,7)){
        $formatOffset=if($offset -eq 0){0}else{2}
        $buffer=[char[]](('#'*$offset)+$text+'####');$formatBuffer=[char[]](('X'*$formatOffset)+$format+'YYYY')
        try{$value=$parse.Invoke($buffer,$offset,$text.Length,$formatBuffer,$formatOffset,$format.Length,$null);$result=[ordered]@{ticks=$value.Ticks}}
        catch{$result=Failure $_}
        $output=[TimeSpan[]]@([TimeSpan]::FromTicks(99))
        try{$success=$tryParse.Invoke($buffer,$offset,$text.Length,$formatBuffer,$formatOffset,$format.Length,$null,$output);$tryResult=[ordered]@{boolean=$success}}
        catch{$success=$null;$tryResult=Failure $_}
        $rows+=[ordered]@{type='TimeSpan';input=$text;format=$format;offset=$offset;formatOffset=$formatOffset;styleValue=0
            result=$result;tryResult=$tryResult;trySuccess=$success;tryTicks=$output[0].Ticks}
    }}}
}finally{[Globalization.CultureInfo]::CurrentCulture=$savedCulture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();cases=$rows
    qualification='SELECTED_GENERAL_EXACT_REFERENCE; INVARIANT_NULL_PROVIDER_NONE_STYLE; OTHER_CULTURES_AND_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned TimeSpan invariant general exact oracle: $($rows.Count) cases"
