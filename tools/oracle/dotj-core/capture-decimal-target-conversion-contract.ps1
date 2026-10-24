param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum query oracle requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$originalCulture=[Globalization.CultureInfo]::CurrentCulture
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
try{
$rows=@();$method=[IConvertible].GetMethod('ToType')
$targets=@('System.Boolean','System.Char','System.SByte','System.Byte','System.Int16','System.UInt16','System.Int32','System.UInt32','System.Int64','System.UInt64','System.Single','System.Double','System.Decimal','System.String','System.Object','System.DateTime','System.DBNull','System.Enum','System.ValueType','System.IConvertible','System.TimeSpan','System.Int32[]',$null)
foreach($text in @('-79228162514264337593543950335','-18446744073709551615.5','-9223372036854775808.5','-9223372036854775808.4','-2147483648.5','-32768.5','-128.5','-128.4','-2.5','-1.5','-0.6','-0.5','-0.4','-0.0000000000000000000000000001','-0','-0.00','0','0.00','0.0000000000000000000000000001','0.1','0.1000000000000000055511151231','0.4','0.5','0.6','1.5','2.5','127.4','127.5','128.5','255.4','255.5','256.5','32767.4','32767.5','65535.4','65535.5','2147483647.4','2147483647.5','4294967295.4','4294967295.5','9223372036854775807.4','9223372036854775807.5','18446744073709551615.4','18446744073709551615.5','16777217','16777217.0000000001','1.000000059604644775390625','1.0000000596046447753906250001','1.0000000596046447753906249999','1.0000001788139343261718750000','1.0000001788139343261718749999','1.0000001788139343261718750001','-1.0000000596046447753906250001','79228162514264337593543950335')){
 $value=[decimal]::Parse($text,[Globalization.CultureInfo]::InvariantCulture)
 foreach($name in $targets){
  $type=if($null -eq $name){$null}else{[Type]::GetType($name,$true)}
  try{
   $output=$method.Invoke($value,[object[]]@($type,$null));$result=[ordered]@{type=$output.GetType().FullName}
   if($output -is [bool]){$result.boolean=$output}
   elseif($output -is [char]){$result.character=[int]$output}
   elseif($output -is [single]){$result.singleBits=[BitConverter]::SingleToInt32Bits($output).ToString()}
   elseif($output -is [double]){$result.doubleBits=[BitConverter]::DoubleToInt64Bits($output).ToString()}
   else{$result.text=[Convert]::ToString($output,[Globalization.CultureInfo]::InvariantCulture)}
   if($output -is [decimal]){$result.decimalBits=[decimal]::GetBits($output)}
  }catch{$result=Failure $_}
  $rows+=[ordered]@{value=$text;target=$name;result=$result}
 }
}
}finally{[Globalization.CultureInfo]::CurrentCulture=$originalCulture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();cultureProfile='Invariant';queries=$rows;qualification='BOUNDED_DECIMAL_TARGET_CONVERSION_REFERENCE; FULL_PROVIDERS_BOXING_AND_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned Decimal target conversions: $($rows.Count) cases"
