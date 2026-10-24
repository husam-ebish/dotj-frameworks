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
foreach($value in [int[]]@([int]::MinValue,-16777217,-65536,-32769,-32768,-129,-128,-1,0,1,127,128,255,256,32767,32768,65535,65536,16777215,16777216,16777217,[int]::MaxValue)){
 foreach($name in $targets){
  $type=if($null -eq $name){$null}else{[Type]::GetType($name,$true)}
  try{
   $output=$method.Invoke($value,[object[]]@($type,$null));$result=[ordered]@{type=$output.GetType().FullName}
   if($output -is [bool]){$result.boolean=$output}
   elseif($output -is [char]){$result.character=[int]$output}
   elseif($output -is [single]){$result.singleBits=[BitConverter]::SingleToInt32Bits($output).ToString()}
   elseif($output -is [double]){$result.doubleBits=[BitConverter]::DoubleToInt64Bits($output).ToString()}
   else{$result.text=[Convert]::ToString($output,[Globalization.CultureInfo]::InvariantCulture)}
  }catch{$result=Failure $_}
  $rows+=[ordered]@{value=$value;target=$name;result=$result}
 }
}
}finally{[Globalization.CultureInfo]::CurrentCulture=$originalCulture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();cultureProfile='Invariant';queries=$rows;qualification='BOUNDED_INT32_TARGET_CONVERSION_REFERENCE; FULL_PROVIDERS_BOXING_AND_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned Int32 target conversions: $($rows.Count) cases"
