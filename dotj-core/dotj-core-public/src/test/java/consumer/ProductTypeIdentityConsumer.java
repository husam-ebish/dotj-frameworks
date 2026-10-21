package consumer;

import System.Type;
import System.Exception;
import System.ArgumentNullException;
import System.ArgumentException;
import System.TypeLoadException;
import System.IO.FileNotFoundException;
import System.IO.FileLoadException;
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
import System.OverflowException;
import System.InvalidCastException;
import System.InvalidOperationException;
import System.FormatException;
import System.Globalization.NumberStyles;
import System.Globalization.CultureNotFoundException;
import System.ISpanFormattable;
import System.IUtf8SpanFormattable;
import System.Reflection.MemberInfo;
import System.Reflection.MemberTypes;
import System.Reflection.GenericParameterAttributes;

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
        if (Type.GetTypeCode(null) != TypeCode.Empty
                || Type.GetTypeCode(Type.GetType("System.Object")) != TypeCode.Object
                || Type.GetTypeCode(string) != TypeCode.String
                || Type.GetTypeCode(integer) != TypeCode.Int32
                || Type.GetTypeCode(Type.GetType("System.Decimal")) != TypeCode.Decimal
                || Type.GetTypeCode(Type.GetType("System.DateTime")) != TypeCode.DateTime
                || Type.GetTypeCode(Type.GetType("System.Reflection.MemberTypes")) != TypeCode.Int32
                || Type.GetTypeCode(Type.GetType("System.String[]")) != TypeCode.Object
                || Type.GetTypeCode(definition) != TypeCode.Object) {
            throw new AssertionError("Selected Type.GetTypeCode values changed");
        }
        Object[] primitiveValues = {true, 'x', (byte) 2, (short) 3, 4L, 5.0f, 6.0d};
        TypeCode[] primitiveCodes = {TypeCode.Boolean, TypeCode.Char, TypeCode.Byte,
                TypeCode.Int16, TypeCode.Int64, TypeCode.Single, TypeCode.Double};
        Type[] primitiveTypes = Type.GetTypeArray(primitiveValues);
        for (int index = 0; index < primitiveCodes.length; index++) {
            if (Type.GetTypeCode(primitiveTypes[index]) != primitiveCodes[index]) {
                throw new AssertionError("Selected primitive TypeCode changed at " + index);
            }
        }
        Type booleanType = Type.GetType("System.Boolean");
        if (booleanType == null || booleanType != primitiveTypes[0]
                || !"Boolean".equals(booleanType.get_Name())
                || !"System.Boolean".equals(booleanType.get_FullName())
                || !"System.ValueType".equals(booleanType.get_BaseType().get_FullName())
                || !booleanType.get_IsPrimitive() || !booleanType.get_IsValueType()
                || !booleanType.get_IsSealed() || booleanType.get_IsClass()
                || !booleanType.IsAssignableTo(Type.GetType("System.ValueType"))
                || Type.GetTypeCode(booleanType) != TypeCode.Boolean) {
            throw new AssertionError("Selected Boolean Type identity changed");
        }
        Type charType = Type.GetType("System.Char");
        if (charType == null || charType != primitiveTypes[1]
                || !"Char".equals(charType.get_Name())
                || !"System.Char".equals(charType.get_FullName())
                || !"System.ValueType".equals(charType.get_BaseType().get_FullName())
                || !charType.get_IsPrimitive() || !charType.get_IsValueType()
                || !charType.get_IsSealed() || charType.get_IsClass()
                || !charType.IsAssignableTo(Type.GetType("System.ValueType"))
                || Type.GetTypeCode(charType) != TypeCode.Char) {
            throw new AssertionError("Selected Char Type identity changed");
        }
        Type int16Type = Type.GetType("System.Int16");
        if (int16Type == null || int16Type != primitiveTypes[3]
                || !"Int16".equals(int16Type.get_Name())
                || !"System.Int16".equals(int16Type.get_FullName())
                || !"System.ValueType".equals(int16Type.get_BaseType().get_FullName())
                || !int16Type.get_IsPrimitive() || !int16Type.get_IsValueType()
                || !int16Type.get_IsSealed() || int16Type.get_IsClass()
                || !int16Type.IsAssignableTo(Type.GetType("System.ValueType"))
                || Type.GetTypeCode(int16Type) != TypeCode.Int16) {
            throw new AssertionError("Selected Int16 Type identity changed");
        }
        Type int64Type = Type.GetType("System.Int64");
        if (int64Type == null || int64Type != primitiveTypes[4]
                || !"Int64".equals(int64Type.get_Name())
                || !"System.Int64".equals(int64Type.get_FullName())
                || !"System.ValueType".equals(int64Type.get_BaseType().get_FullName())
                || !int64Type.get_IsPrimitive() || !int64Type.get_IsValueType()
                || !int64Type.get_IsSealed() || int64Type.get_IsClass()
                || !int64Type.IsAssignableTo(Type.GetType("System.ValueType"))
                || Type.GetTypeCode(int64Type) != TypeCode.Int64) {
            throw new AssertionError("Selected Int64 Type identity changed");
        }
        Type singleType = Type.GetType("System.Single");
        if (singleType == null || singleType != primitiveTypes[5]
                || !"Single".equals(singleType.get_Name())
                || !"System.Single".equals(singleType.get_FullName())
                || !"System.ValueType".equals(singleType.get_BaseType().get_FullName())
                || !singleType.get_IsPrimitive() || !singleType.get_IsValueType()
                || !singleType.get_IsSealed() || singleType.get_IsClass()
                || !singleType.IsAssignableTo(Type.GetType("System.ValueType"))
                || Type.GetTypeCode(singleType) != TypeCode.Single) {
            throw new AssertionError("Selected Single Type identity changed");
        }
        Type doubleType = Type.GetType("System.Double");
        if (doubleType == null || doubleType != primitiveTypes[6]
                || !"Double".equals(doubleType.get_Name())
                || !"System.Double".equals(doubleType.get_FullName())
                || !"System.ValueType".equals(doubleType.get_BaseType().get_FullName())
                || !doubleType.get_IsPrimitive() || !doubleType.get_IsValueType()
                || !doubleType.get_IsSealed() || doubleType.get_IsClass()
                || !doubleType.IsAssignableTo(Type.GetType("System.ValueType"))
                || Type.GetTypeCode(doubleType) != TypeCode.Double) {
            throw new AssertionError("Selected Double Type identity changed");
        }
        Type byteType = Type.GetType("System.Byte");
        if (byteType == null || byteType != primitiveTypes[2]
                || !"Byte".equals(byteType.get_Name())
                || !"System.Byte".equals(byteType.get_FullName())
                || !"System.ValueType".equals(byteType.get_BaseType().get_FullName())
                || !byteType.get_IsPrimitive() || !byteType.get_IsValueType()
                || !byteType.get_IsSealed() || byteType.get_IsClass()
                || !byteType.IsAssignableTo(Type.GetType("System.ValueType"))
                || Type.GetTypeCode(byteType) != TypeCode.Byte) {
            throw new AssertionError("Selected Byte Type identity changed");
        }
        String[] selectedPrimitiveNames = {"System.Boolean", "System.Char", "System.Byte",
                "System.Int16", "System.Int64", "System.Single", "System.Double"};
        for (int index = 0; index < selectedPrimitiveNames.length; index++) {
            String name = selectedPrimitiveNames[index];
            String lower = name.toLowerCase(java.util.Locale.ROOT);
            String qualified = name + ", System.Private.CoreLib";
            if (Type.GetType(name) != primitiveTypes[index]
                    || Type.GetType(lower, false, false) != null
                    || Type.GetType(lower, false, true) != primitiveTypes[index]
                    || Type.GetType(qualified) != primitiveTypes[index]
                    || Type.GetType(qualified.toLowerCase(java.util.Locale.ROOT), false, true)
                            != primitiveTypes[index]) {
                throw new AssertionError("Selected primitive lookup changed: " + name);
            }
        }
        for (int index = 0; index < selectedPrimitiveNames.length; index++) {
            Type element = primitiveTypes[index];
            String vectorName = selectedPrimitiveNames[index] + "[]";
            Type vector = Type.GetType(vectorName);
            if (vector == null || vector != element.MakeArrayType()
                    || vector.GetElementType() != element || !vector.get_IsSZArray()
                    || vector.GetArrayRank() != 1 || Type.GetTypeCode(vector) != TypeCode.Object
                    || !(element.get_Name() + "[]").equals(vector.get_Name())
                    || !vectorName.equals(vector.get_FullName())
                    || Type.GetType(vector.get_AssemblyQualifiedName()) != vector
                    || Type.GetType(vectorName.toLowerCase(java.util.Locale.ROOT), false, true) != vector) {
                throw new AssertionError("Selected primitive vector identity changed: " + vectorName);
            }
        }
        for (int index = 0; index < selectedPrimitiveNames.length; index++) {
            Type element = primitiveTypes[index];
            String rectangularName = selectedPrimitiveNames[index] + "[,]";
            Type rectangularType = Type.GetType(rectangularName);
            if (rectangularType == null || rectangularType != element.MakeArrayType(2)
                    || rectangularType.GetElementType() != element
                    || rectangularType.get_IsSZArray() || !rectangularType.get_IsVariableBoundArray()
                    || rectangularType.GetArrayRank() != 2
                    || Type.GetTypeCode(rectangularType) != TypeCode.Object
                    || !(element.get_Name() + "[,]").equals(rectangularType.get_Name())
                    || !rectangularName.equals(rectangularType.get_FullName())
                    || Type.GetType(rectangularType.get_AssemblyQualifiedName()) != rectangularType
                    || Type.GetType(rectangularName.toLowerCase(java.util.Locale.ROOT), false, true)
                            != rectangularType) {
                throw new AssertionError("Selected primitive rectangular identity changed: " + rectangularName);
            }
        }
        for (int index = 0; index < selectedPrimitiveNames.length; index++) {
            Type element = primitiveTypes[index];
            String rankThreeName = selectedPrimitiveNames[index] + "[,,]";
            Type rankThree = Type.GetType(rankThreeName);
            if (rankThree == null || rankThree != element.MakeArrayType(3)
                    || rankThree.GetElementType() != element
                    || rankThree.get_IsSZArray() || !rankThree.get_IsVariableBoundArray()
                    || rankThree.GetArrayRank() != 3 || Type.GetTypeCode(rankThree) != TypeCode.Object
                    || !(element.get_Name() + "[,,]").equals(rankThree.get_Name())
                    || !rankThreeName.equals(rankThree.get_FullName())
                    || Type.GetType(rankThree.get_AssemblyQualifiedName()) != rankThree
                    || Type.GetType(rankThreeName.toLowerCase(java.util.Locale.ROOT), false, true)
                            != rankThree) {
                throw new AssertionError("Selected primitive rank-three identity changed: " + rankThreeName);
            }
        }
        for (int index = 0; index < selectedPrimitiveNames.length; index++) {
            Type element = primitiveTypes[index];
            String variableName = selectedPrimitiveNames[index] + "[*]";
            Type variableBound = Type.GetType(variableName);
            if (variableBound == null || variableBound != element.MakeArrayType(1)
                    || variableBound == element.MakeArrayType()
                    || variableBound.GetElementType() != element
                    || variableBound.get_IsSZArray() || !variableBound.get_IsVariableBoundArray()
                    || variableBound.GetArrayRank() != 1
                    || Type.GetTypeCode(variableBound) != TypeCode.Object
                    || !(element.get_Name() + "[*]").equals(variableBound.get_Name())
                    || !variableName.equals(variableBound.get_FullName())
                    || Type.GetType(variableBound.get_AssemblyQualifiedName()) != variableBound
                    || Type.GetType(variableName.toLowerCase(java.util.Locale.ROOT), false, true)
                            != variableBound) {
                throw new AssertionError("Selected primitive variable-bound identity changed: " + variableName);
            }
        }
        Type[] mixedTypes = Type.GetTypeArray(new Object[] {"text", 42, new Exception("x")});
        if (mixedTypes.length != 3 || mixedTypes[0] != string || mixedTypes[1] != integer
                || mixedTypes[2] != Type.GetType("System.Exception")
                || Type.GetTypeArray(new Object[0]).length != 0
                || Type.GetTypeArray(new Object[] {"text"}) == Type.GetTypeArray(new Object[] {"text"})) {
            throw new AssertionError("Selected Type.GetTypeArray results changed");
        }
        Type listOfString = definition.MakeGenericType(new Type[] {string});
        if (string.GetHashCode() != string.GetHashCode()
                || string.GetHashCode() != Type.GetType("System.String").GetHashCode()
                || integer.GetHashCode() != Type.GetType("System.Int32").GetHashCode()
                || listOfString.GetHashCode()
                    != definition.MakeGenericType(new Type[] {string}).GetHashCode()) {
            throw new AssertionError("Selected Type.GetHashCode stability changed");
        }
        if (!string.IsAssignableTo(Type.GetType("System.Object"))
                || Type.GetType("System.Object").IsAssignableTo(string)
                || !string.IsAssignableTo(Type.GetType("System.IComparable"))
                || Type.GetType("System.IComparable").IsAssignableTo(string)
                || !string.IsAssignableTo(string)
                || string.IsAssignableTo(null)
                || !integer.IsAssignableTo(Type.GetType("System.ValueType"))) {
            throw new AssertionError("Selected Type.IsAssignableTo direction changed");
        }
        if (!string.IsEquivalentTo(string)
                || !string.IsEquivalentTo(Type.GetType("System.String"))
                || string.IsEquivalentTo(integer)
                || string.IsEquivalentTo(null)
                || !listOfString.IsEquivalentTo(
                    definition.MakeGenericType(new Type[] {string}))
                || listOfString.IsEquivalentTo(
                    definition.MakeGenericType(new Type[] {integer}))
                || Type.GetType("System.String[]").IsEquivalentTo(
                    Type.GetType("System.String[,]"))) {
            throw new AssertionError("Selected Type.IsEquivalentTo identity changed");
        }
        try {
            Type.GetTypeArray(null);
            throw new AssertionError("Null type-array input accepted");
        } catch (ArgumentNullException expected) {
            if (!"args".equals(expected.get_ParamName())) {
                throw new AssertionError("Null type-array parameter changed");
            }
        }
        try {
            Type.GetTypeArray(new Object[] {"text", null});
            throw new AssertionError("Null type-array element accepted");
        } catch (ArgumentException expected) {
            if (!"args".equals(expected.get_ParamName())) {
                throw new AssertionError("Null type-array element parameter changed");
            }
        }
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
        if (Type.GetType("system.type", false, true) != Type.GetType("System.Type")
                || Type.GetType("system.type", false, false) != null
                || Type.GetType("system.invalidoperationexception", false, true)
                    != Type.GetType("System.InvalidOperationException")
                || Type.GetType("system.invalidoperationexception", false, false) != null
                || Type.GetType("system.string&[]", false, false) != null) {
            throw new AssertionError("Selected case-sensitive type boundaries changed");
        }
        try {
            Type.GetType("system.string&[]", false, true);
            throw new AssertionError("Insensitive invalid nested type accepted");
        } catch (TypeLoadException expected) {
            // Selected pinned error type.
        }
        if (Type.GetType("System.String, System.Private.CoreLib") != string
                || Type.GetType("System.Int32, System.Private.CoreLib") != integer
                || Type.GetType("System.String, mscorlib") != string
                || Type.GetType("System.String, NotAnAssembly") != null) {
            throw new AssertionError("Selected assembly-qualified lookup changed");
        }
        if (Type.GetType("System.String, system.private.corelib") != string
                || Type.GetType("System.String, SYSTEM.PRIVATE.CORELIB") != string
                || Type.GetType("System.String, MSCORLIB") != string
                || Type.GetType("System.String, MsCoRlIb") != string
                || Type.GetType("System.String, UnknownAssembly") != null) {
            throw new AssertionError("Selected assembly-name casing changed");
        }
        if (Type.GetType("System.String,  System.Private.CoreLib  ") != string
                || Type.GetType("System.String, \"System.Private.CoreLib\"") != string
                || Type.GetType("System.String, System.Private.CoreLib.dll") != string
                || Type.GetType("System.String,  mscorlib  ") != string
                || Type.GetType("System.String, System. Private.CoreLib") != null
                || Type.GetType("System.String, .System.Private.CoreLib") != null
                || Type.GetType("System.String, , Version=10.0.0.0") != null) {
            throw new AssertionError("Selected assembly simple-name boundary changed");
        }
        if (Type.GetType("System.String, \"mscorlib\"") != string
                || Type.GetType("System.String, SYSTEM.PRIVATE.CORELIB.DLL") != string
                || Type.GetType("System.String, mscorlib.dll") != null
                || Type.GetType("System.String, \"mscorlib.dll\"") != null
                || Type.GetType("System.String, mscorlib.exe") != null
                || Type.GetType("System.String, \"mscorlib.dll\", Version=4.0.0.0") != null) {
            throw new AssertionError("Selected legacy assembly alias boundary changed");
        }
        for (String missingAssembly : new String[] {
                "System.String, mscorlib.dll", "System.String, System. Private.CoreLib"}) {
            try {
                Type.GetType(missingAssembly, true);
                throw new AssertionError("Missing assembly accepted with throwOnError");
            } catch (FileNotFoundException expected) {
                // Selected missing-assembly error.
            }
        }
        try {
            Type.GetType("System.String, , Version=10.0.0.0", true);
            throw new AssertionError("Empty assembly name accepted with throwOnError");
        } catch (ArgumentException expected) {
            if (!"typeName@15".equals(expected.get_ParamName())) {
                throw new AssertionError("Empty assembly position changed", expected);
            }
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib, Version=banana", true);
            throw new AssertionError("Invalid version accepted with throwOnError");
        } catch (FileLoadException expected) {
            // Selected malformed-assembly error.
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib, Culture=123", true);
            throw new AssertionError("Numeric culture accepted with throwOnError");
        } catch (CultureNotFoundException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Numeric culture parameter changed", expected);
            }
        }
        if (Type.GetType("System.String, System.Private.CoreLib, UnknownAttr=foo", true) != string) {
            throw new AssertionError("Unknown assembly attribute rejected with throwOnError");
        }
        for (String validWhitespace : new String[] {
                "Version= 10.0.0.0 ", "Culture= neutral ",
                "PublicKeyToken= 7cec85d7bea7798e ", "UnknownAttr=foo bar"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + validWhitespace) != string) {
                throw new AssertionError("Selected outer/value whitespace rejected: " + validWhitespace);
            }
        }
        for (String invalidWhitespace : new String[] {
                "Version=10.0 .0.0", "PublicKeyToken=7cec85d7 bea7798e"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + invalidWhitespace);
                throw new AssertionError("Invalid inner whitespace accepted: " + invalidWhitespace);
            } catch (FileLoadException expected) {
                // Selected pinned malformed value.
            }
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib, Culture=en US");
            throw new AssertionError("Invalid inner culture space accepted");
        } catch (CultureNotFoundException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Invalid culture parameter changed", expected);
            }
        }
        for (String validQuoted : new String[] {
                "Culture=\"\"", "UnknownAttr=\"\"", "UnknownAttr=\"foo,bar\""}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + validQuoted) != string) {
                throw new AssertionError("Selected quoted value rejected: " + validQuoted);
            }
        }
        for (String malformedQuote : new String[] {"Culture=\"neutral", "Culture=neutral\""}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + malformedQuote);
                throw new AssertionError("Malformed quote accepted: " + malformedQuote);
            } catch (FileLoadException expected) {
                // Selected pinned malformed quote.
            }
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib, Culture=\"en US\"");
            throw new AssertionError("Invalid quoted culture accepted");
        } catch (CultureNotFoundException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Quoted culture parameter changed", expected);
            }
        }
        for (String quotedUnknown : new String[] {"UnknownAttr=\"a,b,c\"", "UnknownAttr=\"a=b\""}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + quotedUnknown) != string) {
                throw new AssertionError("Selected quoted unknown value rejected: " + quotedUnknown);
            }
        }
        for (String invalidQuoted : new String[] {
                "Version=\"1,2\"", "PublicKeyToken=\"01234567,89abcdef\""}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + invalidQuoted);
                throw new AssertionError("Invalid quoted value accepted: " + invalidQuoted);
            } catch (FileLoadException expected) {
                // Selected pinned format error.
            }
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib, Culture=\"en,US\"");
            throw new AssertionError("Invalid comma culture accepted");
        } catch (CultureNotFoundException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Comma culture parameter changed", expected);
            }
        }
        for (String escapedUnknown : new String[] {
                "UnknownAttr=\"a\\\"b\"", "UnknownAttr=\"a\\\\b\""}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + escapedUnknown) != string) {
                throw new AssertionError("Selected escaped unknown value rejected: " + escapedUnknown);
            }
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib, UnknownAttr=\"a\"\"b\"");
            throw new AssertionError("Doubled quoted value accepted");
        } catch (FileLoadException expected) {
            // Selected pinned quote syntax error.
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib, Culture=\"en\\\"US\"");
            throw new AssertionError("Escaped quote culture accepted");
        } catch (CultureNotFoundException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Escaped quote culture parameter changed", expected);
            }
        }
        for (String keyForm : new String[] {
                " Version  =10.0.0.0", "Culture  =neutral", "PublicKeyToken =null",
                "Unknown Attr=foo", "Unknown.Attr=foo", "Ver-sion=10.0.0.0"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + keyForm) != string) {
                throw new AssertionError("Selected assembly attribute key rejected: " + keyForm);
            }
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib, =foo");
            throw new AssertionError("Empty assembly attribute key accepted");
        } catch (FileLoadException expected) {
            // Selected pinned empty-key error.
        }
        for (String unknownValue : new String[] {
                "UnknownAttr=foo:bar", "UnknownAttr=foo/bar", "UnknownAttr=foo;bar",
                "UnknownAttr=foo?bar", "UnknownAttr=foo, unknownattr=bar"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + unknownValue) != string) {
                throw new AssertionError("Selected unknown attribute value rejected: " + unknownValue);
            }
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib, UnknownAttr=foo=bar");
            throw new AssertionError("Unquoted equals accepted in unknown attribute");
        } catch (FileLoadException expected) {
            // Selected pinned separator error.
        }
        for (String architecture : new String[] {"MSIL", "X86", "Amd64"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, ProcessorArchitecture=" + architecture)
                    != string) {
                throw new AssertionError("Selected processor architecture rejected: " + architecture);
            }
        }
        for (String invalidArchitecture : new String[] {
                "ProcessorArchitecture=None", "ProcessorArchitecture=xyz",
                "ProcessorArchitecture=MSIL, ProcessorArchitecture=X86"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + invalidArchitecture);
                throw new AssertionError("Invalid processor architecture accepted: " + invalidArchitecture);
            } catch (FileLoadException expected) {
                // Selected pinned identity error.
            }
        }
        for (String retargetable : new String[] {"Yes", "No"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, Retargetable=" + retargetable)
                    != string) {
                throw new AssertionError("Selected Retargetable value rejected: " + retargetable);
            }
        }
        for (String invalidRetargetable : new String[] {
                "Retargetable=true", "Retargetable=false", "Retargetable=1",
                "Retargetable=Yes, Retargetable=No"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + invalidRetargetable);
                throw new AssertionError("Invalid Retargetable accepted: " + invalidRetargetable);
            } catch (FileLoadException expected) {
                // Selected pinned identity error.
            }
        }
        if (Type.GetType("System.String, System.Private.CoreLib, ContentType=WindowsRuntime") != string) {
            throw new AssertionError("Selected WindowsRuntime ContentType rejected");
        }
        for (String invalidContentType : new String[] {
                "ContentType=Default", "contenttype=default", "ContentType=xyz",
                "ContentType=1", "ContentType=Default, ContentType=WindowsRuntime"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + invalidContentType);
                throw new AssertionError("Invalid ContentType accepted: " + invalidContentType);
            } catch (FileLoadException expected) {
                // Selected pinned identity error.
            }
        }
        if (Type.GetType("System.String, System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, PublicKeyToken=null, ProcessorArchitecture=MSIL, Retargetable=No, ContentType=WindowsRuntime") != string) {
            throw new AssertionError("Selected combined assembly identity rejected");
        }
        for (String malformedCombination : new String[] {
                "System.String, System.Private.CoreLib, Version=banana, Culture=123",
                "System.String, System.Private.CoreLib, Culture=123, Version=banana",
                "System.String, Missing.Assembly, Version=banana",
                "System.String, System.Private.CoreLib, ContentType=Default, Version=banana"}) {
            try {
                Type.GetType(malformedCombination);
                throw new AssertionError("Malformed combined identity accepted: " + malformedCombination);
            } catch (FileLoadException expected) {
                // Selected malformed attribute error precedes culture or binder errors.
            }
        }
        try {
            Type.GetType("System.String, Missing.Assembly, Version=banana", true);
            throw new AssertionError("Malformed unknown assembly accepted with throwOnError");
        } catch (FileLoadException expected) {
            // Selected malformed-attribute precedence.
        }
        if (Type.GetType("System.String, Missing.Assembly, Version=10.0.0.0") != null
                || Type.GetType("System.String, Missing.Assembly, UnknownAttr=foo") != null) {
            throw new AssertionError("Unknown assembly with valid attributes resolved");
        }
        for (String missingWithValidAttribute : new String[] {
                "Version=10.0.0.0", "UnknownAttr=foo"}) {
            try {
                Type.GetType("System.String, Missing.Assembly, " + missingWithValidAttribute, true);
                throw new AssertionError("Missing assembly accepted with attribute");
            } catch (FileNotFoundException expected) {
                // Selected missing-assembly result after valid attribute parsing.
            }
        }
        for (String invalidUnknownAssembly : new String[] {
                "PublicKeyToken=xyz", "Version=1.2.3.4, Version=2.3.4.5"}) {
            try {
                Type.GetType("System.String, Missing.Assembly, " + invalidUnknownAssembly);
                throw new AssertionError("Malformed unknown-assembly identity accepted");
            } catch (FileLoadException expected) {
                // Selected malformed-attribute result precedes missing assembly.
            }
        }
        try {
            Type.GetType("System.String, Missing.Assembly, Culture=123");
            throw new AssertionError("Numeric culture accepted under missing assembly");
        } catch (CultureNotFoundException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Missing-assembly culture parameter changed", expected);
            }
        }
        for (String acceptedAlias : new String[] {
                "processorarchitecture=msil", "RETARGETABLE=YES",
                "contenttype=windowsruntime", "PublicKey=null", "CultureInfo=neutral"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + acceptedAlias) != string) {
                throw new AssertionError("Selected assembly attribute alias rejected: " + acceptedAlias);
            }
        }
        for (String invalidAlias : new String[] {
                "PublicKey=xyz", "Retargetable=Yes, retargetable=No"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + invalidAlias);
                throw new AssertionError("Invalid assembly attribute alias accepted: " + invalidAlias);
            } catch (FileLoadException expected) {
                // Selected pinned identity error.
            }
        }
        for (String publicKey : new String[] {
                "00", "0011", "0011223344556677", "00112233445566778899aabbccddeeff", "NULL"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, PublicKey=" + publicKey) != string) {
                throw new AssertionError("Selected PublicKey value rejected: " + publicKey);
            }
        }
        for (String invalidPublicKey : new String[] {"0", "gg"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, PublicKey=" + invalidPublicKey);
                throw new AssertionError("Invalid PublicKey accepted: " + invalidPublicKey);
            } catch (FileLoadException expected) {
                // Selected pinned PublicKey parse error.
            }
        }
        for (String conflictingKeys : new String[] {
                "PublicKey=null, PublicKeyToken=null", "PublicKey=00, PublicKeyToken=null",
                "PublicKeyToken=null, PublicKey=00",
                "PublicKey=00, PublicKeyToken=7cec85d7bea7798e",
                "PublicKeyToken=null, PublicKey=xyz", "PublicKeyToken=xyz, PublicKey=00"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + conflictingKeys);
                throw new AssertionError("Conflicting key and token accepted: " + conflictingKeys);
            } catch (FileLoadException expected) {
                // Selected pinned mutually exclusive identity attributes.
            }
        }
        for (String acceptedCulture : new String[] {
                "Neutral", "NEUTRAL", "en-us", "EN-US", "iv"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, Culture=" + acceptedCulture) != string) {
                throw new AssertionError("Selected culture name rejected: " + acceptedCulture);
            }
        }
        for (String invalidCultureName : new String[] {"invariant", "null"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, Culture=" + invalidCultureName);
                throw new AssertionError("Invalid culture name accepted: " + invalidCultureName);
            } catch (CultureNotFoundException expected) {
                if (!"name".equals(expected.get_ParamName())) {
                    throw new AssertionError("Culture name parameter changed", expected);
                }
            }
        }
        if (Type.GetType("System.String, System.Private.CoreLib, Culture=en_US") != string) {
            throw new AssertionError("Selected underscore culture rejected");
        }
        for (String invalidSeparator : new String[] {
                "en.US", "en--US", "en-", "-US", "en/US", "en@US"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, Culture=" + invalidSeparator);
                throw new AssertionError("Invalid culture separator accepted: " + invalidSeparator);
            } catch (CultureNotFoundException expected) {
                if (!"name".equals(expected.get_ParamName())) {
                    throw new AssertionError("Culture separator parameter changed", expected);
                }
            }
        }
        for (String acceptedLocale : new String[] {"fr-CH", "zh-Hant", "ja-JP"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, Culture=" + acceptedLocale) != string) {
                throw new AssertionError("Selected locale rejected: " + acceptedLocale);
            }
        }
        for (String invalidLocale : new String[] {"123", "١٢٣", "é"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, Culture=" + invalidLocale);
                throw new AssertionError("Invalid locale accepted: " + invalidLocale);
            } catch (CultureNotFoundException expected) {
                if (!"name".equals(expected.get_ParamName())) {
                    throw new AssertionError("Unicode locale parameter changed", expected);
                }
            }
        }
        for (String acceptedVersion : new String[] {
                "0001.0002", "0.0", "65534.65534", "0000001.0"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, Version=" + acceptedVersion) != string) {
                throw new AssertionError("Selected Version components rejected: " + acceptedVersion);
            }
        }
        for (String invalidVersion : new String[] {"65535.0", "2147483648.0"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, Version=" + invalidVersion);
                throw new AssertionError("Invalid Version component accepted: " + invalidVersion);
            } catch (FileLoadException expected) {
                // Selected pinned component overflow.
            }
        }
        if (Type.GetType("System.String, System.Private.CoreLib, Version=1.2.3.4") != string) {
            throw new AssertionError("Selected four-component Version rejected");
        }
        for (String invalidVersionGrammar : new String[] {
                "+1.2", "-1.2", "1 .2", "1. 2", "1.2.3.4.5", "1..2"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, Version=" + invalidVersionGrammar);
                throw new AssertionError("Invalid Version grammar accepted: " + invalidVersionGrammar);
            } catch (FileLoadException expected) {
                // Selected pinned Version syntax error.
            }
        }
        for (String acceptedOrdering : new String[] {
                "ContentType=WindowsRuntime, Retargetable=Yes",
                "Retargetable=Yes, ContentType=WindowsRuntime",
                "ProcessorArchitecture=X86, Retargetable=Yes",
                "Retargetable=No, Version=1.2"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + acceptedOrdering) != string) {
                throw new AssertionError("Selected known-attribute order rejected: " + acceptedOrdering);
            }
        }
        for (String invalidOrdering : new String[] {
                "Culture=123, PublicKeyToken=xyz", "PublicKeyToken=xyz, Culture=123"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + invalidOrdering);
                throw new AssertionError("Malformed known-attribute order accepted: " + invalidOrdering);
            } catch (FileLoadException expected) {
                // Selected parse error precedes invalid culture.
            }
        }
        for (String distinctAlias : new String[] {
                "Culture=neutral, CultureInfo=neutral", "Version=1.2, Ver-sion=3.4"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + distinctAlias) != string) {
                throw new AssertionError("Selected distinct alias rejected: " + distinctAlias);
            }
        }
        for (String duplicateKnownKey : new String[] {
                "PublicKeyToken=null, publickeytoken=null",
                "ProcessorArchitecture=MSIL, processorarchitecture=X86",
                "PublicKey=00, publickey=11",
                "ContentType=WindowsRuntime, contenttype=WindowsRuntime"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + duplicateKnownKey);
                throw new AssertionError("Duplicate known key accepted: " + duplicateKnownKey);
            } catch (FileLoadException expected) {
                // Selected case-insensitive duplicate key error.
            }
        }
        for (String acceptedSimpleName : new String[] {
                "  \"System.Private.CoreLib\"  ",
                "\"System.Private.CoreLib.dll\"", "'System.Private.CoreLib'"}) {
            if (Type.GetType("System.String, " + acceptedSimpleName) != string) {
                throw new AssertionError("Selected simple-name quoting rejected: " + acceptedSimpleName);
            }
        }
        for (String missingSimpleName : new String[] {
                "\" System.Private.CoreLib \"", "System.Private.CoreLib .dll",
                "\"Missing.Assembly\""}) {
            if (Type.GetType("System.String, " + missingSimpleName) != null) {
                throw new AssertionError("Selected missing simple name resolved: " + missingSimpleName);
            }
        }
        for (String unbalancedName : new String[] {
                "\"System.Private.CoreLib", "System.Private.CoreLib\"",
                "'System.Private.CoreLib", "System.Private.CoreLib'"}) {
            try {
                Type.GetType("System.String, " + unbalancedName);
                throw new AssertionError("Unbalanced assembly name accepted: " + unbalancedName);
            } catch (FileLoadException expected) {
                // Selected pinned quote parse error.
            }
        }
        if (Type.GetType("System.String, '\"System.Private.CoreLib\"'") != null
                || Type.GetType("System.String, \"'System.Private.CoreLib'\"") != null) {
            throw new AssertionError("Nested assembly name quotes resolved");
        }
        if (Type.GetType("System.String, \"System.Private.CoreLib,Extra\"") != string
                || Type.GetType("System.String, System.Private.CoreLib, Version=1.2") != string
                || Type.GetType("System.String, \"System.Private.CoreLib=Extra\"") != null
                || Type.GetType("System.String, System.Private.CoreLib;Extra") != null
                || Type.GetType("System.String, System.Private.CoreLib/Extra") != null) {
            throw new AssertionError("Selected assembly name punctuation changed");
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib=Extra");
            throw new AssertionError("Unquoted equals assembly name accepted");
        } catch (FileLoadException expected) {
            // Selected pinned assembly name parse error.
        }
        if (Type.GetType("System.String, SYSTEM.PRIVATE.CORELIB") != string
                || Type.GetType("System.String, SyStEm.PrIvAtE.CoReLiB") != string
                || Type.GetType("System.String, System.Prıvate.CoreLib") != null
                || Type.GetType("System.String, System.Prİvate.CoreLib") != null
                || Type.GetType("System.String, Systém.Private.CoreLib") != null
                || Type.GetType("System.String, ｍscorlib") != null) {
            throw new AssertionError("Selected assembly Unicode casing changed");
        }
        for (String unicodeKey : new String[] {
                "Versıon=banana", "VERSİON=banana", "PublıcKeyToken=xyz",
                "Retargetablé=blah", "Versıon=banana, Version=1.2",
                "Version=1.2, VERSİON=banana"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + unicodeKey) != string) {
                throw new AssertionError("Selected Unicode attribute key rejected: " + unicodeKey);
            }
        }
        if (Type.GetType("System.String, System.Private.CoreLib, ContentType=WINDOWSRUNTIME") != string
                || Type.GetType("System.String, System.Private.CoreLib, UnknownAttr=é") != string) {
            throw new AssertionError("Selected ASCII/unknown Unicode value rejected");
        }
        for (String unicodeKnownValue : new String[] {
                "Retargetable=Yés", "ProcessorArchitecture=MSİL",
                "ContentType=WındowsRuntime", "PublicKeyToken=nüll"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + unicodeKnownValue);
                throw new AssertionError("Unicode known value accepted: " + unicodeKnownValue);
            } catch (FileLoadException expected) {
                // Selected pinned ASCII-only identity value.
            }
        }
        for (String coreLibAlias : new String[] {
                "System.Private.CoreLib.DLL", "system.private.corelib.dll",
                "\"SYSTEM.PRIVATE.CORELIB.DLL\"", "'System.Private.CoreLib.dll'"}) {
            if (Type.GetType("System.String, " + coreLibAlias) != string) {
                throw new AssertionError("Selected CoreLib suffix alias rejected: " + coreLibAlias);
            }
        }
        for (String legacySuffix : new String[] {"mscorlib.DLL", "'mscorlib.dll'"}) {
            if (Type.GetType("System.String, " + legacySuffix) != null) {
                throw new AssertionError("Selected legacy suffix unexpectedly resolved: " + legacySuffix);
            }
        }
        for (String quotedNameWithAttribute : new String[] {
                "\"System.Private.CoreLib\", Version=1.2",
                "'System.Private.CoreLib', Version=1.2",
                "\"System.Private.CoreLib.dll\", Version=1.2",
                "\"System.Private.CoreLib\", UnknownAttr=foo",
                "\"System.Private.CoreLib,Extra\", Version=1.2"}) {
            if (Type.GetType("System.String, " + quotedNameWithAttribute) != string) {
                throw new AssertionError("Selected quoted name attribute rejected: " + quotedNameWithAttribute);
            }
        }
        try {
            Type.GetType("System.String, \"System.Private.CoreLib\", Version=banana");
            throw new AssertionError("Malformed attribute after quoted name accepted");
        } catch (FileLoadException expected) {
            // Selected pinned malformed identity error.
        }
        for (String quotedPunctuation : new String[] {
                "'System.Private.CoreLib,Extra'",
                "\"System.Private.CoreLib,Extra\", UnknownAttr=foo",
                "\"System.Private.CoreLib,Extra\", PublicKeyToken=null"}) {
            if (Type.GetType("System.String, " + quotedPunctuation) != string) {
                throw new AssertionError("Selected quoted punctuation rejected: " + quotedPunctuation);
            }
        }
        for (String missingQuotedPunctuation : new String[] {
                "\"System.Private.CoreLib=Extra\", Version=1.2",
                "'System.Private.CoreLib=Extra'"}) {
            if (Type.GetType("System.String, " + missingQuotedPunctuation) != null) {
                throw new AssertionError("Selected quoted equals resolved: " + missingQuotedPunctuation);
            }
        }
        try {
            Type.GetType("System.String, \"System.Private.CoreLib,Extra\", Version=banana");
            throw new AssertionError("Malformed Version after quoted comma accepted");
        } catch (FileLoadException expected) {
            // Selected pinned malformed attribute error.
        }
        for (String escapedName : new String[] {
                "\"System.Private.CoreLib\\,Extra\"",
                "'System.Private.CoreLib\\,Extra'",
                "System.Private.CoreLib\\,Extra"}) {
            if (Type.GetType("System.String, " + escapedName) != string) {
                throw new AssertionError("Selected escaped comma name rejected: " + escapedName);
            }
        }
        if (Type.GetType("System.String, \"System.Private.CoreLib\\=Extra\"") != null
                || Type.GetType("System.String, \"System.Private.CoreLib\\\\Extra\"") != null) {
            throw new AssertionError("Selected escaped punctuation name resolved");
        }
        for (String escapedNameAttribute : new String[] {
                "System.Private.CoreLib\\,Extra, Version=1.2",
                "\"System.Private.CoreLib\\,Extra\", Version=1.2",
                "'System.Private.CoreLib\\,Extra', Version=1.2",
                "System.Private.CoreLib\\,Extra, UnknownAttr=foo"}) {
            if (Type.GetType("System.String, " + escapedNameAttribute) != string) {
                throw new AssertionError("Selected escaped name attribute rejected: " + escapedNameAttribute);
            }
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib\\,Extra, Version=banana");
            throw new AssertionError("Invalid Version after escaped comma accepted");
        } catch (FileLoadException expected) {
            // Selected pinned malformed attribute result.
        }
        for (String escapedQuoteName : new String[] {
                "\"System.Private.CoreLib\\\"Extra\"",
                "'System.Private.CoreLib\\'Extra'",
                "System.Private.CoreLib\\\"",
                "System.Private.CoreLib\\'",
                "\"System.Private.CoreLib\\\"Extra\", Version=1.2",
                "'System.Private.CoreLib\\'Extra', Version=1.2"}) {
            if (Type.GetType("System.String, " + escapedQuoteName) != null) {
                throw new AssertionError("Escaped quote name resolved: " + escapedQuoteName);
            }
        }
        for (String invalidEvenSeparator : new String[] {
                "System.Private.CoreLib\\\\,Extra",
                "System.Private.CoreLib\\\\\\\\,Extra"}) {
            try {
                Type.GetType("System.String, " + invalidEvenSeparator);
                throw new AssertionError("Even escape run accepted: " + invalidEvenSeparator);
            } catch (FileLoadException expected) {
                // A comma after an even run separates an invalid attribute.
            }
        }
        for (String unknownEscapedName : new String[] {
                "System.Private.CoreLib\\\\\\,Extra",
                "\"System.Private.CoreLib\\\\,Extra\"",
                "\"System.Private.CoreLib\\\\\\,Extra\"",
                "'System.Private.CoreLib\\\\,Extra'"}) {
            if (Type.GetType("System.String, " + unknownEscapedName) != null) {
                throw new AssertionError("Backslash-run name resolved: " + unknownEscapedName);
            }
        }
        for (String invalidQuoteRun : new String[] {
                "\"System.Private.CoreLib\\\\\\\"",
                "'System.Private.CoreLib\\\\\\'",
                "System.Private.CoreLib\\\\\""}) {
            try {
                Type.GetType("System.String, " + invalidQuoteRun);
                throw new AssertionError("Invalid quote run accepted: " + invalidQuoteRun);
            } catch (FileLoadException expected) {
                // Selected unbalanced quote boundary.
            }
        }
        for (String unknownQuoteRun : new String[] {
                "\"System.Private.CoreLib\\\\\"",
                "'System.Private.CoreLib\\\\'",
                "System.Private.CoreLib\\\\\\\""}) {
            if (Type.GetType("System.String, " + unknownQuoteRun) != null) {
                throw new AssertionError("Quote run resolved: " + unknownQuoteRun);
            }
        }
        for (String validAttributeRun : new String[] {
                "UnknownAttr=\"a\\\\\", Version=1.2",
                "UnknownAttr=a\\\\, Version=1.2",
                "UnknownAttr=\"a\\\\,b\", Version=1.2",
                "UnknownAttr=\"a\\\\\\,b\", Version=1.2"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + validAttributeRun) != string) {
                throw new AssertionError("Valid attribute escape run rejected: " + validAttributeRun);
            }
        }
        for (String invalidAttributeRun : new String[] {
                "UnknownAttr=\"a\\\\\\\", Version=1.2",
                "UnknownAttr=a\\\\\\, Version=1.2"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + invalidAttributeRun);
                throw new AssertionError("Invalid attribute escape run accepted: " + invalidAttributeRun);
            } catch (FileLoadException expected) {
                // Selected quote or separator escape parity.
            }
        }
        for (String unresolvedName : new String[] {
                "\"Missing\\\"Assembly\", Version=1.2",
                "Missing\\,Assembly, Version=1.2"}) {
            if (Type.GetType("System.String, " + unresolvedName) != null) {
                throw new AssertionError("Missing escaped assembly resolved: " + unresolvedName);
            }
        }
        for (String invalidMissingName : new String[] {
                "\"Missing\\\"Assembly\", Version=banana",
                "Missing\\,Assembly, Version=banana",
                "Missing\\\\, Version=banana"}) {
            try {
                Type.GetType("System.String, " + invalidMissingName);
                throw new AssertionError("Invalid attribute ignored for missing assembly: " + invalidMissingName);
            } catch (FileLoadException expected) {
                // Attribute validation precedes selected assembly resolution.
            }
        }
        try {
            Type.GetType("System.String, Missing\\\\, Culture=123");
            throw new AssertionError("Invalid culture ignored for missing assembly");
        } catch (CultureNotFoundException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Missing-assembly culture parameter changed", expected);
            }
        }
        for (String missingEscapedName : new String[] {
                "\"Missing\\\"Assembly\", Version=1.2",
                "Missing\\,Assembly, Version=1.2"}) {
            try {
                Type.GetType("System.String, " + missingEscapedName, true);
                throw new AssertionError("Missing escaped assembly accepted: " + missingEscapedName);
            } catch (FileNotFoundException expected) {
                // Selected throwOnError assembly binding failure.
            }
        }
        for (String invalidEscapedVersion : new String[] {
                "\"Missing\\\"Assembly\", Version=banana",
                "Missing\\,Assembly, Version=banana"}) {
            try {
                Type.GetType("System.String, " + invalidEscapedVersion, true);
                throw new AssertionError("Invalid escaped Version accepted: " + invalidEscapedVersion);
            } catch (FileLoadException expected) {
                // Attribute syntax precedes assembly binding with throwOnError.
            }
        }
        try {
            Type.GetType("System.String, Missing\\\\, Culture=123", true);
            throw new AssertionError("Invalid culture accepted with throwOnError");
        } catch (CultureNotFoundException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Escaped culture parameter changed", expected);
            }
        }
        if (Type.GetType("System.String, System.Private.CoreLib\\,Extra, Version=1.2", true) != string) {
            throw new AssertionError("Escaped CoreLib alias rejected with throwOnError");
        }
        for (String mixedInvalidIdentity : new String[] {
                "\"Missing\\\"Assembly\", Culture=123, Version=banana",
                "\"Missing\\\"Assembly\", Version=banana, Culture=123",
                "Missing\\,Assembly, UnknownAttr=foo=bar, Culture=123",
                "System.Private.CoreLib\\,Extra, Culture=123, Version=banana",
                "Missing\\\\, Version=banana, Culture=123",
                "Missing\\,Assembly, Culture=123, UnknownAttr=foo=bar"}) {
            try {
                Type.GetType("System.String, " + mixedInvalidIdentity);
                throw new AssertionError("Mixed invalid identity accepted: " + mixedInvalidIdentity);
            } catch (FileLoadException expected) {
                // Syntactic identity error precedes deferred culture validation.
            }
        }
        try {
            Type.GetType("System.String, UnknownAssembly", true);
            throw new AssertionError("Unknown assembly accepted");
        } catch (FileNotFoundException expected) {
            // Selected pinned error type.
        }
        if (Type.GetType("System.String, System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e") != string
                || Type.GetType("System.String, System.Private.CoreLib, Version=99.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e") != string
                || Type.GetType("System.String, System.Private.CoreLib, Version=10.0.0.0, Culture=en-US, PublicKeyToken=7cec85d7bea7798e") != string
                || Type.GetType("System.String, System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, PublicKeyToken=null") != string
                || Type.GetType("System.String, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089") != string
                || Type.GetType("System.String, System.Private.CoreLib, Version=99.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e", true) != string) {
            throw new AssertionError("Selected assembly identity lookup changed");
        }
        if (Type.GetType("System.String, System.Private.CoreLib, UnknownAttr=foo") != string
                || Type.GetType("System.IO.FileLoadException") == null) {
            throw new AssertionError("Selected unknown assembly attribute behavior changed");
        }
        for (String invalid : new String[] {
                "Version=banana", "Culture=", "PublicKeyToken=xyz",
                "Version=10.0.0.0, Version=11.0.0.0", "UnknownAttr=",
                "Culture=neutral, Culture=en-US", "Version=10", "Version=1.2.3.4.5",
                "Version=10.0.0.0,", ", Version=10.0.0.0", "", "UnknownAttr=foo=bar",
                "Version=65535.0.0.0", "Version=65536.0.0.0", "Version=-1.0.0.0"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + invalid);
                throw new AssertionError("Invalid assembly attribute accepted: " + invalid);
            } catch (FileLoadException expected) {
                // Pinned malformed-identity error, including with throwOnError=false.
            }
        }
        for (String invalidToken : new String[] {
                "123456789abcdef", "123456789abcdef01", "gggggggggggggggg"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, PublicKeyToken=" + invalidToken);
                throw new AssertionError("Invalid token accepted: " + invalidToken);
            } catch (FileLoadException expected) {
                // Selected pinned token format error.
            }
        }
        for (String valid : new String[] {
                "version=10.0.0.0", "CULTURE=neutral", "Publickeytoken=null",
                "Version = 10.0.0.0", " Version=10.0.0.0", "Culture=\"neutral\"",
                "Version=\"10.0.0.0\"", "UnknownAttr=\"foo\"",
                "PublicKeyToken=\"null\"", "Version=1.2", "Version=1.2.3",
                "Culture=en_US", "Culture=not-a-real-culture"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + valid) != string) {
                throw new AssertionError("Selected assembly attribute spelling rejected: " + valid);
            }
        }
        for (String validToken : new String[] {
                "7CEC85D7BEA7798E", "0000000000000000", "NULL",
                "\"7cec85d7bea7798e\""}) {
            if (Type.GetType("System.String, System.Private.CoreLib, PublicKeyToken=" + validToken) != string) {
                throw new AssertionError("Selected public key token rejected: " + validToken);
            }
        }
        for (String validAttributes : new String[] {
                "PublicKeyToken=null, Culture=neutral, Version=10.0.0.0",
                "UnknownAttr=foo, Version=10.0.0.0",
                "Version=10.0.0.0, UnknownAttr=foo",
                "UnknownAttr=foo, UnknownAttr=bar"}) {
            if (Type.GetType("System.String, System.Private.CoreLib, " + validAttributes) != string) {
                throw new AssertionError("Selected attribute order rejected: " + validAttributes);
            }
        }
        for (String duplicate : new String[] {
                "PublicKeyToken=null, PublicKeyToken=null",
                "Version=10.0.0.0, version=11.0.0.0"}) {
            try {
                Type.GetType("System.String, System.Private.CoreLib, " + duplicate);
                throw new AssertionError("Duplicate known attribute accepted: " + duplicate);
            } catch (FileLoadException expected) {
                // Selected pinned duplicate error.
            }
        }
        try {
            Type.GetType("System.String, System.Private.CoreLib, Culture=123");
            throw new AssertionError("Numeric culture accepted");
        } catch (CultureNotFoundException expected) {
            if (!"name".equals(expected.get_ParamName())
                    || !"123".equals(expected.get_InvalidCultureName())
                    || Type.GetType("System.Globalization.CultureNotFoundException") == null) {
                throw new AssertionError("Selected culture error identity changed", expected);
            }
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
        for (Type selectedDictionary : new Type[] {dictionary, dictionaryStringInt,
                dictionary.MakeGenericType(new Type[] {integer, string}),
                dictionary.MakeGenericType(new Type[] {string, string}),
                dictionary.MakeGenericType(new Type[] {integer, integer})}) {
            if (Type.GetType(selectedDictionary.get_AssemblyQualifiedName()) != selectedDictionary) {
                throw new AssertionError("Dictionary assembly-qualified round trip changed");
            }
            String lowerDictionary = selectedDictionary.get_AssemblyQualifiedName()
                    .toLowerCase(java.util.Locale.ROOT);
            if (Type.GetType(lowerDictionary, false, false) != null
                    || Type.GetType(lowerDictionary, false, true) != selectedDictionary) {
                throw new AssertionError("Dictionary qualified case lookup changed");
            }
        }
        Type listInt = definition.MakeGenericType(new Type[] {integer});
        for (Type nestedGeneric : new Type[] {
                definition.MakeGenericType(new Type[] {first}),
                dictionary.MakeGenericType(new Type[] {string, listInt}),
                dictionary.MakeGenericType(new Type[] {first, listInt})}) {
            if (Type.GetType(nestedGeneric.get_AssemblyQualifiedName()) != nestedGeneric) {
                throw new AssertionError("Nested generic assembly-qualified round trip changed");
            }
            String lowerNested = nestedGeneric.get_AssemblyQualifiedName()
                    .toLowerCase(java.util.Locale.ROOT);
            if (Type.GetType(lowerNested, false, false) != null
                    || Type.GetType(lowerNested, false, true) != nestedGeneric) {
                throw new AssertionError("Nested generic qualified case lookup changed");
            }
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
        if (Type.GetType("System.Object").get_IsSZArray()
                || !Type.GetType("System.String[]").get_IsSZArray()
                || !jagged.get_IsSZArray()
                || Type.GetType("System.String[*]").get_IsSZArray()
                || rectangular.get_IsSZArray() || rankThree.get_IsSZArray()
                || !listArray.get_IsSZArray()) {
            throw new AssertionError("Selected vector array flags changed");
        }
        if (Type.GetType("System.Object").get_IsVariableBoundArray()
                || Type.GetType("System.String[]").get_IsVariableBoundArray()
                || jagged.get_IsVariableBoundArray()
                || !Type.GetType("System.String[*]").get_IsVariableBoundArray()
                || !rectangular.get_IsVariableBoundArray()
                || !rankThree.get_IsVariableBoundArray()
                || listArray.get_IsVariableBoundArray()) {
            throw new AssertionError("Selected variable-bound array flags changed");
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
        if (Type.GetType("System.Object").get_HasElementType()
                || integer.get_HasElementType() || definition.get_HasElementType()
                || first.get_HasElementType()
                || !Type.GetType("System.String[]").get_HasElementType()
                || !rectangular.get_HasElementType()
                || !Type.GetType("System.String[*]").get_HasElementType()
                || !byReference.get_HasElementType() || !pointer.get_HasElementType()
                || rectangular.GetElementType() != string
                || byReference.GetElementType() != string
                || pointer.GetElementType() != string) {
            throw new AssertionError("Selected element type flags changed");
        }
        for (int rank : new int[] {1, 2}) {
            try {
                if (rank == 1) {
                    byReference.MakeArrayType();
                } else {
                    byReference.MakeArrayType(rank);
                }
                throw new AssertionError("Array of by-reference type accepted");
            } catch (TypeLoadException expected) {
                // Selected pinned error type.
            }
        }
        if (!"System.String*[]".equals(pointer.MakeArrayType().get_FullName())
                || !"System.String*&".equals(pointer.MakeByRefType().get_FullName())
                || Type.GetType("System.String[]").MakeByRefType()
                    != Type.GetType("System.String[]&")) {
            throw new AssertionError("Selected pointer/array construction changed");
        }
        if (Type.GetType("System.String*[]") != pointer.MakeArrayType()
                || Type.GetType("System.String*&") != pointer.MakeByRefType()
                || Type.GetType("System.String[]&")
                    != Type.GetType("System.String[]").MakeByRefType()
                || Type.GetType("System.String**") != pointer.MakePointerType()) {
            throw new AssertionError("Selected nested type-name lookup changed");
        }
        for (boolean throwOnError : new boolean[] {false, true}) {
            try {
                Type.GetType("System.String&[]", throwOnError);
                throw new AssertionError("By-reference array type name accepted");
            } catch (TypeLoadException expected) {
                // Selected pinned error type for both overload choices.
            }
        }
        if (Type.GetType("System.String*[], System.Private.CoreLib") != pointer.MakeArrayType()
                || Type.GetType("system.string*[], System.Private.CoreLib", false, true)
                    != pointer.MakeArrayType()
                || Type.GetType("system.string*[], System.Private.CoreLib", false, false) != null
                || Type.GetType("System.String*&, mscorlib") != pointer.MakeByRefType()
                || Type.GetType("System.String**, System.Private.CoreLib")
                    != pointer.MakePointerType()) {
            throw new AssertionError("Selected qualified nested type lookup changed");
        }
        try {
            Type.GetType("System.String&[], System.Private.CoreLib", false, false);
            throw new AssertionError("Qualified by-reference array accepted");
        } catch (TypeLoadException expected) {
            // Selected pinned error type.
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
        for (Type nonGeneric : new Type[] {Type.GetType("System.Object"), string,
                parameter, Type.GetType("System.String[]")}) {
            try {
                nonGeneric.GetGenericTypeDefinition();
                throw new AssertionError("Non-generic type accepted as a generic definition");
            } catch (InvalidOperationException expected) {
                // Selected pinned error type.
            }
        }
        Type dictionaryDefinition = Type.GetType("System.Collections.Generic.Dictionary`2");
        Type dictionaryConstructed = dictionaryDefinition.MakeGenericType(new Type[] {string, integer});
        Type[] dictionaryArguments = dictionaryDefinition.GetGenericArguments();
        Type[] copiedArguments = dictionaryDefinition.GetGenericArguments();
        if (dictionaryArguments == copiedArguments || dictionaryArguments.length != 2
                || !"TKey".equals(dictionaryArguments[0].get_Name())
                || !"TValue".equals(dictionaryArguments[1].get_Name())
                || dictionaryArguments[0].get_GenericParameterPosition() != 0
                || dictionaryArguments[1].get_GenericParameterPosition() != 1
                || dictionaryArguments[0] != copiedArguments[0]
                || dictionaryArguments[1] != copiedArguments[1]) {
            throw new AssertionError("Selected open generic argument ordering changed");
        }
        dictionaryArguments[0] = Type.GetType("System.Object");
        if (copiedArguments[0] != dictionaryDefinition.GetGenericArguments()[0]
                || dictionaryConstructed.GetGenericArguments()[0] != string
                || dictionaryConstructed.GetGenericArguments()[1] != integer
                || dictionaryDefinition.get_GenericTypeArguments().length != 0
                || dictionaryConstructed.get_GenericTypeArguments()[0] != string
                || dictionaryConstructed.get_GenericTypeArguments()[1] != integer
                || Type.GetType("System.String[]").GetGenericArguments().length != 0) {
            throw new AssertionError("Selected generic argument copies changed");
        }
        if (parameter.GetGenericParameterConstraints().length != 0
                || copiedArguments[0].GetGenericParameterConstraints().length != 0
                || copiedArguments[1].GetGenericParameterConstraints().length != 0) {
            throw new AssertionError("Selected generic parameter constraints changed");
        }
        for (Type nonParameter : new Type[] {Type.GetType("System.Object"), definition}) {
            try {
                nonParameter.GetGenericParameterConstraints();
                throw new AssertionError("Non-parameter constraints accepted");
            } catch (InvalidOperationException expected) {
                // Selected pinned error type.
            }
        }
        if (Type.GetType("System.Object").get_IsGenericTypeDefinition()
                || integer.get_IsGenericTypeDefinition()
                || !definition.get_IsGenericTypeDefinition()
                || first.get_IsGenericTypeDefinition()
                || !dictionaryDefinition.get_IsGenericTypeDefinition()
                || dictionaryConstructed.get_IsGenericTypeDefinition()
                || parameter.get_IsGenericTypeDefinition()
                || Type.GetType("System.String[]").get_IsGenericTypeDefinition()) {
            throw new AssertionError("Selected generic definition flags changed");
        }
        if (Type.GetType("System.Object").get_ContainsGenericParameters()
                || !definition.get_ContainsGenericParameters()
                || first.get_ContainsGenericParameters()
                || !dictionaryDefinition.get_ContainsGenericParameters()
                || dictionaryConstructed.get_ContainsGenericParameters()
                || !parameter.get_ContainsGenericParameters()
                || !definition.MakeArrayType().get_ContainsGenericParameters()
                || !definition.MakeGenericType(new Type[] {parameter})
                        .get_ContainsGenericParameters()) {
            throw new AssertionError("Selected contained generic parameters changed");
        }
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
        if (!integer.get_IsPrimitive() || object.get_IsPrimitive()
                || string.get_IsPrimitive() || Type.GetType("System.Decimal").get_IsPrimitive()
                || Type.GetType("System.DateTime").get_IsPrimitive()
                || Type.GetType("System.TypeCode").get_IsPrimitive()
                || arrayBase.get_IsPrimitive() || disposalType.get_IsPrimitive()
                || Type.GetType("System.String[]").get_IsPrimitive()
                || definition.get_IsPrimitive()) {
            throw new AssertionError("Selected primitive type flags changed");
        }
        if (object.get_IsAbstract() || string.get_IsAbstract() || integer.get_IsAbstract()
                || !Type.GetType("System.Type").get_IsAbstract()
                || !valueType.get_IsAbstract() || !Type.GetType("System.Enum").get_IsAbstract()
                || !arrayBase.get_IsAbstract() || !disposalType.get_IsAbstract()
                || !Type.GetType("System.IComparable").get_IsAbstract()
                || definition.get_IsAbstract()) {
            throw new AssertionError("Selected abstract type flags changed");
        }
        if (object.get_IsSealed() || !string.get_IsSealed() || !integer.get_IsSealed()
                || Type.GetType("System.Type").get_IsSealed() || valueType.get_IsSealed()
                || arrayBase.get_IsSealed() || disposalType.get_IsSealed()
                || !Type.GetType("System.TypeCode").get_IsSealed()
                || !Type.GetType("System.Decimal").get_IsSealed()
                || definition.get_IsSealed()) {
            throw new AssertionError("Selected sealed type flags changed");
        }
        if (!object.get_IsPublic() || !string.get_IsPublic() || !integer.get_IsPublic()
                || !valueType.get_IsPublic() || !arrayBase.get_IsPublic()
                || !Type.GetType("System.IComparable").get_IsPublic()
                || !definition.get_IsPublic() || !first.get_IsPublic()
                || !Type.GetType("System.String[]").get_IsPublic()
                || !byReference.get_IsPublic()) {
            throw new AssertionError("Selected public type flags changed");
        }
        if (!object.get_IsVisible() || !string.get_IsVisible()
                || !integer.get_IsVisible() || !Type.GetType("System.Type").get_IsVisible()
                || !disposalType.get_IsVisible() || !definition.get_IsVisible()
                || !first.get_IsVisible() || !Type.GetType("System.String[]").get_IsVisible()
                || !byReference.get_IsVisible() || !pointer.get_IsVisible()
                || !parameter.get_IsVisible() || !parameter.get_IsPublic()) {
            throw new AssertionError("Selected visible type flags changed");
        }
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
        if (integer.GetInterface("System.IComparable") != comparableType
                || integer.GetInterface("IComparable") != comparableType
                || integer.GetInterface("system.icomparable", true) != null
                || !comparableType.IsAssignableFrom(integer)
                || !comparableType.IsInstanceOfType(42)) {
            throw new AssertionError("Selected Int32 IComparable query changed");
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
        if (!"00042".equals(int32Value.ToString("D5", provider))
                || !"002A".equals(int32Value.ToString("X4", provider))
                || !"002a".equals(int32Value.ToString("x4", provider))
                || !"-00042".equals(new Int32(-42).ToString("D5", provider))
                || !"FFFFFFFF".equals(new Int32(-1).ToString("X", provider))) {
            throw new AssertionError("Selected Int32 format specifiers changed");
        }
        if (!"D-1".equals(int32Value.ToString("D-1", provider))
                || !"X-1".equals(int32Value.ToString("X-1", provider))) {
            throw new AssertionError("Selected Int32 custom format literals changed");
        }
        Int32 groupedValue = new Int32(12345);
        if (!"12,345".equals(groupedValue.ToString("N0", provider))
                || !"12,345.00".equals(groupedValue.ToString("N2", provider))
                || !"12,345.00".equals(groupedValue.ToString("n2", provider))
                || !"-12,345.00".equals(new Int32(-12345).ToString("N2", provider))
                || !"42.00".equals(int32Value.ToString("N", provider))) {
            throw new AssertionError("Selected Int32 number format changed");
        }
        if (!"\u00a412,345.00".equals(groupedValue.ToString("C", provider))
                || !"\u00a412,345".equals(groupedValue.ToString("C0", provider))
                || !"\u00a412,345.00".equals(groupedValue.ToString("c2", provider))
                || !"(\u00a412,345.00)".equals(new Int32(-12345).ToString("C2", provider))
                || !"\u00a442.00".equals(int32Value.ToString("C", provider))) {
            throw new AssertionError("Selected Int32 currency format changed");
        }
        if (!"12345".equals(groupedValue.ToString("F0", provider))
                || !"12345.00".equals(groupedValue.ToString("F2", provider))
                || !"12345.00".equals(groupedValue.ToString("f2", provider))
                || !"-12345.00".equals(new Int32(-12345).ToString("F2", provider))
                || !"42.00".equals(int32Value.ToString("F", provider))) {
            throw new AssertionError("Selected Int32 fixed-point format changed");
        }
        Int32 percentValue = new Int32(123);
        if (!"12,300.00 %".equals(percentValue.ToString("P", provider))
                || !"12,300 %".equals(percentValue.ToString("P0", provider))
                || !"12,300.00 %".equals(percentValue.ToString("p2", provider))
                || !"-12,300.00 %".equals(new Int32(-123).ToString("P2", provider))
                || !"4,200.00 %".equals(int32Value.ToString("P", provider))) {
            throw new AssertionError("Selected Int32 percent format changed");
        }
        if (!"42".equals(int32Value.ToString("G", provider))
                || !"42".equals(int32Value.ToString("G5", provider))
                || !"42".equals(int32Value.ToString("g5", provider))
                || !"42".equals(int32Value.ToString("G0", provider))
                || !"-42".equals(new Int32(-42).ToString("G5", provider))) {
            throw new AssertionError("Selected Int32 general format changed");
        }
        if (!"101010".equals(int32Value.ToString("B", provider))
                || !"00101010".equals(int32Value.ToString("B8", provider))
                || !"00101010".equals(int32Value.ToString("b8", provider))
                || !"11111111111111111111111111111111".equals(
                        new Int32(-1).ToString("B", provider))
                || !"42".equals(int32Value.ToString("R", provider))) {
            throw new AssertionError("Selected Int32 binary/round-trip format changed");
        }
        if (!"4.200000E+001".equals(int32Value.ToString("E", provider))
                || !"1.23E+004".equals(groupedValue.ToString("E2", provider))
                || !"1.23e+004".equals(groupedValue.ToString("e2", provider))
                || !"-4.2E+001".equals(new Int32(-42).ToString("E1", provider))
                || !"0.00E+000".equals(new Int32(0).ToString("E2", provider))) {
            throw new AssertionError("Selected Int32 exponential format changed");
        }
        if (!"1.0E+003".equals(new Int32(999).ToString("E1", provider))
                || !"1.0E+003".equals(new Int32(995).ToString("E1", provider))
                || !"9.9E+002".equals(new Int32(985).ToString("E1", provider))
                || !"9.5E+002".equals(new Int32(949).ToString("E1", provider))
                || !"2.15E+009".equals(new Int32(Integer.MAX_VALUE).ToString("E2", provider))
                || !"-2.15E+009".equals(new Int32(Integer.MIN_VALUE).ToString("E2", provider))) {
            throw new AssertionError("Selected Int32 exponential rounding changed");
        }
        if (!"000042".equals(int32Value.ToString("000000", provider))
                || !"-000042".equals(new Int32(-42).ToString("000000", provider))
                || !"12,345".equals(groupedValue.ToString("#,##0", provider))
                || !"12,345.00".equals(groupedValue.ToString("#,##0.00", provider))
                || !"42.00".equals(int32Value.ToString("0.00", provider))) {
            throw new AssertionError("Selected Int32 custom numeric format changed");
        }
        if (!"42".equals(int32Value.ToString("0;(0);zero", provider))
                || !"(42)".equals(new Int32(-42).ToString("0;(0);zero", provider))
                || !"zero".equals(new Int32(0).ToString("0;(0);zero", provider))) {
            throw new AssertionError("Selected Int32 custom sections changed");
        }
        if (!"42%".equals(int32Value.ToString("0\\%", provider))
                || !"4200%".equals(int32Value.ToString("0%", provider))
                || !"-42%".equals(new Int32(-42).ToString("0\\%", provider))
                || !"-4200%".equals(new Int32(-42).ToString("0%", provider))) {
            throw new AssertionError("Selected Int32 escaped percent changed");
        }
        if (!"42\u2030".equals(int32Value.ToString("0\\\u2030", provider))
                || !"42000\u2030".equals(int32Value.ToString("0\u2030", provider))
                || !"-42\u2030".equals(new Int32(-42).ToString("0\\\u2030", provider))
                || !"-42000\u2030".equals(new Int32(-42).ToString("0\u2030", provider))) {
            throw new AssertionError("Selected Int32 per-mille formatting changed");
        }
        if (!"12".equals(groupedValue.ToString("0,", provider))
                || !"1".equals(new Int32(1234567).ToString("0,,", provider))
                || !"1,235".equals(new Int32(1234567).ToString("#,##0,", provider))
                || !"-12".equals(new Int32(-12345).ToString("0,", provider))
                || !"1000".equals(new Int32(999500).ToString("0,", provider))) {
            throw new AssertionError("Selected Int32 comma scaling changed");
        }
        if (!"12.3".equals(groupedValue.ToString("0,.0", provider))
                || !"12.35".equals(groupedValue.ToString("0,.00", provider))
                || !"1,234.6".equals(new Int32(1234567).ToString("#,##0,.0", provider))
                || !"-12.3".equals(new Int32(-12345).ToString("0,.0", provider))
                || !"1.3".equals(new Int32(1250).ToString("0,.0", provider))) {
            throw new AssertionError("Selected Int32 scaled fraction changed");
        }
        if (!"42".equals(int32Value.ToString("0.##", provider))
                || !"12.35".equals(groupedValue.ToString("0,.##", provider))
                || !"12".equals(new Int32(12000).ToString("0,.##", provider))
                || !"1,234.57".equals(new Int32(1234567).ToString("#,##0,.##", provider))
                || !"-12.35".equals(new Int32(-12345).ToString("0,.##", provider))) {
            throw new AssertionError("Selected Int32 optional fraction changed");
        }
        if (!"item 42".equals(int32Value.ToString("'item '0", provider))
                || !"42 units".equals(int32Value.ToString("0' units'", provider))
                || !"[42]".equals(int32Value.ToString("'['0']'", provider))
                || !"-item 42".equals(new Int32(-42).ToString("'item '0", provider))
                || !"item 0".equals(new Int32(0).ToString("'item '0", provider))) {
            throw new AssertionError("Selected Int32 quoted literals changed");
        }
        if (!"42".equals(int32Value.ToString("0;[0];'none'", provider))
                || !"[42]".equals(new Int32(-42).ToString("0;[0];'none'", provider))
                || !"none".equals(new Int32(0).ToString("0;[0];'none'", provider))
                || !"42".equals(new Int32(-42).ToString("0;0;'zero'", provider))
                || !"minus 42".equals(new Int32(-42).ToString("0;'minus '0;'zero'", provider))) {
            throw new AssertionError("Selected Int32 quoted sections changed");
        }
        String bracketPattern = "[>=100]0;[<0]'neg '0;'small '0";
        if (!"[>=115]0".equals(new Int32(150).ToString(bracketPattern, provider))
                || !"[>=110]0".equals(new Int32(100).ToString(bracketPattern, provider))
                || !"[>=104]2".equals(int32Value.ToString(bracketPattern, provider))
                || !"[<4]neg 2".equals(new Int32(-42).ToString(bracketPattern, provider))
                || !"small 0".equals(new Int32(0).ToString(bracketPattern, provider))) {
            throw new AssertionError("Selected Int32 bracket literals changed");
        }
        if (!"0".equals(new Int32(-1).ToString("0,", provider))
                || !"0.0".equals(new Int32(-1).ToString("0,.0", provider))
                || !"0".equals(new Int32(-1).ToString("0,.##", provider))
                || !"-0.1".equals(new Int32(-50).ToString("0,.0", provider))
                || !"0.1".equals(new Int32(50).ToString("0,.0", provider))) {
            throw new AssertionError("Selected Int32 near-zero scaling changed");
        }
        String scaledSections = "0,;(0,);'zero'";
        if (!"12".equals(new Int32(12345).ToString(scaledSections, provider))
                || !"(12)".equals(new Int32(-12345).ToString(scaledSections, provider))
                || !"zero".equals(new Int32(0).ToString(scaledSections, provider))
                || !"zero".equals(new Int32(-1).ToString(scaledSections, provider))
                || !"(1.3)".equals(new Int32(-1250).ToString("0,.0;(0,.0);'zero'", provider))) {
            throw new AssertionError("Selected Int32 scaled sections changed");
        }
        try {
            int32Value.ToString("Q", provider);
            throw new AssertionError("Unknown format accepted");
        } catch (FormatException expected) {
            // Selected exception identity.
        }
        try {
            int32Value.ToString("D999999999999", provider);
            throw new AssertionError("Huge precision accepted");
        } catch (FormatException expected) {
            // Selected exception identity.
        }
        try {
            new Int32(300).ToByte(provider);
            throw new AssertionError("Byte overflow accepted");
        } catch (OverflowException expected) {
            // Selected exception identity.
        }
        try {
            new Int32(-1).ToUInt32(provider);
            throw new AssertionError("Unsigned overflow accepted");
        } catch (OverflowException expected) {
            // Selected exception identity.
        }
        try {
            new Int32(70000).ToChar(provider);
            throw new AssertionError("Char overflow accepted");
        } catch (OverflowException expected) {
            // Selected exception identity.
        }
        try {
            int32Value.ToDateTime(provider);
            throw new AssertionError("Int32 converted to DateTime");
        } catch (InvalidCastException expected) {
            // Selected exception identity.
        }
        if (Type.GetType("System.OverflowException") == null
                || Type.GetType("System.InvalidCastException") == null
                || Type.GetType("System.FormatException") == null) {
            throw new AssertionError("Selected conversion exception identities changed");
        }
        if (Int32.Parse("42").get_Value() != 42 || Int32.Parse(" 42 ").get_Value() != 42) {
            throw new AssertionError("Selected Int32.Parse values changed");
        }
        if (NumberStyles.None.get_Value() != 0 || NumberStyles.Integer.get_Value() != 7
                || NumberStyles.AllowHexSpecifier.get_Value() != 512
                || NumberStyles.HexNumber.get_Value() != 515
                || Int32.Parse("FF", NumberStyles.HexNumber, provider).get_Value() != 255
                || Int32.Parse(" FF ", NumberStyles.HexNumber, provider).get_Value() != 255
                || Int32.Parse("FFFFFFFF", NumberStyles.HexNumber, provider).get_Value() != -1
                || !Type.GetType("System.Globalization.NumberStyles").get_IsEnum()) {
            throw new AssertionError("Selected hexadecimal Int32.Parse values changed");
        }
        if (Int32.Parse("42", NumberStyles.None, provider).get_Value() != 42) {
            throw new AssertionError("NumberStyles.None decimal digits changed");
        }
        for (String text : new String[] {"+42", " 42", "42 "}) {
            try {
                Int32.Parse(text, NumberStyles.None, provider);
                throw new AssertionError("NumberStyles.None accepted sign or whitespace");
            } catch (FormatException expected) {
                // Pinned CLR failure type.
            }
        }
        Int32[] noneResult = new Int32[1];
        if (Int32.TryParse("+42", NumberStyles.None, provider, noneResult)
                || noneResult[0].get_Value() != 0) {
            throw new AssertionError("NumberStyles.None TryParse changed");
        }
        try {
            Int32.Parse("100000000", NumberStyles.HexNumber, provider);
            throw new AssertionError("Hexadecimal overflow accepted");
        } catch (OverflowException expected) {
            // Selected exception identity.
        }
        try {
            Int32.Parse("0xFF", NumberStyles.HexNumber, provider);
            throw new AssertionError("Hexadecimal prefix accepted");
        } catch (FormatException expected) {
            // Selected exception identity.
        }
        try {
            Int32.Parse(null, NumberStyles.HexNumber, provider);
            throw new AssertionError("Null hexadecimal Int32 parsed");
        } catch (ArgumentNullException expected) {
            if (!"s".equals(expected.get_ParamName())) {
                throw new AssertionError("Hexadecimal parse null parameter changed", expected);
            }
        }
        try {
            Int32.Parse("oops");
            throw new AssertionError("Invalid Int32 parsed");
        } catch (FormatException expected) {
            // Selected exception identity.
        }
        try {
            Int32.Parse("2147483648");
            throw new AssertionError("Out-of-range Int32 parsed");
        } catch (OverflowException expected) {
            // Selected exception identity.
        }
        try {
            Int32.Parse(null);
            throw new AssertionError("Null Int32 parsed");
        } catch (ArgumentNullException expected) {
            if (!"s".equals(expected.get_ParamName())) {
                throw new AssertionError("Int32.Parse null parameter changed", expected);
            }
        }
        Int32[] parsedResult = new Int32[1];
        if (!Int32.TryParse("42", parsedResult) || parsedResult[0].get_Value() != 42
                || !Int32.TryParse(" 42 ", parsedResult) || parsedResult[0].get_Value() != 42
                || !Int32.TryParse("-7", parsedResult) || parsedResult[0].get_Value() != -7
                || Int32.TryParse("oops", parsedResult) || parsedResult[0].get_Value() != 0
                || Int32.TryParse("2147483648", parsedResult) || parsedResult[0].get_Value() != 0
                || Int32.TryParse(null, parsedResult) || parsedResult[0].get_Value() != 0) {
            throw new AssertionError("Selected Int32.TryParse behavior changed");
        }
        if (!Int32.TryParse("FF", NumberStyles.HexNumber, provider, parsedResult)
                || parsedResult[0].get_Value() != 255
                || !Int32.TryParse(" FF ", NumberStyles.HexNumber, provider, parsedResult)
                || parsedResult[0].get_Value() != 255
                || !Int32.TryParse("FFFFFFFF", NumberStyles.HexNumber, provider, parsedResult)
                || parsedResult[0].get_Value() != -1
                || Int32.TryParse("100000000", NumberStyles.HexNumber, provider, parsedResult)
                || parsedResult[0].get_Value() != 0
                || Int32.TryParse("0xFF", NumberStyles.HexNumber, provider, parsedResult)
                || parsedResult[0].get_Value() != 0
                || Int32.TryParse(null, NumberStyles.HexNumber, provider, parsedResult)
                || parsedResult[0].get_Value() != 0) {
            throw new AssertionError("Selected hexadecimal Int32.TryParse behavior changed");
        }
        ISpanFormattable spanFormattable = int32Value;
        Type spanType = Type.GetType("System.ISpanFormattable");
        char[] enough = new char[2];
        int[] charsWritten = new int[1];
        boolean enoughResult = spanFormattable.TryFormat(enough, charsWritten, "D", provider);
        char[] shortBuffer = new char[1];
        int[] shortWritten = new int[1];
        boolean shortResult = spanFormattable.TryFormat(shortBuffer, shortWritten, "D", provider);
        if (spanType == null || !spanType.get_IsInterface()
                || spanType.GetInterfaces().length != 1
                || spanType.GetInterfaces()[0] != formattableType
                || integer.GetInterface("System.ISpanFormattable") != spanType
                || integer.GetInterface("ISpanFormattable") != spanType
                || integer.GetInterface("system.ispanformattable", true) != null
                || !spanType.IsAssignableFrom(integer) || !spanType.IsInstanceOfType(42)
                || !enoughResult || charsWritten[0] != 2 || !"42".equals(new String(enough))
                || shortResult || shortWritten[0] != 0) {
            throw new AssertionError("Selected Int32 span formatting changed");
        }
        IUtf8SpanFormattable utf8Formattable = int32Value;
        Type utf8Type = Type.GetType("System.IUtf8SpanFormattable");
        byte[] utf8Enough = new byte[2];
        int[] utf8Written = new int[1];
        boolean utf8EnoughResult = utf8Formattable.TryFormat(utf8Enough, utf8Written, "D", provider);
        byte[] utf8Short = new byte[1];
        int[] utf8ShortWritten = new int[1];
        boolean utf8ShortResult = utf8Formattable.TryFormat(utf8Short, utf8ShortWritten, "D", provider);
        if (utf8Type == null || !utf8Type.get_IsInterface()
                || utf8Type.GetInterfaces().length != 0
                || integer.GetInterface("System.IUtf8SpanFormattable") != utf8Type
                || integer.GetInterface("IUtf8SpanFormattable") != utf8Type
                || integer.GetInterface("system.iutf8spanformattable", true) != null
                || !utf8Type.IsAssignableFrom(integer) || !utf8Type.IsInstanceOfType(42)
                || !utf8EnoughResult || utf8Written[0] != 2
                || !"42".equals(new String(utf8Enough, java.nio.charset.StandardCharsets.UTF_8))
                || utf8ShortResult || utf8ShortWritten[0] != 0) {
            throw new AssertionError("Selected Int32 UTF-8 formatting changed");
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
        String corelibIdentity = ", System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, "
                + "PublicKeyToken=7cec85d7bea7798e";
        for (Type selected : new Type[] {string, integer, definition, first,
                Type.GetType("System.String[]"), rectangular, byReference, pointer}) {
            if (!(selected.get_FullName() + corelibIdentity).equals(selected.get_AssemblyQualifiedName())) {
                throw new AssertionError("Selected assembly-qualified type name changed: " + selected.get_Name());
            }
            if (Type.GetType(selected.get_AssemblyQualifiedName()) != selected) {
                throw new AssertionError("Assembly-qualified name failed identity round-trip: "
                        + selected.get_Name());
            }
        }
        if (parameter.get_GenericParameterAttributes() != GenericParameterAttributes.None) {
            throw new AssertionError("Selected generic parameter attributes changed");
        }
        Type attributesType = Type.GetType("System.Reflection.GenericParameterAttributes");
        if (attributesType == null
                || !"GenericParameterAttributes".equals(attributesType.get_Name())
                || !"System.Reflection.GenericParameterAttributes".equals(attributesType.get_FullName())
                || !"System.Enum".equals(attributesType.get_BaseType().get_FullName())
                || !attributesType.get_IsEnum() || !attributesType.get_IsValueType()
                || !attributesType.get_IsSealed()
                || attributesType.GetEnumUnderlyingType() != Type.GetType("System.Int32")
                || Type.GetTypeCode(attributesType) != TypeCode.Int32
                || Type.GetType(attributesType.get_AssemblyQualifiedName()) != attributesType
                || Type.GetType("system.reflection.genericparameterattributes", false, true)
                        != attributesType) {
            throw new AssertionError("GenericParameterAttributes Type identity changed");
        }
        Type[] definitionKinds = {string, integer, Type.GetType("System.IDisposable"),
                attributesType, definition, first, parameter, Type.GetType("System.String[]"),
                Type.GetType("System.String[,]"), string.MakeByRefType(),
                string.MakePointerType(), definition.MakeArrayType()};
        for (int index = 0; index < definitionKinds.length; index++) {
            if (definitionKinds[index].get_IsTypeDefinition() != (index < 5)) {
                throw new AssertionError("Selected IsTypeDefinition changed at " + index);
            }
        }
        for (Type selected : new Type[] {string, integer, Type.GetType("System.String[]"),
                string.MakeByRefType(), first, parameter}) {
            if (selected.get_IsByRefLike()) {
                throw new AssertionError("Represented Type became by-ref-like: " + selected.get_Name());
            }
        }
        int[] attributeValues = {0, 1, 2, 3, 4, 8, 16, 28, 32};
        GenericParameterAttributes[] attributes = GenericParameterAttributes.values();
        if (attributes.length != attributeValues.length) {
            throw new AssertionError("Generic parameter attribute enum shape changed");
        }
        for (int index = 0; index < attributes.length; index++) {
            if (attributes[index].get_Value() != attributeValues[index]) {
                throw new AssertionError("Generic parameter attribute value changed");
            }
        }
        try {
            string.get_GenericParameterAttributes();
            throw new AssertionError("Nonparameter attributes unexpectedly available");
        } catch (InvalidOperationException expected) {
            // Pinned selected exception class.
        }
        if (parameter.get_AssemblyQualifiedName() != null) {
            throw new AssertionError("Generic parameter gained an assembly-qualified name");
        }
        Type[] toStringTypes = {string, integer, Type.GetType("System.String[]"),
                Type.GetType("System.String[,]"), string.MakeByRefType(),
                string.MakePointerType(), definition, parameter, first,
                Type.GetType("System.Collections.Generic.Dictionary`2[System.String,System.Int32]")};
        String[] typeTexts = {"System.String", "System.Int32", "System.String[]",
                "System.String[,]", "System.String&", "System.String*",
                "System.Collections.Generic.List`1[T]", "T",
                "System.Collections.Generic.List`1[System.String]",
                "System.Collections.Generic.Dictionary`2[System.String,System.Int32]"};
        for (int index = 0; index < toStringTypes.length; index++) {
            if (!typeTexts[index].equals(toStringTypes[index].ToString())) {
                throw new AssertionError("Selected Type.ToString changed at " + index);
            }
        }
        Type nestedList = definition.MakeGenericType(new Type[] {first});
        Type listOfInt = definition.MakeGenericType(new Type[] {integer});
        Type nestedDictionary = Type.GetType("System.Collections.Generic.Dictionary`2")
                .MakeGenericType(new Type[] {string, listOfInt});
        Type[] nestedTextTypes = {first.MakeArrayType(), first.MakeArrayType(2), nestedList,
                nestedDictionary, definition.MakeArrayType(), parameter.MakeArrayType()};
        String[] nestedTexts = {"System.Collections.Generic.List`1[System.String][]",
                "System.Collections.Generic.List`1[System.String][,]",
                "System.Collections.Generic.List`1[System.Collections.Generic.List`1[System.String]]",
                "System.Collections.Generic.Dictionary`2[System.String,System.Collections.Generic.List`1[System.Int32]]",
                "System.Collections.Generic.List`1[T][]", "T[]"};
        for (int index = 0; index < nestedTexts.length; index++) {
            if (!nestedTexts[index].equals(nestedTextTypes[index].ToString())) {
                throw new AssertionError("Nested Type.ToString changed at " + index);
            }
            if (!nestedTextTypes[index].ToString().equals(nestedTextTypes[index].toString())) {
                throw new AssertionError("Java Type.toString bridge changed at " + index);
            }
        }
        for (Type element : primitiveTypes) {
            String name = element.get_FullName();
            Type[] shapes = {element.MakeArrayType(), element.MakeArrayType(1),
                    element.MakeArrayType(2), element.MakeArrayType(3)};
            String[] suffixes = {"[]", "[*]", "[,]", "[,,]"};
            for (int index = 0; index < shapes.length; index++) {
                if (!(name + suffixes[index]).equals(shapes[index].ToString())
                        || !shapes[index].ToString().equals(shapes[index].toString())) {
                    throw new AssertionError("Selected primitive array text changed: " + name);
                }
            }
        }
        for (Type selected : new Type[] {string, integer, definition, first,
                Type.GetType("System.String[]"), parameter}) {
            if (selected.get_UnderlyingSystemType() != selected) {
                throw new AssertionError("Selected underlying Type identity changed: " + selected.get_Name());
            }
            if (selected.get_IsGenericTypeParameter() != (selected == parameter)
                    || selected.get_IsGenericMethodParameter()) {
                throw new AssertionError("Selected generic parameter kind changed: " + selected.get_Name());
            }
        }
        for (String selectedCoreLibName : new String[] {
                "System.IDisposable", "System.IComparable", "System.IFormattable",
                "System.ISpanFormattable", "System.IUtf8SpanFormattable", "System.IFormatProvider",
                "System.IConvertible", "System.TypeCode", "System.Decimal", "System.DateTime",
                "System.Int32", "System.Type", "System.Reflection.MemberInfo",
                "System.Reflection.MemberTypes", "System.Exception", "System.SystemException",
                "System.ArgumentException", "System.ArgumentNullException", "System.TypeLoadException",
                "System.IndexOutOfRangeException", "System.IO.IOException",
                "System.IO.FileNotFoundException", "System.IO.FileLoadException",
                "System.Globalization.CultureNotFoundException", "System.OverflowException",
                "System.InvalidCastException", "System.InvalidOperationException",
                "System.FormatException", "System.Globalization.NumberStyles",
                "System.Reflection.GenericParameterAttributes"}) {
            Type selectedCoreLibType = Type.GetType(selectedCoreLibName);
            if (selectedCoreLibType == null
                    || !(selectedCoreLibName + corelibIdentity)
                            .equals(selectedCoreLibType.get_AssemblyQualifiedName())
                    || Type.GetType(selectedCoreLibType.get_AssemblyQualifiedName()) != selectedCoreLibType) {
                throw new AssertionError("Selected CoreLib identity round trip changed: " + selectedCoreLibName);
            }
            String lowerName = selectedCoreLibName.toLowerCase(java.util.Locale.ROOT);
            if (Type.GetType(lowerName, false, false) != null
                    || Type.GetType(lowerName, false, true) != selectedCoreLibType) {
                throw new AssertionError("Selected CoreLib case lookup changed: " + selectedCoreLibName);
            }
            String lowerQualifiedName = selectedCoreLibType.get_AssemblyQualifiedName()
                    .toLowerCase(java.util.Locale.ROOT);
            if (Type.GetType(lowerQualifiedName, false, false) != null
                    || Type.GetType(lowerQualifiedName, false, true) != selectedCoreLibType) {
                throw new AssertionError("Selected qualified case lookup changed: " + selectedCoreLibName);
            }
            for (String lowerCaseForm : new String[] {lowerName, lowerQualifiedName}) {
                try {
                    Type.GetType(lowerCaseForm, true, false);
                    throw new AssertionError("Sensitive lowercase lookup accepted: " + lowerCaseForm);
                } catch (TypeLoadException expected) {
                    // Selected pinned case-sensitive throw behavior.
                }
                if (Type.GetType(lowerCaseForm, true, true) != selectedCoreLibType) {
                    throw new AssertionError("Insensitive lowercase throw lookup changed: " + lowerCaseForm);
                }
            }
        }
        if (!parameter.get_IsGenericParameter() || parameter.get_GenericParameterPosition() != 0
                || parameter != definition.GetGenericArguments()[0]) {
            throw new AssertionError("External generic parameter identity changed");
        }
        java.lang.System.out.println("PASS external System.Type selected identity consumer");
    }
}
