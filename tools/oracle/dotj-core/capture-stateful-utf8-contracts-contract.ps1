param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
$types=@();foreach($type in @([Text.Encoder],[Text.Decoder])){
 $methods=@($type.GetMethods([Reflection.BindingFlags]'Public,Instance,DeclaredOnly')|Sort-Object Name,@{Expression={$_.ToString()}}|ForEach-Object {[ordered]@{name=$_.Name;returnType=$_.ReturnType.ToString();isAbstract=$_.IsAbstract;isVirtual=$_.IsVirtual;parameters=@($_.GetParameters()|ForEach-Object {[ordered]@{name=$_.Name;type=$_.ParameterType.ToString();isOut=$_.IsOut}})}})
 $types+=[ordered]@{fullName=$type.FullName;baseType=$type.BaseType.FullName;isAbstract=$type.IsAbstract;isSerializable=$type.IsSerializable;constructors=@($type.GetConstructors([Reflection.BindingFlags]'Instance,Public,NonPublic')|ForEach-Object {[ordered]@{isPublic=$_.IsPublic;isFamily=$_.IsFamily;parameters=@($_.GetParameters()|ForEach-Object {$_.ParameterType.ToString()})}});methods=$methods}
}
function Action([string]$Operation,[int[]]$Units=@(),[bool]$Flush=$false){return [ordered]@{operation=$Operation;units=$Units;flush=$Flush}}
$encoderSequences=@(
 @((Action Bytes @(0xd800)),(Action Bytes @(0xdc00)),(Action Bytes @() $true),(Action Bytes @(65) $true)),
 @((Action Count @(0xd800)),(Action Bytes @(0xdc00)),(Action Bytes @() $true)),
 @((Action Bytes @(0xd800)),(Action Count @() $true),(Action Bytes @(0xdc00)),(Action Bytes @() $true)),
 @((Action Bytes @(0xd800,0xdc00)),(Action Count @() $true)),
 @((Action Bytes @(0xd800)),(Action Reset),(Action Bytes @(0xdc00) $true)),
 @((Action Bytes @(0xd800)),(Action Replace @(65,66)),(Action Bytes @(0xdc00) $true)),
 @((Action Bytes @(0xdc00) $true),(Action Bytes @(65) $true)),
 @((Action Bytes @(0xd800)),(Action Bytes @(0xd800)),(Action Bytes @(0xdc00) $true)),
 @((Action Bytes @(0xd800)),(Action Bytes @() $true),(Action Bytes @(0xdc00) $true)),
 @((Action Count @(0xd800,0xdc00) $true),(Action Bytes @(0xd800,0xdc00) $true))
)
$decoderSequences=@(
 @((Action Chars @(240)),(Action Chars @(144)),(Action Chars @(128)),(Action Chars @(128)),(Action Chars @() $true)),
 @((Action Count @(240,144)),(Action Chars @(128,128)),(Action Chars @() $true)),
 @((Action Chars @(240,144)),(Action Count @() $true),(Action Chars @(128,128)),(Action Chars @() $true)),
 @((Action Chars @(240,144,128,128)),(Action Count @() $true)),
 @((Action Chars @(226,130)),(Action Reset),(Action Chars @(172) $true)),
 @((Action Chars @(226,130)),(Action Replace @(65,66)),(Action Chars @(172) $true)),
 @((Action Chars @(255) $true),(Action Chars @(65) $true)),
 @((Action Chars @(226)),(Action Chars @(226,130)),(Action Chars @(172) $true)),
 @((Action Chars @(240,144)),(Action Chars @() $true),(Action Chars @(128,128) $true)),
 @((Action Count @(240,144,128,128) $true),(Action Chars @(240,144,128,128) $true))
)
$profiles=@();foreach($emit in @($false,$true)){foreach($strict in @($false,$true)){foreach($direction in @('Encoder','Decoder')){
 $encoding=[Text.UTF8Encoding]::new($emit,$strict);$instance=if($direction -eq 'Encoder'){$encoding.GetEncoder()}else{$encoding.GetDecoder()};$again=if($direction -eq 'Encoder'){$encoding.GetEncoder()}else{$encoding.GetDecoder()};$initialFallback=if($direction -eq 'Encoder'){$encoding.EncoderFallback}else{$encoding.DecoderFallback};$sequences=if($direction -eq 'Encoder'){$encoderSequences}else{$decoderSequences};$observations=@()
 foreach($sequenceId in 0..($sequences.Count-1)){$state=if($direction -eq 'Encoder'){$encoding.GetEncoder()}else{$encoding.GetDecoder()};$rows=@();foreach($action in $sequences[$sequenceId]){
  $destination=$null;try{switch($action.operation){
   'Reset'{$state.Reset();$result=[ordered]@{ok=$true}}
   'Replace'{$replacement=[string]::new([char[]][int[]]$action.units);$state.Fallback=if($direction -eq 'Encoder'){[Text.EncoderReplacementFallback]::new($replacement)}else{[Text.DecoderReplacementFallback]::new($replacement)};$result=[ordered]@{ok=$true;maximum=$state.Fallback.MaxCharCount}}
   'Count'{if($direction -eq 'Encoder'){$units=[char[]][int[]]$action.units;$count=$state.GetByteCount($units,0,$units.Length,[bool]$action.flush)}else{$units=[byte[]][int[]]$action.units;$count=$state.GetCharCount($units,0,$units.Length,[bool]$action.flush)};$result=[ordered]@{ok=$true;count=$count}}
   'Bytes'{$units=[char[]][int[]]$action.units;$destination=[byte[]]::new(64);[Array]::Fill[byte]($destination,99);$count=$state.GetBytes($units,0,$units.Length,$destination,1,[bool]$action.flush);$result=[ordered]@{ok=$true;count=$count}}
   'Chars'{$units=[byte[]][int[]]$action.units;$destination=[char[]]::new(64);[Array]::Fill[char]($destination,[char]99);$count=$state.GetChars($units,0,$units.Length,$destination,1,[bool]$action.flush);$result=[ordered]@{ok=$true;count=$count}}
  }}catch{$e=$_.Exception;while(($e -is [Management.Automation.RuntimeException] -or $e -is [Reflection.TargetInvocationException]) -and $null -ne $e.InnerException){$e=$e.InnerException};$result=[ordered]@{ok=$false;exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})};if($e -is [Text.EncoderFallbackException]){$result.unknown=[int]$e.CharUnknown;$result.index=$e.Index}elseif($e -is [Text.DecoderFallbackException]){$result.unknownBytes=[int[]]$e.BytesUnknown;$result.index=$e.Index}}
  $rows+=[ordered]@{action=$action;result=$result;after=$(if($null -eq $destination){$null}else{,[int[]]$destination})}
 };$observations+=[ordered]@{sequence=$sequenceId;rows=$rows}}
 $profiles+=[ordered]@{emit=$emit;strict=$strict;direction=$direction;runtimeType=$instance.GetType().FullName;fallbackType=$instance.Fallback.GetType().FullName;freshInstances=-not [object]::ReferenceEquals($instance,$again);fallbackSharedWithEncoding=[object]::ReferenceEquals($initialFallback,$instance.Fallback);sequences=$observations}
}}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();types=$types;profiles=$profiles;qualification='PINNED_STATEFUL_UTF8_BASELINE_ONLY; NO_CANDIDATE_STATEFUL_BEHAVIOR_SOURCE_ABI_OR_TASK_ACCEPTANCE'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false));Write-Output 'PASS pinned stateful UTF-8 baseline: two abstract declarations, eight profiles and eighty sequences'
