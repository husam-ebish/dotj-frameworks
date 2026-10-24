param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum query oracle requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$inputs=@()
foreach($value in @(-1,0,1,2,7,8,15,111,1027,[int]::MaxValue)){
 foreach($kind in @('int','long','short','number','style','day','dateKind')){
  if($kind -eq 'short' -and $value -gt 32767){continue}
  if($kind -eq 'number' -and $value -notin @(0,1,2,7,8,15,111,1027)){continue}
  if($kind -eq 'day' -and ($value -lt 0 -or $value -gt 6)){continue}
  if($kind -eq 'dateKind' -and ($value -lt 0 -or $value -gt 2)){continue}
  $object=switch($kind){int {[int]$value};long {[long]$value};short {[short]$value};number {[Enum]::ToObject([Globalization.NumberStyles],[int]$value)};style {[Enum]::ToObject([Globalization.TimeSpanStyles],[int]$value)};day {[Enum]::ToObject([DayOfWeek],[int]$value)};dateKind {[Enum]::ToObject([DateTimeKind],[int]$value)}}
  $inputs+=@{kind=$kind;value=$value;object=$object}
 }
}
foreach($value in @('None','Integer','AssumeNegative','none','1','None, AssumeNegative')){$inputs+=@{kind='string';value=$value;object=$value}}
$inputs+=@{kind='null';value=$null;object=$null};$inputs+=@{kind='boolean';value=$true;object=$true};$inputs+=@{kind='double';value=1.0;object=[double]1}
$rows=@();foreach($type in @([Globalization.NumberStyles],[Globalization.TimeSpanStyles],[DayOfWeek],[DateTimeKind])){foreach($item in $inputs){
 try{$name=[ordered]@{name=$type.GetEnumName($item.object)}}catch{$name=Failure $_}
 try{$defined=[ordered]@{boolean=$type.IsEnumDefined($item.object)}}catch{$defined=Failure $_}
 $rows+=[ordered]@{target=$type.FullName;kind=$item.kind;value=$item.value;nameResult=$name;definedResult=$defined}
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();queries=$rows;qualification='BOUNDED_ENUM_QUERY_REFERENCE; OTHER_UNDERLYING_TYPES_AND_FULL_REFLECTION_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned enum queries: $($rows.Count) pairs"
