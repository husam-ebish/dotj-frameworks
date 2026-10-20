package System;

import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.ConcurrentHashMap;
import System.IO.FileNotFoundException;

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
    private static final ConcurrentHashMap<List<Object>, Type> arrayShapes = new ConcurrentHashMap<>();

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

    private static Type arrayOf(Type elementType, int rank) {
        return arrayOf(elementType, rank, rank == 1);
    }

    private static Type arrayOf(Type elementType, int rank, boolean vector) {
        List<Object> key = List.of(elementType, rank, vector);
        return arrayShapes.computeIfAbsent(key, ignored -> new ArrayType(elementType, rank));
    }

    /** Selected CoreLib names only; broader lookup and assembly resolution remain open. */
    public static Type GetType(String typeName) {
        return GetType(typeName, false, false);
    }

    public static Type GetType(String typeName, boolean throwOnError) {
        return GetType(typeName, throwOnError, false);
    }

    /** Selected CoreLib names only; assembly resolution remains open. */
    public static Type GetType(String typeName, boolean throwOnError, boolean ignoreCase) {
        if (typeName == null) {
            throw new ArgumentNullException("typeName");
        }
        String name = typeName.stripLeading();
        int assemblySeparator = -1;
        int bracketDepth = 0;
        for (int index = 0; index < typeName.length(); index++) {
            char character = typeName.charAt(index);
            if (character == '[') {
                bracketDepth++;
            } else if (character == ']') {
                bracketDepth--;
            } else if (character == ',' && bracketDepth == 0) {
                assemblySeparator = index;
                break;
            }
        }
        if (assemblySeparator >= 0) {
            String assembly = typeName.substring(assemblySeparator + 1).trim();
            if (assembly.isEmpty()) {
                if (throwOnError) {
                    throw new ArgumentException("Invalid assembly name", "typeName@" + assemblySeparator);
                }
                return null;
            }
            if (assembly.equals("System.Private.CoreLib") || assembly.equals("mscorlib")) {
                name = typeName.substring(0, assemblySeparator).stripLeading();
            } else if (throwOnError) {
                throw new FileNotFoundException("Could not load assembly: " + assembly);
            }
        }
        String key = ignoreCase ? name.toLowerCase(Locale.ROOT) : name;
        Type resolved = switch (key) {
            case "System.String" -> fromJavaClass(String.class);
            case "System.Int32" -> fromJavaClass(Integer.class);
            case "System.Collections.Generic.List`1" -> fromJavaClass(java.util.List.class);
            case "System.Collections.Generic.Dictionary`2" -> fromJavaClass(java.util.Map.class);
            case "System.String[]" -> fromJavaClass(String[].class);
            case "System.String[][]" -> fromJavaClass(String[][].class);
            case "System.String[,]" -> arrayOf(fromJavaClass(String.class), 2);
            case "System.String[,,]" -> arrayOf(fromJavaClass(String.class), 3);
            case "System.String[*]" -> arrayOf(fromJavaClass(String.class), 1, false);
            case "System.Int32[]" -> fromJavaClass(int[].class);
            case "System.Collections.Generic.List`1[System.String]",
                    "System.Collections.Generic.List`1[[System.String, System.Private.CoreLib]]" ->
                    fromJavaClass(java.util.List.class).MakeGenericType(new Type[] {fromJavaClass(String.class)});
            case "System.Collections.Generic.Dictionary`2[System.String,System.Int32]",
                    "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Int32, System.Private.CoreLib]]" ->
                    fromJavaClass(java.util.Map.class).MakeGenericType(
                            new Type[] {fromJavaClass(String.class), fromJavaClass(Integer.class)});
            case "System.Collections.Generic.Dictionary`2[System.Int32,System.String]" ->
                    fromJavaClass(java.util.Map.class).MakeGenericType(
                            new Type[] {fromJavaClass(Integer.class), fromJavaClass(String.class)});
            case "System.Collections.Generic.List`1[System.String][]" ->
                    arrayOf(fromJavaClass(java.util.List.class)
                            .MakeGenericType(new Type[] {fromJavaClass(String.class)}), 1);
            case "system.string" -> ignoreCase ? fromJavaClass(String.class) : null;
            case "system.int32" -> ignoreCase ? fromJavaClass(Integer.class) : null;
            case "system.collections.generic.list`1" -> ignoreCase ? fromJavaClass(java.util.List.class) : null;
            case "system.collections.generic.dictionary`2" -> ignoreCase ? fromJavaClass(java.util.Map.class) : null;
            case "system.string[]" -> ignoreCase ? fromJavaClass(String[].class) : null;
            case "system.string[][]" -> ignoreCase ? fromJavaClass(String[][].class) : null;
            case "system.string[,]" -> ignoreCase ? arrayOf(fromJavaClass(String.class), 2) : null;
            case "system.string[,,]" -> ignoreCase ? arrayOf(fromJavaClass(String.class), 3) : null;
            case "system.string[*]" -> ignoreCase ? arrayOf(fromJavaClass(String.class), 1, false) : null;
            case "system.int32[]" -> ignoreCase ? fromJavaClass(int[].class) : null;
            case "system.collections.generic.list`1[system.string]",
                    "system.collections.generic.list`1[[system.string, system.private.corelib]]" ->
                    ignoreCase ? fromJavaClass(java.util.List.class)
                            .MakeGenericType(new Type[] {fromJavaClass(String.class)}) : null;
            default -> null;
        };
        if (resolved == null && throwOnError) {
            throw new TypeLoadException("Could not resolve selected type: " + typeName);
        }
        return resolved;
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

    public Type MakeArrayType() {
        if (this == fromJavaClass(String.class)) {
            return fromJavaClass(String[].class);
        }
        if (this == fromJavaClass(Integer.class)) {
            return fromJavaClass(int[].class);
        }
        if (this == fromJavaClass(String[].class)) {
            return fromJavaClass(String[][].class);
        }
        return arrayOf(this, 1);
    }

    public Type MakeArrayType(int rank) {
        if (rank < 1) {
            throw new IndexOutOfRangeException("Array rank is out of range");
        }
        return arrayOf(this, rank, false);
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

    public boolean get_IsArray() {
        return this.definition.isArray();
    }

    public Type GetElementType() {
        Class<?> element = this.definition.getComponentType();
        return element == null ? null : fromJavaClass(element);
    }

    public int GetArrayRank() {
        if (!this.get_IsArray()) {
            throw new ArgumentException("Type must be an array");
        }
        return 1;
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

    private static final class ArrayType extends Type {
        private final Type elementType;
        private final int rank;

        private ArrayType(Type elementType, int rank) {
            super(Object.class, List.of());
            this.elementType = elementType;
            this.rank = rank;
        }

        @Override
        public boolean get_IsArray() {
            return true;
        }

        @Override
        public Type GetElementType() {
            return this.elementType;
        }

        @Override
        public int GetArrayRank() {
            return this.rank;
        }
    }
}
