param([Parameter(Mandatory)][string]$OutputPath,[string]$PlanPath=(Join-Path $PSScriptRoot 'method-info-equality-plan-v1.json'))
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture;[Globalization.CultureInfo]::CurrentUICulture=[Globalization.CultureInfo]::InvariantCulture




function Units($value){if($null -eq $value){return $null};return ,([int[]][char[]][string]$value)}



$plan=Get-Content -LiteralPath $PlanPath -Raw|ConvertFrom-Json;$methods=[Collections.Generic.List[Reflection.MethodInfo]]::new();$flags=[Reflection.BindingFlags]'Public,Instance';$apiCalls=0
foreach($spec in $plan.interfaces){$type=[Type]::GetType($spec.type,$true,$false);$parameters=[type[]]@($spec.parameters|ForEach-Object {[Type]::GetType($_,$true,$false)});foreach($route in $plan.routes){for($pass=0;$pass -lt $plan.passes;$pass++){$method=switch($route){'name'{$type.GetMethod($spec.method)};'flags'{$type.GetMethod($spec.method,$flags)};'types'{$type.GetMethod($spec.method,$parameters)};'flags-types'{$type.GetMethod($spec.method,$flags,$null,$parameters,$null)};'methods'{$type.GetMethods($flags)[0]};'ignore-case'{$type.GetMethod($spec.method.ToUpperInvariant(),($flags -bor [Reflection.BindingFlags]::IgnoreCase))}};if($null -eq $method -or $method.Name -ne $spec.method){throw 'Unexpected lookup method'};$methods.Add($method);$apiCalls++}}}
$rows=[Collections.Generic.List[object]]::new();$hashes=[Collections.Generic.List[object]]::new();$foreign=[object]::new();for($left=0;$left -lt $methods.Count;$left++){for($right=0;$right -lt ($methods.Count+3);$right++){$other=if($right -lt $methods.Count){$methods[$right]}elseif($right -eq $methods.Count){$foreign}elseif($right -eq ($methods.Count+1)){[int]}else{$null};$equal=$methods[$left].Equals($other);$apiCalls++;$hashesAgree=$true;if($equal){$hashesAgree=$methods[$left].GetHashCode() -eq $other.GetHashCode();$apiCalls+=2};$rows.Add([ordered]@{left=$left;right=$right;equal=$equal;reference=[object]::ReferenceEquals($methods[$left],$other);equalHash=$hashesAgree})};$first=$methods[$left].GetHashCode();$second=$methods[$left].GetHashCode();$apiCalls+=2;$hashes.Add([ordered]@{left=$left;stable=($first -eq $second)})}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();planSha256=(Get-FileHash -LiteralPath $PlanPath -Algorithm SHA256).Hash.ToLowerInvariant();methodCount=$methods.Count;apiCalls=$apiCalls;rows=$rows.ToArray();hashes=$hashes.ToArray();qualification=$plan.qualification};[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS interface method equality: $apiCalls calls"
