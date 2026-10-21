package System;

import java.util.List;
import java.util.Map;

/** Exercises selected Type identity and null boundaries against the candidate implementation. */
public final class TypeIdentityCandidateTest {
    static final class NestedAssemblyFixture {
    }

    private static final class NestedPrivateFixture {
    }

    protected static final class NestedFamilyFixture {
    }

    public static void main(String[] args) {
        Type list = Type.fromJavaClass(List.class);
        Type string = Type.fromJavaClass(String.class);
        Type integer = Type.fromJavaClass(Integer.class);
        if (integer != Type.fromJavaClass(Int32.class) || integer != Type.fromJavaClass(int.class)
                || integer != Type.GetType("System.Int32")) {
            throw new AssertionError("Int32 public facade and primitive backend identities diverged");
        }
        Type integerArray = Type.GetType("System.Int32[]");
        Type dictionary = Type.GetType("System.Collections.Generic.Dictionary`2[System.String,System.Int32]");
        if (integerArray.GetElementType() != integer || integer.MakeArrayType() != integerArray
                || dictionary.GetGenericArguments()[1] != integer
                || integer.MakePointerType() != Type.GetType("System.Int32*")) {
            throw new AssertionError("Int32 array, generic or pointer identity diverged");
        }
        Type longer = Type.fromJavaClass(Long.class);
        Type[] firstArguments = {string};
        Type first = list.MakeGenericType(firstArguments);
        firstArguments[0] = longer;
        Type same = list.MakeGenericType(new Type[] {string});
        Type different = list.MakeGenericType(new Type[] {longer});
        if (first != same || !first.Equals(same) || first.Equals(different)
                || first == different || first.GetGenericTypeDefinition() != list
                || !list.get_IsGenericType() || list.get_IsConstructedGenericType()
                || !first.get_IsConstructedGenericType() || first.GetGenericArguments()[0] != string) {
            throw new AssertionError("Selected closed generic identity changed");
        }
        Type[] returned = first.GetGenericArguments();
        returned[0] = longer;
        if (first.GetGenericArguments()[0] != string) {
            throw new AssertionError("Generic arguments escaped by reference");
        }
        Type map = Type.fromJavaClass(Map.class);
        Type nestedEntry = Type.fromJavaClass(Map.Entry.class);
        Type privateArgument = Type.fromJavaClass(NestedPrivateFixture.class);
        Type privateList = list.MakeGenericType(new Type[] {privateArgument});
        if (privateList.get_IsVisible() || privateList.MakeArrayType().get_IsVisible()
                || !list.MakeGenericType(new Type[] {string}).get_IsVisible()) {
            throw new AssertionError("Selected generic argument visibility changed");
        }
        if (nestedEntry.get_IsPublic() || !nestedEntry.get_IsNestedPublic()
                || !nestedEntry.get_IsVisible()
                || Type.fromJavaClass(NestedPrivateFixture.class).get_IsVisible()) {
            throw new AssertionError("Selected nested Type visibility changed");
        }
        if (Type.GetType("System.Collections.Generic.Dictionary`2+Entry") != nestedEntry
                || Type.GetType("System.Collections.Generic.Dictionary`2+Entry[]")
                        != nestedEntry.MakeArrayType()
                || Type.GetType("system.collections.generic.dictionary`2+entry", false, true)
                        != nestedEntry) {
            throw new AssertionError("Selected nested Type lookup changed");
        }
        if (!"Entry".equals(nestedEntry.get_Name())
                || !"System.Collections.Generic".equals(nestedEntry.get_Namespace())
                || !"System.Collections.Generic.Dictionary`2+Entry".equals(nestedEntry.get_FullName())) {
            throw new AssertionError("Selected nested Type names changed");
        }
        if (!"System.Collections.Generic.Dictionary`2+Entry[TKey,TValue]".equals(nestedEntry.ToString())
                || !"System.Collections.Generic.Dictionary`2+Entry[TKey,TValue][]"
                        .equals(nestedEntry.MakeArrayType().ToString())) {
            throw new AssertionError("Selected nested Type text changed");
        }
        if (nestedEntry.get_DeclaringType() != map || nestedEntry.get_ReflectedType() != map
                || string.get_DeclaringType() != null || string.get_ReflectedType() != null
                || nestedEntry.MakeArrayType().get_DeclaringType() != null) {
            throw new AssertionError("Selected nested Type owner changed");
        }
        if (string.get_IsNested() || string.get_IsNestedPublic()
                || list.get_IsNested() || list.get_IsNestedPublic()
                || !list.GetGenericArguments()[0].get_IsNested()
                || list.GetGenericArguments()[0].get_IsNestedPublic()
                || !nestedEntry.get_IsNested() || !nestedEntry.get_IsNestedPublic()) {
            throw new AssertionError("Selected nested Type flags changed");
        }
        Type nestedAssembly = Type.fromJavaClass(NestedAssemblyFixture.class);
        if (string.get_IsNestedAssembly() || list.GetGenericArguments()[0].get_IsNestedAssembly()
                || nestedEntry.get_IsNestedAssembly() || !nestedAssembly.get_IsNestedAssembly()
                || !nestedAssembly.get_IsNested() || nestedAssembly.get_IsNestedPublic()) {
            throw new AssertionError("Selected nested assembly visibility changed");
        }
        Type nestedPrivate = Type.fromJavaClass(NestedPrivateFixture.class);
        if (string.get_IsNestedPrivate() || list.GetGenericArguments()[0].get_IsNestedPrivate()
                || nestedEntry.get_IsNestedPrivate() || nestedAssembly.get_IsNestedPrivate()
                || !nestedPrivate.get_IsNestedPrivate() || !nestedPrivate.get_IsNested()) {
            throw new AssertionError("Selected nested private visibility changed");
        }
        Type nestedFamily = Type.fromJavaClass(NestedFamilyFixture.class);
        if (string.get_IsNestedFamily() || list.GetGenericArguments()[0].get_IsNestedFamily()
                || nestedEntry.get_IsNestedFamily() || nestedAssembly.get_IsNestedFamily()
                || nestedPrivate.get_IsNestedFamily() || !nestedFamily.get_IsNestedFamily()
                || !nestedFamily.get_IsNested()) {
            throw new AssertionError("Selected nested family visibility changed");
        }
        Type[] listParameters = list.GetGenericArguments();
        Type[] mapParameters = map.GetGenericArguments();
        if (listParameters.length != 1 || mapParameters.length != 2
                || !listParameters[0].get_IsGenericParameter()
                || listParameters[0].get_GenericParameterPosition() != 0
                || mapParameters[0].get_GenericParameterPosition() != 0
                || mapParameters[1].get_GenericParameterPosition() != 1
                || listParameters[0] != list.GetGenericArguments()[0]
                || mapParameters[0] == listParameters[0]
                || listParameters[0].get_IsGenericType()) {
            throw new AssertionError("Generic parameter Type identity changed");
        }
        listParameters[0] = string;
        if (!list.GetGenericArguments()[0].get_IsGenericParameter()) {
            throw new AssertionError("Generic parameter array escaped by reference");
        }
        Type nested = map.MakeGenericType(new Type[] {string, first});
        if (nested != map.MakeGenericType(new Type[] {string, same})
                || nested == map.MakeGenericType(new Type[] {string, different})) {
            throw new AssertionError("Nested generic identity changed");
        }
        try {
            list.MakeGenericType(null);
            throw new AssertionError("Null generic arguments accepted");
        } catch (ArgumentNullException expected) {
            if (!"typeArguments".equals(expected.get_ParamName())) {
                throw new AssertionError("Null parameter identity changed", expected);
            }
        }
        try {
            Type.GetType(null);
            throw new AssertionError("Null type name accepted");
        } catch (ArgumentNullException expected) {
            if (!"typeName".equals(expected.get_ParamName())) {
                throw new AssertionError("Null type-name parameter identity changed", expected);
            }
        }
        try {
            list.MakeGenericType(new Type[] {null});
            throw new AssertionError("Null generic argument accepted");
        } catch (NullPointerException expected) {
            if (!"typeArguments[0]".equals(expected.getMessage())) {
                throw new AssertionError("Null element identity changed", expected);
            }
        }
        java.lang.System.out.println("PASS selected System.Type identity, nested arguments, defensive copies and null boundary");
    }
}
