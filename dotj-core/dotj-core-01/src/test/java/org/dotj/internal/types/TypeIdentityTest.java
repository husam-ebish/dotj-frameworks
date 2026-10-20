package org.dotj.internal.types;

import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Independent Java fixtures for designed DJ-001-F01-01 and F01-02. */
public final class TypeIdentityTest {
    private List<String> first;
    private List<String> same;
    private List<Integer> different;
    private List<?> wildcard;

    public static void main(String[] args) throws NoSuchFieldException {
        TypeIdentity first = identityOf("first");
        TypeIdentity same = identityOf("same");
        TypeIdentity different = identityOf("different");
        if (!first.equals(same) || first.hashCode() != same.hashCode()) {
            throw new AssertionError("F01-01: equal closed parameterizations differ");
        }
        if (first.equals(different) || first.equals(TypeIdentity.of(List.class))) {
            throw new AssertionError("F01-02: different type arguments share identity");
        }
        Map<TypeIdentity, String> values = new HashMap<>();
        values.put(first, "shared");
        if (!"shared".equals(values.get(same)) || values.containsKey(different)) {
            throw new AssertionError("type identity does not work as a structural key");
        }
        try {
            identityOf("wildcard");
            throw new AssertionError("unmapped wildcard was accepted as a closed type");
        } catch (IllegalArgumentException expected) {
            // Unmapped generic forms remain explicit.
        }
        System.out.println("PASS: DJ-001-F01-01 and F01-02 closed generic identity");
    }

    private static TypeIdentity identityOf(String field) throws NoSuchFieldException {
        Type type = TypeIdentityTest.class.getDeclaredField(field).getGenericType();
        return TypeIdentity.of(type);
    }
}
