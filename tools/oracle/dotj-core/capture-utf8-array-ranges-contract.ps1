param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
$texts=@(@(),@(65),@(65,66,67),@(0,0x7ff,0x800),@(0xd800),@(0xdc00),@(65,0xd800,0xdc00,90),@(65,0xd800,66),@(65,0xdc00,66),@(0xd800,0xd800,0xdc00),@(0xdbff,0xdfff),@(0xdfff,0xd800,65))
$buffers=@(@(),@(65),@(65,66,67),@(0),@(0xc2,0x80),@(0xe0,0xa0,0x80),@(0xed,0x9f,0xbf),@(0xed,0xa0,0x80),@(0xf0,0x90,0x80,0x80),@(0xf4,0x8f,0xbf,0xbf),@(0xf4,0x90,0x80,0x80),@(0xef,0xbb,0xbf),@(0xff),@(65,0xe2,0x82,0xac,90),@(65,0xe2,0x82,90),@(65,0xf0,0x90,0x80),@(0xc0,0x80),@(0x80,0xbf),@(0xe0,0x80,0x80),@(0xf0,0x80,0x80,0x80))
$rows=[Collections.Generic.List[object]]::new()
foreach($strict in @($false,$true)){$encoding=[Text.UTF8Encoding]::new($false,$strict)
foreach($operation in @('GetBytesString','GetByteCountString','GetBytesChars','GetByteCountChars','GetStringBytes','GetCharsBytes','GetCharCountBytes')){
 $isBytes=$operation.EndsWith('Bytes');$isString=$operation.EndsWith('String');$name=$operation.Replace('String','').Replace('Chars','').Replace('Bytes','');if($operation.StartsWith('GetBytes')){$name='GetBytes'}elseif($operation.StartsWith('GetByteCount')){$name='GetByteCount'}elseif($operation.StartsWith('GetChars')){$name='GetChars'}elseif($operation.StartsWith('GetCharCount')){$name='GetCharCount'}else{$name='GetString'}
 $sourceType=if($isBytes){[byte[]]}elseif($isString){[string]}else{[char[]]};[type[]]$signature=@($sourceType,[int],[int]);$method=[Text.Encoding].GetMethod($name,$signature)
 $sources=if($isBytes){$buffers}else{$texts}
 foreach($sourceId in -1..($sources.Count-1)){
  $units=$null;if($sourceId -ge 0){$units=[int[]]$sources[$sourceId]};$length=if($null -eq $units){0}else{$units.Count}
  $indices=@(-2147483648,-1,0,1,2,$length,($length+1),2147483647)|Select-Object -Unique
  $counts=@(-2147483648,-1,0,1,2,$length,($length+1),2147483647)|Select-Object -Unique
  foreach($index in $indices){foreach($count in $counts){
   $arguments=[object[]]::new(3);if($null -ne $units){if($isBytes){$arguments[0]=[byte[]]$units}elseif($isString){$arguments[0]=[string]::new([char[]]$units)}else{$arguments[0]=[char[]]$units}};$arguments[1]=[int]$index;$arguments[2]=[int]$count
   try{$value=$method.Invoke($encoding,$arguments);$result=[ordered]@{ok=$true};if($value -is [byte[]] -or $value -is [char[]]){$result.units=[int[]]$value}elseif($value -is [string]){$result.units=[int[]][char[]]$value}else{$result.count=[int]$value}}
   catch{$e=$_.Exception;while(($e -is [Management.Automation.RuntimeException] -or $e -is [Reflection.TargetInvocationException]) -and $null -ne $e.InnerException){$e=$e.InnerException};$result=[ordered]@{ok=$false;exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$e.ParamName};if($e -is [Text.EncoderFallbackException]){$result.index=$e.Index;$result.charUnknown=[int]$e.CharUnknown};if($e -is [Text.DecoderFallbackException]){$result.index=$e.Index;$result.bytesUnknown=[int[]]$e.BytesUnknown}}
   $rows.Add([ordered]@{strict=$strict;operation=$operation;sourceId=$sourceId;index=$index;count=$count;result=$result})
  }}
 }
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();textInputs=$texts;byteInputs=$buffers;rows=$rows;qualification='SELECTED_STATELESS_ARRAY_RANGES_ONLY; BUFFER_STATEFUL_SPAN_POINTER_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 11)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned UTF-8 array ranges: $($rows.Count) rows"
