param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'DateTime style oracle requires pinned CoreLib.'}
$styleType=[Globalization.DateTimeStyles]
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
if([TimeZoneInfo]::Local.Id -ne 'W. Europe Standard Time'){throw 'Selected style parse reference requires W. Europe Standard Time.'}
function New-StyledParser([bool]$Span,[bool]$Try){
 $inputType=if($Span){[type]'System.ReadOnlySpan[char]'}else{[string]}
 $signature=[type[]]@($inputType,[IFormatProvider],$styleType)
 $parameters=[type[]]@([string],[IFormatProvider],$styleType)
 if($Try){$signature+=[DateTime].MakeByRefType();$parameters+=[DateTime[]];$returnType=[bool];$name='TryParse'}else{$returnType=[DateTime];$name='Parse'}
 $target=[DateTime].GetMethod($name,[type[]]$signature)
 $bridge=[Reflection.Emit.DynamicMethod]::new('StyledDateTimeParser',$returnType,[type[]]$parameters);$il=$bridge.GetILGenerator()
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0)
 if($Span){$il.Emit([Reflection.Emit.OpCodes]::Call,[MemoryExtensions].GetMethod('AsSpan',[type[]]@([string])))}
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_2)
 if($Try){$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0);$il.Emit([Reflection.Emit.OpCodes]::Ldelema,[DateTime])}
 $il.Emit([Reflection.Emit.OpCodes]::Call,$target);$il.Emit([Reflection.Emit.OpCodes]::Ret)
 $definition=if($Try){[type]'System.Func`5'}else{[type]'System.Func`4'}
 return $bridge.CreateDelegate($definition.MakeGenericType([type[]]@($parameters+$returnType)))
}
function ValueResult([DateTime]$value){
 $result=[ordered]@{ticks=$value.Ticks.ToString();kind=$value.Kind.ToString()}
 if($value.Year -ge 2020 -and $value.Year -le 2030){$result.binary=$value.ToBinary().ToString();$result.utcTicks=$value.ToUniversalTime().Ticks.ToString()}
 return $result
}
$stringParse=New-StyledParser $false $false;$stringTry=New-StyledParser $false $true;$spanParse=New-StyledParser $true $false;$spanTry=New-StyledParser $true $true
$texts=@($null,'','garbage','2023-02-29','2024-02-29','2024-02-29T12:34:56',' 2024-02-29T12:34:56 ','2024-02-29T12:34:56.12345675','2024-03-31T02:30:00','2024-10-27T02:30:00','2026-03-29T02:30:00','2026-10-25T02:30:00','2024-10-27T00:30:00Z','2024-10-27T01:30:00Z','2024-10-27T02:30:00+02:00','2024-10-27T02:30:00+01:00','2024-10-27T02:30:00+00:00','2024-02-29T12:34:56-05:30','2024-02-29T12:34:56+14:00','2024-02-29T12:34:56-14:00','2024-02-29T12:34:56+14:01','2024-02-29T12:34:56+15:00','2024-02-29T12:34:56+01:60','2024-02-29T12:34:56z')
$requests=@();foreach($style in 0..255){$requests+=@{style=$style;text='2024-02-29T12:34:56'}}
foreach($style in @([int]::MinValue,-1,0,1,2,4,7,8,16,32,48,64,80,96,128,136,144,160,192,256,[int]::MaxValue)){foreach($text in $texts){$requests+=@{style=$style;text=$text}}}
foreach($style in @(0,1,7,8,32,80,128)){foreach($text in @('0001-01-01','9999-12-31T23:59:59.9999999')){$requests+=@{style=$style;text=$text}}}
$seen=[Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal);$rows=@();$culture=[Globalization.CultureInfo]::CurrentCulture
try{
 [Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
 foreach($request in $requests){foreach($mode in @('String','Span')){
  $text=$request.text;$styleValue=[int]$request.style;$key=$mode+'|'+$styleValue+'|'+$(if($null -eq $text){'<null>'}else{$text})
  if(!$seen.Add($key)){continue};$style=[Enum]::ToObject($styleType,$styleValue)
  $parse=if($mode -eq 'String'){$stringParse}else{$spanParse};$tryParse=if($mode -eq 'String'){$stringTry}else{$spanTry}
  $arguments=[object[]]::new(3);$arguments[0]=$text;$arguments[1]=[Globalization.CultureInfo]::InvariantCulture;$arguments[2]=$style
  try{$result=ValueResult ($parse.DynamicInvoke($arguments))}catch{$result=Failure $_}
  $output=[DateTime[]]@([DateTime]::new([long]99,[DateTimeKind]::Utc));$tryArguments=[object[]]::new(4);[Array]::Copy($arguments,$tryArguments,3);$tryArguments[3]=$output
  try{$success=$tryParse.DynamicInvoke($tryArguments);$tryResult=[ordered]@{boolean=$success}}catch{$tryResult=Failure $_}
  $rows+=[ordered]@{input=$text;style=$styleValue;mode=$mode;result=$result;tryResult=$tryResult;tryValue=(ValueResult $output[0])}
 }}
}finally{[Globalization.CultureInfo]::CurrentCulture=$culture}
$declared=@();foreach($name in [Enum]::GetNames($styleType)){$declared+=[ordered]@{name=$name;value=[int][Enum]::Parse($styleType,$name)}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=[TimeZoneInfo]::Local.Id;javaZoneProfile='Europe/Zurich';styleValues=$declared;cases=$rows;qualification='BOUNDED_INVARIANT_ISO_STYLE_PARSE_REFERENCE; MODERN_LOCAL_PROFILE_ONLY_FULL_GRAMMAR_PROVIDER_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 18)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned DateTime style parsing: $($rows.Count) String/span cases"
