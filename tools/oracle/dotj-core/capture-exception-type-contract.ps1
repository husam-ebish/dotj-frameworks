param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Exception Type reference requires pinned CoreLib.'}
$names=@('System.Exception','System.SystemException','System.ArgumentException','System.ArgumentNullException','System.ArgumentOutOfRangeException','System.ArithmeticException','System.DivideByZeroException','System.OverflowException','System.InvalidCastException','System.InvalidOperationException','System.NullReferenceException','System.IndexOutOfRangeException','System.FormatException','System.TypeLoadException','System.IO.IOException','System.IO.FileNotFoundException','System.IO.FileLoadException','System.Globalization.CultureNotFoundException','System.Runtime.Serialization.SerializationException')
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$types=@();$lookups=@();$relations=@()
$lookupMethod=[Type].GetMethod('GetInterface',[type[]]@([string],[bool]))
foreach($name in $names){
 $type=[Type]::GetType($name,$true);$instance=[Activator]::CreateInstance($type)
 $types+=[ordered]@{name=$name;baseType=$type.BaseType.FullName;isSealed=$type.IsSealed;isSerializable=$type.IsSerializable;isClass=$type.IsClass;isValueType=$type.IsValueType;isAbstract=$type.IsAbstract;isPrimitive=$type.IsPrimitive;typeCode=[int][Type]::GetTypeCode($type);interfaces=@($type.GetInterfaces()|ForEach-Object{$_.FullName}|Sort-Object)}
 foreach($query in @('ISerializable','System.Runtime.Serialization.ISerializable','iserializable','System.Runtime.Serialization.iserializable','system.runtime.serialization.ISerializable','system.runtime.serialization.iserializable','IConvertible','System.IDisposable','','NotThere',$null)){
  foreach($ignoreCase in @($false,$true)){
   try{$contract=$lookupMethod.Invoke($type,[object[]]@($query,$ignoreCase));$result=[ordered]@{name=$(if($null -eq $contract){$null}else{$contract.FullName})}}catch{$result=Failure $_}
   $lookups+=[ordered]@{source=$name;query=$query;ignoreCase=$ignoreCase;result=$result}
  }
 }
 foreach($targetName in @($names)+@('System.Object','System.Runtime.Serialization.ISerializable','System.String')){
  $target=[Type]::GetType($targetName,$true)
  $relations+=[ordered]@{source=$name;target=$targetName;assignable=$target.IsAssignableFrom($type);subclass=$type.IsSubclassOf($target);instance=$target.IsInstanceOfType($instance)}
 }
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();types=$types;lookups=$lookups;relations=$relations;qualification='BOUNDED_SELECTED_EXCEPTION_TYPE_HIERARCHY_REFERENCE; SERIALIZATION_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned exception Type reference: $($types.Count) types, $($lookups.Count) lookups, $($relations.Count) relation triples"
