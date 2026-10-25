param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum formatter requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
function New-Slicer([type]$Element,[bool]$ReadOnly,[bool]$Two){
 $array=$Element.MakeArrayType();$spanDefinition=[type]'System.Span`1';$span=$spanDefinition.MakeGenericType([type[]]@($Element));$definition=if($ReadOnly){[type]'System.ReadOnlySpan`1'}else{$spanDefinition};$sourceType=$definition.MakeGenericType([type[]]@($Element));$signature=[type[]]@($array,[int],[int],[int],[int],[int[]],$array)
 $bridge=[Reflection.Emit.DynamicMethod]::new('SelectedSpanSlice',[bool],$signature);$il=$bridge.GetILGenerator();$source=$il.DeclareLocal($sourceType);$slice=$il.DeclareLocal($sourceType)
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_2);$il.Emit([Reflection.Emit.OpCodes]::Newobj,$sourceType.GetConstructor([type[]]@($array,[int],[int])));$il.Emit([Reflection.Emit.OpCodes]::Stloc,$source)
 $il.Emit([Reflection.Emit.OpCodes]::Ldloca,$source);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3)
 if($Two){$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4);$parameters=[type[]]@([int],[int])}else{$parameters=[type[]]@([int])}
 $il.Emit([Reflection.Emit.OpCodes]::Call,$sourceType.GetMethod('Slice',$parameters));$il.Emit([Reflection.Emit.OpCodes]::Stloc,$slice)
 foreach($index in 0..1){$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]5);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4,$index);$il.Emit([Reflection.Emit.OpCodes]::Ldloca,$slice);$property=if($index -eq 0){'Length'}else{'IsEmpty'};$il.Emit([Reflection.Emit.OpCodes]::Call,$sourceType.GetProperty($property).GetMethod);$il.Emit([Reflection.Emit.OpCodes]::Stelem_I4)}
 $empty=$il.DefineLabel();$il.Emit([Reflection.Emit.OpCodes]::Ldloca,$slice);$il.Emit([Reflection.Emit.OpCodes]::Call,$sourceType.GetProperty('Length').GetMethod);$il.Emit([Reflection.Emit.OpCodes]::Brfalse,$empty)
 if($ReadOnly){$il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3);$il.Emit([Reflection.Emit.OpCodes]::Add);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4,123);$opcode=if($Element -eq [char]){[Reflection.Emit.OpCodes]::Stelem_I2}else{[Reflection.Emit.OpCodes]::Stelem_I1};$il.Emit($opcode)}
 else{$il.Emit([Reflection.Emit.OpCodes]::Ldloca,$slice);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0);$il.Emit([Reflection.Emit.OpCodes]::Call,$span.GetProperty('Item').GetMethod);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4,123);$opcode=if($Element -eq [char]){[Reflection.Emit.OpCodes]::Stind_I2}else{[Reflection.Emit.OpCodes]::Stind_I1};$il.Emit($opcode)}
 $il.MarkLabel($empty);$il.Emit([Reflection.Emit.OpCodes]::Ldloca,$slice);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]6);$il.Emit([Reflection.Emit.OpCodes]::Call,$span.GetMethod('op_Implicit',[type[]]@($array)));$il.Emit([Reflection.Emit.OpCodes]::Call,$sourceType.GetMethod('CopyTo',[type[]]@($span)));$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_1);$il.Emit([Reflection.Emit.OpCodes]::Ret)
 $delegate=[type]'System.Func`8';return $bridge.CreateDelegate($delegate.MakeGenericType([type[]]@($signature+[bool])))
}
function Units([Array]$values){return ,([int[]]@(foreach($value in $values){[int]$value}))}
$seeds=[ordered]@{Char=[int[]]@(65,98,0,55357,56898,9731,65535,42,13,10,90,255);Byte=[int[]]@(0,1,127,128,255,42,13,10,64,65,254,3)};$views=@();foreach($offset in @(0,1,4,8,12)){foreach($length in @(0,1,3,4,8,12)){if($offset+$length -le 12){$views+=@{offset=$offset;length=$length}}}}
$rows=@();foreach($encoding in @('Char','Byte')){foreach($readOnly in @($false,$true)){foreach($two in @($false,$true)){
 $element=if($encoding -eq 'Char'){[char]}else{[byte]};$probe=New-Slicer $element $readOnly $two
 foreach($view in $views){foreach($start in [int[]]@([int]::MinValue,-1,0,1,3,4,8,12,13,[int]::MaxValue)){
  if($two){$lengths=[int[]]@([int]::MinValue,-1,0,1,3,4,8,12,13,[int]::MaxValue)}else{$lengths=[int[]]@(-999)}
  foreach($length in $lengths){
   if($encoding -eq 'Char'){$source=[char[]]$seeds.Char;$output=[char[]]('#'*12)}else{$source=[byte[]]$seeds.Byte;$output=[byte[]]::new(12);[Array]::Fill($output,[byte]35)};$geometry=[int[]]@(99,99)
   try{$success=$probe.Invoke($source,$view.offset,$view.length,$start,$length,$geometry,$output);$result=[ordered]@{boolean=$success}}catch{$result=Failure $_}
   $rows+=[ordered]@{encoding=$encoding;readOnly=$readOnly;twoArguments=$two;baseOffset=$view.offset;baseLength=$view.length;start=$start;length=$length;geometry=$geometry;sourceAfter=(Units $source);output=(Units $output);result=$result}
  }
 }}
}}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();seeds=$seeds;cases=$rows;qualification='BOUNDED_CHAR_BYTE_SPAN_SLICE_REFERENCE; CLR_BYREF_LIFETIME_INDEXER_MEMORY_CONCURRENCY_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned Span slicing: $($rows.Count) cases"
