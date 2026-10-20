package org.dotj.internal.types;

import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.util.Objects;

/** Internal identity value for concrete Java types; not a public System.Type substitute. */
final class TypeIdentity {
    private final Type type;

    private TypeIdentity(Type type) {
        this.type = type;
    }

    static TypeIdentity of(Type type) {
        requireClosed(Objects.requireNonNull(type, "type"));
        return new TypeIdentity(type);
    }

    private static void requireClosed(Type type) {
        if (type instanceof Class<?>) {
            return;
        }
        if (type instanceof ParameterizedType parameterized) {
            requireClosed(parameterized.getRawType());
            Type owner = parameterized.getOwnerType();
            if (owner != null) {
                requireClosed(owner);
            }
            for (Type argument : parameterized.getActualTypeArguments()) {
                requireClosed(argument);
            }
            return;
        }
        throw new IllegalArgumentException("Only concrete class and parameterized types are supported");
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof TypeIdentity identity && type.equals(identity.type);
    }

    @Override
    public int hashCode() {
        return type.hashCode();
    }
}
