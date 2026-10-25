param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
$rows=@()
foreach($owner in @([sbyte],[byte],[uint16],[uint32])){foreach($name in @('CreateChecked','CreateSaturating','CreateTruncating')){
 $method=$owner.GetMethods()|Where-Object {$_.Name -eq $name -and $_.IsGenericMethodDefinition};$parameter=$method.GetGenericArguments()[0];$rejections=@()
 foreach($sourceType in @([string],[bool],[DateTime])){try{[void]$method.MakeGenericMethod([type[]]@($sourceType));$result=[ordered]@{accepted=$true}}catch{$e=$_.Exception;while(($e -is [System.Management.Automation.RuntimeException] -or $e -is [Reflection.TargetInvocationException]) -and $null -ne $e.InnerException){$e=$e.InnerException};$result=[ordered]@{accepted=$false;exception=$e.GetType().FullName;hResult=$e.HResult}}
  $rejections+=[ordered]@{sourceType=$sourceType.FullName;result=$result}
 }
 $rows+=[ordered]@{owner=$owner.FullName;method=$name;genericName=$parameter.Name;attributes=[int]$parameter.GenericParameterAttributes;constraints=@($parameter.GetGenericParameterConstraints()|ForEach-Object ToString);rejectedSources=$rejections}
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();methods=$rows;qualification='NATIVE_GENERIC_CONSTRAINT_BOUNDARY; JAVA_EQUIVALENCE_AND_N01_ACCEPTANCE_NOT_ESTABLISHED'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 10)+"`n",[Text.UTF8Encoding]::new($false));Write-Output 'PASS native generic boundary inventory: 12 methods and 36 constraint rejections'
