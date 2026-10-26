param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture;[Globalization.CultureInfo]::CurrentUICulture=[Globalization.CultureInfo]::InvariantCulture
function Normal($Value){
 if([object]::ReferenceEquals($Value,$null)){return 'N'}
 if($Value -is [Collections.DictionaryEntry]){return 'E('+(Normal $Value.Key)+','+(Normal $Value.Value)+')'}
 if($Value -is [string]){return 'S:'+(([int[]][char[]]$Value)-join ',')}
 if($Value -is [single]){return 'F32:'+([BitConverter]::SingleToInt32Bits($Value).ToString('x8'))}
 if($Value -is [double]){return 'F64:'+([BitConverter]::DoubleToInt64Bits($Value).ToString('x16'))}
 if($Value -is [char]){return 'Char:'+([int]$Value)}
 if($Value -is [bool]){return 'Boolean:'+([int]$Value)}
 return $Value.GetType().Name+':'+[string]$Value
}
function Make-Array([string]$Kind){
 switch($Kind){'object'{$a=[object[]]@('guard','guard','guard','guard')};'entry'{$a=[Collections.DictionaryEntry[]]::new(4);for($i=0;$i -lt 4;$i++){$a[$i]=[Collections.DictionaryEntry]::new('guard',99)}};'string'{$a=[string[]]@('guard','guard','guard','guard')};'short'{$a=[short[]]@(99,99,99,99)};'int'{$a=[int[]]@(99,99,99,99)};'long'{$a=[long[]]@(99,99,99,99)};'float'{$a=[single[]]@(99,99,99,99)};'double'{$a=[double[]]@(99,99,99,99)};'char'{$a=[char[]]@(99,99,99,99)};'bool'{$a=[bool[]]@($true,$true,$true,$true)}}
 return ,$a
}
function Snapshot($Array){$values=@();foreach($value in $Array){$values+=@(Normal $value)};return ,$values}
$sources=[Collections.Generic.List[object]]::new();$sources.Add($null);$sources.Add('text');foreach($v in @(-128,-1,0,127)){$sources.Add([sbyte]$v)};foreach($v in @(-32768,0,32767)){$sources.Add([short]$v)};foreach($v in @([int]::MinValue,-1,0,[int]::MaxValue)){$sources.Add([int]$v)};foreach($v in @([long]::MinValue,-1,0,[long]::MaxValue)){$sources.Add([long]$v)};foreach($v in @(0,65,65535)){$sources.Add([char]$v)};foreach($v in @($false,$true)){$sources.Add($v)}
foreach($hex in @('00000000','80000000','7fc00001','7f800000','ff800000','7f7fffff','00000001','3fc00000')){$sources.Add([BitConverter]::Int32BitsToSingle([Convert]::ToInt32($hex,16)))}
foreach($hex in @('0000000000000000','8000000000000000','7ff8000000000001','7ff0000000000000','fff0000000000000','7fefffffffffffff','0000000000000001','3ff8000000000000')){$sources.Add([BitConverter]::Int64BitsToDouble([Convert]::ToInt64($hex,16)))}
$rows=[Collections.Generic.List[object]]::new();$profile=0
foreach($value in $sources){foreach($kind in @('object','entry','string','short','int','long','float','double','char','bool')){foreach($index in @(-1,0,1,2,3,4)){
 $d=[Exception]::new('primitive copy').Data;[void][Collections.IDictionary].GetMethod('Add').Invoke($d,[object[]]@('first',$value));[void][Collections.IDictionary].GetMethod('Add').Invoke($d,[object[]]@('last','tail'));$collection=[Collections.IDictionary].GetMethod('get_Values').Invoke($d,[object[]]@());$array=Make-Array $kind
 try{[void][Collections.ICollection].GetMethod('CopyTo').Invoke($collection,[object[]]@($array,$index));$outcome=[ordered]@{ok=$true}}catch{$e=$_.Exception;while($e.InnerException){$e=$e.InnerException};$outcome=[ordered]@{ok=$false;exception=$e.GetType().FullName;messageUnits=[int[]][char[]]$e.Message;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null});actualValue=$(if($e -is [ArgumentOutOfRangeException]){Normal $e.ActualValue}else{$null})}}
 $first=[Collections.IDictionary].GetMethod('get_Item').Invoke($d,[object[]]@('first'));$last=[Collections.IDictionary].GetMethod('get_Item').Invoke($d,[object[]]@('last'));$rows.Add([ordered]@{profile=$profile;source=(Normal $value);kind=$kind;index=$index;outcome=$outcome;array=(Snapshot $array);count=[Collections.ICollection].GetProperty('Count').GetValue($d);values=@((Normal $first),(Normal $last))})
}};$profile++}
if($profile -ne 38 -or $rows.Count -ne 2280){throw "Wrong primitive matrix profiles=$profile rows=$($rows.Count)"}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();culture='Invariant';profiles=$profile;rows=$rows.ToArray();qualification='SELECTED_VALUES_COPYTO_PRIMITIVE_WIDENING_NULLS_AND_RAW_FLOAT_BITS_ONLY; UNSIGNED_ARRAYS_FULL_BOXING_ABI_SERIALIZATION_REENTRANCY_AND_TASK_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 18 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS primitive CopyTo native matrix: $profile profiles, $($rows.Count) cases"
