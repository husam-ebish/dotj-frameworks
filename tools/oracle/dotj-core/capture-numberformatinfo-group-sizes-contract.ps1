param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture;[Globalization.CultureInfo]::CurrentUICulture=[Globalization.CultureInfo]::InvariantCulture
$names=@('NumberGroupSizes','CurrencyGroupSizes','PercentGroupSizes')
function Seed([int]$Index){switch($Index){0{$a=[int[]]@(3)};1{$a=[int[]]@(1,2,0)};2{$a=[int[]]@()}};return ,$a}
function Input-Sizes([int]$Index){switch($Index){0{$a=$null};1{$a=[int[]]@()};2{$a=[int[]]@(0)};3{$a=[int[]]@(1)};4{$a=[int[]]@(9)};5{$a=[int[]]@(3,0)};6{$a=[int[]]@(1,2,3)};7{$a=[int[]]@(9,9,0)};8{$a=[int[]]@(-1)};9{$a=[int[]]@(10)};10{$a=[int[]]@(0,3)};11{$a=[int[]]@(3,0,0)};12{$a=[int[]]@(3,-1)};13{$a=[int[]]@([int]::MinValue)};14{$a=[int[]]@([int]::MaxValue)}};return ,$a}
function Snapshot($N){$r=[ordered]@{};foreach($name in $names){$r[$name]=[int[]][Globalization.NumberFormatInfo].GetProperty($name).GetValue($N)};return $r}
$rows=[Collections.Generic.List[object]]::new()
foreach($name in $names){foreach($seed in 0..2){foreach($profile in 0..14){
 $n=[Globalization.NumberFormatInfo]::new();$property=[Globalization.NumberFormatInfo].GetProperty($name);$property.SetValue($n,(Seed $seed));$before=Snapshot $n;$inputSizes=Input-Sizes $profile;$inputBefore=if([object]::ReferenceEquals($inputSizes,$null)){$null}else{,$inputSizes.Clone()}
 try{$property.SetValue($n,$inputSizes);$result=[ordered]@{ok=$true}}catch{$e=$_.Exception;while($e -is [Reflection.TargetInvocationException] -or $e -is [Management.Automation.MethodInvocationException]){$e=$e.InnerException};$result=[ordered]@{ok=$false;exception=$e.GetType().FullName;messageUnits=[int[]][char[]]$e.Message;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
 $inputAfter=if([object]::ReferenceEquals($inputSizes,$null)){$null}else{,$inputSizes.Clone()};$afterSet=Snapshot $n
 if(-not [object]::ReferenceEquals($inputSizes,$null) -and $inputSizes.Length -gt 0){$inputSizes[0]=8};$afterInputMutation=Snapshot $n
 $first=[int[]]$property.GetValue($n);$second=[int[]]$property.GetValue($n);$distinct=-not [object]::ReferenceEquals($first,$second);if($first.Length -gt 0){$first[0]=7};$afterGetterMutation=Snapshot $n
 $rows.Add([ordered]@{property=$name;seed=$seed;profile=$profile;inputBefore=$inputBefore;inputAfter=$inputAfter;before=$before;result=$result;afterSet=$afterSet;afterInputMutation=$afterInputMutation;distinctGetters=$distinct;afterGetterMutation=$afterGetterMutation})
}}}
if($rows.Count -ne 135){throw 'Wrong group-size matrix'}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();culture='Invariant';properties=$names;rows=$rows.ToArray();qualification='SELECTED_WRITABLE_GROUP_SIZE_VALIDATION_AND_DEFENSIVE_COPIES_ONLY; READONLY_CLONE_CONCURRENCY_FULL_CULTURE_METADATA_AND_TASK_ACCEPTANCE_OPEN'};[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 20 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output 'PASS group-size native matrix: 3 properties, 135 cases'
