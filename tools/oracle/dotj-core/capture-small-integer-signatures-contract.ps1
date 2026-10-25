param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
$flags=[Reflection.BindingFlags]'Public,Instance,Static,DeclaredOnly';$types=@()
foreach($numericType in @([sbyte],[byte],[uint16],[uint32])){
 $methods=@(foreach($method in ($numericType.GetMethods($flags)|Sort-Object Name,ToString)){
  [ordered]@{name=$method.Name;signature=$method.ToString();isStatic=$method.IsStatic;isSpecialName=$method.IsSpecialName;genericArity=$method.GetGenericArguments().Count;returnType=$method.ReturnType.ToString();parameters=@(foreach($parameter in $method.GetParameters()){[ordered]@{name=$parameter.Name;type=$parameter.ParameterType.ToString();isOut=$parameter.IsOut}})}
 })
 $fields=@(foreach($field in $numericType.GetFields($flags)){[ordered]@{name=$field.Name;type=$field.FieldType.ToString();isStatic=$field.IsStatic;isLiteral=$field.IsLiteral;value=$(if($field.IsLiteral){[string]$field.GetRawConstantValue()}else{$null})}})
 $types+=[ordered]@{fullName=$numericType.FullName;methods=$methods;fields=$fields;interfaces=@($numericType.GetInterfaces()|ForEach-Object ToString);constructors=@($numericType.GetConstructors($flags)|ForEach-Object ToString)}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();types=$types;qualification='DECLARED_SMALL_INTEGER_METADATA_ONLY; PROJECTION_BEHAVIOR_ACCEPTANCE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 16)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned small-integer signature inventory: $($types.Count) types"
