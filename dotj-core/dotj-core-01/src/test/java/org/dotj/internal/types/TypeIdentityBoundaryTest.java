package org.dotj.internal.types;

import java.lang.reflect.Type;
import java.util.List;
import java.util.Map;

/** Small independent boundary checks for concrete Java type identity. */
public final class TypeIdentityBoundaryTest<T> {
    private List<String> first;
    private List<String> same;
    private List<Integer> different;
    private Map<String, List<Integer>> nestedFirst;
    private Map<String, List<Integer>> nestedSame;
    private Map<String, List<Long>> nestedDifferent;
    private List<?> wildcard;
    private List<T> variable;

    public static void main(String[] args) throws Exception {
        sameClassIdentity();
        // Next bounded case.
        System.out.println("PASS: internal type-identity boundary checks");
    }

    private static TypeIdentity identity(String field) throws Exception {
        Type type = TypeIdentityBoundaryTest.class.getDeclaredField(field).getGenericType();
        return TypeIdentity.of(type);
    }

    private static void sameClassIdentity() throws Exception {
        TypeIdentity first = TypeIdentity.of(String.class), same = TypeIdentity.of(String.class);
        if (!first.equals(same) || first.hashCode() != same.hashCode())
            throw new AssertionError("Same class identity differs");
    }

    // Next bounded method.
}
