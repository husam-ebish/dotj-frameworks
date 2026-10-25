"""Compare sixteen compiled Java candidate types with pinned selected CoreLib metadata."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
METADATA = EVIDENCE / "foundation-selected-metadata-v10.0.12.json"
ARTIFACT = EVIDENCE / "foundation-product-candidate-v1.json"
OUTPUT = EVIDENCE / "foundation-public-candidate-ledger-v1.json"
DATE_TIME_CONSTRUCTORS = [
    "public System.DateTime();",
    "public System.DateTime(long);",
    "public System.DateTime(long, System.DateTimeKind);",
    "public System.DateTime(int, int, int);",
    "public System.DateTime(int, int, int, int, int, int);",
    "public System.DateTime(int, int, int, int, int, int, int);",
    "public System.DateTime(int, int, int, int, int, int, System.DateTimeKind);",
    "public System.DateTime(int, int, int, int, int, int, int, System.DateTimeKind);",
    "public System.DateTime(int, int, int, int, int, int, int, int);",
    "public System.DateTime(int, int, int, int, int, int, int, int, System.DateTimeKind);",
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    pinned = json.loads(METADATA.read_text(encoding="utf-8"))
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    jar = ROOT / artifact["jarPath"]
    assert sha256(jar) == artifact["jarSha256"]
    assert pinned["coreLibSha256"] == "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"
    records = []
    for upstream in pinned["types"]:
        name = upstream["fullName"]
        output = subprocess.run(["javap", "-public", "-classpath", str(jar), name],
                                cwd=ROOT, capture_output=True, text=True, check=True).stdout
        lines = [line.strip() for line in output.splitlines()]
        header = next(line for line in lines if line.startswith("public ") and line.endswith("{"))
        declarations = [line for line in lines if line.startswith("public ") and line.endswith(";")]
        constructors = [line for line in declarations if line.startswith("public " + name + "(")]
        if name == "System.Decimal":
            assert constructors == ["public System.Decimal(int);", "public System.Decimal(long);",
                                    "public System.Decimal(int[]);",
                                    "public System.Decimal(int, int, int, boolean, int);"]
            assert len(upstream["publicConstructors"]) == 9
        elif name == "System.DateTime":
            assert constructors == DATE_TIME_CONSTRUCTORS
            assert len(upstream["publicConstructors"]) == 17
        elif name == "System.Int32":
            assert constructors == ["public System.Int32(int);"]
            assert len(upstream["publicConstructors"]) == 0
        else:
            assert len(constructors) == len(upstream["publicConstructors"])
        if name == "System.IDisposable":
            assert declarations == ["public abstract void Dispose();"]
            disposition = "EXACT_SELECTED_INTERFACE_MEMBER; behavior and release unqualified"
        elif name == "System.IComparable":
            assert "public interface System.IComparable" in header
            assert declarations == ["public abstract int CompareTo(java.lang.Object);"]
            disposition = "SELECTED_INTERFACE_MEMBER; Java Object parameter and behavior unqualified"
        elif name == "System.IFormattable":
            assert "public interface System.IFormattable" in header
            assert declarations == ["public abstract java.lang.String ToString(java.lang.String, System.IFormatProvider);"]
            disposition = "SELECTED_INTERFACE_MEMBER; formatting behavior unqualified"
        elif name == "System.ISpanFormattable":
            assert "public interface System.ISpanFormattable extends System.IFormattable" in header
            assert declarations == [
                "public abstract boolean TryFormat(char[], int[], java.lang.String, System.IFormatProvider);"]
            assert upstream["declaredPublicMethodCount"] == 1
            assert upstream["selectedMethods"][0]["name"] == "TryFormat"
            disposition = "SELECTED_BUFFER_FORMAT; Java arrays differ from CLR Span/out parameters"
        elif name == "System.IUtf8SpanFormattable":
            assert header == "public interface System.IUtf8SpanFormattable {"
            assert declarations == [
                "public abstract boolean TryFormat(byte[], int[], java.lang.String, System.IFormatProvider);"]
            assert upstream["declaredPublicMethodCount"] == 1
            assert upstream["selectedMethods"][0]["name"] == "TryFormat"
            disposition = "SELECTED_UTF8_BUFFER_FORMAT; Java arrays differ from CLR Span/out parameters"
        elif name == "System.IFormatProvider":
            assert "public interface System.IFormatProvider" in header
            assert declarations == ["public abstract java.lang.Object GetFormat(System.Type);"]
            disposition = "SELECTED_INTERFACE_MEMBER; provider behavior unqualified"
        elif name == "System.IConvertible":
            assert "public interface System.IConvertible" in header
            assert declarations == [
                "public abstract System.TypeCode GetTypeCode();",
                "public abstract boolean ToBoolean(System.IFormatProvider);",
                "public abstract char ToChar(System.IFormatProvider);",
                "public abstract byte ToSByte(System.IFormatProvider);",
                "public abstract short ToByte(System.IFormatProvider);",
                "public abstract short ToInt16(System.IFormatProvider);",
                "public abstract int ToUInt16(System.IFormatProvider);",
                "public abstract int ToInt32(System.IFormatProvider);",
                "public abstract long ToUInt32(System.IFormatProvider);",
                "public abstract long ToInt64(System.IFormatProvider);",
                "public abstract java.math.BigInteger ToUInt64(System.IFormatProvider);",
                "public abstract float ToSingle(System.IFormatProvider);",
                "public abstract double ToDouble(System.IFormatProvider);",
                "public abstract System.Decimal ToDecimal(System.IFormatProvider);",
                "public abstract System.DateTime ToDateTime(System.IFormatProvider);",
                "public abstract java.lang.String ToString(System.IFormatProvider);",
                "public abstract java.lang.Object ToType(System.Type, System.IFormatProvider);",
            ]
            assert upstream["declaredPublicMethodCount"] == 17
            assert len(upstream["selectedMethods"]) == 17
            pinned_methods = {method["name"]: method for method in upstream["selectedMethods"]}
            assert pinned_methods["ToUInt64"]["returnType"] == "System.UInt64"
            assert pinned_methods["ToSingle"]["returnType"] == "System.Single"
            assert pinned_methods["ToBoolean"]["parameters"] == [
                {"name": "provider", "type": "System.IFormatProvider"}]
            disposition = "SELECTED_INTERFACE_METHOD_NAMES; 17 methods, backend return types and conversion behavior unqualified"
        elif name == "System.Type":
            assert "public abstract class System.Type extends System.Reflection.MemberInfo" in header
            assert any(" MakeGenericType(System.Type[]);" in line for line in declarations)
            disposition = "PARTIAL_PUBLIC_SURFACE; MemberInfo base selected, other inherited members and semantics open"
        elif name == "System.Reflection.MemberInfo":
            assert header == "public abstract class System.Reflection.MemberInfo {"
            assert declarations == ["public abstract java.lang.String get_Name();",
                                    "public abstract System.Reflection.MemberTypes get_MemberType();",
                                    "public abstract System.Type get_DeclaringType();",
                                    "public abstract System.Type get_ReflectedType();",
                                    "public boolean get_IsCollectible();",
                                    "public boolean HasSameMetadataDefinitionAs(System.Reflection.MemberInfo);"]
            assert upstream["nameGetterIsAbstract"]
            assert upstream["declaringGetterIsAbstract"] and upstream["reflectedGetterIsAbstract"]
            disposition = "PARTIAL_MEMBERINFO_SURFACE; four selected abstract properties, collectibility and metadata identity"
        elif name == "System.Reflection.MemberTypes":
            assert header == "public final class System.Reflection.MemberTypes {"
            assert "public int get_Value();" in declarations
            assert "public System.Reflection.MemberTypes or(System.Reflection.MemberTypes);" in declarations
            disposition = "PARTIAL_ENUM_SURFACE; selected combinable values, CLR Enum inheritance open"
        elif name == "System.Reflection.GenericParameterAttributes":
            assert "extends java.lang.Enum<System.Reflection.GenericParameterAttributes>" in header
            assert "public int get_Value();" in declarations
            assert upstream["baseType"] == "System.Enum"
            disposition = "SELECTED_ENUM_VALUES; Java enum differs from CLR flags enum"
        elif name == "System.TypeCode":
            assert "extends java.lang.Enum<System.TypeCode>" in header
            assert "public int get_Value();" in declarations
            assert upstream["declaredPublicMethodCount"] == 0
            disposition = "SELECTED_ENUM_VALUES; Java enum differs from CLR Enum"
        elif name == "System.Decimal":
            assert header == "public final class System.Decimal implements System.IConvertible {"
            assert declarations == ["public System.Decimal(int);", "public System.Decimal(long);",
                                    "public System.Decimal(int[]);",
                                    "public System.Decimal(int, int, int, boolean, int);",
                                    "public int get_Scale();",
                                    "public static int[] GetBits(System.Decimal);",
                                    "public static System.Decimal Truncate(System.Decimal);",
                                    "public static System.Decimal Floor(System.Decimal);",
                                    "public static System.Decimal Ceiling(System.Decimal);",
                                    "public static System.Decimal Round(System.Decimal, int);",
                                    "public static System.Decimal Round(System.Decimal, int, System.MidpointRounding);",
                                    "public static System.Decimal Round(System.Decimal);",
                                    "public static System.Decimal Round(System.Decimal, System.MidpointRounding);",
                                    "public static System.Decimal Abs(System.Decimal);",
                                    "public static int Sign(System.Decimal);",
                                    "public static System.Decimal Negate(System.Decimal);",
                                    "public static System.Decimal Add(System.Decimal, System.Decimal);",
                                    "public static System.Decimal Subtract(System.Decimal, System.Decimal);",
                                    "public static System.Decimal Multiply(System.Decimal, System.Decimal);",
                                    "public static System.Decimal Divide(System.Decimal, System.Decimal);",
                                    "public static System.Decimal Remainder(System.Decimal, System.Decimal);",
                                    "public static int Compare(System.Decimal, System.Decimal);",
                                    "public static boolean Equals(System.Decimal, System.Decimal);",
                                    "public int GetHashCode();",
                                    "public boolean Equals(System.Decimal);",
                                    "public boolean Equals(java.lang.Object);",
                                    "public boolean equals(java.lang.Object);",
                                    "public int hashCode();",
                                    "public int CompareTo(System.Decimal);",
                                    "public int CompareTo(java.lang.Object);",
                                    "public static int ToInt32(System.Decimal);",
                                    "public static boolean IsNegative(System.Decimal);",
                                    "public static boolean IsPositive(System.Decimal);",
                                    "public static boolean IsInteger(System.Decimal);",
                                    "public static boolean IsEvenInteger(System.Decimal);",
                                    "public static boolean IsOddInteger(System.Decimal);",
                                    "public static long ToInt64(System.Decimal);",
                                    "public static long ToOACurrency(System.Decimal);",
                                    "public static System.Decimal FromOACurrency(long);",
                                    "public static long ToUInt32(System.Decimal);",
                                    "public static java.math.BigInteger ToUInt64(System.Decimal);",
                                    "public static short ToByte(System.Decimal);",
                                    "public static byte ToSByte(System.Decimal);",
                                    "public static short ToInt16(System.Decimal);",
                                    "public static int ToUInt16(System.Decimal);",
                                    "public static double ToDouble(System.Decimal);",
                                    "public static float ToSingle(System.Decimal);",
                                    "public static System.Decimal CopySign(System.Decimal, System.Decimal);",
                                    "public static System.Decimal Max(System.Decimal, System.Decimal);",
                                    "public static System.Decimal Min(System.Decimal, System.Decimal);",
                                    "public static System.Decimal Clamp(System.Decimal, System.Decimal, System.Decimal);",
                                    "public static System.Decimal MaxMagnitude(System.Decimal, System.Decimal);",
                                    "public static System.Decimal MinMagnitude(System.Decimal, System.Decimal);",
                                    "public static boolean IsCanonical(System.Decimal);",
                                    "public static System.Decimal Parse(java.lang.String);",
                                    "public static <T> System.Decimal Parse(System.ReadOnlySpan<T>);",
                                    "public static System.Decimal Parse(java.lang.String, System.IFormatProvider);",
                                    "public static <T> System.Decimal Parse(System.ReadOnlySpan<T>, System.IFormatProvider);",
                                    "public static System.Decimal Parse(java.lang.String, System.Globalization.NumberStyles, System.IFormatProvider);",
                                    "public static <T> System.Decimal Parse(System.ReadOnlySpan<T>, System.Globalization.NumberStyles, System.IFormatProvider);",
                                    "public static boolean TryParse(java.lang.String, System.Decimal[]);",
                                    "public static <T> boolean TryParse(System.ReadOnlySpan<T>, System.Decimal[]);",
                                    "public static boolean TryParse(java.lang.String, System.IFormatProvider, System.Decimal[]);",
                                    "public static <T> boolean TryParse(System.ReadOnlySpan<T>, System.IFormatProvider, System.Decimal[]);",
                                    "public static boolean TryParse(java.lang.String, System.Globalization.NumberStyles, System.IFormatProvider, System.Decimal[]);",
                                    "public static <T> boolean TryParse(System.ReadOnlySpan<T>, System.Globalization.NumberStyles, System.IFormatProvider, System.Decimal[]);",
                                    "public java.lang.String ToString();",
                                    "public java.lang.String ToString(System.IFormatProvider);",
                                    "public java.lang.String ToString(java.lang.String, System.IFormatProvider);",
                                    "public System.TypeCode GetTypeCode();",
                                    "public boolean ToBoolean(System.IFormatProvider);",
                                    "public char ToChar(System.IFormatProvider);",
                                    "public byte ToSByte(System.IFormatProvider);",
                                    "public short ToByte(System.IFormatProvider);",
                                    "public short ToInt16(System.IFormatProvider);",
                                    "public int ToUInt16(System.IFormatProvider);",
                                    "public int ToInt32(System.IFormatProvider);",
                                    "public long ToUInt32(System.IFormatProvider);",
                                    "public long ToInt64(System.IFormatProvider);",
                                    "public java.math.BigInteger ToUInt64(System.IFormatProvider);",
                                    "public float ToSingle(System.IFormatProvider);",
                                    "public double ToDouble(System.IFormatProvider);",
                                    "public System.Decimal ToDecimal(System.IFormatProvider);",
                                    "public System.DateTime ToDateTime(System.IFormatProvider);",
                                    "public java.lang.Object ToType(System.Type, System.IFormatProvider);"]
            assert upstream["declaredPublicMethodCount"] == 78
            disposition = "PARTIAL_VALUE_SURFACE; selected Decimal IConvertible, Parse and invariant text"
        elif name == "System.DateTime":
            assert header == "public final class System.DateTime implements System.IConvertible,System.IComparable,System.ISpanFormattable,System.IUtf8SpanFormattable {"
            assert declarations == ["public static final System.DateTime MinValue;",
                                    "public static final System.DateTime MaxValue;",
                                    "public static final System.DateTime UnixEpoch;",
                                    *DATE_TIME_CONSTRUCTORS,
                                    "public static System.DateTime SpecifyKind(System.DateTime, System.DateTimeKind);",
                                    "public static System.DateTime Parse(java.lang.String);",
                                    "public static System.DateTime Parse(java.lang.String, System.IFormatProvider);",
                                    "public static System.DateTime Parse(java.lang.String, System.IFormatProvider, System.Globalization.DateTimeStyles);",
                                    "public static System.DateTime Parse(System.ReadOnlySpan<java.lang.Character>);",
                                    "public static System.DateTime Parse(System.ReadOnlySpan<java.lang.Character>, System.IFormatProvider);",
                                    "public static System.DateTime Parse(System.ReadOnlySpan<java.lang.Character>, System.IFormatProvider, System.Globalization.DateTimeStyles);",
                                    "public static boolean TryParse(java.lang.String, System.DateTime[]);",
                                    "public static boolean TryParse(java.lang.String, System.IFormatProvider, System.DateTime[]);",
                                    "public static boolean TryParse(java.lang.String, System.IFormatProvider, System.Globalization.DateTimeStyles, System.DateTime[]);",
                                    "public static boolean TryParse(System.ReadOnlySpan<java.lang.Character>, System.DateTime[]);",
                                    "public static boolean TryParse(System.ReadOnlySpan<java.lang.Character>, System.IFormatProvider, System.DateTime[]);",
                                    "public static boolean TryParse(System.ReadOnlySpan<java.lang.Character>, System.IFormatProvider, System.Globalization.DateTimeStyles, System.DateTime[]);",
                                    "public static System.DateTime ParseExact(java.lang.String, java.lang.String, System.IFormatProvider);",
                                    "public static boolean TryParseExact(java.lang.String, java.lang.String, System.IFormatProvider, System.DateTime[]);",
                                    "public static System.DateTime ParseExact(System.ReadOnlySpan<java.lang.Character>, System.ReadOnlySpan<java.lang.Character>, System.IFormatProvider);",
                                    "public static boolean TryParseExact(System.ReadOnlySpan<java.lang.Character>, System.ReadOnlySpan<java.lang.Character>, System.IFormatProvider, System.DateTime[]);",
                                    "public static System.DateTime FromBinary(long);",
                                    "public static System.DateTime FromFileTimeUtc(long);",
                                    "public static System.DateTime FromFileTime(long);",
                                    "public static System.DateTime FromOADate(double);",
                                    "public static boolean IsLeapYear(int);",
                                    "public static int DaysInMonth(int, int);",
                                    "public static int Compare(System.DateTime, System.DateTime);",
                                    "public int CompareTo(System.DateTime);",
                                    "public int CompareTo(java.lang.Object);",
                                    "public static boolean Equals(System.DateTime, System.DateTime);",
                                    "public boolean Equals(System.DateTime);",
                                    "public boolean Equals(java.lang.Object);",
                                    "public boolean equals(java.lang.Object);",
                                    "public int GetHashCode();",
                                    "public int hashCode();",
                                    "public System.DateTime AddTicks(long);",
                                    "public System.DateTime Add(System.TimeSpan);",
                                    "public System.DateTime Subtract(System.TimeSpan);",
                                    "public System.TimeSpan Subtract(System.DateTime);",
                                    "public System.DateTime AddMonths(int);",
                                    "public System.DateTime AddYears(int);",
                                    "public System.DateTime AddDays(double);",
                                    "public System.DateTime AddHours(double);",
                                    "public System.DateTime AddMinutes(double);",
                                    "public System.DateTime AddSeconds(double);",
                                    "public System.DateTime AddMilliseconds(double);",
                                    "public System.DateTime AddMicroseconds(double);",
                                    "public static System.DateTime get_UtcNow();",
                                    "public static System.DateTime get_Now();",
                                    "public static System.DateTime get_Today();",
                                    "public int get_Year();", "public int get_Month();",
                                    "public int get_Day();", "public int get_DayOfYear();",
                                    "public System.DayOfWeek get_DayOfWeek();",
                                    "public System.TimeSpan get_TimeOfDay();",
                                    "public System.DateTime get_Date();",
                                    "public System.DateTimeKind get_Kind();",
                                    "public long get_Ticks();",
                                    "public long ToBinary();",
                                    "public long ToFileTimeUtc();",
                                    "public long ToFileTime();",
                                    "public System.DateTime ToUniversalTime();",
                                    "public System.DateTime ToLocalTime();",
                                    "public boolean IsDaylightSavingTime();",
                                    "public void Deconstruct(int[], int[], int[]);",
                                    "public double ToOADate();",
                                    "public int get_Hour();",
                                    "public int get_Minute();", "public int get_Second();",
                                    "public int get_Millisecond();",
                                    "public int get_Microsecond();",
                                    "public int get_Nanosecond();",
                                    "public System.TypeCode GetTypeCode();",
                                    "public boolean ToBoolean(System.IFormatProvider);",
                                    "public char ToChar(System.IFormatProvider);",
                                    "public byte ToSByte(System.IFormatProvider);",
                                    "public short ToByte(System.IFormatProvider);",
                                    "public short ToInt16(System.IFormatProvider);",
                                    "public int ToUInt16(System.IFormatProvider);",
                                    "public int ToInt32(System.IFormatProvider);",
                                    "public long ToUInt32(System.IFormatProvider);",
                                    "public long ToInt64(System.IFormatProvider);",
                                    "public java.math.BigInteger ToUInt64(System.IFormatProvider);",
                                    "public float ToSingle(System.IFormatProvider);",
                                    "public double ToDouble(System.IFormatProvider);",
                                    "public System.Decimal ToDecimal(System.IFormatProvider);",
                                    "public System.DateTime ToDateTime(System.IFormatProvider);",
                                    "public java.lang.String ToString();",
                                    "public java.lang.String ToString(java.lang.String);",
                                    "public java.lang.String toString();",
                                    "public java.lang.String ToString(System.IFormatProvider);",
                                    "public java.lang.Object ToType(System.Type, System.IFormatProvider);",
                                    "public java.lang.String ToString(java.lang.String, System.IFormatProvider);",
                                    "public java.lang.String ToLongDateString();",
                                    "public java.lang.String ToShortDateString();",
                                    "public java.lang.String ToLongTimeString();",
                                    "public java.lang.String ToShortTimeString();",
                                    "public java.lang.String[] GetDateTimeFormats(char, System.IFormatProvider);",
                                    "public java.lang.String[] GetDateTimeFormats(char);",
                                    "public java.lang.String[] GetDateTimeFormats(System.IFormatProvider);",
                                    "public java.lang.String[] GetDateTimeFormats();",
                                    "public boolean TryFormat(char[], int[], java.lang.String, System.IFormatProvider);",
                                    "public boolean TryFormat(byte[], int[], java.lang.String, System.IFormatProvider);",
                                    "public <T> boolean TryFormat(System.Span<T>, int[], System.ReadOnlySpan<java.lang.Character>, System.IFormatProvider);"]
            assert upstream["declaredPublicMethodCount"] == 70
            disposition = "PARTIAL_VALUE_SURFACE; selected DateTime IConvertible and date construction/Parse/properties/text"
        elif name == "System.Int32":
            assert header.startswith("public final class System.Int32")
            assert "public static final int MaxValue;" in declarations
            assert "public static final int MinValue;" in declarations
            assert "public System.TypeCode GetTypeCode();" in declarations
            assert "public int ToInt32(System.IFormatProvider);" in declarations
            assert "public System.Decimal ToDecimal(System.IFormatProvider);" in declarations
            assert "public int CompareTo(java.lang.Object);" in declarations
            assert "public static System.Int32 Parse(java.lang.String);" in declarations
            assert "public static System.Int32 Parse(java.lang.String, System.Globalization.NumberStyles, System.IFormatProvider);" in declarations
            assert "public static boolean TryParse(java.lang.String, System.Int32[]);" in declarations
            assert "public static boolean TryParse(java.lang.String, System.Globalization.NumberStyles, System.IFormatProvider, System.Int32[]);" in declarations
            assert upstream["declaredPublicMethodCount"] == 53
            disposition = "PARTIAL_VALUE_SURFACE; selected conversion and comparison behavior only"
        elif name == "System.OverflowException":
            assert header == "public class System.OverflowException extends System.ArithmeticException {"
            assert len(constructors) == 3
            disposition = "SELECTED_ARITHMETIC_EXCEPTION; default message and HRESULT pinned"
        elif name == "System.InvalidCastException":
            assert header == "public class System.InvalidCastException extends System.SystemException {"
            assert len(constructors) == 4
            disposition = "SELECTED_EXCEPTION_CONSTRUCTORS; errorCode/HRESULT semantics open"
        elif name == "System.InvalidOperationException":
            assert header == "public class System.InvalidOperationException extends System.SystemException {"
            assert len(constructors) == 3
            disposition = "SELECTED_EXCEPTION_CONSTRUCTORS; exact messages and HRESULT open"
        elif name == "System.FormatException":
            assert header == "public class System.FormatException extends System.SystemException {"
            assert len(constructors) == 3
            disposition = "SELECTED_EXCEPTION_CONSTRUCTORS; exact messages and HRESULT open"
        elif name == "System.Globalization.CultureNotFoundException":
            assert header == "public class System.Globalization.CultureNotFoundException extends System.ArgumentException {"
            assert len(constructors) == 8
            assert "public java.lang.String get_InvalidCultureName();" in declarations
            disposition = "SELECTED_EXCEPTION_CONSTRUCTORS; culture semantics and exact messages open"
        elif name == "System.Globalization.NumberStyles":
            assert header == "public final class System.Globalization.NumberStyles {"
            assert "public int get_Value();" in declarations
            assert "public System.Globalization.NumberStyles Or(System.Globalization.NumberStyles);" in declarations
            assert "public static System.Globalization.NumberStyles[] values();" in declarations
            assert sum(line.startswith("public static final System.Globalization.NumberStyles ")
                       for line in declarations) == 19
            assert upstream["declaredPublicMethodCount"] == 0
            disposition = "SELECTED_FLAG_VALUES; immutable Java carrier plus Type enum projection; CLR ABI open"
        else:
            prefix = "public final class " if name == "System.IndexOutOfRangeException" else "public class "
            assert header.startswith(prefix + name)
            if name == "System.Exception":
                assert "public java.lang.String get_Message();" in declarations
                assert "public System.Exception get_InnerException();" in declarations
                assert "public System.Collections.IDictionary get_Data();" in declarations
                assert "public void GetObjectData(System.Runtime.Serialization.SerializationInfo, System.Runtime.Serialization.StreamingContext);" in declarations
                assert "public System.Reflection.MethodBase get_TargetSite();" in declarations
            if name == "System.ArgumentException":
                assert "public java.lang.String get_ParamName();" in declarations
            disposition = "PARTIAL_EXCEPTION_SURFACE; selected inheritance/constructors only"
        records.append({
            "upstreamFullName": name,
            "upstreamBaseType": upstream["baseType"],
            "upstreamIsInterface": upstream["isInterface"],
            "upstreamIsAbstract": upstream["isAbstract"],
            "upstreamDeclaredNonAccessorMethods": upstream["declaredPublicMethodCount"],
            "upstreamDeclaredProperties": upstream["declaredPublicPropertyCount"],
            "upstreamPublicConstructors": len(upstream["publicConstructors"]),
            "javaPublicConstructors": len(constructors),
            "javaPublicHeader": header,
            "javaPublicDeclarations": declarations,
            "disposition": disposition,
            "qualified": False,
        })
    assert len(records) == 30
    dictionary_api = subprocess.run(
        ["javap", "-public", "-classpath", str(jar), "System.Collections.IDictionary"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    assert "public interface System.Collections.IDictionary extends System.Collections.ICollection {" in dictionary_api
    assert "public abstract System.Collections.ICollection get_Keys();" in dictionary_api
    assert "public abstract System.Collections.IDictionaryEnumerator GetEnumerator();" in dictionary_api
    assert "public abstract void Add(java.lang.Object, java.lang.Object);" in dictionary_api
    type_record = next(item for item in records if item["upstreamFullName"] == "System.Type")
    assert type_record["upstreamDeclaredNonAccessorMethods"] == 109
    assert type_record["upstreamDeclaredProperties"] == 70
    snapshot = json.loads((EVIDENCE / "api-shapes-v10.0.12/system-type.json").read_text(encoding="utf-8"))
    assert len(snapshot["type"]["methods"]) == 181
    assert len(snapshot["type"]["properties"]) == 70
    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "coreLibSha256": pinned["coreLibSha256"],
        "metadataEvidence": METADATA.name,
        "candidateEvidence": ARTIFACT.name,
        "candidateJarSha256": artifact["jarSha256"],
        "typeCount": len(records),
        "typeMethodCountNote": "The earlier Type snapshot lists 181 declared methods including property accessors; this oracle counts 109 non-accessor methods and 70 properties.",
        "types": records,
        "acceptedN01TaskCredit": False,
        "status": "SELECTED_COMPILED_CANDIDATES_ONLY; complete E01/E02/E03/N01 public API and behavior qualification OPEN",
    }, indent=2) + "\n", encoding="utf-8")
    print("PASS thirty selected CoreLib identities mapped to compiled Java candidate declarations")


if __name__ == "__main__":
    main()
