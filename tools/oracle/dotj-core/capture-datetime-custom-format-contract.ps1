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
$formats=@('%y','yy','yyy','yyyy','yyyyy','yyyyyyyyyyyy','%M','MM','MMM','MMMM','MMMMM','%d','dd','ddd','dddd','ddddd','%H','HH','HHHH','%h','hh','hhhh','%m','mm','mmmm','%s','ss','ssss','%t','tt','tttt','%g','gggg','%f','ff','fffffff','%F','FF','FFFFFFF','ss.FFFFFFF','ss.FFF','%z','zz','zzz','zzzz','%K','KK','yyyy/MM/dd HH:mm:ss.fffffff K','yyyy-MM-ddTHH:mm:ss.FFFFFFFK',"'hello' yyyy",'"hello" MM',"'a\'b' dd",'\y\y','%/','%:','%x','abc','yyyy qqq',"yyyy 'a\'b'",'yyyy \','yyyy %','%%','%','ffffffff','FFFFFFFF',"yyyy 'unclosed",'yyyy "unclosed','HH:mm:ss.fffffff','HH:mm:ss.FFFFFFF','日yyyy月MM')
$ticksList=[long[]]@(0,1,863999999999,31241376000000000,621355968000000000,638447204961234567,638447204960000000,638637714001000000,3155378975999999999)
$strings=@();$culture=[Globalization.CultureInfo]::CurrentCulture
try{
 [Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
 foreach($ticks in $ticksList){foreach($kind in [Enum]::GetValues([DateTimeKind])){foreach($format in $formats){
  # Historical timezone equivalence is not selected for custom offset tokens.
  if(($format.Contains('z') -or $format.Contains('K')) -and $ticks -lt 864000000000){continue}
  if(($format.Contains('z') -or $format.Contains('K')) -and ($ticks -lt 637134336000000000 -or $ticks -gt 640605888000000000) -and $kind -ne [DateTimeKind]::Utc){continue}
  $value=[DateTime]::new($ticks,$kind);$row=[ordered]@{ticks=$ticks.ToString();kind=$kind.ToString();format=$format}
  try{$row.result=[ordered]@{text=$value.ToString($format,[Globalization.CultureInfo]::InvariantCulture);singleText=$value.ToString($format);interfaceText=([IFormattable].GetMethod('ToString').Invoke($value,[object[]]@($format,[Globalization.CultureInfo]::InvariantCulture)))}}catch{$row.result=Failure $_}
  $strings+=$row
 }}}
}finally{[Globalization.CultureInfo]::CurrentCulture=$culture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=[TimeZoneInfo]::Local.Id;javaZoneProfile='Europe/Zurich';strings=$strings;qualification='BOUNDED_INVARIANT_CUSTOM_DATETIME_STRING_REFERENCE; BUFFER_PROVIDER_HISTORICAL_ZONE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned custom DateTime strings: $($strings.Count) cases"
