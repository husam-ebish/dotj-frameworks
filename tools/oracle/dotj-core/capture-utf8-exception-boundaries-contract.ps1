param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentUICulture=[Globalization.CultureInfo]::InvariantCulture
function Record($e){$r=[ordered]@{exception=$e.GetType().FullName;message=$e.Message;hResult=$e.HResult;paramName=$e.ParamName;innerMessage=$(if($null -eq $e.InnerException){$null}else{$e.InnerException.Message})};if($e -is [Text.EncoderFallbackException]){$r.index=$e.Index;$r.charUnknown=[int]$e.CharUnknown;$r.charUnknownHigh=[int]$e.CharUnknownHigh;$r.charUnknownLow=[int]$e.CharUnknownLow;$r.isUnknownSurrogate=$e.IsUnknownSurrogate()};if($e -is [Text.DecoderFallbackException]){$r.index=$e.Index;$r.bytesUnknown=$(if($null -eq $e.BytesUnknown){$null}else{,[int[]]$e.BytesUnknown})};return $r}
$constructors=@()
foreach($direction in @('Encoder','Decoder')){foreach($kind in @('default','null-message','empty-message','message','inner')){
 $type=[type]("System.Text.${direction}FallbackException");$inner=[Exception]::new('inner payload')
 $e=switch($kind){'default'{[Activator]::CreateInstance($type)}'null-message'{$arguments=[object[]]::new(1);[Activator]::CreateInstance($type,$arguments)}'empty-message'{[Activator]::CreateInstance($type,[object[]]@(''))}'message'{[Activator]::CreateInstance($type,[object[]]@('custom payload'))}'inner'{[Activator]::CreateInstance($type,[object[]]@('custom payload',$inner))}}
 $constructors+=[ordered]@{direction=$direction;kind=$kind;result=(Record $e)}
}}
foreach($index in @(-7,0,3,2147483647)){foreach($isNull in @($false,$true)){[byte[]]$bytes=if($isNull){$null}else{[byte[]]@(128,255)};$e=[Text.DecoderFallbackException]::new('custom payload',$bytes,$index);$constructors+=[ordered]@{direction='Decoder';kind='bytes-index';index=$index;nullBytes=$isNull;preservesReference=[object]::ReferenceEquals($bytes,$e.BytesUnknown);result=(Record $e)}}}
$nulls=@()
foreach($strict in @($false,$true)){$encoding=[Text.UTF8Encoding]::new($false,$strict);foreach($name in @('GetBytes','GetByteCount','GetChars','GetCharCount','GetString')){
 [type[]]$signature=if($name -in @('GetBytes','GetByteCount')){@([string])}else{@([byte[]])};$method=[Text.Encoding].GetMethod($name,$signature);$arguments=[object[]]::new(1)
 try{[void]$method.Invoke($encoding,$arguments);throw 'Expected null rejection'}catch{$e=$_.Exception;while(($e -is [Management.Automation.RuntimeException] -or $e -is [Reflection.TargetInvocationException]) -and $null -ne $e.InnerException){$e=$e.InnerException};$nulls+=[ordered]@{strict=$strict;method=$name;result=(Record $e)}}
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();constructors=$constructors;nullControls=$nulls;qualification='SELECTED_EXCEPTION_CONSTRUCTOR_AND_NULL_BOUNDARIES_ONLY; RANGE_STATEFUL_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 10)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned UTF-8 boundaries: $($constructors.Count) constructors and $($nulls.Count) null controls"
