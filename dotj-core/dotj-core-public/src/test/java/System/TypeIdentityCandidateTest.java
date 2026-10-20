package System;

import java.util.List;
import java.util.Map;

/** Exercises selected Type identity and null boundaries against the candidate implementation. */
public final class TypeIdentityCandidateTest {
    public static void main(String[] args) {
        Type list = Type.fromJavaClass(List.class);
        Type string = Type.fromJavaClass(String.class);
        Type integer = Type.fromJavaClass(Integer.class);
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
        try {
            list.GetGenericArguments();
            throw new AssertionError("Unimplemented generic parameter Type accepted");
        } catch (UnsupportedOperationException expected) {
            // The unimplemented shape stays explicit.
        }
        java.lang.System.out.println("PASS selected System.Type identity, nested arguments, defensive copies and null boundary");
    }
}
