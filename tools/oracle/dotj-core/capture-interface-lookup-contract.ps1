param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Selected interface lookup reference requires pinned CoreLib.'}
$profiles=@(@{name='System.String';interfaces=@('System.IComparable','System.IConvertible')},@{name='System.Int32';interfaces=@('System.IComparable','System.IConvertible','System.IFormattable','System.ISpanFormattable','System.IUtf8SpanFormattable')},@{name='System.Byte';interfaces=@('System.IConvertible','System.IFormattable','System.IComparable')},@{name='System.SByte';interfaces=@('System.IConvertible','System.IFormattable','System.IComparable')},@{name='System.UInt16';interfaces=@('System.IConvertible','System.IFormattable')},@{name='System.UInt32';interfaces=@('System.IConvertible')},@{name='System.Decimal';interfaces=@('System.IConvertible')},@{name='System.DBNull';interfaces=@('System.IConvertible','System.Runtime.Serialization.ISerializable')},@{name='System.DateTime';interfaces=@('System.IComparable','System.IConvertible','System.IFormattable','System.ISpanFormattable','System.IUtf8SpanFormattable')},@{name='System.TimeSpan';interfaces=@('System.IComparable','System.IFormattable','System.ISpanFormattable','System.IUtf8SpanFormattable')},@{name='System.Object';interfaces=@()},@{name='System.Diagnostics.Stopwatch';interfaces=@()},@{name='System.IConvertible';interfaces=@()},@{name='System.IComparable';interfaces=@()},@{name='System.IFormattable';interfaces=@()},@{name='System.IFormatProvider';interfaces=@()},@{name='System.Runtime.Serialization.ISerializable';interfaces=@()},@{name='System.IDisposable';interfaces=@()},@{name='System.IUtf8SpanFormattable';interfaces=@()},@{name='System.ISpanFormattable';interfaces=@('System.IFormattable')})
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$types=@();$lookups=@();$lookupMethod=[Type].GetMethod('GetInterface',[type[]]@([string],[bool]))
foreach($profile in $profiles){
 $type=[Type]::GetType($profile.name,$true);$selected=@($profile.interfaces)
 $native=@($type.GetInterfaces()|ForEach-Object{$_.FullName}|Sort-Object)
 foreach($name in $selected){if($name -cnotin $native){throw "Selected interface missing from native type: $name"}}
 $types+=[ordered]@{name=$profile.name;selectedInterfaces=@($selected|Sort-Object);omittedInterfaces=@($native|Where-Object{$_ -cnotin $selected})}
 $queries=@('NotThere','System.NotThere','',$null)
 foreach($name in $selected){
  $split=$name.LastIndexOf('.');$namespace=$name.Substring(0,$split);$leaf=$name.Substring($split+1)
  $queries+=@($name,$leaf,$name.ToLowerInvariant(),$leaf.ToLowerInvariant(),($namespace+'.'+$leaf.ToLowerInvariant()),($namespace.ToLowerInvariant()+'.'+$leaf))
 }
 if($queries.Count -ne 4+6*$selected.Count){throw 'Interface query corpus shape changed.'}
 foreach($query in $queries){foreach($ignoreCase in @($false,$true)){
  try{$contract=$lookupMethod.Invoke($type,[object[]]@($query,$ignoreCase));$result=[ordered]@{name=$(if($null -eq $contract){$null}else{$contract.FullName})}}catch{$result=Failure $_}
  $lookups+=[ordered]@{source=$profile.name;query=$query;ignoreCase=$ignoreCase;result=$result}
 }}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();types=$types;lookups=$lookups;qualification='BOUNDED_SELECTED_INTERFACE_LOOKUP_REFERENCE; OMITTED_INTERFACES_DISPATCH_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 18)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned selected interface lookup: $($types.Count) profiles and $($lookups.Count) queries"
