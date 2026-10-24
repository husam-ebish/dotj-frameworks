param([Parameter(Mandatory)][string]$OutputPath,[Parameter(Mandatory)][string]$JarPath,[Parameter(Mandatory)][string]$ConsumerClassPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Stopwatch oracle requires pinned CoreLib.'}
if([Diagnostics.Stopwatch]::Frequency -ne 10000000 -or ![Diagnostics.Stopwatch]::IsHighResolution){throw 'Selected Stopwatch reference requires the recorded 10 MHz high-resolution native profile.'}
$flags=[Reflection.BindingFlags]'Public,Instance,Static,DeclaredOnly';$type=[Diagnostics.Stopwatch]
$methods=@();foreach($method in $type.GetMethods($flags)){
    $methods+=[ordered]@{name=$method.Name;returnType=$method.ReturnType.FullName;parameters=@($method.GetParameters()|ForEach-Object{$_.ParameterType.FullName});isStatic=$method.IsStatic;isVirtual=$method.IsVirtual}
}
$fields=@();foreach($field in $type.GetFields($flags)){$fields+=[ordered]@{name=$field.Name;type=$field.FieldType.FullName;isStatic=$field.IsStatic;isInitOnly=$field.IsInitOnly}}
$values=@([long]::MinValue,([long]::MinValue+1),[long]-10000000,[long]-10000,[long]-1,[long]0,[long]1,[long]99,[long]100,[long]9999,[long]10000,[long]10000000,([long]::MaxValue-1),[long]::MaxValue)
$arithmetic=@();foreach($start in $values){foreach($end in $values){$arithmetic+=[ordered]@{start=$start;end=$end;ticks=[Diagnostics.Stopwatch]::GetElapsedTime($start,$end).Ticks}}}
$operations=@('new','stop','reset','start','sleep:5','start','sleep:5','stop','stop','reset','restart','sleep:5','stop','start','sleep:5','stop','restart','reset','startNew','sleep:5','stop')
$nativeTrace=@();$watch=$null
foreach($operation in $operations){
    switch($operation){
        'new'{$watch=[Diagnostics.Stopwatch]::new()}
        'start'{$watch.Start()}
        'stop'{$watch.Stop()}
        'reset'{$watch.Reset()}
        'restart'{$watch.Restart()}
        'startNew'{$watch=[Diagnostics.Stopwatch]::StartNew()}
        default{[Threading.Thread]::Sleep([int]$operation.Substring(6))}
    }
    $nativeTrace+=[ordered]@{operation=$operation;running=$watch.IsRunning;elapsedZero=($watch.ElapsedTicks -eq 0);observedElapsedTicks=$watch.ElapsedTicks}
}
$java=(Get-Command java -CommandType Application -ErrorAction Stop).Source
$javaHash=(Get-FileHash -LiteralPath $java -Algorithm SHA256).Hash.ToLowerInvariant()
if($javaHash -ne '1f41cc782de7ddd8824376568f9011413d710cf225047906106d2a01a0e3f7a9'){throw 'Stopwatch consumer requires pinned Java.'}
foreach($path in @($JarPath,$ConsumerClassPath)){if([IO.Path]::GetPathRoot([IO.Path]::GetFullPath($path)) -ine 'D:\'){throw 'Stopwatch artifacts must remain on D:.'}}
$info=[Diagnostics.ProcessStartInfo]::new($java);$info.UseShellExecute=$false;$info.CreateNoWindow=$true;$info.RedirectStandardOutput=$true;$info.RedirectStandardError=$true
foreach($argument in @('-cp',($JarPath+';'+$ConsumerClassPath),'StopwatchProbe')+$operations){$info.ArgumentList.Add($argument)}
$process=[Diagnostics.Process]::new();$process.StartInfo=$info;$outer=[Diagnostics.Stopwatch]::StartNew()
try{
    if(!$process.Start()){throw 'Cannot start Stopwatch consumer.'}
    $outTask=$process.StandardOutput.ReadToEndAsync();$errTask=$process.StandardError.ReadToEndAsync()
    if(!$process.WaitForExit(30000)){$process.Kill();throw 'Stopwatch consumer timed out.'}
    $outer.Stop();$stdout=$outTask.GetAwaiter().GetResult();$stderr=$errTask.GetAwaiter().GetResult()
    if($process.ExitCode -ne 0){throw "Stopwatch consumer failed: $stderr"}
}finally{$process.Dispose()}
$output=@($stdout.Trim().Split("`n")|ForEach-Object{$_|ConvertFrom-Json});$states=@($output|Where-Object record -eq 'state');$counter=@($output|Where-Object record -eq 'counter')
if($states.Count -ne $nativeTrace.Count -or $counter.Count -ne 1){throw 'Stopwatch consumer trace is incomplete.'}
for($index=0;$index -lt $states.Count;$index++){
    $state=$states[$index];$reference=$nativeTrace[$index]
    if($state.operation -ne $reference.operation -or $state.running -ne $reference.running){throw "Stopwatch state mismatch at $index"}
    if($state.before -lt 0 -or $state.after -lt $state.before -or (!$state.running -and $state.before -ne $state.after)){throw "Stopwatch counter/freeze mismatch at $index"}
    if(!$state.running -and (($state.before -eq 0) -ne $reference.elapsedZero)){throw "Stopwatch stopped zero-state mismatch at $index"}
    $minimum=[Diagnostics.Stopwatch]::GetElapsedTime(0,[long]$state.before).Ticks;$maximum=[Diagnostics.Stopwatch]::GetElapsedTime(0,[long]$state.after).Ticks
    if($state.spanTicks -lt $minimum -or $state.spanTicks -gt $maximum -or $state.milliseconds -lt [Math]::Truncate($minimum/10000.0) -or $state.milliseconds -gt [Math]::Truncate($maximum/10000.0)){throw "Stopwatch elapsed projection mismatch at $index"}
    foreach($text in @($state.text,$state.javaText)){
        $ticks=[TimeSpan]::ParseExact([string]$text,'c',[Globalization.CultureInfo]::InvariantCulture).Ticks
        if($ticks -lt $minimum -or $ticks -gt $maximum){throw "Stopwatch text mismatch at $index"}
    }
    if($index -gt 0 -and $state.operation -eq 'start' -and $state.before -lt $states[$index-1].after){throw 'Start reset accumulated time.'}
    if($index -gt 0 -and $state.operation -eq 'stop' -and !$states[$index-1].running -and $state.before -ne $states[$index-1].after){throw 'Repeated Stop changed elapsed time.'}
}
$counter=$counter[0]
if($counter.frequency -ne [Diagnostics.Stopwatch]::Frequency -or !$counter.highResolution -or !$counter.nondecreasing -or !$counter.advanced -or !$counter.derivedReset){throw 'Stopwatch counter/profile/inheritance check failed.'}
if($counter.end -lt $counter.start -or $counter.oneArgumentTicks -lt 0 -or $counter.oneArgumentTicks -gt [Diagnostics.Stopwatch]::GetElapsedTime([long]$counter.start,[long]$counter.end).Ticks){throw 'One-argument elapsed-time envelope failed.'}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;javaSha256=$javaHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();candidateJarSha256=(Get-FileHash -LiteralPath $JarPath -Algorithm SHA256).Hash.ToLowerInvariant()
    consumerSourceSha256=(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'fixtures/StopwatchProbe.java') -Algorithm SHA256).Hash.ToLowerInvariant()
    upstreamSourceMember='src/libraries/System.Private.CoreLib/src/System/Diagnostics/Stopwatch.cs';upstreamSourceSha256='8ee76eff6d199d65064dd6e8b29e05b95722e670a8af8dd048c6d7fb84957955'
    metadata=[ordered]@{name=$type.FullName;baseType=$type.BaseType.FullName;isSealed=$type.IsSealed;constructorCount=$type.GetConstructors().Count;methods=$methods;fields=$fields}
    frequency=[Diagnostics.Stopwatch]::Frequency;isHighResolution=[Diagnostics.Stopwatch]::IsHighResolution;arithmetic=$arithmetic;nativeTrace=$nativeTrace;candidateTrace=$states;candidateCounter=$counter
    liveStateChecksPassed=$states.Count;outerNativeElapsedTicks=$outer.ElapsedTicks
    qualification='BOUNDED_100NS_MONOTONIC_PROFILE_PASS; ORIGIN_LIFETIME_RESOLUTION_SUSPEND_CONCURRENCY_REFLECTION_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned Stopwatch reference and live state checks: $($arithmetic.Count) arithmetic vectors; $($states.Count) state steps"
