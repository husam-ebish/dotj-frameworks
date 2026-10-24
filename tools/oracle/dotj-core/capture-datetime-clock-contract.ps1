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
$rows=@()
foreach($name in @('UtcNow','Now','Today')){
    $property=[DateTime].GetProperty($name)
    if($null -eq $property -or !$property.GetGetMethod().IsStatic){throw 'Expected native static DateTime clock property is missing.'}
    foreach($iteration in 1..8){
        $info=[Diagnostics.ProcessStartInfo]::new($java)
        $info.UseShellExecute=$false;$info.CreateNoWindow=$true;$info.RedirectStandardOutput=$true;$info.RedirectStandardError=$true
        foreach($argument in @('-cp',($JarPath+';'+$ConsumerClassPath),'WallClockProbe',$name)){$info.ArgumentList.Add($argument)}
        $process=[Diagnostics.Process]::new();$process.StartInfo=$info
        try{
            $before=$property.GetValue($null)
            if(!$process.Start()){throw 'Cannot start independent clock consumer.'}
            $stdoutTask=$process.StandardOutput.ReadToEndAsync();$stderrTask=$process.StandardError.ReadToEndAsync()
            if(!$process.WaitForExit(30000)){$process.Kill();throw 'Clock consumer timed out.'}
            $after=$property.GetValue($null)
            $stdout=$stdoutTask.GetAwaiter().GetResult().Trim();$stderr=$stderrTask.GetAwaiter().GetResult()
            if($process.ExitCode -ne 0){throw "Clock consumer failed: $stderr"}
            $parts=$stdout.Split('|');if($parts.Length -ne 5){throw "Unexpected clock consumer output: $stdout"}
            $ticks=[long]::Parse($parts[0],[Globalization.CultureInfo]::InvariantCulture)
            $date=[long]::Parse($parts[2],[Globalization.CultureInfo]::InvariantCulture)
            $time=[long]::Parse($parts[3],[Globalization.CultureInfo]::InvariantCulture)
            if($parts[1] -ne $before.Kind.ToString() -or $parts[1] -ne $after.Kind.ToString()){throw "Clock Kind mismatch for $name"}
            if($name -eq 'Today'){
                if(($ticks -ne $before.Ticks -and $ticks -ne $after.Ticks) -or $time -ne 0){throw 'Today differs from both native midnight boundaries.'}
            }elseif($ticks -lt [Math]::Min($before.Ticks,$after.Ticks) -or $ticks -gt [Math]::Max($before.Ticks,$after.Ticks)){
                throw "$name is outside the paired native wall-clock envelope. Native zone: $([TimeZoneInfo]::Local.Id); Java zone: $($parts[4])"
            }
            if($ticks -lt 0 -or $ticks -gt [DateTime]::MaxValue.Ticks -or $time -lt 0 -or $time -ge 864000000000 -or $date+$time -ne $ticks -or $date%864000000000 -ne 0){throw 'Clock value/date/time decomposition is invalid.'}
            $rows+=[ordered]@{property=$name;iteration=$iteration;referenceBeforeTicks=$before.Ticks;referenceAfterTicks=$after.Ticks
                referenceClockReversed=($after.Ticks -lt $before.Ticks);ticks=$ticks;kind=$parts[1];dateTicks=$date;timeOfDayTicks=$time;javaZone=$parts[4];passed=$true}
        }finally{$process.Dispose()}
    }
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;javaSha256=$javaHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    consumerSourceSha256=(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'fixtures/WallClockProbe.java') -Algorithm SHA256).Hash.ToLowerInvariant()
    consumerClassSha256=(Get-FileHash -LiteralPath (Join-Path $ConsumerClassPath 'WallClockProbe.class') -Algorithm SHA256).Hash.ToLowerInvariant()
    candidateJarSha256=(Get-FileHash -LiteralPath $JarPath -Algorithm SHA256).Hash.ToLowerInvariant();nativeLocalZone=[TimeZoneInfo]::Local.Id
    cases=$rows;casesPassed=$rows.Count;qualification='BOUNDED_HOST_WALL_CLOCK_ENVELOPE_PASS; NOT_MONOTONIC; DST_AMBIGUITY_PRECISION_OTHER_HOSTS_AND_LANGUAGE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS paired DateTime wall clocks: $($rows.Count) host samples"
