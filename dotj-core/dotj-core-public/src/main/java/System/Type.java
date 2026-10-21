package System;

import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.ConcurrentHashMap;
import System.IO.FileNotFoundException;
import System.Reflection.MemberInfo;
import System.Reflection.MemberTypes;

/** Bounded candidate for closed generic identity; not a complete System.Type surface. */
public abstract class Type extends MemberInfo {
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
    private static final ConcurrentHashMap<Type, Type> byReferences = new ConcurrentHashMap<>();
    private static final ConcurrentHashMap<Type, Type> pointers = new ConcurrentHashMap<>();

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
        return arrayShapes.computeIfAbsent(key, ignored -> new ArrayType(elementType, rank, vector));
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
            case "System.Object" -> fromJavaClass(Object.class);
            case "System.ValueType" -> fromJavaClass(Number.class);
            case "System.Array" -> fromJavaClass(java.lang.reflect.Array.class);
            case "System.IDisposable" -> fromJavaClass(IDisposable.class);
            case "System.IComparable" -> fromJavaClass(IComparable.class);
            case "System.IFormattable" -> fromJavaClass(IFormattable.class);
            case "System.IFormatProvider" -> fromJavaClass(IFormatProvider.class);
            case "System.IConvertible" -> fromJavaClass(IConvertible.class);
            case "System.Reflection.MemberTypes" -> fromJavaClass(MemberTypes.class);
            case "System.Enum" -> fromJavaClass(Enum.class);
            case "System.Collections.Generic.List`1" -> fromJavaClass(java.util.List.class);
            case "System.Collections.Generic.Dictionary`2" -> fromJavaClass(java.util.Map.class);
            case "System.String[]" -> fromJavaClass(String[].class);
            case "System.String[][]" -> fromJavaClass(String[][].class);
            case "System.String[,]" -> arrayOf(fromJavaClass(String.class), 2);
            case "System.String[,,]" -> arrayOf(fromJavaClass(String.class), 3);
            case "System.String[*]" -> arrayOf(fromJavaClass(String.class), 1, false);
            case "System.String&" -> fromJavaClass(String.class).MakeByRefType();
            case "System.String[]&" -> fromJavaClass(String[].class).MakeByRefType();
            case "System.String*" -> fromJavaClass(String.class).MakePointerType();
            case "System.Int32*" -> fromJavaClass(Integer.class).MakePointerType();
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
            case "system.object" -> ignoreCase ? fromJavaClass(Object.class) : null;
            case "system.valuetype" -> ignoreCase ? fromJavaClass(Number.class) : null;
            case "system.array" -> ignoreCase ? fromJavaClass(java.lang.reflect.Array.class) : null;
            case "system.idisposable" -> ignoreCase ? fromJavaClass(IDisposable.class) : null;
            case "system.icomparable" -> ignoreCase ? fromJavaClass(IComparable.class) : null;
            case "system.iformattable" -> ignoreCase ? fromJavaClass(IFormattable.class) : null;
            case "system.iformatprovider" -> ignoreCase ? fromJavaClass(IFormatProvider.class) : null;
            case "system.iconvertible" -> ignoreCase ? fromJavaClass(IConvertible.class) : null;
            case "system.reflection.membertypes" -> ignoreCase ? fromJavaClass(MemberTypes.class) : null;
            case "system.enum" -> ignoreCase ? fromJavaClass(Enum.class) : null;
            case "system.collections.generic.list`1" -> ignoreCase ? fromJavaClass(java.util.List.class) : null;
            case "system.collections.generic.dictionary`2" -> ignoreCase ? fromJavaClass(java.util.Map.class) : null;
            case "system.string[]" -> ignoreCase ? fromJavaClass(String[].class) : null;
            case "system.string[][]" -> ignoreCase ? fromJavaClass(String[][].class) : null;
            case "system.string[,]" -> ignoreCase ? arrayOf(fromJavaClass(String.class), 2) : null;
            case "system.string[,,]" -> ignoreCase ? arrayOf(fromJavaClass(String.class), 3) : null;
            case "system.string[*]" -> ignoreCase ? arrayOf(fromJavaClass(String.class), 1, false) : null;
            case "system.string&" -> ignoreCase ? fromJavaClass(String.class).MakeByRefType() : null;
            case "system.string[]&" -> ignoreCase ? fromJavaClass(String[].class).MakeByRefType() : null;
            case "system.string*" -> ignoreCase ? fromJavaClass(String.class).MakePointerType() : null;
            case "system.int32*" -> ignoreCase ? fromJavaClass(Integer.class).MakePointerType() : null;
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

    public Type MakeByRefType() {
        if (this.get_IsByRef()) {
            throw new TypeLoadException("Cannot make a by-reference type from a by-reference type");
        }
        return byReferences.computeIfAbsent(this, ByRefType::new);
    }

    public Type MakePointerType() {
        if (this.get_IsByRef()) {
            throw new TypeLoadException("Cannot make a pointer type from a by-reference type");
        }
        return pointers.computeIfAbsent(this, PointerType::new);
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

    protected final String nameCore() {
        if (this.parameterIndex >= 0) {
            if (this.definition == java.util.List.class) {
                return "T";
            }
            if (this.definition == java.util.Map.class) {
                return this.parameterIndex == 0 ? "TKey" : "TValue";
            }
            return this.definition.getTypeParameters()[this.parameterIndex].getName();
        }
        if (this instanceof ArrayType array) {
            return array.elementType.get_Name() + arraySuffix(array.rank, array.vector);
        }
        if (this.get_IsByRef() || this.get_IsPointer()) {
            return this.GetElementType().get_Name() + (this.get_IsByRef() ? "&" : "*");
        }
        if (this.definition.isArray()) {
            return this.GetElementType().get_Name() + "[]";
        }
        if (this.definition == String.class) return "String";
        if (this.definition == Integer.class) return "Int32";
        if (this.definition == Object.class) return "Object";
        if (this.definition == Number.class) return "ValueType";
        if (this.definition == java.lang.reflect.Array.class) return "Array";
        if (this.definition == Enum.class) return "Enum";
        if (this.definition == java.util.List.class) return "List`1";
        if (this.definition == java.util.Map.class) return "Dictionary`2";
        return this.definition.getSimpleName();
    }

    public String get_FullName() {
        if (this.parameterIndex >= 0) {
            return null;
        }
        if (this instanceof ArrayType array) {
            String element = array.elementType.get_FullName();
            return element == null ? null : element + arraySuffix(array.rank, array.vector);
        }
        if (this.get_IsByRef() || this.get_IsPointer()) {
            String element = this.GetElementType().get_FullName();
            return element == null ? null : element + (this.get_IsByRef() ? "&" : "*");
        }
        if (this.definition.isArray()) {
            String element = this.GetElementType().get_FullName();
            return element == null ? null : element + "[]";
        }
        String baseName = this.get_Namespace() + "." + this.get_Name();
        if (this.arguments.isEmpty()) {
            return baseName;
        }
        StringBuilder constructed = new StringBuilder(baseName).append('[');
        for (int index = 0; index < this.arguments.size(); index++) {
            String argument = this.arguments.get(index).get_FullName();
            if (argument == null) {
                return null;
            }
            if (index != 0) {
                constructed.append(',');
            }
            constructed.append('[').append(argument)
                    .append(", System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, ")
                    .append("PublicKeyToken=7cec85d7bea7798e]");
        }
        return constructed.append(']').toString();
    }

    public String get_Namespace() {
        if (this instanceof ArrayType array) {
            return array.elementType.get_Namespace();
        }
        if (this.get_IsByRef() || this.get_IsPointer() || this.definition.isArray()) {
            return this.GetElementType().get_Namespace();
        }
        if (this.definition == java.util.List.class || this.definition == java.util.Map.class) {
            return "System.Collections.Generic";
        }
        if (this.definition == String.class || this.definition == Integer.class
                || this.definition == Object.class || this.definition == Number.class
                || this.definition == java.lang.reflect.Array.class || this.definition == Enum.class) {
            return "System";
        }
        return this.definition.getPackageName();
    }

    @Override
    public Type get_DeclaringType() {
        return this.parameterIndex < 0 ? null : fromJavaClass(this.definition);
    }

    @Override
    public Type get_ReflectedType() {
        return this.parameterIndex < 0 ? null : fromJavaClass(this.definition);
    }

    public Type get_BaseType() {
        if (this.get_IsByRef() || this.get_IsPointer()) {
            return null;
        }
        if (this.get_IsArray()) {
            return fromJavaClass(java.lang.reflect.Array.class);
        }
        if (this.definition == Object.class && this.parameterIndex < 0) {
            return null;
        }
        if (this.definition == Integer.class) {
            return fromJavaClass(Number.class);
        }
        if (this.definition == MemberTypes.class) {
            return fromJavaClass(Enum.class);
        }
        if (this.definition == Enum.class) {
            return fromJavaClass(Number.class);
        }
        if (this.parameterIndex >= 0 || this.definition == String.class
                || this.definition == java.util.List.class || this.definition == java.util.Map.class
                || this.definition == Number.class || this.definition == java.lang.reflect.Array.class) {
            return fromJavaClass(Object.class);
        }
        Class<?> parent = this.definition.getSuperclass();
        return parent == null ? null : fromJavaClass(parent);
    }

    public boolean get_IsValueType() {
        return this.parameterIndex < 0
                && (this.definition == Integer.class || this.definition == MemberTypes.class);
    }

    public boolean get_IsClass() {
        return !this.get_IsValueType() && !this.get_IsInterface();
    }

    public boolean get_IsInterface() {
        return this.definition == IDisposable.class || this.definition == IComparable.class
                || this.definition == IFormattable.class || this.definition == IFormatProvider.class
                || this.definition == IConvertible.class;
    }

    public boolean get_IsEnum() {
        return this.definition == MemberTypes.class;
    }

    public Type GetEnumUnderlyingType() {
        if (!this.get_IsEnum()) {
            throw new ArgumentException("Type must be an enum");
        }
        return fromJavaClass(Integer.class);
    }

    public boolean IsAssignableFrom(Type candidate) {
        if (candidate == null) {
            return false;
        }
        if (this == candidate) {
            return true;
        }
        if (this.definition == IComparable.class && candidate.definition == String.class) {
            return true;
        }
        if (this.definition == IFormattable.class && candidate.definition == Integer.class) {
            return true;
        }
        if (this.definition == IConvertible.class && candidate.definition == Integer.class) {
            return true;
        }
        if (candidate.get_IsByRef() || candidate.get_IsPointer()) {
            return false;
        }
        if (this == fromJavaClass(Object.class)) {
            return true;
        }
        Type ancestor = candidate.get_BaseType();
        while (ancestor != null) {
            if (this == ancestor) {
                return true;
            }
            ancestor = ancestor.get_BaseType();
        }
        return false;
    }

    public boolean IsSubclassOf(Type parent) {
        if (parent == null) {
            throw new ArgumentNullException("type");
        }
        if (this == parent) {
            return false;
        }
        if (this.get_IsInterface() && parent == fromJavaClass(Object.class)) {
            return true;
        }
        Type ancestor = this.get_BaseType();
        while (ancestor != null) {
            if (ancestor == parent) {
                return true;
            }
            ancestor = ancestor.get_BaseType();
        }
        return false;
    }

    public boolean IsInstanceOfType(Object value) {
        if (value == null || this.get_IsByRef() || this.get_IsPointer()) {
            return false;
        }
        if (this.definition == Object.class) {
            return true;
        }
        if (this.definition == Number.class) {
            return value instanceof Integer || value instanceof MemberTypes;
        }
        if (this.definition == Enum.class) {
            return value instanceof MemberTypes;
        }
        if (this.definition == IComparable.class) {
            return value instanceof String;
        }
        if (this.definition == IFormattable.class) {
            return value instanceof Integer;
        }
        if (this.definition == IConvertible.class) {
            return value instanceof Integer;
        }
        if (this.definition == java.lang.reflect.Array.class) {
            return value.getClass().isArray();
        }
        if (this instanceof ArrayType || this.definition == java.util.List.class
                || this.definition == java.util.Map.class) {
            return false;
        }
        return this.definition.isInstance(value);
    }

    public Type[] GetInterfaces() {
        if (this.definition == Object.class || this.definition == IDisposable.class) {
            return new Type[0];
        }
        throw new UnsupportedOperationException("Interface enumeration is not mapped for this candidate type");
    }

    public Type GetInterface(String fullname) {
        return this.GetInterface(fullname, false);
    }

    public Type GetInterface(String fullname, boolean ignoreCase) {
        if (fullname == null) {
            throw new ArgumentNullException("fullname");
        }
        if (this.definition == Object.class || this.definition == IDisposable.class) {
            return null;
        }
        if (this.definition == String.class) {
            if (fullname.equals("System.IComparable") || fullname.equals("IComparable")) {
                return fromJavaClass(IComparable.class);
            }
            if (fullname.equals("system.icomparable") || fullname.equals("System.IDisposable")
                    || fullname.equals("System.IFormattable")
                    || fullname.isEmpty()) {
                return null;
            }
        }
        if (this.definition == Integer.class) {
            if (fullname.equals("System.IFormattable") || fullname.equals("IFormattable")) {
                return fromJavaClass(IFormattable.class);
            }
            if (fullname.equals("system.iformattable")) {
                return null;
            }
            if (fullname.equals("System.IConvertible") || fullname.equals("IConvertible")) {
                return fromJavaClass(IConvertible.class);
            }
            if (fullname.equals("system.iconvertible")) {
                return null;
            }
        }
        throw new UnsupportedOperationException("Interface lookup is not mapped for this candidate type");
    }

    private static String arraySuffix(int rank, boolean vector) {
        if (rank == 1) {
            return vector ? "[]" : "[*]";
        }
        return "[" + ",".repeat(rank - 1) + "]";
    }

    public boolean get_IsArray() {
        return this.definition.isArray();
    }

    public boolean get_IsByRef() {
        return false;
    }

    public boolean get_IsPointer() {
        return false;
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

        @Override
        public String get_Name() {
            return this.nameCore();
        }

        @Override
        public MemberTypes get_MemberType() {
            return MemberTypes.TypeInfo;
        }
    }

    private static final class GenericParameterType extends Type {
        private GenericParameterType(Class<?> definition, int index) {
            super(definition, List.of(), index);
        }

        @Override
        public String get_Name() {
            return this.nameCore();
        }

        @Override
        public MemberTypes get_MemberType() {
            return MemberTypes.TypeInfo;
        }
    }

    private static final class ArrayType extends Type {
        private final Type elementType;
        private final int rank;
        private final boolean vector;

        private ArrayType(Type elementType, int rank, boolean vector) {
            super(Object.class, List.of());
            this.elementType = elementType;
            this.rank = rank;
            this.vector = vector;
        }

        @Override
        public String get_Name() {
            return this.nameCore();
        }

        @Override
        public MemberTypes get_MemberType() {
            return MemberTypes.TypeInfo;
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

    private static final class ByRefType extends Type {
        private final Type elementType;

        private ByRefType(Type elementType) {
            super(Object.class, List.of());
            this.elementType = elementType;
        }

        @Override
        public String get_Name() {
            return this.nameCore();
        }

        @Override
        public MemberTypes get_MemberType() {
            return MemberTypes.TypeInfo;
        }

        @Override
        public boolean get_IsByRef() {
            return true;
        }

        @Override
        public Type GetElementType() {
            return this.elementType;
        }
    }

    private static final class PointerType extends Type {
        private final Type elementType;

        private PointerType(Type elementType) {
            super(Object.class, List.of());
            this.elementType = elementType;
        }

        @Override
        public String get_Name() {
            return this.nameCore();
        }

        @Override
        public MemberTypes get_MemberType() {
            return MemberTypes.TypeInfo;
        }

        @Override
        public boolean get_IsPointer() {
            return true;
        }

        @Override
        public Type GetElementType() {
            return this.elementType;
        }
    }
}
