param([Parameter(Mandatory)][string]$OutputPath,
      [Parameter(Mandatory)][string]$JarPath,
      [Parameter(Mandatory)][string]$ConsumerClassPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Clock oracle requires pinned CoreLib.'}
$java=(Get-Command java -CommandType Application -ErrorAction Stop).Source
$javaHash=(Get-FileHash -LiteralPath $java -Algorithm SHA256).Hash.ToLowerInvariant()
if($javaHash -ne '1f41cc782de7ddd8824376568f9011413d710cf225047906106d2a01a0e3f7a9'){throw 'Clock oracle requires the pinned Java executable.'}
foreach($path in @($JarPath,$ConsumerClassPath)){
    if([IO.Path]::GetPathRoot([IO.Path]::GetFullPath($path)) -ine 'D:\'){throw 'Clock artifact and consumer builds must remain on D:.'}
}
. (Join-Path $PSScriptRoot 'clock-envelope-v1.ps1')
$rows=@();$inconclusive=@()
foreach($name in @('UtcNow','Now','Today')){
    $property=[DateTime].GetProperty($name)
    if($null -eq $property -or !$property.GetGetMethod().IsStatic){throw 'Expected native static DateTime clock property is missing.'}
    $iteration=0;$attempt=0
    while($iteration -lt 8 -and $attempt -lt 16){
        $attempt++
        $info=[Diagnostics.ProcessStartInfo]::new($java)
        $info.UseShellExecute=$false;$info.CreateNoWindow=$true;$info.RedirectStandardOutput=$true;$info.RedirectStandardError=$true
        foreach($argument in @('-cp',($JarPath+';'+$ConsumerClassPath),'WallClockProbe',$name)){$info.ArgumentList.Add($argument)}
        $process=[Diagnostics.Process]::new();$process.StartInfo=$info
        try{
            $beforeUtc=[DateTime]::UtcNow
            $before=$property.GetValue($null)
            if(!$process.Start()){throw 'Cannot start independent clock consumer.'}
            $stdoutTask=$process.StandardOutput.ReadToEndAsync();$stderrTask=$process.StandardError.ReadToEndAsync()
            if(!$process.WaitForExit(30000)){$process.Kill();throw 'Clock consumer timed out.'}
            $after=$property.GetValue($null)
            $afterUtc=[DateTime]::UtcNow
            $stdout=$stdoutTask.GetAwaiter().GetResult().Trim();$stderr=$stderrTask.GetAwaiter().GetResult()
            if($process.ExitCode -ne 0){throw "Clock consumer failed: $stderr"}
            $parts=$stdout.Split('|');if($parts.Length -ne 6){throw "Unexpected clock consumer output: $stdout"}
            $ticks=[long]::Parse($parts[0],[Globalization.CultureInfo]::InvariantCulture)
            $date=[long]::Parse($parts[2],[Globalization.CultureInfo]::InvariantCulture)
            $time=[long]::Parse($parts[3],[Globalization.CultureInfo]::InvariantCulture)
            $utc=[long]::Parse($parts[4],[Globalization.CultureInfo]::InvariantCulture)
            $beforeOffset=[TimeZoneInfo]::Local.GetUtcOffset($beforeUtc).Ticks
            $afterOffset=[TimeZoneInfo]::Local.GetUtcOffset($afterUtc).Ticks
            $arguments=@{Property=$name;BeforeUtcTicks=$beforeUtc.Ticks;AfterUtcTicks=$afterUtc.Ticks;BeforePropertyTicks=$before.Ticks;AfterPropertyTicks=$after.Ticks
                BeforeOffsetTicks=$beforeOffset;AfterOffsetTicks=$afterOffset;Ticks=$ticks;Kind=$parts[1];DateTicks=$date;TimeTicks=$time;UtcTicks=$utc}
            $result=Test-SelectedClockEnvelope @arguments
            if($result.status -eq 'ReferenceClockReversed'){
                $inconclusive+=[ordered]@{property=$name;attempt=$attempt;referenceBeforeUtcTicks=$beforeUtc.Ticks;referenceAfterUtcTicks=$afterUtc.Ticks;reason=$result.reason}
                continue
            }
            if($result.status -ne 'Pass'){throw "$name clock check failed: $($result.reason) Native zone: $([TimeZoneInfo]::Local.Id); Java zone: $($parts[5])"}
            $iteration++
            $rows+=[ordered]@{property=$name;iteration=$iteration;attempt=$attempt;referenceBeforeTicks=$before.Ticks;referenceAfterTicks=$after.Ticks
                referenceBeforeUtcTicks=$beforeUtc.Ticks;referenceAfterUtcTicks=$afterUtc.Ticks;referenceBeforeOffsetTicks=$beforeOffset;referenceAfterOffsetTicks=$afterOffset
                referenceLocalClockReversed=($after.Ticks -lt $before.Ticks);ticks=$ticks;kind=$parts[1];dateTicks=$date;timeOfDayTicks=$time;normalizedUtcTicks=$utc;javaZone=$parts[5];passed=$true}
        }finally{$process.Dispose()}
    }
    if($iteration -ne 8){throw "Insufficient trustworthy native UTC clock frames for $name after 16 attempts."}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;javaSha256=$javaHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    helperSha256=(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'clock-envelope-v1.ps1') -Algorithm SHA256).Hash.ToLowerInvariant()
    consumerSourceSha256=(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'fixtures/WallClockProbe.java') -Algorithm SHA256).Hash.ToLowerInvariant()
    consumerClassSha256=(Get-FileHash -LiteralPath (Join-Path $ConsumerClassPath 'WallClockProbe.class') -Algorithm SHA256).Hash.ToLowerInvariant()
    candidateJarSha256=(Get-FileHash -LiteralPath $JarPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=[TimeZoneInfo]::Local.Id
    cases=$rows;casesPassed=$rows.Count;inconclusiveReferenceFrames=$inconclusive
    qualification='BOUNDED_HOST_UTC_NORMALIZED_WALL_CLOCK_ENVELOPE_PASS; NOT_MONOTONIC; OTHER_CLOCK_JUMPS_ZONES_PRECISION_AND_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS paired DateTime wall clocks: $($rows.Count) host samples"
