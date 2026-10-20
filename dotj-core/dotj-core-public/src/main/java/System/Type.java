package System;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

/** Bounded candidate for closed generic identity; not a complete System.Type surface. */
public abstract class Type {
    private static final ClassValue<ConcurrentHashMap<List<Type>, Type>> canonical =
            new ClassValue<>() {
                @Override
                protected ConcurrentHashMap<List<Type>, Type> computeValue(Class<?> ignored) {
                    return new ConcurrentHashMap<>();
                }
            };

    private final Class<?> definition;
    private final List<Type> arguments;

    private Type(Class<?> definition, List<Type> arguments) {
        this.definition = definition;
        this.arguments = arguments;
    }

    // A future .j typeof operation may lower to this package-internal entry point.
    static Type fromJavaClass(Class<?> definition) {
        if (definition == null) {
            throw new NullPointerException("definition");
        }
        return canonical.get(definition).computeIfAbsent(List.of(), key -> new ResolvedType(definition, key));
    }

    public Type MakeGenericType(Type[] typeArguments) {
        if (typeArguments == null) {
            throw new NullPointerException("typeArguments");
        }
        if (!this.arguments.isEmpty() || this.definition.getTypeParameters().length == 0) {
            throw new IllegalStateException("Not a generic type definition");
        }
        if (typeArguments.length != this.definition.getTypeParameters().length) {
            throw new IllegalArgumentException("Generic argument count does not match the definition");
        }
        for (int index = 0; index < typeArguments.length; index++) {
            if (typeArguments[index] == null) {
                throw new NullPointerException("typeArguments[" + index + "]");
            }
        }
        List<Type> key = List.copyOf(Arrays.asList(typeArguments.clone()));
        return canonical.get(this.definition).computeIfAbsent(key, arguments -> new ResolvedType(this.definition, arguments));
    }

    public Type GetGenericTypeDefinition() {
        if (this.definition.getTypeParameters().length == 0) {
            throw new IllegalStateException("Not a generic type");
        }
        return fromJavaClass(this.definition);
    }

    public Type[] GetGenericArguments() {
        if (this.arguments.isEmpty() && this.definition.getTypeParameters().length != 0) {
            throw new UnsupportedOperationException("Generic parameter Type values are not implemented");
        }
        return this.arguments.toArray(Type[]::new);
    }

    public Type[] get_GenericTypeArguments() {
        return this.arguments.toArray(Type[]::new);
    }

    public boolean get_IsGenericType() {
        return this.definition.getTypeParameters().length != 0;
    }

    public boolean get_IsConstructedGenericType() {
        return !this.arguments.isEmpty();
    }

    public boolean Equals(Type other) {
        return this == other;
    }

    private static final class ResolvedType extends Type {
        private ResolvedType(Class<?> definition, List<Type> arguments) {
            super(definition, arguments);
        }
    }
}
