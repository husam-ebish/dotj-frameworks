param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Array shape oracle requires pinned CoreLib.'}
$elements=@(@{type=[Diagnostics.Stopwatch];base='System.Diagnostics.Stopwatch';carrier='direct'},@{type=[object];base='System.Object';carrier='direct'},
    @{type=[string];base='System.String';carrier='direct'},@{type=[DateTime];base='System.DateTime';carrier='direct'},@{type=[TimeSpan];base='System.TimeSpan';carrier='direct'},
    @{type=[int];base='System.Int32';carrier='direct'},@{type=[byte];base='System.Byte';carrier='direct'},@{type=[void];base='System.Void';carrier='direct'},
    @{type=[Diagnostics.Stopwatch].MakeByRefType();base='System.Diagnostics.Stopwatch';carrier='byRef'},
    @{type=[Diagnostics.Stopwatch].MakePointerType();base='System.Diagnostics.Stopwatch';carrier='pointer'},@{type=[void].MakePointerType();base='System.Void';carrier='pointer'})
$rows=@()
foreach($element in $elements){foreach($shape in @(@{vector=$true;rank=$null},@{vector=$false;rank=[int]::MinValue},@{vector=$false;rank=-1},@{vector=$false;rank=0},
    @{vector=$false;rank=1},@{vector=$false;rank=2},@{vector=$false;rank=3},@{vector=$false;rank=32},@{vector=$false;rank=33},@{vector=$false;rank=[int]::MaxValue})){
    try{
        $array=if($shape.vector){$element.type.MakeArrayType()}else{$element.type.MakeArrayType([int]$shape.rank)}
        $result=[ordered]@{name=$array.Name;fullName=$array.FullName;namespace=$array.Namespace;rank=$array.GetArrayRank();isSZArray=$array.IsSZArray
            isVariableBoundArray=$array.IsVariableBoundArray;isArray=$array.IsArray;isClass=$array.IsClass;isValueType=$array.IsValueType;isSealed=$array.IsSealed
            baseType=$array.BaseType.FullName;elementType=$array.GetElementType().FullName}
    }catch{$e=$_.Exception.GetBaseException();$result=[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult}}
    $rows+=[ordered]@{baseName=$element.base;carrier=$element.carrier;elementName=$element.type.FullName;vector=$shape.vector;rankArgument=$shape.rank;result=$result}
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash
    oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();cases=$rows
    qualification='SELECTED_ARRAY_FACTORY_AND_METADATA_REFERENCE; RUNTIME_RECTANGULAR_STORAGE_GENERIC_LANGUAGE_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned array shape reference: $($rows.Count) cases"
