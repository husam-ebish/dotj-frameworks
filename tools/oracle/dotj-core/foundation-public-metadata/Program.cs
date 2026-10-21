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
static object ObserveNestedType(Type type, string? name)
{
    try
    {
        return new { result = type.GetNestedType(name!)?.FullName,
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (string?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveNestedTypeFlags(Type type, string? name, BindingFlags flags)
{
    try
    {
        return new { result = type.GetNestedType(name!, flags)?.Name,
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (string?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveEnumNames(Type type)
{
    try
    {
        return new { names = type.GetEnumNames(), exception = (string?)null,
            paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { names = (string[]?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveEnumDefined(Type type, object? value)
{
    try
    {
        return new { result = (bool?)type.IsEnumDefined(value!), exception = (string?)null,
            paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (bool?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveEnumName(Type type, object? value)
{
    try
    {
        return new { result = type.GetEnumName(value!), exception = (string?)null,
            paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (string?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveEnumValues(Type type)
{
    try
    {
        Array values = type.GetEnumValues();
        return new { arrayType = values.GetType().FullName,
            names = values.Cast<object>().Select(value => value.ToString()).ToArray(),
            values = values.Cast<object>().Select(Convert.ToInt32).ToArray(),
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { arrayType = (string?)null, names = (string?[]?)null,
            values = (int[]?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveEnumUnderlyingValues(Type type)
{
    try
    {
        Array values = type.GetEnumValuesAsUnderlyingType();
        return new { arrayType = values.GetType().FullName,
            values = values.Cast<int>().ToArray(), exception = (string?)null,
            paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { arrayType = (string?)null, values = (int[]?)null,
            exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveEnumUnderlyingType(Type type)
{
    try
    {
        return new { result = type.GetEnumUnderlyingType().FullName,
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (string?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static string? ObserveFunctionPointerQuery(Func<object> operation)
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
static object ObserveMemberName(Type type, string? name)
{
    try
    {
        return new { members = type.GetMember(name!).Select(member => new
            { name = member.Name, kind = member.MemberType.ToString() }).ToArray(),
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { members = (object[]?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveMemberFlags(Type type, string? name, BindingFlags flags)
{
    try
    {
        return new { members = type.GetMember(name!, flags).Select(member => new
            { name = member.Name, kind = member.MemberType.ToString() }).ToArray(),
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { members = (object[]?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveMemberKinds(Type type, string? name, MemberTypes kinds, BindingFlags flags)
{
    try
    {
        return new { members = type.GetMember(name!, kinds, flags).Select(member => new
            { name = member.Name, kind = member.MemberType.ToString() }).ToArray(),
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { members = (object[]?)null, exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveMembersFlags(Type type, BindingFlags flags)
{
    return type.GetMembers(flags).Select(member => new
        { name = member.Name, kind = member.MemberType.ToString() }).ToArray();
}
static object ObserveMethodName(Type type, string? name)
{
    try
    {
        MethodInfo? method = type.GetMethod(name!);
        return new { result = method?.Name, kind = method?.MemberType.ToString(),
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (string?)null, kind = (string?)null,
            exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveMethodFlags(Type type, string? name, BindingFlags flags)
{
    try
    {
        MethodInfo? method = type.GetMethod(name!, flags);
        return new { result = method?.Name, kind = method?.MemberType.ToString(),
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (string?)null, kind = (string?)null,
            exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveMethodParameters(Type type, string? name, Type[]? parameters)
{
    try
    {
        MethodInfo? method = type.GetMethod(name!, parameters!);
        return new { result = method?.Name, kind = method?.MemberType.ToString(),
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (string?)null, kind = (string?)null,
            exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static object ObserveMethodFlagsParameters(Type type, string? name, BindingFlags flags, Type[]? parameters)
{
    try
    {
        MethodInfo? method = type.GetMethod(name!, flags, parameters!);
        return new { result = method?.Name, kind = method?.MemberType.ToString(),
            exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new { result = (string?)null, kind = (string?)null,
            exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName };
    }
}
static string? ObserveMethodError(Action operation)
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
static string? ObserveMethodArgumentName(Action operation)
{
    try
    {
        operation();
        return null;
    }
    catch (ArgumentException exception)
    {
        return exception.ParamName;
    }
    catch (Exception)
    {
        return null;
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
static object ObserveInt32ProviderFormat()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NumberGroupSeparator = "_",
        NumberDecimalSeparator = ":",
        NumberDecimalDigits = 3,
    };
    return new
    {
        grouped = ((IFormattable)12345).ToString("N2", provider),
        negative = ((IFormattable)(-42)).ToString("N2", provider),
        defaultPrecision = ((IFormattable)42).ToString("N", provider),
    };
}
static object ObserveInt32NumberGroupSizes()
{
    var repeated = new System.Globalization.NumberFormatInfo
    {
        NumberGroupSeparator = "_",
        NumberGroupSizes = [3, 2],
    };
    var stopped = new System.Globalization.NumberFormatInfo
    {
        NumberGroupSeparator = "_",
        NumberGroupSizes = [3, 2, 0],
    };
    return new
    {
        repeated = ((IFormattable)123456789).ToString("N0", repeated),
        negative = ((IFormattable)(-123456789)).ToString("N2", repeated),
        stopped = ((IFormattable)123456789).ToString("N0", stopped),
        parsed = int.Parse("12_34_56_789", System.Globalization.NumberStyles.Number, repeated),
    };
}
static object ObserveInt32CurrencyPercentGroupSizes()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        CurrencySymbol = "USD",
        CurrencyGroupSeparator = "_",
        CurrencyGroupSizes = [3, 2],
        PercentSymbol = "pct",
        PercentGroupSeparator = "_",
        PercentGroupSizes = [2],
    };
    return new
    {
        currency = ((IFormattable)123456789).ToString("C0", provider),
        negativeCurrency = ((IFormattable)(-123456789)).ToString("C0", provider),
        percent = ((IFormattable)42).ToString("P0", provider),
        negativePercent = ((IFormattable)(-42)).ToString("P0", provider),
    };
}
static object ObserveInt32GroupSizeBoundaries()
{
    var provider = new System.Globalization.NumberFormatInfo();
    return new
    {
        nullNumber = ObserveInt32Error(() => provider.NumberGroupSizes = null!),
        emptyNumber = ObserveInt32Error(() => provider.NumberGroupSizes = []),
        zeroNumber = ObserveInt32Error(() => provider.NumberGroupSizes = [0]),
        negativeNumber = ObserveInt32Error(() => provider.NumberGroupSizes = [-1]),
        tenNumber = ObserveInt32Error(() => provider.NumberGroupSizes = [10]),
        interiorZeroNumber = ObserveInt32Error(() => provider.NumberGroupSizes = [3, 0, 2]),
        terminalZeroNumber = ObserveInt32Error(() => provider.NumberGroupSizes = [3, 0]),
        negativeCurrency = ObserveInt32Error(() => provider.CurrencyGroupSizes = [-1]),
        interiorZeroCurrency = ObserveInt32Error(() => provider.CurrencyGroupSizes = [3, 0, 2]),
        negativePercent = ObserveInt32Error(() => provider.PercentGroupSizes = [-1]),
        interiorZeroPercent = ObserveInt32Error(() => provider.PercentGroupSizes = [3, 0, 2]),
    };
}
static object ObserveInt32NegativeSign()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NegativeSign = "~",
    };
    bool customSuccess = int.TryParse("~42", System.Globalization.NumberStyles.Integer,
        provider, out int customValue);
    bool standardSuccess = int.TryParse("-42", System.Globalization.NumberStyles.Integer,
        provider, out int standardValue);
    return new
    {
        customParse = int.Parse("~42", System.Globalization.NumberStyles.Integer, provider),
        customSuccess,
        customValue,
        standardSuccess,
        standardValue,
        negativeFormat = ((IFormattable)(-42)).ToString("N2", provider),
        decimalFormat = ((IFormattable)(-42)).ToString("D", provider),
        paddedDecimalFormat = ((IFormattable)(-42)).ToString("D5", provider),
        providerText = (-42).ToString(provider),
        generalFormat = ((IFormattable)(-42)).ToString("G", provider),
        lowerGeneral = ((IFormattable)(-42)).ToString("g2", provider),
        generalPrecision = ((IFormattable)(-42)).ToString("G5", provider),
        roundTrip = ((IFormattable)(-42)).ToString("R", provider),
    };
}
static object ObserveInt32CurrencyProvider()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        CurrencySymbol = "USD",
        CurrencyGroupSeparator = "_",
        CurrencyDecimalSeparator = ":",
        CurrencyDecimalDigits = 3,
        CurrencyNegativePattern = 1,
        NegativeSign = "~",
    };
    string negativeWithSign = ((IFormattable)(-12345)).ToString("C2", provider);
    provider.CurrencyNegativePattern = 0;
    return new
    {
        defaultPrecision = ((IFormattable)12345).ToString("C", provider),
        zeroPrecision = ((IFormattable)12345).ToString("C0", provider),
        negativeWithSign,
        negativeParentheses = ((IFormattable)(-12345)).ToString("C2", provider),
    };
}
static object ObserveInt32PercentProvider()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        PercentSymbol = "pct",
        PercentGroupSeparator = "_",
        PercentDecimalSeparator = ":",
        PercentDecimalDigits = 3,
        NegativeSign = "~",
    };
    string defaultPositive = ((IFormattable)42).ToString("P", provider);
    string defaultNegative = ((IFormattable)(-42)).ToString("P2", provider);
    provider.PercentPositivePattern = 1;
    provider.PercentNegativePattern = 1;
    return new
    {
        defaultPositive,
        defaultNegative,
        compactPositive = ((IFormattable)42).ToString("P2", provider),
        compactNegative = ((IFormattable)(-42)).ToString("P2", provider),
    };
}
static object ObserveInt32FixedProvider()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NumberDecimalSeparator = ":",
        NumberDecimalDigits = 3,
        NegativeSign = "~",
    };
    return new
    {
        defaultPrecision = ((IFormattable)(-42)).ToString("F", provider),
        explicitPrecision = ((IFormattable)(-42)).ToString("f1", provider),
        zeroPrecision = ((IFormattable)(-42)).ToString("F0", provider),
    };
}
static object ObserveInt32ExponentialProvider()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NumberDecimalSeparator = ":",
        NegativeSign = "~",
    };
    return new
    {
        upper = ((IFormattable)(-42)).ToString("E2", provider),
        lower = ((IFormattable)42).ToString("e1", provider),
        zeroPrecision = ((IFormattable)(-42)).ToString("E0", provider),
    };
}
static object ObserveInt32PositiveSign()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        PositiveSign = "plus",
        NegativeSign = "~",
    };
    bool customSuccess = int.TryParse("plus42", System.Globalization.NumberStyles.Integer,
        provider, out int customValue);
    bool standardSuccess = int.TryParse("+42", System.Globalization.NumberStyles.Integer,
        provider, out int standardValue);
    return new
    {
        customParse = int.Parse("plus42", System.Globalization.NumberStyles.Integer, provider),
        customSuccess,
        customValue,
        standardSuccess,
        standardValue,
        positiveExponent = ((IFormattable)42).ToString("E1", provider),
        negativeExponent = ((IFormattable)(-42)).ToString("E1", provider),
    };
}
static object ObserveInt32NumberStyleProvider()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NumberGroupSeparator = "_",
        NumberDecimalSeparator = ":",
        PositiveSign = "plus",
        NegativeSign = "~",
    };
    bool fractionalSuccess = int.TryParse("42:5", System.Globalization.NumberStyles.Number,
        provider, out int fractionalValue);
    bool standardSignSuccess = int.TryParse("+42", System.Globalization.NumberStyles.Number,
        provider, out int standardSignValue);
    return new
    {
        grouped = int.Parse("12_345", System.Globalization.NumberStyles.Number, provider),
        decimalZero = int.Parse("12_345:00", System.Globalization.NumberStyles.Number, provider),
        negative = int.Parse("~12_345:00", System.Globalization.NumberStyles.Number, provider),
        positive = int.Parse("plus12_345:00", System.Globalization.NumberStyles.Number, provider),
        trailingNegative = int.Parse("12_345:00~", System.Globalization.NumberStyles.Number, provider),
        fractionalSuccess,
        fractionalValue,
        standardSignSuccess,
        standardSignValue,
    };
}
static object ObserveInt32NumberStyleBoundaries()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NumberGroupSeparator = "_",
        NumberDecimalSeparator = ":",
        PositiveSign = "plus",
        NegativeSign = "~",
    };
    string[] texts = ["_123", "123_", "12__345", "42:", "42:0_0", "42:5",
        "42::0", "12_:00", "42plus", "42~", "~42plus", ":00"];
    return texts.Select(text =>
    {
        bool success = int.TryParse(text, System.Globalization.NumberStyles.Number,
            provider, out int value);
        return new { text, success, value };
    }).ToArray();
}
static object ObserveInt32FloatStyle()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NumberDecimalSeparator = ":",
        NumberGroupSeparator = "_",
        PositiveSign = "plus",
        NegativeSign = "~",
    };
    string[] texts = ["42", " 42:00 ", "4:2e1", "420e~1", "plus4:2Eplus1",
        "~4:2eplus1", "12_345", "42:5", "4:2e0", "2147483648",
        "42plus", "42~", "42:", ":0", "4:2e~1"];
    return texts.Select(text =>
    {
        bool success = int.TryParse(text, System.Globalization.NumberStyles.Float,
            provider, out int value);
        string? error = ObserveInt32Error(() => int.Parse(text,
            System.Globalization.NumberStyles.Float, provider));
        return new { text, success, value, error };
    }).ToArray();
}
static object ObserveInt32SingleStyles()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NumberDecimalSeparator = ":",
        NumberGroupSeparator = "_",
        PositiveSign = "plus",
        NegativeSign = "~",
    };
    return new
    {
        thousands = ObserveInt32SingleStyle(System.Globalization.NumberStyles.AllowThousands,
            ["12_345", "_123", "123_", " 123", "~123", "123:00", "12__345"], provider),
        decimalPoint = ObserveInt32SingleStyle(System.Globalization.NumberStyles.AllowDecimalPoint,
            ["42:00", "42:5", ":0", "42:", "12_345", " 42", "~42"], provider),
        exponent = ObserveInt32SingleStyle(System.Globalization.NumberStyles.AllowExponent,
            ["42e1", "420e~1", "4:2e1", "42", " 42", "~42", "42eplus1",
                "42e1plus", "42e~1"], provider),
    };
}
static object ObserveInt32CurrencyStyle()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        CurrencySymbol = "USD",
        CurrencyGroupSeparator = "_",
        CurrencyDecimalSeparator = ":",
        NumberGroupSeparator = ".",
        NumberDecimalSeparator = "=",
        PositiveSign = "plus",
        NegativeSign = "~",
    };
    string[] texts = ["USD12_345:00", "(USD12_345:00)", "~USD12_345:00",
        "plusUSD12_345:00", "12_345:00USD", "USD 12_345:00", "12_345:00 USD",
        "12_345:00", "12.345=00", "USD12.345=00", "USD42:5", "USD_42",
        "USD42e1", "  USD42  ", "USD42~", "USD42plus"];
    return ObserveInt32SingleStyle(System.Globalization.NumberStyles.Currency, texts, provider);
}
static object ObserveInt32AnyStyle()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        CurrencySymbol = "USD",
        CurrencyGroupSeparator = "_",
        CurrencyDecimalSeparator = ":",
        NumberGroupSeparator = ".",
        NumberDecimalSeparator = "=",
        PositiveSign = "plus",
        NegativeSign = "~",
    };
    string[] texts = ["USD12_345:00", "12.345=00", "~USD12_345:00",
        "42e1", "4:2e1", "4=2e1", "(USD42)", "USD42e1", "USD42:5",
        "42:5", "42=5", "12_345", "12.345", "42plus", "USD42~",
        "USD42eplus1", "(42)"];
    return ObserveInt32SingleStyle(System.Globalization.NumberStyles.Any, texts, provider);
}
static object ObserveInt32CombinedStyles()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NumberDecimalSeparator = ":",
        NumberGroupSeparator = "_",
        PositiveSign = "plus",
        NegativeSign = "~",
    };
    var signThousands = System.Globalization.NumberStyles.AllowLeadingSign
        | System.Globalization.NumberStyles.AllowThousands;
    var paddedThousands = System.Globalization.NumberStyles.AllowLeadingWhite
        | System.Globalization.NumberStyles.AllowTrailingWhite
        | System.Globalization.NumberStyles.AllowThousands;
    var decimalExponent = System.Globalization.NumberStyles.AllowDecimalPoint
        | System.Globalization.NumberStyles.AllowExponent;
    return new
    {
        signThousandsValue = (int)signThousands,
        signThousands = ObserveInt32SingleStyle(signThousands,
            ["~12_345", "12_345", " 12_345", "12_345~", "12_345:00", "plus12_345"], provider),
        paddedThousandsValue = (int)paddedThousands,
        paddedThousands = ObserveInt32SingleStyle(paddedThousands,
            [" 12_345 ", "~12_345", "12_345", "12_345:00"], provider),
        decimalExponentValue = (int)decimalExponent,
        decimalExponent = ObserveInt32SingleStyle(decimalExponent,
            ["4:2e1", "420e~1", "~4:2e1", " 42", "4:2e0", "42", "12_345"], provider),
    };
}
static object ObserveInt32MoreCombinedStyles()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NumberDecimalSeparator = ":",
        PositiveSign = "plus",
        NegativeSign = "~",
    };
    var signExponent = System.Globalization.NumberStyles.AllowLeadingSign
        | System.Globalization.NumberStyles.AllowExponent;
    var paddedDecimal = System.Globalization.NumberStyles.AllowLeadingWhite
        | System.Globalization.NumberStyles.AllowTrailingWhite
        | System.Globalization.NumberStyles.AllowDecimalPoint;
    var signDecimalExponent = System.Globalization.NumberStyles.AllowLeadingSign
        | System.Globalization.NumberStyles.AllowDecimalPoint
        | System.Globalization.NumberStyles.AllowExponent;
    return new
    {
        signExponentValue = (int)signExponent,
        signExponent = ObserveInt32SingleStyle(signExponent,
            ["~42e1", "42e~1", "42:0", " 42", "plus42e1"], provider),
        paddedDecimalValue = (int)paddedDecimal,
        paddedDecimal = ObserveInt32SingleStyle(paddedDecimal,
            [" 42:00 ", "42:5", "~42", "4:2e1", "42"], provider),
        signDecimalExponentValue = (int)signDecimalExponent,
        signDecimalExponent = ObserveInt32SingleStyle(signDecimalExponent,
            ["~4:2e1", "plus4:2e1", " 4:2e1", "4:2e~1", "42"], provider),
    };
}
static object ObserveInt32TrailingSignStyles()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NumberGroupSeparator = "_",
        PositiveSign = "plus",
        NegativeSign = "~",
    };
    var groupedTrailing = System.Globalization.NumberStyles.AllowThousands
        | System.Globalization.NumberStyles.AllowTrailingSign;
    var paddedTrailing = System.Globalization.NumberStyles.AllowLeadingWhite
        | System.Globalization.NumberStyles.AllowTrailingWhite
        | groupedTrailing;
    var bothSigns = System.Globalization.NumberStyles.AllowLeadingSign | groupedTrailing;
    return new
    {
        trailingValue = (int)System.Globalization.NumberStyles.AllowTrailingSign,
        trailing = ObserveInt32SingleStyle(System.Globalization.NumberStyles.AllowTrailingSign,
            ["42~", "42plus", "~42"], provider),
        groupedTrailingValue = (int)groupedTrailing,
        groupedTrailing = ObserveInt32SingleStyle(groupedTrailing,
            ["12_345~", "12_345plus", "~12_345", " 12_345~", "12_345:00~", "12__345~"], provider),
        paddedTrailingValue = (int)paddedTrailing,
        paddedTrailing = ObserveInt32SingleStyle(paddedTrailing,
            [" 12_345~ ", "12_345plus", "~12_345", "12_345:00~"], provider),
        bothSignsValue = (int)bothSigns,
        bothSigns = ObserveInt32SingleStyle(bothSigns,
            ["~12_345", "12_345~", "~12_345~", "plus12_345~", "12_345plus"], provider),
    };
}
static object ObserveInt32GroupedDecimalStyles()
{
    var provider = new System.Globalization.NumberFormatInfo
    {
        NumberGroupSeparator = "_",
        NumberDecimalSeparator = ":",
        PositiveSign = "plus",
        NegativeSign = "~",
    };
    var groupedDecimal = System.Globalization.NumberStyles.AllowThousands
        | System.Globalization.NumberStyles.AllowDecimalPoint;
    var parenthesizedDecimal = System.Globalization.NumberStyles.AllowParentheses
        | groupedDecimal;
    var groupedExponent = groupedDecimal | System.Globalization.NumberStyles.AllowExponent;
    return new
    {
        parenthesesValue = (int)System.Globalization.NumberStyles.AllowParentheses,
        parentheses = ObserveInt32SingleStyle(System.Globalization.NumberStyles.AllowParentheses,
            ["(42)", "42", "~42", " (42)", "(42)~"], provider),
        groupedDecimalValue = (int)groupedDecimal,
        groupedDecimal = ObserveInt32SingleStyle(groupedDecimal,
            ["12_345:00", "12_345:5", " 12_345:00", "~12_345:00", "12_345:0_0"], provider),
        parenthesizedDecimalValue = (int)parenthesizedDecimal,
        parenthesizedDecimal = ObserveInt32SingleStyle(parenthesizedDecimal,
            ["(12_345:00)", "(12_345:5)", "~12_345:00", "(12_345:00)~", "12_345:00"], provider),
        groupedExponentValue = (int)groupedExponent,
        groupedExponent = ObserveInt32SingleStyle(groupedExponent,
            ["12_345:00e1", "1_234:5e1", "12_345:5e0", "12_345:00e~1",
                "12_345:00eplus1", "12_345:00"], provider),
    };
}
static object ObserveInt32SingleStyle(System.Globalization.NumberStyles style,
    string[] texts, System.Globalization.NumberFormatInfo provider)
{
    return texts.Select(text =>
    {
        bool success = int.TryParse(text, style, provider, out int value);
        string? error = ObserveInt32Error(() => int.Parse(text, style, provider));
        return new { text, success, value, error };
    }).ToArray();
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
static object ObserveSelectedAttributeInstance()
{
    ParameterInfo parameter = typeof(IFormattable).GetMethod("ToString")!.ReturnParameter;
    Attribute first = (Attribute)parameter.GetCustomAttributes(false)[0];
    Attribute second = (Attribute)parameter.GetCustomAttributes(false)[0];
    return new
    {
        sameReference = ReferenceEquals(first, second),
        equalsRepeat = first.Equals(second),
        matchesRepeat = first.Match(second),
        typeId = ((Type)first.TypeId).FullName,
        typeIdEqualsType = ReferenceEquals(first.TypeId, first.GetType()),
        isDefault = first.IsDefaultAttribute(),
    };
}
static object ObserveNullableAttributeConstructor()
{
    Type type = typeof(IFormattable).GetMethod("ToString")!.ReturnParameter
        .GetCustomAttributes(false)[0].GetType();
    ConstructorInfo[] constructors = type.GetConstructors(
        BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
    ConstructorInfo arrayConstructor = type.GetConstructor(
        BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance,
        null, new[] { typeof(byte[]) }, null)!;
    byte[] input = { 1, 2 };
    object instance = arrayConstructor.Invoke(new object[] { input });
    byte[] flags = (byte[])type.GetField("NullableFlags")!.GetValue(instance)!;
    bool sameReference = ReferenceEquals(input, flags);
    input[0] = 3;
    return new
    {
        constructors = constructors.Select(ctor => new
        {
            parameters = ctor.GetParameters().Select(parameter => parameter.ParameterType.FullName).ToArray(),
            isPublic = ctor.IsPublic,
        }).OrderBy(ctor => ctor.parameters[0]).ToArray(),
        sameArrayReference = sameReference,
        firstFlagAfterInputMutation = flags[0],
        secondFlag = flags[1],
    };
}
static object ObserveStreamingContextEquality()
{
    object marker = new();
    var first = new System.Runtime.Serialization.StreamingContext(
        System.Runtime.Serialization.StreamingContextStates.Other, marker);
    var same = new System.Runtime.Serialization.StreamingContext(
        System.Runtime.Serialization.StreamingContextStates.Other, marker);
    var differentObject = new System.Runtime.Serialization.StreamingContext(
        System.Runtime.Serialization.StreamingContextStates.Other, new object());
    var differentState = new System.Runtime.Serialization.StreamingContext(
        System.Runtime.Serialization.StreamingContextStates.CrossProcess, marker);
    return new
    {
        defaultEquals = default(System.Runtime.Serialization.StreamingContext)
            .Equals(default(System.Runtime.Serialization.StreamingContext)),
        sameStateSameContext = first.Equals(same),
        sameStateDifferentContext = first.Equals(differentObject),
        differentStateSameContext = first.Equals(differentState),
        sameHash = first.GetHashCode() == same.GetHashCode(),
        text = first.ToString(),
        defaultText = default(System.Runtime.Serialization.StreamingContext).ToString(),
    };
}
static object ObserveSerializationInfoConstruction()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), converter);
    return new
    {
        constructors = typeof(System.Runtime.Serialization.SerializationInfo)
            .GetConstructors(BindingFlags.Public | BindingFlags.Instance)
            .Select(ctor => ctor.GetParameters()
                .Select(parameter => parameter.ParameterType.FullName).ToArray()).ToArray(),
        converterMethods = typeof(System.Runtime.Serialization.IFormatterConverter)
            .GetMethods().Select(method => new { name = method.Name,
                result = method.ReturnType.FullName,
                parameters = method.GetParameters().Select(parameter =>
                    parameter.ParameterType.FullName).ToArray() })
            .OrderBy(method => method.name).ToArray(),
        objectType = info.ObjectType.FullName,
        fullTypeName = info.FullTypeName,
        memberCount = info.MemberCount,
        threeArgType = new System.Runtime.Serialization.SerializationInfo(
            typeof(DBNull), converter, true).ObjectType.FullName,
        nullTypeError = ObserveMethodError(() =>
            new System.Runtime.Serialization.SerializationInfo(null!, converter)),
        nullTypeParameter = ObserveMethodArgumentName(() =>
            new System.Runtime.Serialization.SerializationInfo(null!, converter)),
        nullConverterError = ObserveMethodError(() =>
            new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), null!)),
        nullConverterParameter = ObserveMethodArgumentName(() =>
            new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), null!)),
    };
}
static object ObserveFormatterConverter()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    return new
    {
        constructorCount = typeof(System.Runtime.Serialization.FormatterConverter)
            .GetConstructors(BindingFlags.Public | BindingFlags.Instance).Length,
        interfaceName = typeof(System.Runtime.Serialization.FormatterConverter)
            .GetInterfaces().Single(type => type == typeof(System.Runtime.Serialization.IFormatterConverter)).FullName,
        integer = converter.ToInt32(42),
        stringInteger = converter.ToInt32("17"),
        integerText = converter.ToString(42),
        integerBoolean = converter.ToBoolean(1),
        byType = converter.Convert("17", typeof(int)),
        byTypeCode = converter.Convert("17", TypeCode.Int32),
        nullIntegerError = ObserveMethodError(() => converter.ToInt32(null!)),
        nullIntegerParameter = ObserveMethodArgumentName(() => converter.ToInt32(null!)),
        badIntegerError = ObserveMethodError(() => converter.ToInt32("oops")),
    };
}
static object ObserveSerializationInfoMembers()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), converter);
    info.AddValue("age", 42);
    info.AddValue("name", "Ada");
    return new
    {
        count = info.MemberCount,
        age = info.GetInt32("age"),
        name = info.GetString("name"),
        ageByType = info.GetValue("age", typeof(int)),
        nullAddError = ObserveMethodError(() => info.AddValue(null!, 1)),
        nullAddParameter = ObserveMethodArgumentName(() => info.AddValue(null!, 1)),
        nullGetError = ObserveMethodError(() => info.GetInt32(null!)),
        nullGetParameter = ObserveMethodArgumentName(() => info.GetInt32(null!)),
        duplicateError = ObserveMethodError(() => info.AddValue("age", 1)),
        missingError = ObserveMethodError(() => info.GetInt32("missing")),
        exceptionBase = typeof(System.Runtime.Serialization.SerializationException).BaseType?.FullName,
    };
}
static object ObserveSerializationInfoEnumeration()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("age", 42);
    info.AddValue("name", "Ada");
    var enumerator = info.GetEnumerator();
    var entries = new List<object>();
    while (enumerator.MoveNext())
    {
        entries.Add(new { name = enumerator.Name,
            type = enumerator.ObjectType.FullName,
            value = enumerator.Value?.ToString(),
            currentName = enumerator.Current.Name });
    }
    enumerator.Reset();
    return new
    {
        enumeratorType = info.GetEnumerator().GetType().FullName,
        entryType = typeof(System.Runtime.Serialization.SerializationEntry).FullName,
        entries,
        afterReset = enumerator.MoveNext() ? enumerator.Name : null,
    };
}
static object ObserveSerializationInfoTypedValues()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("text", "17", typeof(string));
    info.AddValue("typed", 42, typeof(object));
    var cursor = info.GetEnumerator();
    cursor.MoveNext();
    var firstType = cursor.ObjectType.FullName;
    cursor.MoveNext();
    var secondType = cursor.ObjectType.FullName;
    return new
    {
        count = info.MemberCount,
        parsed = info.GetInt32("text"),
        parsedByType = info.GetValue("text", typeof(int)),
        typedValue = info.GetValue("typed", typeof(object)),
        firstType,
        secondType,
        nullAddTypeError = ObserveMethodError(() => info.AddValue("bad", 1, null!)),
        nullAddTypeParameter = ObserveMethodArgumentName(() => info.AddValue("bad", 1, null!)),
        nullGetTypeError = ObserveMethodError(() => info.GetValue("text", null!)),
        nullGetTypeParameter = ObserveMethodArgumentName(() => info.GetValue("text", null!)),
    };
}
static object ObserveSerializationInfoConversionBoundaries()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("number", 42);
    info.AddValue("bad", "oops");
    info.AddValue("empty", null, typeof(string));
    return new
    {
        numberAsString = info.GetValue("number", typeof(string)),
        nullString = info.GetString("empty"),
        nullValue = info.GetValue("empty", typeof(string)),
        badIntError = ObserveMethodError(() => info.GetInt32("bad")),
        incompatibleError = ObserveMethodError(() => info.GetValue("number", typeof(DateTime))),
        nullIntError = ObserveMethodError(() => info.GetInt32("empty")),
    };
}
static object ObserveSerializationInfoTypeMetadata()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    var initialType = info.ObjectType.FullName;
    var initialFullName = info.FullTypeName;
    var initialAssemblyName = info.AssemblyName;
    var initialFullNameExplicit = info.IsFullTypeNameSetExplicit;
    var initialAssemblyNameExplicit = info.IsAssemblyNameSetExplicit;
    info.SetType(typeof(string));
    var afterSetType = new { objectType = info.ObjectType.FullName,
        fullTypeName = info.FullTypeName,
        assemblyName = info.AssemblyName,
        fullNameExplicit = info.IsFullTypeNameSetExplicit,
        assemblyNameExplicit = info.IsAssemblyNameSetExplicit };
    info.FullTypeName = "custom.Record";
    info.AssemblyName = "custom.assembly";
    return new
    {
        initialType, initialFullName, initialAssemblyName,
        initialFullNameExplicit, initialAssemblyNameExplicit,
        afterSetType,
        customFullName = info.FullTypeName,
        customAssemblyName = info.AssemblyName,
        customFullNameExplicit = info.IsFullTypeNameSetExplicit,
        customAssemblyNameExplicit = info.IsAssemblyNameSetExplicit,
        nullSetTypeError = ObserveMethodError(() => info.SetType(null!)),
        nullSetTypeParameter = ObserveMethodArgumentName(() => info.SetType(null!)),
    };
}
static object ObserveSerializationInfoNameValidation()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    var nullFullError = ObserveMethodError(() => info.FullTypeName = null!);
    var nullFullParameter = ObserveMethodArgumentName(() => info.FullTypeName = null!);
    var emptyFullError = ObserveMethodError(() => info.FullTypeName = "");
    var nullAssemblyError = ObserveMethodError(() => info.AssemblyName = null!);
    var nullAssemblyParameter = ObserveMethodArgumentName(() => info.AssemblyName = null!);
    var emptyAssemblyError = ObserveMethodError(() => info.AssemblyName = "");
    return new
    {
        nullFullError, nullFullParameter, emptyFullError,
        nullAssemblyError, nullAssemblyParameter, emptyAssemblyError,
        fullNameAfterErrors = info.FullTypeName,
        assemblyNameAfterErrors = info.AssemblyName,
        fullExplicitAfterErrors = info.IsFullTypeNameSetExplicit,
        assemblyExplicitAfterErrors = info.IsAssemblyNameSetExplicit,
    };
}
static object ObserveSerializationInfoSetTypeReset()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.FullTypeName = "custom.Record";
    info.AssemblyName = "custom.assembly";
    info.SetType(typeof(DBNull));
    var sameType = new { fullName = info.FullTypeName,
        assemblyName = info.AssemblyName,
        fullExplicit = info.IsFullTypeNameSetExplicit,
        assemblyExplicit = info.IsAssemblyNameSetExplicit };
    info.SetType(typeof(string));
    return new
    {
        sameType,
        differentType = new { objectType = info.ObjectType.FullName,
            fullName = info.FullTypeName,
            assemblyName = info.AssemblyName,
            fullExplicit = info.IsFullTypeNameSetExplicit,
            assemblyExplicit = info.IsAssemblyNameSetExplicit },
    };
}
static object ObserveSerializationInfoEnumeratorBoundaries()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("only", 1);
    var cursor = info.GetEnumerator();
    var beforeCurrent = ObserveMethodError(() => { _ = cursor.Current; });
    var beforeName = ObserveMethodError(() => { _ = cursor.Name; });
    var beforeType = ObserveMethodError(() => { _ = cursor.ObjectType; });
    var beforeValue = ObserveMethodError(() => { _ = cursor.Value; });
    var firstMove = cursor.MoveNext();
    var secondMove = cursor.MoveNext();
    var thirdMove = cursor.MoveNext();
    return new
    {
        beforeCurrent, beforeName, beforeType, beforeValue,
        firstMove, secondMove, thirdMove,
        afterCurrent = ObserveMethodError(() => { _ = cursor.Current; }),
        afterName = ObserveMethodError(() => { _ = cursor.Name; }),
        afterType = ObserveMethodError(() => { _ = cursor.ObjectType; }),
        afterValue = ObserveMethodError(() => { _ = cursor.Value; }),
    };
}
static object ObserveSerializationInfoEnumeratorMutation()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("first", 1);
    var cursor = info.GetEnumerator();
    info.AddValue("second", 2);
    var observed = new List<string>();
    while (cursor.MoveNext())
    {
        observed.Add(cursor.Name);
    }
    cursor.Reset();
    var afterReset = new List<string>();
    while (cursor.MoveNext())
    {
        afterReset.Add(cursor.Name);
    }
    var fresh = info.GetEnumerator();
    var freshNames = new List<string>();
    while (fresh.MoveNext())
    {
        freshNames.Add(fresh.Name);
    }
    return new { memberCount = info.MemberCount, observed, afterReset, freshNames };
}
static object ObserveEmptySerializationInfoEnumeration()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    var empty = info.GetEnumerator();
    var firstMove = empty.MoveNext();
    empty.Reset();
    var afterReset = empty.MoveNext();
    info.AddValue("added", 1);
    var afterAdd = empty.MoveNext();
    var fresh = info.GetEnumerator();
    return new
    {
        firstMove, afterReset, afterAdd,
        emptyCurrentError = ObserveMethodError(() => { _ = empty.Current; }),
        memberCount = info.MemberCount,
        freshMove = fresh.MoveNext(),
        freshName = fresh.Name,
    };
}
static object ObserveSerializationInfoPrimitiveMembers()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("flag", true);
    info.AddValue("large", 5000000000L);
    info.AddValue("ratio", 1.5d);
    var cursor = info.GetEnumerator();
    var types = new List<string>();
    while (cursor.MoveNext())
    {
        types.Add(cursor.ObjectType.FullName!);
    }
    return new
    {
        count = info.MemberCount,
        flag = info.GetBoolean("flag"),
        large = info.GetInt64("large"),
        ratio = info.GetDouble("ratio"),
        types,
    };
}
static object ObserveSerializationInfoPrimitiveConversions()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("one", 1);
    info.AddValue("integerText", "17");
    info.AddValue("decimalText", "1.5");
    info.AddValue("long", 5L);
    return new
    {
        oneAsBoolean = info.GetBoolean("one"),
        integerTextAsLong = info.GetInt64("integerText"),
        decimalTextAsDouble = info.GetDouble("decimalText"),
        longAsInt = info.GetInt32("long"),
        integerTextByType = info.GetValue("integerText", typeof(long)),
        decimalTextByTypeCode = new System.Runtime.Serialization.FormatterConverter()
            .Convert("1.5", TypeCode.Double),
    };
}
static object ObservePrimitiveConversionErrors()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    return new
    {
        malformedLong = ObserveMethodError(() => converter.ToInt64("oops")),
        overflowLong = ObserveMethodError(() => converter.ToInt64("9223372036854775808")),
        overflowInt = ObserveMethodError(() => converter.ToInt32(5000000000L)),
        malformedDouble = ObserveMethodError(() => converter.ToDouble("oops")),
        nullLong = ObserveMethodError(() => converter.ToInt64(null!)),
        nullLongParameter = ObserveMethodArgumentName(() => converter.ToInt64(null!)),
        nullDouble = ObserveMethodError(() => converter.ToDouble(null!)),
        nullDoubleParameter = ObserveMethodArgumentName(() => converter.ToDouble(null!)),
    };
}
static object ObserveSerializationInfoObjectMembers()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    object marker = new();
    info.AddValue("item", marker);
    info.AddValue("empty", (object?)null);
    info.AddValue("typedEmpty", null, typeof(string));
    var cursor = info.GetEnumerator();
    var types = new List<string>();
    while (cursor.MoveNext())
    {
        types.Add(cursor.ObjectType.FullName!);
    }
    return new
    {
        count = info.MemberCount,
        markerSame = ReferenceEquals(info.GetValue("item", typeof(object)), marker),
        emptyObject = info.GetValue("empty", typeof(object)),
        emptyString = info.GetValue("empty", typeof(string)),
        typedEmptyString = info.GetString("typedEmpty"),
        types,
    };
}
static object ObserveSerializationInfoGetValueTypes()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    object marker = new();
    info.AddValue("text", "hello");
    info.AddValue("marker", marker);
    return new
    {
        textAsObject = info.GetValue("text", typeof(object)),
        textAsComparable = info.GetValue("text", typeof(IComparable)),
        markerAsObjectSame = ReferenceEquals(info.GetValue("marker", typeof(object)), marker),
        markerAsStringError = ObserveMethodError(() => info.GetValue("marker", typeof(string))),
        nullNameError = ObserveMethodError(() => info.GetValue(null!, typeof(object))),
        nullNameParameter = ObserveMethodArgumentName(() => info.GetValue(null!, typeof(object))),
    };
}
static object ObserveSerializationInfoMemberNames()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("", 1);
    info.AddValue("Name", 2);
    info.AddValue("name", 3);
    return new
    {
        count = info.MemberCount,
        empty = info.GetInt32(""),
        uppercase = info.GetInt32("Name"),
        lowercase = info.GetInt32("name"),
        duplicateError = ObserveMethodError(() => info.AddValue("Name", 4)),
        wrongCaseError = ObserveMethodError(() => info.GetInt32("NAME")),
    };
}
static object ObserveSerializationInfoEnumeratorResetCycles()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("first", 1);
    info.AddValue("second", 2);
    var cursor = info.GetEnumerator();
    cursor.MoveNext();
    var firstName = cursor.Name;
    cursor.Reset();
    var currentAfterReset = ObserveMethodError(() => { _ = cursor.Current; });
    cursor.MoveNext();
    var firstAfterReset = cursor.Name;
    cursor.MoveNext();
    var secondAfterReset = cursor.Name;
    var exhausted = cursor.MoveNext();
    cursor.Reset();
    var firstAfterSecondReset = cursor.MoveNext() ? cursor.Name : null;
    return new { firstName, currentAfterReset, firstAfterReset,
        secondAfterReset, exhausted, firstAfterSecondReset };
}
static object ObserveSerializationInfoEnumeratorInterface()
{
    var type = typeof(System.Runtime.Serialization.SerializationInfoEnumerator);
    return new
    {
        interfaces = type.GetInterfaces().Select(item => item.FullName).ToArray(),
        declaredMethods = type.GetMethods(BindingFlags.Public | BindingFlags.Instance
            | BindingFlags.DeclaredOnly)
            .Select(method => new { name = method.Name,
                result = method.ReturnType.FullName })
            .OrderBy(method => method.name).ToArray(),
        currentType = type.GetProperty("Current")?.PropertyType.FullName,
        assignable = typeof(System.Collections.IEnumerator).IsAssignableFrom(type),
        instance = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
            new System.Runtime.Serialization.FormatterConverter()).GetEnumerator()
            is System.Collections.IEnumerator,
    };
}
static object ObserveSerializationEntryShape()
{
    var type = typeof(System.Runtime.Serialization.SerializationEntry);
    var empty = default(System.Runtime.Serialization.SerializationEntry);
    return new
    {
        baseType = type.BaseType?.FullName,
        isValueType = type.IsValueType,
        publicConstructorCount = type.GetConstructors(BindingFlags.Public | BindingFlags.Instance).Length,
        properties = type.GetProperties(BindingFlags.Public | BindingFlags.Instance
            | BindingFlags.DeclaredOnly).Select(property => new { name = property.Name,
                type = property.PropertyType.FullName }).OrderBy(property => property.name).ToArray(),
        defaultName = empty.Name,
        defaultObjectType = empty.ObjectType?.FullName,
        defaultValue = empty.Value,
    };
}
static object ObserveSerializationEntryValueSnapshot()
{
    var values = new List<int> { 1 };
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("values", values, typeof(List<int>));
    var cursor = info.GetEnumerator();
    cursor.MoveNext();
    var entry = cursor.Current;
    info.AddValue("second", 2);
    values.Add(3);
    return new
    {
        entryName = entry.Name,
        entryType = entry.ObjectType.FullName,
        sameValueReference = ReferenceEquals(entry.Value, values),
        updatedValueCount = ((List<int>)entry.Value).Count,
        entryNameAfterAdd = entry.Name,
        cursorHasSecond = cursor.MoveNext(),
        freshMemberCount = info.MemberCount,
    };
}
static object ObserveSerializationEntryEquality()
{
    static System.Runtime.Serialization.SerializationEntry Entry(string name, object value)
    {
        var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
            new System.Runtime.Serialization.FormatterConverter());
        info.AddValue(name, value);
        var cursor = info.GetEnumerator();
        cursor.MoveNext();
        return cursor.Current;
    }
    object shared = new();
    var first = Entry("item", shared);
    var equal = Entry("item", shared);
    var differentName = Entry("other", shared);
    var differentValue = Entry("item", new object());
    var empty = default(System.Runtime.Serialization.SerializationEntry);
    return new
    {
        equalEntries = first.Equals(equal),
        equalHashes = first.GetHashCode() == equal.GetHashCode(),
        differentNameEqual = first.Equals(differentName),
        differentValueEqual = first.Equals(differentValue),
        defaultEqual = empty.Equals(default(System.Runtime.Serialization.SerializationEntry)),
        defaultText = empty.ToString(),
        populatedText = first.ToString(),
    };
}
static object ObserveSerializationEntryTypeEquality()
{
    static System.Runtime.Serialization.SerializationEntry Entry(object? value, Type type)
    {
        var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
            new System.Runtime.Serialization.FormatterConverter());
        info.AddValue("item", value, type);
        var cursor = info.GetEnumerator();
        cursor.MoveNext();
        return cursor.Current;
    }
    var text = Entry("same", typeof(string));
    var objectTyped = Entry("same", typeof(object));
    var changedValue = Entry("different", typeof(string));
    var nullA = Entry(null, typeof(string));
    var nullB = Entry(null, typeof(string));
    return new
    {
        differentDeclaredTypeEqual = text.Equals(objectTyped),
        differentValueEqual = text.Equals(changedValue),
        sameNullEqual = nullA.Equals(nullB),
        sameNullHash = nullA.GetHashCode() == nullB.GetHashCode(),
        nullVersusTextEqual = nullA.Equals(text),
    };
}
static object ObserveSerializationInfoDuplicateState()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("item", 42);
    var duplicateError = ObserveMethodError(() => info.AddValue("item", 99));
    var cursor = info.GetEnumerator();
    cursor.MoveNext();
    return new
    {
        duplicateError,
        count = info.MemberCount,
        original = info.GetInt32("item"),
        enumeratedValue = cursor.Value,
        secondMove = cursor.MoveNext(),
    };
}
static object ObserveSerializationInfoValueOverloads()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("character", 'Q');
    info.AddValue("single", 1.25f);
    info.AddValue("decimal", 12m);
    info.AddValue("date", new DateTime(2024, 2, 29));
    var cursor = info.GetEnumerator();
    var types = new List<string>();
    while (cursor.MoveNext())
    {
        types.Add(cursor.ObjectType.FullName!);
    }
    return new
    {
        count = info.MemberCount,
        character = info.GetChar("character").ToString(),
        single = info.GetSingle("single"),
        decimalText = info.GetDecimal("decimal").ToString(),
        date = info.GetDateTime("date").ToString("yyyy-MM-dd"),
        types,
    };
}
static object ObserveSerializationInfoNumericOverloads()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("signed", (short)-1234);
    info.AddValue("unsigned", ulong.MaxValue);
    var cursor = info.GetEnumerator();
    var types = new List<string>();
    while (cursor.MoveNext())
    {
        types.Add(cursor.ObjectType.FullName!);
    }
    return new
    {
        count = info.MemberCount,
        signed = info.GetInt16("signed"),
        unsignedText = info.GetUInt64("unsigned").ToString(),
        types,
        unsignedTypeCode = Type.GetTypeCode(typeof(ulong)).ToString(),
    };
}
static object ObserveSerializationInfoUnsignedMembers()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("u16", (ushort)60000);
    info.AddValue("u32", (uint)4000000000);
    var cursor = info.GetEnumerator();
    var types = new List<string>();
    while (cursor.MoveNext())
    {
        types.Add(cursor.ObjectType.FullName!);
    }
    return new
    {
        count = info.MemberCount,
        u16 = info.GetUInt16("u16"),
        u32 = info.GetUInt32("u32"),
        types,
        u16TypeCode = Type.GetTypeCode(typeof(ushort)).ToString(),
        u32TypeCode = Type.GetTypeCode(typeof(uint)).ToString(),
    };
}
static object ObserveSerializationInfoByteMembers()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("byte", (byte)200);
    info.AddValue("sbyte", (sbyte)-5);
    var cursor = info.GetEnumerator();
    var types = new List<string>();
    while (cursor.MoveNext())
    {
        types.Add(cursor.ObjectType.FullName!);
    }
    return new
    {
        count = info.MemberCount,
        byteValue = info.GetByte("byte"),
        sbyteValue = info.GetSByte("sbyte"),
        types,
        byteTypeCode = Type.GetTypeCode(typeof(byte)).ToString(),
        sbyteTypeCode = Type.GetTypeCode(typeof(sbyte)).ToString(),
    };
}
static object ObserveSerializationInfoByteConversions()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), converter);
    info.AddValue("byteText", "255");
    info.AddValue("sbyteText", "-128");
    return new
    {
        byteText = info.GetByte("byteText"),
        sbyteText = info.GetSByte("sbyteText"),
        byteInteger = converter.ToByte(200),
        sbyteInteger = converter.ToSByte(-5),
        byteType = converter.Convert("200", typeof(byte)),
        sbyteTypeCode = converter.Convert("-5", TypeCode.SByte),
        byteOverflowHigh = ObserveMethodError(() => converter.ToByte("256")),
        byteOverflowLow = ObserveMethodError(() => converter.ToByte(-1)),
        sbyteOverflowHigh = ObserveMethodError(() => converter.ToSByte("128")),
        sbyteOverflowLow = ObserveMethodError(() => converter.ToSByte(-129)),
        byteFormat = ObserveMethodError(() => converter.ToByte("bad")),
        sbyteFormat = ObserveMethodError(() => converter.ToSByte("bad")),
        byteNull = ObserveMethodError(() => converter.ToByte(null!)),
    };
}
static object ObserveByteConvertibleContract()
{
    IConvertible unsigned = (byte)200;
    IConvertible signed = (sbyte)-5;
    return new
    {
        byteConvertible = typeof(IConvertible).IsAssignableFrom(typeof(byte)),
        sbyteConvertible = typeof(IConvertible).IsAssignableFrom(typeof(sbyte)),
        byteTypeCode = unsigned.GetTypeCode().ToString(),
        sbyteTypeCode = signed.GetTypeCode().ToString(),
        byteToInt32 = unsigned.ToInt32(null),
        sbyteToInt32 = signed.ToInt32(null),
        byteToString = unsigned.ToString(null),
        sbyteToString = signed.ToString(null),
        byteToSByte = ObserveMethodError(() => unsigned.ToSByte(null)),
        sbyteToByte = ObserveMethodError(() => signed.ToByte(null)),
        byteToDateTime = ObserveMethodError(() => unsigned.ToDateTime(null)),
    };
}
static object ObserveByteToTypeContract()
{
    IConvertible unsigned = (byte)200;
    IConvertible signed = (sbyte)-5;
    return new
    {
        byteSelf = unsigned.ToType(typeof(byte), null).GetType().FullName,
        sbyteSelf = signed.ToType(typeof(sbyte), null).GetType().FullName,
        byteInt = unsigned.ToType(typeof(int), null),
        sbyteInt = signed.ToType(typeof(int), null),
        byteString = unsigned.ToType(typeof(string), null),
        sbyteString = signed.ToType(typeof(string), null),
        byteDecimal = unsigned.ToType(typeof(decimal), null).ToString(),
        sbyteDecimal = signed.ToType(typeof(decimal), null).ToString(),
        byteToSByte = ObserveMethodError(() => unsigned.ToType(typeof(sbyte), null)),
        sbyteToByte = ObserveMethodError(() => signed.ToType(typeof(byte), null)),
        byteNull = ObserveMethodError(() => unsigned.ToType(null!, null)),
    };
}
static object ObserveUInt16ConvertibleContract()
{
    IConvertible value = (ushort)60000;
    return new
    {
        implements = typeof(IConvertible).IsAssignableFrom(typeof(ushort)),
        typeCode = value.GetTypeCode().ToString(),
        int32 = value.ToInt32(null),
        uint32 = value.ToUInt32(null),
        text = value.ToString(null),
        byteOverflow = ObserveMethodError(() => value.ToByte(null)),
        int16Overflow = ObserveMethodError(() => value.ToInt16(null)),
        dateTime = ObserveMethodError(() => value.ToDateTime(null)),
    };
}
static object ObserveUInt32ConvertibleContract()
{
    IConvertible value = (uint)4000000000;
    return new
    {
        implements = typeof(IConvertible).IsAssignableFrom(typeof(uint)),
        typeCode = value.GetTypeCode().ToString(),
        int64 = value.ToInt64(null),
        uint32 = value.ToUInt32(null),
        uint64Text = value.ToUInt64(null).ToString(),
        decimalText = value.ToDecimal(null).ToString(),
        text = value.ToString(null),
        int32Overflow = ObserveMethodError(() => value.ToInt32(null)),
        byteOverflow = ObserveMethodError(() => value.ToByte(null)),
        dateTime = ObserveMethodError(() => value.ToDateTime(null)),
    };
}
static object ObserveUnsignedFormatterRoutes()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), converter);
    info.AddValue("u16Text", "60000");
    info.AddValue("u32Text", "4000000000");
    return new
    {
        u16Text = info.GetUInt16("u16Text"),
        u32Text = info.GetUInt32("u32Text"),
        u16Type = converter.Convert("60000", typeof(ushort)),
        u32TypeCode = converter.Convert("4000000000", TypeCode.UInt32),
        u16Overflow = ObserveMethodError(() => converter.ToUInt16("65536")),
        u32Overflow = ObserveMethodError(() => converter.ToUInt32("4294967296")),
        negativeOverflow = ObserveMethodError(() => converter.ToUInt32("-1")),
        format = ObserveMethodError(() => converter.ToUInt16("bad")),
        nullValue = ObserveMethodError(() => converter.ToUInt32(null!)),
    };
}
static object ObserveUnsignedToTypeContract()
{
    IConvertible u16 = (ushort)60000;
    IConvertible u32 = (uint)4000000000;
    return new
    {
        u16Self = u16.ToType(typeof(ushort), null).GetType().FullName,
        u32Self = u32.ToType(typeof(uint), null).GetType().FullName,
        u16ToUInt32 = u16.ToType(typeof(uint), null),
        u16ToInt32 = u16.ToType(typeof(int), null),
        u32ToInt64 = u32.ToType(typeof(long), null),
        u32ToDecimal = u32.ToType(typeof(decimal), null).ToString(),
        u32ToString = u32.ToType(typeof(string), null),
        u32ToInt32 = ObserveMethodError(() => u32.ToType(typeof(int), null)),
        u32ToUInt16 = ObserveMethodError(() => u32.ToType(typeof(ushort), null)),
        u16Null = ObserveMethodError(() => u16.ToType(null!, null)),
    };
}
static object ObserveInt16SingleFormatterRoutes()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), converter);
    info.AddValue("int16Text", "-1234");
    info.AddValue("singleText", "1.25");
    return new
    {
        int16Text = info.GetInt16("int16Text"),
        singleText = info.GetSingle("singleText"),
        int16Type = converter.Convert("-1234", typeof(short)),
        singleTypeCode = converter.Convert("1.25", TypeCode.Single),
        int16OverflowHigh = ObserveMethodError(() => converter.ToInt16("32768")),
        int16OverflowLow = ObserveMethodError(() => converter.ToInt16("-32769")),
        int16Format = ObserveMethodError(() => converter.ToInt16("bad")),
        singleFormat = ObserveMethodError(() => converter.ToSingle("bad")),
        singleNull = ObserveMethodError(() => converter.ToSingle(null!)),
    };
}
static object ObserveUInt64FormatterRoutes()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), converter);
    info.AddValue("u64Text", "18446744073709551615");
    return new
    {
        text = info.GetUInt64("u64Text").ToString(),
        type = converter.Convert("18446744073709551615", typeof(ulong)).ToString(),
        typeCode = converter.Convert("18446744073709551615", TypeCode.UInt64).ToString(),
        overflow = ObserveMethodError(() => converter.ToUInt64("18446744073709551616")),
        negative = ObserveMethodError(() => converter.ToUInt64("-1")),
        format = ObserveMethodError(() => converter.ToUInt64("bad")),
        nullValue = ObserveMethodError(() => converter.ToUInt64(null!)),
    };
}
static object ObserveDecimalFormatterRoutes()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), converter);
    info.AddValue("decimalText", "12.5");
    return new
    {
        text = info.GetDecimal("decimalText").ToString(),
        type = converter.Convert("12.5", typeof(decimal)).ToString(),
        typeCode = converter.Convert("12.5", TypeCode.Decimal).ToString(),
        integer = converter.ToDecimal(42).ToString(),
        format = ObserveMethodError(() => converter.ToDecimal("bad")),
        nullValue = ObserveMethodError(() => converter.ToDecimal(null!)),
    };
}
static object ObserveDateTimeFormatterRoutes()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), converter);
    info.AddValue("dateText", "2024-02-29");
    return new
    {
        text = info.GetDateTime("dateText").ToString("yyyy-MM-dd"),
        type = ((DateTime)converter.Convert("2024-02-29", typeof(DateTime))).ToString("yyyy-MM-dd"),
        typeCode = ((DateTime)converter.Convert("2024-02-29", TypeCode.DateTime)).ToString("yyyy-MM-dd"),
        invalid = ObserveMethodError(() => converter.ToDateTime("bad")),
        impossible = ObserveMethodError(() => converter.ToDateTime("2023-02-29")),
        nullValue = ObserveMethodError(() => converter.ToDateTime(null!)),
    };
}
static object ObserveCharFormatterRoutes()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), converter);
    info.AddValue("charText", "Q");
    return new
    {
        text = info.GetChar("charText").ToString(),
        type = converter.Convert("Q", typeof(char)).ToString(),
        typeCode = converter.Convert("Q", TypeCode.Char).ToString(),
        integer = converter.ToChar(65).ToString(),
        empty = ObserveMethodError(() => converter.ToChar("")),
        longText = ObserveMethodError(() => converter.ToChar("AB")),
        nullValue = ObserveMethodError(() => converter.ToChar(null!)),
    };
}
static object ObserveFormatterObjectRoutes()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    object token = new object();
    object number = 42;
    return new
    {
        objectTypeSame = ReferenceEquals(number, converter.Convert(number, typeof(object))),
        objectCodeSame = ReferenceEquals(number, converter.Convert(number, TypeCode.Object)),
        plainObjectType = ObserveMethodError(() => converter.Convert(token, typeof(object))),
        plainObjectCode = ObserveMethodError(() => converter.Convert(token, TypeCode.Object)),
        integerCode = converter.Convert(42, TypeCode.Object),
        nullType = ObserveMethodError(() => converter.Convert(null!, typeof(object))),
        nullCode = ObserveMethodError(() => converter.Convert(null!, TypeCode.Object)),
        nullTarget = ObserveMethodError(() => converter.Convert(token, (Type)null!)),
    };
}
static object ObserveFormatterTypeCodeBoundaries()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    return new
    {
        dbNullCode = ObserveMethodError(() => converter.Convert(DBNull.Value, TypeCode.DBNull)),
        dbNullType = ObserveMethodError(() => converter.Convert(DBNull.Value, typeof(DBNull))),
        integerToDBNull = ObserveMethodError(() => converter.Convert(42, TypeCode.DBNull)),
        integerToEmpty = ObserveMethodError(() => converter.Convert(42, TypeCode.Empty)),
        dbNullToEmpty = ObserveMethodError(() => converter.Convert(DBNull.Value, TypeCode.Empty)),
        nullToDBNull = ObserveMethodError(() => converter.Convert(null!, TypeCode.DBNull)),
    };
}
static object ObserveSerializationGetValueConversions()
{
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull),
        new System.Runtime.Serialization.FormatterConverter());
    info.AddValue("u64", ulong.MaxValue);
    info.AddValue("u32", (uint)4000000000);
    info.AddValue("byte", (byte)200);
    info.AddValue("dateText", "2024-02-29");
    return new
    {
        u64String = info.GetValue("u64", typeof(string)),
        u32String = info.GetValue("u32", typeof(string)),
        byteString = info.GetValue("byte", typeof(string)),
        date = ((DateTime)info.GetValue("dateText", typeof(DateTime))!).ToString("yyyy-MM-dd"),
        u32ToInt32 = ObserveMethodError(() => info.GetValue("u32", typeof(int))),
    };
}
static object ObserveDateTimeConvertibleContract()
{
    var date = new DateTime(2024, 2, 29);
    IConvertible convertible = date;
    return new
    {
        implements = typeof(IConvertible).IsAssignableFrom(typeof(DateTime)),
        typeCode = convertible.GetTypeCode().ToString(),
        dateSame = ReferenceEquals(date, convertible.ToDateTime(null)),
        invariantText = convertible.ToString(System.Globalization.CultureInfo.InvariantCulture),
        int32 = ObserveMethodError(() => convertible.ToInt32(null)),
        boolean = ObserveMethodError(() => convertible.ToBoolean(null)),
        byteValue = ObserveMethodError(() => convertible.ToByte(null)),
        selfTypeSame = ReferenceEquals(date, convertible.ToType(typeof(DateTime), null)),
    };
}
static object ObserveDecimalConvertibleContract()
{
    decimal value = 12.5m;
    IConvertible convertible = value;
    return new
    {
        implements = typeof(IConvertible).IsAssignableFrom(typeof(decimal)),
        typeCode = convertible.GetTypeCode().ToString(),
        int32 = convertible.ToInt32(null),
        roundedUp = ((IConvertible)13.5m).ToInt32(null),
        doubleValue = convertible.ToDouble(null),
        boolean = convertible.ToBoolean(null),
        text = convertible.ToString(System.Globalization.CultureInfo.InvariantCulture),
        selfValue = convertible.ToDecimal(null).ToString(),
        charValue = ObserveMethodError(() => convertible.ToChar(null)),
        dateTime = ObserveMethodError(() => convertible.ToDateTime(null)),
    };
}
static object ObserveUInt64CrossConversions()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    var info = new System.Runtime.Serialization.SerializationInfo(typeof(DBNull), converter);
    info.AddValue("u64", ulong.MaxValue);
    return new
    {
        decimalText = converter.ToDecimal(ulong.MaxValue).ToString(),
        getValueDecimal = ((decimal)info.GetValue("u64", typeof(decimal))!).ToString(),
        maxToInt64 = ObserveMethodError(() => converter.ToInt64(ulong.MaxValue)),
        smallToInt64 = converter.ToInt64((ulong)42),
        maxToUInt32 = ObserveMethodError(() => converter.ToUInt32(ulong.MaxValue)),
    };
}
static object ObserveUnsignedConvertResultIdentity()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    object byteByType = converter.Convert("200", typeof(byte));
    object sbyteByCode = converter.Convert("-5", TypeCode.SByte);
    object u16ByType = converter.Convert("60000", typeof(ushort));
    object u32ByCode = converter.Convert("4000000000", TypeCode.UInt32);
    return new
    {
        types = new[] {byteByType.GetType().FullName, sbyteByCode.GetType().FullName,
            u16ByType.GetType().FullName, u32ByCode.GetType().FullName},
        values = new[] {byteByType.ToString(), sbyteByCode.ToString(),
            u16ByType.ToString(), u32ByCode.ToString()},
    };
}
static object ObserveUInt64NarrowingConversions()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    ulong small = 42;
    ulong maximum = ulong.MaxValue;
    return new
    {
        int32Small = converter.ToInt32(small),
        byteSmall = converter.ToByte(small),
        u16Small = converter.ToUInt16(small),
        int32Max = ObserveMethodError(() => converter.ToInt32(maximum)),
        byteMax = ObserveMethodError(() => converter.ToByte(maximum)),
        u16Max = ObserveMethodError(() => converter.ToUInt16(maximum)),
    };
}
static object ObserveInt64NarrowingConversions()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    long small = 42;
    long large = 5000000000;
    return new
    {
        byteSmall = converter.ToByte(small),
        sbyteSmall = converter.ToSByte(small),
        int16Small = converter.ToInt16(small),
        u16Small = converter.ToUInt16(small),
        u32Small = converter.ToUInt32(small),
        byteLarge = ObserveMethodError(() => converter.ToByte(large)),
        u32Large = ObserveMethodError(() => converter.ToUInt32(large)),
        negativeU32 = ObserveMethodError(() => converter.ToUInt32(-1L)),
    };
}
static object ObserveInt64WideningConversions()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    long value = 5000000000;
    return new
    {
        text = converter.ToString(value),
        decimalText = converter.ToDecimal(value).ToString(),
        doubleValue = converter.ToDouble(value),
        boolean = converter.ToBoolean(value),
        uint64Text = converter.ToUInt64(value).ToString(),
        negativeUInt64 = ObserveMethodError(() => converter.ToUInt64(-1L)),
    };
}
static object ObserveFloatingFormatterConversions()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    return new
    {
        doubleToSingle = converter.ToSingle(1.25d),
        singleToDouble = converter.ToDouble(1.25f),
        doubleToDecimal = converter.ToDecimal(1.25d).ToString(),
        singleToDecimal = converter.ToDecimal(1.25f).ToString(),
        midpointEven = converter.ToInt32(2.5d),
        midpointUp = converter.ToInt32(3.5d),
        doubleBoolean = converter.ToBoolean(1.25d),
        hugeInt32 = ObserveMethodError(() => converter.ToInt32(double.MaxValue)),
    };
}
static object ObserveFloatingExceptionalBoundaries()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    return new
    {
        nanInt32 = ObserveMethodError(() => converter.ToInt32(double.NaN)),
        infinityInt32 = ObserveMethodError(() => converter.ToInt32(double.PositiveInfinity)),
        nanDecimal = ObserveMethodError(() => converter.ToDecimal(double.NaN)),
        infinityDecimal = ObserveMethodError(() => converter.ToDecimal(double.PositiveInfinity)),
        nanBoolean = converter.ToBoolean(double.NaN),
        infinitySingle = float.IsPositiveInfinity(converter.ToSingle(double.PositiveInfinity)),
        nanDouble = double.IsNaN(converter.ToDouble(float.NaN)),
    };
}
static object ObserveFloatingTextConversions()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    return new
    {
        nanSingle = float.IsNaN(converter.ToSingle("NaN")),
        nanDouble = double.IsNaN(converter.ToDouble("NaN")),
        infinitySingle = float.IsPositiveInfinity(converter.ToSingle("Infinity")),
        infinityDouble = double.IsNegativeInfinity(converter.ToDouble("-Infinity")),
        nanText = converter.ToString(float.NaN),
        positiveInfinityText = converter.ToString(double.PositiveInfinity),
        negativeInfinityText = converter.ToString(double.NegativeInfinity),
    };
}
static object ObserveBooleanTextConversions()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    return new
    {
        paddedTrue = converter.ToBoolean("  True  "),
        mixedCaseFalse = converter.ToBoolean("fAlSe"),
        tabbedTrue = converter.ToBoolean("\ttrue\r\n"),
        numericText = ObserveMethodError(() => converter.ToBoolean("1")),
        emptyText = ObserveMethodError(() => converter.ToBoolean("")),
        nullValue = ObserveMethodError(() => converter.ToBoolean(null!)),
    };
}
static object ObserveDecimalIntegerLimits()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    return new
    {
        maximum = decimal.Parse("79228162514264337593543950335").ToString(),
        minimum = decimal.Parse("-79228162514264337593543950335").ToString(),
        maximumPlusOne = ObserveMethodError(() => decimal.Parse("79228162514264337593543950336")),
        minimumMinusOne = ObserveMethodError(() => decimal.Parse("-79228162514264337593543950336")),
        converterOverflow = ObserveMethodError(() => converter.ToDecimal("79228162514264337593543950336")),
    };
}
static object ObserveFloatingTextGrammar()
{
    var converter = new System.Runtime.Serialization.FormatterConverter();
    return new
    {
        decimalSingle = converter.ToSingle(" 1.25 "),
        exponentDouble = converter.ToDouble("1.25e2"),
        singleSuffix = ObserveMethodError(() => converter.ToSingle("1.25f")),
        doubleSuffix = ObserveMethodError(() => converter.ToDouble("1.25d")),
        hexadecimalFloat = ObserveMethodError(() => converter.ToDouble("0x1p0")),
    };
}
static object ObserveDecimalGroupedText()
{
    var invariant = System.Globalization.CultureInfo.InvariantCulture;
    return new
    {
        grouped = decimal.Parse("1,234.50", invariant).ToString(invariant),
        negativeGrouped = decimal.Parse("-1,234.50", invariant).ToString(invariant),
    };
}
static object ObserveInt32NoneStyle()
{
    var style = System.Globalization.NumberStyles.None;
    var invariant = System.Globalization.CultureInfo.InvariantCulture;
    return new
    {
        digits = int.Parse("42", style, invariant),
        leadingSign = ObserveMethodError(() => int.Parse("+42", style, invariant)),
        leadingSpace = ObserveMethodError(() => int.Parse(" 42", style, invariant)),
        trailingSpace = ObserveMethodError(() => int.Parse("42 ", style, invariant)),
        tryLeadingSign = int.TryParse("+42", style, invariant, out _),
    };
}
static object ObserveInt32BinaryStyle()
{
    var style = System.Globalization.NumberStyles.BinaryNumber;
    var invariant = System.Globalization.CultureInfo.InvariantCulture;
    return new
    {
        value = int.Parse("101010", style, invariant),
        padded = int.Parse(" 101010 ", style, invariant),
        allBits = int.Parse(new string('1', 32), style, invariant),
        prefix = ObserveMethodError(() => int.Parse("0b101010", style, invariant)),
        overflow = ObserveMethodError(() => int.Parse(new string('1', 33), style, invariant)),
        tryPrefix = int.TryParse("0b101010", style, invariant, out _),
    };
}
static object ObserveDateTimeTimeOfDay()
{
    var invariant = System.Globalization.CultureInfo.InvariantCulture;
    var constructed = new DateTime(2026, 1, 2, 3, 4, 5);
    var parsed = DateTime.Parse("2026-01-02T03:04:05", invariant);
    return new
    {
        constructedHour = constructed.Hour,
        constructedMinute = constructed.Minute,
        constructedSecond = constructed.Second,
        constructedText = constructed.ToString("yyyy-MM-dd HH:mm:ss", invariant),
        parsedText = parsed.ToString("yyyy-MM-dd HH:mm:ss", invariant),
        convertedSame = ((IConvertible)constructed).ToDateTime(invariant) == constructed,
    };
}
static object ObserveDateTimeMilliseconds()
{
    var invariant = System.Globalization.CultureInfo.InvariantCulture;
    var constructed = new DateTime(2026, 1, 2, 3, 4, 5, 123);
    var parsed = DateTime.Parse("2026-01-02T03:04:05.123", invariant);
    return new
    {
        constructedMillisecond = constructed.Millisecond,
        constructedText = constructed.ToString("yyyy-MM-dd HH:mm:ss.fff", invariant),
        parsedMillisecond = parsed.Millisecond,
        parsedText = parsed.ToString("yyyy-MM-dd HH:mm:ss.fff", invariant),
        convertedMillisecond = ((IConvertible)constructed).ToDateTime(invariant).Millisecond,
    };
}
static object ObserveExceptionSerialization()
{
    var inner = new InvalidOperationException("inner");
    var exception = new Exception("boom", inner)
    {
        HelpLink = "https://example.test/help",
        Source = "dotj-test",
    };
    var info = new System.Runtime.Serialization.SerializationInfo(
        typeof(Exception), new System.Runtime.Serialization.FormatterConverter());
    var context = new System.Runtime.Serialization.StreamingContext(
        System.Runtime.Serialization.StreamingContextStates.All);
#pragma warning disable SYSLIB0051
    exception.GetObjectData(info, context);
    var nullError = ObserveMethodError(() => exception.GetObjectData(null!, context));
    var nullParameter = ObserveMethodArgumentName(() => exception.GetObjectData(null!, context));
#pragma warning restore SYSLIB0051
    var names = new List<string>();
    var enumerator = info.GetEnumerator();
    while (enumerator.MoveNext())
    {
        names.Add(enumerator.Name);
    }
    return new
    {
        interfaces = typeof(Exception).GetInterfaces()
            .Select(type => type.FullName).ToArray(),
        count = info.MemberCount,
        names,
        className = info.GetString("ClassName"),
        message = info.GetString("Message"),
        dataIsNull = info.GetValue("Data", typeof(System.Collections.IDictionary)) is null,
        innerSame = ReferenceEquals(info.GetValue("InnerException", typeof(Exception)), inner),
        stackTraceString = info.GetString("StackTraceString"),
        remoteStackTraceString = info.GetString("RemoteStackTraceString"),
        remoteStackIndex = info.GetInt32("RemoteStackIndex"),
        exceptionMethod = info.GetString("ExceptionMethod"),
        watsonBucketsIsNull = info.GetValue("WatsonBuckets", typeof(byte[])) is null,
        hResult = info.GetInt32("HResult"),
        helpUrl = info.GetString("HelpURL"),
        source = info.GetString("Source"),
        nullError,
        nullParameter,
    };
}
static object ObserveExceptionTargetSite()
{
    var exception = new Exception("target");
    bool beforeNull = exception.TargetSite is null;
    try
    {
        throw exception;
    }
    catch (Exception caught)
    {
        var target = caught.TargetSite;
        return new
        {
            beforeNull,
            afterExists = target is not null,
            nameContainsCaller = target?.Name.Contains("ObserveExceptionTargetSite") ?? false,
            memberType = target?.MemberType.ToString(),
            repeatedSame = ReferenceEquals(target, caught.TargetSite),
        };
    }
}
static object ObserveExceptionDataDictionary()
{
    var dictionary = new Exception("data").Data;
    int initialCount = dictionary.Count;
    dictionary.Add("key", "first");
    bool containsAfterAdd = dictionary.Contains("key");
    object? firstValue = dictionary["key"];
    int keysCount = dictionary.Keys.Count;
    int valuesCount = dictionary.Values.Count;
    var enumerator = dictionary.GetEnumerator();
    bool enumeratorMoved = enumerator.MoveNext();
    object? enumeratedKey = enumerator.Key;
    object? enumeratedValue = enumerator.Value;
    var copiedEntries = new System.Collections.DictionaryEntry[1];
    dictionary.CopyTo(copiedEntries, 0);
    object? copiedKey = copiedEntries[0].Key;
    object? copiedValue = copiedEntries[0].Value;
    string duplicateError = ObserveMethodError(() => dictionary.Add("key", "duplicate"));
    dictionary["key"] = "second";
    object? replacedValue = dictionary["key"];
    dictionary.Remove("key");
    int countAfterRemove = dictionary.Count;
    dictionary.Add("another", 42);
    dictionary.Clear();
    return new
    {
        interfaceName = typeof(System.Collections.IDictionary).FullName,
        interfaceMethods = typeof(System.Collections.IDictionary)
            .GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
            .Where(method => !method.IsSpecialName).Select(method => method.Name).ToArray(),
        interfaceProperties = typeof(System.Collections.IDictionary)
            .GetProperties(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
            .Select(property => property.Name).ToArray(),
        baseInterfaces = typeof(System.Collections.IDictionary).GetInterfaces()
            .Select(type => type.FullName).ToArray(),
        collectionMethods = typeof(System.Collections.ICollection)
            .GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
            .Where(method => !method.IsSpecialName).Select(method => method.Name).ToArray(),
        collectionProperties = typeof(System.Collections.ICollection)
            .GetProperties(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
            .Select(property => property.Name).ToArray(),
        enumerableMethods = typeof(System.Collections.IEnumerable)
            .GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
            .Select(method => method.Name).ToArray(),
        enumeratorProperties = typeof(System.Collections.IDictionaryEnumerator)
            .GetProperties(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
            .Select(property => property.Name).ToArray(),
        entryIsValueType = typeof(System.Collections.DictionaryEntry).IsValueType,
        initialCount,
        containsAfterAdd,
        firstValue,
        keysCount,
        valuesCount,
        enumeratorMoved,
        enumeratedKey,
        enumeratedValue,
        copiedKey,
        copiedValue,
        duplicateError,
        replacedValue,
        countAfterRemove,
        countAfterClear = dictionary.Count,
        isReadOnly = dictionary.IsReadOnly,
        isFixedSize = dictionary.IsFixedSize,
    };
}
static object ObserveExceptionDataBoundaries()
{
    var dictionary = new Exception("boundaries").Data;
    string nullAdd = ObserveMethodError(() => dictionary.Add(null!, "value"));
    string nullContains = ObserveMethodError(() => dictionary.Contains(null!));
    string nullRead = ObserveMethodError(() => { _ = dictionary[null!]; });
    string nullWrite = ObserveMethodError(() => dictionary[null!] = "value");
    string nullRemove = ObserveMethodError(() => dictionary.Remove(null!));
    dictionary.Add("nullable", null);
    bool containsNullValue = dictionary.Contains("nullable");
    object? nullValue = dictionary["nullable"];
    object key = new();
    dictionary.Add(key, 42);
    bool objectKeyRetained = dictionary.Contains(key) && (int)dictionary[key]! == 42;
    var enumerator = dictionary.GetEnumerator();
    string beforeMove = ObserveMethodError(() => { _ = enumerator.Entry; });
    while (enumerator.MoveNext()) { }
    string afterEnd = ObserveMethodError(() => { _ = enumerator.Entry; });
    return new { nullAdd, nullContains, nullRead, nullWrite, nullRemove,
        containsNullValue, nullValue, objectKeyRetained, beforeMove, afterEnd };
}
static object ObserveExceptionDataEnumeratorMutation()
{
    object Probe(Action<System.Collections.IDictionary> mutate)
    {
        var dictionary = new Exception("enumerator").Data;
        dictionary.Add("first", 1);
        dictionary.Add("second", 2);
        var enumerator = dictionary.GetEnumerator();
        bool firstMoved = enumerator.MoveNext();
        mutate(dictionary);
        string? currentError = ObserveMethodError(() => { _ = enumerator.Entry; });
        string? moveError = ObserveMethodError(() => { _ = enumerator.MoveNext(); });
        string? resetError = ObserveMethodError(() => enumerator.Reset());
        return new { firstMoved, currentError, moveError, resetError };
    }
    return new
    {
        add = Probe(dictionary => dictionary.Add("third", 3)),
        replace = Probe(dictionary => dictionary["second"] = 20),
        remove = Probe(dictionary => dictionary.Remove("second")),
        clear = Probe(dictionary => dictionary.Clear()),
    };
}
static object ObserveExceptionDataViewEnumeration()
{
    object Probe(bool keys, Action<System.Collections.IDictionary> mutate)
    {
        var dictionary = new Exception("views").Data;
        dictionary.Add("first", 1);
        dictionary.Add("second", 2);
        var view = keys ? dictionary.Keys : dictionary.Values;
        var enumerator = view.GetEnumerator();
        bool firstMoved = enumerator.MoveNext();
        object? firstCurrent = enumerator.Current;
        mutate(dictionary);
        string? currentError = ObserveMethodError(() => { _ = enumerator.Current; });
        string? moveError = ObserveMethodError(() => { _ = enumerator.MoveNext(); });
        string? resetError = ObserveMethodError(() => enumerator.Reset());
        return new { firstMoved, firstCurrent, currentError, moveError, resetError,
            liveCount = view.Count };
    }
    return new
    {
        keysAdd = Probe(true, value => value.Add("third", 3)),
        keysReplace = Probe(true, value => value["second"] = 20),
        keysRemove = Probe(true, value => value.Remove("second")),
        keysClear = Probe(true, value => value.Clear()),
        valuesAdd = Probe(false, value => value.Add("third", 3)),
        valuesReplace = Probe(false, value => value["second"] = 20),
        valuesRemove = Probe(false, value => value.Remove("second")),
        valuesClear = Probe(false, value => value.Clear()),
    };
}
static object ObserveExceptionDataViewProperties()
{
    var dictionary = new Exception("view properties").Data;
    var keys = dictionary.Keys;
    var values = dictionary.Values;
    object syncRoot = dictionary.SyncRoot;
    object keySyncRoot = keys.SyncRoot;
    object valueSyncRoot = values.SyncRoot;
    dictionary.Add("first", 1);
    return new
    {
        dictionarySynchronized = dictionary.IsSynchronized,
        keysSynchronized = keys.IsSynchronized,
        valuesSynchronized = values.IsSynchronized,
        syncRootIsDictionary = ReferenceEquals(syncRoot, dictionary),
        keySyncRootIsDictionary = ReferenceEquals(keySyncRoot, dictionary),
        valueSyncRootIsDictionary = ReferenceEquals(valueSyncRoot, dictionary),
        keySyncRootIsDictionaryRoot = ReferenceEquals(keySyncRoot, syncRoot),
        valueSyncRootIsDictionaryRoot = ReferenceEquals(valueSyncRoot, syncRoot),
        repeatedKeyViewSame = ReferenceEquals(keys, dictionary.Keys),
        repeatedValueViewSame = ReferenceEquals(values, dictionary.Values),
        keysCount = keys.Count,
        valuesCount = values.Count,
    };
}
static object ObserveExceptionDataCopyToBoundaries()
{
    var dictionary = new Exception("copy").Data;
    dictionary.Add("key", 7);
    var entries = new System.Collections.DictionaryEntry[2];
    dictionary.CopyTo(entries, 1);
    var keys = new object[2];
    dictionary.Keys.CopyTo(keys, 1);
    var values = new object[2];
    dictionary.Values.CopyTo(values, 1);
    return new
    {
        nullArray = ObserveMethodError(() => dictionary.CopyTo(null!, 0)),
        nullArrayParam = ObserveMethodArgumentName(() => dictionary.CopyTo(null!, 0)),
        negativeIndex = ObserveMethodError(() => dictionary.CopyTo(new object[1], -1)),
        negativeIndexParam = ObserveMethodArgumentName(() => dictionary.CopyTo(new object[1], -1)),
        indexAtLength = ObserveMethodError(() => dictionary.CopyTo(new object[1], 1)),
        indexAtLengthParam = ObserveMethodArgumentName(() => dictionary.CopyTo(new object[1], 1)),
        tooSmall = ObserveMethodError(() => dictionary.CopyTo(new object[0], 0)),
        tooSmallParam = ObserveMethodArgumentName(() => dictionary.CopyTo(new object[0], 0)),
        wrongElement = ObserveMethodError(() => dictionary.CopyTo(new string[1], 0)),
        wrongElementParam = ObserveMethodArgumentName(() => dictionary.CopyTo(new string[1], 0)),
        multidimensional = ObserveMethodError(() => dictionary.CopyTo(new object[1, 1], 0)),
        multidimensionalParam = ObserveMethodArgumentName(() => dictionary.CopyTo(new object[1, 1], 0)),
        entryOffsetKey = entries[1].Key,
        entryOffsetValue = entries[1].Value,
        keyOffset = keys[1],
        valueOffset = values[1],
        argumentOutOfRangeConstructors = typeof(ArgumentOutOfRangeException)
            .GetConstructors(BindingFlags.Public | BindingFlags.Instance)
            .Select(constructor => constructor.GetParameters()
                .Select(parameter => parameter.ParameterType.FullName).ToArray()).ToArray(),
        argumentOutOfRangeHResult = new ArgumentOutOfRangeException("index").HResult,
    };
}
static object ObserveArgumentOutOfRangeConstructors()
{
    var inner = new Exception("inner");
    ArgumentOutOfRangeException[] values =
    [
        new(),
        new("index"),
        new("index", "custom"),
        new("custom", inner),
        new("index", 42, "custom"),
    ];
    return values.Select(value => new
    {
        paramName = value.ParamName,
        message = value.Message,
        actualValue = value.ActualValue,
        innerSame = ReferenceEquals(value.InnerException, inner),
        hResult = value.HResult,
    }).ToArray();
}
static object ObserveInt32BitHelpers()
{
    int[] values = [0, 1, 2, 3, -1, int.MinValue, int.MaxValue, 0x40000000];
    (int Value, int Amount)[] rotations = [(1, 1), (-1, 1), (int.MinValue, 31), (1, 32), (1, -1)];
    return new
    {
        values = values.Select(value => new
        {
            value,
            isEven = int.IsEvenInteger(value),
            isOdd = int.IsOddInteger(value),
            isNegative = int.IsNegative(value),
            isPositive = int.IsPositive(value),
            isPow2 = int.IsPow2(value),
            leadingZeroCount = int.LeadingZeroCount(value),
            trailingZeroCount = int.TrailingZeroCount(value),
            popCount = int.PopCount(value),
            log2 = value >= 0 ? int.Log2(value) : (int?)null,
            log2Error = ObserveMethodError(() => { _ = int.Log2(value); }),
            log2ErrorParam = ObserveMethodArgumentName(() => { _ = int.Log2(value); }),
        }).ToArray(),
        rotations = rotations.Select(item => new
        {
            value = item.Value,
            amount = item.Amount,
            left = int.RotateLeft(item.Value, item.Amount),
            right = int.RotateRight(item.Value, item.Amount),
        }).ToArray(),
    };
}
static object ObserveInt32SignedArithmetic()
{
    int[] values = [int.MinValue, -3, -1, 0, 1, 3, int.MaxValue];
    (int X, int Y)[] pairs = [(2, 3), (-3, 3), (int.MinValue, int.MaxValue), (0, 0), (-3, -3)];
    (int Value, int Min, int Max)[] clamps = [(5, 0, 10), (-5, 0, 10), (15, 0, 10), (0, 10, 0)];
    (int Value, int Sign)[] signs = [(-3, 1), (3, -1), (int.MinValue, -1), (int.MinValue, 1), (0, -1)];
    return new
    {
        unary = values.Select(value => new
        {
            value,
            abs = value == int.MinValue ? (int?)null : int.Abs(value),
            absError = ObserveMethodError(() => { _ = int.Abs(value); }),
            sign = int.Sign(value),
        }).ToArray(),
        pairs = pairs.Select(pair => new
        {
            x = pair.X, y = pair.Y,
            max = int.Max(pair.X, pair.Y), min = int.Min(pair.X, pair.Y),
            maxMagnitude = int.MaxMagnitude(pair.X, pair.Y),
            minMagnitude = int.MinMagnitude(pair.X, pair.Y),
        }).ToArray(),
        clamps = clamps.Select(item => new
        {
            value = item.Value, min = item.Min, max = item.Max,
            result = item.Min > item.Max ? (int?)null : int.Clamp(item.Value, item.Min, item.Max),
            error = ObserveMethodError(() => { _ = int.Clamp(item.Value, item.Min, item.Max); }),
            errorParam = ObserveMethodArgumentName(() => { _ = int.Clamp(item.Value, item.Min, item.Max); }),
        }).ToArray(),
        copies = signs.Select(item => new
        {
            value = item.Value, sign = item.Sign,
            result = item.Value == int.MinValue && item.Sign >= 0 ? (int?)null : int.CopySign(item.Value, item.Sign),
            error = ObserveMethodError(() => { _ = int.CopySign(item.Value, item.Sign); }),
        }).ToArray(),
    };
}
static object ObserveInt32ValueIdentityAndBigMul()
{
    int value = 42;
    object boxed = 42;
    (int Left, int Right)[] products =
    [(int.MinValue, int.MaxValue), (int.MaxValue, int.MaxValue), (-3, 7), (0, int.MinValue)];
    return new
    {
        typedSame = value.Equals(42),
        typedDifferent = value.Equals(-42),
        objectSame = value.Equals(boxed),
        objectDifferentType = value.Equals("42"),
        objectNull = value.Equals(null),
        zeroHash = 0.GetHashCode(),
        negativeHash = (-42).GetHashCode(),
        positiveHash = value.GetHashCode(),
        products = products.Select(item => new
        {
            left = item.Left,
            right = item.Right,
            product = int.BigMul(item.Left, item.Right),
        }).ToArray(),
    };
}
static object ObserveInt32DivRem()
{
    (int Left, int Right)[] pairs =
    [(7, 3), (-7, 3), (7, -3), (int.MinValue, 3), (int.MaxValue, 1)];
    return new
    {
        pairs = pairs.Select(pair =>
        {
            var result = int.DivRem(pair.Left, pair.Right);
            return new { left = pair.Left, right = pair.Right,
                quotient = result.Item1, remainder = result.Item2 };
        }).ToArray(),
        zeroError = ObserveMethodError(() => { _ = int.DivRem(1, 0); }),
        overflowError = ObserveMethodError(() => { _ = int.DivRem(int.MinValue, -1); }),
        tupleDefinition = typeof(ValueTuple<int, int>).GetGenericTypeDefinition().FullName,
        tupleIsValueType = typeof(ValueTuple<int, int>).IsValueType,
        tupleFields = typeof(ValueTuple<int, int>).GetFields(BindingFlags.Public | BindingFlags.Instance)
            .Select(field => new { name = field.Name, type = field.FieldType.FullName,
                isInitOnly = field.IsInitOnly }).ToArray(),
        tupleConstructors = typeof(ValueTuple<int, int>).GetConstructors(BindingFlags.Public | BindingFlags.Instance)
            .Select(constructor => constructor.GetParameters()
                .Select(parameter => parameter.ParameterType.FullName).ToArray()).ToArray(),
        divideByZeroBase = typeof(DivideByZeroException).BaseType?.FullName,
        divideByZeroConstructors = typeof(DivideByZeroException)
            .GetConstructors(BindingFlags.Public | BindingFlags.Instance)
            .Select(constructor => constructor.GetParameters()
                .Select(parameter => parameter.ParameterType.FullName).ToArray()).ToArray(),
        divideByZeroHResult = new DivideByZeroException().HResult,
        divideByZeroMessage = new DivideByZeroException().Message,
        arithmeticBase = typeof(ArithmeticException).BaseType?.FullName,
        arithmeticConstructors = typeof(ArithmeticException)
            .GetConstructors(BindingFlags.Public | BindingFlags.Instance)
            .Select(constructor => constructor.GetParameters()
                .Select(parameter => parameter.ParameterType.FullName).ToArray()).ToArray(),
        arithmeticHResult = new ArithmeticException().HResult,
        arithmeticMessage = new ArithmeticException().Message,
        overflowBase = typeof(OverflowException).BaseType?.FullName,
        overflowHResult = new OverflowException().HResult,
        overflowMessage = new OverflowException().Message,
    };
}
static object ObserveInt32CreateFromInt64()
{
    long[] values = [long.MinValue, (long)int.MinValue - 1, int.MinValue, -3,
        0, 3, int.MaxValue, (long)int.MaxValue + 1, long.MaxValue];
    return values.Select(value => new
    {
        value,
        checkedValue = value >= int.MinValue && value <= int.MaxValue
            ? (int?)int.CreateChecked(value) : null,
        checkedError = ObserveMethodError(() => { _ = int.CreateChecked(value); }),
        saturated = int.CreateSaturating(value),
        truncated = int.CreateTruncating(value),
    }).ToArray();
}
static object ObserveInt32CreateFromBigInteger()
{
    System.Numerics.BigInteger[] values =
    [-(System.Numerics.BigInteger.One << 80),
        new System.Numerics.BigInteger(int.MinValue) - 1,
        new System.Numerics.BigInteger(int.MinValue),
        new System.Numerics.BigInteger(-3),
        System.Numerics.BigInteger.Zero,
        new System.Numerics.BigInteger(3),
        new System.Numerics.BigInteger(int.MaxValue),
        new System.Numerics.BigInteger(int.MaxValue) + 1,
        System.Numerics.BigInteger.One << 80];
    return values.Select(value => new
    {
        value = value.ToString(),
        checkedValue = value >= int.MinValue && value <= int.MaxValue
            ? (int?)int.CreateChecked(value) : null,
        checkedError = ObserveMethodError(() => { _ = int.CreateChecked(value); }),
        saturated = int.CreateSaturating(value),
        truncated = int.CreateTruncating(value),
    }).ToArray();
}
static int? ObserveInt32CreateCheckedFromDouble(double value)
{
    try { return int.CreateChecked(value); }
    catch (OverflowException) { return null; }
}
static object ObserveInt32CreateFromDouble()
{
    double[] values = [double.NegativeInfinity, -2147483649.0, -2147483648.75,
        -2147483648.0, -3.9, -0.5, 0.0, 0.5, 3.9,
        2147483647.0, 2147483647.75, 2147483648.0,
        double.PositiveInfinity, double.NaN];
    return values.Select(value => new
    {
        value = value.ToString("R", System.Globalization.CultureInfo.InvariantCulture),
        checkedValue = ObserveInt32CreateCheckedFromDouble(value),
        checkedError = ObserveMethodError(() => { _ = int.CreateChecked(value); }),
        saturated = int.CreateSaturating(value),
        truncated = int.CreateTruncating(value),
    }).ToArray();
}
static int? ObserveInt32CreateCheckedFromSingle(float value)
{
    try { return int.CreateChecked(value); }
    catch (OverflowException) { return null; }
}
static object ObserveInt32CreateFromSingle()
{
    float[] values = [float.NegativeInfinity, float.MinValue,
        -2147483904f, -2147483648f, -3.9f, -0.5f, 0f,
        0.5f, 3.9f, 2147483520f, 2147483648f,
        float.MaxValue, float.PositiveInfinity, float.NaN];
    return values.Select(value => new
    {
        value = value.ToString("R", System.Globalization.CultureInfo.InvariantCulture),
        checkedValue = ObserveInt32CreateCheckedFromSingle(value),
        checkedError = ObserveMethodError(() => { _ = int.CreateChecked(value); }),
        saturated = int.CreateSaturating(value),
        truncated = int.CreateTruncating(value),
    }).ToArray();
}
static int? ObserveInt32CreateCheckedFromDecimal(decimal value)
{
    try { return int.CreateChecked(value); }
    catch (OverflowException) { return null; }
}
static object ObserveInt32CreateFromDecimal()
{
    decimal[] values = [decimal.MinValue, -2147483649m, -2147483648.9m,
        -2147483648m, -3.9m, -0.5m, 0m, 0.5m, 3.9m,
        2147483647m, 2147483647.9m, 2147483648m, decimal.MaxValue];
    return values.Select(value => new
    {
        value = value.ToString(System.Globalization.CultureInfo.InvariantCulture),
        checkedValue = ObserveInt32CreateCheckedFromDecimal(value),
        checkedError = ObserveMethodError(() => { _ = int.CreateChecked(value); }),
        saturated = int.CreateSaturating(value),
        truncated = int.CreateTruncating(value),
    }).ToArray();
}
static object ObserveInt32OrdinaryOverloads()
{
    int.TryParse(" -7 ", System.Globalization.CultureInfo.InvariantCulture, out int parsed);
    bool invalid = int.TryParse("oops", System.Globalization.CultureInfo.InvariantCulture,
        out int invalidResult);
    bool nullValue = int.TryParse((string?)null, System.Globalization.CultureInfo.InvariantCulture,
        out int nullResult);
    return new
    {
        comparisons = new (int Left, int Right)[]
        { (5, 3), (3, 5), (3, 3), (int.MinValue, int.MaxValue),
          (int.MaxValue, int.MinValue) }
            .Select(item => new { left = item.Left, right = item.Right,
                result = item.Left.CompareTo(item.Right) }).ToArray(),
        parseHex = int.Parse("FF", System.Globalization.NumberStyles.HexNumber),
        parseProvider = int.Parse(" -7 ", System.Globalization.CultureInfo.InvariantCulture),
        parseInvalidError = ObserveMethodError(() =>
        { _ = int.Parse("oops", System.Globalization.CultureInfo.InvariantCulture); }),
        parseNullError = ObserveMethodError(() =>
        { _ = int.Parse((string)null!, System.Globalization.CultureInfo.InvariantCulture); }),
        tryParsed = parsed,
        tryInvalid = invalid,
        tryInvalidResult = invalidResult,
        tryNull = nullValue,
        tryNullResult = nullResult,
        textDefault = 42.ToString(),
        textFormat = 42.ToString("D4"),
        textNegative = (-42).ToString("D4"),
    };
}
static object ObserveInt32CreateIntegralSource<T>(T value)
    where T : System.Numerics.INumberBase<T>
{
    int? checkedValue = null;
    try { checkedValue = int.CreateChecked(value); }
    catch (OverflowException) { }
    return new
    {
        sourceType = typeof(T).FullName,
        value = value.ToString(),
        checkedValue,
        checkedError = ObserveMethodError(() => { _ = int.CreateChecked(value); }),
        saturated = int.CreateSaturating(value),
        truncated = int.CreateTruncating(value),
    };
}
static object ObserveInt32CreateSmallIntegrals()
{
    return new object[]
    {
        ObserveInt32CreateIntegralSource((byte)0),
        ObserveInt32CreateIntegralSource(byte.MaxValue),
        ObserveInt32CreateIntegralSource(sbyte.MinValue),
        ObserveInt32CreateIntegralSource(sbyte.MaxValue),
        ObserveInt32CreateIntegralSource((ushort)0),
        ObserveInt32CreateIntegralSource(ushort.MaxValue),
        ObserveInt32CreateIntegralSource((uint)0),
        ObserveInt32CreateIntegralSource((uint)int.MaxValue),
        ObserveInt32CreateIntegralSource((uint)int.MaxValue + 1),
        ObserveInt32CreateIntegralSource(uint.MaxValue),
    };
}
static object ObserveInt32SpanParse()
{
    var provider = System.Globalization.CultureInfo.InvariantCulture;
    byte[] number = System.Text.Encoding.UTF8.GetBytes(" -7 ");
    byte[] hex = System.Text.Encoding.UTF8.GetBytes("FF");
    byte[] invalid = System.Text.Encoding.UTF8.GetBytes("oops");
    bool charPlain = int.TryParse(" -7 ".AsSpan(), out int charPlainValue);
    bool charProvider = int.TryParse(" -7 ".AsSpan(), provider, out int charProviderValue);
    bool charStyled = int.TryParse("FF".AsSpan(),
        System.Globalization.NumberStyles.HexNumber, provider, out int charStyledValue);
    bool bytePlain = int.TryParse(number.AsSpan(), out int bytePlainValue);
    bool byteProvider = int.TryParse(number.AsSpan(), provider, out int byteProviderValue);
    bool byteStyled = int.TryParse(hex.AsSpan(),
        System.Globalization.NumberStyles.HexNumber, provider, out int byteStyledValue);
    bool charInvalid = int.TryParse("oops".AsSpan(), out int charInvalidValue);
    bool byteInvalid = int.TryParse(invalid.AsSpan(), out int byteInvalidValue);
    return new
    {
        charParseProvider = int.Parse(" -7 ".AsSpan(), provider),
        charParseStyled = int.Parse("FF".AsSpan(),
            System.Globalization.NumberStyles.HexNumber, provider),
        byteParseProvider = int.Parse(number.AsSpan(), provider),
        byteParseStyled = int.Parse(hex.AsSpan(),
            System.Globalization.NumberStyles.HexNumber, provider),
        charPlain, charPlainValue, charProvider, charProviderValue,
        charStyled, charStyledValue, bytePlain, bytePlainValue,
        byteProvider, byteProviderValue, byteStyled, byteStyledValue,
        charInvalid, charInvalidValue, byteInvalid, byteInvalidValue,
    };
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
    selectedDBNullBehavior = new
    {
        fullName = DBNull.Value.GetType().FullName,
        sameReference = ReferenceEquals(DBNull.Value, DBNull.Value),
        text = DBNull.Value.ToString(),
        providerText = DBNull.Value.ToString(System.Globalization.CultureInfo.InvariantCulture),
        typeCode = DBNull.Value.GetTypeCode().ToString(),
    },
    selectedDBNullConversionBehavior = new
    {
        isConvertible = DBNull.Value is IConvertible,
        toBoolean = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToBoolean(null)),
        toChar = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToChar(null)),
        toSByte = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToSByte(null)),
        toByte = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToByte(null)),
        toInt16 = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToInt16(null)),
        toUInt16 = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToUInt16(null)),
        toInt32 = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToInt32(null)),
        toUInt32 = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToUInt32(null)),
        toInt64 = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToInt64(null)),
        toUInt64 = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToUInt64(null)),
        toSingle = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToSingle(null)),
        toDouble = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToDouble(null)),
        toDecimal = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToDecimal(null)),
        toDateTime = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToDateTime(null)),
        toTypeString = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToType(typeof(string), null)),
        toTypeStringText = ((IConvertible)DBNull.Value).ToType(typeof(string), null) as string,
        toTypeSelf = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToType(typeof(DBNull), null)),
        toTypeSelfSameReference = ReferenceEquals(
            ((IConvertible)DBNull.Value).ToType(typeof(DBNull), null), DBNull.Value),
        toTypeNull = ObserveMethodError(() => ((IConvertible)DBNull.Value).ToType(null!, null)),
        toTypeNullParameter = ObserveMethodArgumentName(() =>
            ((IConvertible)DBNull.Value).ToType(null!, null)),
    },
    selectedDBNullInterfaceBehavior = new
    {
        interfaces = typeof(DBNull).GetInterfaces().Select(type => type.FullName).ToArray(),
        convertibleAssignable = typeof(IConvertible).IsAssignableFrom(typeof(DBNull)),
        convertibleInstance = typeof(IConvertible).IsInstanceOfType(DBNull.Value),
        convertibleInterface = typeof(DBNull).GetInterface("System.IConvertible")?.FullName,
    },
    selectedDBNullSerializationContractBehavior = new
    {
        interfaceName = typeof(System.Runtime.Serialization.ISerializable).FullName,
        methodName = typeof(System.Runtime.Serialization.ISerializable)
            .GetMethods().Single().Name,
        parameterTypes = typeof(System.Runtime.Serialization.ISerializable)
            .GetMethods().Single().GetParameters()
            .Select(parameter => parameter.ParameterType.FullName).ToArray(),
        infoBase = typeof(System.Runtime.Serialization.SerializationInfo).BaseType?.FullName,
        contextBase = typeof(System.Runtime.Serialization.StreamingContext).BaseType?.FullName,
        nullInfoError = ObserveMethodError(() =>
            ((System.Runtime.Serialization.ISerializable)DBNull.Value)
                .GetObjectData(null!, default)),
        nullInfoParameter = ObserveMethodArgumentName(() =>
            ((System.Runtime.Serialization.ISerializable)DBNull.Value)
                .GetObjectData(null!, default)),
    },
    selectedStreamingContextBehavior = new
    {
        values = Enum.GetNames<System.Runtime.Serialization.StreamingContextStates>()
            .Select(name => new { name, value = (int)Enum.Parse<
                System.Runtime.Serialization.StreamingContextStates>(name) }).ToArray(),
        defaultState = (int)default(System.Runtime.Serialization.StreamingContext).State,
        defaultContext = default(System.Runtime.Serialization.StreamingContext).Context,
        oneArgState = (int)new System.Runtime.Serialization.StreamingContext(
            System.Runtime.Serialization.StreamingContextStates.CrossProcess).State,
        oneArgContext = new System.Runtime.Serialization.StreamingContext(
            System.Runtime.Serialization.StreamingContextStates.CrossProcess).Context,
        twoArgState = (int)new System.Runtime.Serialization.StreamingContext(
            System.Runtime.Serialization.StreamingContextStates.Other, "marker").State,
        twoArgContext = new System.Runtime.Serialization.StreamingContext(
            System.Runtime.Serialization.StreamingContextStates.Other, "marker").Context,
    },
    selectedStreamingContextEqualityBehavior = ObserveStreamingContextEquality(),
    selectedSerializationInfoConstructionBehavior = ObserveSerializationInfoConstruction(),
    selectedFormatterConverterBehavior = ObserveFormatterConverter(),
    selectedSerializationInfoMembersBehavior = ObserveSerializationInfoMembers(),
    selectedSerializationInfoEnumerationBehavior = ObserveSerializationInfoEnumeration(),
    selectedSerializationInfoTypedValuesBehavior = ObserveSerializationInfoTypedValues(),
    selectedSerializationInfoConversionBoundariesBehavior = ObserveSerializationInfoConversionBoundaries(),
    selectedSerializationInfoTypeMetadataBehavior = ObserveSerializationInfoTypeMetadata(),
    selectedSerializationInfoNameValidationBehavior = ObserveSerializationInfoNameValidation(),
    selectedSerializationInfoSetTypeResetBehavior = ObserveSerializationInfoSetTypeReset(),
    selectedSerializationInfoEnumeratorBoundariesBehavior = ObserveSerializationInfoEnumeratorBoundaries(),
    selectedSerializationInfoEnumeratorMutationBehavior = ObserveSerializationInfoEnumeratorMutation(),
    selectedEmptySerializationInfoEnumerationBehavior = ObserveEmptySerializationInfoEnumeration(),
    selectedSerializationInfoPrimitiveMembersBehavior = ObserveSerializationInfoPrimitiveMembers(),
    selectedSerializationInfoPrimitiveConversionsBehavior = ObserveSerializationInfoPrimitiveConversions(),
    selectedPrimitiveConversionErrorsBehavior = ObservePrimitiveConversionErrors(),
    selectedSerializationInfoObjectMembersBehavior = ObserveSerializationInfoObjectMembers(),
    selectedSerializationInfoGetValueTypesBehavior = ObserveSerializationInfoGetValueTypes(),
    selectedSerializationInfoMemberNamesBehavior = ObserveSerializationInfoMemberNames(),
    selectedSerializationInfoEnumeratorResetCyclesBehavior = ObserveSerializationInfoEnumeratorResetCycles(),
    selectedSerializationInfoEnumeratorInterfaceBehavior = ObserveSerializationInfoEnumeratorInterface(),
    selectedSerializationEntryShapeBehavior = ObserveSerializationEntryShape(),
    selectedSerializationEntryValueSnapshotBehavior = ObserveSerializationEntryValueSnapshot(),
    selectedSerializationEntryEqualityBehavior = ObserveSerializationEntryEquality(),
    selectedSerializationEntryTypeEqualityBehavior = ObserveSerializationEntryTypeEquality(),
    selectedSerializationInfoDuplicateStateBehavior = ObserveSerializationInfoDuplicateState(),
    selectedSerializationInfoValueOverloadsBehavior = ObserveSerializationInfoValueOverloads(),
    selectedSerializationInfoNumericOverloadsBehavior = ObserveSerializationInfoNumericOverloads(),
    selectedSerializationInfoUnsignedMembersBehavior = ObserveSerializationInfoUnsignedMembers(),
    selectedSerializationInfoByteMembersBehavior = ObserveSerializationInfoByteMembers(),
    selectedSerializationInfoByteConversionsBehavior = ObserveSerializationInfoByteConversions(),
    selectedByteConvertibleContractBehavior = ObserveByteConvertibleContract(),
    selectedByteToTypeContractBehavior = ObserveByteToTypeContract(),
    selectedUInt16ConvertibleContractBehavior = ObserveUInt16ConvertibleContract(),
    selectedUInt32ConvertibleContractBehavior = ObserveUInt32ConvertibleContract(),
    selectedUnsignedFormatterRoutesBehavior = ObserveUnsignedFormatterRoutes(),
    selectedUnsignedToTypeContractBehavior = ObserveUnsignedToTypeContract(),
    selectedInt16SingleFormatterRoutesBehavior = ObserveInt16SingleFormatterRoutes(),
    selectedUInt64FormatterRoutesBehavior = ObserveUInt64FormatterRoutes(),
    selectedDecimalFormatterRoutesBehavior = ObserveDecimalFormatterRoutes(),
    selectedDateTimeFormatterRoutesBehavior = ObserveDateTimeFormatterRoutes(),
    selectedCharFormatterRoutesBehavior = ObserveCharFormatterRoutes(),
    selectedFormatterObjectRoutesBehavior = ObserveFormatterObjectRoutes(),
    selectedFormatterTypeCodeBoundariesBehavior = ObserveFormatterTypeCodeBoundaries(),
    selectedSerializationGetValueConversionsBehavior = ObserveSerializationGetValueConversions(),
    selectedDateTimeConvertibleContractBehavior = ObserveDateTimeConvertibleContract(),
    selectedDecimalConvertibleContractBehavior = ObserveDecimalConvertibleContract(),
    selectedUInt64CrossConversionsBehavior = ObserveUInt64CrossConversions(),
    selectedUnsignedConvertResultIdentityBehavior = ObserveUnsignedConvertResultIdentity(),
    selectedUInt64NarrowingConversionsBehavior = ObserveUInt64NarrowingConversions(),
    selectedInt64NarrowingConversionsBehavior = ObserveInt64NarrowingConversions(),
    selectedInt64WideningConversionsBehavior = ObserveInt64WideningConversions(),
    selectedFloatingFormatterConversionsBehavior = ObserveFloatingFormatterConversions(),
    selectedFloatingExceptionalBoundariesBehavior = ObserveFloatingExceptionalBoundaries(),
    selectedFloatingTextConversionsBehavior = ObserveFloatingTextConversions(),
    selectedBooleanTextConversionsBehavior = ObserveBooleanTextConversions(),
    selectedDecimalIntegerLimitsBehavior = ObserveDecimalIntegerLimits(),
    selectedFloatingTextGrammarBehavior = ObserveFloatingTextGrammar(),
    selectedDecimalGroupedTextBehavior = ObserveDecimalGroupedText(),
    selectedInt32NoneStyleBehavior = ObserveInt32NoneStyle(),
    selectedInt32BinaryStyleBehavior = ObserveInt32BinaryStyle(),
    selectedDateTimeTimeOfDayBehavior = ObserveDateTimeTimeOfDay(),
    selectedDateTimeMillisecondsBehavior = ObserveDateTimeMilliseconds(),
    selectedExceptionSerializationBehavior = ObserveExceptionSerialization(),
    selectedExceptionTargetSiteBehavior = ObserveExceptionTargetSite(),
    selectedExceptionDataDictionaryBehavior = ObserveExceptionDataDictionary(),
    selectedExceptionDataBoundaries = ObserveExceptionDataBoundaries(),
    selectedExceptionDataEnumeratorMutation = ObserveExceptionDataEnumeratorMutation(),
    selectedExceptionDataViewEnumeration = ObserveExceptionDataViewEnumeration(),
    selectedExceptionDataViewProperties = ObserveExceptionDataViewProperties(),
    selectedExceptionDataCopyToBoundaries = ObserveExceptionDataCopyToBoundaries(),
    selectedArgumentOutOfRangeConstructors = ObserveArgumentOutOfRangeConstructors(),
    selectedInt32BitHelpers = ObserveInt32BitHelpers(),
    selectedInt32SignedArithmetic = ObserveInt32SignedArithmetic(),
    selectedInt32ValueIdentityAndBigMul = ObserveInt32ValueIdentityAndBigMul(),
    selectedInt32DivRem = ObserveInt32DivRem(),
    selectedInt32CreateFromInt64 = ObserveInt32CreateFromInt64(),
    selectedInt32CreateFromBigInteger = ObserveInt32CreateFromBigInteger(),
    selectedInt32CreateFromDouble = ObserveInt32CreateFromDouble(),
    selectedInt32CreateFromSingle = ObserveInt32CreateFromSingle(),
    selectedInt32CreateFromDecimal = ObserveInt32CreateFromDecimal(),
    selectedInt32OrdinaryOverloads = ObserveInt32OrdinaryOverloads(),
    selectedInt32CreateSmallIntegrals = ObserveInt32CreateSmallIntegrals(),
    selectedInt32SpanParse = ObserveInt32SpanParse(),
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
    selectedTypeDefinitionBehavior = new[]
    {
        typeof(string), typeof(int), typeof(IDisposable),
        typeof(GenericParameterAttributes), typeof(System.Collections.Generic.List<>),
        typeof(System.Collections.Generic.List<string>),
        typeof(System.Collections.Generic.List<>).GetGenericArguments()[0],
        typeof(string[]), typeof(string[,]), typeof(string).MakeByRefType(),
        typeof(string).MakePointerType(), typeof(System.Collections.Generic.List<>).MakeArrayType(),
    }.Select(type => new { name = type.FullName ?? type.Name, result = type.IsTypeDefinition }).ToArray(),
    selectedByRefLikeBehavior = new[]
    {
        typeof(string), typeof(int), typeof(string[]), typeof(string).MakeByRefType(),
        typeof(System.Collections.Generic.List<string>),
        typeof(System.Collections.Generic.List<>).GetGenericArguments()[0],
        typeof(Span<int>), typeof(ReadOnlySpan<char>),
    }.Select(type => new { name = type.FullName ?? type.Name, result = type.IsByRefLike }).ToArray(),
    selectedDefaultMemberBehavior = new[]
    {
        typeof(object), typeof(IDisposable), typeof(TypeCode),
        typeof(string), typeof(List<>), typeof(List<string>),
    }.Select(type => new { name = type.FullName,
        members = type.GetDefaultMembers().Select(member => new
        {
            name = member.Name, kind = member.MemberType.ToString(),
            declaring = member.DeclaringType?.FullName,
            reflected = member.ReflectedType?.FullName,
        }).ToArray() }).ToArray(),
    selectedInterfaceMemberEnumeration = new[]
    {
        typeof(IDisposable), typeof(IComparable), typeof(IFormattable),
        typeof(IFormatProvider),
    }.Select(type => new { owner = type.FullName,
        members = type.GetMembers().Select(member => new
        {
            name = member.Name, kind = member.MemberType.ToString(),
            declaring = member.DeclaringType?.FullName,
            reflected = member.ReflectedType?.FullName,
        }).ToArray() }).ToArray(),
    selectedInterfaceMemberMissBehavior = new[]
    {
        (typeof(IDisposable), "dispose"), (typeof(IDisposable), "Missing"),
        (typeof(IComparable), "compareto"),
        (typeof(IFormattable), "tostring"),
        (typeof(IFormatProvider), "getformat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        query = ObserveMemberName(item.Item1, item.Item2) }).ToArray(),
    selectedMemberNameBehavior = new
    {
        stringChars = ObserveMemberName(typeof(string), "Chars"),
        stringLower = ObserveMemberName(typeof(string), "chars"),
        stringMissing = ObserveMemberName(typeof(string), "Missing"),
        listItem = ObserveMemberName(typeof(List<>), "Item"),
        disposableDispose = ObserveMemberName(typeof(IDisposable), "Dispose"),
        objectMissing = ObserveMemberName(typeof(object), "Missing"),
        nullName = ObserveMemberName(typeof(string), null),
    },
    selectedMemberFlagsBehavior = new
    {
        stringChars = ObserveMemberFlags(typeof(string), "Chars", BindingFlags.Public | BindingFlags.Instance),
        publicOnly = ObserveMemberFlags(typeof(string), "Chars", BindingFlags.Public),
        instanceOnly = ObserveMemberFlags(typeof(string), "Chars", BindingFlags.Instance),
        nonPublic = ObserveMemberFlags(typeof(string), "Chars", BindingFlags.NonPublic | BindingFlags.Instance),
        ignoreCase = ObserveMemberFlags(typeof(string), "chars", BindingFlags.Public | BindingFlags.Instance | BindingFlags.IgnoreCase),
        disposableDispose = ObserveMemberFlags(typeof(IDisposable), "Dispose", BindingFlags.Public | BindingFlags.Instance),
        nullName = ObserveMemberFlags(typeof(string), null, BindingFlags.Public | BindingFlags.Instance),
    },
    selectedMemberKindsBehavior = new
    {
        property = ObserveMemberKinds(typeof(string), "Chars", MemberTypes.Property,
            BindingFlags.Public | BindingFlags.Instance),
        methodMiss = ObserveMemberKinds(typeof(string), "Chars", MemberTypes.Method,
            BindingFlags.Public | BindingFlags.Instance),
        all = ObserveMemberKinds(typeof(string), "Chars", MemberTypes.All,
            BindingFlags.Public | BindingFlags.Instance),
        disposeMethod = ObserveMemberKinds(typeof(IDisposable), "Dispose", MemberTypes.Method,
            BindingFlags.Public | BindingFlags.Instance),
        disposePropertyMiss = ObserveMemberKinds(typeof(IDisposable), "Dispose", MemberTypes.Property,
            BindingFlags.Public | BindingFlags.Instance),
        nullName = ObserveMemberKinds(typeof(string), null, MemberTypes.Property,
            BindingFlags.Public | BindingFlags.Instance),
    },
    selectedMembersFlagsBehavior = new[]
    {
        typeof(IDisposable), typeof(IComparable), typeof(IFormattable), typeof(IFormatProvider),
    }.Select(type => new { owner = type.FullName,
        publicInstance = ObserveMembersFlags(type, BindingFlags.Public | BindingFlags.Instance),
        publicOnly = ObserveMembersFlags(type, BindingFlags.Public),
        nonPublicInstance = ObserveMembersFlags(type, BindingFlags.NonPublic | BindingFlags.Instance),
    }).ToArray(),
    selectedMethodInfoBehavior = new
    {
        methodBase = new { name = typeof(MethodBase).FullName,
            parent = typeof(MethodBase).BaseType?.FullName, isAbstract = typeof(MethodBase).IsAbstract },
        methodInfo = new { name = typeof(MethodInfo).FullName,
            parent = typeof(MethodInfo).BaseType?.FullName, isAbstract = typeof(MethodInfo).IsAbstract },
        disposableMethods = typeof(IDisposable).GetMethods(BindingFlags.Public | BindingFlags.Instance)
            .Select(method => new { name = method.Name, kind = method.MemberType.ToString() }).ToArray(),
        publicOnly = typeof(IDisposable).GetMethods(BindingFlags.Public)
            .Select(method => method.Name).ToArray(),
        nonPublicInstance = typeof(IDisposable).GetMethods(BindingFlags.NonPublic | BindingFlags.Instance)
            .Select(method => method.Name).ToArray(),
    },
    selectedMethodReturnBehavior = new
    {
        voidType = new { name = typeof(void).Name, fullName = typeof(void).FullName,
            baseType = typeof(void).BaseType?.FullName, isValueType = typeof(void).IsValueType,
            isPrimitive = typeof(void).IsPrimitive },
        methods = new[]
        {
            (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
            (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
        }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
            returnType = item.Item1.GetMethod(item.Item2)!.ReturnType.FullName }).ToArray(),
    },
    selectedParameterInfoBehavior = new
    {
        type = new { name = typeof(ParameterInfo).FullName,
            parent = typeof(ParameterInfo).BaseType?.FullName,
            isAbstract = typeof(ParameterInfo).IsAbstract },
        methods = new[]
        {
            (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
            (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
        }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
            parameters = item.Item1.GetMethod(item.Item2)!.GetParameters()
                .Select(parameter => new { name = parameter.Name,
                    type = parameter.ParameterType.FullName, position = parameter.Position })
                .ToArray() }).ToArray(),
    },
    selectedReturnParameterBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        parameter = new { name = item.Item1.GetMethod(item.Item2)!.ReturnParameter.Name,
            type = item.Item1.GetMethod(item.Item2)!.ReturnParameter.ParameterType.FullName,
            position = item.Item1.GetMethod(item.Item2)!.ReturnParameter.Position } }).ToArray(),
    selectedParameterMemberBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item =>
    {
        MethodInfo method = item.Item1.GetMethod(item.Item2)!;
        return new { owner = item.Item1.FullName, name = item.Item2,
            parameterMembers = method.GetParameters()
                .Select(parameter => new { name = parameter.Member.Name,
                    sameReference = ReferenceEquals(parameter.Member, method) }).ToArray(),
            returnMember = method.ReturnParameter.Member.Name,
            returnSameReference = ReferenceEquals(method.ReturnParameter.Member, method) };
    }).ToArray(),
    selectedParameterFlagBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        parameters = item.Item1.GetMethod(item.Item2)!.GetParameters()
            .Append(item.Item1.GetMethod(item.Item2)!.ReturnParameter)
            .Select(parameter => new { position = parameter.Position,
                isOptional = parameter.IsOptional, hasDefaultValue = parameter.HasDefaultValue,
                isIn = parameter.IsIn, isOut = parameter.IsOut,
                isRetval = parameter.IsRetval, isLcid = parameter.IsLcid })
            .ToArray() }).ToArray(),
    selectedParameterAttributeBehavior = new
    {
        values = Enum.GetNames<ParameterAttributes>()
            .Select(name => new { name, value = (int)Enum.Parse<ParameterAttributes>(name) })
            .ToArray(),
        methods = new[]
        {
            (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
            (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
        }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
            attributes = item.Item1.GetMethod(item.Item2)!.GetParameters()
                .Append(item.Item1.GetMethod(item.Item2)!.ReturnParameter)
                .Select(parameter => new { position = parameter.Position,
                    value = (int)parameter.Attributes, text = parameter.Attributes.ToString() })
                .ToArray() }).ToArray(),
    },
    selectedParameterDefaultValueBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        parameters = item.Item1.GetMethod(item.Item2)!.GetParameters()
            .Append(item.Item1.GetMethod(item.Item2)!.ReturnParameter)
            .Select(parameter => new { position = parameter.Position,
                defaultType = parameter.DefaultValue?.GetType().FullName,
                rawDefaultType = parameter.RawDefaultValue?.GetType().FullName,
                sameReference = ReferenceEquals(parameter.DefaultValue, parameter.RawDefaultValue) })
            .ToArray() }).ToArray(),
    selectedParameterModifierBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        parameters = item.Item1.GetMethod(item.Item2)!.GetParameters()
            .Append(item.Item1.GetMethod(item.Item2)!.ReturnParameter)
            .Select(parameter => new { position = parameter.Position,
                optional = parameter.GetOptionalCustomModifiers()
                    .Select(type => type.FullName).ToArray(),
                required = parameter.GetRequiredCustomModifiers()
                    .Select(type => type.FullName).ToArray() })
            .ToArray() }).ToArray(),
    selectedParameterCustomAttributeBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        parameters = item.Item1.GetMethod(item.Item2)!.GetParameters()
            .Append(item.Item1.GetMethod(item.Item2)!.ReturnParameter)
            .Select(parameter => new { position = parameter.Position,
                direct = parameter.GetCustomAttributes(false)
                    .Select(value => new { type = value.GetType().FullName,
                        baseType = value.GetType().BaseType?.FullName,
                        flags = value.GetType().GetField("NullableFlags")?.GetValue(value) as byte[] })
                    .ToArray(),
                inherited = parameter.GetCustomAttributes(true)
                    .Select(value => value.GetType().FullName).ToArray() })
            .ToArray() }).ToArray(),
    selectedAttributeInstanceBehavior = ObserveSelectedAttributeInstance(),
    selectedNullableAttributeConstructorBehavior = ObserveNullableAttributeConstructor(),
    selectedParameterAttributeFilterBehavior = new
    {
        returnBase = typeof(IFormattable).GetMethod("ToString")!.ReturnParameter
            .GetCustomAttributes(typeof(Attribute), false)
            .Select(value => value.GetType().FullName).ToArray(),
        returnExact = typeof(IFormattable).GetMethod("ToString")!.ReturnParameter
            .GetCustomAttributes(typeof(IFormattable).GetMethod("ToString")!.ReturnParameter
                .GetCustomAttributes(false)[0].GetType(), true)
            .Select(value => value.GetType().FullName).ToArray(),
        inputBase = typeof(IFormattable).GetMethod("ToString")!.GetParameters()[0]
            .GetCustomAttributes(typeof(Attribute), false)
            .Select(value => value.GetType().FullName).ToArray(),
        nullError = ObserveMethodError(() => typeof(IFormattable).GetMethod("ToString")!
            .ReturnParameter.GetCustomAttributes((Type)null!, false)),
        nullParameter = ObserveMethodArgumentName(() => typeof(IFormattable).GetMethod("ToString")!
            .ReturnParameter.GetCustomAttributes((Type)null!, false)),
    },
    selectedParameterIsDefinedBehavior = new
    {
        returnBase = typeof(IFormattable).GetMethod("ToString")!.ReturnParameter
            .IsDefined(typeof(Attribute), false),
        returnExact = typeof(IFormattable).GetMethod("ToString")!.ReturnParameter
            .IsDefined(typeof(IFormattable).GetMethod("ToString")!.ReturnParameter
                .GetCustomAttributes(false)[0].GetType(), true),
        inputBase = typeof(IFormattable).GetMethod("ToString")!.GetParameters()[0]
            .IsDefined(typeof(Attribute), false),
        nullError = ObserveMethodError(() => typeof(IFormattable).GetMethod("ToString")!
            .ReturnParameter.IsDefined((Type)null!, false)),
        nullParameter = ObserveMethodArgumentName(() => typeof(IFormattable).GetMethod("ToString")!
            .ReturnParameter.IsDefined((Type)null!, false)),
    },
    selectedParameterTextBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        parameters = item.Item1.GetMethod(item.Item2)!.GetParameters()
            .Append(item.Item1.GetMethod(item.Item2)!.ReturnParameter)
            .Select(parameter => new { position = parameter.Position,
                text = parameter.ToString() }).ToArray() }).ToArray(),
    selectedMethodFlagBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        isPublic = item.Item1.GetMethod(item.Item2)!.IsPublic,
        isStatic = item.Item1.GetMethod(item.Item2)!.IsStatic,
        isAbstract = item.Item1.GetMethod(item.Item2)!.IsAbstract,
        isVirtual = item.Item1.GetMethod(item.Item2)!.IsVirtual,
        isFinal = item.Item1.GetMethod(item.Item2)!.IsFinal }).ToArray(),
    selectedGenericMethodBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        isGenericMethod = item.Item1.GetMethod(item.Item2)!.IsGenericMethod,
        isGenericMethodDefinition = item.Item1.GetMethod(item.Item2)!.IsGenericMethodDefinition,
        isConstructedGenericMethod = item.Item1.GetMethod(item.Item2)!.IsConstructedGenericMethod,
        containsGenericParameters = item.Item1.GetMethod(item.Item2)!.ContainsGenericParameters,
        genericArguments = item.Item1.GetMethod(item.Item2)!.GetGenericArguments()
            .Select(type => type.FullName).ToArray() }).ToArray(),
    selectedMethodClassificationBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        isSpecialName = item.Item1.GetMethod(item.Item2)!.IsSpecialName,
        isConstructor = item.Item1.GetMethod(item.Item2)!.IsConstructor,
        isPrivate = item.Item1.GetMethod(item.Item2)!.IsPrivate,
        isFamily = item.Item1.GetMethod(item.Item2)!.IsFamily,
        isFamilyAndAssembly = item.Item1.GetMethod(item.Item2)!.IsFamilyAndAssembly,
        isFamilyOrAssembly = item.Item1.GetMethod(item.Item2)!.IsFamilyOrAssembly,
        isAssembly = item.Item1.GetMethod(item.Item2)!.IsAssembly,
        isHideBySig = item.Item1.GetMethod(item.Item2)!.IsHideBySig }).ToArray(),
    selectedCallingConventionBehavior = new
    {
        values = Enum.GetNames<CallingConventions>()
            .Select(name => new { name, value = (int)Enum.Parse<CallingConventions>(name) })
            .ToArray(),
        methods = new[]
        {
            (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
            (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
        }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
            value = (int)item.Item1.GetMethod(item.Item2)!.CallingConvention,
            standard = item.Item1.GetMethod(item.Item2)!.CallingConvention.HasFlag(CallingConventions.Standard),
            hasThis = item.Item1.GetMethod(item.Item2)!.CallingConvention.HasFlag(CallingConventions.HasThis) })
            .ToArray(),
    },
    selectedMethodBaseDefinitionBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        baseName = item.Item1.GetMethod(item.Item2)!.GetBaseDefinition().Name,
        baseOwner = item.Item1.GetMethod(item.Item2)!.GetBaseDefinition().DeclaringType?.FullName,
        sameReference = ReferenceEquals(item.Item1.GetMethod(item.Item2),
            item.Item1.GetMethod(item.Item2)!.GetBaseDefinition()) }).ToArray(),
    selectedMethodSecurityBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        isSecurityCritical = item.Item1.GetMethod(item.Item2)!.IsSecurityCritical,
        isSecuritySafeCritical = item.Item1.GetMethod(item.Item2)!.IsSecuritySafeCritical,
        isSecurityTransparent = item.Item1.GetMethod(item.Item2)!.IsSecurityTransparent })
        .ToArray(),
    selectedMethodImplementationBehavior = new
    {
        values = Enum.GetNames<MethodImplAttributes>()
            .Select(name => new { name, value = (int)Enum.Parse<MethodImplAttributes>(name) })
            .ToArray(),
        methods = new[]
        {
            (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
            (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
        }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
            value = (int)item.Item1.GetMethod(item.Item2)!.GetMethodImplementationFlags(),
            text = item.Item1.GetMethod(item.Item2)!.GetMethodImplementationFlags().ToString() })
            .ToArray(),
    },
    selectedMethodSignatureTextBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        text = item.Item1.GetMethod(item.Item2)!.ToString() }).ToArray(),
    selectedMethodCustomAttributeBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        direct = item.Item1.GetMethod(item.Item2)!.GetCustomAttributes(false)
            .Select(value => value.GetType().FullName).ToArray(),
        inherited = item.Item1.GetMethod(item.Item2)!.GetCustomAttributes(true)
            .Select(value => value.GetType().FullName).ToArray() }).ToArray(),
    selectedMethodAttributeFilterBehavior = new
    {
        direct = typeof(IDisposable).GetMethod("Dispose")!
            .GetCustomAttributes(typeof(Attribute), false)
            .Select(value => value.GetType().FullName).ToArray(),
        inherited = typeof(IFormattable).GetMethod("ToString")!
            .GetCustomAttributes(typeof(Attribute), true)
            .Select(value => value.GetType().FullName).ToArray(),
        nullError = ObserveMethodError(() => typeof(IDisposable).GetMethod("Dispose")!
            .GetCustomAttributes((Type)null!, false)),
        nullParameter = ObserveMethodArgumentName(() => typeof(IDisposable).GetMethod("Dispose")!
            .GetCustomAttributes((Type)null!, false)),
    },
    selectedMethodIsDefinedBehavior = new
    {
        direct = typeof(IDisposable).GetMethod("Dispose")!.IsDefined(typeof(Attribute), false),
        inherited = typeof(IFormattable).GetMethod("ToString")!.IsDefined(typeof(Attribute), true),
        nullError = ObserveMethodError(() => typeof(IDisposable).GetMethod("Dispose")!
            .IsDefined((Type)null!, false)),
        nullParameter = ObserveMethodArgumentName(() => typeof(IDisposable).GetMethod("Dispose")!
            .IsDefined((Type)null!, false)),
    },
    selectedNongenericMethodErrorBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        definitionError = ObserveMethodError(() => item.Item1.GetMethod(item.Item2)!
            .GetGenericMethodDefinition()),
        instantiationError = ObserveMethodError(() => item.Item1.GetMethod(item.Item2)!
            .MakeGenericMethod(Type.EmptyTypes)),
        nullInstantiationError = ObserveMethodError(() => item.Item1.GetMethod(item.Item2)!
            .MakeGenericMethod((Type[]?)null!)),
        nullInstantiationParameter = ObserveMethodArgumentName(() => item.Item1.GetMethod(item.Item2)!
            .MakeGenericMethod((Type[]?)null!)),
        nonemptyInstantiationError = ObserveMethodError(() => item.Item1.GetMethod(item.Item2)!
            .MakeGenericMethod(typeof(string))) }).ToArray(),
    selectedAbstractMethodBodyBehavior = new
    {
        type = new { name = typeof(MethodBody).FullName,
            parent = typeof(MethodBody).BaseType?.FullName,
            isAbstract = typeof(MethodBody).IsAbstract },
        methods = new[]
        {
            (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
            (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
        }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
            hasBody = item.Item1.GetMethod(item.Item2)!.GetMethodBody() is not null }).ToArray(),
    },
    selectedMethodNameBehavior = new[]
    {
        (typeof(IDisposable), "Dispose"), (typeof(IComparable), "CompareTo"),
        (typeof(IFormattable), "ToString"), (typeof(IFormatProvider), "GetFormat"),
        (typeof(IDisposable), "dispose"), (typeof(IDisposable), "Missing"),
        (typeof(IDisposable), (string?)null),
    }.Select(item => new { owner = item.Item1.FullName, name = item.Item2,
        query = ObserveMethodName(item.Item1, item.Item2) }).ToArray(),
    selectedMethodFlagsBehavior = new
    {
        positive = ObserveMethodFlags(typeof(IDisposable), "Dispose", BindingFlags.Public | BindingFlags.Instance),
        publicOnly = ObserveMethodFlags(typeof(IDisposable), "Dispose", BindingFlags.Public),
        nonPublic = ObserveMethodFlags(typeof(IDisposable), "Dispose", BindingFlags.NonPublic | BindingFlags.Instance),
        ignoreCase = ObserveMethodFlags(typeof(IDisposable), "dispose",
            BindingFlags.Public | BindingFlags.Instance | BindingFlags.IgnoreCase),
        missing = ObserveMethodFlags(typeof(IDisposable), "Missing", BindingFlags.Public | BindingFlags.Instance),
        nullName = ObserveMethodFlags(typeof(IDisposable), null, BindingFlags.Public | BindingFlags.Instance),
    },
    selectedMethodEnumerationBehavior = new[]
    {
        typeof(IDisposable), typeof(IComparable), typeof(IFormattable), typeof(IFormatProvider),
    }.Select(type => new { owner = type.FullName,
        methods = type.GetMethods().Select(method => new
        {
            name = method.Name, kind = method.MemberType.ToString(),
            declaring = method.DeclaringType?.FullName,
        }).ToArray() }).ToArray(),
    selectedMethodParameterBehavior = new
    {
        dispose = ObserveMethodParameters(typeof(IDisposable), "Dispose", Type.EmptyTypes),
        compareTo = ObserveMethodParameters(typeof(IComparable), "CompareTo", new[] {typeof(object)}),
        toString = ObserveMethodParameters(typeof(IFormattable), "ToString",
            new[] {typeof(string), typeof(IFormatProvider)}),
        getFormat = ObserveMethodParameters(typeof(IFormatProvider), "GetFormat", new[] {typeof(Type)}),
        wrongTypes = ObserveMethodParameters(typeof(IDisposable), "Dispose", new[] {typeof(object)}),
        nullName = ObserveMethodParameters(typeof(IDisposable), null, Type.EmptyTypes),
        nullArray = ObserveMethodParameters(typeof(IDisposable), "Dispose", null),
        nullElement = ObserveMethodParameters(typeof(IDisposable), "Dispose", new Type[] {null!}),
    },
    selectedMethodFlagsParameterBehavior = new
    {
        dispose = ObserveMethodFlagsParameters(typeof(IDisposable), "Dispose",
            BindingFlags.Public | BindingFlags.Instance, Type.EmptyTypes),
        publicOnly = ObserveMethodFlagsParameters(typeof(IDisposable), "Dispose",
            BindingFlags.Public, Type.EmptyTypes),
        ignoreCase = ObserveMethodFlagsParameters(typeof(IDisposable), "dispose",
            BindingFlags.Public | BindingFlags.Instance | BindingFlags.IgnoreCase, Type.EmptyTypes),
        wrongTypes = ObserveMethodFlagsParameters(typeof(IDisposable), "Dispose",
            BindingFlags.Public | BindingFlags.Instance, new[] {typeof(object)}),
        nullName = ObserveMethodFlagsParameters(typeof(IDisposable), null,
            BindingFlags.Public | BindingFlags.Instance, Type.EmptyTypes),
        nullArray = ObserveMethodFlagsParameters(typeof(IDisposable), "Dispose",
            BindingFlags.Public | BindingFlags.Instance, null),
    },
    selectedNestedTypeFlagsBehavior = new
    {
        publicChild = ObserveNestedTypeFlags(typeof(ReflectionFixture), "PublicChild", BindingFlags.Public),
        publicChildNonPublic = ObserveNestedTypeFlags(typeof(ReflectionFixture), "PublicChild", BindingFlags.NonPublic),
        privateChild = ObserveNestedTypeFlags(typeof(ReflectionFixture), "PrivateChild", BindingFlags.NonPublic),
        privateChildPublic = ObserveNestedTypeFlags(typeof(ReflectionFixture), "PrivateChild", BindingFlags.Public),
        ignoreCase = ObserveNestedTypeFlags(typeof(ReflectionFixture), "publicchild", BindingFlags.Public | BindingFlags.IgnoreCase),
        nullName = ObserveNestedTypeFlags(typeof(ReflectionFixture), null, BindingFlags.Public),
    },
    selectedNestedTypesFlagsBehavior = new
    {
        publicTypes = typeof(ReflectionFixture).GetNestedTypes(BindingFlags.Public)
            .Select(type => type.Name).ToArray(),
        nonPublicTypes = typeof(ReflectionFixture).GetNestedTypes(BindingFlags.NonPublic)
            .Select(type => type.Name).ToArray(),
        both = typeof(ReflectionFixture).GetNestedTypes(BindingFlags.Public | BindingFlags.NonPublic)
            .Select(type => type.Name).OrderBy(name => name).ToArray(),
        none = typeof(ReflectionFixture).GetNestedTypes(BindingFlags.Default)
            .Select(type => type.Name).ToArray(),
    },
    selectedCustomModifierBehavior = new[]
    {
        typeof(string), typeof(int), typeof(List<>),
        typeof(List<>).GetGenericArguments()[0], typeof(string[]),
        typeof(string).MakeByRefType(), typeof(string).MakePointerType(),
    }.Select(type => new { name = type.FullName ?? type.Name,
        optional = type.GetOptionalCustomModifiers().Select(modifier => modifier.FullName).ToArray(),
        required = type.GetRequiredCustomModifiers().Select(modifier => modifier.FullName).ToArray() }).ToArray(),
    selectedSecurityTransparencyBehavior = new[]
    {
        typeof(string), typeof(int), typeof(TypeCode), typeof(IDisposable),
        typeof(Type), typeof(Exception), typeof(List<>),
        typeof(List<>).GetGenericArguments()[0], typeof(string[]),
        typeof(string).MakeByRefType(),
    }.Select(type => new { name = type.FullName ?? type.Name,
        isSecurityCritical = type.IsSecurityCritical,
        isSecuritySafeCritical = type.IsSecuritySafeCritical,
        isSecurityTransparent = type.IsSecurityTransparent }).ToArray(),
    selectedFunctionPointerFlagBehavior = new[]
    {
        typeof(string), typeof(int), typeof(TypeCode), typeof(IDisposable),
        typeof(List<>), typeof(List<>).GetGenericArguments()[0],
        typeof(string[]), typeof(string).MakePointerType(),
    }.Select(type => new { name = type.FullName ?? type.Name,
        isFunctionPointer = type.IsFunctionPointer,
        isUnmanagedFunctionPointer = type.IsUnmanagedFunctionPointer }).ToArray(),
    selectedNonFunctionPointerQueryBehavior = new[]
    {
        typeof(string), typeof(string).MakePointerType(),
    }.Select(type => new { name = type.FullName,
        returnTypeError = ObserveFunctionPointerQuery(type.GetFunctionPointerReturnType),
        parameterTypesError = ObserveFunctionPointerQuery(type.GetFunctionPointerParameterTypes),
        callingConventionsError = ObserveFunctionPointerQuery(type.GetFunctionPointerCallingConventions),
    }).ToArray(),
    selectedInteropTypeFlagBehavior = new[]
    {
        typeof(string), typeof(int), typeof(Type), typeof(Exception),
        typeof(IDisposable), typeof(List<>),
        typeof(List<>).GetGenericArguments()[0], typeof(string[]),
        typeof(string).MakeByRefType(),
    }.Select(type => new { name = type.FullName ?? type.Name,
        isImport = type.IsImport, isCOMObject = type.IsCOMObject,
        isContextful = type.IsContextful, isMarshalByRef = type.IsMarshalByRef,
        isSignatureType = type.IsSignatureType }).ToArray(),
    selectedLayoutBehavior = new[]
    {
        typeof(string), typeof(int), typeof(TypeCode), typeof(IDisposable),
        typeof(List<>), typeof(List<string>),
        typeof(List<>).GetGenericArguments()[0], typeof(string[]),
        typeof(string).MakeByRefType(),
        typeof(System.Collections.Generic.Dictionary<string, int>.KeyCollection),
    }.Select(type => new { name = type.FullName ?? type.Name,
        isAutoLayout = type.IsAutoLayout,
        isLayoutSequential = type.IsLayoutSequential,
        isExplicitLayout = type.IsExplicitLayout }).ToArray(),
    selectedCharacterSetBehavior = new[]
    {
        typeof(string), typeof(int), typeof(TypeCode), typeof(IDisposable),
        typeof(List<>), typeof(List<string>),
        typeof(List<>).GetGenericArguments()[0], typeof(string[]),
        typeof(string).MakeByRefType(),
        typeof(System.Collections.Generic.Dictionary<string, int>.KeyCollection),
    }.Select(type => new { name = type.FullName ?? type.Name,
        isAnsiClass = type.IsAnsiClass, isUnicodeClass = type.IsUnicodeClass,
        isAutoClass = type.IsAutoClass }).ToArray(),
    selectedSpecialNameBehavior = new[]
    {
        typeof(string), typeof(TypeCode), typeof(List<>),
        typeof(List<>).GetGenericArguments()[0], typeof(string[]),
        typeof(string).MakeByRefType(),
        typeof(System.Collections.Generic.Dictionary<string, int>.KeyCollection),
    }.Select(type => new { name = type.FullName ?? type.Name,
        isSpecialName = type.IsSpecialName }).ToArray(),
    selectedSerializableBehavior = new[]
    {
        typeof(string), typeof(int), typeof(TypeCode), typeof(IDisposable),
        typeof(Type), typeof(Exception), typeof(List<>), typeof(List<string>),
        typeof(List<>).GetGenericArguments()[0], typeof(string[]),
        typeof(IDisposable[]), typeof(string).MakeByRefType(),
    }.Select(type => new { name = type.FullName ?? type.Name,
        isSerializable = type.IsSerializable }).ToArray(),
    selectedNotPublicBehavior = new[]
    {
        typeof(string), typeof(NestedFamilyProbe),
        NestedFamilyProbe.PrivateMarkerType,
        typeof(string[]), typeof(System.Collections.Generic.List<>).GetGenericArguments()[0],
    }.Select(type => new { name = type.FullName ?? type.Name,
        isPublic = type.IsPublic, isNotPublic = type.IsNotPublic,
        isNested = type.IsNested }).ToArray(),
    selectedNestedTypeFlagBehavior = new[]
    {
        typeof(string), typeof(System.Collections.Generic.List<>),
        typeof(System.Collections.Generic.List<>).GetGenericArguments()[0],
        typeof(System.Collections.Generic.Dictionary<string, int>.KeyCollection),
        typeof(System.Collections.Generic.List<int>.Enumerator),
    }.Select(type => new
    {
        name = type.FullName ?? type.Name,
        isNested = type.IsNested,
        isNestedPublic = type.IsNestedPublic,
    }).ToArray(),
    selectedNestedAssemblyBehavior = new[]
    {
        typeof(string), typeof(System.Collections.Generic.List<>).GetGenericArguments()[0],
        typeof(System.Collections.Generic.List<int>.Enumerator),
        typeof(string).Assembly.GetType("Interop+OleAut32", throwOnError: true)!,
    }.Select(type => new { name = type.FullName ?? type.Name, result = type.IsNestedAssembly }).ToArray(),
    selectedNestedPrivateBehavior = new[]
    {
        typeof(string), typeof(System.Collections.Generic.List<>).GetGenericArguments()[0],
        typeof(System.Collections.Generic.List<int>.Enumerator),
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!,
    }.Select(type => new { name = type.FullName ?? type.Name, result = type.IsNestedPrivate }).ToArray(),
    selectedNestedFamilyBehavior = new[]
    {
        typeof(string), typeof(System.Collections.Generic.List<>).GetGenericArguments()[0],
        typeof(System.Collections.Generic.List<int>.Enumerator),
        NestedFamilyProbe.MarkerType,
    }.Select(type => new { name = type.FullName ?? type.Name, result = type.IsNestedFamily }).ToArray(),
    selectedNestedTypeToStringBehavior = new[]
    {
        typeof(System.Collections.Generic.List<string>[]),
        typeof(System.Collections.Generic.List<string>[,]),
        typeof(System.Collections.Generic.List<System.Collections.Generic.List<string>>),
        typeof(System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<int>>),
        typeof(System.Collections.Generic.List<>).MakeArrayType(),
        typeof(System.Collections.Generic.List<>).GetGenericArguments()[0].MakeArrayType(),
    }.Select(type => new { fullName = type.FullName, text = type.ToString() }).ToArray(),
    selectedPrimitiveArrayToStringBehavior = new[]
    {
        typeof(bool), typeof(char), typeof(byte), typeof(short),
        typeof(long), typeof(float), typeof(double),
    }.Select(type => new
    {
        name = type.FullName,
        vector = type.MakeArrayType().ToString(),
        variableBound = type.MakeArrayType(1).ToString(),
        rankTwo = type.MakeArrayType(2).ToString(),
        rankThree = type.MakeArrayType(3).ToString(),
    }).ToArray(),
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
    completeDeclaredSurface = selected
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
    selectedMemberTypeCombinationBehavior = new
    {
        value = (int)(MemberTypes.Method | MemberTypes.Property),
        hasMethod = (MemberTypes.Method | MemberTypes.Property).HasFlag(MemberTypes.Method),
        hasProperty = (MemberTypes.Method | MemberTypes.Property).HasFlag(MemberTypes.Property),
        named = typeof(MemberTypes).IsEnumDefined(MemberTypes.Method | MemberTypes.Property),
        enumName = typeof(MemberTypes).GetEnumName(MemberTypes.Method | MemberTypes.Property),
    },
    selectedBindingFlagsValues = Enum.GetNames<BindingFlags>()
        .Select(name => new { name, value = (int)Enum.Parse<BindingFlags>(name) })
        .ToArray(),
    selectedBindingCombinationBehavior = new
    {
        value = (int)(BindingFlags.Public | BindingFlags.Instance),
        hasPublic = (BindingFlags.Public | BindingFlags.Instance).HasFlag(BindingFlags.Public),
        hasInstance = (BindingFlags.Public | BindingFlags.Instance).HasFlag(BindingFlags.Instance),
        named = typeof(BindingFlags).IsEnumDefined(BindingFlags.Public | BindingFlags.Instance),
        enumName = typeof(BindingFlags).GetEnumName(BindingFlags.Public | BindingFlags.Instance),
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
    selectedMemberCollectibilityBehavior = new
    {
        stringType = typeof(string).IsCollectible,
        genericListType = typeof(List<string>).IsCollectible,
        disposableMethod = typeof(IDisposable).GetMethod("Dispose")!.IsCollectible,
        stringCharsProperty = typeof(string).GetProperty("Chars")!.IsCollectible,
    },
    selectedMemberMetadataDefinitionBehavior = new
    {
        sameMethod = typeof(IDisposable).GetMethod("Dispose")!
            .HasSameMetadataDefinitionAs(typeof(IDisposable).GetMethod("Dispose")!),
        differentMethod = typeof(IDisposable).GetMethod("Dispose")!
            .HasSameMetadataDefinitionAs(typeof(IComparable).GetMethod("CompareTo")!),
        methodVsType = typeof(IDisposable).GetMethod("Dispose")!
            .HasSameMetadataDefinitionAs(typeof(IDisposable)),
        sameProperty = typeof(string).GetProperty("Chars")!
            .HasSameMetadataDefinitionAs(typeof(string).GetProperty("Chars")!),
        nullError = ObserveMethodError(() => typeof(IDisposable).GetMethod("Dispose")!
            .HasSameMetadataDefinitionAs(null!)),
        nullParameter = ObserveMethodArgumentName(() => typeof(IDisposable).GetMethod("Dispose")!
            .HasSameMetadataDefinitionAs(null!)),
    },
    selectedNestedOwnerBehavior = new[]
    {
        typeof(string), typeof(System.Collections.Generic.List<>).GetGenericArguments()[0],
        typeof(System.Collections.Generic.Dictionary<string, int>.KeyCollection),
        typeof(System.Collections.Generic.List<int>.Enumerator),
        typeof(System.Collections.Generic.List<int>.Enumerator[]),
    }.Select(type => new
    {
        name = type.FullName ?? type.Name,
        declaringType = type.DeclaringType?.FullName,
        reflectedType = type.ReflectedType?.FullName,
    }).ToArray(),
    selectedNestedNameBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!,
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "KeyCollection", System.Reflection.BindingFlags.Public)!,
        typeof(System.Collections.Generic.List<>).GetNestedType(
            "Enumerator", System.Reflection.BindingFlags.Public)!,
    }.Select(type => new
    {
        name = type.Name,
        fullName = type.FullName,
        @namespace = type.Namespace,
    }).ToArray(),
    selectedNestedDefinitionStringBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!,
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!.MakeArrayType(),
    }.Select(type => new { name = type.FullName, text = type.ToString() }).ToArray(),
    selectedNestedLookupBehavior = new[]
    {
        "System.Collections.Generic.Dictionary`2+Entry",
        "System.Collections.Generic.Dictionary`2+Entry[]",
        "system.collections.generic.dictionary`2+entry",
    }.Select((name, index) => new
    {
        name,
        resolved = Type.GetType(name, throwOnError: false, ignoreCase: index == 2)?.FullName,
    }).ToArray(),
    selectedNestedNameOnlyQueryBehavior = new
    {
        positive = ObserveNestedType(typeof(System.Collections.Generic.Dictionary<,>), "KeyCollection"),
        lowerMiss = ObserveNestedType(typeof(System.Collections.Generic.Dictionary<,>), "keycollection"),
        missing = ObserveNestedType(typeof(System.Collections.Generic.Dictionary<,>), "Missing"),
        nullName = ObserveNestedType(typeof(System.Collections.Generic.Dictionary<,>), null),
    },
    selectedEnumNamesBehavior = new
    {
        typeCode = ObserveEnumNames(typeof(TypeCode)),
        memberTypes = ObserveEnumNames(typeof(MemberTypes)),
        genericParameterAttributes = ObserveEnumNames(typeof(GenericParameterAttributes)),
        numberStyles = ObserveEnumNames(typeof(System.Globalization.NumberStyles)),
        nonEnum = ObserveEnumNames(typeof(int)),
    },
    selectedNumberStylesFullValues = Enum.GetNames<System.Globalization.NumberStyles>()
        .Select(name => new { name, value = (int)Enum.Parse<System.Globalization.NumberStyles>(name) })
        .ToArray(),
    selectedEnumDefinedBehavior = new
    {
        enumValue = ObserveEnumDefined(typeof(TypeCode), TypeCode.Empty),
        integerValue = ObserveEnumDefined(typeof(TypeCode), 0),
        exactName = ObserveEnumDefined(typeof(TypeCode), "Empty"),
        lowerName = ObserveEnumDefined(typeof(TypeCode), "empty"),
        missingName = ObserveEnumDefined(typeof(TypeCode), "Missing"),
        missingValue = ObserveEnumDefined(typeof(TypeCode), 17),
        longValue = ObserveEnumDefined(typeof(TypeCode), 0L),
        byteValue = ObserveEnumDefined(typeof(TypeCode), (byte)0),
        wrongEnumType = ObserveEnumDefined(typeof(MemberTypes), TypeCode.Empty),
        nullValue = ObserveEnumDefined(typeof(TypeCode), null),
        nonEnumOwner = ObserveEnumDefined(typeof(int), 0),
    },
    selectedEnumNameBehavior = new
    {
        enumValue = ObserveEnumName(typeof(TypeCode), TypeCode.Empty),
        integerValue = ObserveEnumName(typeof(TypeCode), 0),
        missingValue = ObserveEnumName(typeof(TypeCode), 17),
        longValue = ObserveEnumName(typeof(TypeCode), 0L),
        byteValue = ObserveEnumName(typeof(TypeCode), (byte)0),
        stringValue = ObserveEnumName(typeof(TypeCode), "Empty"),
        wrongEnumType = ObserveEnumName(typeof(MemberTypes), TypeCode.Empty),
        nullValue = ObserveEnumName(typeof(TypeCode), null),
        nonEnumOwner = ObserveEnumName(typeof(int), 0),
    },
    selectedEnumValuesBehavior = new
    {
        typeCode = ObserveEnumValues(typeof(TypeCode)),
        memberTypes = ObserveEnumValues(typeof(MemberTypes)),
        numberStyles = ObserveEnumValues(typeof(System.Globalization.NumberStyles)),
        nonEnum = ObserveEnumValues(typeof(int)),
    },
    selectedEnumUnderlyingValuesBehavior = new
    {
        typeCode = ObserveEnumUnderlyingValues(typeof(TypeCode)),
        memberTypes = ObserveEnumUnderlyingValues(typeof(MemberTypes)),
        numberStyles = ObserveEnumUnderlyingValues(typeof(System.Globalization.NumberStyles)),
        nonEnum = ObserveEnumUnderlyingValues(typeof(int)),
    },
    selectedEnumUnderlyingTypeBehavior = new
    {
        typeCode = ObserveEnumUnderlyingType(typeof(TypeCode)),
        memberTypes = ObserveEnumUnderlyingType(typeof(MemberTypes)),
        nonEnum = ObserveEnumUnderlyingType(typeof(int)),
    },
    selectedNestedEnumerationBehavior = new[]
    {
        typeof(System.Collections.Generic.List<>), typeof(object),
        typeof(System.Collections.Generic.Dictionary<,>),
    }.Select(type => new
    {
        owner = type.FullName,
        publicNested = type.GetNestedTypes().Select(nested => nested.FullName).ToArray(),
    }).ToArray(),
    selectedConstructedNestedQueryBehavior = new
    {
        open = typeof(System.Collections.Generic.Dictionary<,>).GetNestedType("KeyCollection")?.FullName,
        closed = typeof(System.Collections.Generic.Dictionary<string, int>).GetNestedType("KeyCollection")?.FullName,
        sameReference = ReferenceEquals(
            typeof(System.Collections.Generic.Dictionary<,>).GetNestedType("KeyCollection"),
            typeof(System.Collections.Generic.Dictionary<string, int>).GetNestedType("KeyCollection")),
        closedEnumeration = typeof(System.Collections.Generic.Dictionary<string, int>)
            .GetNestedTypes().Select(nested => nested.FullName).ToArray(),
    },
    selectedNonpublicNestedQueryBehavior = new
    {
        publicOnly = ObserveNestedType(typeof(System.Collections.Generic.Dictionary<,>), "Entry"),
        nonpublic = typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", BindingFlags.NonPublic)?.FullName,
        publicEnumerationContainsEntry = typeof(System.Collections.Generic.Dictionary<,>)
            .GetNestedTypes().Any(nested => nested.Name == "Entry"),
    },
    selectedElementNestedQueryBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).MakeArrayType(),
        typeof(System.Collections.Generic.Dictionary<,>).MakeByRefType(),
        typeof(System.Collections.Generic.Dictionary<,>).MakePointerType(),
        typeof(System.Collections.Generic.Dictionary<,>).GetGenericArguments()[0],
    }.Select(type => new
    {
        owner = type.FullName ?? type.Name,
        query = ObserveNestedType(type, "KeyCollection"),
        enumerationLength = type.GetNestedTypes().Length,
    }).ToArray(),
    selectedNestedPublicVisibilityBehavior = new[]
    {
        typeof(string), typeof(System.Collections.Generic.List<>).GetGenericArguments()[0],
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!,
        typeof(System.Collections.Generic.Dictionary<string, int>.KeyCollection),
        typeof(System.Collections.Generic.List<int>.Enumerator),
    }.Select(type => new
    {
        name = type.FullName ?? type.Name,
        isPublic = type.IsPublic,
        isNestedPublic = type.IsNestedPublic,
        isVisible = type.IsVisible,
    }).ToArray(),
    selectedGenericArgumentVisibilityBehavior = new[]
    {
        typeof(System.Collections.Generic.List<string>),
        typeof(System.Collections.Generic.List<>).MakeGenericType(NestedFamilyProbe.PrivateMarkerType),
        typeof(System.Collections.Generic.List<>).MakeGenericType(NestedFamilyProbe.PrivateMarkerType).MakeArrayType(),
    }.Select(type => new { name = type.FullName, isVisible = type.IsVisible }).ToArray(),
    selectedNestedParentVisibilityBehavior = new[]
    {
        typeof(System.Collections.Generic.List<int>.Enumerator),
        NestedFamilyProbe.PrivateOwnerChildType,
    }.Select(type => new
    {
        name = type.FullName,
        isPublic = type.IsPublic,
        isNestedPublic = type.IsNestedPublic,
        isVisible = type.IsVisible,
        declaringVisible = type.DeclaringType!.IsVisible,
    }).ToArray(),
    selectedNestedArrayVisibilityBehavior = new[]
    {
        typeof(System.Collections.Generic.List<int>.Enumerator[]),
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!.MakeArrayType(),
    }.Select(type => new
    {
        name = type.FullName,
        isPublic = type.IsPublic,
        isVisible = type.IsVisible,
        isNested = type.IsNested,
    }).ToArray(),
    selectedNestedQualifiedRoundTripBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!,
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!.MakeArrayType(),
    }.Select(type => new
    {
        name = type.FullName,
        qualified = type.AssemblyQualifiedName,
        sameReference = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
    }).ToArray(),
    selectedNestedConstructedIdentityBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
            .MakeGenericType(typeof(string), typeof(int)),
    }.Select(type => new
    {
        name = type.FullName,
        text = type.ToString(),
        isConstructed = type.IsConstructedGenericType,
        definition = type.GetGenericTypeDefinition().FullName,
        arguments = type.GetGenericArguments().Select(argument => argument.FullName).ToArray(),
    }).ToArray(),
    selectedNestedConstructedLookupBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
            .MakeGenericType(typeof(string), typeof(int)),
    }.Select(type => new
    {
        name = type.FullName,
        qualified = type.AssemblyQualifiedName,
        fullNameSameReference = ReferenceEquals(type, Type.GetType(type.FullName!)),
        qualifiedSameReference = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
    }).ToArray(),
    selectedNestedConstructedArrayLookupBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
            .MakeGenericType(typeof(string), typeof(int)).MakeArrayType(),
    }.Select(type => new
    {
        name = type.FullName,
        fullNameSameReference = ReferenceEquals(type, Type.GetType(type.FullName!)),
        qualifiedSameReference = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
    }).ToArray(),
    selectedNestedConstructedRectangleLookupBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
            .MakeGenericType(typeof(string), typeof(int)).MakeArrayType(2),
    }.Select(type => new
    {
        name = type.FullName,
        fullNameSameReference = ReferenceEquals(type, Type.GetType(type.FullName!)),
        qualifiedSameReference = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
    }).ToArray(),
    selectedNestedConstructedRankThreeLookupBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
            .MakeGenericType(typeof(string), typeof(int)).MakeArrayType(3),
    }.Select(type => new
    {
        name = type.FullName,
        fullNameSameReference = ReferenceEquals(type, Type.GetType(type.FullName!)),
        qualifiedSameReference = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
    }).ToArray(),
    selectedNestedConstructedVariableLookupBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
            .MakeGenericType(typeof(string), typeof(int)).MakeArrayType(1),
    }.Select(type => new
    {
        name = type.FullName,
        fullNameSameReference = ReferenceEquals(type, Type.GetType(type.FullName!)),
        qualifiedSameReference = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
    }).ToArray(),
    selectedNestedConstructedByRefLookupBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
            .MakeGenericType(typeof(string), typeof(int)).MakeByRefType(),
    }.Select(type => new
    {
        name = type.FullName,
        fullNameSameReference = ReferenceEquals(type, Type.GetType(type.FullName!)),
        qualifiedSameReference = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
    }).ToArray(),
    selectedNestedConstructedPointerLookupBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
            .MakeGenericType(typeof(string), typeof(int)).MakePointerType(),
    }.Select(type => new
    {
        name = type.FullName,
        fullNameSameReference = ReferenceEquals(type, Type.GetType(type.FullName!)),
        qualifiedSameReference = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
    }).ToArray(),
    selectedNestedCompositeLookupBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
            .MakeGenericType(typeof(string), typeof(int)).MakeArrayType().MakeByRefType(),
    }.Select(type => new
    {
        name = type.FullName,
        fullNameSameReference = ReferenceEquals(type, Type.GetType(type.FullName!)),
        qualifiedSameReference = ReferenceEquals(type, Type.GetType(type.AssemblyQualifiedName!)),
    }).ToArray(),
    selectedNestedLookupMissBehavior = new[]
    {
        "System.Collections.Generic.Dictionary`2+entry",
        "System.Collections.Generic.Dictionary`2+Missing",
        "System.Collections.Generic.Dictionary`2+Entry[[System.String, System.Private.CoreLib]]",
    }.Select(name =>
    {
        try
        {
            return new { name, outcome = Type.GetType(name, throwOnError: false)?.FullName ?? "null" };
        }
        catch (Exception error)
        {
            return new { name, outcome = error.GetType().FullName ?? error.GetType().Name };
        }
    }).ToArray(),
    selectedNestedConstructedIgnoreCaseBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
            .MakeGenericType(typeof(string), typeof(int)),
    }.Select(type => new
    {
        lower = type.FullName!.ToLowerInvariant(),
        exactMiss = Type.GetType(type.FullName!.ToLowerInvariant()) is null,
        insensitiveSameReference = ReferenceEquals(type,
            Type.GetType(type.FullName!.ToLowerInvariant(), throwOnError: false, ignoreCase: true)),
    }).ToArray(),
    selectedNestedQualifiedIgnoreCaseBehavior = new[]
    {
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
            .MakeGenericType(typeof(string), typeof(int)),
    }.Select(type => new
    {
        lower = type.AssemblyQualifiedName!.ToLowerInvariant(),
        exactMiss = Type.GetType(type.AssemblyQualifiedName!.ToLowerInvariant()) is null,
        insensitiveSameReference = ReferenceEquals(type,
            Type.GetType(type.AssemblyQualifiedName!.ToLowerInvariant(),
                throwOnError: false, ignoreCase: true)),
    }).ToArray(),
    selectedNestedGenericParameterOwnerBehavior =
        typeof(System.Collections.Generic.Dictionary<,>).GetNestedType(
            "Entry", System.Reflection.BindingFlags.NonPublic)!
        .GetGenericArguments().Select(type => new
        {
            name = type.Name,
            position = type.GenericParameterPosition,
            declaring = type.DeclaringType?.FullName,
            isNested = type.IsNested,
            isNestedPublic = type.IsNestedPublic,
            isPublic = type.IsPublic,
            isVisible = type.IsVisible,
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
    selectedInt32ProviderFormatBehavior = ObserveInt32ProviderFormat(),
    selectedInt32NumberGroupSizes = ObserveInt32NumberGroupSizes(),
    selectedInt32CurrencyPercentGroupSizes = ObserveInt32CurrencyPercentGroupSizes(),
    selectedInt32GroupSizeBoundaries = ObserveInt32GroupSizeBoundaries(),
    selectedInt32NegativeSignBehavior = ObserveInt32NegativeSign(),
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
    selectedInt32CurrencyProviderBehavior = ObserveInt32CurrencyProvider(),
    selectedInt32PercentProviderBehavior = ObserveInt32PercentProvider(),
    selectedInt32FixedProviderBehavior = ObserveInt32FixedProvider(),
    selectedInt32ExponentialProviderBehavior = ObserveInt32ExponentialProvider(),
    selectedInt32PositiveSignBehavior = ObserveInt32PositiveSign(),
    selectedInt32NumberStyleProviderBehavior = ObserveInt32NumberStyleProvider(),
    selectedInt32NumberStyleBoundaries = ObserveInt32NumberStyleBoundaries(),
    selectedInt32FloatStyle = ObserveInt32FloatStyle(),
    selectedInt32SingleStyles = ObserveInt32SingleStyles(),
    selectedInt32CurrencyStyle = ObserveInt32CurrencyStyle(),
    selectedInt32AnyStyle = ObserveInt32AnyStyle(),
    selectedInt32CombinedStyles = ObserveInt32CombinedStyles(),
    selectedInt32MoreCombinedStyles = ObserveInt32MoreCombinedStyles(),
    selectedInt32TrailingSignStyles = ObserveInt32TrailingSignStyles(),
    selectedInt32GroupedDecimalStyles = ObserveInt32GroupedDecimalStyles(),
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
