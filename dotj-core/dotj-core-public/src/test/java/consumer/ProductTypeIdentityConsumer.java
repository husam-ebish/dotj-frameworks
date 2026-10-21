package consumer;

import System.Type;
import System.ArgumentNullException;
import System.ArgumentException;
import System.TypeLoadException;
import System.IO.FileNotFoundException;
import System.IO.IOException;
import System.IndexOutOfRangeException;
import System.IDisposable;
import System.IComparable;
import System.IFormattable;
import System.IFormatProvider;
import System.IConvertible;
import System.TypeCode;
import System.Decimal;
import System.DateTime;
import System.Int32;
import System.Reflection.MemberInfo;
import System.Reflection.MemberTypes;

/** Calls the candidate's public members from outside the System package. */
public final class ProductTypeIdentityConsumer {
    public static void main(String[] args) {
        Type definition = Type.GetType("System.Collections.Generic.List`1");
        Type string = Type.GetType("System.String");
        MemberInfo stringMember = string;
        if (!"String".equals(stringMember.get_Name())
                || stringMember.get_MemberType() != MemberTypes.TypeInfo
                || MemberTypes.TypeInfo.get_Value() != 32
                || MemberTypes.All.get_Value() != 191) {
            throw new AssertionError("Selected MemberInfo Name inheritance changed");
        }
        Type integer = Type.GetType("System.Int32");
        if (definition == null || string == null || integer == null
                || Type.GetType("System.Unknown") != null) {
            throw new AssertionError("Selected type-name lookup changed");
        }
        if (Type.GetType("system.string", false, true) != string
                || Type.GetType("system.string", false) != null
                || Type.GetType("System.Unknown", false, true) != null
                || Type.GetType("System.String", true) != string) {
            throw new AssertionError("Selected GetType overload behavior changed");
        }
        if (Type.GetType("System.String, System.Private.CoreLib") != string
                || Type.GetType("System.Int32, System.Private.CoreLib") != integer
                || Type.GetType("System.String, mscorlib") != string
                || Type.GetType("System.String, NotAnAssembly") != null) {
            throw new AssertionError("Selected assembly-qualified lookup changed");
        }
        if (Type.GetType("") != null || Type.GetType(" System.String") != string
                || Type.GetType("System.String ") != null
                || Type.GetType("System.String , System.Private.CoreLib") != null
                || Type.GetType("System.String, ") != null) {
            throw new AssertionError("Selected type-name boundary behavior changed");
        }
        try {
            Type.GetType("System.String, ", true);
            throw new AssertionError("Empty assembly accepted with throwOnError");
        } catch (ArgumentException expected) {
            if (!"typeName@13".equals(expected.get_ParamName())) {
                throw new AssertionError("Empty assembly parameter changed", expected);
            }
        }
        try {
            Type.GetType("System.String, NotAnAssembly", true);
            throw new AssertionError("Missing assembly accepted with throwOnError");
        } catch (FileNotFoundException expected) {
            if (!(expected instanceof IOException)) {
                throw new AssertionError("Missing assembly exception hierarchy changed", expected);
            }
        }
        try {
            Type.GetType("System.Unknown", true, false);
            throw new AssertionError("Missing type accepted with throwOnError");
        } catch (TypeLoadException expected) {
            // Selected error type observed from pinned CoreLib.
        }
        try {
            Type.GetType(null);
            throw new AssertionError("Null type name accepted");
        } catch (ArgumentNullException expected) {
            if (!"typeName".equals(expected.get_ParamName())) {
                throw new AssertionError("Public exception parameter changed", expected);
            }
        }
        Type first = definition.MakeGenericType(new Type[] {string});
        Type dictionary = Type.GetType("System.Collections.Generic.Dictionary`2");
        Type dictionaryStringInt = dictionary.MakeGenericType(new Type[] {string, integer});
        if (Type.GetType("System.Collections.Generic.Dictionary`2[System.String,System.Int32]")
                    != dictionaryStringInt
                || Type.GetType("System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Int32, System.Private.CoreLib]]")
                    != dictionaryStringInt
                || Type.GetType("System.Collections.Generic.Dictionary`2[System.Int32,System.String]")
                    != dictionary.MakeGenericType(new Type[] {integer, string})) {
            throw new AssertionError("Selected Dictionary name lookup changed");
        }
        if (Type.GetType("System.String[]") == null
                || Type.GetType("System.String[]") != Type.GetType("system.string[]", false, true)
                || Type.GetType("System.String[], System.Private.CoreLib") != Type.GetType("System.String[]")
                || Type.GetType("System.Int32[]") == null
                || Type.GetType("System.Collections.Generic.List`1[System.String]") != first
                || Type.GetType("System.Collections.Generic.List`1[[System.String, System.Private.CoreLib]]") != first) {
            throw new AssertionError("Selected array or generic type-name lookup changed");
        }
        Type jagged = Type.GetType("System.String[][]");
        if (jagged == null || jagged == Type.GetType("System.String[]")
                || jagged != Type.GetType("system.string[][]", false, true)) {
            throw new AssertionError("Selected jagged array identity changed");
        }
        Type rectangular = Type.GetType("System.String[,]");
        Type rankThree = Type.GetType("System.String[,,]");
        Type listArray = Type.GetType("System.Collections.Generic.List`1[System.String][]");
        if (rectangular == null || rankThree == null || listArray == null
                || rectangular == rankThree || rectangular == jagged
                || rectangular == Type.GetType("System.String[]")
                || rectangular != Type.GetType("System.String[,]")
                || rankThree != Type.GetType("system.string[,,]", false, true)
                || listArray != Type.GetType("System.Collections.Generic.List`1[System.String][]")
                || listArray.get_IsGenericType()) {
            throw new AssertionError("Selected CLR array-shape identity changed");
        }
        if (string.get_IsArray() || string.GetElementType() != null
                || !Type.GetType("System.String[]").get_IsArray()
                || Type.GetType("System.String[]").GetElementType() != string
                || Type.GetType("System.String[]").GetArrayRank() != 1
                || jagged.GetElementType() != Type.GetType("System.String[]")
                || jagged.GetArrayRank() != 1
                || rectangular.GetElementType() != string || rectangular.GetArrayRank() != 2
                || rankThree.GetElementType() != string || rankThree.GetArrayRank() != 3
                || listArray.GetElementType() != first || listArray.GetArrayRank() != 1) {
            throw new AssertionError("Selected array reflection behavior changed");
        }
        Type nonVectorRankOne = Type.GetType("System.String[*]");
        if (string.MakeArrayType() != Type.GetType("System.String[]")
                || string.MakeArrayType(1) != nonVectorRankOne
                || nonVectorRankOne == string.MakeArrayType()
                || nonVectorRankOne.GetArrayRank() != 1
                || nonVectorRankOne.GetElementType() != string
                || string.MakeArrayType(2) != rectangular
                || Type.GetType("System.String[]").MakeArrayType() != jagged
                || first.MakeArrayType() != listArray) {
            throw new AssertionError("Selected MakeArrayType behavior changed");
        }
        Type byReference = string.MakeByRefType();
        if (byReference != string.MakeByRefType()
                || byReference != Type.GetType("System.String&")
                || byReference != Type.GetType("system.string&", false, true)
                || !byReference.get_IsByRef() || string.get_IsByRef()
                || byReference.get_IsArray() || byReference.GetElementType() != string
                || Type.GetType("System.String[]").MakeByRefType()
                    != Type.GetType("System.String[]&")) {
            throw new AssertionError("Selected by-reference identity changed");
        }
        try {
            byReference.MakeByRefType();
            throw new AssertionError("Double by-reference type accepted");
        } catch (TypeLoadException expected) {
            // Selected pinned error type.
        }
        Type pointer = string.MakePointerType();
        if (pointer != string.MakePointerType() || pointer != Type.GetType("System.String*")
                || !pointer.get_IsPointer() || string.get_IsPointer()
                || pointer.get_IsByRef() || pointer.GetElementType() != string
                || pointer.MakePointerType() != pointer.MakePointerType()
                || pointer.MakePointerType().GetElementType() != pointer
                || integer.MakePointerType() != Type.GetType("System.Int32*")) {
            throw new AssertionError("Selected pointer type identity changed");
        }
        try {
            byReference.MakePointerType();
            throw new AssertionError("Pointer from by-reference type accepted");
        } catch (TypeLoadException expected) {
            // Selected pinned error type.
        }
        try {
            string.MakeArrayType(0);
            throw new AssertionError("Rank zero accepted");
        } catch (IndexOutOfRangeException expected) {
            // Selected pinned error type.
        }
        try {
            string.GetArrayRank();
            throw new AssertionError("Non-array rank accepted");
        } catch (ArgumentException expected) {
            // Selected pinned error type.
        }
        Type same = definition.MakeGenericType(new Type[] {string});
        Type different = definition.MakeGenericType(new Type[] {integer});
        if (first != same || !first.Equals(same) || first.Equals(different)
                || first.GetGenericTypeDefinition() != definition
                || first.GetGenericArguments()[0] != string
                || first.get_GenericTypeArguments()[0] != string
                || !first.get_IsConstructedGenericType() || !definition.get_IsGenericType()) {
            throw new AssertionError("External Type identity call changed");
        }
        Type parameter = definition.GetGenericArguments()[0];
        Type object = Type.GetType("System.Object");
        Type valueType = Type.GetType("System.ValueType");
        Type arrayBase = Type.GetType("System.Array");
        if (object == null || valueType == null || arrayBase == null
                || object.get_BaseType() != null || string.get_BaseType() != object
                || integer.get_BaseType() != valueType
                || valueType.get_BaseType() != object
                || definition.get_BaseType() != object || first.get_BaseType() != object
                || parameter.get_BaseType() != object
                || Type.GetType("System.String[]").get_BaseType() != arrayBase
                || rectangular.get_BaseType() != arrayBase
                || byReference.get_BaseType() != null || pointer.get_BaseType() != null) {
            throw new AssertionError("Selected BaseType projections changed");
        }
        if (!object.get_IsClass() || object.get_IsValueType()
                || !string.get_IsClass() || string.get_IsValueType()
                || integer.get_IsClass() || !integer.get_IsValueType()
                || !valueType.get_IsClass() || valueType.get_IsValueType()
                || !arrayBase.get_IsClass() || !definition.get_IsClass()
                || !first.get_IsClass() || !parameter.get_IsClass()
                || !rectangular.get_IsClass() || !byReference.get_IsClass()
                || !pointer.get_IsClass()) {
            throw new AssertionError("Selected class and value-type flags changed");
        }
        Type disposalType = Type.GetType("System.IDisposable");
        Type memberTypesType = Type.GetType("System.Reflection.MemberTypes");
        if (disposalType == null || memberTypesType == null
                || !disposalType.get_IsInterface() || disposalType.get_IsClass()
                || disposalType.get_IsValueType() || disposalType.get_IsEnum()
                || !memberTypesType.get_IsEnum() || !memberTypesType.get_IsValueType()
                || memberTypesType.get_IsClass() || memberTypesType.get_IsInterface()
                || string.get_IsInterface() || integer.get_IsEnum()) {
            throw new AssertionError("Selected interface and enum flags changed");
        }
        Type enumBase = Type.GetType("System.Enum");
        if (enumBase == null || memberTypesType.get_BaseType() != enumBase
                || enumBase.get_BaseType() != valueType
                || memberTypesType.GetEnumUnderlyingType() != integer) {
            throw new AssertionError("Selected enum base or underlying type changed");
        }
        try {
            string.GetEnumUnderlyingType();
            throw new AssertionError("Non-enum underlying type accepted");
        } catch (ArgumentException expected) {
            // Selected pinned error type.
        }
        if (!object.IsAssignableFrom(string) || !object.IsAssignableFrom(integer)
                || !object.IsAssignableFrom(disposalType)
                || !object.IsAssignableFrom(Type.GetType("System.String[]"))
                || object.IsAssignableFrom(byReference) || object.IsAssignableFrom(pointer)
                || !valueType.IsAssignableFrom(integer)
                || !valueType.IsAssignableFrom(memberTypesType)
                || valueType.IsAssignableFrom(string)
                || !enumBase.IsAssignableFrom(memberTypesType)
                || enumBase.IsAssignableFrom(integer)
                || !arrayBase.IsAssignableFrom(Type.GetType("System.String[]"))
                || arrayBase.IsAssignableFrom(string)
                || definition.IsAssignableFrom(first)
                || !first.IsAssignableFrom(first)
                || string.IsAssignableFrom(null)) {
            throw new AssertionError("Selected Type assignability changed");
        }
        if (!string.IsSubclassOf(object) || !integer.IsSubclassOf(valueType)
                || !integer.IsSubclassOf(object)
                || !memberTypesType.IsSubclassOf(enumBase)
                || !memberTypesType.IsSubclassOf(valueType)
                || !Type.GetType("System.String[]").IsSubclassOf(arrayBase)
                || !disposalType.IsSubclassOf(object)
                || first.IsSubclassOf(definition)
                || string.IsSubclassOf(string)) {
            throw new AssertionError("Selected Type subclass relationships changed");
        }
        try {
            string.IsSubclassOf(null);
            throw new AssertionError("Null subclass target accepted");
        } catch (ArgumentNullException expected) {
            if (!"type".equals(expected.get_ParamName())) {
                throw new AssertionError("Subclass null parameter changed", expected);
            }
        }
        IDisposable disposableValue = new IDisposable() {
            @Override
            public void Dispose() {
            }
        };
        if (!object.IsInstanceOfType("text") || !object.IsInstanceOfType(42)
                || object.IsInstanceOfType(null)
                || !string.IsInstanceOfType("text") || string.IsInstanceOfType(42)
                || !integer.IsInstanceOfType(42) || integer.IsInstanceOfType("text")
                || !valueType.IsInstanceOfType(42)
                || !enumBase.IsInstanceOfType(MemberTypes.TypeInfo)
                || !arrayBase.IsInstanceOfType(new String[] {"text"})
                || !Type.GetType("System.String[]").IsInstanceOfType(new String[] {"text"})
                || !disposalType.IsInstanceOfType(disposableValue)
                || definition.IsInstanceOfType(java.util.List.of("text"))
                || string.IsInstanceOfType(null)) {
            throw new AssertionError("Selected instance-of-type behavior changed");
        }
        if (object.GetInterfaces().length != 0 || disposalType.GetInterfaces().length != 0
                || object.GetInterface("System.IDisposable") != null
                || disposalType.GetInterface("System.IDisposable") != null
                || disposalType.GetInterface("") != null) {
            throw new AssertionError("Selected empty interface queries changed");
        }
        try {
            disposalType.GetInterface(null);
            throw new AssertionError("Null interface name accepted");
        } catch (ArgumentNullException expected) {
            if (!"fullname".equals(expected.get_ParamName())) {
                throw new AssertionError("Interface lookup parameter changed", expected);
            }
        }
        IComparable comparable = other -> other == null ? 1 : 0;
        Type comparableType = Type.GetType("System.IComparable");
        if (comparable.CompareTo(null) != 1 || comparableType == null
                || !comparableType.get_IsInterface()
                || string.GetInterface("System.IComparable") != comparableType
                || string.GetInterface("System.IComparable", true) != comparableType
                || string.GetInterface("IComparable") != comparableType
                || string.GetInterface("system.icomparable", true) != null
                || string.GetInterface("system.icomparable") != null
                || string.GetInterface("System.IDisposable") != null
                || !comparableType.IsAssignableFrom(string)
                || !comparableType.IsInstanceOfType("text")) {
            throw new AssertionError("Selected IComparable contract changed");
        }
        IFormatProvider provider = formatType -> formatType == null ? null : "format";
        IFormattable formattable = (format, formatProvider) ->
                formatProvider == provider && "D".equals(format) ? "42" : null;
        Type formattableType = Type.GetType("System.IFormattable");
        Type providerType = Type.GetType("System.IFormatProvider");
        if (!"42".equals(formattable.ToString("D", provider))
                || !"format".equals(provider.GetFormat(formattableType))
                || formattableType == null || providerType == null
                || !formattableType.get_IsInterface() || !providerType.get_IsInterface()
                || integer.GetInterface("System.IFormattable") != formattableType
                || integer.GetInterface("IFormattable") != formattableType
                || integer.GetInterface("system.iformattable", true) != null
                || string.GetInterface("System.IFormattable") != null
                || !formattableType.IsAssignableFrom(integer)
                || !formattableType.IsInstanceOfType(42)) {
            throw new AssertionError("Selected formatting interface contract changed");
        }
        IConvertible convertible = new IConvertible() {
            public TypeCode GetTypeCode() { return TypeCode.Int32; }
            public boolean ToBoolean(IFormatProvider formatProvider) { return true; }
            public char ToChar(IFormatProvider formatProvider) { return '*'; }
            public byte ToSByte(IFormatProvider formatProvider) { return 42; }
            public short ToByte(IFormatProvider formatProvider) { return 42; }
            public short ToInt16(IFormatProvider formatProvider) { return 42; }
            public int ToUInt16(IFormatProvider formatProvider) { return 42; }
            public int ToInt32(IFormatProvider formatProvider) { return 42; }
            public long ToUInt32(IFormatProvider formatProvider) { return 42; }
            public long ToInt64(IFormatProvider formatProvider) { return 42; }
            public java.math.BigInteger ToUInt64(IFormatProvider formatProvider) {
                return java.math.BigInteger.valueOf(42);
            }
            public float ToSingle(IFormatProvider formatProvider) { return 42; }
            public double ToDouble(IFormatProvider formatProvider) { return 42; }
            public Decimal ToDecimal(IFormatProvider formatProvider) {
                return new Decimal(42);
            }
            public DateTime ToDateTime(IFormatProvider formatProvider) {
                return new DateTime(2026, 1, 2);
            }
            public String ToString(IFormatProvider formatProvider) { return "42"; }
            public Object ToType(Type conversionType, IFormatProvider formatProvider) {
                return conversionType == integer ? 42 : null;
            }
        };
        Type convertibleType = Type.GetType("System.IConvertible");
        Int32 int32Value = new Int32(42);
        IConvertible int32Conversion = int32Value;
        IFormattable int32Formatting = int32Value;
        IComparable int32Comparison = int32Value;
        if (int32Conversion.GetTypeCode() != TypeCode.Int32
                || !int32Conversion.ToBoolean(provider)
                || int32Conversion.ToChar(provider) != '*'
                || int32Conversion.ToInt32(provider) != 42
                || !"42".equals(int32Conversion.ToDecimal(provider).ToString(provider))
                || !"42".equals(int32Conversion.ToString(provider))
                || !"42".equals(int32Formatting.ToString("D", provider))
                || int32Comparison.CompareTo(new Int32(41)) != 1
                || !integer.IsInstanceOfType(int32Value)
                || !convertibleType.IsInstanceOfType(int32Value)) {
            throw new AssertionError("Selected Int32 conversion behavior changed");
        }
        if (convertible.GetTypeCode() != TypeCode.Int32
                || TypeCode.Int32.get_Value() != 9 || TypeCode.String.get_Value() != 18
                || !Type.GetType("System.TypeCode").get_IsEnum()
                || !convertible.ToBoolean(provider) || convertible.ToChar(provider) != '*'
                || convertible.ToSByte(provider) != 42 || convertible.ToByte(provider) != 42
                || convertible.ToInt16(provider) != 42 || convertible.ToUInt16(provider) != 42
                || convertible.ToInt32(provider) != 42 || convertible.ToUInt32(provider) != 42
                || convertible.ToInt64(provider) != 42
                || !java.math.BigInteger.valueOf(42).equals(convertible.ToUInt64(provider))
                || convertible.ToSingle(provider) != 42 || convertible.ToDouble(provider) != 42
                || !"42".equals(convertible.ToDecimal(provider).ToString(provider))
                || !Type.GetType("System.Decimal").get_IsValueType()
                || convertible.ToDateTime(provider).get_Year() != 2026
                || convertible.ToDateTime(provider).get_Month() != 1
                || convertible.ToDateTime(provider).get_Day() != 2
                || !"2026-01-02".equals(convertible.ToDateTime(provider)
                        .ToString("yyyy-MM-dd", provider))
                || !Type.GetType("System.DateTime").get_IsValueType()
                || !"42".equals(convertible.ToString(provider))
                || !Integer.valueOf(42).equals(convertible.ToType(integer, provider))
                || convertibleType == null || !convertibleType.get_IsInterface()
                || integer.GetInterface("System.IConvertible") != convertibleType
                || integer.GetInterface("IConvertible") != convertibleType
                || integer.GetInterface("system.iconvertible", true) != null
                || object.GetInterface("System.IConvertible") != null
                || !convertibleType.IsAssignableFrom(integer)
                || !convertibleType.IsInstanceOfType(42)) {
            throw new AssertionError("Selected IConvertible contract changed");
        }
        MemberInfo parameterMember = parameter;
        if (stringMember.get_DeclaringType() != null || stringMember.get_ReflectedType() != null
                || parameterMember.get_DeclaringType() != definition
                || parameterMember.get_ReflectedType() != definition
                || first.get_DeclaringType() != null || first.get_ReflectedType() != null) {
            throw new AssertionError("Selected MemberInfo owner type changed");
        }
        if (!"String".equals(string.get_Name()) || !"System.String".equals(string.get_FullName())
                || !"System".equals(string.get_Namespace())
                || !"Int32".equals(integer.get_Name())
                || !"List`1".equals(definition.get_Name())
                || !"System.Collections.Generic.List`1".equals(definition.get_FullName())
                || !"System.Collections.Generic".equals(definition.get_Namespace())
                || !first.get_FullName().startsWith("System.Collections.Generic.List`1[[System.String,")
                || !"String[]".equals(Type.GetType("System.String[]").get_Name())
                || !"System.String[,]".equals(rectangular.get_FullName())
                || !"String&".equals(byReference.get_Name())
                || !"System.String*".equals(pointer.get_FullName())
                || !"T".equals(parameter.get_Name()) || parameter.get_FullName() != null
                || !"System.Collections.Generic".equals(parameter.get_Namespace())) {
            throw new AssertionError("Selected Type name projections changed");
        }
        if (!parameter.get_IsGenericParameter() || parameter.get_GenericParameterPosition() != 0
                || parameter != definition.GetGenericArguments()[0]) {
            throw new AssertionError("External generic parameter identity changed");
        }
        java.lang.System.out.println("PASS external System.Type selected identity consumer");
    }
}
