param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Element modifier oracle requires pinned CoreLib.'}
$rows=@()
foreach($base in @([Diagnostics.Stopwatch],[object],[string],[DateTime],[int],[void])){
    foreach($inputModifier in @('direct','array','byRef','pointer')){foreach($operation in @('byRef','pointer')){
        try{
            $inputType=switch($inputModifier){'direct'{$base};'array'{$base.MakeArrayType()};'byRef'{$base.MakeByRefType()};'pointer'{$base.MakePointerType()}}
            $type=if($operation -eq 'byRef'){$inputType.MakeByRefType()}else{$inputType.MakePointerType()}
            $result=[ordered]@{name=$type.Name;fullName=$type.FullName;namespace=$type.Namespace;elementName=$type.GetElementType().FullName
                baseName=$(if($null -eq $type.BaseType){$null}else{$type.BaseType.FullName});isClass=$type.IsClass;isValueType=$type.IsValueType;isInterface=$type.IsInterface
                isAbstract=$type.IsAbstract;isSealed=$type.IsSealed;isPrimitive=$type.IsPrimitive;isArray=$type.IsArray;isByRef=$type.IsByRef;isPointer=$type.IsPointer
                hasElementType=$type.HasElementType;typeCode=[int][Type]::GetTypeCode($type);assignableFromSelf=$type.IsAssignableFrom($type)
                assignableFromObject=$type.IsAssignableFrom([object]);assignableToObject=$type.IsAssignableTo([object]);subclassOfObject=$type.IsSubclassOf([object])
                instanceNull=$type.IsInstanceOfType($null);instanceObject=$type.IsInstanceOfType([object]::new())}
        }catch{$e=$_.Exception.GetBaseException();$result=[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult}}
        $rows+=[ordered]@{baseName=$base.FullName;inputModifier=$inputModifier;operation=$operation;result=$result}
    }}
}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();cases=$rows
    qualification='SELECTED_BYREF_POINTER_FACTORY_METADATA_REFERENCE; RAW_MEMORY_RUNTIME_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned element modifier reference: $($rows.Count) cases"
