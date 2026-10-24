param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum query oracle requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$rows=@()
$bases=@('System.DayOfWeek','System.DateTimeKind','System.Globalization.NumberStyles','System.Globalization.TimeSpanStyles','System.Diagnostics.Stopwatch','System.DateTime','System.TimeSpan','System.Int32')
$suffixes=@('[]','[*]','[,]','[,,]','*','&','**','*&','*[]','[]&','[][]','[,][]')
foreach($base in $bases){foreach($suffix in $suffixes){foreach($variant in @('canonical','lower','assembly')){
 $canonical=$base+$suffix
 $query=switch($variant){canonical {$canonical};lower {$canonical.ToLowerInvariant()};assembly {$canonical+', System.Private.CoreLib'}}
 foreach($ignoreCase in @($false,$true)){foreach($throwOnError in @($false,$true)){
  try{$type=[Type]::GetType($query,$throwOnError,$ignoreCase)
   if($null -eq $type){$result=[ordered]@{name=$null}}
   else{$result=[ordered]@{name=$type.FullName;simpleName=$type.Name;isArray=$type.IsArray;isByRef=$type.IsByRef;isPointer=$type.IsPointer;isEnum=$type.IsEnum;elementName=$type.GetElementType().FullName}}
  }catch{$result=Failure $_}
  $rows+=[ordered]@{base=$base;suffix=$suffix;query=$query;ignoreCase=$ignoreCase;throwOnError=$throwOnError;result=$result}
 }}
}}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();queries=$rows;qualification='BOUNDED_SELECTED_SHAPE_NAME_LOOKUP_REFERENCE; GENERAL_GRAMMAR_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned selected shape-name lookup: $($rows.Count) cases"
