param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Array exact oracle requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$parse=[TimeSpan].GetMethod('ParseExact',[type[]]@([string],[string[]],[IFormatProvider]))
$target=[TimeSpan].GetMethod('TryParseExact',[type[]]@([string],[string[]],[IFormatProvider],[TimeSpan].MakeByRefType()))
$bridge=[Reflection.Emit.DynamicMethod]::new('ArrayExactOut',[bool],[type[]]@([string],[string[]],[IFormatProvider],[TimeSpan[]]));$il=$bridge.GetILGenerator()
$il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_2)
$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0);$il.Emit([Reflection.Emit.OpCodes]::Ldelema,[TimeSpan])
$il.Emit([Reflection.Emit.OpCodes]::Call,$target);$il.Emit([Reflection.Emit.OpCodes]::Ret)
$tryParse=$bridge.CreateDelegate([Func[string,string[],IFormatProvider,TimeSpan[],bool]])
$nullOnly=[string[]]::new(1);$leadingNull=[string[]]::new(2);$leadingNull[1]='c';$trailingNull=[string[]]::new(2);$trailingNull[0]='c'
$sets=@(@{formats=$null},@{formats=[string[]]@()},@{formats=$nullOnly},@{formats=[string[]]@('')},
    @{formats=[string[]]@('c')},@{formats=[string[]]@('hh\:mm')},@{formats=[string[]]@('bad','c')},@{formats=[string[]]@('c','bad')},
    @{formats=[string[]]@('','c')},@{formats=[string[]]@('c','')},@{formats=$leadingNull},@{formats=$trailingNull},
    @{formats=[string[]]@('g','G')},@{formats=[string[]]@('G','g')},@{formats=[string[]]@("''")},@{formats=[string[]]@('hh','%d')},
    @{formats=[string[]]@('hh\:mm\:ss\.FFFFFFF')},@{formats=[string[]]@('?','g','c')})
if($sets[2].formats.Length -ne 1 -or $null -ne $sets[2].formats[0]){throw 'True null-element format-array coverage missing.'}
$inputs=@($null,'','0','1','01','1:2','12:34','12:34:56','12:34:56.001','1.02:03:04.0000005',
    '1:02:03:04.0000005','-12:34:56','10675199.02:48:05.4775807','-10675199.02:48:05.4775808',
    '10675199.02:48:05.4775808','10675200','24:00:00','bad',' 1:2 ')
$rows=@();$savedCulture=[Globalization.CultureInfo]::CurrentCulture
try{
    [Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
    foreach($text in $inputs){foreach($set in $sets){
        $formats=$set.formats;$arguments=[object[]]::new(3);$arguments[0]=$text;$arguments[1]=$formats;$arguments[2]=$null
        try{$value=$parse.Invoke($null,$arguments);$result=[ordered]@{ticks=$value.Ticks}}catch{$result=Failure $_}
        $output=[TimeSpan[]]@([TimeSpan]::FromTicks(99))
        try{$success=$tryParse.Invoke($text,$formats,$null,$output);$tryResult=[ordered]@{boolean=$success}}catch{$success=$null;$tryResult=Failure $_}
        $rows+=[ordered]@{input=$text;formats=$formats;result=$result;tryResult=$tryResult;trySuccess=$success;tryTicks=$output[0].Ticks}
    }}
}finally{[Globalization.CultureInfo]::CurrentCulture=$savedCulture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();cases=$rows
    qualification='SELECTED_STRING_FORMAT_ARRAY_NONE_STYLE_REFERENCE; CULTURES_STYLES_AND_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned TimeSpan array exact oracle: $($rows.Count) cases"
