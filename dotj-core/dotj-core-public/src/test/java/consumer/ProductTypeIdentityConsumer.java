package consumer;

import System.Type;
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
        if (!parameter.get_IsGenericParameter() || parameter.get_GenericParameterPosition() != 0
                || parameter != definition.GetGenericArguments()[0]) {
            throw new AssertionError("External generic parameter identity changed");
        }
        java.lang.System.out.println("PASS external System.Type selected identity consumer");
    }
}
