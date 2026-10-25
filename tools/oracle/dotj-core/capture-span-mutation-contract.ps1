param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum formatter requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
function New-Mutator([type]$Element,[bool]$Fill){
 $array=$Element.MakeArrayType();$definition=[type]'System.Span`1';$span=$definition.MakeGenericType([type[]]@($Element));$signature=[type[]]@($array,[int],[int],$Element);$bridge=[Reflection.Emit.DynamicMethod]::new('SelectedSpanMutation',[bool],$signature);$il=$bridge.GetILGenerator();$local=$il.DeclareLocal($span)
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_2);$il.Emit([Reflection.Emit.OpCodes]::Newobj,$span.GetConstructor([type[]]@($array,[int],[int])));$il.Emit([Reflection.Emit.OpCodes]::Stloc,$local);$il.Emit([Reflection.Emit.OpCodes]::Ldloca,$local)
 if($Fill){$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3);$method=$span.GetMethod('Fill',[type[]]@($Element))}else{$method=$span.GetMethod('Clear',[type[]]@())};$il.Emit([Reflection.Emit.OpCodes]::Call,$method);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_1);$il.Emit([Reflection.Emit.OpCodes]::Ret)
 $delegate=[type]'System.Func`5';return $bridge.CreateDelegate($delegate.MakeGenericType([type[]]@($signature+[bool])))
}
function Units([Array]$values){return ,([int[]]@(foreach($value in $values){[int]$value}))}
$seeds=[ordered]@{Char=[int[]]@(65,98,0,55357,56898,9731,65535,42,13,10,90,255);Byte=[int[]]@(0,1,127,128,255,42,13,10,64,65,254,3)};$rows=@()
foreach($encoding in @('Char','Byte')){foreach($fill in @($false,$true)){
 $element=if($encoding -eq 'Char'){[char]}else{[byte]};$mutate=New-Mutator $element $fill
 if(!$fill){$values=[int[]]@(0)}elseif($encoding -eq 'Char'){$values=[int[]]@(0,1,65,127,128,255,55357,56898,65535)}else{$values=[int[]]@(0,1,127,128,255)}
 foreach($offset in @(0,1,4,8,12)){foreach($length in @(0,1,3,4,8,12)){if($offset+$length -gt 12){continue};foreach($number in $values){
  if($encoding -eq 'Char'){$source=[char[]]$seeds.Char;$value=[char]$number}else{$source=[byte[]]$seeds.Byte;$value=[byte]$number}
  try{$result=[ordered]@{boolean=$mutate.Invoke($source,$offset,$length,$value)}}catch{$result=Failure $_}
  $rows+=[ordered]@{encoding=$encoding;fill=$fill;offset=$offset;length=$length;value=$number;sourceAfter=(Units $source);result=$result}
 }}}
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();seeds=$seeds;cases=$rows;qualification='BOUNDED_CHAR_BYTE_SPAN_CLEAR_FILL_REFERENCE; CLR_BYREF_LIFETIME_OTHER_ELEMENTS_MEMORY_CONCURRENCY_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned Span Clear/Fill: $($rows.Count) cases"
