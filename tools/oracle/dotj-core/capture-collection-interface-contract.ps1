param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Selected interface lookup reference requires pinned CoreLib.'}
$profiles=@(@{name='System.Collections.IEnumerable';interfaces=@()},@{name='System.Collections.IEnumerator';interfaces=@()},@{name='System.Collections.ICollection';interfaces=@('System.Collections.IEnumerable')},@{name='System.Collections.IDictionary';interfaces=@('System.Collections.ICollection','System.Collections.IEnumerable')},@{name='System.Collections.IDictionaryEnumerator';interfaces=@('System.Collections.IEnumerator')},@{name='System.Collections.DictionaryEntry';interfaces=@()},@{name='System.Runtime.Serialization.SerializationInfoEnumerator';interfaces=@('System.Collections.IEnumerator')},@{name='System.Runtime.Serialization.IFormatterConverter';interfaces=@()})
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
$targets=@($profiles|ForEach-Object{$_.name})+@('System.Object','System.ValueType')
$relations=@();foreach($profile in $profiles){foreach($targetName in $targets){
 $sourceType=[Type]::GetType($profile.name,$true);$target=[Type]::GetType($targetName,$true)
 $relations+=[ordered]@{source=$profile.name;target=$targetName;assignable=$target.IsAssignableFrom($sourceType);subclass=$sourceType.IsSubclassOf($target)}
}}
$data=([Exception]::new()).Data
$samples=@(@{name='data';value=$data},@{name='enumerator';value=$data.GetEnumerator()},@{name='entry';value=[Collections.DictionaryEntry]::new('key','value')},@{name='object';value=[object]::new()},@{name='null';value=$null})
$instances=@();foreach($sample in $samples){foreach($targetName in $targets){$instances+=[ordered]@{sample=$sample.name;target=$targetName;result=([Type]::GetType($targetName,$true).IsInstanceOfType($sample.value))}}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();types=$types;lookups=$lookups;relations=$relations;instances=$instances;qualification='BOUNDED_COLLECTION_INTERFACE_LOOKUP_AND_RELATIONS_REFERENCE; OMITTED_INTERFACES_DISPATCH_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 18)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned selected interface lookup: $($types.Count) profiles and $($lookups.Count) queries"
