param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}

function Encoder-Call($Encoder,[string]$Operation,[char[]]$Source,[int]$Index,[int]$Count,[byte[]]$Destination,[int]$OutputIndex,[bool]$Flush){
 try{$n=if($Operation -eq 'Count'){$Encoder.GetByteCount($Source,$Index,$Count,$Flush)}else{$Encoder.GetBytes($Source,$Index,$Count,$Destination,$OutputIndex,$Flush)};return [ordered]@{ok=$true;count=$n}}catch{$e=$_.Exception;while($e.InnerException){$e=$e.InnerException};$f=[ordered]@{ok=$false;exception=$e.GetType().FullName;hResult=$e.HResult;message=$e.Message;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})};if($e -is [Text.EncoderFallbackException]){$f.unknown=[int]$e.CharUnknown;$f.index=$e.Index;$f.high=[int]$e.CharUnknownHigh;$f.low=[int]$e.CharUnknownLow;$f.isPair=$e.IsUnknownSurrogate()};return $f}
}

$texts=[Collections.Generic.List[object]]::new();$texts.Add([int[]]@());$level=[Collections.Generic.List[object]]::new();$level.Add([int[]]@());foreach($length in 1..4){$next=[Collections.Generic.List[object]]::new();foreach($prefix in $level){foreach($unit in @(65,0xd800,0xdc00)){$v=[int[]](@($prefix)+@($unit));$texts.Add($v);$next.Add($v)}};$level=$next.ToArray()};foreach($v in @(@(0),@(0x7ff),@(0x800),@(0xd7ff),@(0xe000),@(0xffff),@(0xdbff,0xdfff),@(65,0,0xdbff,0xdfff),@(0xd800,0xdbff,0xdfff,0xdc00))){$texts.Add([int[]]$v)}
$configs=@();foreach($big in @($false,$true)){foreach($strict in @($false,$true)){$configs+=@([ordered]@{bigEndian=$big;strict=$strict;replacement=$null})};foreach($replacement in @(@(),@(65,66),@(0xd800,0xdc00))){$configs+=@([ordered]@{bigEndian=$big;strict=$false;replacement=[int[]]$replacement})}}


function Convert-Call($Encoder,[char[]]$Source,[int]$Index,[int]$Count,[byte[]]$Destination,[int]$OutputIndex,[int]$Capacity,[bool]$Flush){
 $cu=-71;$bu=-72;$done=$true;$result=$null
 try{$Encoder.Convert($Source,$Index,$Count,$Destination,$OutputIndex,$Capacity,$Flush,[ref]$cu,[ref]$bu,[ref]$done);$result=[ordered]@{ok=$true}}catch{$e=$_.Exception;while($e.InnerException){$e=$e.InnerException};$result=[ordered]@{ok=$false;exception=$e.GetType().FullName;message=$e.Message;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})};if($e -is [Text.EncoderFallbackException]){$result.unknown=[int]$e.CharUnknown;$result.index=$e.Index;$result.high=[int]$e.CharUnknownHigh;$result.low=[int]$e.CharUnknownLow;$result.isPair=$e.IsUnknownSurrogate()}}
 $result.charsUsed=$cu;$result.bytesUsed=$bu;$result.completed=$done;$result.remaining=$Encoder.FallbackBuffer.Remaining;return $result
}

function Operation-Call($Encoder,$Owner,[string]$Operation,[byte[]]$Destination){
 try{$n=switch($Operation){
 'Count' {$Encoder.GetByteCount([char[]]@(65,55296),0,2,$true)}
 'CountEmpty' {$Encoder.GetByteCount([char[]]@(),0,0,$true)}
 'Bytes' {$Encoder.GetBytes([char[]]@(65,55296),0,2,$Destination,1,$true)}
 'BytesEmpty' {$Encoder.GetBytes([char[]]@(),0,0,$Destination,1,$true)}
 'Reset' {$Encoder.Reset();0}
 'SetEmpty' {$Encoder.Fallback=[Text.EncoderReplacementFallback]::new('');0}
 'SetAB' {$Encoder.Fallback=[Text.EncoderReplacementFallback]::new('AB');0}
 'SetStrict' {$Encoder.Fallback=[Text.EncoderFallback]::ExceptionFallback;0}
 'OwnerStrict' {$Owner.EncoderFallback=[Text.EncoderFallback]::ExceptionFallback;0}
 'BufferNext' {[int]$Encoder.FallbackBuffer.GetNextChar()}
 'BufferPrevious' {[int]$Encoder.FallbackBuffer.MovePrevious()}
 'BufferReset' {$Encoder.FallbackBuffer.Reset();0}
 };$r=[ordered]@{ok=$true;count=$n}}catch{$e=$_.Exception;while($e.InnerException){$e=$e.InnerException};$r=[ordered]@{ok=$false;exception=$e.GetType().FullName;hResult=$e.HResult;message=$e.Message;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})};if($e -is [Text.EncoderFallbackException]){$r.unknown=[int]$e.CharUnknown;$r.index=$e.Index;$r.high=[int]$e.CharUnknownHigh;$r.low=[int]$e.CharUnknownLow;$r.isPair=$e.IsUnknownSurrogate()}}
 $r.remaining=$Encoder.FallbackBuffer.Remaining;return $r
}
function State-Of($Encoder,$Owner){return [ordered]@{fallbackType=$Encoder.Fallback.GetType().FullName;replacement=$(if($Encoder.Fallback -is [Text.EncoderReplacementFallback]){,[int[]][char[]]$Encoder.Fallback.DefaultString}else{$null});ownerType=$Owner.EncoderFallback.GetType().FullName;ownerReplacement=$(if($Owner.EncoderFallback -is [Text.EncoderReplacementFallback]){,[int[]][char[]]$Owner.EncoderFallback.DefaultString}else{$null});sharedOwner=[object]::ReferenceEquals($Encoder.Fallback,$Owner.EncoderFallback)}}
$inputs=@(@(),@(55296),@(56320),@(65,66),@(55296,65),@(56320,65),@(55296,56320),@(56320,55296));$operations=@('Count','CountEmpty','Bytes','BytesEmpty','Reset','SetEmpty','SetAB','SetStrict','OwnerStrict','BufferNext','BufferPrevious','BufferReset');$profiles=[Collections.Generic.List[object]]::new()
foreach($config in $configs){
 $profileOwner=[Text.Encoding]([Text.UnicodeEncoding]::new([bool]$config.bigEndian,$true,[bool]$config.strict)).Clone();if($null -ne $config.replacement){$profileOwner.EncoderFallback=[Text.EncoderReplacementFallback]::new([string]::new([char[]][int[]]$config.replacement))};$rows=[Collections.Generic.List[object]]::new()
 foreach($sourceId in 0..($inputs.Count-1)){foreach($pending in @($false,$true)){foreach($flush in @($false,$true)){foreach($capacity in @(0,2,4,6)){foreach($operation in $operations){
  $owner=[Text.Encoding]$profileOwner.Clone();$encoder=$owner.GetEncoder();if($pending){$seed=Encoder-Call $encoder 'Bytes' ([char[]]@(55296)) 0 1 ([byte[]]@()) 0 $false;if(-not $seed.ok -or $seed.count -ne 0){throw 'Pending seed failed'}}
  $source=[char[]][int[]]$inputs[$sourceId];$dest=[byte[]](@(99)*($capacity+4));$first=Convert-Call $encoder $source 0 $source.Length $dest 1 $capacity $flush
  $opDest=[byte[]](@(99)*18);$result=Operation-Call $encoder $owner $operation $opDest;$state=State-Of $encoder $owner
  $count=Operation-Call $encoder $owner 'CountEmpty' ([byte[]]@());$tail=[byte[]](@(99)*18);$write=Operation-Call $encoder $owner 'BytesEmpty' $tail
  $bufferResults=@();foreach($probe in @('BufferPrevious','BufferNext','BufferPrevious','BufferPrevious','BufferNext','BufferNext')){$bufferResults+=@([ordered]@{operation=$probe;result=(Operation-Call $encoder $owner $probe ([byte[]]@()))})}
  $last=[byte[]](@(99)*20);$lastResult=Convert-Call $encoder ([char[]]@(56320,65)) 0 2 $last 1 16 $true
  $rows.Add([ordered]@{sourceId=$sourceId;pending=$pending;flush=$flush;capacity=$capacity;operation=$operation;first=$first;after=[int[]]$dest;operationResult=$result;operationAfter=[int[]]$opDest;state=$state;countResult=$count;writeResult=$write;writeAfter=[int[]]$tail;bufferResults=$bufferResults;lastResult=$lastResult;lastAfter=[int[]]$last})
 }}}}}
 $profiles.Add([ordered]@{config=$config;rows=$rows.ToArray()})
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();inputs=$inputs;operations=$operations;profiles=$profiles.ToArray();qualification='NATIVE_UNICODE_ENCODER_INTERLEAVING_REFERENCE_ONLY; NO_JAVA_QUALIFICATION_OR_TASK_ACCEPTANCE'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 19 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS UTF16 encoder interleaving capture: $($profiles.Count) configurations"
