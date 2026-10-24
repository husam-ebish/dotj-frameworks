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
            foreach($operation in @('ToBinary','BinaryRoundTrip','BinaryRoundTripUtc','BinaryImportedThenDaylight',
                'BinaryImportedThenAddTickUtc','BinaryImportedDateThen230Utc','BinaryImportedSpecifyLocalUtc','BinaryWithLocalAmbiguousFlag')){
                $encoded=$value.ToBinary()
                $resultValue=switch($operation){
                    'ToBinary'{$encoded}
                    'BinaryRoundTrip'{[DateTime]::FromBinary($encoded)}
                    'BinaryRoundTripUtc'{[DateTime]::FromBinary($encoded).ToUniversalTime()}
                    'BinaryImportedThenDaylight'{[DateTime]::FromBinary($encoded).IsDaylightSavingTime()}
                    'BinaryImportedThenAddTickUtc'{[DateTime]::FromBinary($encoded).AddTicks(1).ToUniversalTime()}
                    'BinaryImportedDateThen230Utc'{[DateTime]::FromBinary($encoded).Date.AddHours(2.5).ToUniversalTime()}
                    'BinaryImportedSpecifyLocalUtc'{[DateTime]::SpecifyKind([DateTime]::FromBinary($encoded),[DateTimeKind]::Local).ToUniversalTime()}
                    'BinaryWithLocalAmbiguousFlag'{if($value.Kind -eq [DateTimeKind]::Local){[DateTime]::FromBinary($encoded -bor 4611686018427387904)}else{[DateTime]::FromBinary($encoded)}}
                }
                $result=if($resultValue -is [bool]){[ordered]@{boolean=$resultValue}}elseif($resultValue -is [DateTime]){[ordered]@{ticks=$resultValue.Ticks;kind=$resultValue.Kind.ToString()}}else{[ordered]@{integer=$resultValue}}
                $rows+=[ordered]@{inputTicks=$inputValue.Ticks;inputKind=$kind.ToString();route=$route;valueTicks=$value.Ticks;valueKind=$value.Kind.ToString();operation=$operation;result=$result}
            }
        }
    }
}}}
if(@($facts|Where-Object isAmbiguous).Count -eq 0 -or @($facts|Where-Object isInvalid).Count -eq 0){throw 'Selected reference corpus contains no DST gap or overlap.'}
$hash=[Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($zone.ToSerializedString()))
$utcFlag=[long]4611686018427387904;$localFlag=[long]::MinValue
$binaryInputs=@([long]0,[long]1,[long]863999999999,[long]621355968000000000,[long]3155378975999999999,
    ($utcFlag -bor 0),($utcFlag -bor 1),($utcFlag -bor 863999999999),($utcFlag -bor 621355968000000000),($utcFlag -bor 3155378975999999999),
    [long]3155378976000000000,($utcFlag -bor 3155378976000000000),[long]::MaxValue,
    [long]-1,$localFlag,($localFlag -bor 638655858000000000),($localFlag -bor $utcFlag -bor 638655858000000000),
    ($localFlag -bor ($utcFlag-1728000000000)))
$binaryScalars=@()
foreach($data in $binaryInputs){
    $comparison=if($data -eq -1 -or $data -eq $localFlag){'classificationAndNormalizationOnly'}else{'exact'}
    try{$decoded=[DateTime]::FromBinary($data);$result=[ordered]@{ticks=$decoded.Ticks;kind=$decoded.Kind.ToString();normalizedBinary=$decoded.ToBinary()}}
    catch{$e=$_.Exception.GetBaseException();$result=[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
    $binaryScalars+=[ordered]@{dateData=$data;comparison=$comparison;result=$result}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=$zone.Id
    nativeZoneSerializationSha256=[Convert]::ToHexString($hash).ToLowerInvariant();javaZoneProfile='Europe/Zurich';selectedZoneFacts=$facts;cases=$rows;binaryScalars=$binaryScalars
    binaryScalarComparisonPolicy='Two historical local encodings check validity and normalized binary only; exact historical local tick parity remains open.'
    qualification='SELECTED_2024_2026_W_EUROPE_ZURICH_BINARY_REFERENCE; HISTORICAL_LOCAL_TICK_PARITY_OTHER_ZONES_FULL_EXTREMA_AND_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned modern binary reference: $($rows.Count) cases"
