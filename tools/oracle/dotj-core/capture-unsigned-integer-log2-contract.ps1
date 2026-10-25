param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
$types=@()
foreach($numericType in @([byte],[uint16],[uint32])){
 if($numericType -eq [byte]){$values=[long[]](0..255)}else{
  $bits=if($numericType -eq [uint16]){16}else{32};$max=([long]1 -shl $bits)-1;$set=[Collections.Generic.HashSet[long]]::new();[void]$set.Add(0);[void]$set.Add($max)
  foreach($bit in 0..($bits-1)){$power=[long]1 -shl $bit;foreach($value in @(($power-1),$power,($power+1))){if($value -ge 0 -and $value -le $max){[void]$set.Add($value)}}};$values=[long[]]@($set|Sort-Object)
 }
 $method=$numericType.GetMethod('Log2',[type[]]@($numericType));$rows=@()
 foreach($value in $values){$arguments=[object[]]@([Convert]::ChangeType($value,$numericType));$rows+=[ordered]@{value=$value;result=[long]$method.Invoke($null,$arguments)}}
 $types+=[ordered]@{fullName=$numericType.FullName;values=$rows}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();types=$types;qualification='BOUNDED_UNSIGNED_LOG2; SIGNED_NEGATIVE_DOMAIN_OTHER_APIS_AND_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false));Write-Output 'PASS pinned unsigned Log2: 396 values across three types'
