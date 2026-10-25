param([Parameter(Mandatory)][string]$OutputPath,[string]$InputPath=(Join-Path $PSScriptRoot '../../../planning/stage-2/repos/dotj-core/evidence/utf8-array-ranges-contract-v10.0.12.json'))
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
$input=Get-Content -LiteralPath $InputPath -Raw -Encoding UTF8|ConvertFrom-Json;$rows=[Collections.Generic.List[object]]::new()
foreach($strict in @($false,$true)){$encoding=[Text.UTF8Encoding]::new($false,$strict)
foreach($op in 0..2){$sourceType=if($op -eq 0){[string]}elseif($op -eq 1){[char[]]}else{[byte[]]};$destinationType=if($op -eq 2){[char[]]}else{[byte[]]};[type[]]$signature=@($sourceType,[int],[int],$destinationType,[int]);$method=[Text.Encoding].GetMethod($(if($op -eq 2){'GetChars'}else{'GetBytes'}),$signature);$sources=if($op -eq 2){$input.byteInputs}else{$input.textInputs}
foreach($sourceId in -1..($sources.Count-1)){$units=$null;if($sourceId -ge 0){$units=[int[]]$sources[$sourceId]};$length=if($null -eq $units){0}else{$units.Count};$ranges=@(@(0,$length),@(1,([Math]::Max(0,$length-1))),@(-1,0),@(0,-1),@(($length+1),0),@(0,($length+1)))
foreach($range in $ranges){foreach($capacity in @(-1,0,1,2,3,4,8)){foreach($offset in @(-1,0,1,($capacity+1),2147483647)|Select-Object -Unique){
 $arguments=[object[]]::new(5);if($null -ne $units){if($op -eq 0){$arguments[0]=[string]::new([char[]]$units)}elseif($op -eq 1){$arguments[0]=[char[]]$units}else{$arguments[0]=[byte[]]$units}};$arguments[1]=[int]$range[0];$arguments[2]=[int]$range[1]
 $destination=$null;if($capacity -ge 0){if($op -eq 2){$destination=[char[]]::new($capacity)}else{$destination=[byte[]]::new($capacity)};for($i=0;$i -lt $capacity;$i++){$destination[$i]=99};$arguments[3]=$destination};$arguments[4]=[int]$offset
 try{$written=$method.Invoke($encoding,$arguments);$result=[ordered]@{ok=$true;written=[int]$written}}
 catch{$e=$_.Exception;while(($e -is [Management.Automation.RuntimeException] -or $e -is [Reflection.TargetInvocationException]) -and $null -ne $e.InnerException){$e=$e.InnerException};$result=[ordered]@{ok=$false;exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$e.ParamName};if($e -is [Text.EncoderFallbackException]){$result.index=$e.Index;$result.charUnknown=[int]$e.CharUnknown};if($e -is [Text.DecoderFallbackException]){$result.index=$e.Index;$result.bytesUnknown=[int[]]$e.BytesUnknown}}
 $rows.Add([ordered]@{strict=$strict;operation=$op;sourceId=$sourceId;index=$range[0];count=$range[1];capacity=$capacity;offset=$offset;result=$result;after=$(if($null -eq $destination){$null}else{,[int[]]$destination})})
}}}
}
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();inputSha256=(Get-FileHash -LiteralPath $InputPath -Algorithm SHA256).Hash.ToLowerInvariant();rows=$rows;qualification='SELECTED_STATELESS_DESTINATION_BUFFERS_ONLY; STATEFUL_SPAN_POINTER_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 11)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned UTF-8 destinations: $($rows.Count) rows"
