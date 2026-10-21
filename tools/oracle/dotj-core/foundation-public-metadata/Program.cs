using System.Reflection;
using System.Security.Cryptography;
using System.Text.Json;

Type[] selected = [
    typeof(IDisposable),
    typeof(IComparable),
    typeof(IFormattable),
    typeof(ISpanFormattable),
    typeof(IUtf8SpanFormattable),
    typeof(IFormatProvider),
    typeof(IConvertible),
    typeof(TypeCode),
    typeof(decimal),
    typeof(DateTime),
    typeof(int),
    typeof(Type),
    typeof(MemberInfo),
    typeof(MemberTypes),
    typeof(GenericParameterAttributes),
    typeof(Exception),
    typeof(SystemException),
    typeof(ArgumentException),
    typeof(ArgumentNullException),
    typeof(TypeLoadException),
    typeof(IndexOutOfRangeException),
    typeof(System.IO.IOException),
    typeof(System.IO.FileNotFoundException),
    typeof(System.IO.FileLoadException),
    typeof(System.Globalization.CultureNotFoundException),
    typeof(OverflowException),
    typeof(InvalidCastException),
    typeof(InvalidOperationException),
    typeof(FormatException),
    typeof(System.Globalization.NumberStyles),
];

BindingFlags declaredPublic = BindingFlags.Public | BindingFlags.DeclaredOnly
    | BindingFlags.Instance | BindingFlags.Static;
Exception inner = new("inner");
ArgumentException outer = new("outer", "value", inner);
ArgumentNullException nullArgument = new("typeName", "missing type");
Exception rootException = new InvalidOperationException("root");
Exception middleException = new("middle", rootException);
Exception chainException = new ArgumentException("outer", "value", middleException);
Exception standaloneException = new("standalone");
Exception helpLinkException = new("help");
bool helpLinkStartsNull = helpLinkException.HelpLink is null;
helpLinkException.HelpLink = "https://example.invalid/help";
string? helpLinkAfterSet = helpLinkException.HelpLink;
helpLinkException.HelpLink = null;
Exception sourceException = new("source");
string? sourceBeforeSet = sourceException.Source;
sourceException.Source = "selected.component";
string? sourceAfterSet = sourceException.Source;
sourceException.Source = null;
Exception stackBeforeThrow = new("before throw");
Exception stackAfterThrow = null!;
try
{
    throw new Exception("after throw");
}
catch (Exception caught)
{
    stackAfterThrow = caught;
}
Exception rethrowOriginal = new("rethrow");
Exception rethrowCaught = null!;
string? stackBeforeRethrow = null;
try
{
    try
    {
        throw rethrowOriginal;
    }
    catch (Exception caught)
    {
        stackBeforeRethrow = caught.StackTrace;
        throw;
    }
}
catch (Exception caught)
{
    rethrowCaught = caught;
}
Exception dataException = new("data");
System.Collections.IDictionary data = dataException.Data;
bool dataStartsEmpty = data.Count == 0;
data["key"] = "value";
System.Collections.IDictionary secondData = new Exception("other").Data;
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
static object ObserveGenericParameterAttributes(Type type)
{
    try
    {
        return new { value = (int?)type.GenericParameterAttributes, exception = (string?)null };
    }
    catch (Exception exception)
    {
        return new { value = (int?)null, exception = exception.GetType().FullName };
    }
}
static string? ObserveGenericDefinitionError(Type type)
{
    try
    {
        type.GetGenericTypeDefinition();
        return null;
    }
    catch (Exception exception)
    {
        return exception.GetType().FullName;
    }
}
static object ObserveGenericArgumentCopies()
{
    Type open = typeof(Dictionary<,>);
    Type[] first = open.GetGenericArguments();
    Type[] second = open.GetGenericArguments();
    bool distinctArrays = !ReferenceEquals(first, second);
    bool stableElements = ReferenceEquals(first[0], second[0])
        && ReferenceEquals(first[1], second[1]);
    string[] openNames = first.Select(type => type.Name).ToArray();
    int[] positions = first.Select(type => type.GenericParameterPosition).ToArray();
    first[0] = typeof(object);
    bool mutationIsolated = ReferenceEquals(second[0], open.GetGenericArguments()[0]);
    Type closed = typeof(Dictionary<string, int>);
    return new
    {
        openNames,
        positions,
        distinctArrays,
        stableElements,
        mutationIsolated,
        closedNames = closed.GetGenericArguments().Select(type => type.FullName).ToArray(),
        openTypeArgumentsLength = open.GenericTypeArguments.Length,
        closedTypeArguments = closed.GenericTypeArguments.Select(type => type.FullName).ToArray(),
        arrayArgumentsLength = typeof(string[]).GetGenericArguments().Length,
    };
}
static object ObserveGenericParameterConstraints(Type type)
{
    try
    {
        return new { constraints = type.GetGenericParameterConstraints()
                .Select(constraint => constraint.FullName).ToArray(), exception = (string?)null };
    }
    catch (Exception exception)
    {
        return new { constraints = (string?[]?)null,
            exception = exception.GetType().FullName };
    }
}
static object ObserveTypeConstruction(Func<Type> operation)
{
    try
    {
        return new { result = operation().FullName, exception = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (string?)null, exception = exception.GetType().FullName };
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
static object ObserveSpanFormat(int value, int length)
{
    Span<char> destination = stackalloc char[length];
    bool success = value.TryFormat(destination, out int charsWritten, "D",
        System.Globalization.CultureInfo.InvariantCulture);
    return new { success, charsWritten, text = new string(destination[..charsWritten]) };
}
static object ObserveUtf8SpanFormat(int value, int length)
{
    Span<byte> destination = stackalloc byte[length];
    bool success = ((IUtf8SpanFormattable)value).TryFormat(destination,
        out int bytesWritten, "D", System.Globalization.CultureInfo.InvariantCulture);
    return new { success, bytesWritten,
        text = System.Text.Encoding.UTF8.GetString(destination[..bytesWritten]) };
}
static string? ObserveInt32Error(Action operation)
{
    try
    {
        operation();
        return null;
    }
    catch (Exception exception)
    {
        return exception.GetType().FullName;
    }
}
static object ObserveInt32Parse(string? text)
{
    try
    {
        return new { result = (int?)int.Parse(text!), exception = (string?)null,
            paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (int?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveInt32TryParse(string? text)
{
    bool success = int.TryParse(text, out int value);
    return new { success, value };
}
static object ObserveInt32HexParse(string? text)
{
    try
    {
        return new { result = (int?)int.Parse(text!,
                System.Globalization.NumberStyles.HexNumber,
                System.Globalization.CultureInfo.InvariantCulture),
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (int?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveInt32HexTryParse(string? text)
{
    bool success = int.TryParse(text, System.Globalization.NumberStyles.HexNumber,
        System.Globalization.CultureInfo.InvariantCulture, out int value);
    return new { success, value };
}
static string? ObserveInt32FormatError(string format)
{
    try
    {
        ((IFormattable)42).ToString(format, System.Globalization.CultureInfo.InvariantCulture);
        return null;
    }
    catch (Exception exception)
    {
        return exception.GetType().FullName;
    }
}
static object ObserveTypeArray(object?[]? values)
{
    try
    {
        return new { result = Array.ConvertAll(Type.GetTypeArray(values!), type => type.FullName),
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (string?[]?)null, exception = exception.GetType().FullName,
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
    selectedBaseExceptionBehavior = new
    {
        standaloneIsSelf = ReferenceEquals(standaloneException.GetBaseException(), standaloneException),
        rootIsSelf = ReferenceEquals(rootException.GetBaseException(), rootException),
        middleReturnsRoot = ReferenceEquals(middleException.GetBaseException(), rootException),
        chainReturnsRoot = ReferenceEquals(chainException.GetBaseException(), rootException),
        chainInnerPreserved = ReferenceEquals(chainException.InnerException, middleException),
        baseType = chainException.GetBaseException().GetType().FullName,
        baseMessage = chainException.GetBaseException().Message,
    },
    selectedExceptionDataBehavior = new
    {
        startsEmpty = dataStartsEmpty,
        sameReference = ReferenceEquals(data, dataException.Data),
        storedValue = dataException.Data["key"] as string,
        countAfterInsert = dataException.Data.Count,
        separateInstance = !ReferenceEquals(data, secondData),
        secondStartsEmpty = secondData.Count == 0,
    },
    selectedExceptionHResultBehavior = new
    {
        parameterless = new Exception().HResult,
        message = new Exception("message").HResult,
        inner = new Exception("outer", inner).HResult,
        argument = new ArgumentException("argument").HResult,
        invalidOperation = new InvalidOperationException("invalid").HResult,
    },
    selectedExceptionHelpLinkBehavior = new
    {
        startsNull = helpLinkStartsNull,
        afterSet = helpLinkAfterSet,
        afterReset = helpLinkException.HelpLink,
        separateInstanceIsNull = new Exception("other").HelpLink is null,
    },
    selectedExceptionSourceBehavior = new
    {
        beforeSet = sourceBeforeSet,
        afterSet = sourceAfterSet,
        afterReset = sourceException.Source,
        separateInstance = new Exception("other").Source,
    },
    selectedExceptionToStringBehavior = new
    {
        exceptionWithMessage = new Exception("message").ToString(),
        exceptionWithoutMessage = new Exception().ToString(),
        argumentWithParameter = new ArgumentException("invalid", "value").ToString(),
        invalidOperation = new InvalidOperationException("invalid").ToString(),
    },
    selectedExceptionInnerToStringBehavior = new
    {
        twoLevel = new Exception("outer", new Exception("inner")).ToString(),
        threeLevel = new ArgumentException("outer", "value",
            new Exception("middle", new InvalidOperationException("root"))).ToString(),
    },
    selectedExceptionRuntimeTypeBehavior = new
    {
        baseType = new Exception("base").GetType().FullName,
        argumentType = new ArgumentException("argument").GetType().FullName,
        invalidOperationType = new InvalidOperationException("invalid").GetType().FullName,
        repeatedReference = ReferenceEquals(new Exception().GetType(), new Exception().GetType()),
    },
    selectedExceptionStackBoundary = new
    {
        prethrowStackIsNull = stackBeforeThrow.StackTrace is null,
        prethrowTargetSiteIsNull = stackBeforeThrow.TargetSite is null,
        thrownStackNonEmpty = !string.IsNullOrEmpty(stackAfterThrow.StackTrace),
        thrownTargetSitePresent = stackAfterThrow.TargetSite is not null,
    },
    selectedExceptionRethrowBoundary = new
    {
        sameReference = ReferenceEquals(rethrowOriginal, rethrowCaught),
        stackBeforeNonEmpty = !string.IsNullOrEmpty(stackBeforeRethrow),
        stackAfterNonEmpty = !string.IsNullOrEmpty(rethrowCaught.StackTrace),
        stackTextUnchanged = string.Equals(stackBeforeRethrow, rethrowCaught.StackTrace,
            StringComparison.Ordinal),
    },
    selectedTypeCodeBehavior = new
    {
        nullType = Type.GetTypeCode(null).ToString(),
        objectType = Type.GetTypeCode(typeof(object)).ToString(),
        stringType = Type.GetTypeCode(typeof(string)).ToString(),
        booleanType = Type.GetTypeCode(typeof(bool)).ToString(),
        charType = Type.GetTypeCode(typeof(char)).ToString(),
        byteType = Type.GetTypeCode(typeof(byte)).ToString(),
        int16Type = Type.GetTypeCode(typeof(short)).ToString(),
        int32Type = Type.GetTypeCode(typeof(int)).ToString(),
        int64Type = Type.GetTypeCode(typeof(long)).ToString(),
        singleType = Type.GetTypeCode(typeof(float)).ToString(),
        doubleType = Type.GetTypeCode(typeof(double)).ToString(),
        decimalType = Type.GetTypeCode(typeof(decimal)).ToString(),
        dateTimeType = Type.GetTypeCode(typeof(DateTime)).ToString(),
        enumType = Type.GetTypeCode(typeof(MemberTypes)).ToString(),
        arrayType = Type.GetTypeCode(typeof(string[])).ToString(),
        genericType = Type.GetTypeCode(typeof(System.Collections.Generic.List<string>)).ToString(),
    },
    selectedBooleanTypeIdentityBehavior = new
    {
        name = typeof(bool).Name,
        fullName = typeof(bool).FullName,
        baseType = typeof(bool).BaseType?.FullName,
        isPrimitive = typeof(bool).IsPrimitive,
        isValueType = typeof(bool).IsValueType,
        isSealed = typeof(bool).IsSealed,
        isClass = typeof(bool).IsClass,
        isAssignableToValueType = typeof(bool).IsAssignableTo(typeof(ValueType)),
        typeCode = Type.GetTypeCode(typeof(bool)).ToString(),
    },
    selectedCharTypeIdentityBehavior = new
    {
        name = typeof(char).Name,
        fullName = typeof(char).FullName,
        baseType = typeof(char).BaseType?.FullName,
        isPrimitive = typeof(char).IsPrimitive,
        isValueType = typeof(char).IsValueType,
        isSealed = typeof(char).IsSealed,
        isClass = typeof(char).IsClass,
        isAssignableToValueType = typeof(char).IsAssignableTo(typeof(ValueType)),
        typeCode = Type.GetTypeCode(typeof(char)).ToString(),
    },
    selectedInt16TypeIdentityBehavior = new
    {
        name = typeof(short).Name,
        fullName = typeof(short).FullName,
        baseType = typeof(short).BaseType?.FullName,
        isPrimitive = typeof(short).IsPrimitive,
        isValueType = typeof(short).IsValueType,
        isSealed = typeof(short).IsSealed,
        isClass = typeof(short).IsClass,
        isAssignableToValueType = typeof(short).IsAssignableTo(typeof(ValueType)),
        typeCode = Type.GetTypeCode(typeof(short)).ToString(),
    },
    selectedInt64TypeIdentityBehavior = new
    {
        name = typeof(long).Name,
        fullName = typeof(long).FullName,
        baseType = typeof(long).BaseType?.FullName,
        isPrimitive = typeof(long).IsPrimitive,
        isValueType = typeof(long).IsValueType,
        isSealed = typeof(long).IsSealed,
        isClass = typeof(long).IsClass,
        isAssignableToValueType = typeof(long).IsAssignableTo(typeof(ValueType)),
        typeCode = Type.GetTypeCode(typeof(long)).ToString(),
    },
    selectedSingleTypeIdentityBehavior = new
    {
        name = typeof(float).Name,
        fullName = typeof(float).FullName,
        baseType = typeof(float).BaseType?.FullName,
        isPrimitive = typeof(float).IsPrimitive,
        isValueType = typeof(float).IsValueType,
        isSealed = typeof(float).IsSealed,
        isClass = typeof(float).IsClass,
        isAssignableToValueType = typeof(float).IsAssignableTo(typeof(ValueType)),
        typeCode = Type.GetTypeCode(typeof(float)).ToString(),
    },
    selectedDoubleTypeIdentityBehavior = new
    {
        name = typeof(double).Name,
        fullName = typeof(double).FullName,
        baseType = typeof(double).BaseType?.FullName,
        isPrimitive = typeof(double).IsPrimitive,
        isValueType = typeof(double).IsValueType,
        isSealed = typeof(double).IsSealed,
        isClass = typeof(double).IsClass,
        isAssignableToValueType = typeof(double).IsAssignableTo(typeof(ValueType)),
        typeCode = Type.GetTypeCode(typeof(double)).ToString(),
    },
    selectedByteTypeIdentityBehavior = new
    {
        name = typeof(byte).Name,
        fullName = typeof(byte).FullName,
        baseType = typeof(byte).BaseType?.FullName,
        isPrimitive = typeof(byte).IsPrimitive,
        isValueType = typeof(byte).IsValueType,
        isSealed = typeof(byte).IsSealed,
        isClass = typeof(byte).IsClass,
        isAssignableToValueType = typeof(byte).IsAssignableTo(typeof(ValueType)),
        typeCode = Type.GetTypeCode(typeof(byte)).ToString(),
    },
    selectedPrimitiveLookupBehavior = new[]
    {
        "System.Boolean", "System.Char", "System.Byte", "System.Int16",
        "System.Int64", "System.Single", "System.Double",
    }.Select(name => new
    {
        name,
        exact = Type.GetType(name)?.FullName,
        lowerSensitive = Type.GetType(name.ToLowerInvariant(), false, false)?.FullName,
        lowerInsensitive = Type.GetType(name.ToLowerInvariant(), false, true)?.FullName,
        qualified = Type.GetType(name + ", System.Private.CoreLib")?.FullName,
        qualifiedLowerInsensitive = Type.GetType(
            (name + ", System.Private.CoreLib").ToLowerInvariant(), false, true)?.FullName,
    }).ToArray(),
    selectedPrimitiveVectorBehavior = new[]
    {
        typeof(bool[]), typeof(char[]), typeof(byte[]), typeof(short[]),
        typeof(long[]), typeof(float[]), typeof(double[]),
    }.Select(type => new
    {
        name = type.Name,
        fullName = type.FullName,
        elementFullName = type.GetElementType()?.FullName,
        rank = type.GetArrayRank(),
        isVector = type.IsSZArray,
        typeCode = Type.GetTypeCode(type).ToString(),
        lookupIdentity = ReferenceEquals(type, Type.GetType(type.FullName!)),
        assemblyLookupIdentity = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
        insensitiveLookupIdentity = ReferenceEquals(type, Type.GetType(type.FullName!.ToLowerInvariant(), false, true)),
    }).ToArray(),
    selectedPrimitiveRectangularBehavior = new[]
    {
        typeof(bool[,]), typeof(char[,]), typeof(byte[,]), typeof(short[,]),
        typeof(long[,]), typeof(float[,]), typeof(double[,]),
    }.Select(type => new
    {
        name = type.Name,
        fullName = type.FullName,
        elementFullName = type.GetElementType()?.FullName,
        rank = type.GetArrayRank(),
        isVector = type.IsSZArray,
        isVariableBound = type.IsVariableBoundArray,
        typeCode = Type.GetTypeCode(type).ToString(),
        lookupIdentity = ReferenceEquals(type, Type.GetType(type.FullName!)),
        assemblyLookupIdentity = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
        insensitiveLookupIdentity = ReferenceEquals(type, Type.GetType(type.FullName!.ToLowerInvariant(), false, true)),
    }).ToArray(),
    selectedPrimitiveRankThreeBehavior = new[]
    {
        typeof(bool[,,]), typeof(char[,,]), typeof(byte[,,]), typeof(short[,,]),
        typeof(long[,,]), typeof(float[,,]), typeof(double[,,]),
    }.Select(type => new
    {
        name = type.Name,
        fullName = type.FullName,
        elementFullName = type.GetElementType()?.FullName,
        rank = type.GetArrayRank(),
        isVector = type.IsSZArray,
        isVariableBound = type.IsVariableBoundArray,
        typeCode = Type.GetTypeCode(type).ToString(),
        lookupIdentity = ReferenceEquals(type, Type.GetType(type.FullName!)),
        assemblyLookupIdentity = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
        insensitiveLookupIdentity = ReferenceEquals(type, Type.GetType(type.FullName!.ToLowerInvariant(), false, true)),
    }).ToArray(),
    selectedPrimitiveVariableBoundBehavior = new[]
    {
        typeof(bool).MakeArrayType(1), typeof(char).MakeArrayType(1),
        typeof(byte).MakeArrayType(1), typeof(short).MakeArrayType(1),
        typeof(long).MakeArrayType(1), typeof(float).MakeArrayType(1),
        typeof(double).MakeArrayType(1),
    }.Select(type => new
    {
        name = type.Name,
        fullName = type.FullName,
        elementFullName = type.GetElementType()?.FullName,
        rank = type.GetArrayRank(),
        isVector = type.IsSZArray,
        isVariableBound = type.IsVariableBoundArray,
        typeCode = Type.GetTypeCode(type).ToString(),
        lookupIdentity = ReferenceEquals(type, Type.GetType(type.FullName!)),
        assemblyLookupIdentity = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
        insensitiveLookupIdentity = ReferenceEquals(type, Type.GetType(type.FullName!.ToLowerInvariant(), false, true)),
    }).ToArray(),
    selectedTypeToStringBehavior = new[]
    {
        typeof(string), typeof(int), typeof(string[]), typeof(string[,]),
        typeof(string).MakeByRefType(), typeof(string).MakePointerType(),
        typeof(System.Collections.Generic.List<>),
        typeof(System.Collections.Generic.List<>).GetGenericArguments()[0],
        typeof(System.Collections.Generic.List<string>),
        typeof(System.Collections.Generic.Dictionary<string, int>),
    }.Select(type => new { fullName = type.FullName, text = type.ToString() }).ToArray(),
    selectedTypeArrayBehavior = new
    {
        mixed = ObserveTypeArray(["text", 42, new Exception("x")]),
        empty = ObserveTypeArray([]),
        nullArray = ObserveTypeArray(null),
        nullElement = ObserveTypeArray(["text", null]),
        separateArrays = !ReferenceEquals(Type.GetTypeArray(["text"]), Type.GetTypeArray(["text"])),
    },
    selectedTypeHashBehavior = new
    {
        stringRepeatStable = typeof(string).GetHashCode() == typeof(string).GetHashCode(),
        stringLookupStable = typeof(string).GetHashCode() == Type.GetType("System.String")!.GetHashCode(),
        int32RepeatStable = typeof(int).GetHashCode() == Type.GetType("System.Int32")!.GetHashCode(),
        genericRepeatStable = typeof(System.Collections.Generic.List<string>).GetHashCode()
            == typeof(System.Collections.Generic.List<string>).GetHashCode(),
    },
    selectedAssignableToBehavior = new
    {
        stringToObject = typeof(string).IsAssignableTo(typeof(object)),
        objectToString = typeof(object).IsAssignableTo(typeof(string)),
        stringToComparable = typeof(string).IsAssignableTo(typeof(IComparable)),
        comparableToString = typeof(IComparable).IsAssignableTo(typeof(string)),
        stringToSelf = typeof(string).IsAssignableTo(typeof(string)),
        stringToNull = typeof(string).IsAssignableTo(null),
        int32ToValueType = typeof(int).IsAssignableTo(typeof(ValueType)),
    },
    selectedEquivalentTypeBehavior = new
    {
        stringSelf = typeof(string).IsEquivalentTo(typeof(string)),
        stringLookup = typeof(string).IsEquivalentTo(Type.GetType("System.String")),
        stringInt32 = typeof(string).IsEquivalentTo(typeof(int)),
        stringNull = typeof(string).IsEquivalentTo(null),
        genericSame = typeof(System.Collections.Generic.List<string>)
            .IsEquivalentTo(typeof(System.Collections.Generic.List<string>)),
        genericDifferent = typeof(System.Collections.Generic.List<string>)
            .IsEquivalentTo(typeof(System.Collections.Generic.List<int>)),
        vectorRankTwo = typeof(string[]).IsEquivalentTo(typeof(string[,])),
    },
    selectedUnderlyingSystemTypeBehavior = new
    {
        stringSelf = ReferenceEquals(typeof(string).UnderlyingSystemType, typeof(string)),
        int32Self = ReferenceEquals(typeof(int).UnderlyingSystemType, typeof(int)),
        genericDefinitionSelf = ReferenceEquals(typeof(System.Collections.Generic.List<>).UnderlyingSystemType,
            typeof(System.Collections.Generic.List<>)),
        closedGenericSelf = ReferenceEquals(typeof(System.Collections.Generic.List<string>).UnderlyingSystemType,
            typeof(System.Collections.Generic.List<string>)),
        arraySelf = ReferenceEquals(typeof(string[]).UnderlyingSystemType, typeof(string[])),
        genericParameterSelf = ReferenceEquals(typeof(System.Collections.Generic.List<>).GetGenericArguments()[0]
            .UnderlyingSystemType, typeof(System.Collections.Generic.List<>).GetGenericArguments()[0]),
    },
    selectedGenericParameterKindBehavior = new
    {
        stringIsTypeParameter = typeof(string).IsGenericTypeParameter,
        stringIsMethodParameter = typeof(string).IsGenericMethodParameter,
        listParameterIsTypeParameter = typeof(System.Collections.Generic.List<>).GetGenericArguments()[0]
            .IsGenericTypeParameter,
        listParameterIsMethodParameter = typeof(System.Collections.Generic.List<>).GetGenericArguments()[0]
            .IsGenericMethodParameter,
        convertAllParameterIsTypeParameter = typeof(System.Collections.Generic.List<>).GetMethod("ConvertAll")!
            .GetGenericArguments()[0].IsGenericTypeParameter,
        convertAllParameterIsMethodParameter = typeof(System.Collections.Generic.List<>).GetMethod("ConvertAll")!
            .GetGenericArguments()[0].IsGenericMethodParameter,
    },
    selectedGenericParameterAttributeBehavior = new
    {
        stringType = ObserveGenericParameterAttributes(typeof(string)),
        listParameter = ObserveGenericParameterAttributes(typeof(System.Collections.Generic.List<>).GetGenericArguments()[0]),
        dictionaryKeyParameter = ObserveGenericParameterAttributes(typeof(System.Collections.Generic.Dictionary<,>).GetGenericArguments()[0]),
        convertAllParameter = ObserveGenericParameterAttributes(typeof(System.Collections.Generic.List<>).GetMethod("ConvertAll")!.GetGenericArguments()[0]),
    },
    selectedGenericParameterAttributeValues = Enum.GetNames<GenericParameterAttributes>()
        .ToDictionary(name => name, name => (int)Enum.Parse<GenericParameterAttributes>(name)),
    selectedGenericParameterAttributesTypeIdentity = new
    {
        name = typeof(GenericParameterAttributes).Name,
        fullName = typeof(GenericParameterAttributes).FullName,
        baseType = typeof(GenericParameterAttributes).BaseType?.FullName,
        isEnum = typeof(GenericParameterAttributes).IsEnum,
        isValueType = typeof(GenericParameterAttributes).IsValueType,
        isSealed = typeof(GenericParameterAttributes).IsSealed,
        underlyingType = typeof(GenericParameterAttributes).GetEnumUnderlyingType().FullName,
        typeCode = Type.GetTypeCode(typeof(GenericParameterAttributes)).ToString(),
        qualifiedLookup = ReferenceEquals(typeof(GenericParameterAttributes),
            Type.GetType(typeof(GenericParameterAttributes).AssemblyQualifiedName!)),
        insensitiveLookup = ReferenceEquals(typeof(GenericParameterAttributes),
            Type.GetType("system.reflection.genericparameterattributes", false, true)),
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
        type.AssemblyQualifiedName,
        roundTripSameReference = type.AssemblyQualifiedName is string assemblyQualifiedName
            && ReferenceEquals(Type.GetType(assemblyQualifiedName), type),
        type.Namespace,
    }).ToArray(),
    selectedDictionaryQualifiedRoundTrip = new[]
    {
        typeof(Dictionary<,>), typeof(Dictionary<string, int>), typeof(Dictionary<int, string>),
        typeof(Dictionary<string, string>), typeof(Dictionary<int, int>),
    }.Select(type => new
    {
        type.FullName,
        type.AssemblyQualifiedName,
        sameReference = ReferenceEquals(Type.GetType(type.AssemblyQualifiedName), type),
        lowerSensitive = ObserveGetType(type.AssemblyQualifiedName!.ToLowerInvariant(), false, false),
        lowerInsensitiveSameReference = ReferenceEquals(
            Type.GetType(type.AssemblyQualifiedName!.ToLowerInvariant(), false, true), type),
    }).ToArray(),
    selectedNestedGenericQualifiedRoundTrip = new[]
    {
        typeof(List<List<string>>), typeof(Dictionary<string, List<int>>),
        typeof(Dictionary<List<string>, List<int>>),
    }.Select(type => new
    {
        type.FullName,
        type.AssemblyQualifiedName,
        sameReference = ReferenceEquals(Type.GetType(type.AssemblyQualifiedName), type),
        lowerSensitive = ObserveGetType(type.AssemblyQualifiedName!.ToLowerInvariant(), false, false),
        lowerInsensitiveSameReference = ReferenceEquals(
            Type.GetType(type.AssemblyQualifiedName!.ToLowerInvariant(), false, true), type),
    }).ToArray(),
    selectedCoreLibCaseLookup = selected.Select(type => new
    {
        fullName = type.FullName,
        lowerSensitive = ObserveGetType(type.FullName!.ToLowerInvariant(), false, false),
        lowerInsensitive = ObserveGetType(type.FullName!.ToLowerInvariant(), false, true),
        lowerQualifiedSensitive = ObserveGetType(type.AssemblyQualifiedName!.ToLowerInvariant(), false, false),
        lowerQualifiedInsensitive = ObserveGetType(type.AssemblyQualifiedName!.ToLowerInvariant(), false, true),
        lowerThrowSensitive = ObserveGetType(type.FullName!.ToLowerInvariant(), true, false),
        lowerThrowInsensitive = ObserveGetType(type.FullName!.ToLowerInvariant(), true, true),
        lowerQualifiedThrowSensitive = ObserveGetType(type.AssemblyQualifiedName!.ToLowerInvariant(), true, false),
        lowerQualifiedThrowInsensitive = ObserveGetType(type.AssemblyQualifiedName!.ToLowerInvariant(), true, true),
    }).ToArray(),
    completeDeclaredSurface = new[] { typeof(Type), typeof(Exception) }
        .Select(type => new
        {
            fullName = type.FullName,
            methods = type.GetMethods(declaredPublic)
                .OrderBy(method => method.Name, StringComparer.Ordinal)
                .ThenBy(method => method.ToString(), StringComparer.Ordinal)
                .Select(method => new
                {
                    name = method.Name,
                    signature = method.ToString(),
                    isStatic = method.IsStatic,
                    isSpecialName = method.IsSpecialName,
                    genericArity = method.GetGenericArguments().Length,
                    returnType = method.ReturnType.FullName ?? method.ReturnType.ToString(),
                    parameters = method.GetParameters().Select(parameter => new
                    {
                        name = parameter.Name,
                        type = parameter.ParameterType.FullName ?? parameter.ParameterType.ToString(),
                        isOut = parameter.IsOut,
                        isOptional = parameter.IsOptional,
                    }).ToArray(),
                }).ToArray(),
            properties = type.GetProperties(declaredPublic)
                .OrderBy(property => property.Name, StringComparer.Ordinal)
                .Select(property => new
                {
                    name = property.Name,
                    type = property.PropertyType.FullName ?? property.PropertyType.ToString(),
                    publicGetter = property.GetMethod?.IsPublic == true,
                    publicSetter = property.SetMethod?.IsPublic == true,
                    indexParameters = property.GetIndexParameters().Select(parameter => new
                    {
                        name = parameter.Name,
                        type = parameter.ParameterType.FullName ?? parameter.ParameterType.ToString(),
                    }).ToArray(),
                }).ToArray(),
            constructors = type.GetConstructors(declaredPublic)
                .OrderBy(constructor => constructor.ToString(), StringComparer.Ordinal)
                .Select(constructor => new
                {
                    signature = constructor.ToString(),
                    parameters = constructor.GetParameters().Select(parameter => new
                    {
                        name = parameter.Name,
                        type = parameter.ParameterType.FullName ?? parameter.ParameterType.ToString(),
                    }).ToArray(),
                }).ToArray(),
            fields = type.GetFields(declaredPublic)
                .OrderBy(field => field.Name, StringComparer.Ordinal)
                .Select(field => new
                {
                    name = field.Name,
                    type = field.FieldType.FullName ?? field.FieldType.ToString(),
                    isStatic = field.IsStatic,
                    isLiteral = field.IsLiteral,
                }).ToArray(),
            events = type.GetEvents(declaredPublic)
                .OrderBy(eventInfo => eventInfo.Name, StringComparer.Ordinal)
                .Select(eventInfo => new
                {
                    name = eventInfo.Name,
                    handlerType = eventInfo.EventHandlerType?.FullName,
                }).ToArray(),
            nestedPublicTypes = type.GetNestedTypes(BindingFlags.Public)
                .Select(nested => nested.FullName)
                .OrderBy(name => name, StringComparer.Ordinal)
                .ToArray(),
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
    selectedPrimitiveBehavior = new[]
    {
        typeof(object), typeof(string), typeof(int), typeof(decimal), typeof(DateTime),
        typeof(TypeCode), typeof(Array), typeof(IDisposable), typeof(string[]),
        typeof(List<>),
    }.Select(type => new
    {
        name = type.FullName,
        isPrimitive = type.IsPrimitive,
    }).ToArray(),
    selectedAbstractBehavior = new[]
    {
        typeof(object), typeof(string), typeof(int), typeof(Type), typeof(ValueType),
        typeof(Enum), typeof(Array), typeof(IDisposable), typeof(IComparable),
        typeof(List<>),
    }.Select(type => new
    {
        name = type.FullName,
        isAbstract = type.IsAbstract,
    }).ToArray(),
    selectedSealedBehavior = new[]
    {
        typeof(object), typeof(string), typeof(int), typeof(Type), typeof(ValueType),
        typeof(Array), typeof(IDisposable), typeof(TypeCode), typeof(decimal),
        typeof(List<>),
    }.Select(type => new
    {
        name = type.FullName,
        isSealed = type.IsSealed,
    }).ToArray(),
    selectedPublicBehavior = new[]
    {
        typeof(object), typeof(string), typeof(int), typeof(ValueType), typeof(Array),
        typeof(IComparable), typeof(List<>), typeof(List<string>), typeof(string[]),
        typeof(string).MakeByRefType(),
    }.Select(type => new
    {
        name = type.FullName,
        isPublic = type.IsPublic,
    }).ToArray(),
    selectedVisibleBehavior = new[]
    {
        typeof(object), typeof(string), typeof(int), typeof(Type), typeof(IDisposable),
        typeof(List<>), typeof(List<string>), typeof(string[]),
        typeof(string).MakeByRefType(), typeof(string).MakePointerType(),
        typeof(List<>).GetGenericArguments()[0],
    }.Select(type => new
    {
        name = type.FullName ?? type.Name,
        isVisible = type.IsVisible,
        isPublic = type.IsPublic,
    }).ToArray(),
    selectedGenericDefinitionBehavior = new[]
    {
        typeof(object), typeof(int), typeof(List<>), typeof(List<string>),
        typeof(Dictionary<,>), typeof(Dictionary<string, int>),
        typeof(List<>).GetGenericArguments()[0], typeof(string[]),
    }.Select(type => new
    {
        name = type.FullName ?? type.Name,
        isGenericTypeDefinition = type.IsGenericTypeDefinition,
    }).ToArray(),
    selectedGenericDefinitionErrorBehavior = new
    {
        objectType = ObserveGenericDefinitionError(typeof(object)),
        stringType = ObserveGenericDefinitionError(typeof(string)),
        parameter = ObserveGenericDefinitionError(typeof(List<>).GetGenericArguments()[0]),
        array = ObserveGenericDefinitionError(typeof(string[])),
    },
    selectedGenericArgumentCopyBehavior = ObserveGenericArgumentCopies(),
    selectedGenericParameterConstraintBehavior = new[]
    {
        typeof(List<>).GetGenericArguments()[0],
        typeof(Dictionary<,>).GetGenericArguments()[0],
        typeof(Dictionary<,>).GetGenericArguments()[1],
        typeof(object), typeof(List<>),
    }.Select(type => new
    {
        name = type.FullName ?? type.Name,
        observation = ObserveGenericParameterConstraints(type),
    }).ToArray(),
    selectedSzArrayBehavior = new[]
    {
        typeof(object), typeof(string[]), typeof(string[][]),
        typeof(string).MakeArrayType(1), typeof(string[,]), typeof(string[,,]),
        typeof(List<string>[]),
    }.Select(type => new
    {
        name = type.FullName,
        isSzArray = type.IsSZArray,
    }).ToArray(),
    selectedVariableBoundArrayBehavior = new[]
    {
        typeof(object), typeof(string[]), typeof(string[][]),
        typeof(string).MakeArrayType(1), typeof(string[,]), typeof(string[,,]),
        typeof(List<string>[]),
    }.Select(type => new
    {
        name = type.FullName,
        isVariableBoundArray = type.IsVariableBoundArray,
    }).ToArray(),
    selectedHasElementTypeBehavior = new[]
    {
        typeof(object), typeof(int), typeof(List<>), typeof(List<string>),
        typeof(string[]), typeof(string[,]), typeof(string).MakeArrayType(1),
        typeof(string).MakeByRefType(), typeof(string).MakePointerType(),
    }.Select(type => new
    {
        name = type.FullName,
        hasElementType = type.HasElementType,
        elementType = type.GetElementType()?.FullName,
    }).ToArray(),
    selectedTypeConstructionBoundaryBehavior = new
    {
        byRefVector = ObserveTypeConstruction(() => typeof(string).MakeByRefType().MakeArrayType()),
        byRefRankTwo = ObserveTypeConstruction(() => typeof(string).MakeByRefType().MakeArrayType(2)),
        pointerVector = ObserveTypeConstruction(() => typeof(string).MakePointerType().MakeArrayType()),
        pointerByRef = ObserveTypeConstruction(() => typeof(string).MakePointerType().MakeByRefType()),
        arrayByRef = ObserveTypeConstruction(() => typeof(string[]).MakeByRefType()),
        byRefPointer = ObserveTypeConstruction(() => typeof(string).MakeByRefType().MakePointerType()),
    },
    selectedNestedTypeNameBehavior = new
    {
        pointerArray = ObserveGetType("System.String*[]", false, false),
        pointerByRef = ObserveGetType("System.String*&", false, false),
        arrayByRef = ObserveGetType("System.String[]&", false, false),
        doublePointer = ObserveGetType("System.String**", false, false),
        byRefArray = ObserveGetType("System.String&[]", false, false),
        byRefArrayThrow = ObserveGetType("System.String&[]", true, false),
    },
    selectedQualifiedNestedNameBehavior = new
    {
        coreLibArray = ObserveGetType("System.String*[], System.Private.CoreLib", false, false),
        insensitiveArray = ObserveGetType("system.string*[], System.Private.CoreLib", false, true),
        sensitiveMiss = ObserveGetType("system.string*[], System.Private.CoreLib", false, false),
        legacyByRef = ObserveGetType("System.String*&, mscorlib", false, false),
        coreLibDoublePointer = ObserveGetType("System.String**, System.Private.CoreLib", false, false),
        invalidByRefArray = ObserveGetType("System.String&[], System.Private.CoreLib", false, false),
    },
    selectedCaseBoundaryBehavior = new
    {
        typeInsensitive = ObserveGetType("system.type", false, true),
        typeSensitive = ObserveGetType("system.type", false, false),
        operationInsensitive = ObserveGetType("system.invalidoperationexception", false, true),
        operationSensitive = ObserveGetType("system.invalidoperationexception", false, false),
        invalidNestedInsensitive = ObserveGetType("system.string&[]", false, true),
        invalidNestedSensitive = ObserveGetType("system.string&[]", false, false),
    },
    selectedAssemblyCaseBehavior = new
    {
        coreLibLower = ObserveGetType("System.String, system.private.corelib", false, false),
        coreLibUpper = ObserveGetType("System.String, SYSTEM.PRIVATE.CORELIB", false, false),
        legacyUpper = ObserveGetType("System.String, MSCORLIB", false, false),
        legacyMixed = ObserveGetType("System.String, MsCoRlIb", false, false),
        unknown = ObserveGetType("System.String, UnknownAssembly", false, false),
        unknownThrow = ObserveGetType("System.String, UnknownAssembly", true, false),
    },
    selectedAssemblyIdentityBehavior = new
    {
        canonical = ObserveGetType("System.String, System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e", false, false),
        versionMismatch = ObserveGetType("System.String, System.Private.CoreLib, Version=99.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e", false, false),
        cultureMismatch = ObserveGetType("System.String, System.Private.CoreLib, Version=10.0.0.0, Culture=en-US, PublicKeyToken=7cec85d7bea7798e", false, false),
        tokenMismatch = ObserveGetType("System.String, System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, PublicKeyToken=null", false, false),
        legacy = ObserveGetType("System.String, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089", false, false),
        mismatchThrow = ObserveGetType("System.String, System.Private.CoreLib, Version=99.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e", true, false),
    },
    selectedInvalidAssemblyAttributeBehavior = new
    {
        invalidVersion = ObserveGetType("System.String, System.Private.CoreLib, Version=banana", false, false),
        emptyCulture = ObserveGetType("System.String, System.Private.CoreLib, Culture=", false, false),
        invalidToken = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=xyz", false, false),
        unknownAttribute = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo", false, false),
        duplicateVersion = ObserveGetType("System.String, System.Private.CoreLib, Version=10.0.0.0, Version=11.0.0.0", false, false),
    },
    selectedAssemblyAttributeCasingBehavior = new
    {
        versionLower = ObserveGetType("System.String, System.Private.CoreLib, version=10.0.0.0", false, false),
        cultureUpper = ObserveGetType("System.String, System.Private.CoreLib, CULTURE=neutral", false, false),
        tokenMixed = ObserveGetType("System.String, System.Private.CoreLib, Publickeytoken=null", false, false),
        spacesAroundEquals = ObserveGetType("System.String, System.Private.CoreLib, Version = 10.0.0.0", false, false),
        spacesAfterComma = ObserveGetType("System.String, System.Private.CoreLib,  Version=10.0.0.0", false, false),
        unknownEmpty = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=", false, false),
        duplicateCulture = ObserveGetType("System.String, System.Private.CoreLib, Culture=neutral, Culture=en-US", false, false),
        versionOnePart = ObserveGetType("System.String, System.Private.CoreLib, Version=10", false, false),
        versionFivePart = ObserveGetType("System.String, System.Private.CoreLib, Version=1.2.3.4.5", false, false),
    },
    selectedAssemblyAttributeDelimiterBehavior = new
    {
        quotedCulture = ObserveGetType("System.String, System.Private.CoreLib, Culture=\"neutral\"", false, false),
        quotedVersion = ObserveGetType("System.String, System.Private.CoreLib, Version=\"10.0.0.0\"", false, false),
        trailingComma = ObserveGetType("System.String, System.Private.CoreLib, Version=10.0.0.0,", false, false),
        doubleComma = ObserveGetType("System.String, System.Private.CoreLib,, Version=10.0.0.0", false, false),
        emptyAttribute = ObserveGetType("System.String, System.Private.CoreLib,", false, false),
        extraEquals = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo=bar", false, false),
        unknownQuoted = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"foo\"", false, false),
        tokenQuoted = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=\"null\"", false, false),
    },
    selectedAssemblyVersionCultureBoundBehavior = new
    {
        versionTwoPart = ObserveGetType("System.String, System.Private.CoreLib, Version=1.2", false, false),
        versionThreePart = ObserveGetType("System.String, System.Private.CoreLib, Version=1.2.3", false, false),
        versionMaxComponent = ObserveGetType("System.String, System.Private.CoreLib, Version=65535.0.0.0", false, false),
        versionOverflow = ObserveGetType("System.String, System.Private.CoreLib, Version=65536.0.0.0", false, false),
        versionNegative = ObserveGetType("System.String, System.Private.CoreLib, Version=-1.0.0.0", false, false),
        cultureUnderscore = ObserveGetType("System.String, System.Private.CoreLib, Culture=en_US", false, false),
        cultureUnknown = ObserveGetType("System.String, System.Private.CoreLib, Culture=not-a-real-culture", false, false),
        cultureNumeric = ObserveGetType("System.String, System.Private.CoreLib, Culture=123", false, false),
    },
    selectedPublicKeyTokenBoundBehavior = new
    {
        upperHex = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=7CEC85D7BEA7798E", false, false),
        zeroHex = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=0000000000000000", false, false),
        upperNull = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=NULL", false, false),
        shortHex = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=123456789abcdef", false, false),
        longHex = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=123456789abcdef01", false, false),
        nonHex = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=gggggggggggggggg", false, false),
        quotedHex = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=\"7cec85d7bea7798e\"", false, false),
    },
    selectedAssemblyAttributeOrderBehavior = new
    {
        reversedKnown = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=null, Culture=neutral, Version=10.0.0.0", false, false),
        unknownBeforeKnown = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo, Version=10.0.0.0", false, false),
        unknownAfterKnown = ObserveGetType("System.String, System.Private.CoreLib, Version=10.0.0.0, UnknownAttr=foo", false, false),
        duplicateToken = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=null, PublicKeyToken=null", false, false),
        duplicateUnknown = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo, UnknownAttr=bar", false, false),
        duplicateVersionMixedCase = ObserveGetType("System.String, System.Private.CoreLib, Version=10.0.0.0, version=11.0.0.0", false, false),
    },
    selectedAssemblySimpleNameBoundaryBehavior = new
    {
        extraOuterSpace = ObserveGetType("System.String,  System.Private.CoreLib  ", false, false),
        quotedName = ObserveGetType("System.String, \"System.Private.CoreLib\"", false, false),
        fileExtension = ObserveGetType("System.String, System.Private.CoreLib.dll", false, false),
        embeddedSpace = ObserveGetType("System.String, System. Private.CoreLib", false, false),
        leadingDot = ObserveGetType("System.String, .System.Private.CoreLib", false, false),
        emptyBeforeAttribute = ObserveGetType("System.String, , Version=10.0.0.0", false, false),
        legacyOuterSpace = ObserveGetType("System.String,  mscorlib  ", false, false),
    },
    selectedLegacyAssemblyAliasBehavior = new
    {
        legacyDll = ObserveGetType("System.String, mscorlib.dll", false, false),
        legacyQuoted = ObserveGetType("System.String, \"mscorlib\"", false, false),
        legacyQuotedDll = ObserveGetType("System.String, \"mscorlib.dll\"", false, false),
        coreLibUpperDll = ObserveGetType("System.String, SYSTEM.PRIVATE.CORELIB.DLL", false, false),
        legacyExe = ObserveGetType("System.String, mscorlib.exe", false, false),
        legacyWithVersion = ObserveGetType("System.String, \"mscorlib.dll\", Version=4.0.0.0", false, false),
    },
    selectedAssemblyThrowBoundaryBehavior = new
    {
        legacyDllThrow = ObserveGetType("System.String, mscorlib.dll", true, false),
        embeddedSpaceThrow = ObserveGetType("System.String, System. Private.CoreLib", true, false),
        emptyBeforeAttributeThrow = ObserveGetType("System.String, , Version=10.0.0.0", true, false),
        invalidVersionThrow = ObserveGetType("System.String, System.Private.CoreLib, Version=banana", true, false),
        numericCultureThrow = ObserveGetType("System.String, System.Private.CoreLib, Culture=123", true, false),
        acceptedUnknownThrow = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo", true, false),
    },
    selectedAssemblyValueWhitespaceBehavior = new
    {
        versionOuterSpaces = ObserveGetType("System.String, System.Private.CoreLib, Version= 10.0.0.0 ", false, false),
        versionInnerSpace = ObserveGetType("System.String, System.Private.CoreLib, Version=10.0 .0.0", false, false),
        cultureOuterSpaces = ObserveGetType("System.String, System.Private.CoreLib, Culture= neutral ", false, false),
        cultureInnerSpace = ObserveGetType("System.String, System.Private.CoreLib, Culture=en US", false, false),
        tokenOuterSpaces = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken= 7cec85d7bea7798e ", false, false),
        tokenInnerSpace = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=7cec85d7 bea7798e", false, false),
        unknownInnerSpace = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo bar", false, false),
    },
    selectedQuotedAssemblyValueBoundaryBehavior = new
    {
        emptyQuotedCulture = ObserveGetType("System.String, System.Private.CoreLib, Culture=\"\"", false, false),
        emptyQuotedUnknown = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"\"", false, false),
        unclosedCulture = ObserveGetType("System.String, System.Private.CoreLib, Culture=\"neutral", false, false),
        trailingQuoteCulture = ObserveGetType("System.String, System.Private.CoreLib, Culture=neutral\"", false, false),
        quotedCultureWithSpace = ObserveGetType("System.String, System.Private.CoreLib, Culture=\"en US\"", false, false),
        quotedUnknownWithComma = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"foo,bar\"", false, false),
    },
    selectedQuotedAssemblyDelimiterBehavior = new
    {
        unknownManyCommas = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"a,b,c\"", false, false),
        unknownEquals = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"a=b\"", false, false),
        cultureComma = ObserveGetType("System.String, System.Private.CoreLib, Culture=\"en,US\"", false, false),
        versionComma = ObserveGetType("System.String, System.Private.CoreLib, Version=\"1,2\"", false, false),
        tokenComma = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=\"01234567,89abcdef\"", false, false),
    },
    selectedEscapedAssemblyQuoteBehavior = new
    {
        unknownBackslashQuote = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"a\\\"b\"", false, false),
        unknownDoubledQuote = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"a\"\"b\"", false, false),
        unknownBackslash = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"a\\\\b\"", false, false),
        cultureBackslashQuote = ObserveGetType("System.String, System.Private.CoreLib, Culture=\"en\\\"US\"", false, false),
    },
    selectedAssemblyAttributeKeyBoundaryBehavior = new
    {
        versionKeySpaces = ObserveGetType("System.String, System.Private.CoreLib,  Version  =10.0.0.0", false, false),
        cultureKeySpaces = ObserveGetType("System.String, System.Private.CoreLib, Culture  =neutral", false, false),
        tokenKeySpaces = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken =null", false, false),
        unknownKeySpace = ObserveGetType("System.String, System.Private.CoreLib, Unknown Attr=foo", false, false),
        unknownKeyDot = ObserveGetType("System.String, System.Private.CoreLib, Unknown.Attr=foo", false, false),
        emptyKey = ObserveGetType("System.String, System.Private.CoreLib, =foo", false, false),
        versionKeyHyphen = ObserveGetType("System.String, System.Private.CoreLib, Ver-sion=10.0.0.0", false, false),
    },
    selectedUnknownAssemblyAttributeValueBehavior = new
    {
        colon = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo:bar", false, false),
        slash = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo/bar", false, false),
        semicolon = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo;bar", false, false),
        question = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo?bar", false, false),
        unquotedEquals = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo=bar", false, false),
        duplicateMixedCase = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=foo, unknownattr=bar", false, false),
    },
    selectedProcessorArchitectureAttributeBehavior = new
    {
        msil = ObserveGetType("System.String, System.Private.CoreLib, ProcessorArchitecture=MSIL", false, false),
        x86 = ObserveGetType("System.String, System.Private.CoreLib, ProcessorArchitecture=X86", false, false),
        amd64 = ObserveGetType("System.String, System.Private.CoreLib, ProcessorArchitecture=Amd64", false, false),
        none = ObserveGetType("System.String, System.Private.CoreLib, ProcessorArchitecture=None", false, false),
        unknown = ObserveGetType("System.String, System.Private.CoreLib, ProcessorArchitecture=xyz", false, false),
        duplicate = ObserveGetType("System.String, System.Private.CoreLib, ProcessorArchitecture=MSIL, ProcessorArchitecture=X86", false, false),
    },
    selectedRetargetableAttributeBehavior = new
    {
        yes = ObserveGetType("System.String, System.Private.CoreLib, Retargetable=Yes", false, false),
        no = ObserveGetType("System.String, System.Private.CoreLib, Retargetable=No", false, false),
        trueValue = ObserveGetType("System.String, System.Private.CoreLib, Retargetable=true", false, false),
        falseValue = ObserveGetType("System.String, System.Private.CoreLib, Retargetable=false", false, false),
        numeric = ObserveGetType("System.String, System.Private.CoreLib, Retargetable=1", false, false),
        duplicate = ObserveGetType("System.String, System.Private.CoreLib, Retargetable=Yes, Retargetable=No", false, false),
    },
    selectedContentTypeAttributeBehavior = new
    {
        defaultValue = ObserveGetType("System.String, System.Private.CoreLib, ContentType=Default", false, false),
        windowsRuntime = ObserveGetType("System.String, System.Private.CoreLib, ContentType=WindowsRuntime", false, false),
        lowerDefault = ObserveGetType("System.String, System.Private.CoreLib, contenttype=default", false, false),
        unknown = ObserveGetType("System.String, System.Private.CoreLib, ContentType=xyz", false, false),
        numeric = ObserveGetType("System.String, System.Private.CoreLib, ContentType=1", false, false),
        duplicate = ObserveGetType("System.String, System.Private.CoreLib, ContentType=Default, ContentType=WindowsRuntime", false, false),
    },
    selectedMixedAssemblyIdentityBehavior = new
    {
        allValid = ObserveGetType("System.String, System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, PublicKeyToken=null, ProcessorArchitecture=MSIL, Retargetable=No, ContentType=WindowsRuntime", false, false),
        invalidVersionFirst = ObserveGetType("System.String, System.Private.CoreLib, Version=banana, Culture=123", false, false),
        invalidCultureFirst = ObserveGetType("System.String, System.Private.CoreLib, Culture=123, Version=banana", false, false),
        unknownAssemblyInvalidVersion = ObserveGetType("System.String, Missing.Assembly, Version=banana", false, false),
        unknownAssemblyInvalidVersionThrow = ObserveGetType("System.String, Missing.Assembly, Version=banana", true, false),
        invalidContentFirst = ObserveGetType("System.String, System.Private.CoreLib, ContentType=Default, Version=banana", false, false),
    },
    selectedUnknownAssemblyAttributeBehavior = new
    {
        validVersion = ObserveGetType("System.String, Missing.Assembly, Version=10.0.0.0", false, false),
        validVersionThrow = ObserveGetType("System.String, Missing.Assembly, Version=10.0.0.0", true, false),
        invalidCulture = ObserveGetType("System.String, Missing.Assembly, Culture=123", false, false),
        invalidToken = ObserveGetType("System.String, Missing.Assembly, PublicKeyToken=xyz", false, false),
        unknownAttribute = ObserveGetType("System.String, Missing.Assembly, UnknownAttr=foo", false, false),
        unknownAttributeThrow = ObserveGetType("System.String, Missing.Assembly, UnknownAttr=foo", true, false),
        duplicateVersion = ObserveGetType("System.String, Missing.Assembly, Version=1.2.3.4, Version=2.3.4.5", false, false),
    },
    selectedAssemblyAttributeAliasBehavior = new
    {
        lowerArchitecture = ObserveGetType("System.String, System.Private.CoreLib, processorarchitecture=msil", false, false),
        upperRetargetable = ObserveGetType("System.String, System.Private.CoreLib, RETARGETABLE=YES", false, false),
        lowerContentType = ObserveGetType("System.String, System.Private.CoreLib, contenttype=windowsruntime", false, false),
        publicKeyNull = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=null", false, false),
        publicKeyGarbage = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=xyz", false, false),
        cultureInfoAlias = ObserveGetType("System.String, System.Private.CoreLib, CultureInfo=neutral", false, false),
        duplicateRetargetableCase = ObserveGetType("System.String, System.Private.CoreLib, Retargetable=Yes, retargetable=No", false, false),
    },
    selectedPublicKeyValueBehavior = new
    {
        zeroByte = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=00", false, false),
        oneNibble = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=0", false, false),
        twoBytes = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=0011", false, false),
        eightBytes = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=0011223344556677", false, false),
        sixteenBytes = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=00112233445566778899aabbccddeeff", false, false),
        nonHex = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=gg", false, false),
        upperNull = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=NULL", false, false),
    },
    selectedPublicKeyTokenInteractionBehavior = new
    {
        bothNull = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=null, PublicKeyToken=null", false, false),
        keyThenNullToken = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=00, PublicKeyToken=null", false, false),
        tokenThenKey = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=null, PublicKey=00", false, false),
        keyThenToken = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=00, PublicKeyToken=7cec85d7bea7798e", false, false),
        tokenThenInvalidKey = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=null, PublicKey=xyz", false, false),
        invalidTokenThenKey = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=xyz, PublicKey=00", false, false),
    },
    selectedCultureNameBoundaryBehavior = new
    {
        titleNeutral = ObserveGetType("System.String, System.Private.CoreLib, Culture=Neutral", false, false),
        upperNeutral = ObserveGetType("System.String, System.Private.CoreLib, Culture=NEUTRAL", false, false),
        lowerLocale = ObserveGetType("System.String, System.Private.CoreLib, Culture=en-us", false, false),
        upperLocale = ObserveGetType("System.String, System.Private.CoreLib, Culture=EN-US", false, false),
        invariant = ObserveGetType("System.String, System.Private.CoreLib, Culture=invariant", false, false),
        nullText = ObserveGetType("System.String, System.Private.CoreLib, Culture=null", false, false),
        shortLocale = ObserveGetType("System.String, System.Private.CoreLib, Culture=iv", false, false),
    },
    selectedCultureSeparatorBehavior = new
    {
        underscore = ObserveGetType("System.String, System.Private.CoreLib, Culture=en_US", false, false),
        dot = ObserveGetType("System.String, System.Private.CoreLib, Culture=en.US", false, false),
        doubleHyphen = ObserveGetType("System.String, System.Private.CoreLib, Culture=en--US", false, false),
        trailingHyphen = ObserveGetType("System.String, System.Private.CoreLib, Culture=en-", false, false),
        leadingHyphen = ObserveGetType("System.String, System.Private.CoreLib, Culture=-US", false, false),
        slash = ObserveGetType("System.String, System.Private.CoreLib, Culture=en/US", false, false),
        atSign = ObserveGetType("System.String, System.Private.CoreLib, Culture=en@US", false, false),
    },
    selectedCultureUnicodeBoundaryBehavior = new
    {
        swissFrench = ObserveGetType("System.String, System.Private.CoreLib, Culture=fr-CH", false, false),
        scriptTag = ObserveGetType("System.String, System.Private.CoreLib, Culture=zh-Hant", false, false),
        numericTag = ObserveGetType("System.String, System.Private.CoreLib, Culture=123", false, false),
        arabicDigits = ObserveGetType("System.String, System.Private.CoreLib, Culture=١٢٣", false, false),
        accentedName = ObserveGetType("System.String, System.Private.CoreLib, Culture=é", false, false),
        japanese = ObserveGetType("System.String, System.Private.CoreLib, Culture=ja-JP", false, false),
    },
    selectedVersionComponentBoundaryBehavior = new
    {
        leadingZeros = ObserveGetType("System.String, System.Private.CoreLib, Version=0001.0002", false, false),
        zeroPair = ObserveGetType("System.String, System.Private.CoreLib, Version=0.0", false, false),
        maxPair = ObserveGetType("System.String, System.Private.CoreLib, Version=65534.65534", false, false),
        overflowPair = ObserveGetType("System.String, System.Private.CoreLib, Version=65535.0", false, false),
        manyLeadingZeros = ObserveGetType("System.String, System.Private.CoreLib, Version=0000001.0", false, false),
        integerOverflow = ObserveGetType("System.String, System.Private.CoreLib, Version=2147483648.0", false, false),
    },
    selectedVersionGrammarBoundaryBehavior = new
    {
        plusSign = ObserveGetType("System.String, System.Private.CoreLib, Version=+1.2", false, false),
        negativeSign = ObserveGetType("System.String, System.Private.CoreLib, Version=-1.2", false, false),
        spaceBeforeDot = ObserveGetType("System.String, System.Private.CoreLib, Version=1 .2", false, false),
        spaceAfterDot = ObserveGetType("System.String, System.Private.CoreLib, Version=1. 2", false, false),
        fourParts = ObserveGetType("System.String, System.Private.CoreLib, Version=1.2.3.4", false, false),
        fiveParts = ObserveGetType("System.String, System.Private.CoreLib, Version=1.2.3.4.5", false, false),
        emptyMiddle = ObserveGetType("System.String, System.Private.CoreLib, Version=1..2", false, false),
    },
    selectedKnownAssemblyAttributeOrderBehavior = new
    {
        contentThenRetargetable = ObserveGetType("System.String, System.Private.CoreLib, ContentType=WindowsRuntime, Retargetable=Yes", false, false),
        retargetableThenContent = ObserveGetType("System.String, System.Private.CoreLib, Retargetable=Yes, ContentType=WindowsRuntime", false, false),
        architectureThenRetargetable = ObserveGetType("System.String, System.Private.CoreLib, ProcessorArchitecture=X86, Retargetable=Yes", false, false),
        retargetableThenVersion = ObserveGetType("System.String, System.Private.CoreLib, Retargetable=No, Version=1.2", false, false),
        cultureThenInvalidToken = ObserveGetType("System.String, System.Private.CoreLib, Culture=123, PublicKeyToken=xyz", false, false),
        invalidTokenThenCulture = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=xyz, Culture=123", false, false),
    },
    selectedAssemblyAttributeCollisionBehavior = new
    {
        cultureAndCultureInfo = ObserveGetType("System.String, System.Private.CoreLib, Culture=neutral, CultureInfo=neutral", false, false),
        versionAndHyphenAlias = ObserveGetType("System.String, System.Private.CoreLib, Version=1.2, Ver-sion=3.4", false, false),
        duplicateTokenCase = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=null, publickeytoken=null", false, false),
        duplicateArchitectureCase = ObserveGetType("System.String, System.Private.CoreLib, ProcessorArchitecture=MSIL, processorarchitecture=X86", false, false),
        duplicatePublicKeyCase = ObserveGetType("System.String, System.Private.CoreLib, PublicKey=00, publickey=11", false, false),
        duplicateContentCase = ObserveGetType("System.String, System.Private.CoreLib, ContentType=WindowsRuntime, contenttype=WindowsRuntime", false, false),
    },
    selectedAssemblySimpleNameQuoteBehavior = new
    {
        quotedOuterSpaces = ObserveGetType("System.String,  \"System.Private.CoreLib\"  ", false, false),
        quotedInnerSpaces = ObserveGetType("System.String, \" System.Private.CoreLib \"", false, false),
        spaceBeforeDll = ObserveGetType("System.String, System.Private.CoreLib .dll", false, false),
        quotedDll = ObserveGetType("System.String, \"System.Private.CoreLib.dll\"", false, false),
        singleQuotes = ObserveGetType("System.String, 'System.Private.CoreLib'", false, false),
        quotedUnknown = ObserveGetType("System.String, \"Missing.Assembly\"", false, false),
    },
    selectedUnbalancedAssemblyQuoteBehavior = new
    {
        missingDoubleClose = ObserveGetType("System.String, \"System.Private.CoreLib", false, false),
        missingDoubleOpen = ObserveGetType("System.String, System.Private.CoreLib\"", false, false),
        missingSingleClose = ObserveGetType("System.String, 'System.Private.CoreLib", false, false),
        missingSingleOpen = ObserveGetType("System.String, System.Private.CoreLib'", false, false),
        nestedDoubleInSingle = ObserveGetType("System.String, '\"System.Private.CoreLib\"'", false, false),
        nestedSingleInDouble = ObserveGetType("System.String, \"'System.Private.CoreLib'\"", false, false),
    },
    selectedAssemblyNamePunctuationBehavior = new
    {
        quotedComma = ObserveGetType("System.String, \"System.Private.CoreLib,Extra\"", false, false),
        quotedEquals = ObserveGetType("System.String, \"System.Private.CoreLib=Extra\"", false, false),
        unquotedEquals = ObserveGetType("System.String, System.Private.CoreLib=Extra", false, false),
        semicolon = ObserveGetType("System.String, System.Private.CoreLib;Extra", false, false),
        slash = ObserveGetType("System.String, System.Private.CoreLib/Extra", false, false),
        canonicalWithVersion = ObserveGetType("System.String, System.Private.CoreLib, Version=1.2", false, false),
    },
    selectedAssemblyUnicodeCaseBehavior = new
    {
        asciiUpper = ObserveGetType("System.String, SYSTEM.PRIVATE.CORELIB", false, false),
        asciiMixed = ObserveGetType("System.String, SyStEm.PrIvAtE.CoReLiB", false, false),
        dotlessI = ObserveGetType("System.String, System.Prıvate.CoreLib", false, false),
        dottedUpperI = ObserveGetType("System.String, System.Prİvate.CoreLib", false, false),
        accentedE = ObserveGetType("System.String, Systém.Private.CoreLib", false, false),
        fullwidthM = ObserveGetType("System.String, ｍscorlib", false, false),
    },
    selectedAssemblyAttributeUnicodeKeyBehavior = new
    {
        dotlessVersion = ObserveGetType("System.String, System.Private.CoreLib, Versıon=banana", false, false),
        dottedUpperVersion = ObserveGetType("System.String, System.Private.CoreLib, VERSİON=banana", false, false),
        dotlessToken = ObserveGetType("System.String, System.Private.CoreLib, PublıcKeyToken=xyz", false, false),
        accentedRetargetable = ObserveGetType("System.String, System.Private.CoreLib, Retargetablé=blah", false, false),
        unicodeThenVersion = ObserveGetType("System.String, System.Private.CoreLib, Versıon=banana, Version=1.2", false, false),
        versionThenUnicode = ObserveGetType("System.String, System.Private.CoreLib, Version=1.2, VERSİON=banana", false, false),
    },
    selectedAssemblyAttributeUnicodeValueBehavior = new
    {
        accentedRetargetable = ObserveGetType("System.String, System.Private.CoreLib, Retargetable=Yés", false, false),
        dottedArchitecture = ObserveGetType("System.String, System.Private.CoreLib, ProcessorArchitecture=MSİL", false, false),
        dotlessContent = ObserveGetType("System.String, System.Private.CoreLib, ContentType=WındowsRuntime", false, false),
        accentedTokenNull = ObserveGetType("System.String, System.Private.CoreLib, PublicKeyToken=nüll", false, false),
        asciiContent = ObserveGetType("System.String, System.Private.CoreLib, ContentType=WINDOWSRUNTIME", false, false),
        unicodeUnknown = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=é", false, false),
    },
    selectedAssemblyAliasSuffixBehavior = new
    {
        upperDll = ObserveGetType("System.String, System.Private.CoreLib.DLL", false, false),
        lowerDll = ObserveGetType("System.String, system.private.corelib.dll", false, false),
        quotedUpperDll = ObserveGetType("System.String, \"SYSTEM.PRIVATE.CORELIB.DLL\"", false, false),
        singleQuotedDll = ObserveGetType("System.String, 'System.Private.CoreLib.dll'", false, false),
        legacyUpperDll = ObserveGetType("System.String, mscorlib.DLL", false, false),
        legacySingleQuotedDll = ObserveGetType("System.String, 'mscorlib.dll'", false, false),
    },
    selectedQuotedAssemblyNameAttributeBehavior = new
    {
        doubleVersion = ObserveGetType("System.String, \"System.Private.CoreLib\", Version=1.2", false, false),
        singleVersion = ObserveGetType("System.String, 'System.Private.CoreLib', Version=1.2", false, false),
        quotedDllVersion = ObserveGetType("System.String, \"System.Private.CoreLib.dll\", Version=1.2", false, false),
        quotedUnknownAttribute = ObserveGetType("System.String, \"System.Private.CoreLib\", UnknownAttr=foo", false, false),
        quotedInvalidVersion = ObserveGetType("System.String, \"System.Private.CoreLib\", Version=banana", false, false),
        quotedCommaVersion = ObserveGetType("System.String, \"System.Private.CoreLib,Extra\", Version=1.2", false, false),
    },
    selectedQuotedAssemblyNamePunctuationBehavior = new
    {
        singleQuotedComma = ObserveGetType("System.String, 'System.Private.CoreLib,Extra'", false, false),
        commaUnknownAttribute = ObserveGetType("System.String, \"System.Private.CoreLib,Extra\", UnknownAttr=foo", false, false),
        commaInvalidVersion = ObserveGetType("System.String, \"System.Private.CoreLib,Extra\", Version=banana", false, false),
        quotedEqualsVersion = ObserveGetType("System.String, \"System.Private.CoreLib=Extra\", Version=1.2", false, false),
        singleQuotedEquals = ObserveGetType("System.String, 'System.Private.CoreLib=Extra'", false, false),
        quotedCommaToken = ObserveGetType("System.String, \"System.Private.CoreLib,Extra\", PublicKeyToken=null", false, false),
    },
    selectedEscapedAssemblyNameSeparatorBehavior = new
    {
        quotedEscapedComma = ObserveGetType("System.String, \"System.Private.CoreLib\\,Extra\"", false, false),
        singleEscapedComma = ObserveGetType("System.String, 'System.Private.CoreLib\\,Extra'", false, false),
        unquotedEscapedComma = ObserveGetType("System.String, System.Private.CoreLib\\,Extra", false, false),
        quotedEscapedEquals = ObserveGetType("System.String, \"System.Private.CoreLib\\=Extra\"", false, false),
        quotedBackslash = ObserveGetType("System.String, \"System.Private.CoreLib\\\\Extra\"", false, false),
    },
    selectedEscapedAssemblyNameAttributeBehavior = new
    {
        unquotedVersion = ObserveGetType("System.String, System.Private.CoreLib\\,Extra, Version=1.2", false, false),
        doubleQuotedVersion = ObserveGetType("System.String, \"System.Private.CoreLib\\,Extra\", Version=1.2", false, false),
        singleQuotedVersion = ObserveGetType("System.String, 'System.Private.CoreLib\\,Extra', Version=1.2", false, false),
        unquotedUnknown = ObserveGetType("System.String, System.Private.CoreLib\\,Extra, UnknownAttr=foo", false, false),
        unquotedInvalidVersion = ObserveGetType("System.String, System.Private.CoreLib\\,Extra, Version=banana", false, false),
    },
    selectedEscapedAssemblyNameQuoteBehavior = new
    {
        doubleEmbedded = ObserveGetType("System.String, \"System.Private.CoreLib\\\"Extra\"", false, false),
        singleEmbedded = ObserveGetType("System.String, 'System.Private.CoreLib\\'Extra'", false, false),
        unquotedDouble = ObserveGetType("System.String, System.Private.CoreLib\\\"", false, false),
        unquotedSingle = ObserveGetType("System.String, System.Private.CoreLib\\'", false, false),
        doubleWithVersion = ObserveGetType("System.String, \"System.Private.CoreLib\\\"Extra\", Version=1.2", false, false),
        singleWithVersion = ObserveGetType("System.String, 'System.Private.CoreLib\\'Extra', Version=1.2", false, false),
    },
    selectedAssemblySeparatorEscapeParityBehavior = new
    {
        unquotedTwo = ObserveGetType("System.String, System.Private.CoreLib\\\\,Extra", false, false),
        unquotedThree = ObserveGetType("System.String, System.Private.CoreLib\\\\\\,Extra", false, false),
        unquotedFour = ObserveGetType("System.String, System.Private.CoreLib\\\\\\\\,Extra", false, false),
        quotedTwo = ObserveGetType("System.String, \"System.Private.CoreLib\\\\,Extra\"", false, false),
        quotedThree = ObserveGetType("System.String, \"System.Private.CoreLib\\\\\\,Extra\"", false, false),
        singleTwo = ObserveGetType("System.String, 'System.Private.CoreLib\\\\,Extra'", false, false),
    },
    selectedAssemblyQuoteEscapeParityBehavior = new
    {
        doubleTwo = ObserveGetType("System.String, \"System.Private.CoreLib\\\\\"", false, false),
        doubleThree = ObserveGetType("System.String, \"System.Private.CoreLib\\\\\\\"", false, false),
        singleTwo = ObserveGetType("System.String, 'System.Private.CoreLib\\\\'", false, false),
        singleThree = ObserveGetType("System.String, 'System.Private.CoreLib\\\\\\'", false, false),
        unquotedDoubleTwo = ObserveGetType("System.String, System.Private.CoreLib\\\\\"", false, false),
        unquotedDoubleThree = ObserveGetType("System.String, System.Private.CoreLib\\\\\\\"", false, false),
    },
    selectedAssemblyAttributeEscapeParityBehavior = new
    {
        quotedTwo = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"a\\\\\", Version=1.2", false, false),
        quotedThree = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"a\\\\\\\", Version=1.2", false, false),
        unquotedTwo = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=a\\\\, Version=1.2", false, false),
        unquotedThree = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=a\\\\\\, Version=1.2", false, false),
        quotedCommaTwo = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"a\\\\,b\", Version=1.2", false, false),
        quotedCommaThree = ObserveGetType("System.String, System.Private.CoreLib, UnknownAttr=\"a\\\\\\,b\", Version=1.2", false, false),
    },
    selectedEscapedMissingAssemblyAttributePrecedence = new
    {
        quotedValid = ObserveGetType("System.String, \"Missing\\\"Assembly\", Version=1.2", false, false),
        quotedInvalidVersion = ObserveGetType("System.String, \"Missing\\\"Assembly\", Version=banana", false, false),
        escapedCommaValid = ObserveGetType("System.String, Missing\\,Assembly, Version=1.2", false, false),
        escapedCommaInvalidVersion = ObserveGetType("System.String, Missing\\,Assembly, Version=banana", false, false),
        evenBackslashInvalidVersion = ObserveGetType("System.String, Missing\\\\, Version=banana", false, false),
        evenBackslashInvalidCulture = ObserveGetType("System.String, Missing\\\\, Culture=123", false, false),
    },
    selectedEscapedAssemblyThrowOnErrorBehavior = new
    {
        quotedMissing = ObserveGetType("System.String, \"Missing\\\"Assembly\", Version=1.2", true, false),
        escapedCommaMissing = ObserveGetType("System.String, Missing\\,Assembly, Version=1.2", true, false),
        quotedInvalidVersion = ObserveGetType("System.String, \"Missing\\\"Assembly\", Version=banana", true, false),
        escapedCommaInvalidVersion = ObserveGetType("System.String, Missing\\,Assembly, Version=banana", true, false),
        evenBackslashInvalidCulture = ObserveGetType("System.String, Missing\\\\, Culture=123", true, false),
        escapedAlias = ObserveGetType("System.String, System.Private.CoreLib\\,Extra, Version=1.2", true, false),
    },
    selectedEscapedAssemblyMixedErrorPrecedence = new
    {
        cultureThenVersion = ObserveGetType("System.String, \"Missing\\\"Assembly\", Culture=123, Version=banana", false, false),
        versionThenCulture = ObserveGetType("System.String, \"Missing\\\"Assembly\", Version=banana, Culture=123", false, false),
        unknownEqualsThenCulture = ObserveGetType("System.String, Missing\\,Assembly, UnknownAttr=foo=bar, Culture=123", false, false),
        escapedAliasMixed = ObserveGetType("System.String, System.Private.CoreLib\\,Extra, Culture=123, Version=banana", false, false),
        evenBackslashMixed = ObserveGetType("System.String, Missing\\\\, Version=banana, Culture=123", false, false),
        cultureThenUnknownEquals = ObserveGetType("System.String, Missing\\,Assembly, Culture=123, UnknownAttr=foo=bar", false, false),
    },
    selectedContainsGenericParametersBehavior = new[]
    {
        typeof(object), typeof(List<>), typeof(List<string>), typeof(Dictionary<,>),
        typeof(Dictionary<string, int>), typeof(List<>).GetGenericArguments()[0],
        typeof(List<>).MakeArrayType(),
        typeof(List<>).MakeGenericType(typeof(List<>).GetGenericArguments()[0]),
    }.Select(type => new
    {
        name = type.FullName ?? type.Name,
        containsGenericParameters = type.ContainsGenericParameters,
    }).ToArray(),
    selectedEnumBaseBehavior = new
    {
        enumBase = typeof(MemberTypes).BaseType?.FullName,
        baseBase = typeof(Enum).BaseType?.FullName,
        underlying = typeof(MemberTypes).GetEnumUnderlyingType().FullName,
        nonEnumError = ObserveNonEnumUnderlying(),
    },
    selectedTypeCodeValues = Enum.GetValues<TypeCode>()
        .Select(value => new { name = value.ToString(), number = (int)value }).ToArray(),
    selectedDecimalBehavior = new
    {
        intText = new decimal(42).ToString(System.Globalization.CultureInfo.InvariantCulture),
        fractionalText = new decimal(42, 0, 0, false, 1)
            .ToString(System.Globalization.CultureInfo.InvariantCulture),
        intBits = decimal.GetBits(new decimal(42)),
        isValueType = typeof(decimal).IsValueType,
        baseType = typeof(decimal).BaseType?.FullName,
    },
    selectedDateTimeBehavior = new
    {
        year = new DateTime(2026, 1, 2).Year,
        month = new DateTime(2026, 1, 2).Month,
        day = new DateTime(2026, 1, 2).Day,
        text = new DateTime(2026, 1, 2)
            .ToString("yyyy-MM-dd", System.Globalization.CultureInfo.InvariantCulture),
        isValueType = typeof(DateTime).IsValueType,
        baseType = typeof(DateTime).BaseType?.FullName,
    },
    selectedInt32Behavior = new
    {
        typeCode = ((IConvertible)42).GetTypeCode().ToString(),
        booleanValue = ((IConvertible)42).ToBoolean(System.Globalization.CultureInfo.InvariantCulture),
        charValue = ((IConvertible)42).ToChar(System.Globalization.CultureInfo.InvariantCulture),
        intValue = ((IConvertible)42).ToInt32(System.Globalization.CultureInfo.InvariantCulture),
        decimalText = ((IConvertible)42).ToDecimal(System.Globalization.CultureInfo.InvariantCulture)
            .ToString(System.Globalization.CultureInfo.InvariantCulture),
        text = ((IConvertible)42).ToString(System.Globalization.CultureInfo.InvariantCulture),
        formattedText = ((IFormattable)42).ToString("D", System.Globalization.CultureInfo.InvariantCulture),
        compareTo41 = ((IComparable)42).CompareTo(41),
    },
    selectedInt32FormatBehavior = new
    {
        decimal5 = ((IFormattable)42).ToString("D5", System.Globalization.CultureInfo.InvariantCulture),
        hexUpper4 = ((IFormattable)42).ToString("X4", System.Globalization.CultureInfo.InvariantCulture),
        hexLower4 = ((IFormattable)42).ToString("x4", System.Globalization.CultureInfo.InvariantCulture),
        negativeDecimal5 = ((IFormattable)(-42)).ToString("D5", System.Globalization.CultureInfo.InvariantCulture),
        negativeHex = ((IFormattable)(-1)).ToString("X", System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32NumberFormatBehavior = new
    {
        groupedInteger = ((IFormattable)12345).ToString("N0",
            System.Globalization.CultureInfo.InvariantCulture),
        groupedTwoDecimals = ((IFormattable)12345).ToString("N2",
            System.Globalization.CultureInfo.InvariantCulture),
        lowerCase = ((IFormattable)12345).ToString("n2",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-12345)).ToString("N2",
            System.Globalization.CultureInfo.InvariantCulture),
        defaultPrecision = ((IFormattable)42).ToString("N",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32CurrencyFormatBehavior = new
    {
        defaultPrecision = ((IFormattable)12345).ToString("C",
            System.Globalization.CultureInfo.InvariantCulture),
        zeroPrecision = ((IFormattable)12345).ToString("C0",
            System.Globalization.CultureInfo.InvariantCulture),
        lowerCase = ((IFormattable)12345).ToString("c2",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-12345)).ToString("C2",
            System.Globalization.CultureInfo.InvariantCulture),
        small = ((IFormattable)42).ToString("C",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32FixedFormatBehavior = new
    {
        zeroPrecision = ((IFormattable)12345).ToString("F0",
            System.Globalization.CultureInfo.InvariantCulture),
        twoDecimals = ((IFormattable)12345).ToString("F2",
            System.Globalization.CultureInfo.InvariantCulture),
        lowerCase = ((IFormattable)12345).ToString("f2",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-12345)).ToString("F2",
            System.Globalization.CultureInfo.InvariantCulture),
        defaultPrecision = ((IFormattable)42).ToString("F",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32PercentFormatBehavior = new
    {
        defaultPrecision = ((IFormattable)123).ToString("P",
            System.Globalization.CultureInfo.InvariantCulture),
        zeroPrecision = ((IFormattable)123).ToString("P0",
            System.Globalization.CultureInfo.InvariantCulture),
        lowerCase = ((IFormattable)123).ToString("p2",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-123)).ToString("P2",
            System.Globalization.CultureInfo.InvariantCulture),
        small = ((IFormattable)42).ToString("P",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32GeneralFormatBehavior = new
    {
        defaultFormat = ((IFormattable)42).ToString("G",
            System.Globalization.CultureInfo.InvariantCulture),
        paddedPrecision = ((IFormattable)42).ToString("G5",
            System.Globalization.CultureInfo.InvariantCulture),
        lowerCase = ((IFormattable)42).ToString("g5",
            System.Globalization.CultureInfo.InvariantCulture),
        zeroPrecision = ((IFormattable)42).ToString("G0",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-42)).ToString("G5",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32BinaryFormatBehavior = new
    {
        binary = ((IFormattable)42).ToString("B",
            System.Globalization.CultureInfo.InvariantCulture),
        binary8 = ((IFormattable)42).ToString("B8",
            System.Globalization.CultureInfo.InvariantCulture),
        lowerCase = ((IFormattable)42).ToString("b8",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-1)).ToString("B",
            System.Globalization.CultureInfo.InvariantCulture),
        roundTripError = ObserveInt32FormatError("R"),
        roundTripResult = ((IFormattable)42).ToString("R",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32ExponentialFormatBehavior = new
    {
        defaultPrecision = ((IFormattable)42).ToString("E",
            System.Globalization.CultureInfo.InvariantCulture),
        twoDecimals = ((IFormattable)12345).ToString("E2",
            System.Globalization.CultureInfo.InvariantCulture),
        lowerCase = ((IFormattable)12345).ToString("e2",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-42)).ToString("E1",
            System.Globalization.CultureInfo.InvariantCulture),
        zero = ((IFormattable)0).ToString("E2",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32ExponentialRoundingBehavior = new
    {
        exponentCarry = ((IFormattable)999).ToString("E1",
            System.Globalization.CultureInfo.InvariantCulture),
        midpointCarry = ((IFormattable)995).ToString("E1",
            System.Globalization.CultureInfo.InvariantCulture),
        midpointEven = ((IFormattable)985).ToString("E1",
            System.Globalization.CultureInfo.InvariantCulture),
        belowMidpoint = ((IFormattable)949).ToString("E1",
            System.Globalization.CultureInfo.InvariantCulture),
        maximum = ((IFormattable)int.MaxValue).ToString("E2",
            System.Globalization.CultureInfo.InvariantCulture),
        minimum = ((IFormattable)int.MinValue).ToString("E2",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32CustomFormatBehavior = new
    {
        padded = ((IFormattable)42).ToString("000000",
            System.Globalization.CultureInfo.InvariantCulture),
        negativePadded = ((IFormattable)(-42)).ToString("000000",
            System.Globalization.CultureInfo.InvariantCulture),
        grouped = ((IFormattable)12345).ToString("#,##0",
            System.Globalization.CultureInfo.InvariantCulture),
        groupedFixed = ((IFormattable)12345).ToString("#,##0.00",
            System.Globalization.CultureInfo.InvariantCulture),
        fixedTwo = ((IFormattable)42).ToString("0.00",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32CustomSectionBehavior = new
    {
        positive = ((IFormattable)42).ToString("0;(0);zero",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-42)).ToString("0;(0);zero",
            System.Globalization.CultureInfo.InvariantCulture),
        zero = ((IFormattable)0).ToString("0;(0);zero",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32EscapedPercentBehavior = new
    {
        escaped = ((IFormattable)42).ToString(@"0\%",
            System.Globalization.CultureInfo.InvariantCulture),
        active = ((IFormattable)42).ToString("0%",
            System.Globalization.CultureInfo.InvariantCulture),
        negativeEscaped = ((IFormattable)(-42)).ToString(@"0\%",
            System.Globalization.CultureInfo.InvariantCulture),
        negativeActive = ((IFormattable)(-42)).ToString("0%",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32PerMilleBehavior = new
    {
        escaped = ((IFormattable)42).ToString(@"0\‰",
            System.Globalization.CultureInfo.InvariantCulture),
        active = ((IFormattable)42).ToString("0‰",
            System.Globalization.CultureInfo.InvariantCulture),
        negativeEscaped = ((IFormattable)(-42)).ToString(@"0\‰",
            System.Globalization.CultureInfo.InvariantCulture),
        negativeActive = ((IFormattable)(-42)).ToString("0‰",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32CommaScalingBehavior = new
    {
        single = ((IFormattable)12345).ToString("0,",
            System.Globalization.CultureInfo.InvariantCulture),
        doubleScale = ((IFormattable)1234567).ToString("0,,",
            System.Globalization.CultureInfo.InvariantCulture),
        grouped = ((IFormattable)1234567).ToString("#,##0,",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-12345)).ToString("0,",
            System.Globalization.CultureInfo.InvariantCulture),
        halfway = ((IFormattable)999500).ToString("0,",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32ScaledFractionBehavior = new
    {
        onePlace = ((IFormattable)12345).ToString("0,.0",
            System.Globalization.CultureInfo.InvariantCulture),
        twoPlaces = ((IFormattable)12345).ToString("0,.00",
            System.Globalization.CultureInfo.InvariantCulture),
        grouped = ((IFormattable)1234567).ToString("#,##0,.0",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-12345)).ToString("0,.0",
            System.Globalization.CultureInfo.InvariantCulture),
        halfway = ((IFormattable)1250).ToString("0,.0",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32OptionalFractionBehavior = new
    {
        integer = ((IFormattable)42).ToString("0.##",
            System.Globalization.CultureInfo.InvariantCulture),
        scaled = ((IFormattable)12345).ToString("0,.##",
            System.Globalization.CultureInfo.InvariantCulture),
        exact = ((IFormattable)12000).ToString("0,.##",
            System.Globalization.CultureInfo.InvariantCulture),
        grouped = ((IFormattable)1234567).ToString("#,##0,.##",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-12345)).ToString("0,.##",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32QuotedLiteralBehavior = new
    {
        prefix = ((IFormattable)42).ToString("'item '0",
            System.Globalization.CultureInfo.InvariantCulture),
        suffix = ((IFormattable)42).ToString("0' units'",
            System.Globalization.CultureInfo.InvariantCulture),
        both = ((IFormattable)42).ToString("'['0']'",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-42)).ToString("'item '0",
            System.Globalization.CultureInfo.InvariantCulture),
        zero = ((IFormattable)0).ToString("'item '0",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32QuotedSectionBehavior = new
    {
        positive = ((IFormattable)42).ToString("0;[0];'none'",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-42)).ToString("0;[0];'none'",
            System.Globalization.CultureInfo.InvariantCulture),
        zero = ((IFormattable)0).ToString("0;[0];'none'",
            System.Globalization.CultureInfo.InvariantCulture),
        unsignedNegative = ((IFormattable)(-42)).ToString("0;0;'zero'",
            System.Globalization.CultureInfo.InvariantCulture),
        labeledNegative = ((IFormattable)(-42)).ToString("0;'minus '0;'zero'",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32BracketLiteralBehavior = new
    {
        above = ((IFormattable)150).ToString("[>=100]0;[<0]'neg '0;'small '0",
            System.Globalization.CultureInfo.InvariantCulture),
        boundary = ((IFormattable)100).ToString("[>=100]0;[<0]'neg '0;'small '0",
            System.Globalization.CultureInfo.InvariantCulture),
        below = ((IFormattable)42).ToString("[>=100]0;[<0]'neg '0;'small '0",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-42)).ToString("[>=100]0;[<0]'neg '0;'small '0",
            System.Globalization.CultureInfo.InvariantCulture),
        zero = ((IFormattable)0).ToString("[>=100]0;[<0]'neg '0;'small '0",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32ScaledNearZeroBehavior = new
    {
        negativeWhole = ((IFormattable)(-1)).ToString("0,",
            System.Globalization.CultureInfo.InvariantCulture),
        negativeFixed = ((IFormattable)(-1)).ToString("0,.0",
            System.Globalization.CultureInfo.InvariantCulture),
        negativeOptional = ((IFormattable)(-1)).ToString("0,.##",
            System.Globalization.CultureInfo.InvariantCulture),
        negativeHalfway = ((IFormattable)(-50)).ToString("0,.0",
            System.Globalization.CultureInfo.InvariantCulture),
        positiveHalfway = ((IFormattable)50).ToString("0,.0",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32ScaledSectionBehavior = new
    {
        positive = ((IFormattable)12345).ToString("0,;(0,);'zero'",
            System.Globalization.CultureInfo.InvariantCulture),
        negative = ((IFormattable)(-12345)).ToString("0,;(0,);'zero'",
            System.Globalization.CultureInfo.InvariantCulture),
        zero = ((IFormattable)0).ToString("0,;(0,);'zero'",
            System.Globalization.CultureInfo.InvariantCulture),
        negativeSmall = ((IFormattable)(-1)).ToString("0,;(0,);'zero'",
            System.Globalization.CultureInfo.InvariantCulture),
        negativeFraction = ((IFormattable)(-1250)).ToString("0,.0;(0,.0);'zero'",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32FormatErrors = new
    {
        unknownSpecifier = ObserveInt32FormatError("Q"),
        negativeDecimalPrecision = ObserveInt32FormatError("D-1"),
        negativeHexPrecision = ObserveInt32FormatError("X-1"),
        hugePrecision = ObserveInt32FormatError("D999999999999"),
    },
    selectedInt32OddFormatResults = new
    {
        negativeDecimalPrecision = ((IFormattable)42).ToString("D-1",
            System.Globalization.CultureInfo.InvariantCulture),
        negativeHexPrecision = ((IFormattable)42).ToString("X-1",
            System.Globalization.CultureInfo.InvariantCulture),
    },
    selectedInt32ConversionErrors = new
    {
        byteOverflow = ObserveInt32Error(() => ((IConvertible)300)
            .ToByte(System.Globalization.CultureInfo.InvariantCulture)),
        unsignedOverflow = ObserveInt32Error(() => ((IConvertible)(-1))
            .ToUInt32(System.Globalization.CultureInfo.InvariantCulture)),
        charOverflow = ObserveInt32Error(() => ((IConvertible)70000)
            .ToChar(System.Globalization.CultureInfo.InvariantCulture)),
        invalidDateTime = ObserveInt32Error(() => ((IConvertible)42)
            .ToDateTime(System.Globalization.CultureInfo.InvariantCulture)),
    },
    selectedInt32ParseBehavior = new
    {
        number = ObserveInt32Parse("42"),
        padded = ObserveInt32Parse(" 42 "),
        invalid = ObserveInt32Parse("oops"),
        overflow = ObserveInt32Parse("2147483648"),
        nullValue = ObserveInt32Parse(null),
    },
    selectedInt32TryParseBehavior = new
    {
        number = ObserveInt32TryParse("42"),
        padded = ObserveInt32TryParse(" 42 "),
        negative = ObserveInt32TryParse("-7"),
        invalid = ObserveInt32TryParse("oops"),
        overflow = ObserveInt32TryParse("2147483648"),
        nullValue = ObserveInt32TryParse(null),
    },
    selectedNumberStylesValues = new
    {
        none = (int)System.Globalization.NumberStyles.None,
        integer = (int)System.Globalization.NumberStyles.Integer,
        allowHexSpecifier = (int)System.Globalization.NumberStyles.AllowHexSpecifier,
        hexNumber = (int)System.Globalization.NumberStyles.HexNumber,
    },
    selectedInt32HexParseBehavior = new
    {
        uppercase = ObserveInt32HexParse("FF"),
        padded = ObserveInt32HexParse(" FF "),
        allBits = ObserveInt32HexParse("FFFFFFFF"),
        overflow = ObserveInt32HexParse("100000000"),
        prefix = ObserveInt32HexParse("0xFF"),
        nullValue = ObserveInt32HexParse(null),
    },
    selectedInt32HexTryParseBehavior = new
    {
        uppercase = ObserveInt32HexTryParse("FF"),
        padded = ObserveInt32HexTryParse(" FF "),
        allBits = ObserveInt32HexTryParse("FFFFFFFF"),
        overflow = ObserveInt32HexTryParse("100000000"),
        prefix = ObserveInt32HexTryParse("0xFF"),
        nullValue = ObserveInt32HexTryParse(null),
    },
    selectedSpanFormattingBehavior = new
    {
        enough = ObserveSpanFormat(42, 2),
        shortBuffer = ObserveSpanFormat(42, 1),
    },
    selectedUtf8SpanFormattingBehavior = new
    {
        enough = ObserveUtf8SpanFormat(42, 2),
        shortBuffer = ObserveUtf8SpanFormat(42, 1),
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
        (typeof(IComparable), typeof(string)),
        (typeof(IFormattable), typeof(int)),
        (typeof(IConvertible), typeof(int)),
        (typeof(IComparable), typeof(int)),
        (typeof(ISpanFormattable), typeof(int)),
        (typeof(IUtf8SpanFormattable), typeof(int)),
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
        (typeof(IComparable), "text"),
        (typeof(IFormattable), 42),
        (typeof(IConvertible), 42),
        (typeof(IComparable), 42),
        (typeof(ISpanFormattable), 42),
        (typeof(IUtf8SpanFormattable), 42),
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
        intInterfaces = typeof(int).GetInterfaces().Select(type => type.FullName).ToArray(),
        spanFormattableInterfaces = typeof(ISpanFormattable).GetInterfaces()
            .Select(type => type.FullName).ToArray(),
        utf8SpanFormattableInterfaces = typeof(IUtf8SpanFormattable).GetInterfaces()
            .Select(type => type.FullName).ToArray(),
        objectMiss = ObserveInterface(typeof(object), "System.IDisposable", false),
        disposableSelf = ObserveInterface(typeof(IDisposable), "System.IDisposable", false),
        emptyName = ObserveInterface(typeof(IDisposable), "", false),
        nullName = ObserveInterface(typeof(IDisposable), null, false),
        stringComparable = ObserveInterface(typeof(string), "System.IComparable", false),
        stringComparableIgnoreCase = ObserveInterface(typeof(string), "System.IComparable", true),
        stringComparableShort = ObserveInterface(typeof(string), "IComparable", false),
        stringInsensitive = ObserveInterface(typeof(string), "system.icomparable", true),
        stringSensitiveMiss = ObserveInterface(typeof(string), "system.icomparable", false),
        stringDisposableMiss = ObserveInterface(typeof(string), "System.IDisposable", false),
        intFormattable = ObserveInterface(typeof(int), "System.IFormattable", false),
        intFormattableShort = ObserveInterface(typeof(int), "IFormattable", false),
        intFormattableLower = ObserveInterface(typeof(int), "system.iformattable", true),
        stringFormattableMiss = ObserveInterface(typeof(string), "System.IFormattable", false),
        intConvertible = ObserveInterface(typeof(int), "System.IConvertible", false),
        intConvertibleShort = ObserveInterface(typeof(int), "IConvertible", false),
        intConvertibleLower = ObserveInterface(typeof(int), "system.iconvertible", true),
        objectConvertibleMiss = ObserveInterface(typeof(object), "System.IConvertible", false),
        intComparable = ObserveInterface(typeof(int), "System.IComparable", false),
        intComparableShort = ObserveInterface(typeof(int), "IComparable", false),
        intComparableLower = ObserveInterface(typeof(int), "system.icomparable", true),
        intSpanFormattable = ObserveInterface(typeof(int), "System.ISpanFormattable", false),
        intSpanFormattableShort = ObserveInterface(typeof(int), "ISpanFormattable", false),
        intSpanFormattableLower = ObserveInterface(typeof(int), "system.ispanformattable", true),
        intUtf8SpanFormattable = ObserveInterface(typeof(int), "System.IUtf8SpanFormattable", false),
        intUtf8SpanFormattableShort = ObserveInterface(typeof(int), "IUtf8SpanFormattable", false),
        intUtf8SpanFormattableLower = ObserveInterface(typeof(int), "system.iutf8spanformattable", true),
    },
    types = selected.Select(type => new
    {
        fullName = type.FullName,
        assemblyQualifiedName = type.AssemblyQualifiedName,
        qualifiedNameRoundTripSameReference = ReferenceEquals(Type.GetType(type.AssemblyQualifiedName), type),
        baseType = type.BaseType?.FullName,
        isInterface = type.IsInterface,
        isAbstract = type.IsAbstract,
        nameGetterIsAbstract = type.GetProperty("Name")?.GetMethod?.IsAbstract,
        declaringGetterIsAbstract = type.GetProperty("DeclaringType")?.GetMethod?.IsAbstract,
        reflectedGetterIsAbstract = type.GetProperty("ReflectedType")?.GetMethod?.IsAbstract,
        declaredPublicMethodCount = type.GetMethods(declaredPublic).Count(method => !method.IsSpecialName),
        declaredPublicPropertyCount = type.GetProperties(declaredPublic).Length,
        selectedMethods = type.GetMethods(declaredPublic)
            .Where(method => !method.IsSpecialName && (type == typeof(IConvertible) ||
                method.Name is "Dispose" or "CompareTo" or "ToString" or "TryFormat" or "ToInt32" or "GetFormat" or "Equals" or "GetType" or "MakeGenericType"
                    or "GetGenericArguments" or "GetGenericTypeDefinition" or "GetGenericParameterConstraints"
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
                or "GenericParameterPosition" or "GenericTypeArguments" or "IsArray" or "IsSZArray" or "IsVariableBoundArray" or "HasElementType" or "IsByRef"
                or "IsPointer" or "Name" or "FullName" or "Namespace" or "MemberType"
                or "DeclaringType" or "ReflectedType" or "BaseType" or "IsClass" or "IsValueType" or "IsPrimitive" or "IsAbstract" or "IsSealed" or "IsPublic" or "IsVisible" or "IsGenericTypeDefinition" or "ContainsGenericParameters"
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
