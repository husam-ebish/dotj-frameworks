param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$coreHash = (Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if ([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678') {
    throw 'Temporal type oracle requires the pinned .NET 10.0.12 CoreLib.'
}
$temporal = @([DateTime],[TimeSpan],[DateTimeKind],[DayOfWeek])
$interfaces = @('System.IComparable','System.IFormattable','System.ISpanFormattable','System.IUtf8SpanFormattable','System.IConvertible')
$targets = @($temporal) + @([object],[ValueType],[Enum],[int],[string]) + @($interfaces | ForEach-Object { [type]$_ })
$types = @()
foreach ($type in $temporal) {
    $row = [ordered]@{name=$type.FullName;simpleName=$type.Name;baseType=$type.BaseType.FullName
        isClass=$type.IsClass;isValueType=$type.IsValueType;isEnum=$type.IsEnum;isSealed=$type.IsSealed;isPrimitive=$type.IsPrimitive
        typeCode=[int][Type]::GetTypeCode($type);arrayName=$type.MakeArrayType().FullName}
    if (-not $type.IsEnum) {
        $row.selectedInterfaces = @($type.GetInterfaces() | Where-Object {$_.FullName -in $interfaces} | ForEach-Object {$_.FullName} | Sort-Object)
        $row.omittedInterfaces = @($type.GetInterfaces() | Where-Object {$_.FullName -notin $interfaces} | ForEach-Object {$_.FullName} | Sort-Object)
    }
    $types += $row
}
$assignability = @()
$interfaceLookups = @()
foreach ($source in @([DateTime],[TimeSpan])) {
    foreach ($target in $targets) {
        $assignability += [ordered]@{source=$source.FullName;target=$target.FullName;result=$target.IsAssignableFrom($source)}
    }
    foreach ($name in $interfaces) {
        foreach ($query in @(@{name=$name;ignoreCase=$false},@{name=$name.Split('.')[-1];ignoreCase=$false},
            @{name=$name.ToLowerInvariant();ignoreCase=$false},@{name=$name.ToLowerInvariant();ignoreCase=$true},
            @{name=('System.'+$name.Split('.')[-1].ToLowerInvariant());ignoreCase=$true},
            @{name=$name.Split('.')[-1].ToLowerInvariant();ignoreCase=$true},
            @{name=('System.'+$name.Split('.')[-1].ToLowerInvariant());ignoreCase=$false},
            @{name=$name.Split('.')[-1].ToLowerInvariant();ignoreCase=$false})) {
            $contract = $source.GetInterface($query.name,$query.ignoreCase)
            $interfaceLookups += [ordered]@{source=$source.FullName;query=$query.name;ignoreCase=$query.ignoreCase
                result=$(if ($null -eq $contract) {$null} else {$contract.FullName})}
        }
    }
}
$samples = @(@{name='Null';value=$null},@{name='Object';value=[object]::new()},@{name='DateTime';value=[DateTime]::new([long]1)},
    @{name='TimeSpan';value=[TimeSpan]::FromTicks(1)},@{name='DateTimeKind';value=[DateTimeKind]::Utc},@{name='DayOfWeek';value=[DayOfWeek]::Wednesday})
$instances = @()
foreach ($sample in $samples) {
    foreach ($target in $targets) {
        if ($sample.name -in @('DateTimeKind','DayOfWeek') -and $target.IsInterface) { continue }
        $instances += [ordered]@{sample=$sample.name;target=$target.FullName;result=$target.IsInstanceOfType($sample.value)}
    }
}
$record = [ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    types=$types;assignability=$assignability;instances=$instances;interfaceLookups=$interfaceLookups
    qualification='SELECTED_TEMPORAL_METADATA_ONLY; OMITTED_INTERFACES_AND_LANGUAGE_MAPPING_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned temporal type oracle: $($types.Count) identities, $($assignability.Count) assignability and $($instances.Count) instance cases"
