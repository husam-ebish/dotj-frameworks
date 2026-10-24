param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'TimeSpan style oracle requires pinned CoreLib.'}
$styleType=[Globalization.TimeSpanStyles]
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
function New-TryParser([type]$FormatType){
    $parameters=[type[]]@([string],$FormatType,[IFormatProvider],$styleType,[TimeSpan[]])
    $target=[TimeSpan].GetMethod('TryParseExact',[type[]]@([string],$FormatType,[IFormatProvider],$styleType,[TimeSpan].MakeByRefType()))
    $bridge=[Reflection.Emit.DynamicMethod]::new('StyledExactOut',[bool],$parameters);$il=$bridge.GetILGenerator()
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_2);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3)
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0);$il.Emit([Reflection.Emit.OpCodes]::Ldelema,[TimeSpan])
    $il.Emit([Reflection.Emit.OpCodes]::Call,$target);$il.Emit([Reflection.Emit.OpCodes]::Ret)
    $definition=[type]'System.Func`6';$delegateType=$definition.MakeGenericType([type[]]@($parameters+[bool]))
    return $bridge.CreateDelegate($delegateType)
}
$singleParse=[TimeSpan].GetMethod('ParseExact',[type[]]@([string],[string],[IFormatProvider],$styleType));$singleTry=New-TryParser ([string])
$arrayParse=[TimeSpan].GetMethod('ParseExact',[type[]]@([string],[string[]],[IFormatProvider],$styleType));$arrayTry=New-TryParser ([string[]])
$inputs=@($null,'','0','1','-1','1:2','-1:2','24:00:00','12:34:56.1234567','1.02:03:04.0000005',
    '10675199.02:48:05.4775807','10675199.02:48:05.4775808','-10675199.02:48:05.4775808','garbage')
$singleFormats=@($null,'','c','t','T','g','G','hh\:mm','d\.hh\:mm\:ss\.fffffff','\-d\.hh\:mm\:ss\.fffffff','?')
$nullOnly=[string[]]::new(1)
$sets=@(@{formats=$null},@{formats=[string[]]@()},@{formats=$nullOnly},@{formats=[string[]]@('c')},@{formats=[string[]]@('g','G')},
    @{formats=[string[]]@('hh\:mm','c')},@{formats=[string[]]@('d\.hh\:mm\:ss\.fffffff','c')},@{formats=[string[]]@('','c')})
$rows=@();$savedCulture=[Globalization.CultureInfo]::CurrentCulture
try{
    [Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
    foreach($styleValue in @([int]::MinValue,-1,0,1,2,3,[int]::MaxValue)){
        $style=[Enum]::ToObject($styleType,[int]$styleValue)
        foreach($text in $inputs){foreach($mode in @('single','array')){
            $formats=if($mode -eq 'single'){@($singleFormats)}else{@($sets)}
            foreach($formatEntry in $formats){
                if($mode -eq 'single'){$format=$formatEntry}else{$format=$formatEntry.formats}
                $parse=if($mode -eq 'single'){$singleParse}else{$arrayParse};$tryParse=if($mode -eq 'single'){$singleTry}else{$arrayTry}
                $arguments=[object[]]::new(4);$arguments[0]=$text;$arguments[1]=$format;$arguments[2]=$null;$arguments[3]=$style
                try{$result=[ordered]@{ticks=$parse.Invoke($null,$arguments).Ticks}}catch{$result=Failure $_}
                $output=[TimeSpan[]]@([TimeSpan]::FromTicks(99));$tryArguments=[object[]]::new(5)
                [Array]::Copy($arguments,$tryArguments,4);$tryArguments[4]=$output
                try{$success=$tryParse.DynamicInvoke($tryArguments);$tryResult=[ordered]@{boolean=$success}}catch{$tryResult=Failure $_}
                $row=[ordered]@{input=$text;mode=$mode;style=$styleValue;result=$result;tryResult=$tryResult;tryTicks=$output[0].Ticks}
                if($mode -eq 'single'){$row.format=$format}else{$row.formats=$format};$rows+=$row
            }
        }}
    }
}finally{[Globalization.CultureInfo]::CurrentCulture=$savedCulture}
$names=[Enum]::GetNames($styleType);$declared=@();foreach($name in $names){$declared+=[ordered]@{name=$name;value=[int][Enum]::Parse($styleType,$name)}}
if(@($rows|Where-Object{$_.mode -eq 'array' -and $null -ne $_.formats -and $_.formats.Length -eq 0}).Count -eq 0){throw 'Empty format-array coverage was lost.'}
$control=@($rows|Where-Object{$_.mode -eq 'array' -and $_.input -eq '1' -and $_.style -eq 0 -and $null -ne $_.formats -and $_.formats.Length -eq 2 -and $_.formats[0] -eq 'g'})
if($control.Count -ne 1 -or $control[0].result.ticks -ne 864000000000){throw 'Native format-array invocation control failed.'}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    styleMetadata=[ordered]@{name=$styleType.FullName;isEnum=$styleType.IsEnum;underlyingType=[Enum]::GetUnderlyingType($styleType).FullName;declaredValues=$declared}
    cases=$rows;qualification='SELECTED_STYLE_BEARING_STRING_EXACT_REFERENCE; CULTURE_SPAN_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned TimeSpan style reference: $($rows.Count) cases"
