param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$assembly = [object].Assembly.Location
$coreHash = (Get-FileHash -LiteralPath $assembly -Algorithm SHA256).Hash.ToLowerInvariant()
if ([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678') {
    throw 'Oracle requires the pinned .NET 10.0.12 CoreLib, not a bundled PowerShell runtime.'
}
function Failure($ErrorRecord) {
    $errorObject = $ErrorRecord.Exception.GetBaseException()
    $parameter = $null
    if ($errorObject -is [ArgumentException]) { $parameter = $errorObject.ParamName }
    [ordered]@{ exception = $errorObject.GetType().FullName; paramName = $parameter }
}
$factories = @()
$values = @([double]0, [double]-0.0, [double]0.19, [double]-0.19, [double]0.15,
    [double]-0.15, [double]1.5, [double]-1.5, [double]::NaN,
    [double]::PositiveInfinity, [double]::NegativeInfinity, [double]9223372036854775808,
    [double]-9223372036854775808, [double]::MaxValue, [double]::MinValue)
foreach ($unit in @('Days', 'Hours', 'Minutes', 'Seconds', 'Milliseconds', 'Microseconds')) {
    $method = [TimeSpan].GetMethod('From' + $unit, [type[]]@([double]))
    $scales = @{ Days = 864000000000.0; Hours = 36000000000.0; Minutes = 600000000.0; Seconds = 10000000.0; Milliseconds = 10000.0; Microseconds = 10.0 }
    $limit = [double][long]::MaxValue / $scales[$unit]
    $boundaryValues = @($limit, [Math]::BitDecrement($limit), [Math]::BitIncrement($limit), -$limit, [Math]::BitDecrement(-$limit), [Math]::BitIncrement(-$limit))
    foreach ($value in ($values + $boundaryValues)) {
        try { $result = [ordered]@{ ticks = $method.Invoke($null, [object[]]@($value)).Ticks } }
        catch { $result = Failure $_ }
        $factories += [ordered]@{ method = $method.Name; inputBits = [BitConverter]::DoubleToInt64Bits($value).ToString('X16'); result = $result }
    }
}
$operations = @()
foreach ($ticks in @([long]0, [long]1, [long]3, [long]-3, [long]::MaxValue, [long]::MinValue)) {
    foreach ($factor in @([double]0, [double]0.5, [double]-0.5, [double]1, [double]-1, [double]2, [double]::NaN, [double]::PositiveInfinity, [double]::NegativeInfinity, [double]::MaxValue, [double]::Epsilon)) {
        foreach ($name in @('Multiply', 'Divide')) {
            $span = [TimeSpan]::FromTicks($ticks)
            try {
                if ($name -eq 'Multiply') { $result = [ordered]@{ ticks = $span.Multiply($factor).Ticks } }
                else { $result = [ordered]@{ ticks = $span.Divide($factor).Ticks } }
            } catch { $result = Failure $_ }
            $operations += [ordered]@{ method = $name; ticks = $ticks; operandBits = [BitConverter]::DoubleToInt64Bits($factor).ToString('X16'); result = $result }
        }
    }
}
$constructors = @()
foreach ($components in @(@(1,2,3), @(25,-2,61), @(1,2,3,4), @(-1,2,-3,4), @(1,2,3,4,5), @(1,2,3,4,5,6), @(2147483647,0,0), @(2147483647,0,0,0))) {
    $parameterTypes = [type[]]@($components | ForEach-Object { [int] })
    $constructor = [TimeSpan].GetConstructor($parameterTypes)
    try { $result = [ordered]@{ ticks = $constructor.Invoke([object[]]$components).Ticks } }
    catch { $result = Failure $_ }
    $constructors += [ordered]@{ components = $components; result = $result }
}
$metadata = [ordered]@{
    type = [TimeSpan].FullName
    interfaces = @([TimeSpan].GetInterfaces().FullName | Sort-Object)
    methods = @([TimeSpan].GetMethods([Reflection.BindingFlags]'Public,Static,Instance,DeclaredOnly') | ForEach-Object { $_.ToString() } | Sort-Object)
    fields = @([TimeSpan].GetFields([Reflection.BindingFlags]'Public,Static') | ForEach-Object { [ordered]@{ name = $_.Name; type = $_.FieldType.FullName; value = $_.GetValue($null).ToString() } })
}
$record = [ordered]@{
    schemaVersion = 1; scope = 'Pinned TimeSpan metadata, interval factories, constructors, Multiply and Divide vectors; bounded oracle only'
    runtimeVersion = [Environment]::Version.ToString(); coreLibSha256 = $coreHash
    oracleSha256 = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    metadata = $metadata; factories = $factories; constructors = $constructors; operations = $operations
    qualification = 'REFERENCE_EVIDENCE_ONLY; NO_JAVA_OR_PUBLIC_QUALIFICATION'
}
[IO.File]::WriteAllText($OutputPath, ($record | ConvertTo-Json -Depth 12) + "`n", [Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned TimeSpan oracle: $($factories.Count) factories, $($constructors.Count) constructors, $($operations.Count) arithmetic vectors"
