param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
$integerTexts=@('-340282366920938463463374607431768211456','-170141183460469231731687303715884105728','-18446744073709551616','-9223372036854775809','-9223372036854775808','-4294967297','-4294967296','-2147483649','-2147483648','-65537','-65536','-32769','-32768','-257','-256','-129','-128','-127','-1','0','1','126','127','128','255','256','257','32767','32768','65535','65536','2147483647','2147483648','4294967295','4294967296','9223372036854775807','9223372036854775808','18446744073709551615','18446744073709551616','170141183460469231731687303715884105727','340282366920938463463374607431768211455',('1'+'0'*100))
$realTexts=@('-Infinity','NaN','Infinity','-1e100','1e100','-4294967297','-2147483649','-65537','-32769','-257','-129','-128.99','-128.1','-128','-127.99','-1.99','-1','-0.99','-0','0','0.99','1','1.99','126.99','127','127.99','128','254.99','255','255.99','256','32767.99','32768','65535','65535.99','65536','2147483647','2147483647.99','2147483648','4294967295','4294967295.99','4294967296','79228162514264337593543950335','-79228162514264337593543950335')
$sourceTypes=@([sbyte],[byte],[int16],[uint16],[int32],[uint32],[int64],[uint64],[Int128],[UInt128],[single],[double],[Half],[decimal],[System.Numerics.BigInteger])
$targets=@([sbyte],[byte],[uint16],[uint32]);$modes=@('CreateChecked','CreateSaturating','CreateTruncating');$sources=[Collections.Generic.List[object]]::new();$rows=[Collections.Generic.List[object]]::new();$skipped=0
for($sourceIndex=0;$sourceIndex -lt $sourceTypes.Count;$sourceIndex++){
 $sourceType=$sourceTypes[$sourceIndex];$parse=$sourceType.GetMethod('Parse',[type[]]@([string],[IFormatProvider]));$floatSource=$sourceType -in @([single],[double],[Half]);$texts=if($floatSource -or $sourceType -eq [decimal]){$realTexts+$integerTexts}else{$integerTexts};$values=[Collections.Generic.List[object]]::new();$identities=[Collections.Generic.HashSet[string]]::new()
 if($sourceType -eq [sbyte]){$texts=@(-128..127|ForEach-Object {$_.ToString()})}elseif($sourceType -eq [byte]){$texts=@(0..255|ForEach-Object {$_.ToString()})}
 foreach($text in $texts){
  $arguments=[object[]]::new(2);$arguments[0]=$text;$arguments[1]=[Globalization.CultureInfo]::InvariantCulture
  try{$value=$parse.Invoke($null,$arguments)}catch{$skipped++;continue}
  $bits=$null
  if($sourceType -eq [single]){$bits=[BitConverter]::SingleToUInt32Bits($value).ToString('X8')}elseif($sourceType -eq [double]){$bits=[BitConverter]::DoubleToUInt64Bits($value).ToString('X16')}elseif($sourceType -eq [Half]){
   $singleFactory=[single].GetMethods()|Where-Object {$_.Name -eq 'CreateChecked' -and $_.IsGenericMethodDefinition};$asSingle=$singleFactory.MakeGenericMethod([type[]]@([Half])).Invoke($null,[object[]]@($value));$bits=[BitConverter]::SingleToUInt32Bits($asSingle).ToString('X8')
  }
  $canonical=$value.ToString([Globalization.CultureInfo]::InvariantCulture);$identity=if($null -eq $bits){$canonical}else{$bits};if(-not $identities.Add($identity)){continue};$id=$sources.Count;$sources.Add([ordered]@{type=$sourceType.FullName;text=$canonical;bits=$bits});$values.Add([ordered]@{id=$id;value=$value})
 }
 for($targetIndex=0;$targetIndex -lt $targets.Count;$targetIndex++){foreach($mode in $modes){
  $definition=$targets[$targetIndex].GetMethods()|Where-Object {$_.Name -eq $mode -and $_.IsGenericMethodDefinition};$method=$definition.MakeGenericMethod([type[]]@($sourceType))
  foreach($source in $values){try{$result=[object[]]@('V',[long]$method.Invoke($null,[object[]]@($source.value)))}catch{$e=$_.Exception.GetBaseException();$result=[object[]]@('E',$e.GetType().FullName,$e.HResult)};$rows.Add([object[]]@($targetIndex,$source.id,$mode,$result))}
 }}
}
$numerics=[System.Numerics.BigInteger].Assembly
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;numericsAssembly=$numerics.FullName;numericsAssemblySha256=(Get-FileHash -LiteralPath $numerics.Location -Algorithm SHA256).Hash.ToLowerInvariant();oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();sourceTypes=@($sourceTypes|ForEach-Object FullName);sources=$sources;sourceConstructionSkips=$skipped;targets=@($targets|ForEach-Object FullName);rows=$rows;qualification='BOUNDED_GENERIC_NUMERIC_FACTORIES; SOURCE_CONSTRAINTS_CARRIER_ABI_AND_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 10 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned numeric factories: $($sources.Count) source values across $($sourceTypes.Count) types; $($rows.Count) results"
