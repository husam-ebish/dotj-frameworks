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
    private static final ClassValue<Type[]> genericParameters = new ClassValue<>() {
        @Override
        protected Type[] computeValue(Class<?> definition) {
            var variables = definition.getTypeParameters();
            Type[] result = new Type[variables.length];
            for (int index = 0; index < variables.length; index++) {
                result[index] = new GenericParameterType(definition, index);
            }
            return result;
        }
    };

    private final Class<?> definition;
    private final List<Type> arguments;
    private final int parameterIndex;

    private Type(Class<?> definition, List<Type> arguments) {
        this(definition, arguments, -1);
    }

    private Type(Class<?> definition, List<Type> arguments, int parameterIndex) {
        this.definition = definition;
        this.arguments = arguments;
        this.parameterIndex = parameterIndex;
    }

    // A future .j typeof operation may lower to this package-internal entry point.
    static Type fromJavaClass(Class<?> definition) {
        if (definition == null) {
            throw new NullPointerException("definition");
        }
        return canonical.get(definition).computeIfAbsent(List.of(), key -> new ResolvedType(definition, key));
    }

    /** Selected CoreLib names only; broader lookup and assembly resolution remain open. */
    public static Type GetType(String typeName) {
        if (typeName == null) {
            throw new ArgumentNullException("typeName");
        }
        return switch (typeName) {
            case "System.String" -> fromJavaClass(String.class);
            case "System.Int32" -> fromJavaClass(Integer.class);
            case "System.Collections.Generic.List`1" -> fromJavaClass(java.util.List.class);
            case "System.Collections.Generic.Dictionary`2" -> fromJavaClass(java.util.Map.class);
            default -> null;
        };
    }

    public Type MakeGenericType(Type[] typeArguments) {
        if (typeArguments == null) {
            throw new ArgumentNullException("typeArguments");
        }
        if (this.parameterIndex >= 0 || !this.arguments.isEmpty()
                || this.definition.getTypeParameters().length == 0) {
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
        if (this.parameterIndex >= 0 || this.definition.getTypeParameters().length == 0) {
            throw new IllegalStateException("Not a generic type");
        }
        return fromJavaClass(this.definition);
    }

    public Type[] GetGenericArguments() {
        if (this.parameterIndex >= 0) {
            return new Type[0];
        }
        if (this.arguments.isEmpty()) {
            return genericParameters.get(this.definition).clone();
        }
        return this.arguments.toArray(Type[]::new);
    }

    public Type[] get_GenericTypeArguments() {
        return this.arguments.toArray(Type[]::new);
    }

    public boolean get_IsGenericType() {
        return this.parameterIndex < 0 && this.definition.getTypeParameters().length != 0;
    }

    public boolean get_IsConstructedGenericType() {
        return this.parameterIndex < 0 && !this.arguments.isEmpty();
    }

    public boolean get_IsGenericParameter() {
        return this.parameterIndex >= 0;
    }

    public int get_GenericParameterPosition() {
        if (this.parameterIndex < 0) {
            throw new IllegalStateException("Not a generic parameter");
        }
        return this.parameterIndex;
    }

    public boolean Equals(Type other) {
        return this == other;
    }

    private static final class ResolvedType extends Type {
        private ResolvedType(Class<?> definition, List<Type> arguments) {
            super(definition, arguments);
        }
    }

    private static final class GenericParameterType extends Type {
        private GenericParameterType(Class<?> definition, int index) {
            super(definition, List.of(), index);
        }
    }
}
