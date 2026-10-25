param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture;[Globalization.CultureInfo]::CurrentUICulture=[Globalization.CultureInfo]::InvariantCulture
$types=@()
foreach($numericType in @([sbyte],[byte],[uint16],[uint32])){
 if($numericType -eq [sbyte]){$values=[long[]](-128..127);$name='Log2'}elseif($numericType -eq [byte]){$values=[long[]](0..255);$name='Sign'}else{
  $name='Sign';$bits=if($numericType -eq [uint16]){16}else{32};$max=([long]1 -shl $bits)-1;$set=[Collections.Generic.HashSet[long]]::new();[void]$set.Add(0);[void]$set.Add($max)
  foreach($bit in 0..($bits-1)){$power=[long]1 -shl $bit;foreach($value in @(($power-1),$power,($power+1))){if($value -ge 0 -and $value -le $max){[void]$set.Add($value)}}};$values=[long[]]@($set|Sort-Object)
 }
 $method=$numericType.GetMethod($name,[type[]]@($numericType));$rows=@()
 foreach($value in $values){$arguments=[object[]]@([Convert]::ChangeType($value,$numericType))
  try{$result=[ordered]@{value=[long]$method.Invoke($null,$arguments)}}catch{$e=$_.Exception.GetBaseException();$result=[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$e.ParamName;actualValue=$e.ActualValue;message=$e.Message}}
  $rows+=[ordered]@{value=$value;result=$result}
 }
 $types+=[ordered]@{fullName=$numericType.FullName;method=$name;values=$rows}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();types=$types;qualification='BOUNDED_INTEGER_SIGN_AND_LOG2_ERRORS; OTHER_APIS_AND_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false));Write-Output 'PASS pinned integer sign/log boundaries: 652 values'
