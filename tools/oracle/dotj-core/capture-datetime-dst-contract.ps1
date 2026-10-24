param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'DST oracle requires pinned CoreLib.'}
$zone=[TimeZoneInfo]::Local
if($zone.Id -ne 'W. Europe Standard Time'){throw 'This bounded DST reference profile requires the recorded Windows W. Europe Standard Time host zone.'}
$dates=@(@(2024,3,31),@(2024,10,27),@(2026,3,29),@(2026,10,25),@(2024,1,15),@(2024,7,15))
$rows=@();$facts=@()
foreach($date in $dates){foreach($hour in 0..3){foreach($minute in @(0,30)){
    $plain=[DateTime]::new($date[0],$date[1],$date[2],$hour,$minute,0,[DateTimeKind]::Unspecified)
    $facts+=[ordered]@{ticks=$plain.Ticks;isAmbiguous=$zone.IsAmbiguousTime($plain);isInvalid=$zone.IsInvalidTime($plain);offsetTicks=$zone.GetUtcOffset($plain).Ticks}
    foreach($kind in @([DateTimeKind]::Unspecified,[DateTimeKind]::Utc,[DateTimeKind]::Local)){
        $inputValue=[DateTime]::SpecifyKind($plain,$kind)
        foreach($route in @('direct','viaLocal')){
            $value=if($route -eq 'direct'){$inputValue}else{$inputValue.ToLocalTime()}
            foreach($operation in @('ToUniversalTime','ToLocalTime','IsDaylightSavingTime','AddTicksZeroThenUtc','AddTickThenUtc',
                'AddMonthsZeroThenUtc','AddYearsZeroThenUtc','DateThenUtc','SpecifyLocalThenUtc','SpecifyUnspecifiedThenUtc',
                'DateThen230ThenUtc','AddDayRoundTripUtc','AddMonthsRoundTripUtc','AddYearsRoundTripUtc')){
                $resultValue=switch($operation){
                    'ToUniversalTime'{$value.ToUniversalTime()}
                    'ToLocalTime'{$value.ToLocalTime()}
                    'IsDaylightSavingTime'{$value.IsDaylightSavingTime()}
                    'AddTicksZeroThenUtc'{$value.AddTicks(0).ToUniversalTime()}
                    'AddTickThenUtc'{$value.AddTicks(1).ToUniversalTime()}
                    'AddMonthsZeroThenUtc'{$value.AddMonths(0).ToUniversalTime()}
                    'AddYearsZeroThenUtc'{$value.AddYears(0).ToUniversalTime()}
                    'DateThenUtc'{$value.Date.ToUniversalTime()}
                    'SpecifyLocalThenUtc'{[DateTime]::SpecifyKind($value,[DateTimeKind]::Local).ToUniversalTime()}
                    'SpecifyUnspecifiedThenUtc'{[DateTime]::SpecifyKind($value,[DateTimeKind]::Unspecified).ToUniversalTime()}
                    'DateThen230ThenUtc'{$value.Date.AddHours(2.5).ToUniversalTime()}
                    'AddDayRoundTripUtc'{$value.AddDays(1).AddDays(-1).ToUniversalTime()}
                    'AddMonthsRoundTripUtc'{$value.AddMonths(1).AddMonths(-1).ToUniversalTime()}
                    'AddYearsRoundTripUtc'{$value.AddYears(1).AddYears(-1).ToUniversalTime()}
                }
                $result=if($resultValue -is [bool]){[ordered]@{boolean=$resultValue}}else{[ordered]@{ticks=$resultValue.Ticks;kind=$resultValue.Kind.ToString()}}
                $rows+=[ordered]@{inputTicks=$inputValue.Ticks;inputKind=$kind.ToString();route=$route;valueTicks=$value.Ticks;valueKind=$value.Kind.ToString();operation=$operation;result=$result}
            }
        }
    }
}}}
if(@($facts|Where-Object isAmbiguous).Count -eq 0 -or @($facts|Where-Object isInvalid).Count -eq 0){throw 'Selected reference corpus contains no DST gap or overlap.'}
$hash=[Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($zone.ToSerializedString()))
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=$zone.Id
    nativeZoneSerializationSha256=[Convert]::ToHexString($hash).ToLowerInvariant();javaZoneProfile='Europe/Zurich';selectedZoneFacts=$facts;cases=$rows
    qualification='SELECTED_2024_2026_W_EUROPE_ZURICH_DST_REFERENCE; OTHER_RULES_HISTORICAL_ZONES_BINARY_AND_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned modern DST reference: $($rows.Count) cases"
