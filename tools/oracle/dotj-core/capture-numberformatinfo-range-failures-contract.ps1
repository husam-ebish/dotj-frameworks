param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture;[Globalization.CultureInfo]::CurrentUICulture=[Globalization.CultureInfo]::InvariantCulture
$names=@('NumberDecimalDigits','CurrencyDecimalDigits','PercentDecimalDigits','NumberNegativePattern','CurrencyPositivePattern','CurrencyNegativePattern','PercentPositivePattern','PercentNegativePattern');$maxima=@(99,99,99,4,3,16,3,11);$inputs=@([int]::MinValue,-100,-1,0,1,2,3,4,5,6,10,11,12,15,16,17,18,98,99,100,[int]::MaxValue)
function Snapshot($N){$values=@();foreach($name in $names){$values+=@([Globalization.NumberFormatInfo].GetProperty($name).GetValue($N))};return ,$values}
$rows=[Collections.Generic.List[object]]::new()
for($p=0;$p -lt $names.Count;$p++){foreach($initial in @(0,[int][Math]::Floor($maxima[$p]/2),$maxima[$p])){foreach($inputValue in $inputs){
 $n=[Globalization.NumberFormatInfo]::new();$property=[Globalization.NumberFormatInfo].GetProperty($names[$p]);$property.SetValue($n,$initial);$before=Snapshot $n
 try{$property.SetValue($n,$inputValue);$result=[ordered]@{ok=$true}}catch{$e=$_.Exception;while($e -is [Reflection.TargetInvocationException] -or $e -is [Management.Automation.MethodInvocationException]){$e=$e.InnerException};$result=[ordered]@{ok=$false;exception=$e.GetType().FullName;messageUnits=[int[]][char[]]$e.Message;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null});actualValue=$(if($e -is [ArgumentOutOfRangeException]){$e.ActualValue}else{$null})}}
 $rows.Add([ordered]@{property=$names[$p];maximum=$maxima[$p];initial=$initial;inputValue=$inputValue;before=$before;result=$result;after=(Snapshot $n)})
}}}
if($rows.Count -ne 504){throw 'Wrong NumberFormatInfo range matrix'}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();culture='Invariant';properties=$names;maxima=$maxima;inputs=$inputs;rows=$rows.ToArray();qualification='SELECTED_WRITABLE_NUMBERFORMATINFO_DIGIT_PATTERN_RANGES_ONLY; READONLY_CLONE_CULTURE_FULL_METADATA_AND_TASK_ACCEPTANCE_OPEN'};[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 20 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output 'PASS NumberFormatInfo native ranges: 8 properties, 504 cases'
