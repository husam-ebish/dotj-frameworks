param([Parameter(Mandatory)][string]$OutputPath,[string]$InputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
if(-not $InputPath){$InputPath=Join-Path ([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))) 'planning/stage-2/repos/dotj-core/evidence/small-integer-bit-operations-contract-v10.0.12.json'}
$inputs=Get-Content -LiteralPath $InputPath -Raw|ConvertFrom-Json;if($inputs.runtimeVersion -ne '10.0.12' -or $inputs.coreLibSha256 -ne $coreHash){throw 'Pinned UInt32 inputs required'}
$set=[Collections.Generic.HashSet[long]]::new();foreach($row in $inputs.types[3].values){[void]$set.Add([long]$row.value)};$state=[long]20261025
foreach($index in 1..128){$state=($state*1664525+1013904223)-band 4294967295L;[void]$set.Add($state)}
$values=[long[]]@($set|Sort-Object);$method=[uint32].GetMethod('BigMul',[type[]]@([uint32],[uint32]));$rows=[Collections.Generic.List[object]]::new()
foreach($left in $values){foreach($right in $values){$arguments=[object[]]@([uint32]$left,[uint32]$right);$product=$method.Invoke($null,$arguments);$rows.Add([object[]]@($left,$right,$product.ToString([Globalization.CultureInfo]::InvariantCulture)))}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();inputEvidence='small-integer-bit-operations-contract-v10.0.12.json';inputSha256=(Get-FileHash -LiteralPath $InputPath -Algorithm SHA256).Hash.ToLowerInvariant();valueCount=$values.Count;rows=$rows;qualification='BOUNDED_UINT32_BIGMUL_REFERENCE; UINT64_CARRIER_ABI_AND_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 8 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned UInt32 BigMul: $($rows.Count) products"
