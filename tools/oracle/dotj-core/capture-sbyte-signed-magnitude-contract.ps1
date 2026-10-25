param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
function Result([Reflection.MethodInfo]$Method,[object[]]$Arguments){try{[ordered]@{value=[int]$Method.Invoke($null,$Arguments)}}catch{$e=$_.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult}}}
$abs=[sbyte].GetMethod('Abs',[type[]]@([sbyte]));$sign=[sbyte].GetMethod('Sign',[type[]]@([sbyte]));$copy=[sbyte].GetMethod('CopySign',[type[]]@([sbyte],[sbyte]));$max=[sbyte].GetMethod('MaxMagnitude',[type[]]@([sbyte],[sbyte]));$min=[sbyte].GetMethod('MinMagnitude',[type[]]@([sbyte],[sbyte]));$values=@();$pairs=@()
foreach($value in -128..127){$arguments=[object[]]@([sbyte]$value);$values+=[ordered]@{value=$value;abs=(Result $abs $arguments);sign=(Result $sign $arguments)}}
$anchors=[int[]]@(-128,-127,-126,-100,-65,-64,-42,-10,-9,-2,-1,0,1,2,9,10,42,63,64,65,100,126,127)
foreach($x in $anchors){foreach($y in $anchors){$arguments=[object[]]@([sbyte]$x,[sbyte]$y);$pairs+=[ordered]@{x=$x;y=$y;copySign=(Result $copy $arguments);maxMagnitude=(Result $max $arguments);minMagnitude=(Result $min $arguments)}}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();typeName='System.SByte';values=$values;pairs=$pairs;qualification='BOUNDED_SBYTE_SIGNED_MAGNITUDE; OTHER_ARITHMETIC_GENERIC_INTERFACES_AND_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 14)+"`n",[Text.UTF8Encoding]::new($false));Write-Output 'PASS pinned SByte signed magnitude: 256 values and 529 pairs'
