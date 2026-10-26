param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Enum formatter requires pinned CoreLib.'}
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;message=$e.Message;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$assembly=[Reflection.Emit.AssemblyBuilder]::DefineDynamicAssembly([Reflection.AssemblyName]::new('IgnoredEnumProvider'),[Reflection.Emit.AssemblyBuilderAccess]::Run)
$builder=$assembly.DefineDynamicModule('Main').DefineType('IgnoredProvider',[Reflection.TypeAttributes]'Public,Sealed');$builder.AddInterfaceImplementation([IFormatProvider]);$builder.DefineDefaultConstructor([Reflection.MethodAttributes]::Public)|Out-Null
$method=$builder.DefineMethod('GetFormat',[Reflection.MethodAttributes]'Public,Virtual,Final,HideBySig,NewSlot',[object],[type[]]@([type]));$il=$method.GetILGenerator();$il.Emit([Reflection.Emit.OpCodes]::Ldstr,'Provider must be ignored');$il.Emit([Reflection.Emit.OpCodes]::Newobj,[InvalidOperationException].GetConstructor([type[]]@([string])));$il.Emit([Reflection.Emit.OpCodes]::Throw);$builder.DefineMethodOverride($method,[IFormatProvider].GetMethod('GetFormat'))
$provider=[Activator]::CreateInstance($builder.CreateType());$enumType=[Globalization.DigitShapes]

function New-EnumFormatter(){
 $span=[type]'System.Span[char]';$bridge=[Reflection.Emit.DynamicMethod]::new('EnumSliceTryFormat',[bool],[type[]]@([object],[char[]],[int],[int],[int[]],[string],[IFormatProvider]));$il=$bridge.GetILGenerator()
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_0);$il.Emit([Reflection.Emit.OpCodes]::Castclass,[ISpanFormattable]);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_1);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_2);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_3);$il.Emit([Reflection.Emit.OpCodes]::Newobj,$span.GetConstructor([type[]]@([char[]],[int],[int])))
 $il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]4);$il.Emit([Reflection.Emit.OpCodes]::Ldc_I4_0);$il.Emit([Reflection.Emit.OpCodes]::Ldelema,[int]);$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]5);$il.Emit([Reflection.Emit.OpCodes]::Call,[MemoryExtensions].GetMethod('AsSpan',[type[]]@([string])));$il.Emit([Reflection.Emit.OpCodes]::Ldarg_S,[byte]6);$il.Emit([Reflection.Emit.OpCodes]::Callvirt,[ISpanFormattable].GetMethod('TryFormat'));$il.Emit([Reflection.Emit.OpCodes]::Ret)
 return $bridge.CreateDelegate([Func[object,char[],int,int,int[],string,IFormatProvider,bool]])
}
$formatter=New-EnumFormatter;$single=[Enum].GetMethod('ToString',[type[]]@([string]));$buffers=[Collections.Generic.List[object]]::new()
foreach($number in [int[]]@([int]::MinValue,-1,0,1,2,3,4,5,6,7,8,9,10,[int]::MaxValue)){$boxed=[Enum]::ToObject($enumType,$number)
 foreach($format in @($null,'','G','g','F','f','D','d','X','x','?','GG','G ')){$arguments=[object[]]::new(1);$arguments[0]=$format
  try{$text=$single.Invoke($boxed,$arguments);$length=$text.Length;$capacities=@(0,1,[Math]::Max(0,$length-1),$length,($length+1))|Sort-Object -Unique}catch{$capacities=@(0,1,3,7,32)}
  foreach($capacity in $capacities){foreach($route in @('array','span')){$offset=if($route -eq 'array'){0}else{2};$suffix=if($route -eq 'array'){0}else{3};$buffer=[char[]]('#'*($capacity+$offset+$suffix));$written=[int[]]@(99)
   try{$success=$formatter.Invoke($boxed,$buffer,$offset,$capacity,$written,$format,$provider);$result=[ordered]@{boolean=$success}}catch{$result=Failure $_}
   $buffers.Add([ordered]@{value=$number;format=$format;route=$route;capacity=$capacity;offset=$offset;suffix=$suffix;written=$written[0];buffer=[string]::new($buffer);result=$result})
  }}
 }
}
$numbers=[int[]]@([int]::MinValue,([int]::MinValue+1),-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,15,16,255,256,65535,[int]::MaxValue);$rows=[Collections.Generic.List[object]]::new();$controls=[Collections.Generic.List[object]]::new()
foreach($number in $numbers){$value=[Enum]::ToObject([Globalization.DigitShapes],$number);foreach($flag in $numbers){$other=[Enum]::ToObject([Globalization.DigitShapes],$flag);$rows.Add([ordered]@{value=$number;flag=$flag;result=$value.HasFlag($other)})};foreach($kind in @('null','day','date')){$other=switch($kind){'null'{$null}'day'{[DayOfWeek]::Monday}'date'{[DateTimeKind]::Utc}};$result=$null;$failure=$null;try{$result=$value.HasFlag($other)}catch{$e=$_.Exception;while($e.InnerException){$e=$e.InnerException};$failure=[ordered]@{type=$e.GetType().FullName;message=$e.Message;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}};$controls.Add([ordered]@{value=$number;kind=$kind;result=$result;failure=$failure})}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();enumType=$enumType.FullName;interfaces=@($enumType.GetInterfaces()|ForEach-Object FullName);providerThrowsIfQueried=$true;utf8Assignable=[IUtf8SpanFormattable].IsAssignableFrom($enumType);buffers=$buffers.ToArray();rows=$rows.ToArray();controls=$controls.ToArray();isFlagsEnum=($enumType.GetCustomAttributes([FlagsAttribute],$false).Length -ne 0);qualification='SELECTED_DIGITSHAPES_CHAR_BUFFERS_AND_HASFLAG_ONLY; BYREF_LIFETIME_UTF8_FULL_ENUM_ABI_AND_TASK_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15 -Compress)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS DigitShapes Char formatting capture: $($buffers.Count) buffers"
