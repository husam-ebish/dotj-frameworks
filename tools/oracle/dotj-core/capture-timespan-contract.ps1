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
    [ordered]@{ exception = $errorObject.GetType().FullName; paramName = $parameter; hResult = $errorObject.HResult }
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
$ratios = @()
foreach ($left in @([long]0, [long]1, [long]-1, [long]3, [long]-3, [long]::MaxValue, [long]::MinValue)) {
    foreach ($right in @([long]0, [long]1, [long]-1, [long]3, [long]-3, [long]::MaxValue, [long]::MinValue)) {
        $ratio = [TimeSpan]::FromTicks($left).Divide([TimeSpan]::FromTicks($right))
        $ratios += [ordered]@{ method = 'Divide'; ticks = $left; divisorTicks = $right
            result = [ordered]@{ bits = [BitConverter]::DoubleToInt64Bits($ratio).ToString('X16'); isNaN = [double]::IsNaN($ratio) } }
    }
}
$constructorInputs = [Collections.Generic.List[object]]::new()
foreach ($components in @(@(1,2,3), @(25,-2,61), @(1,2,3,4), @(-1,2,-3,4), @(1,2,3,4,5), @(1,2,3,4,5,6), @(2147483647,0,0), @(2147483647,0,0,0), @(10675199,2,48,5,477,580), @(10675199,2,48,5,477,581), @(-10675199,-2,-48,-5,-477,-580), @(-10675199,-2,-48,-5,-477,-581))) {
    $constructorInputs.Add([int[]]$components)
}
foreach ($length in 3..6) {
    $constructorInputs.Add([int[]]::new($length))
    foreach ($position in 0..($length-1)) {
        foreach ($value in @([int]::MinValue, -1000, -25, -1, 1, 25, 1000, [int]::MaxValue)) {
            $components = [int[]]::new($length); $components[$position] = $value
            $constructorInputs.Add($components)
        }
    }
    $constructorInputs.Add([int[]]@((1..$length) | ForEach-Object { [int]::MaxValue }))
    $constructorInputs.Add([int[]]@((1..$length) | ForEach-Object { [int]::MinValue }))
}
foreach ($components in $constructorInputs) {
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
$properties = @()
$propertyNames = @('Ticks', 'Days', 'Hours', 'Minutes', 'Seconds', 'Milliseconds', 'Microseconds', 'Nanoseconds',
    'TotalDays', 'TotalHours', 'TotalMinutes', 'TotalSeconds', 'TotalMilliseconds', 'TotalMicroseconds', 'TotalNanoseconds')
$tickInputs = @([long]::MinValue, ([long]::MinValue + 1), [long]-864000000001, [long]-10001,
    [long]-10000, [long]-9999, [long]-11, [long]-10, [long]-9, [long]-1, [long]0, [long]1,
    [long]9, [long]10, [long]11, [long]9999, [long]10000, [long]10001, [long]864000000001,
    ([long]::MaxValue - 1), [long]::MaxValue)
foreach ($ticks in $tickInputs) {
    $span = [TimeSpan]::FromTicks($ticks)
    foreach ($name in $propertyNames) {
        $value = [TimeSpan].GetProperty($name).GetValue($span)
        $result = if ($value -is [double]) {
            [ordered]@{ bits = [BitConverter]::DoubleToInt64Bits($value).ToString('X16'); isNaN = $false }
        } else { [ordered]@{ value = $value } }
        $properties += [ordered]@{ ticks = $ticks; property = $name; result = $result }
    }
}
$integerFactories = @()
$integerSpecs = @(
    @{ name = 'Days'; type = [int]; scale = [TimeSpan]::TicksPerDay },
    @{ name = 'Hours'; type = [int]; scale = [TimeSpan]::TicksPerHour },
    @{ name = 'Minutes'; type = [long]; scale = [TimeSpan]::TicksPerMinute },
    @{ name = 'Seconds'; type = [long]; scale = [TimeSpan]::TicksPerSecond },
    @{ name = 'Milliseconds'; type = [long]; scale = [TimeSpan]::TicksPerMillisecond },
    @{ name = 'Microseconds'; type = [long]; scale = [TimeSpan]::TicksPerMicrosecond })
foreach ($spec in $integerSpecs) {
    $maximum = [long][Numerics.BigInteger]::Divide(([Numerics.BigInteger]([long]::MaxValue)), ([Numerics.BigInteger]$spec.scale))
    $minimum = [long][Numerics.BigInteger]::Divide(([Numerics.BigInteger]([long]::MinValue)), ([Numerics.BigInteger]$spec.scale))
    $typeMin = if ($spec.type -eq [int]) { [int]::MinValue } else { [long]::MinValue }
    $typeMax = if ($spec.type -eq [int]) { [int]::MaxValue } else { [long]::MaxValue }
    $values = [long[]]@(0, 1, -1, 25, -25, $typeMin, $typeMax, $maximum, ($maximum-1), ($maximum+1), $minimum, ($minimum-1), ($minimum+1))
    $method = [TimeSpan].GetMethod('From' + $spec.name, [type[]]@($spec.type))
    foreach ($value in $values) {
        $boxed = if ($spec.type -eq [int]) { [int]$value } else { [long]$value }
        try { $result = [ordered]@{ ticks = $method.Invoke($null, [object[]]@($boxed)).Ticks } }
        catch { $result = Failure $_ }
        $integerFactories += [ordered]@{ method = $method.Name; inputType = $spec.type.FullName; value = $boxed; result = $result }
    }
}
$compositeFactories = @()
$compositeSpecs = @(
    @{ name = 'FromDays'; types = [type[]]@([int],[int],[long],[long],[long],[long]); scale = [TimeSpan]::MicrosecondsPerDay },
    @{ name = 'FromHours'; types = [type[]]@([int],[long],[long],[long],[long]); scale = [TimeSpan]::MicrosecondsPerHour },
    @{ name = 'FromMinutes'; types = [type[]]@([long],[long],[long],[long]); scale = [TimeSpan]::MicrosecondsPerMinute },
    @{ name = 'FromSeconds'; types = [type[]]@([long],[long],[long]); scale = [TimeSpan]::MicrosecondsPerSecond },
    @{ name = 'FromMilliseconds'; types = [type[]]@([long],[long]); scale = [TimeSpan]::MicrosecondsPerMillisecond })
$maxMicro = [long][Numerics.BigInteger]::Divide(([Numerics.BigInteger]([long]::MaxValue)), [Numerics.BigInteger]10)
$minMicro = [long][Numerics.BigInteger]::Divide(([Numerics.BigInteger]([long]::MinValue)), [Numerics.BigInteger]10)
foreach ($spec in $compositeSpecs) {
    $inputs = [Collections.Generic.List[object]]::new()
    $fullCount = $spec.types.Count
    $method = [TimeSpan].GetMethod($spec.name, $spec.types)
    foreach ($prefix in 2..$fullCount) {
        for ($index = $prefix; $index -lt $fullCount; $index++) {
            if (-not $method.GetParameters()[$index].IsOptional -or $method.GetParameters()[$index].DefaultValue -ne 0) {
                throw 'Only actual zero-valued trailing CLR defaults may be represented by prefix overloads.'
            }
        }
        foreach ($pattern in 0..3) {
            $values = [long[]]::new($prefix)
            for ($index = 0; $index -lt $prefix; $index++) {
                $values[$index] = switch ($pattern) { 0 { 0 } 1 { 1 } 2 { -1 } 3 { if ($index % 2) { -($index+1) } else { $index+1 } } }
            }
            $inputs.Add($values)
        }
        foreach ($position in 0..($prefix-1)) {
            $minimum = if ($spec.types[$position] -eq [int]) { [int]::MinValue } else { [long]::MinValue }
            $maximum = if ($spec.types[$position] -eq [int]) { [int]::MaxValue } else { [long]::MaxValue }
            foreach ($value in @($minimum, $maximum)) {
                $values = [long[]]::new($prefix); $values[$position] = $value
                $inputs.Add($values)
            }
        }
    }
    foreach ($value in @($maxMicro, ($maxMicro+1), $minMicro, ($minMicro-1))) {
        $values = [long[]]::new($fullCount); $values[$fullCount-1] = $value
        $inputs.Add($values)
    }
    foreach ($bound in @($maxMicro, $minMicro)) {
        $first = [long][Numerics.BigInteger]::Divide(([Numerics.BigInteger]$bound), ([Numerics.BigInteger]$spec.scale))
        $first += $(if ($bound -gt 0) { 1 } else { -1 })
        $correction = [long]([Numerics.BigInteger]$bound - ([Numerics.BigInteger]$first * [Numerics.BigInteger]$spec.scale))
        $values = [long[]]::new($fullCount); $values[0] = $first; $values[$fullCount-1] = $correction
        $inputs.Add($values)
    }
    foreach ($values in $inputs) {
        $arguments = [object[]]::new($fullCount)
        for ($index = 0; $index -lt $fullCount; $index++) {
            $value = if ($index -lt $values.Count) { $values[$index] } else { 0 }
            $arguments[$index] = if ($spec.types[$index] -eq [int]) { [int]$value } else { [long]$value }
        }
        try { $result = [ordered]@{ ticks = $method.Invoke($null, $arguments).Ticks } }
        catch { $result = Failure $_ }
        $compositeFactories += [ordered]@{ method = $spec.name; values = $values
            parameterTypes = @($spec.types[0..($values.Count-1)] | ForEach-Object { $_.FullName })
            declaredClrParameterCount = $fullCount; trailingDefaultsOmitted = ($values.Count -lt $fullCount); result = $result }
    }
}
$comparisons = @()
$comparisonTicks = [long[]]@([long]::MinValue, -4294967296, -3, -1, 0, 1, 3, 4294967296, [long]::MaxValue)
$objectCompare = [TimeSpan].GetMethod('CompareTo', [type[]]@([object]))
$objectEquals = [TimeSpan].GetMethod('Equals', [type[]]@([object]))
foreach ($leftTicks in $comparisonTicks) {
    $left = [TimeSpan]::FromTicks($leftTicks)
    foreach ($rightTicks in $comparisonTicks) {
        $right = [TimeSpan]::FromTicks($rightTicks)
        $comparisons += [ordered]@{ ticks = $leftTicks; rightTicks = $rightTicks
            compareStatic = [TimeSpan]::Compare($left, $right); compareTyped = $left.CompareTo($right)
            compareObject = $objectCompare.Invoke($left, [object[]]@($right))
            equalsStatic = [TimeSpan]::Equals($left, $right); equalsTyped = $left.Equals($right)
            equalsObject = $objectEquals.Invoke($left, [object[]]@($right))
            hash = $left.GetHashCode() }
    }
    foreach ($target in @(@{ kind = 'Null'; value = $null }, @{ kind = 'Int32'; value = [int]0 },
            @{ kind = 'String'; value = 'wrong' }, @{ kind = 'Object'; value = [object]::new() })) {
        foreach ($operation in @('CompareTo', 'Equals')) {
            $method = if ($operation -eq 'CompareTo') { $objectCompare } else { $objectEquals }
            try {
                $value = $method.Invoke($left, [object[]]@($target.value))
                $result = if ($operation -eq 'Equals') { [ordered]@{ boolean = $value } } else { [ordered]@{ value = $value } }
            } catch { $result = Failure $_ }
            $comparisons += [ordered]@{ ticks = $leftTicks; objectKind = $target.kind; operation = $operation; result = $result }
        }
    }
}
$checkedArithmetic = @()
$checkedTicks = [long[]]@([long]::MinValue, ([long]::MinValue+1), -4294967296, -3, -1, 0, 1, 3, 4294967296, ([long]::MaxValue-1), [long]::MaxValue)
foreach ($leftTicks in $checkedTicks) {
    $left = [TimeSpan]::FromTicks($leftTicks)
    foreach ($rightTicks in $checkedTicks) {
        $right = [TimeSpan]::FromTicks($rightTicks)
        foreach ($name in @('Add', 'Subtract')) {
            try {
                $value = if ($name -eq 'Add') { $left.Add($right) } else { $left.Subtract($right) }
                $result = [ordered]@{ ticks = $value.Ticks }
            } catch { $result = Failure $_ }
            $checkedArithmetic += [ordered]@{ method = $name; ticks = $leftTicks; operandTicks = $rightTicks; result = $result }
        }
    }
    foreach ($name in @('Duration', 'Negate')) {
        try {
            $value = if ($name -eq 'Duration') { $left.Duration() } else { $left.Negate() }
            $result = [ordered]@{ ticks = $value.Ticks }
        } catch { $result = Failure $_ }
        $checkedArithmetic += [ordered]@{ method = $name; ticks = $leftTicks; result = $result }
    }
}
$formats = @()
$formatOnly = [TimeSpan].GetMethod('ToString', [type[]]@([string]))
$formatWithProvider = [TimeSpan].GetMethod('ToString', [type[]]@([string],[IFormatProvider]))
foreach ($ticks in $tickInputs) {
    $span = [TimeSpan]::FromTicks($ticks)
    foreach ($format in @($null, '', 'c', 't', 'T', 'C', 'z', 'cc', 'ddddddddd', ':')) {
        try { $result = [ordered]@{ text = $formatOnly.Invoke($span, [object[]]@($format)) } }
        catch { $result = Failure $_ }
        $formats += [ordered]@{ ticks = $ticks; format = $format; withProvider = $false; referenceCulture = $null; result = $result }
        foreach ($culture in @([Globalization.CultureInfo]::InvariantCulture, [Globalization.CultureInfo]::GetCultureInfo('fr-FR'))) {
            try { $result = [ordered]@{ text = $formatWithProvider.Invoke($span, [object[]]@($format,$culture)) } }
            catch { $result = Failure $_ }
            $formats += [ordered]@{ ticks = $ticks; format = $format; withProvider = $true; referenceCulture = $culture.Name; result = $result }
        }
    }
}
$customFormats = @()
$patterns = @('dd', 'dddddddd', 'hh', 'mm', 'ss', 'ff', 'fffffff', 'FF', 'FFFFFFF',
    '%d', '%h', '%m', '%s', '%f', '%F', 'd\.hh\:mm\:ss\.fffffff',
    'hh\:mm\:ss\.FFFFFFF', "'literal'", '"quoted"', "'a\'b'", '\-', "''", '""',
    'hhh', 'mmm', 'sss', 'ffffffff', 'FFFFFFFF', 'ddddddddd', 'h:m', 'ss.',
    '%', '%%', '%z', '%\', '\', "'unclosed", '"unclosed', "'escape\", '%''', '%"')
foreach ($ticks in $tickInputs) {
    $span = [TimeSpan]::FromTicks($ticks)
    foreach ($format in $patterns) {
        try { $result = [ordered]@{ text = $formatWithProvider.Invoke($span, [object[]]@($format,$null)) } }
        catch { $result = Failure $_ }
        $customFormats += [ordered]@{ ticks = $ticks; format = $format; result = $result }
    }
}
$parseInputs = [Collections.Generic.List[object]]::new()
foreach ($text in @($null, '', '-', '+0', 'garbage', '12/12/12', '00:', '00:00:-01',
    '00:00::00', '00:00:00:', '00:00:00:00:00:00', '00:61:00', '1.2', '1:2.3',
    '1:1:1.99999999', '1:1:1.09999999', '1:1:1.00000004', '1:1:1.00000005',
    '1:1:1.00000000000001', '1:1:1.00000000000000', '1:1:1.0123456789',
    '10675199.02:48:05.4775807', '10675199.02:48:05.4775808', '-10675199.02:48:05.4775808',
    '-10675199.02:48:05.4775809', '0000000000000000000000000', '1:1:1.000000000000000000000000001',
    '١:٢:٣', '１:２:３', '1 :2:3', '1:2:3 ', ("`0" + '12:34:56'))) { $parseInputs.Add($text) }
foreach ($first in @('0','1','23','24','59','60','10675199','10675200','2147483647','2147483648')) {
    foreach ($text in @($first, "${first}:02", "${first}:02:03", "${first}.02:03", "${first}:02:03:04",
        "${first}.02:03:04", "${first}:02:03.4", "${first}:02:.04", "${first}.02:03:.004",
        "${first}:02:03:04.0000005", "${first}.02:03:04.0000005")) {
        $parseInputs.Add($text); $parseInputs.Add('-' + $text)
    }
}
foreach ($code in @(9,10,11,12,13,28,31,32,133,160,5760,8192,8232,8233,8239,8287,12288,65279)) {
    $parseInputs.Add([string][char]$code + '1:2:3' + [char]$code)
}
foreach ($fraction in @('0','1','0000000','00000000','9999999','99999999','00000001','00000005','099999999','01234567890','000000002147483648')) {
    $parseInputs.Add('00:00:00.' + $fraction)
}
$parsing = @()
$savedCulture = [Globalization.CultureInfo]::CurrentCulture
try {
    [Globalization.CultureInfo]::CurrentCulture = [Globalization.CultureInfo]::InvariantCulture
    $parseMethod = [TimeSpan].GetMethod('Parse', [type[]]@([string]))
    foreach ($text in $parseInputs) {
        try { $result = [ordered]@{ ticks = $parseMethod.Invoke($null, [object[]]@($text)).Ticks } }
        catch { $result = Failure $_ }
        $outValue = [TimeSpan]::FromTicks(99)
        $success = [TimeSpan]::TryParse([string]$text, [ref]$outValue)
        $parsing += [ordered]@{ input = $text; result = $result; trySuccess = $success; tryTicks = $outValue.Ticks }
    }
} finally { [Globalization.CultureInfo]::CurrentCulture = $savedCulture }
$record = [ordered]@{
    schemaVersion = 1; scope = 'Pinned TimeSpan metadata, numeric and component boundary vectors; bounded oracle only'
    runtimeVersion = [Environment]::Version.ToString(); coreLibSha256 = $coreHash
    oracleSha256 = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    metadata = $metadata; factories = $factories; constructors = $constructors; operations = $operations; ratios = $ratios; properties = $properties
    constants = @([TimeSpan].GetFields([Reflection.BindingFlags]'Public,Static') | ForEach-Object {
        $value = $_.GetValue($null)
        [ordered]@{ name = $_.Name; type = $_.FieldType.FullName
            result = $(if ($value -is [TimeSpan]) { [ordered]@{ ticks = $value.Ticks } } else { [ordered]@{ value = $value } }) }
    })
    defaultValueTicks = [Activator]::CreateInstance([TimeSpan]).Ticks
    integerFactories = $integerFactories
    compositeFactories = $compositeFactories
    comparisons = $comparisons
    checkedArithmetic = $checkedArithmetic
    formats = $formats
    customFormats = $customFormats
    parsing = $parsing
    qualification = 'REFERENCE_EVIDENCE_ONLY; NO_JAVA_OR_PUBLIC_QUALIFICATION'
}
[IO.File]::WriteAllText($OutputPath, ($record | ConvertTo-Json -Depth 12) + "`n", [Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned TimeSpan oracle: $($factories.Count) floating factories, $($integerFactories.Count) integer factories, $($constructors.Count) constructors, $($operations.Count) scaling, $($ratios.Count) ratios and $($properties.Count) properties"
