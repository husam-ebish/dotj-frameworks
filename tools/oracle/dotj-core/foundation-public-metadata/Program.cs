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
    typeof(Exception),
    typeof(SystemException),
    typeof(ArgumentException),
    typeof(ArgumentNullException),
    typeof(TypeLoadException),
    typeof(IndexOutOfRangeException),
    typeof(System.IO.IOException),
    typeof(System.IO.FileNotFoundException),
    typeof(OverflowException),
    typeof(InvalidCastException),
    typeof(FormatException),
    typeof(System.Globalization.NumberStyles),
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
