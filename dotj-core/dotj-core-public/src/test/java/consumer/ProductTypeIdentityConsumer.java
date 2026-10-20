package consumer;

import System.Type;
import System.ArgumentNullException;
import System.ArgumentException;
import System.TypeLoadException;
import System.IO.FileNotFoundException;
import System.IO.IOException;
import System.IndexOutOfRangeException;
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
