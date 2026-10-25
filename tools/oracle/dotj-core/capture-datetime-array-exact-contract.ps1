param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'DateTime style oracle requires pinned CoreLib.'}
$styleType=[Globalization.DateTimeStyles]
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
if([TimeZoneInfo]::Local.Id -ne 'W. Europe Standard Time'){throw 'Selected style parse reference requires W. Europe Standard Time.'}
function New-ArrayExactParser([bool]$Span,[bool]$Try){
 $inputType=if($Span){[type]'System.ReadOnlySpan[char]'}else{[string]}
 $signature=[type[]]@($inputType,[string[]],[IFormatProvider],$styleType);$parameters=[type[]]@([string],[string[]],[IFormatProvider],$styleType)
 if($Try){$signature+=[DateTime].MakeByRefType();$parameters+=[DateTime[]];$returnType=[bool];$name='TryParseExact'}else{$returnType=[DateTime];$name='ParseExact'}
 $target=[DateTime].GetMethod($name,[type[]]$signature);$bridge=[Reflection.Emit.DynamicMethod]::new('StyledExactDateTime',$returnType,[type[]]$parameters);$il=$bridge.GetILGenerator()
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);if($Span){$il.Emit([Reflection.Emit.OpCodes]::Call,[MemoryExtensions].GetMethod('AsSpan',[type[]]@([string])))}
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_1)
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_2);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3)
 if($Try){$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0);$il.Emit([Reflection.Emit.OpCodes]::Ldelema,[DateTime])}
 $il.Emit([Reflection.Emit.OpCodes]::Call,$target);$il.Emit([Reflection.Emit.OpCodes]::Ret)
 $definition=if($Try){[type]'System.Func`6'}else{[type]'System.Func`5'}
 return $bridge.CreateDelegate($definition.MakeGenericType([type[]]@($parameters+$returnType)))
}
function ValueResult([DateTime]$value){
 $result=[ordered]@{ticks=$value.Ticks.ToString();kind=$value.Kind.ToString()}
 if($value.Year -ge 2020 -and $value.Year -le 2030){$result.binary=$value.ToBinary().ToString();$result.utcTicks=$value.ToUniversalTime().Ticks.ToString()}
 return $result
}
$stringParse=New-ArrayExactParser $false $false;$stringTry=New-ArrayExactParser $false $true;$spanParse=New-ArrayExactParser $true $false;$spanTry=New-ArrayExactParser $true $true
$nullOnly=[string[]]::new(1);$firstNull=[string[]]::new(2);$firstNull[1]='yyyy-MM-dd';$lastNull=[string[]]::new(2);$lastNull[0]='yyyy-MM-dd'
$sets=@(@{formats=$null},@{formats=[string[]]@()},@{formats=$nullOnly},@{formats=[string[]]@('')},@{formats=$firstNull},@{formats=$lastNull},@{formats=[string[]]@('','yyyy-MM-dd')},@{formats=[string[]]@('yyyy-MM-dd','')},@{formats=[string[]]@('?','yyyy-MM-dd')},@{formats=[string[]]@('yyyy-MM-dd','?')},@{formats=[string[]]@('yyyy-MM-dd')},@{formats=[string[]]@('s','yyyy-MM-dd')},@{formats=[string[]]@('o','O','yyyy-MM-ddTHH:mm:ss.fffffff','yyyy-MM-dd HH:mm:ss')},@{formats=[string[]]@('yyyy-MM-dd','yyyy-MM-dd')})
$inputs=@($null,'','bad','2024-02-29',' 2024-02-29 ','2024 - 02 - 29','2024-02-29 12:34:56','2024-02-29T12:34:56','2024-02-29T12:34:56.1234567','2024-02-29T12:34:56.1234567Z','2024-10-27T02:30:00.0000000+02:00','2024-10-27T02:30:00.0000000+01:00','2024-02-30')
$requests=@();foreach($style in @(-1,0,7,16,32,64,80,96,128,256)){foreach($text in $inputs){foreach($set in $sets){$requests+=@{style=$style;input=$text;formats=$set.formats}}}}
$seen=[Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal);$rows=@();$culture=[Globalization.CultureInfo]::CurrentCulture
try{
 [Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
 foreach($request in $requests){foreach($mode in @('String','Span')){
  $text=$request.input;$formats=$request.formats;$styleValue=[int]$request.style;$key=$mode+'|'+$styleValue+'|'+$(if($null -eq $text){'<null>'}else{$text})+'|'+$(if($null -eq $formats){'<null>'}else{ConvertTo-Json -InputObject $formats -Compress})
  if(!$seen.Add($key)){continue};$style=[Enum]::ToObject($styleType,$styleValue)
  $parse=if($mode -eq 'String'){$stringParse}else{$spanParse};$tryParse=if($mode -eq 'String'){$stringTry}else{$spanTry}
  $arguments=[object[]]::new(4);$arguments[0]=$text;$arguments[1]=$formats;$arguments[2]=[Globalization.CultureInfo]::InvariantCulture;$arguments[3]=$style
  try{$result=ValueResult ($parse.DynamicInvoke($arguments))}catch{$result=Failure $_}
  $output=[DateTime[]]@([DateTime]::new([long]99,[DateTimeKind]::Utc));$tryArguments=[object[]]::new(5);[Array]::Copy($arguments,$tryArguments,4);$tryArguments[4]=$output
  try{$success=$tryParse.DynamicInvoke($tryArguments);$tryResult=[ordered]@{boolean=$success}}catch{$tryResult=Failure $_}
  $rows+=[ordered]@{input=$text;formats=$formats;style=$styleValue;mode=$mode;result=$result;tryResult=$tryResult;tryValue=(ValueResult $output[0])}
 }}
}finally{[Globalization.CultureInfo]::CurrentCulture=$culture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=[TimeZoneInfo]::Local.Id;javaZoneProfile='Europe/Zurich';cases=$rows;qualification='BOUNDED_SELECTED_ARRAY_EXACT_STYLE_REFERENCE; MODERN_LOCAL_ONLY_FULL_FORMAT_GRAMMAR_PROVIDER_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 18)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned DateTime array exact parsing: $($rows.Count) cases"
