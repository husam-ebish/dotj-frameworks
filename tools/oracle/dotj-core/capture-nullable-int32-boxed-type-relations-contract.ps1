param([Parameter(Mandatory)][string]$OutputPath,[string]$PlanPath=(Join-Path $PSScriptRoot 'nullable-int32-boxed-type-relations-plan-v1.json'))
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture;[Globalization.CultureInfo]::CurrentUICulture=[Globalization.CultureInfo]::InvariantCulture




function Units($value){if($null -eq $value){return $null};return ,([int[]][char[]][string]$value)}
function Actual($name){switch($name){'null'{return $null};'Boolean'{return [bool]$true};'Byte'{return [byte]42};'Char'{return [char]65};'DateTime'{return [DateTime]::new(0)};'Decimal'{return [decimal]42};'Double'{return [double]1.25};'Int16'{return [int16]-42};'Int32'{return [int]-42};'Int64'{return [long]-42};'SByte'{return [sbyte]-42};'Single'{return [single]1.25};'String'{return 'sentinel'};'UInt16'{return [uint16]42};'UInt32'{return [uint32]42};'UInt64'{return [uint64]42}}}

function Shape($name){$definition=[object].Assembly.GetType('System.Nullable`1');switch($name){'D'{return $definition};'C'{return $definition.MakeGenericType([type[]]@([int]))};'P'{return $definition.GetGenericArguments()[0]};'null'{return $null};default{return [object].Assembly.GetType('System.'+$name,$true)}}}
$plan=Get-Content -LiteralPath $PlanPath -Raw|ConvertFrom-Json;$rows=[Collections.Generic.List[object]]::new()
foreach($left in $plan.types){$target=Shape $left;foreach($right in (@('null')+$plan.types)){$candidate=Shape $right;$rows.Add([ordered]@{route='assign';left=$left;right=$right;result=$target.IsAssignableFrom($candidate)})};foreach($right in $plan.types){$candidate=Shape $right;$rows.Add([ordered]@{route='subclass';left=$left;right=$right;result=$target.IsSubclassOf($candidate)})};foreach($right in $plan.actualTypes){$value=Actual $right;$rows.Add([ordered]@{route='instance';left=$left;right=$right;result=$target.IsInstanceOfType($value)})}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();planSha256=(Get-FileHash -LiteralPath $PlanPath -Algorithm SHA256).Hash.ToLowerInvariant();rows=$rows.ToArray();qualification=$plan.qualification};[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 10 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS Nullable type relations: $($rows.Count) comparisons"
