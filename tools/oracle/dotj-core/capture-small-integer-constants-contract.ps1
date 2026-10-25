param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
$rows=@()
foreach($numericType in @([sbyte],[byte],[uint16],[uint32])){
 $min=[long]$numericType.GetField('MinValue').GetRawConstantValue();$max=[long]$numericType.GetField('MaxValue').GetRawConstantValue();$cases=@()
 foreach($number in @(($min-1),$min,($min+1),($max-1),$max,($max+1))){
  try{$value=[Convert]::ChangeType([long]$number,$numericType,[Globalization.CultureInfo]::InvariantCulture);$result=[ordered]@{value=[long]$value;text=$value.ToString([Globalization.CultureInfo]::InvariantCulture)}}catch{$e=$_.Exception.GetBaseException();$result=[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult}}
  $cases+=[ordered]@{input=[long]$number;result=$result}
 }
 $rows+=[ordered]@{fullName=$numericType.FullName;min=$min;max=$max;cases=$cases}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();types=$rows;qualification='SMALL_INTEGER_NATIVE_LIMITS_AND_CONVERSION_BOUNDARIES; CARRIER_FIELD_WIDTHS_AND_RELEASE_REMAIN_JAVA_ADAPTER_SCOPE'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned small-integer limits: $($rows.Count) types"
