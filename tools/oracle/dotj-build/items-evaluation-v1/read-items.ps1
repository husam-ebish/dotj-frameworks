param([Parameter(Mandatory)][string]$ImplementationRoot)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
# Only the reader dependency executes. All reference assemblies are opened in
# MetadataLoadContext, which cannot invoke constructors, methods or getters.
$sdk = Join-Path $ImplementationRoot 'toolchains/dotnet/sdk/10.0.401'
$runtime = Join-Path $ImplementationRoot 'toolchains/dotnet/shared/Microsoft.NETCore.App/10.0.12'
Add-Type -Path (Join-Path $sdk 'System.Reflection.MetadataLoadContext.dll')
$paths = @((Get-ChildItem -LiteralPath $runtime -Filter '*.dll').FullName) + @(
    (Join-Path $sdk 'Microsoft.Build.dll'), (Join-Path $sdk 'Microsoft.Build.Framework.dll'))
$resolver = [System.Reflection.PathAssemblyResolver]::new([string[]]$paths)
$context = [System.Reflection.MetadataLoadContext]::new($resolver, 'System.Private.CoreLib')
$script:contracts = [System.Collections.Generic.SortedDictionary[string,object]]::new([System.StringComparer]::Ordinal)
function Type-Identity([System.Type]$t) {
    if ($null -eq $t) { return $null }
    return $t.AssemblyQualifiedName
}
function Remember-Type([System.Type]$t) {
    if ($null -eq $t) { return }
    if ($t.HasElementType) { Remember-Type $t.GetElementType(); return }
    if ($t.IsGenericParameter) { return }
    $definition = if ($t.IsGenericType) { $t.GetGenericTypeDefinition() } else { $t }
    $key = Type-Identity $definition
    if (-not $script:contracts.ContainsKey($key)) {
        $script:contracts[$key] = [ordered]@{
            identity=$key; fullName=$definition.FullName; assembly=$definition.Assembly.FullName
            assemblyPath=$definition.Assembly.Location; visibility=$definition.Attributes.ToString(); public=$definition.IsVisible
            kind=$(if ($definition.IsInterface) {'interface'} elseif ($definition.IsEnum) {'enum'} elseif ($definition.IsValueType) {'valueType'} else {'class'})
            baseType=(Type-Identity $definition.BaseType)
            interfaces=@($definition.GetInterfaces() | ForEach-Object { Type-Identity $_ } | Sort-Object -CaseSensitive)
            genericParameters=@(Generic-Parameters $definition)
            customAttributes=@($definition.GetCustomAttributesData() | ForEach-Object {$_.ToString()})
            enumUnderlyingType=$(if ($definition.IsEnum) {Type-Identity ($definition.GetEnumUnderlyingType())} else {$null})
            enumConstants=@(if ($definition.IsEnum) {
                $definition.GetFields([System.Reflection.BindingFlags]'Public,Static,DeclaredOnly') | Sort-Object MetadataToken | ForEach-Object {
                    [ordered]@{name=$_.Name; metadataToken=$_.MetadataToken; value=$_.GetRawConstantValue(); attributes=$_.Attributes.ToString()}
                }
            })
        }
    }
    if ($t.IsGenericType) { foreach ($argument in $t.GetGenericArguments()) { Remember-Type $argument } }
}
function Generic-Parameters($owner) {
    if ($owner -is [System.Type]) { $arguments = $owner.GetGenericArguments() }
    elseif ($owner.IsGenericMethod) { $arguments = $owner.GetGenericArguments() }
    else { $arguments = @() }
    foreach ($t in $arguments) {
        if ($t.IsGenericParameter) {
            [ordered]@{name=$t.Name; position=$t.GenericParameterPosition; attributes=$t.GenericParameterAttributes.ToString()
                constraints=@($t.GetGenericParameterConstraints() | ForEach-Object { Type-Identity $_ })}
        }
    }
}
function Parameter-Shape([System.Reflection.ParameterInfo]$p) {
    Remember-Type $p.ParameterType
    $default = $null
    if ($p.HasDefaultValue) {
        $value = $p.RawDefaultValue
        $default = [ordered]@{kind=$(if ($null -eq $value) {'null'} else {$value.GetType().FullName}); value=$value}
    }
    [ordered]@{name=$p.Name; position=$p.Position; type=(Type-Identity $p.ParameterType)
        displayType=$p.ParameterType.ToString(); attributes=$p.Attributes.ToString()
        byRef=$p.ParameterType.IsByRef; isIn=$p.IsIn; isOut=$p.IsOut; optional=$p.IsOptional
        hasDefault=$p.HasDefaultValue; default=$default
        requiredModifiers=@($p.GetRequiredCustomModifiers() | ForEach-Object {Type-Identity $_})
        optionalModifiers=@($p.GetOptionalCustomModifiers() | ForEach-Object {Type-Identity $_})
        customAttributes=@($p.GetCustomAttributesData() | ForEach-Object {$_.ToString()})}
}
function Method-Shape([System.Reflection.MethodBase]$m) {
    $parameters = @($m.GetParameters() | ForEach-Object { Parameter-Shape $_ })
    $return = if ($m -is [System.Reflection.MethodInfo]) { Parameter-Shape $m.ReturnParameter } else { $null }
    [ordered]@{id=('{0}::{1}({2})' -f $m.DeclaringType.FullName, $m.Name, (($parameters | ForEach-Object {$_.displayType}) -join ','))
        metadataToken=$m.MetadataToken; declaringType=$m.DeclaringType.FullName; declaringAssembly=$m.DeclaringType.Assembly.FullName
        kind=$(if ($m -is [System.Reflection.ConstructorInfo]) {if ($m.IsStatic) {'typeInitializer'} else {'constructor'}} else {'method'}); name=$m.Name
        attributes=$m.Attributes.ToString(); implementationAttributes=$m.GetMethodImplementationFlags().ToString()
        public=$m.IsPublic; family=$m.IsFamily; assembly=$m.IsAssembly; private=$m.IsPrivate
        static=$m.IsStatic; abstract=$m.IsAbstract; virtual=$m.IsVirtual; final=$m.IsFinal
        callingConvention=$m.CallingConvention.ToString(); genericParameters=@(Generic-Parameters $m)
        parameters=$parameters; return=$return
        customAttributes=@($m.GetCustomAttributesData() | ForEach-Object {$_.ToString()})}
}
try {
    $assembly = $context.LoadFromAssemblyPath((Join-Path $sdk 'Microsoft.Build.dll'))
    $flags = [System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly'
    $types = @()
    foreach ($name in @('Microsoft.Build.Evaluation.Project', 'Microsoft.Build.Evaluation.ProjectItem', 'Microsoft.Build.Evaluation.ProjectMetadata', 'Microsoft.Build.Evaluation.ProjectItemDefinition', 'Microsoft.Build.Evaluation.ProjectCollection', 'Microsoft.Build.Evaluation.Toolset', 'Microsoft.Build.Execution.ProjectPropertyInstance')) {
        $t = $assembly.GetType($name, $true)
        Remember-Type $t
        foreach ($i in $t.GetInterfaces()) { Remember-Type $i }
        Remember-Type $t.BaseType
        $names = @('GetItems','GetMetadataValue','HasMetadata','GetPropertyValue','AddToolset','RemoveAllToolsets','UnloadAllProjects','Dispose')
        $methods = @($t.GetConstructors($flags)) + @($t.GetMethods($flags) | Where-Object {$_.Name -cin $names})
        $properties = @()
        if ($true) {
            foreach ($p in $t.GetProperties($flags) | Where-Object {$_.Name -cin @('Items','ItemDefinitions','ItemType','EvaluatedInclude','Metadata','DirectMetadata','Name','EvaluatedValue','Count','Toolsets','ToolsVersion','ToolsPath','Properties')} | Sort-Object Name -CaseSensitive) {
                Remember-Type $p.PropertyType
                $properties += [ordered]@{name=$p.Name; metadataToken=$p.MetadataToken; declaringType=$t.FullName
                    declaringAssembly=$assembly.FullName; attributes=$p.Attributes.ToString(); type=(Type-Identity $p.PropertyType)
                    customAttributes=@($p.GetCustomAttributesData() | ForEach-Object {$_.ToString()})
                    requiredModifiers=@($p.GetRequiredCustomModifiers() | ForEach-Object {Type-Identity $_})
                    optionalModifiers=@($p.GetOptionalCustomModifiers() | ForEach-Object {Type-Identity $_})
                    indexParameters=@($p.GetIndexParameters() | ForEach-Object {Parameter-Shape $_})
                    accessors=@($p.GetAccessors($true) | ForEach-Object {Method-Shape $_})}
            }
        }
        $types += [ordered]@{identity=(Type-Identity $t); fullName=$t.FullName; metadataToken=$t.MetadataToken
            attributes=$t.Attributes.ToString(); customAttributes=@($t.GetCustomAttributesData() | ForEach-Object {$_.ToString()}); baseType=(Type-Identity $t.BaseType)
            interfaces=@($t.GetInterfaces() | ForEach-Object {Type-Identity $_} | Sort-Object -CaseSensitive)
            genericParameters=@(Generic-Parameters $t)
            methods=@($methods | Sort-Object MetadataToken | ForEach-Object {Method-Shape $_}); properties=$properties}
    }
    # Source-documented exception, not a CLR throws signature or behavioral proof.
    Remember-Type ($assembly.GetType('Microsoft.Build.Exceptions.InvalidProjectFileException', $true))
    [ordered]@{schemaVersion=1; method='MetadataLoadContext; no reference execution'
        hostRuntime=[System.Runtime.InteropServices.RuntimeInformation]::FrameworkDescription
        powershellVersion=$PSVersionTable.PSVersion.ToString(); assembly=$assembly.FullName
        moduleVersionId=$assembly.ManifestModule.ModuleVersionId.ToString()
        assemblyAttributes=@($assembly.GetCustomAttributesData() | ForEach-Object {$_.ToString()})
        types=$types; directContracts=@($script:contracts.Values)
        loadedAssemblies=@($context.GetAssemblies() | Sort-Object FullName -CaseSensitive | ForEach-Object {
            [ordered]@{identity=$_.FullName; path=$_.Location; moduleVersionId=$_.ManifestModule.ModuleVersionId.ToString()}
        })} | ConvertTo-Json -Depth 60
} finally { $context.Dispose() }
