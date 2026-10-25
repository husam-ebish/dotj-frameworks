param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop'
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
$positive=[sbyte].GetMethod('IsPositive',[type[]]@([sbyte]));$negative=[sbyte].GetMethod('IsNegative',[type[]]@([sbyte]));$rows=@()
foreach($value in -128..127){$arguments=[object[]]@([sbyte]$value);$rows+=[ordered]@{value=$value;positive=[bool]$positive.Invoke($null,$arguments);negative=[bool]$negative.Invoke($null,$arguments)}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();cases=$rows;qualification='EXHAUSTIVE_SBYTE_SIGN_PREDICATES; OTHER_APIS_ABI_AND_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 8)+"`n",[Text.UTF8Encoding]::new($false));Write-Output 'PASS pinned SByte sign predicates: 256 values'
