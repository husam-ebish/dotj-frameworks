param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum formatter requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
function New-Copier([type]$Element,[bool]$ReadOnly,[bool]$Try){
 $array=$Element.MakeArrayType();$spanDefinition=[type]'System.Span`1';$span=$spanDefinition.MakeGenericType([type[]]@($Element));if($ReadOnly){$sourceDefinition=[type]'System.ReadOnlySpan`1';$sourceType=$sourceDefinition.MakeGenericType([type[]]@($Element))}else{$sourceType=$span}
 $signature=[type[]]@($array,[int],[int],$array,[int],[int],[int[]]);$bridge=[Reflection.Emit.DynamicMethod]::new('SelectedSpanCopy',[bool],$signature);$il=$bridge.GetILGenerator();$source=$il.DeclareLocal($sourceType);$destination=$il.DeclareLocal($span)
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_2);$il.Emit([Reflection.Emit.OpCodes]::Newobj,$sourceType.GetConstructor([type[]]@($array,[int],[int])));$il.Emit([Reflection.Emit.OpCodes]::Stloc,$source)
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_3);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]5);$il.Emit([Reflection.Emit.OpCodes]::Newobj,$span.GetConstructor([type[]]@($array,[int],[int])));$il.Emit([Reflection.Emit.OpCodes]::Stloc,$destination)
 foreach($index in 0..3){$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]6);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4,$index)
  if($index -in @(0,2)){$local=$source;$type=$sourceType}else{$local=$destination;$type=$span}
  $property=if($index -lt 2){'Length'}else{'IsEmpty'};$il.Emit([Reflection.Emit.OpCodes]::Ldloca,$local);$il.Emit([Reflection.Emit.OpCodes]::Call,$type.GetProperty($property).GetMethod);$il.Emit([Reflection.Emit.OpCodes]::Stelem_I4)
 }
 $name=if($Try){'TryCopyTo'}else{'CopyTo'};$il.Emit([Reflection.Emit.OpCodes]::Ldloca,$source);$il.Emit([Reflection.Emit.OpCodes]::Ldloc,$destination);$il.Emit([Reflection.Emit.OpCodes]::Call,$sourceType.GetMethod($name,[type[]]@($span)))
 if(!$Try){$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_1)};$il.Emit([Reflection.Emit.OpCodes]::Ret)
 $delegateDefinition=[type]'System.Func`8';return $bridge.CreateDelegate($delegateDefinition.MakeGenericType([type[]]@($signature+[bool])))
}
function Units([Array]$values){return ,([int[]]@(foreach($value in $values){[int]$value}))}
$seeds=[ordered]@{Char=[int[]]@(65,98,0,55357,56898,9731,65535,42,13,10,90,255);Byte=[int[]]@(0,1,127,128,255,42,13,10,64,65,254,3)}
$views=@();foreach($offset in @(0,1,4,8,12)){foreach($length in @(0,1,3,4,8,12)){if($offset+$length -le 12){$views+=@{offset=$offset;length=$length}}}}
$rows=@();foreach($encoding in @('Char','Byte')){foreach($readOnly in @($false,$true)){foreach($try in @($false,$true)){
 $element=if($encoding -eq 'Char'){[char]}else{[byte]};$copy=New-Copier $element $readOnly $try
 foreach($from in $views){foreach($to in $views){foreach($alias in @($false,$true)){
  if($encoding -eq 'Char'){$source=[char[]]$seeds.Char;$initial=[char[]]('#'*12)}else{$source=[byte[]]$seeds.Byte;$initial=[byte[]]::new(12);[Array]::Fill($initial,[byte]35)}
  if($alias){$destination=$source}else{$destination=$initial}
  $geometry=[int[]]@(99,99,99,99)
  try{$success=$copy.Invoke($source,$from.offset,$from.length,$destination,$to.offset,$to.length,$geometry);$result=[ordered]@{boolean=$success}}catch{$result=Failure $_}
  $rows+=[ordered]@{encoding=$encoding;readOnly=$readOnly;try=$try;sourceOffset=$from.offset;sourceLength=$from.length;destinationOffset=$to.offset;destinationLength=$to.length;alias=$alias;geometry=$geometry;sourceAfter=(Units $source);destinationAfter=(Units $destination);result=$result}
 }}}
}}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();seeds=$seeds;cases=$rows;qualification='BOUNDED_CHAR_BYTE_SPAN_COPY_REFERENCE; CLR_BYREF_LIFETIME_MEMORY_CONCURRENCY_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned Span copying: $($rows.Count) cases"
