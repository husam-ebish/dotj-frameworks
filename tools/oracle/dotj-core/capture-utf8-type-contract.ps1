param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
$types=@([Text.Encoding],[Text.UTF8Encoding],[Text.EncoderFallbackException],[Text.DecoderFallbackException]);$metadata=@();$lookups=@()
foreach($type in $types){foreach($shape in @($type,$type.MakeArrayType())){
 $metadata+=[ordered]@{fullName=$shape.FullName;name=$shape.Name;namespace=$shape.Namespace;assemblyQualifiedName=$shape.AssemblyQualifiedName;baseType=$shape.BaseType.FullName;isAbstract=$shape.IsAbstract;isSealed=$shape.IsSealed;isPublic=$shape.IsPublic;isClass=$shape.IsClass;isValueType=$shape.IsValueType;isSerializable=$shape.IsSerializable;nativeInterfaces=@($shape.GetInterfaces()|ForEach-Object FullName)}
 foreach($query in @($shape.FullName,$shape.AssemblyQualifiedName,$shape.FullName.ToLowerInvariant(),$shape.FullName.ToUpperInvariant(),($shape.FullName+', mscorlib'),($shape.FullName+', Missing.Encoding.Assembly'))){foreach($ignoreCase in @($false,$true)){
  try{$resolved=[Type]::GetType($query,$false,$ignoreCase);$result=[ordered]@{ok=$true;resolved=$(if($null -eq $resolved){$null}else{$resolved.FullName})}}catch{$e=$_.Exception;while(($e -is [Management.Automation.RuntimeException] -or $e -is [Reflection.TargetInvocationException]) -and $null -ne $e.InnerException){$e=$e.InnerException};$result=[ordered]@{ok=$false;exception=$e.GetType().FullName}}
  $lookups+=[ordered]@{query=$query;ignoreCase=$ignoreCase;result=$result}
 }}
}}
$relations=@();$targets=@([object],[ArgumentException])+$types
foreach($target in $targets){foreach($source in $targets){$relations+=[ordered]@{target=$target.FullName;source=$source.FullName;assignable=$target.IsAssignableFrom($source);subclass=$source.IsSubclassOf($target)}}}
$instances=[object[]]::new(7);$instances[0]=[object]::new();$instances[1]=[ArgumentException]::new();$instances[2]=[Text.UTF8Encoding]::new();$instances[3]=[Text.UTF8Encoding]::new($true,$true);$instances[4]=[Text.EncoderFallbackException]::new();$instances[5]=[Text.DecoderFallbackException]::new();$instances[6]=$null;$instanceRows=@()
foreach($target in $targets){foreach($index in 0..6){$instanceRows+=[ordered]@{target=$target.FullName;instance=$index;isInstance=$target.IsInstanceOfType($instances[$index])}}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();types=$metadata;lookups=$lookups;relations=$relations;instances=$instanceRows;qualification='SELECTED_UTF8_LOGICAL_TYPE_IDENTITY_ONLY; ICLONEABLE_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 11)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned UTF-8 type identity: $($metadata.Count) shapes, $($lookups.Count) lookups, $($relations.Count) relations, $($instanceRows.Count) instances"
