param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
function Decoder-Call($Decoder,[string]$Operation,[byte[]]$Source,[int]$Index,[int]$Count,[char[]]$Destination,[int]$OutputIndex,[bool]$Flush){
 try{$n=if($Operation -eq 'Count'){$Decoder.GetCharCount($Source,$Index,$Count,$Flush)}else{$Decoder.GetChars($Source,$Index,$Count,$Destination,$OutputIndex,$Flush)};return [ordered]@{ok=$true;count=$n}}catch{$e=$_.Exception;while($e.InnerException){$e=$e.InnerException};$r=[ordered]@{ok=$false;exception=$e.GetType().FullName;hResult=$e.HResult;message=$e.Message;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})};if($e -is [Text.DecoderFallbackException]){$r.unknown=[int[]]$e.BytesUnknown;$r.index=$e.Index};return $r}
}
function Convert-Call($Decoder,[byte[]]$Source,[int]$Index,[int]$Count,[char[]]$Destination,[int]$OutputIndex,[int]$Capacity,[bool]$Flush){
 $cu=-71;$bu=-72;$done=$true;$result=$null
 try{$Decoder.Convert($Source,$Index,$Count,$Destination,$OutputIndex,$Capacity,$Flush,[ref]$cu,[ref]$bu,[ref]$done);$result=[ordered]@{ok=$true}}catch{$e=$_.Exception;while($e.InnerException){$e=$e.InnerException};$result=[ordered]@{ok=$false;exception=$e.GetType().FullName;message=$e.Message;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})};if($e -is [Text.DecoderFallbackException]){$result.unknown=[int[]]$e.BytesUnknown;$result.index=$e.Index}}
 $result.bytesUsed=$cu;$result.charsUsed=$bu;$result.completed=$done;$result.remaining=$Decoder.FallbackBuffer.Remaining;return $result
}


function Operation-Call($Decoder,$Owner,[string]$Operation,[char[]]$Destination){
 [byte[]]$normal=if($Owner.CodePage -eq 1201){@(0,65,216,0)}else{@(65,0,0,216)}
 try{$n=switch($Operation){
 'Count' {$Decoder.GetCharCount($normal,0,$normal.Length,$true)}
 'CountEmpty' {$Decoder.GetCharCount([byte[]]@(),0,0,$true)}
 'Chars' {$Decoder.GetChars($normal,0,$normal.Length,$Destination,1,$true)}
 'CharsEmpty' {$Decoder.GetChars([byte[]]@(),0,0,$Destination,1,$true)}
 'Reset' {$Decoder.Reset();0}
 'SetEmpty' {$Decoder.Fallback=[Text.DecoderReplacementFallback]::new('');0}
 'SetCD' {$Decoder.Fallback=[Text.DecoderReplacementFallback]::new('CD');0}
 'SetStrict' {$Decoder.Fallback=[Text.DecoderFallback]::ExceptionFallback;0}
 'OwnerStrict' {$Owner.DecoderFallback=[Text.DecoderFallback]::ExceptionFallback;0}
 'BufferNext' {[int]$Decoder.FallbackBuffer.GetNextChar()}
 'BufferPrevious' {[int]$Decoder.FallbackBuffer.MovePrevious()}
 'BufferReset' {$Decoder.FallbackBuffer.Reset();0}
 'Prime' {$null=$Decoder.FallbackBuffer.Fallback([byte[]]@(255),0);0}
 'PrimeSetStrict' {$null=$Decoder.FallbackBuffer.Fallback([byte[]]@(255),0);$Decoder.Fallback=[Text.DecoderFallback]::ExceptionFallback;0}
 'PrimeCount' {$null=$Decoder.FallbackBuffer.Fallback([byte[]]@(255),0);$Decoder.GetCharCount($normal,0,$normal.Length,$true)}
 'PrimeChars' {$null=$Decoder.FallbackBuffer.Fallback([byte[]]@(255),0);$Decoder.GetChars($normal,0,$normal.Length,$Destination,1,$true)}
 };$r=[ordered]@{ok=$true;count=$n}}catch{$e=$_.Exception;while($e.InnerException){$e=$e.InnerException};$r=[ordered]@{ok=$false;exception=$e.GetType().FullName;hResult=$e.HResult;message=$e.Message;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})};if($e -is [Text.DecoderFallbackException]){$r.unknown=[int[]]$e.BytesUnknown;$r.index=$e.Index}}
 $r.remaining=$Decoder.FallbackBuffer.Remaining;return $r
}
function State-Of($Decoder,$Owner){return [ordered]@{fallbackType=$Decoder.Fallback.GetType().FullName;replacement=$(if($Decoder.Fallback -is [Text.DecoderReplacementFallback]){,[int[]][char[]]$Decoder.Fallback.DefaultString}else{$null});ownerType=$Owner.DecoderFallback.GetType().FullName;ownerReplacement=$(if($Owner.DecoderFallback -is [Text.DecoderReplacementFallback]){,[int[]][char[]]$Owner.DecoderFallback.DefaultString}else{$null});sharedOwner=[object]::ReferenceEquals($Decoder.Fallback,$Owner.DecoderFallback)}}
$configs=@();foreach($big in @($false,$true)){foreach($strict in @($false,$true)){$configs+=@([ordered]@{bigEndian=$big;strict=$strict;replacement=$null})};foreach($replacement in @(@(),@(67,68),@(0xd800,0xdc00))){$configs+=@([ordered]@{bigEndian=$big;strict=$false;replacement=[int[]]$replacement})}}
$operations=@('Count','CountEmpty','Chars','CharsEmpty','Reset','SetEmpty','SetCD','SetStrict','OwnerStrict','BufferNext','BufferPrevious','BufferReset','Prime','PrimeSetStrict','PrimeCount','PrimeChars');$profiles=[Collections.Generic.List[object]]::new()
foreach($config in $configs){
 $profileOwner=[Text.Encoding]([Text.UnicodeEncoding]::new([bool]$config.bigEndian,$true,[bool]$config.strict)).Clone();if($null -ne $config.replacement){$profileOwner.DecoderFallback=[Text.DecoderReplacementFallback]::new([string]::new([char[]][int[]]$config.replacement))};[int[]]$high=if($config.bigEndian){@(216,0)}else{@(0,216)};[int[]]$low=if($config.bigEndian){@(220,0)}else{@(0,220)};[int[]]$normal=if($config.bigEndian){@(0,65)}else{@(65,0)};$seeds=@(@(),@(65),@($high),@($high+@(0)));$inputs=@(@(),@(65),@($high),@($low),@($high+$low),@($low+$normal));$lastSource=[byte[]]@($low+$normal);$rows=[Collections.Generic.List[object]]::new()
 foreach($seedId in 0..($seeds.Count-1)){foreach($sourceId in 0..($inputs.Count-1)){foreach($flush in @($false,$true)){foreach($capacity in @(0,1,2,3)){foreach($operation in $operations){
  $owner=[Text.Encoding]$profileOwner.Clone();$decoder=$owner.GetDecoder();$seed=[byte[]][int[]]$seeds[$seedId];$seedAfter=[char[]](@(99)*8);$seedResult=Decoder-Call $decoder 'Chars' $seed 0 $seed.Length $seedAfter 0 $false;$source=[byte[]][int[]]$inputs[$sourceId];$dest=[char[]](@(99)*($capacity+4));$first=Convert-Call $decoder $source 0 $source.Length $dest 1 $capacity $flush
  $opDest=[char[]](@(99)*18);$result=Operation-Call $decoder $owner $operation $opDest;$state=State-Of $decoder $owner;$count=Operation-Call $decoder $owner 'CountEmpty' ([char[]]@());$tail=[char[]](@(99)*18);$write=Operation-Call $decoder $owner 'CharsEmpty' $tail
  $bufferResults=@();foreach($probe in @('BufferPrevious','BufferNext','BufferPrevious','BufferPrevious','BufferNext','BufferNext')){$bufferResults+=@([ordered]@{operation=$probe;result=(Operation-Call $decoder $owner $probe ([char[]]@()))})}
  $last=[char[]](@(99)*20);$lastResult=Convert-Call $decoder $lastSource 0 $lastSource.Length $last 1 16 $true
  $rows.Add([ordered]@{seedId=$seedId;sourceId=$sourceId;flush=$flush;capacity=$capacity;operation=$operation;seedResult=$seedResult;seedAfter=[int[]]$seedAfter;first=$first;after=[int[]]$dest;operationResult=$result;operationAfter=[int[]]$opDest;state=$state;countResult=$count;writeResult=$write;writeAfter=[int[]]$tail;bufferResults=$bufferResults;lastResult=$lastResult;lastAfter=[int[]]$last})
 }}}}}
 $profiles.Add([ordered]@{config=$config;seeds=$seeds;inputs=$inputs;normalInput=[int[]]@($normal+$high);lastInput=[int[]]$lastSource;rows=$rows.ToArray()})
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();operations=$operations;profiles=$profiles.ToArray();qualification='NATIVE_UNICODE_DECODER_INTERLEAVING_REFERENCE_ONLY; NO_JAVA_QUALIFICATION_OR_TASK_ACCEPTANCE'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 19 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS UTF16 decoder interleaving capture: $($profiles.Count) configurations"
