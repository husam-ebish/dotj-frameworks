param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$coreHash = (Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if ([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678') {
    throw 'Exception oracle requires the pinned .NET 10.0.12 CoreLib.'
}
$rows = @()
foreach ($name in @('System.Exception','System.SystemException','System.ArgumentException','System.ArgumentNullException',
    'System.ArgumentOutOfRangeException','System.ArithmeticException','System.DivideByZeroException','System.IndexOutOfRangeException',
    'System.OverflowException','System.InvalidCastException','System.InvalidOperationException','System.NullReferenceException',
    'System.FormatException','System.TypeLoadException','System.IO.IOException','System.IO.FileNotFoundException',
    'System.IO.FileLoadException','System.Globalization.CultureNotFoundException','System.Runtime.Serialization.SerializationException')) {
    $type = [type]$name
    foreach ($ctor in $type.GetConstructors()) {
        $parameters = @($ctor.GetParameters())
        if (@($parameters | Where-Object { $_.ParameterType.FullName -notin @('System.String','System.Exception','System.Int32','System.Object') }).Count) { continue }
        $explicitError = @($parameters | Where-Object { $_.Name -in @('hresult','errorCode') }).Count -gt 0
        $codes = if ($explicitError) { @(0,123,-1,[int]::MinValue) } else { @(123) }
        foreach ($profile in @('Supplied','NullReferences')) {
            foreach ($code in $codes) {
                $arguments = [object[]]::new($parameters.Count)
                $values = @()
                for ($index = 0; $index -lt $parameters.Count; $index++) {
                    $parameter = $parameters[$index]
                    $kind = $parameter.ParameterType.FullName
                    $value = switch ($kind) {
                        'System.String' { if ($profile -eq 'Supplied') { $parameter.Name + '-value' } else { $null } }
                        'System.Exception' { if ($profile -eq 'Supplied') { [Exception]::new('inner-value') } else { $null } }
                        'System.Int32' { [int]$code }
                        'System.Object' { if ($profile -eq 'Supplied') { [int]17 } else { $null } }
                    }
                    $arguments[$index] = $value
                    $values += $(if ($kind -eq 'System.Exception') { $null -ne $value } else { $value })
                }
                $value = $ctor.Invoke($arguments)
                $row = [ordered]@{ type = $name; parameterTypes = @($parameters | ForEach-Object { $_.ParameterType.FullName })
                    arguments = $values; profile = $profile; hResult = $value.HResult; innerPresent = ($null -ne $value.InnerException) }
                if ($value -is [ArgumentException]) { $row.paramName = $value.ParamName }
                if ($value -is [IO.FileNotFoundException] -or $value -is [IO.FileLoadException]) { $row.fileName = $value.FileName }
                $rows += $row
            }
        }
    }
}
$record = [ordered]@{ schemaVersion = 1; runtimeVersion = [Environment]::Version.ToString(); coreLibSha256 = $coreHash
    oracleSha256 = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    scope = 'Nineteen selected exception types; public non-serialization constructor metadata and inner identity'
    constructors = $rows; qualification = 'BOUNDED_REFERENCE_ONLY; MESSAGES_AND_SERIALIZATION_OPEN' }
[IO.File]::WriteAllText($OutputPath, ($record | ConvertTo-Json -Depth 12) + "`n", [Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned exception oracle: $($rows.Count) constructor cases"
