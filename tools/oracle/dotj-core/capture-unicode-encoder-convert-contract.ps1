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
$inputs=@(@(),@(65),@(55296),@(56320),@(55296,56320),@(65,55296),@(55296,65),@(55296,55296),@(56320,65),@(55296,56320,65),@(55296,56320,55296),@(0,65),@(55296,55296,56320),@(2047),@(2048),@(65535),@(56319,57343));$profiles=[Collections.Generic.List[object]]::new()
foreach($config in $configs){
 $encoding=[Text.Encoding]([Text.UnicodeEncoding]::new([bool]$config.bigEndian,$true,[bool]$config.strict)).Clone();if($null -ne $config.replacement){$encoding.EncoderFallback=[Text.EncoderReplacementFallback]::new([string]::new([char[]][int[]]$config.replacement))}
 $rows=[Collections.Generic.List[object]]::new()
 foreach($pending in @($false,$true)){foreach($sourceId in 0..($inputs.Count-1)){$units=$inputs[$sourceId];foreach($flush in @($false,$true)){foreach($capacity in @(0,1,2,3,4,5,6,8)){foreach($offset in @(0,2)){
  $encoder=$encoding.GetEncoder();if($pending){$seed=Encoder-Call $encoder 'Bytes' ([char[]]@(55296)) 0 1 ([byte[]]@()) 0 $false;if(-not $seed.ok -or $seed.count -ne 0){throw 'Pending seed failed'}}
  $source=[char[]](@(56320)+$units+@(55296));$dest=[byte[]](@(99)*($offset+$capacity+3));$first=Convert-Call $encoder $source 1 $units.Length $dest $offset $capacity $flush
  $used=if($first.ok){[int]$first.charsUsed}else{0};$next=[byte[]](@(99)*32);$second=Convert-Call $encoder $source (1+$used) ($units.Length-$used) $next 0 32 $true
  $tail=[byte[]](@(99)*16);$third=Convert-Call $encoder ([char[]]@()) 0 0 $tail 0 16 $true
  $rows.Add([ordered]@{pending=$pending;sourceId=$sourceId;flush=$flush;capacity=$capacity;offset=$offset;first=$first;after=[int[]]$dest;second=$second;secondAfter=[int[]]$next;third=$third;thirdAfter=[int[]]$tail})
 }}}}}
 $guards=[Collections.Generic.List[object]]::new();$specs=@(@(0,1,0,8),@(-1,1,0,8),@(0,-1,0,8),@(0,1,-1,8),@(0,1,0,-1),@(2,1,0,8),@(0,2,0,8),@(0,1,9,0),@(0,1,1,8),@(2147483647,1,0,8),@(0,2147483647,0,8),@(0,1,2147483647,0),@(0,1,0,2147483647))
 foreach($nullSource in @($false,$true)){foreach($nullDest in @($false,$true)){foreach($g in $specs){$src=[char[]]@(65);$dst=[byte[]](@(99)*8);if($nullSource){$src=$null};if($nullDest){$dst=$null};$r=Convert-Call ($encoding.GetEncoder()) $src $g[0] $g[1] $dst $g[2] $g[3] $true;$guards.Add([ordered]@{nullSource=$nullSource;nullDestination=$nullDest;charIndex=$g[0];charCount=$g[1];byteIndex=$g[2];byteCount=$g[3];result=$r;after=$(if($nullDest){$null}else{[int[]]$dst})})}}}
 $profiles.Add([ordered]@{config=$config;rows=$rows.ToArray();guards=$guards.ToArray()})
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();inputs=$inputs;profiles=$profiles.ToArray();qualification='NATIVE_UNICODE_ENCODER_ARRAY_CONVERT_REFERENCE_ONLY; NO_JAVA_CONVERT_QUALIFICATION_OR_TASK_ACCEPTANCE'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 19 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS UTF16 encoder Convert capture: $($profiles.Count) configurations"
