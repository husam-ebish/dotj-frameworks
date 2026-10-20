using System.Reflection;
using System.Security.Cryptography;
using System.Text.Json;

Type[] selected = [
    typeof(IDisposable),
    typeof(Type),
    typeof(MemberInfo),
    typeof(MemberTypes),
    typeof(Exception),
    typeof(SystemException),
    typeof(ArgumentException),
    typeof(ArgumentNullException),
    typeof(TypeLoadException),
    typeof(IndexOutOfRangeException),
    typeof(System.IO.IOException),
    typeof(System.IO.FileNotFoundException),
];

BindingFlags declaredPublic = BindingFlags.Public | BindingFlags.DeclaredOnly
    | BindingFlags.Instance | BindingFlags.Static;
Exception inner = new("inner");
ArgumentException outer = new("outer", "value", inner);
ArgumentNullException nullArgument = new("typeName", "missing type");
static object ObserveGetType(string? name, bool throwOnError, bool ignoreCase)
{
    try
    {
        Type? resolved = Type.GetType(name!, throwOnError, ignoreCase);
        return new { result = resolved?.FullName, exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new
        {
            result = (string?)null,
            exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName,
        };
    }
}
static object ObserveArray(string name)
{
    Type type = Type.GetType(name, true)!;
    string? error = null;
    int? rank = null;
    try
    {
        rank = type.GetArrayRank();
    }
    catch (Exception exception)
    {
        error = exception.GetType().FullName;
    }
    return new { name, type.IsArray, element = type.GetElementType()?.FullName, rank, error };
}
static string? ObserveRankZero()
{
    try
    {
        typeof(string).MakeArrayType(0);
        return null;
    }
    catch (Exception exception)
    {
        return exception.GetType().FullName;
    }
}
static string? ObserveDoubleByRef()
{
    try
    {
        typeof(string).MakeByRefType().MakeByRefType();
        return null;
    }
    catch (Exception exception)
    {
        return exception.GetType().FullName;
    }
}
static string? ObservePointerFromByRef()
{
    try
    {
        typeof(string).MakeByRefType().MakePointerType();
        return null;
    }
    catch (Exception exception)
    {
        return exception.GetType().FullName;
    }
}
static string? ObserveNonEnumUnderlying()
{
    try
    {
        typeof(string).GetEnumUnderlyingType();
        return null;
    }
    catch (Exception exception)
    {
        return exception.GetType().FullName;
    }
}
static object ObserveSubclass(Type type, Type? parent)
{
    try
    {
        return new { result = (bool?)type.IsSubclassOf(parent!), exception = (string?)null,
            paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (bool?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveInterface(Type type, string? name, bool ignoreCase)
{
    try
    {
        return new { result = type.GetInterface(name!, ignoreCase)?.FullName,
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (string?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
if (outer.ParamName != "value" || outer.Message != "outer (Parameter 'value')"
    || !ReferenceEquals(outer.InnerException, inner)
    || nullArgument.ParamName != "typeName" || nullArgument.Message != "missing type (Parameter 'typeName')")
{
    throw new InvalidOperationException("Selected exception constructor observation changed.");
}
var result = new
{
    runtimeVersion = Environment.Version.ToString(),
    coreLibSha256 = Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(typeof(Type).Assembly.Location)))
        .ToLowerInvariant(),
    selectedConstructorBehavior = new
    {
        argumentParamName = outer.ParamName,
        argumentMessage = outer.Message,
        argumentInnerSameReference = ReferenceEquals(outer.InnerException, inner),
        nullArgumentParamName = nullArgument.ParamName,
        nullArgumentMessage = nullArgument.Message,
    },
    selectedGetTypeBehavior = new
    {
        exact = ObserveGetType("System.String", false, false),
        insensitive = ObserveGetType("system.string", false, true),
        sensitiveMiss = ObserveGetType("system.string", false, false),
        missing = ObserveGetType("System.Unknown", false, false),
        missingThrow = ObserveGetType("System.Unknown", true, false),
        nullName = ObserveGetType(null, false, false),
        coreLibString = ObserveGetType("System.String, System.Private.CoreLib", false, false),
        coreLibInt32 = ObserveGetType("System.Int32, System.Private.CoreLib", false, false),
        legacyString = ObserveGetType("System.String, mscorlib", false, false),
        unknownAssembly = ObserveGetType("System.String, NotAnAssembly", false, false),
        unknownAssemblyThrow = ObserveGetType("System.String, NotAnAssembly", true, false),
        emptyName = ObserveGetType("", false, false),
        emptyNameThrow = ObserveGetType("", true, false),
        leadingSpace = ObserveGetType(" System.String", false, false),
        trailingSpace = ObserveGetType("System.String ", false, false),
        qualifierSpace = ObserveGetType("System.String , System.Private.CoreLib", false, false),
        emptyAssembly = ObserveGetType("System.String, ", false, false),
        emptyAssemblyThrow = ObserveGetType("System.String, ", true, false),
        stringArray = ObserveGetType("System.String[]", false, false),
        intArray = ObserveGetType("System.Int32[]", false, false),
        stringArrayInsensitive = ObserveGetType("system.string[]", false, true),
        stringArrayQualified = ObserveGetType("System.String[], System.Private.CoreLib", false, false),
        listStringSimple = ObserveGetType("System.Collections.Generic.List`1[System.String]", false, false),
        listStringQualified = ObserveGetType("System.Collections.Generic.List`1[[System.String, System.Private.CoreLib]]", false, false),
        rankOneNonVector = ObserveGetType("System.String[*]", false, false),
        stringByRef = ObserveGetType("System.String&", false, false),
        stringArrayByRef = ObserveGetType("System.String[]&", false, false),
        stringPointer = ObserveGetType("System.String*", false, false),
        intPointer = ObserveGetType("System.Int32*", false, false),
        dictionarySimple = ObserveGetType("System.Collections.Generic.Dictionary`2[System.String,System.Int32]", false, false),
        dictionaryQualified = ObserveGetType("System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Int32, System.Private.CoreLib]]", false, false),
        dictionarySwapped = ObserveGetType("System.Collections.Generic.Dictionary`2[System.Int32,System.String]", false, false),
        jaggedString = ObserveGetType("System.String[][]", false, false),
        rectangularString = ObserveGetType("System.String[,]", false, false),
        rankThreeString = ObserveGetType("System.String[,,]", false, false),
        arrayOfListString = ObserveGetType("System.Collections.Generic.List`1[System.String][]", false, false),
    },
    selectedArrayBehavior = new[]
    {
        "System.String", "System.String[]", "System.String[][]", "System.String[,]",
        "System.String[,,]", "System.Collections.Generic.List`1[System.String][]",
    }.Select(ObserveArray).ToArray(),
    selectedMakeArrayBehavior = new
    {
        vector = typeof(string).MakeArrayType().FullName,
        rankOne = typeof(string).MakeArrayType(1).FullName,
        rankTwo = typeof(string).MakeArrayType(2).FullName,
        nestedVector = typeof(string[]).MakeArrayType().FullName,
        genericVector = typeof(List<string>).MakeArrayType().FullName,
        rankZeroError = ObserveRankZero(),
    },
    selectedByRefBehavior = new
    {
        name = typeof(string).MakeByRefType().FullName,
        isByRef = typeof(string).MakeByRefType().IsByRef,
        element = typeof(string).MakeByRefType().GetElementType()?.FullName,
        arrayName = typeof(string[]).MakeByRefType().FullName,
        repeatSameIdentity = ReferenceEquals(typeof(string).MakeByRefType(), typeof(string).MakeByRefType()),
        doubleByRefError = ObserveDoubleByRef(),
    },
    selectedPointerBehavior = new
    {
        name = typeof(string).MakePointerType().FullName,
        intName = typeof(int).MakePointerType().FullName,
        isPointer = typeof(string).MakePointerType().IsPointer,
        element = typeof(string).MakePointerType().GetElementType()?.FullName,
        repeatSameIdentity = ReferenceEquals(typeof(string).MakePointerType(), typeof(string).MakePointerType()),
        pointerToPointer = typeof(string).MakePointerType().MakePointerType().FullName,
        byRefError = ObservePointerFromByRef(),
    },
    selectedTypeNames = new[]
    {
        typeof(string), typeof(int), typeof(List<>), typeof(List<string>),
        typeof(string[]), typeof(string[,]), typeof(string).MakeByRefType(),
        typeof(string).MakePointerType(), typeof(List<>).GetGenericArguments()[0],
    }.Select(type => new
    {
        type.Name,
        type.FullName,
        type.Namespace,
    }).ToArray(),
    selectedMemberTypeBehavior = new
    {
        enumValues = Enum.GetValues<MemberTypes>()
            .Select(value => new { name = value.ToString(), value = (int)value }).ToArray(),
        stringType = typeof(string).MemberType.ToString(),
        arrayType = typeof(string[]).MemberType.ToString(),
        openGeneric = typeof(List<>).MemberType.ToString(),
        genericParameter = typeof(List<>).GetGenericArguments()[0].MemberType.ToString(),
        memberTypeGetterAbstract = typeof(MemberInfo).GetProperty("MemberType")?.GetMethod?.IsAbstract,
    },
    selectedMemberOwnerBehavior = new[]
    {
        typeof(string), typeof(List<>), typeof(List<string>),
        typeof(List<>).GetGenericArguments()[0], typeof(string[]),
        typeof(string).MakeByRefType(), typeof(string).MakePointerType(),
    }.Select(type => new
    {
        name = type.FullName ?? type.Name,
        declaringType = type.DeclaringType?.FullName,
        reflectedType = type.ReflectedType?.FullName,
    }).ToArray(),
    selectedBaseTypeBehavior = new[]
    {
        typeof(object), typeof(string), typeof(int), typeof(List<>), typeof(List<string>),
        typeof(List<>).GetGenericArguments()[0], typeof(string[]), typeof(string[,]),
        typeof(string).MakeByRefType(), typeof(string).MakePointerType(),
    }.Select(type => new
    {
        name = type.FullName ?? type.Name,
        baseType = type.BaseType?.FullName,
    }).ToArray(),
    selectedKindFlags = new[]
    {
        typeof(object), typeof(string), typeof(int), typeof(ValueType), typeof(Array),
        typeof(List<>), typeof(List<string>), typeof(List<>).GetGenericArguments()[0],
        typeof(string[]), typeof(string[,]), typeof(string).MakeByRefType(),
        typeof(string).MakePointerType(),
        typeof(IDisposable), typeof(MemberTypes),
    }.Select(type => new
    {
        name = type.FullName ?? type.Name,
        type.IsClass,
        type.IsValueType,
        type.IsInterface,
        type.IsEnum,
    }).ToArray(),
    selectedEnumBaseBehavior = new
    {
        enumBase = typeof(MemberTypes).BaseType?.FullName,
        baseBase = typeof(Enum).BaseType?.FullName,
        underlying = typeof(MemberTypes).GetEnumUnderlyingType().FullName,
        nonEnumError = ObserveNonEnumUnderlying(),
    },
    selectedAssignability = new (Type Target, Type? Candidate)[]
    {
        (typeof(object), typeof(string)),
        (typeof(object), typeof(int)),
        (typeof(object), typeof(IDisposable)),
        (typeof(object), typeof(string[])),
        (typeof(object), typeof(string).MakeByRefType()),
        (typeof(object), typeof(string).MakePointerType()),
        (typeof(ValueType), typeof(int)),
        (typeof(ValueType), typeof(MemberTypes)),
        (typeof(ValueType), typeof(string)),
        (typeof(Enum), typeof(MemberTypes)),
        (typeof(Enum), typeof(int)),
        (typeof(Array), typeof(string[])),
        (typeof(Array), typeof(string)),
        (typeof(List<>), typeof(List<string>)),
        (typeof(List<string>), typeof(List<string>)),
        (typeof(string), null),
    }.Select(pair => new
    {
        target = pair.Target.FullName,
        candidate = pair.Candidate?.FullName,
        result = pair.Target.IsAssignableFrom(pair.Candidate),
    }).ToArray(),
    selectedSubclassBehavior = new (Type Type, Type? Parent)[]
    {
        (typeof(string), typeof(object)),
        (typeof(int), typeof(ValueType)),
        (typeof(int), typeof(object)),
        (typeof(MemberTypes), typeof(Enum)),
        (typeof(MemberTypes), typeof(ValueType)),
        (typeof(string[]), typeof(Array)),
        (typeof(IDisposable), typeof(object)),
        (typeof(List<string>), typeof(List<>)),
        (typeof(string), typeof(string)),
        (typeof(string), null),
    }.Select(pair => new
    {
        type = pair.Type.FullName,
        parent = pair.Parent?.FullName,
        observation = ObserveSubclass(pair.Type, pair.Parent),
    }).ToArray(),
    selectedInstanceBehavior = new (Type Target, object? Value)[]
    {
        (typeof(object), "text"),
        (typeof(object), 42),
        (typeof(object), null),
        (typeof(string), "text"),
        (typeof(string), 42),
        (typeof(int), 42),
        (typeof(int), "text"),
        (typeof(ValueType), 42),
        (typeof(Enum), MemberTypes.TypeInfo),
        (typeof(Array), new string[] { "text" }),
        (typeof(string[]), new string[] { "text" }),
        (typeof(IDisposable), new System.IO.MemoryStream()),
        (typeof(List<>), new List<string>()),
        (typeof(string), null),
    }.Select(pair => new
    {
        target = pair.Target.FullName,
        valueType = pair.Value?.GetType().FullName,
        result = pair.Target.IsInstanceOfType(pair.Value),
    }).ToArray(),
    selectedInterfaceBehavior = new
    {
        objectInterfaces = typeof(object).GetInterfaces().Select(type => type.FullName).ToArray(),
        disposableInterfaces = typeof(IDisposable).GetInterfaces().Select(type => type.FullName).ToArray(),
        objectMiss = ObserveInterface(typeof(object), "System.IDisposable", false),
        disposableSelf = ObserveInterface(typeof(IDisposable), "System.IDisposable", false),
        emptyName = ObserveInterface(typeof(IDisposable), "", false),
        nullName = ObserveInterface(typeof(IDisposable), null, false),
    },
    types = selected.Select(type => new
    {
        fullName = type.FullName,
        baseType = type.BaseType?.FullName,
        isInterface = type.IsInterface,
        isAbstract = type.IsAbstract,
        nameGetterIsAbstract = type.GetProperty("Name")?.GetMethod?.IsAbstract,
        declaringGetterIsAbstract = type.GetProperty("DeclaringType")?.GetMethod?.IsAbstract,
        reflectedGetterIsAbstract = type.GetProperty("ReflectedType")?.GetMethod?.IsAbstract,
        declaredPublicMethodCount = type.GetMethods(declaredPublic).Count(method => !method.IsSpecialName),
        declaredPublicPropertyCount = type.GetProperties(declaredPublic).Length,
        selectedMethods = type.GetMethods(declaredPublic)
            .Where(method => !method.IsSpecialName && (
                method.Name is "Dispose" or "Equals" or "GetType" or "MakeGenericType"
                    or "GetGenericArguments" or "GetGenericTypeDefinition"
                    or "GetElementType" or "GetArrayRank" or "MakeArrayType" or "MakeByRefType"
                    or "MakePointerType"))
            .Select(method => new
            {
                name = method.Name,
                isStatic = method.IsStatic,
                returnType = method.ReturnType.FullName,
                parameters = method.GetParameters()
                    .Select(parameter => new { name = parameter.Name, type = parameter.ParameterType.FullName })
                    .ToArray(),
            }).ToArray(),
        selectedProperties = type.GetProperties(declaredPublic)
            .Where(property => property.Name is "ParamName" or "Message" or "InnerException" or "IsGenericType"
                or "IsConstructedGenericType" or "IsGenericParameter"
                or "GenericParameterPosition" or "GenericTypeArguments" or "IsArray" or "IsByRef"
                or "IsPointer" or "Name" or "FullName" or "Namespace" or "MemberType"
                or "DeclaringType" or "ReflectedType" or "BaseType" or "IsClass" or "IsValueType"
                or "IsInterface" or "IsEnum" or "GetEnumUnderlyingType" or "IsAssignableFrom"
                or "IsSubclassOf" or "IsInstanceOfType" or "GetInterfaces" or "GetInterface")
            .Select(property => new { name = property.Name, type = property.PropertyType.FullName })
            .ToArray(),
        publicConstructors = type.GetConstructors(declaredPublic)
            .Select(constructor => constructor.GetParameters()
                .Select(parameter => new { name = parameter.Name, type = parameter.ParameterType.FullName })
                .ToArray()).ToArray(),
    }).ToArray(),
};
Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));
