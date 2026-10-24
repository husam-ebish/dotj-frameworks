param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Saturation oracle requires pinned CoreLib.'}
if([TimeZoneInfo]::Local.Id -ne 'W. Europe Standard Time'){throw 'Selected direct DateTime profile requires Windows W. Europe Standard Time.'}
$rows=[Collections.Generic.List[object]]::new()
function Add-Result($Scenario,$Operation,$InputTicks,$InputKind,$Result,$Comparison='exact',$JavaZone='Europe/Zurich',$CandidateKind=$null,$ReferenceApi=$null){
    if($null -eq $CandidateKind){$CandidateKind=$Result.Kind.ToString()}
    if($null -eq $ReferenceApi){$ReferenceApi='System.DateTime.'+$Operation}
    $row=[ordered]@{scenario=$Scenario;operation=$Operation;input=$InputTicks;inputKind=$InputKind;javaZone=$JavaZone;comparison=$Comparison
        referenceApi=$ReferenceApi;referenceTicks=$Result.Ticks;referenceKind=$Result.Kind.ToString();candidateKind=$CandidateKind}
    $row.referenceInputKind=if($Scenario -eq 'explicitNegativeZoneConverter' -and $Operation -eq 'ToUniversalTime'){'Unspecified'}else{$InputKind}
    if($Comparison -eq 'classificationAndNormalizationOnly'){$row.normalizedBinary=$Result.ToBinary();$row.normalizedUtcTicks=$Result.ToUniversalTime().Ticks}
    $rows.Add($row)
}
foreach($ticks in @([long]0,[long]1,([DateTime]::MaxValue.Ticks-1),[DateTime]::MaxValue.Ticks)){
    foreach($kind in @([DateTimeKind]::Unspecified,[DateTimeKind]::Utc,[DateTimeKind]::Local)){
        $value=[DateTime]::new($ticks,$kind)
        Add-Result 'direct' 'ToUniversalTime' $ticks $kind.ToString() $value.ToUniversalTime()
        $comparison=if($ticks -le 1 -and $kind -ne [DateTimeKind]::Local){'classificationAndNormalizationOnly'}else{'exact'}
        Add-Result 'direct' 'ToLocalTime' $ticks $kind.ToString() $value.ToLocalTime() $comparison
    }
}
foreach($fileTime in @([long]0,[long]1,[long]2650467743999999998,[long]2650467743999999999)){
    Add-Result 'fileTime' 'FromFileTimeUtc' $fileTime $null ([DateTime]::FromFileTimeUtc($fileTime))
    $comparison=if($fileTime -le 1){'classificationAndNormalizationOnly'}else{'exact'}
    Add-Result 'fileTime' 'FromFileTime' $fileTime $null ([DateTime]::FromFileTime($fileTime)) $comparison
}
$negativeZone=[TimeZoneInfo]::FindSystemTimeZoneById('Eastern Standard Time')
foreach($ticks in @(([DateTime]::MaxValue.Ticks-1),[DateTime]::MaxValue.Ticks)){
    $value=[DateTime]::new($ticks,[DateTimeKind]::Unspecified)
    Add-Result 'explicitNegativeZoneConverter' 'ToUniversalTime' $ticks 'Local' ([TimeZoneInfo]::ConvertTimeToUtc($value,$negativeZone)) 'exact' 'America/New_York' 'Utc' 'System.TimeZoneInfo.ConvertTimeToUtc(DateTime, TimeZoneInfo)'
}
foreach($ticks in @([long]0,[long]1)){
    $value=[DateTime]::new($ticks,[DateTimeKind]::Utc)
    Add-Result 'explicitNegativeZoneConverter' 'ToLocalTime' $ticks 'Utc' ([TimeZoneInfo]::ConvertTimeFromUtc($value,$negativeZone)) 'exact' 'America/New_York' 'Local' 'System.TimeZoneInfo.ConvertTimeFromUtc(DateTime, TimeZoneInfo)'
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=[TimeZoneInfo]::Local.Id
    explicitNegativeOffsetZone=$negativeZone.Id;cases=$rows
    comparisonPolicy='Six historical Local results check Kind and normalized UTC/binary only. Four negative-offset saturation cases use explicitly identified TimeZoneInfo converter oracles; Java ToLocalTime Kind is Local while the nonlocal native converter returns Unspecified.'
    qualification='BOUNDED_SATURATION_REFERENCE; HISTORICAL_TICK_PARITY_OTHER_ZONES_AND_FULL_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned DateTime saturation reference: $($rows.Count) cases"
