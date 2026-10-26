param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture;[Globalization.CultureInfo]::CurrentUICulture=[Globalization.CultureInfo]::InvariantCulture
function Normal($Value){
 if([object]::ReferenceEquals($Value,$null)){return 'N'}
 if($Value -is [Collections.DictionaryEntry]){return 'E('+(Normal $Value.Key)+','+(Normal $Value.Value)+')'}
 if($Value -is [string]){return 'S:'+(([int[]][char[]]$Value)-join ',')}
 return $Value.GetType().Name+':'+[string]$Value
}
function Make-Data([int]$Profile){
 $d=[Exception]::new('copy').Data
 $pairs=switch($Profile){0{@()};1{@(@('k',7))};2{@(@(1,1),@('x','text'))};3{@(@(1,1),@(2,'text'),@(3,3))};4{@(@('a',$null),@('b','text'),@('c',1))};5{@(@('a','one'),@('b','two'),@('c','three'))}}
 # Preserve pair arrays even when the selected profile has only one pair.
 if($Profile -eq 1){[void][Collections.IDictionary].GetMethod('Add').Invoke($d,[object[]]@('k',7))}else{foreach($pair in $pairs){[void][Collections.IDictionary].GetMethod('Add').Invoke($d,[object[]]@($pair[0],$pair[1]))}}
 return ,$d
}
function Make-Array([string]$Kind){
 switch($Kind){'null'{$a=$null};'object'{$a=[object[]]@('guard','guard','guard')};'entry'{$a=[Collections.DictionaryEntry[]]@([Collections.DictionaryEntry]::new('guard',99),[Collections.DictionaryEntry]::new('guard',99),[Collections.DictionaryEntry]::new('guard',99))};'string'{$a=[string[]]@('guard','guard','guard')};'int'{$a=[int[]]@(99,99,99)};'long'{$a=[long[]]@(99,99,99)};'byte'{$a=[byte[]]@(99,99,99)};'rank2'{$r=[object[,]]::new(2,2);$r[0,0]='guard';$r[0,1]='guard';$r[1,0]='guard';$r[1,1]='guard';$a=$r}}
 return ,$a
}
function Snapshot($Array){if([object]::ReferenceEquals($Array,$null)){return $null};$values=@();foreach($value in $Array){$values+=@(Normal $value)};return ,$values}
function Contents($Dictionary){$cursor=[Collections.IDictionary].GetMethod('GetEnumerator').Invoke($Dictionary,[object[]]@());$values=@();while([Collections.IEnumerator].GetMethod('MoveNext').Invoke($cursor,[object[]]@())){$values+=@(Normal ([Collections.IDictionaryEnumerator].GetProperty('Entry').GetValue($cursor)))};return ,$values}
$rows=[Collections.Generic.List[object]]::new()
foreach($profile in 0..5){foreach($view in @('dictionary','keys','values')){foreach($kind in @('null','object','entry','string','int','long','byte','rank2')){foreach($index in @([int]::MinValue,-1,0,1,2,3,4,[int]::MaxValue)){
 $d=Make-Data $profile;if($view -eq 'dictionary'){$collection=$d}else{$collection=[Collections.IDictionary].GetMethod($(if($view -eq 'keys'){'get_Keys'}else{'get_Values'})).Invoke($d,[object[]]@())};$array=Make-Array $kind
 try{[Collections.ICollection].GetMethod('CopyTo').Invoke($collection,[object[]]@($array,$index));$outcome=[ordered]@{ok=$true}}catch{$e=$_.Exception;while($e.InnerException){$e=$e.InnerException};$outcome=[ordered]@{ok=$false;exception=$e.GetType().FullName;messageUnits=[int[]][char[]]$e.Message;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null});actualValue=$(if($e -is [ArgumentOutOfRangeException]){Normal $e.ActualValue}else{$null})}}
 $rows.Add([ordered]@{profile=$profile;view=$view;kind=$kind;index=$index;outcome=$outcome;array=(Snapshot $array);count=[Collections.ICollection].GetProperty('Count').GetValue($d);contents=(Contents $d)})
}}}}
if($rows.Count -ne 1152){throw 'Wrong copy matrix'}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();culture='Invariant';rows=$rows.ToArray();qualification='SELECTED_COPYTO_VALIDATION_AND_PARTIAL_WRITES_ONLY; JAGGED_NONZERO_BOUNDS_SERIALIZATION_REENTRANCY_AND_TASK_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 18 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output 'PASS CopyTo native matrix: 1152 cases'
