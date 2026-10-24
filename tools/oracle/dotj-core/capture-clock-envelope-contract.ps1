param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Clock envelope fixture requires pinned CoreLib.'}
if([TimeZoneInfo]::Local.Id -ne 'W. Europe Standard Time'){throw 'Designed modern clock-envelope fixture requires the recorded W. Europe host profile.'}
. (Join-Path $PSScriptRoot 'clock-envelope-v1.ps1')
$rows=[Collections.Generic.List[object]]::new()
function Add-EnvelopeCase($Name,[DateTime]$BeforeUtc,[DateTime]$AfterUtc,[DateTime]$Candidate,[string]$ExpectedStatus,[string]$Property='Now'){
    $beforeProperty=switch($Property){'UtcNow'{$BeforeUtc};'Now'{$BeforeUtc.ToLocalTime()};'Today'{$BeforeUtc.ToLocalTime().Date}}
    $afterProperty=switch($Property){'UtcNow'{$AfterUtc};'Now'{$AfterUtc.ToLocalTime()};'Today'{$AfterUtc.ToLocalTime().Date}}
    $arguments=@{Property=$Property;BeforeUtcTicks=$BeforeUtc.Ticks;AfterUtcTicks=$AfterUtc.Ticks;BeforePropertyTicks=$beforeProperty.Ticks;AfterPropertyTicks=$afterProperty.Ticks
        BeforeOffsetTicks=[TimeZoneInfo]::Local.GetUtcOffset($BeforeUtc).Ticks;AfterOffsetTicks=[TimeZoneInfo]::Local.GetUtcOffset($AfterUtc).Ticks
        Ticks=$Candidate.Ticks;Kind=$Candidate.Kind.ToString();DateTicks=$Candidate.Date.Ticks;TimeTicks=$Candidate.TimeOfDay.Ticks;UtcTicks=$Candidate.ToUniversalTime().Ticks}
    $result=Test-SelectedClockEnvelope @arguments
    if($result.status -ne $ExpectedStatus){throw "Designed clock envelope case failed: $Name; $($result.reason)"}
    $legacyAccepted=$Candidate.Ticks -ge [Math]::Min($beforeProperty.Ticks,$afterProperty.Ticks) -and $Candidate.Ticks -le [Math]::Max($beforeProperty.Ticks,$afterProperty.Ticks)
    $rows.Add([ordered]@{name=$Name;inputs=$arguments;expectedStatus=$ExpectedStatus;actualStatus=$result.status;legacyCalendarEnvelopeAccepted=$legacyAccepted;passed=$true})
}
$stable=[DateTime]::new(2024,10,27,0,15,0,[DateTimeKind]::Utc)
Add-EnvelopeCase 'stable-utc' $stable $stable.AddSeconds(2) $stable.AddSeconds(1) 'Pass' 'UtcNow'
Add-EnvelopeCase 'stable-local' $stable $stable.AddSeconds(2) $stable.AddSeconds(1).ToLocalTime() 'Pass'
$fall=[DateTime]::new(2024,10,27,0,59,59,[DateTimeKind]::Utc).AddMilliseconds(900)
Add-EnvelopeCase 'fold-before-transition' $fall $fall.AddMilliseconds(200) $fall.AddMilliseconds(50).ToLocalTime() 'Pass'
Add-EnvelopeCase 'fold-after-transition' $fall $fall.AddMilliseconds(200) $fall.AddMilliseconds(150).ToLocalTime() 'Pass'
$spring=[DateTime]::new(2024,3,31,0,59,59,[DateTimeKind]::Utc).AddMilliseconds(900)
Add-EnvelopeCase 'gap-before-transition' $spring $spring.AddMilliseconds(200) $spring.AddMilliseconds(50).ToLocalTime() 'Pass'
Add-EnvelopeCase 'gap-after-transition' $spring $spring.AddMilliseconds(200) $spring.AddMilliseconds(150).ToLocalTime() 'Pass'
$lost=[DateTime]::SpecifyKind($stable.AddSeconds(1).ToLocalTime(),[DateTimeKind]::Local)
Add-EnvelopeCase 'lost-overlap-state' $stable $stable.AddSeconds(2) $lost 'Fail'
Add-EnvelopeCase 'wrong-kind' $stable $stable.AddSeconds(2) $stable.AddSeconds(1) 'Fail'
Add-EnvelopeCase 'outside-utc-frame' $stable $stable.AddSeconds(2) $stable.AddSeconds(3).ToLocalTime() 'Fail'
$gapLiteral=[DateTime]::new(2024,3,31,2,30,0,[DateTimeKind]::Local)
Add-EnvelopeCase 'nonexistent-local-gap' $spring $spring.AddMilliseconds(200) $gapLiteral 'Fail'
$midnight=[DateTime]::new(2024,10,26,21,59,59,[DateTimeKind]::Utc).AddMilliseconds(900)
Add-EnvelopeCase 'today-before-midnight' $midnight $midnight.AddMilliseconds(200) $midnight.ToLocalTime().Date 'Pass' 'Today'
Add-EnvelopeCase 'today-after-midnight' $midnight $midnight.AddMilliseconds(200) $midnight.AddMilliseconds(200).ToLocalTime().Date 'Pass' 'Today'
Add-EnvelopeCase 'reversed-native-utc-frame' $stable.AddSeconds(2) $stable $stable.AddSeconds(1).ToLocalTime() 'ReferenceClockReversed'
$counterexamples=@($rows|Where-Object{$_.expectedStatus -eq 'Pass' -and !$_.legacyCalendarEnvelopeAccepted})
if($rows.Count -ne 13 -or $counterexamples.Count -ne 2){throw 'Clock envelope fixture/counterexample coverage changed.'}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    helperSha256=(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'clock-envelope-v1.ps1') -Algorithm SHA256).Hash.ToLowerInvariant()
    nativeLocalZone=[TimeZoneInfo]::Local.Id;cases=$rows;casesPassed=$rows.Count;validFoldCounterexamples=$counterexamples.Count
    qualification='DESIGNED_UTC_ENVELOPE_FIXTURE_PASS; NOT_UPSTREAM_TEST_IDS; OTHER_CLOCK_JUMPS_ZONES_PRECISION_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output 'PASS designed clock envelopes: 13 cases; two valid fold cases rejected by the old calendar-only interval'
