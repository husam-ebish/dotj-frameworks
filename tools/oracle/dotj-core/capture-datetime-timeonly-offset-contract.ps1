param([Parameter(Mandatory)][string]$OutputPath,[Parameter(Mandatory)][string]$JarPath,[Parameter(Mandatory)][string]$ConsumerClassPath)
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
function New-DateTimeBufferFormatter([type]$ElementType) {
    $arrayType = $ElementType.MakeArrayType()
    $spanDefinition = [type]'System.Span`1'
    $spanType = $spanDefinition.MakeGenericType($ElementType)
    $bridge = [Reflection.Emit.DynamicMethod]::new('DateTimeBufferTryFormat',[bool],
        [type[]]@([DateTime],$arrayType,[int[]],[string],[IFormatProvider]))
    $il = $bridge.GetILGenerator()
    $target = [DateTime].GetMethod('TryFormat',[type[]]@($spanType,[int].MakeByRefType(),[type]'System.ReadOnlySpan[char]',[IFormatProvider]))
    $il.Emit([Reflection.Emit.OpCodes]::Ldarga_S,[byte]0)
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_1)
    $il.Emit([Reflection.Emit.OpCodes]::Call,$spanType.GetMethod('op_Implicit',[type[]]@($arrayType)))
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_2)
    $il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0)
    $il.Emit([Reflection.Emit.OpCodes]::Ldelema,[int])
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_3)
    $il.Emit([Reflection.Emit.OpCodes]::Call,[MemoryExtensions].GetMethod('AsSpan',[type[]]@([string])))
    $il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4)
    $il.Emit([Reflection.Emit.OpCodes]::Call,$target)
    $il.Emit([Reflection.Emit.OpCodes]::Ret)
    $delegateDefinition = [type]'System.Func`6'
    $delegateType = $delegateDefinition.MakeGenericType([type[]]@([DateTime],$arrayType,[int[]],[string],[IFormatProvider],[bool]))
    return $bridge.CreateDelegate($delegateType)
}
$charFormatter=New-DateTimeBufferFormatter ([char]);$byteFormatter=New-DateTimeBufferFormatter ([byte])
if([TimeZoneInfo]::Local.Id -ne 'W. Europe Standard Time'){throw 'Time-only offset probe requires selected native timezone.'}
$java=(Get-Command java -ErrorAction Stop).Source
$javaHash=(Get-FileHash -LiteralPath $java -Algorithm SHA256).Hash.ToLowerInvariant()
if($javaHash -ne '1f41cc782de7ddd8824376568f9011413d710cf225047906106d2a01a0e3f7a9'){throw 'Time-only probe requires pinned JDK executable.'}
$work='D:\AI\Implementation\dotj Frameworks\verification\datetime-timeonly-offset'
[IO.Directory]::CreateDirectory($work)|Out-Null
$provider=[Globalization.CultureInfo]::InvariantCulture
function NativeState($request){
 $value=[DateTime]::new([long]$request.ticks,[Enum]::Parse([DateTimeKind],$request.kind));$format=$request.format
 $state=[ordered]@{provider=$value.ToString($format,$provider);single=$value.ToString($format);interface=([IFormattable].GetMethod('ToString').Invoke($value,[object[]]@($format,$provider)))}
 $buffer=[char[]]('#'*64);$written=[int[]]@(99);$success=$charFormatter.Invoke($value,$buffer,$written,$format,$provider)
 $state.Char=$success.ToString().ToLowerInvariant()+'|'+$written[0]+'|'+[string]::new($buffer)
 $buffer=[byte[]]::new(64);[Array]::Fill($buffer,[byte]35);$written=[int[]]@(99);$success=$byteFormatter.Invoke($value,$buffer,$written,$format,$provider)
 $state.Utf8=$success.ToString().ToLowerInvariant()+'|'+$written[0]+'|'+[Convert]::ToHexString($buffer)
 return $state
}
$formats=@('%z','zz','zzz','zzzz','z yyyy','yyyy z','%z yyyy','yyyy %z',"'x' z","yyyy 'z' z",'dd z','MM z','K z','z K','hh:mm:ss z','hh:mm:ss zzz','yyyy-MM-dd HH:mm:ss zzz')
$dateFirst=@('yyyy z',"yyyy 'z' z",'dd z','MM z','yyyy-MM-dd HH:mm:ss zzz')
$requests=@();foreach($ticks in [long[]]@(0,1,863999999999)){foreach($kind in @('Unspecified','Utc','Local')){foreach($format in $formats){
 if($kind -ne 'Utc' -and $format -cin $dateFirst){continue};if($kind -eq 'Local' -and $format.Contains('K')){continue}
 $requests+=@{id=$requests.Count;ticks=$ticks.ToString();kind=$kind;format=$format}
}}}
if($requests.Count -ne 117){throw 'Unexpected live time-only corpus.'}
$inputPath=Join-Path $work 'input.tsv';$lines=@(foreach($request in $requests){$request.id.ToString()+"`t"+$request.ticks+"`t"+$request.kind+"`t"+[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($request.format))})
[IO.File]::WriteAllLines($inputPath,[string[]]$lines,[Text.UTF8Encoding]::new($false))
$rows=@();$frames=@();$culture=[Globalization.CultureInfo]::CurrentCulture
try{
 [Globalization.CultureInfo]::CurrentCulture=$provider
 foreach($sample in 0..3){
  $timer=[Diagnostics.Stopwatch]::StartNew();$beforeTicks=[DateTime]::UtcNow.Ticks;$before=@(foreach($request in $requests){NativeState $request})
  $outputFile=Join-Path $work "output-$sample.tsv"
  $start=[Diagnostics.ProcessStartInfo]::new($java);$start.UseShellExecute=$false;$start.RedirectStandardOutput=$true;$start.RedirectStandardError=$true;$start.CreateNoWindow=$true
  foreach($argument in @('-Duser.timezone=Europe/Zurich','-cp',($JarPath+';'+$ConsumerClassPath),'TimeOnlyOffsetProbe',$inputPath,$outputFile)){$start.ArgumentList.Add($argument)}
  $process=[Diagnostics.Process]::Start($start);$stdout=$process.StandardOutput.ReadToEndAsync();$stderr=$process.StandardError.ReadToEndAsync()
  if(!$process.WaitForExit(10000)){$process.Kill($true);throw 'Time-only consumer exceeded monotonic deadline.'}
  [IO.File]::WriteAllText((Join-Path $work "java-$sample.log"),($stdout.GetAwaiter().GetResult()+$stderr.GetAwaiter().GetResult()))
  if($process.ExitCode -ne 0){throw 'Time-only consumer failed; see D: log.'}
  $after=@(foreach($request in $requests){NativeState $request});$afterTicks=[DateTime]::UtcNow.Ticks;$timer.Stop()
  if($afterTicks -lt $beforeTicks -or $timer.ElapsedMilliseconds -gt 10000){throw 'Invalid paired clock frame.'}
  $actual=@{};$output=[IO.File]::ReadAllLines($outputFile);if($output[0] -cne "ZONE`tEurope/Zurich"){throw 'Unexpected Java zone.'}
  foreach($line in $output[1..($output.Count-1)]){$parts=$line.Split("`t");if($parts.Length -ne 3){throw 'Malformed Java consumer line.'};if(!$actual.ContainsKey($parts[0])){$actual[$parts[0]]=@{}};if($actual[$parts[0]].ContainsKey($parts[1])){throw 'Duplicate Java output.'};$actual[$parts[0]][$parts[1]]=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($parts[2]))}
  if($actual.Count -ne $requests.Count){throw 'Missing Java results.'}
  foreach($request in $requests){$value=$actual[[string]$request.id];if($value.Count -ne 5){throw 'Missing Java route.'};$rows+=[ordered]@{sample=$sample;id=$request.id;inputTicks=$request.ticks;kind=$request.kind;format=$request.format;before=$before[$request.id];after=$after[$request.id];actual=$value}}
  $frames+=[ordered]@{sample=$sample;beforeUtcTicks=$beforeTicks.ToString();afterUtcTicks=$afterTicks.ToString();elapsedMilliseconds=$timer.ElapsedMilliseconds;consumerExitCode=$process.ExitCode};$process.Dispose()
 }
}finally{[Globalization.CultureInfo]::CurrentCulture=$culture}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();consumerSourceSha256=(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'fixtures/TimeOnlyOffsetProbe.java') -Algorithm SHA256).Hash.ToLowerInvariant();candidateJarSha256=(Get-FileHash -LiteralPath $JarPath -Algorithm SHA256).Hash.ToLowerInvariant();javaExecutableSha256=$javaHash;nativeLocalZone=[TimeZoneInfo]::Local.Id;javaZoneProfile='Europe/Zurich';frames=$frames;cases=$rows;qualification='PAIRED_MODERN_HOST_OFFSET_TIMEONLY_PROFILE; HISTORICAL_OTHER_ZONES_CLOCK_CHANGES_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 18)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned live time-only offsets: $($rows.Count) paired cases; five routes each"
