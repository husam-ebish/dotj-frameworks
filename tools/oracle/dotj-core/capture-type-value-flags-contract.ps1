param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Type flags reference requires pinned CoreLib.'}
$names=@('System.Object','System.ValueType','System.Enum','System.Void','System.String','System.Boolean','System.Char','System.SByte','System.Byte','System.Int16','System.UInt16','System.Int32','System.UInt32','System.Int64','System.UInt64','System.Single','System.Double','System.Decimal','System.DateTime','System.TimeSpan','System.DBNull','System.Diagnostics.Stopwatch','System.Runtime.Serialization.StreamingContext','System.Runtime.Serialization.StreamingContextStates','System.Collections.DictionaryEntry','System.Runtime.Serialization.SerializationEntry','System.Globalization.NumberFormatInfo','System.Runtime.Serialization.SerializationInfo','System.Runtime.Serialization.SerializationInfoEnumerator','System.Runtime.CompilerServices.NullableAttribute','System.IConvertible','System.Runtime.Serialization.ISerializable','System.Collections.Generic.List`1','System.Collections.Generic.Dictionary`2','System.ValueTuple`2','System.DayOfWeek','System.Globalization.TimeSpanStyles')
$rows=@();foreach($name in $names){
 $base=[Type]::GetType($name,$true)
 $kinds=@('direct','vector','pointer','byref');if($base.IsGenericTypeDefinition){$kinds+='genericParameter'}
 foreach($kind in $kinds){
  try{
   $type=switch($kind){direct {$base};vector {$base.MakeArrayType()};pointer {$base.MakePointerType()};byref {$base.MakeByRefType()};genericParameter {$base.GetGenericArguments()[0]}}
   $result=[ordered]@{name=$type.FullName;isSerializable=$type.IsSerializable;isSealed=$type.IsSealed;isValueType=$type.IsValueType;isPrimitive=$type.IsPrimitive;isEnum=$type.IsEnum;isClass=$type.IsClass;isAbstract=$type.IsAbstract;typeCode=[int][Type]::GetTypeCode($type)}
  }catch{$e=$_.Exception.GetBaseException();$result=[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult}}
  $rows+=[ordered]@{base=$name;kind=$kind;result=$result}
 }
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();queries=$rows;omittedNonCoreLibType='System.Runtime.Serialization.FormatterConverter';qualification='BOUNDED_SELECTED_TYPE_FLAGS_REFERENCE; SERIALIZATION_IMPLEMENTATION_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned core Type flags: $($rows.Count) cases"
