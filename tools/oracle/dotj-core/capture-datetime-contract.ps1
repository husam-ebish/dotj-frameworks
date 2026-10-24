param([Parameter(Mandatory)][string]$OutputPath)
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
$ticksList = [long[]]@(0,1,4294967296,863999999999,864000000000,638447616000000000,3155378975999999999)
$comparisons = @()
$objectCompare = [DateTime].GetMethod('CompareTo', [type[]]@([object]))
$objectEquals = [DateTime].GetMethod('Equals', [type[]]@([object]))
foreach ($ticks in $ticksList) {
    foreach ($kind in [Enum]::GetValues([DateTimeKind])) {
        $left = [DateTime]::new($ticks, $kind)
        foreach ($rightTicks in $ticksList) {
            foreach ($rightKind in [Enum]::GetValues([DateTimeKind])) {
                $right = [DateTime]::new($rightTicks, $rightKind)
                $comparisons += [ordered]@{ ticks = $ticks; kind = $kind.ToString(); rightTicks = $rightTicks; rightKind = $rightKind.ToString()
                    compareStatic = [DateTime]::Compare($left,$right); compareTyped = $left.CompareTo($right)
                    compareObject = $objectCompare.Invoke($left,[object[]]@($right))
                    equalsStatic = [DateTime]::Equals($left,$right); equalsTyped = $left.Equals($right)
                    equalsObject = $objectEquals.Invoke($left,[object[]]@($right)); hash = $left.GetHashCode() }
            }
        }
        foreach ($target in @(@{kind='Null';value=$null},@{kind='Int32';value=[int]0},@{kind='String';value='wrong'},@{kind='Object';value=[object]::new()})) {
            foreach ($operation in @('CompareTo','Equals')) {
                $method = if ($operation -eq 'CompareTo') { $objectCompare } else { $objectEquals }
                try {
                    $value = $method.Invoke($left,[object[]]@($target.value))
                    $result = if ($operation -eq 'Equals') { [ordered]@{boolean=$value} } else { [ordered]@{value=$value} }
                } catch { $result = Failure $_ }
                $comparisons += [ordered]@{ticks=$ticks;kind=$kind.ToString();objectKind=$target.kind;operation=$operation;result=$result}
            }
        }
    }
}
$tickConstructors = @()
foreach ($ticks in @([long]::MinValue,-1,0,1,4294967296,863999999999,864000000000,621355968000000000,
    3155378975999999998,3155378975999999999,3155378976000000000,[long]::MaxValue)) {
    foreach ($kind in @($null,[DateTimeKind]::Unspecified,[DateTimeKind]::Utc,[DateTimeKind]::Local)) {
        try {
            $value = if ($null -eq $kind) { [DateTime]::new([long]$ticks) } else { [DateTime]::new([long]$ticks,$kind) }
            $result = [ordered]@{ticks=$value.Ticks;kind=$value.Kind.ToString()}
        } catch { $result = Failure $_ }
        $tickConstructors += [ordered]@{ticks=[long]$ticks;kind=$(if ($null -eq $kind) {$null} else {$kind.ToString()});result=$result}
    }
}
$constants = @([DateTime].GetFields([Reflection.BindingFlags]'Public,Static') | ForEach-Object {
    $value=$_.GetValue($null)
    [ordered]@{name=$_.Name;type=$_.FieldType.FullName;ticks=$value.Ticks;kind=$value.Kind.ToString();isInitOnly=$_.IsInitOnly}
})
$componentConstructors = @()
foreach ($length in @(3,6,7,8)) {
    $inputs = [Collections.Generic.List[object]]::new()
    $seed = [int[]]@(2024,2,29,12,34,56,789,123)[0..($length-1)]
    $inputs.Add($seed.Clone())
    foreach ($date in @(@(1,1,1),@(9999,12,31),@(1900,2,28),@(1900,2,29),@(2000,2,29),@(2023,2,29))) {
        $values = $seed.Clone(); [Array]::Copy([int[]]$date,$values,3); $inputs.Add($values)
    }
    foreach ($position in 0..($length-1)) {
        foreach ($number in @([int]::MinValue,-1,0,1,23,24,59,60,999,1000,9999,10000,[int]::MaxValue)) {
            $values = $seed.Clone(); $values[$position] = $number; $inputs.Add($values)
        }
    }
    if ($length -ge 7) {
        foreach ($position in @(0,2,3,6)) {
            $values = $seed.Clone(); $values[$position] = -1; $values[6] = -1
            if ($length -eq 8) { $values[7] = -1 }
            $inputs.Add($values)
        }
    }
    foreach ($values in $inputs) {
        $kinds = if ($length -eq 3) { @($null) } else { @($null,[DateTimeKind]::Unspecified,[DateTimeKind]::Utc,[DateTimeKind]::Local) }
        foreach ($kind in $kinds) {
            $types = [Collections.Generic.List[type]]::new(); $arguments = [Collections.Generic.List[object]]::new()
            foreach ($number in $values) { $types.Add([int]); $arguments.Add([int]$number) }
            if ($null -ne $kind) { $types.Add([DateTimeKind]); $arguments.Add($kind) }
            $ctor = [DateTime].GetConstructor($types.ToArray())
            if ($null -eq $ctor) { throw 'Expected Gregorian component constructor missing from pinned CLR.' }
            try { $value = $ctor.Invoke($arguments.ToArray()); $result = [ordered]@{ticks=$value.Ticks;kind=$value.Kind.ToString()} }
            catch { $result = Failure $_ }
            $componentConstructors += [ordered]@{components=$values;kind=$(if ($null -eq $kind) {$null} else {$kind.ToString()});result=$result}
        }
    }
}
$propertyTicks = [Collections.Generic.List[long]]::new()
foreach ($ticks in $ticksList) { $propertyTicks.Add($ticks) }
foreach ($year in @(1,1900,2000,2024,9999)) {
    $start = [DateTime]::new($year,3,1)
    foreach ($day in 0..6) { $propertyTicks.Add($start.AddDays($day).AddTicks(123456789012).Ticks) }
}
$calendarProperties = @()
foreach ($ticks in $propertyTicks) {
    foreach ($kind in [Enum]::GetValues([DateTimeKind])) {
        $value = [DateTime]::new($ticks,$kind)
        $calendarProperties += [ordered]@{ticks=$ticks;kind=$kind.ToString();dayOfWeek=$value.DayOfWeek.ToString()
            dayOfWeekValue=[int]$value.DayOfWeek;dateTicks=$value.Date.Ticks;dateKind=$value.Date.Kind.ToString()
            timeOfDayTicks=$value.TimeOfDay.Ticks}
    }
}
$enums = @()
foreach ($type in @([DayOfWeek],[DateTimeKind])) {
    $enums += [ordered]@{name=$type.FullName;underlyingType=[Enum]::GetUnderlyingType($type).FullName
        names=[Enum]::GetNames($type);values=@([Enum]::GetValues($type)|ForEach-Object{[int]$_})
        queries=@((-1..8)|ForEach-Object{[ordered]@{value=$_;defined=$type.IsEnumDefined([int]$_);name=$type.GetEnumName([int]$_)}})}
}
$floatingAddition = @()
$scales = [ordered]@{AddDays=[long]864000000000;AddHours=[long]36000000000;AddMinutes=[long]600000000
    AddSeconds=[long]10000000;AddMilliseconds=[long]10000;AddMicroseconds=[long]10}
foreach ($entry in $scales.GetEnumerator()) {
    $scale = $entry.Value
    $limit = [double]([Numerics.BigInteger]::Divide([Numerics.BigInteger]::Parse('3155378975999999999'),[Numerics.BigInteger]$scale))
    $method = [DateTime].GetMethod($entry.Key,[type[]]@([double]))
    $values = @([double]0,[double]-0.0,[double]1,[double]-1,[double]0.5,[double]-0.5,[double]0.15,[double]-0.15,
        [double]1.5,[double]-1.5,[double]24.123456789,[double]-24.123456789,[double]1048576.0000001,[double]-1048576.0000001,
        [double]::NaN,[double]::PositiveInfinity,[double]::NegativeInfinity,[double]::MaxValue,[double]::MinValue,[double]::Epsilon)
    foreach ($fraction in @(0.19,0.5,0.75,1,1.5,1.9)) { $values += [double]($fraction/$scale); $values += [double](-$fraction/$scale) }
    $values += @($limit,[Math]::BitDecrement($limit),[Math]::BitIncrement($limit),-$limit,[Math]::BitDecrement(-$limit),[Math]::BitIncrement(-$limit))
    foreach ($ticks in @([long]0,[long]1,[long]621355968000000000,[long]3155378975999999998,[long]3155378975999999999)) {
        foreach ($kind in [Enum]::GetValues([DateTimeKind])) {
            $origin = [DateTime]::new($ticks,$kind)
            foreach ($number in $values) {
                try { $value = $method.Invoke($origin,[object[]]@([double]$number)); $result = [ordered]@{ticks=$value.Ticks;kind=$value.Kind.ToString()} }
                catch { $result = Failure $_ }
                $floatingAddition += [ordered]@{ticks=$ticks;kind=$kind.ToString();method=$entry.Key
                    inputBits=[BitConverter]::DoubleToInt64Bits($number).ToString('X16');result=$result}
            }
        }
    }
}
$checkedArithmetic = @()
foreach ($ticks in $ticksList) {
    foreach ($kind in [Enum]::GetValues([DateTimeKind])) {
        $origin = [DateTime]::new($ticks,$kind)
        foreach ($operand in @([long]::MinValue,([long]::MinValue+1),[long]-3155378975999999999,[long]-864000000000,[long]-1,[long]0,[long]1,[long]864000000000,[long]3155378975999999999,[long]::MaxValue)) {
            foreach ($operation in @('AddTicks','AddSpan','SubtractSpan')) {
                try {
                    $value = switch ($operation) {
                        'AddTicks' { $origin.AddTicks($operand) }
                        'AddSpan' { $origin.Add([TimeSpan]::FromTicks($operand)) }
                        'SubtractSpan' { $origin.Subtract([TimeSpan]::FromTicks($operand)) }
                    }
                    $result = [ordered]@{ticks=$value.Ticks;kind=$value.Kind.ToString()}
                } catch { $result = Failure $_ }
                $checkedArithmetic += [ordered]@{ticks=$ticks;kind=$kind.ToString();operation=$operation;operand=$operand;result=$result}
            }
        }
        foreach ($otherTicks in $ticksList) {
            foreach ($otherKind in [Enum]::GetValues([DateTimeKind])) {
                $value = $origin.Subtract([DateTime]::new($otherTicks,$otherKind))
                $checkedArithmetic += [ordered]@{ticks=$ticks;kind=$kind.ToString();operation='SubtractDate';operand=$otherTicks
                    operandKind=$otherKind.ToString();result=[ordered]@{spanTicks=$value.Ticks}}
            }
        }
    }
}
foreach ($date in @(@(1,1,1),@(9999,12,31),@(1900,2,28),@(2000,2,29),@(2023,1,31),@(2024,1,31),@(2024,2,29),@(2024,3,31),@(2024,4,30))) {
    foreach ($kind in [Enum]::GetValues([DateTimeKind])) {
        $origin = [DateTime]::SpecifyKind([DateTime]::new($date[0],$date[1],$date[2],12,34,56,789,123).AddTicks(7),$kind)
        foreach ($operand in @([int]::MinValue,-120001,-120000,-10001,-10000,-13,-12,-1,0,1,12,13,10000,10001,120000,120001,[int]::MaxValue)) {
            foreach ($operation in @('AddMonths','AddYears')) {
                try {
                    $value = if ($operation -eq 'AddMonths') { $origin.AddMonths($operand) } else { $origin.AddYears($operand) }
                    $result = [ordered]@{ticks=$value.Ticks;kind=$value.Kind.ToString()}
                } catch { $result = Failure $_ }
                $checkedArithmetic += [ordered]@{ticks=$origin.Ticks;kind=$kind.ToString();operation=$operation;operand=$operand;result=$result}
            }
        }
    }
}
$parsingInputs = [Collections.Generic.List[object]]::new()
foreach ($text in @($null,'','garbage','0000-01-01','-0001-01-01','+10000-01-01','10000-01-01','0001-01-01','9999-12-31',
    '1900-02-29','2000-02-29','2023-02-29','2024-02-29','2024-00-01','2024-13-01','2024-02-30',
    '2024-02-29T12:34','2024-02-29t12:34:56','2024-02-29 12:34:56','2024-02-29T12:34:56.',
    '2024-02-29T24:00:00','2024-02-29T23:60:00','2024-02-29T23:59:60',("`0"+'2024-02-29'))) { $parsingInputs.Add($text) }
foreach ($prefix in @('0001-01-01T00:00:00','2024-02-29T12:34:56','9999-12-31T23:59:59')) {
    foreach ($fraction in @('0','1','1234567','12345665','12345675','00000004','00000005','00000015','99999994','99999995',
        '0000000500000000000','99999999999999','0000000000000000001')) { $parsingInputs.Add($prefix+'.'+$fraction) }
}
foreach ($code in @(9,10,11,12,13,28,31,32,133,160,5760,8192,8232,8233,8239,8287,12288,65279)) {
    $parsingInputs.Add([string][char]$code+'2024-02-29T12:34:56'+[char]$code)
}
$parsing = @()
$savedCulture = [Globalization.CultureInfo]::CurrentCulture
try {
    [Globalization.CultureInfo]::CurrentCulture = [Globalization.CultureInfo]::InvariantCulture
    $parseMethod = [DateTime].GetMethod('Parse',[type[]]@([string]))
    foreach ($text in $parsingInputs) {
        try { $value = $parseMethod.Invoke($null,[object[]]@($text)); $result = [ordered]@{ticks=$value.Ticks;kind=$value.Kind.ToString()} }
        catch { $result = Failure $_ }
        $outValue = [DateTime]::new(2000,1,1)
        $success = [DateTime]::TryParse([string]$text,[ref]$outValue)
        $parsing += [ordered]@{input=$text;result=$result;trySuccess=$success;tryTicks=$outValue.Ticks;tryKind=$outValue.Kind.ToString()}
    }
} finally { [Globalization.CultureInfo]::CurrentCulture = $savedCulture }
$defaultDate = [Activator]::CreateInstance([DateTime])
$record = [ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    comparisons=$comparisons;tickConstructors=$tickConstructors;constants=$constants
    componentConstructors=$componentConstructors
    calendarProperties=$calendarProperties;enums=$enums
    floatingAddition=$floatingAddition
    checkedArithmetic=$checkedArithmetic
    parsing=$parsing
    defaultValue=[ordered]@{ticks=$defaultDate.Ticks;kind=$defaultDate.Kind.ToString()}
    qualification='BOUNDED_REFERENCE_ONLY; PUBLIC_QUALIFICATION_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned DateTime oracle: $($comparisons.Count) comparison cases"
