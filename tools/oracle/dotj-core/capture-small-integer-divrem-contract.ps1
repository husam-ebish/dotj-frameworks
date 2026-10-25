param([Parameter(Mandatory)][string]$OutputPath,[string]$InputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
if(-not $InputPath){$InputPath=Join-Path ([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))) 'planning/stage-2/repos/dotj-core/evidence/small-integer-bit-operations-contract-v10.0.12.json'}
$inputs=Get-Content -LiteralPath $InputPath -Raw|ConvertFrom-Json;if($inputs.runtimeVersion -ne '10.0.12' -or $inputs.coreLibSha256 -ne $coreHash){throw 'Pinned integer input values required'}
$types=@()
foreach($profile in $inputs.types){$owner=[type]$profile.fullName;$method=$owner.GetMethod('DivRem',[type[]]@($owner,$owner));$rows=[Collections.Generic.List[object]]::new()
 foreach($left in $profile.values){foreach($right in $profile.values){$arguments=[object[]]@([Convert]::ChangeType($left.value,$owner),[Convert]::ChangeType($right.value,$owner))
  try{$tuple=$method.Invoke($null,$arguments);$result=[object[]]@('V',[long]$tuple.Item1,[long]$tuple.Item2)}catch{$e=$_.Exception.GetBaseException();$result=[object[]]@('E',$e.GetType().FullName,$e.HResult)}
  $rows.Add([object[]]@([long]$left.value,[long]$right.value,$result))
 }}
 $types+=[ordered]@{fullName=$owner.FullName;valueCount=$profile.values.Count;rows=$rows}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();inputEvidence='small-integer-bit-operations-contract-v10.0.12.json';inputSha256=(Get-FileHash -LiteralPath $InputPath -Algorithm SHA256).Hash.ToLowerInvariant();types=$types;qualification='BOUNDED_SMALL_INTEGER_DIVREM; TUPLE_VALUE_ABI_OTHER_APIS_AND_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output 'PASS pinned small-integer DivRem: all byte pairs and wider bit-boundary pairs'
