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
$record = [ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    comparisons=$comparisons;qualification='BOUNDED_REFERENCE_ONLY; PUBLIC_QUALIFICATION_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned DateTime oracle: $($comparisons.Count) comparison cases"
