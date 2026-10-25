param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$coreHash = (Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if ([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678') {
    throw 'DateTime oracle requires the pinned .NET 10.0.12 CoreLib.'
}
function Failure($ErrorRecord) {
    $value = $ErrorRecord.Exception.GetBaseException()
    [ordered]@{ exception = $value.GetType().FullName; paramName = $(if ($value -is [ArgumentException]) { $value.ParamName } else { $null }); hResult = $value.HResult }
}
if([TimeZoneInfo]::Local.Id -ne 'W. Europe Standard Time'){throw 'Selected format-list reference requires W. Europe Standard Time.'}
$culture=[Globalization.CultureInfo]::CurrentCulture
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
try{
$provider=[Globalization.CultureInfo]::InvariantCulture;$formats=[char[]]('dDfFgGmMoOrRstTuUyY?S'+[char]0);$samples=@();$rows=@();$patterns=@()
foreach($format in [char[]]'dDtTmMyYfFgG'){try{$result=[ordered]@{patterns=$provider.DateTimeFormat.GetAllDateTimePatterns($format)}}catch{$result=Failure $_};$patterns+=[ordered]@{format=[int]$format;result=$result}}
foreach($ticks in [long[]]@(0,1,621355968000000000,638447204961234567,3155378975999999999)){$samples+=@{inputTicks=$ticks;inputKind='Utc';route='direct';value=[DateTime]::new($ticks,[DateTimeKind]::Utc)}}
foreach($date in @(@(2024,3,31),@(2024,10,27),@(2026,3,29),@(2026,10,25))){foreach($hour in 0..3){
 $plain=[DateTime]::new($date[0],$date[1],$date[2],$hour,30,0)
 foreach($kind in @([DateTimeKind]::Local,[DateTimeKind]::Unspecified)){$samples+=@{inputTicks=$plain.Ticks;inputKind=$kind.ToString();route='direct';value=[DateTime]::SpecifyKind($plain,$kind)}}
 $utc=[DateTime]::SpecifyKind($plain,[DateTimeKind]::Utc);$samples+=@{inputTicks=$utc.Ticks;inputKind='Utc';route='viaLocal';value=$utc.ToLocalTime()}
}}
foreach($sample in $samples){
 foreach($withProvider in @($false,$true)){
  $result=if($withProvider){[ordered]@{texts=$sample.value.GetDateTimeFormats($provider)}}else{[ordered]@{texts=$sample.value.GetDateTimeFormats()}}
  $rows+=[ordered]@{inputTicks=$sample.inputTicks.ToString();inputKind=$sample.inputKind;route=$sample.route;format=$null;withProvider=$withProvider;result=$result}
 }
 foreach($format in $formats){foreach($withProvider in @($false,$true)){
  try{$texts=if($withProvider){$sample.value.GetDateTimeFormats($format,$provider)}else{$sample.value.GetDateTimeFormats($format)};$result=[ordered]@{texts=@($texts)}}catch{$result=Failure $_}
  $rows+=[ordered]@{inputTicks=$sample.inputTicks.ToString();inputKind=$sample.inputKind;route=$sample.route;format=[int]$format;withProvider=$withProvider;result=$result}
 }}
}
}finally{[Globalization.CultureInfo]::CurrentCulture=$culture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=[TimeZoneInfo]::Local.Id;javaZoneProfile='Europe/Zurich';patternReference=$patterns;queries=$rows;qualification='BOUNDED_INVARIANT_DATETIME_FORMAT_LIST_REFERENCE; MODERN_LOCAL_PROFILE_ONLY_CULTURES_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 18)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned invariant DateTime format lists: $($rows.Count) calls"
