param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}

class RejectingFormatProvider : System.IFormatProvider { [object] GetFormat([type] $formatType) { throw [InvalidOperationException]::new('provider consulted') } }
$rows=[Collections.Generic.List[object]]::new();$toString=[Enum].GetMethod('ToString',[type[]]@([string],[IFormatProvider]));$default=[Enum].GetMethod('ToString',[type[]]@())
foreach($number in @(-2147483648,-1,0,1,2,3,4,5,6,7,8,9,10,2147483647)){$value=[Enum]::ToObject([Text.NormalizationForm],[int]$number);foreach($format in @($null,'','G','g','F','f','D','d','X','x','GG','Q','0')){foreach($culture in @('','en-US','tr-TR')){
 $provider=[Globalization.CultureInfo]::GetCultureInfo($culture);$result=$null;$failure=$null;try{$parameters=[object[]]::new(2);$parameters[0]=$format;$parameters[1]=$provider;$result=$toString.Invoke($value,$parameters)}catch{$e=$_.Exception;while($e.InnerException){$e=$e.InnerException};$failure=[ordered]@{type=$e.GetType().FullName;message=$e.Message;hResult=$e.HResult}}
 $rows.Add([ordered]@{value=$number;format=$format;culture=$culture;result=$result;failure=$failure;default=$default.Invoke($value,[object[]]@())})
}}}
$trapArguments=[object[]]::new(2);$trapArguments[0]='F';$trapArguments[1]=[RejectingFormatProvider]::new();$trapResult=$toString.Invoke([Enum]::ToObject([Text.NormalizationForm],3),$trapArguments)
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();rows=$rows.ToArray();providerTrapResult=$trapResult;qualification='SELECTED_NORMALIZATION_FORM_ENUM_FORMATTING_ONLY; CONVERSIONS_SPANS_FULL_ENUM_ABI_AND_TASK_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS normalization form formatting capture: $($rows.Count) rows"
