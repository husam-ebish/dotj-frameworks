param([Parameter(Mandatory)][string]$OutputPath,[string]$PlanPath=(Join-Path $PSScriptRoot 'default-member-info-equality-plan-v1.json'))
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture;[Globalization.CultureInfo]::CurrentUICulture=[Globalization.CultureInfo]::InvariantCulture




function Units($value){if($null -eq $value){return $null};return ,([int[]][char[]][string]$value)}




function Owner($name){$list=[object].Assembly.GetType('System.Collections.Generic.List`1');switch($name){'ListD'{return $list};'ListS'{return $list.MakeGenericType([type[]]@([string]))};'ListI'{return $list.MakeGenericType([type[]]@([int]))};default{return [Type]::GetType($name,$true,$false)}}}
$plan=Get-Content -LiteralPath $PlanPath -Raw|ConvertFrom-Json;$members=[Collections.Generic.List[Reflection.MemberInfo]]::new();$arrays=[Collections.Generic.List[object]]::new();$metadata=[Collections.Generic.List[object]]::new();$apiCalls=0
foreach($label in $plan.owners){$owner=Owner $label;$first=$owner.GetDefaultMembers();$second=$owner.GetDefaultMembers();$apiCalls+=2;$count=$first.Length;$saved=$null;if($count -gt 0){$saved=$first[0];foreach($item in @($first[0],$second[0])){$members.Add($item);$metadata.Add([ordered]@{index=$metadata.Count;name=$item.Name;memberType=[int]$item.MemberType;declaringType=$item.DeclaringType.FullName;reflectedType=$item.ReflectedType.FullName})};$first[0]=$null};$third=$owner.GetDefaultMembers();$apiCalls++;$arrays.Add([ordered]@{owner=$label;count=$count;sameArray=[object]::ReferenceEquals($first,$second);defensive=($count -eq 0 -or [object]::ReferenceEquals($saved,$third[0]))})}
$rows=[Collections.Generic.List[object]]::new();$hashes=[Collections.Generic.List[object]]::new();$foreign=[object]::new();for($left=0;$left -lt $members.Count;$left++){for($right=0;$right -lt ($members.Count+3);$right++){$other=if($right -lt $members.Count){$members[$right]}elseif($right -eq $members.Count){$foreign}elseif($right -eq ($members.Count+1)){[int]}else{$null};$equal=$members[$left].Equals($other);$apiCalls++;$hash=$true;if($equal){$hash=$members[$left].GetHashCode() -eq $other.GetHashCode();$apiCalls+=2};$rows.Add([ordered]@{left=$left;right=$right;equal=$equal;reference=[object]::ReferenceEquals($members[$left],$other);equalHash=$hash})};$firstHash=$members[$left].GetHashCode();$secondHash=$members[$left].GetHashCode();$apiCalls+=2;$hashes.Add([ordered]@{left=$left;stable=($firstHash -eq $secondHash)})}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();planSha256=(Get-FileHash -LiteralPath $PlanPath -Algorithm SHA256).Hash.ToLowerInvariant();memberCount=$members.Count;apiCalls=$apiCalls;arrays=$arrays.ToArray();metadata=$metadata.ToArray();rows=$rows.ToArray();hashes=$hashes.ToArray();qualification=$plan.qualification};[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 14 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS default member identity: $apiCalls lookup/equality/hash calls"
