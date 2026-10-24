param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Stopwatch Type oracle requires pinned CoreLib.'}
$watch=[Diagnostics.Stopwatch];$array=$watch.MakeArrayType()
$types=@();foreach($type in @($watch,$array)){
    $types+=[ordered]@{name=$type.FullName;simpleName=$type.Name;namespace=$type.Namespace;baseType=$type.BaseType.FullName
        isClass=$type.IsClass;isValueType=$type.IsValueType;isEnum=$type.IsEnum;isSealed=$type.IsSealed;isPrimitive=$type.IsPrimitive;isArray=$type.IsArray
        typeCode=[int][Type]::GetTypeCode($type);elementName=$(if($type.IsArray){$type.GetElementType().FullName}else{$null})}
}
$targets=@($watch,$array,[object],[Array],[ValueType],[Enum],[DateTime],[TimeSpan],[IDisposable],[IComparable],[IFormattable],[IConvertible],
    [object[]],[DateTime[]],[TimeSpan[]],[string[]],[bool[]],[char[]],[short[]],[int[]],[long[]],[float[]],[double[]],[byte[]])
$assignability=@();foreach($source in @($watch,$array,[object[]],[DateTime[]],[TimeSpan[]],[string[]],[bool[]],[char[]],[short[]],[int[]],[long[]],[float[]],[double[]],[byte[]],[string])){foreach($target in $targets){$assignability+=[ordered]@{source=$source.FullName;target=$target.FullName;result=$target.IsAssignableFrom($source)}}}
$samples=@(@{name='Null';value=$null},@{name='Stopwatch';value=[Diagnostics.Stopwatch]::new()},@{name='StopwatchArray';value=[Diagnostics.Stopwatch[]]::new(0)},
    @{name='Object';value=[object]::new()},@{name='String';value='sample'},@{name='DateTime';value=[DateTime]::new([long]1)},@{name='TimeSpan';value=[TimeSpan]::FromTicks(1)},
    @{name='ObjectArray';value=[object[]]::new(0)},@{name='StringArray';value=[string[]]::new(0)},@{name='DateTimeArray';value=[DateTime[]]::new(0)},@{name='TimeSpanArray';value=[TimeSpan[]]::new(0)},
    @{name='BooleanArray';value=[bool[]]::new(0)},@{name='CharArray';value=[char[]]::new(0)},@{name='Int16Array';value=[short[]]::new(0)},@{name='Int32Array';value=[int[]]::new(0)},
    @{name='Int64Array';value=[long[]]::new(0)},@{name='SingleArray';value=[float[]]::new(0)},@{name='DoubleArray';value=[double[]]::new(0)},@{name='ByteArray';value=[byte[]]::new(0)})
$instances=@();foreach($sample in $samples){foreach($target in $targets){$instances+=[ordered]@{sample=$sample.name;target=$target.FullName;result=$target.IsInstanceOfType($sample.value)}}}
$lookups=@();foreach($query in @($watch.FullName,$watch.FullName.ToLowerInvariant(),'System.Diagnostics.stopwatch',$array.FullName,$array.FullName.ToLowerInvariant(),
    $watch.AssemblyQualifiedName,$array.AssemblyQualifiedName,'System.Diagnostics.Stopwatch, System.Private.CoreLib','Stopwatch','System.Diagnostics.MissingStopwatch')){
    foreach($ignoreCase in @($false,$true)){foreach($throwOnError in @($false,$true)){
        try{$value=[Type]::GetType($query,$throwOnError,$ignoreCase);$result=[ordered]@{name=$(if($null -eq $value){$null}else{$value.FullName})}}
        catch{$e=$_.Exception.GetBaseException();$result=[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult}}
        $lookups+=[ordered]@{query=$query;ignoreCase=$ignoreCase;throwOnError=$throwOnError;result=$result}
    }}
}
$interfaces=@($watch.GetInterfaces()|ForEach-Object{$_.FullName})
$interfaceLookups=@();foreach($query in @('System.IDisposable','IDisposable','System.IComparable','icomparable')){foreach($ignoreCase in @($false,$true)){
    $value=$watch.GetInterface($query,$ignoreCase);$interfaceLookups+=[ordered]@{query=$query;ignoreCase=$ignoreCase;name=$(if($null -eq $value){$null}else{$value.FullName})}
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    types=$types;assignability=$assignability;instances=$instances;lookups=$lookups;interfaces=$interfaces;interfaceLookups=$interfaceLookups
    defaultMembers=@($watch.GetDefaultMembers()|ForEach-Object{$_.Name})
    qualification='SELECTED_STOPWATCH_TYPE_AND_ARRAY_REFERENCE; FULL_REFLECTION_GENERICS_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned Stopwatch Type reference: $($lookups.Count) lookups and $($instances.Count) instance checks"
