package System;

import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.ConcurrentHashMap;
import System.IO.FileNotFoundException;
import System.IO.FileLoadException;
import System.Reflection.MemberInfo;
import System.Reflection.MemberTypes;
import System.Globalization.NumberStyles;
import System.Globalization.CultureNotFoundException;

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
        Class<?> backend = definition == Integer.class || definition == int.class
                ? Int32.class : definition;
        return canonical.get(backend).computeIfAbsent(List.of(), key -> new ResolvedType(backend, key));
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
            String assemblyName = assembly.split(",", 2)[0].trim();
            if (assemblyName.equalsIgnoreCase("System.Private.CoreLib")
                    || assemblyName.equalsIgnoreCase("mscorlib")) {
                String[] attributes = assembly.split(",", -1);
                java.util.HashSet<String> seen = new java.util.HashSet<>();
                for (int index = 1; index < attributes.length; index++) {
                    String[] attribute = attributes[index].trim().split("=", 2);
                    String key = attribute[0].trim().toLowerCase(Locale.ROOT);
                    String value = attribute.length == 2 ? attribute[1].trim() : "";
                    boolean extraEquals = value.indexOf('=') >= 0;
                    if (value.length() >= 2 && value.startsWith("\"") && value.endsWith("\"")) {
                        value = value.substring(1, value.length() - 1);
                    }
                    boolean recognized = key.equals("version") || key.equals("culture")
                            || key.equals("publickeytoken");
                    if (attribute.length != 2 || value.isEmpty() || extraEquals
                            || recognized && !seen.add(key)
                            || key.equals("version") && !value.matches("[0-9]+(\\.[0-9]+){1,3}")
                            || key.equals("publickeytoken") && !value.equalsIgnoreCase("null")
                                    && !value.matches("[0-9a-fA-F]{16}")) {
                        throw new FileLoadException("Invalid assembly identity: " + assembly);
                    }
                    if (key.equals("version")) {
                        for (String component : value.split("\\.")) {
                            if (component.length() > 5 || Integer.parseInt(component) > 65534) {
                                throw new FileLoadException("Invalid assembly version: " + assembly);
                            }
                        }
                    }
                    if (key.equals("culture") && value.matches("[0-9]+")) {
                        throw new CultureNotFoundException("name", value, "Culture is not supported");
                    }
                }
                name = typeName.substring(0, assemblySeparator).stripLeading();
            } else if (throwOnError) {
                throw new FileNotFoundException("Could not load assembly: " + assembly);
            }
        }
        String key = ignoreCase ? name.toLowerCase(Locale.ROOT) : name;
        Type resolved = switch (key) {
            case "System.String" -> fromJavaClass(String.class);
            case "System.Int32" -> fromJavaClass(Int32.class);
            case "System.Object" -> fromJavaClass(Object.class);
            case "System.ValueType" -> fromJavaClass(Number.class);
            case "System.Array" -> fromJavaClass(java.lang.reflect.Array.class);
            case "System.IDisposable" -> fromJavaClass(IDisposable.class);
            case "System.IComparable" -> fromJavaClass(IComparable.class);
            case "System.IFormattable" -> fromJavaClass(IFormattable.class);
            case "System.ISpanFormattable" -> fromJavaClass(ISpanFormattable.class);
            case "System.IUtf8SpanFormattable" -> fromJavaClass(IUtf8SpanFormattable.class);
            case "System.IFormatProvider" -> fromJavaClass(IFormatProvider.class);
            case "System.IConvertible" -> fromJavaClass(IConvertible.class);
            case "System.TypeCode" -> fromJavaClass(TypeCode.class);
            case "System.Type" -> fromJavaClass(Type.class);
            case "System.Decimal" -> fromJavaClass(Decimal.class);
            case "System.DateTime" -> fromJavaClass(DateTime.class);
            case "System.OverflowException" -> fromJavaClass(OverflowException.class);
            case "System.InvalidCastException" -> fromJavaClass(InvalidCastException.class);
            case "System.InvalidOperationException" -> fromJavaClass(InvalidOperationException.class);
            case "System.IO.FileLoadException" -> fromJavaClass(FileLoadException.class);
            case "System.FormatException" -> fromJavaClass(FormatException.class);
            case "System.Globalization.NumberStyles" -> fromJavaClass(NumberStyles.class);
            case "System.Globalization.CultureNotFoundException" -> fromJavaClass(CultureNotFoundException.class);
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
            case "System.String*[]" -> fromJavaClass(String.class).MakePointerType().MakeArrayType();
            case "System.String*&" -> fromJavaClass(String.class).MakePointerType().MakeByRefType();
            case "System.String**" -> fromJavaClass(String.class).MakePointerType().MakePointerType();
            case "System.String&[]" -> throw new TypeLoadException("Array element cannot be by-reference");
            case "System.Int32*" -> fromJavaClass(Int32.class).MakePointerType();
            case "System.Int32[]" -> fromJavaClass(int[].class);
            case "System.Collections.Generic.List`1[System.String]",
                    "System.Collections.Generic.List`1[[System.String, System.Private.CoreLib]]" ->
                    fromJavaClass(java.util.List.class).MakeGenericType(new Type[] {fromJavaClass(String.class)});
            case "System.Collections.Generic.Dictionary`2[System.String,System.Int32]",
                    "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Int32, System.Private.CoreLib]]" ->
                    fromJavaClass(java.util.Map.class).MakeGenericType(
                            new Type[] {fromJavaClass(String.class), fromJavaClass(Int32.class)});
            case "System.Collections.Generic.Dictionary`2[System.Int32,System.String]" ->
                    fromJavaClass(java.util.Map.class).MakeGenericType(
                            new Type[] {fromJavaClass(Int32.class), fromJavaClass(String.class)});
            case "System.Collections.Generic.List`1[System.String][]" ->
                    arrayOf(fromJavaClass(java.util.List.class)
                            .MakeGenericType(new Type[] {fromJavaClass(String.class)}), 1);
            case "system.string" -> ignoreCase ? fromJavaClass(String.class) : null;
            case "system.int32" -> ignoreCase ? fromJavaClass(Int32.class) : null;
            case "system.object" -> ignoreCase ? fromJavaClass(Object.class) : null;
            case "system.valuetype" -> ignoreCase ? fromJavaClass(Number.class) : null;
            case "system.array" -> ignoreCase ? fromJavaClass(java.lang.reflect.Array.class) : null;
            case "system.idisposable" -> ignoreCase ? fromJavaClass(IDisposable.class) : null;
            case "system.icomparable" -> ignoreCase ? fromJavaClass(IComparable.class) : null;
            case "system.iformattable" -> ignoreCase ? fromJavaClass(IFormattable.class) : null;
            case "system.ispanformattable" -> ignoreCase ? fromJavaClass(ISpanFormattable.class) : null;
            case "system.iutf8spanformattable" -> ignoreCase ? fromJavaClass(IUtf8SpanFormattable.class) : null;
            case "system.iformatprovider" -> ignoreCase ? fromJavaClass(IFormatProvider.class) : null;
            case "system.iconvertible" -> ignoreCase ? fromJavaClass(IConvertible.class) : null;
            case "system.typecode" -> ignoreCase ? fromJavaClass(TypeCode.class) : null;
            case "system.type" -> ignoreCase ? fromJavaClass(Type.class) : null;
            case "system.decimal" -> ignoreCase ? fromJavaClass(Decimal.class) : null;
            case "system.datetime" -> ignoreCase ? fromJavaClass(DateTime.class) : null;
            case "system.overflowexception" -> ignoreCase ? fromJavaClass(OverflowException.class) : null;
            case "system.invalidcastexception" -> ignoreCase ? fromJavaClass(InvalidCastException.class) : null;
            case "system.invalidoperationexception" -> ignoreCase
                    ? fromJavaClass(InvalidOperationException.class) : null;
            case "system.io.fileloadexception" -> ignoreCase ? fromJavaClass(FileLoadException.class) : null;
            case "system.formatexception" -> ignoreCase ? fromJavaClass(FormatException.class) : null;
            case "system.globalization.numberstyles" -> ignoreCase ? fromJavaClass(NumberStyles.class) : null;
            case "system.globalization.culturenotfoundexception" -> ignoreCase
                    ? fromJavaClass(CultureNotFoundException.class) : null;
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
            case "system.string*[]" -> ignoreCase
                    ? fromJavaClass(String.class).MakePointerType().MakeArrayType() : null;
            case "system.string*&" -> ignoreCase
                    ? fromJavaClass(String.class).MakePointerType().MakeByRefType() : null;
            case "system.string**" -> ignoreCase
                    ? fromJavaClass(String.class).MakePointerType().MakePointerType() : null;
            case "system.string&[]" -> {
                if (ignoreCase) {
                    throw new TypeLoadException("Array element cannot be by-reference");
                }
                yield null;
            }
            case "system.int32*" -> ignoreCase ? fromJavaClass(Int32.class).MakePointerType() : null;
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
        if (this.get_IsByRef()) {
            throw new TypeLoadException("Cannot make an array of a by-reference type");
        }
        if (this == fromJavaClass(String.class)) {
            return fromJavaClass(String[].class);
        }
        if (this == fromJavaClass(Int32.class)) {
            return fromJavaClass(int[].class);
        }
        if (this == fromJavaClass(String[].class)) {
            return fromJavaClass(String[][].class);
        }
        return arrayOf(this, 1);
    }

    public Type MakeArrayType(int rank) {
        if (this.get_IsByRef()) {
            throw new TypeLoadException("Cannot make an array of a by-reference type");
        }
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
            throw new InvalidOperationException("Not a generic type");
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

    public Type[] GetGenericParameterConstraints() {
        if (!this.get_IsGenericParameter()) {
            throw new InvalidOperationException("Not a generic parameter");
        }
        return new Type[0];
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
        if (this.definition == Int32.class) return "Int32";
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
        if (this.definition == String.class || this.definition == Int32.class
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
        if (this.definition == Int32.class) {
            return fromJavaClass(Number.class);
        }
        if (this.definition == Decimal.class || this.definition == DateTime.class) {
            return fromJavaClass(Number.class);
        }
        if (this.definition == MemberTypes.class || this.definition == TypeCode.class
                || this.definition == NumberStyles.class) {
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
                && (this.definition == Int32.class || this.definition == Decimal.class
                        || this.definition == DateTime.class
                        || this.definition == MemberTypes.class
                        || this.definition == TypeCode.class || this.definition == NumberStyles.class);
    }

    public boolean get_IsPrimitive() {
        return this.definition == Int32.class;
    }

    public boolean get_IsAbstract() {
        return this.definition == Type.class || this.definition == Number.class
                || this.definition == Enum.class || this.definition == java.lang.reflect.Array.class
                || this.get_IsInterface();
    }

    public boolean get_IsSealed() {
        return this.definition == String.class || this.definition == Int32.class
                || this.definition == Decimal.class || this.definition == DateTime.class
                || this.get_IsEnum();
    }

    public boolean get_IsPublic() {
        return this.parameterIndex >= 0 || this instanceof ArrayType
                || this.get_IsByRef() || this.get_IsPointer()
                || java.lang.reflect.Modifier.isPublic(this.definition.getModifiers());
    }

    public boolean get_IsVisible() {
        return this.get_IsPublic();
    }

    public boolean get_IsClass() {
        return !this.get_IsValueType() && !this.get_IsInterface();
    }

    public boolean get_IsInterface() {
        return this.definition == IDisposable.class || this.definition == IComparable.class
                || this.definition == IFormattable.class || this.definition == IFormatProvider.class
                || this.definition == IConvertible.class || this.definition == ISpanFormattable.class
                || this.definition == IUtf8SpanFormattable.class;
    }

    public boolean get_IsEnum() {
        return this.definition == MemberTypes.class || this.definition == TypeCode.class
                || this.definition == NumberStyles.class;
    }

    public Type GetEnumUnderlyingType() {
        if (!this.get_IsEnum()) {
            throw new ArgumentException("Type must be an enum");
        }
        return fromJavaClass(Int32.class);
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
        if (this.definition == IComparable.class && candidate.definition == Int32.class) {
            return true;
        }
        if (this.definition == IFormattable.class && candidate.definition == Int32.class) {
            return true;
        }
        if (this.definition == IConvertible.class && candidate.definition == Int32.class) {
            return true;
        }
        if (this.definition == ISpanFormattable.class && candidate.definition == Int32.class) {
            return true;
        }
        if (this.definition == IUtf8SpanFormattable.class && candidate.definition == Int32.class) {
            return true;
        }
        if (this.definition == IFormattable.class && candidate.definition == ISpanFormattable.class) {
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
            return value instanceof Integer || value instanceof Int32
                    || value instanceof Decimal || value instanceof DateTime
                    || value instanceof MemberTypes || value instanceof TypeCode
                    || value instanceof NumberStyles;
        }
        if (this.definition == Enum.class) {
            return value instanceof MemberTypes || value instanceof TypeCode
                    || value instanceof NumberStyles;
        }
        if (this.definition == IComparable.class) {
            return value instanceof String || value instanceof Integer || value instanceof Int32;
        }
        if (this.definition == IFormattable.class) {
            return value instanceof Integer || value instanceof Int32;
        }
        if (this.definition == IConvertible.class) {
            return value instanceof Integer || value instanceof Int32;
        }
        if (this.definition == ISpanFormattable.class) {
            return value instanceof Integer || value instanceof Int32;
        }
        if (this.definition == IUtf8SpanFormattable.class) {
            return value instanceof Integer || value instanceof Int32;
        }
        if (this.definition == Int32.class && value instanceof Integer) {
            return true;
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
        if (this.definition == Object.class || this.definition == IDisposable.class
                || this.definition == IUtf8SpanFormattable.class) {
            return new Type[0];
        }
        if (this.definition == ISpanFormattable.class) {
            return new Type[] {fromJavaClass(IFormattable.class)};
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
        if (this.definition == Int32.class) {
            if (fullname.equals("System.IUtf8SpanFormattable")
                    || fullname.equals("IUtf8SpanFormattable")) {
                return fromJavaClass(IUtf8SpanFormattable.class);
            }
            if (fullname.equals("system.iutf8spanformattable")) {
                return null;
            }
            if (fullname.equals("System.ISpanFormattable") || fullname.equals("ISpanFormattable")) {
                return fromJavaClass(ISpanFormattable.class);
            }
            if (fullname.equals("system.ispanformattable")) {
                return null;
            }
            if (fullname.equals("System.IComparable") || fullname.equals("IComparable")) {
                return fromJavaClass(IComparable.class);
            }
            if (fullname.equals("system.icomparable")) {
                return null;
            }
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

    public boolean get_IsSZArray() {
        if (this instanceof ArrayType array) {
            return array.vector;
        }
        return this.definition.isArray();
    }

    public boolean get_IsVariableBoundArray() {
        return this.get_IsArray() && !this.get_IsSZArray();
    }

    public boolean get_HasElementType() {
        return this.GetElementType() != null;
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

    public boolean get_IsGenericTypeDefinition() {
        return this.get_IsGenericType() && this.arguments.isEmpty();
    }

    public boolean get_ContainsGenericParameters() {
        if (this.get_IsGenericParameter() || this.get_IsGenericTypeDefinition()) {
            return true;
        }
        for (Type argument : this.arguments) {
            if (argument.get_ContainsGenericParameters()) {
                return true;
            }
        }
        if (this.get_IsArray() || this.get_IsByRef() || this.get_IsPointer()) {
            Type element = this.GetElementType();
            return element != null && element.get_ContainsGenericParameters();
        }
        return false;
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
