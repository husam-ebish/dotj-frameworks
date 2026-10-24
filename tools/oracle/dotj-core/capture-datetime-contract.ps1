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
$defaultDate = [Activator]::CreateInstance([DateTime])
$record = [ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    comparisons=$comparisons;tickConstructors=$tickConstructors;constants=$constants
    componentConstructors=$componentConstructors
    defaultValue=[ordered]@{ticks=$defaultDate.Ticks;kind=$defaultDate.Kind.ToString()}
    qualification='BOUNDED_REFERENCE_ONLY; PUBLIC_QUALIFICATION_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned DateTime oracle: $($comparisons.Count) comparison cases"
