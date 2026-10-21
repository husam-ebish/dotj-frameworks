// SPDX-License-Identifier: MIT

package System;

import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.ConcurrentHashMap;
import System.IO.FileNotFoundException;
import System.IO.FileLoadException;
import System.IO.IOException;
import System.Reflection.MemberInfo;
import System.Reflection.MethodBase;
import System.Reflection.MethodInfo;
import System.Reflection.MemberTypes;
import System.Reflection.BindingFlags;
import System.Reflection.GenericParameterAttributes;
import System.Globalization.NumberStyles;
import System.Globalization.CultureNotFoundException;

/** Bounded candidate for closed generic identity; not a complete System.Type surface. */
public abstract class Type extends MemberInfo {
    private static final String CORELIB_IDENTITY = "System.Private.CoreLib, Version=10.0.0.0, "
            + "Culture=neutral, PublicKeyToken=7cec85d7bea7798e";
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
    public static TypeCode GetTypeCode(Type type) {
        if (type == null) {
            return TypeCode.Empty;
        }
        if (type.get_IsEnum()) {
            return GetTypeCode(type.GetEnumUnderlyingType());
        }
        if (type.definition == String.class) return TypeCode.String;
        if (type.definition == Boolean.class || type.definition == boolean.class) return TypeCode.Boolean;
        if (type.definition == Character.class || type.definition == char.class) return TypeCode.Char;
        if (type.definition == Byte.class || type.definition == byte.class) return TypeCode.Byte;
        if (type.definition == Short.class || type.definition == short.class) return TypeCode.Int16;
        if (type.definition == Int32.class) return TypeCode.Int32;
        if (type.definition == Long.class || type.definition == long.class) return TypeCode.Int64;
        if (type.definition == Float.class || type.definition == float.class) return TypeCode.Single;
        if (type.definition == Double.class || type.definition == double.class) return TypeCode.Double;
        if (type.definition == Decimal.class) return TypeCode.Decimal;
        if (type.definition == DateTime.class) return TypeCode.DateTime;
        return TypeCode.Object;
    }

    public static Type[] GetTypeArray(Object[] args) {
        if (args == null) {
            throw new ArgumentNullException("args");
        }
        Type[] types = new Type[args.length];
        for (int index = 0; index < args.length; index++) {
            if (args[index] == null) {
                throw new ArgumentException("Array element cannot be null", "args");
            }
            types[index] = fromJavaClass(args[index].getClass());
        }
        return types;
    }

    public int GetHashCode() {
        return this.hashCode();
    }

    public static Type GetType(String typeName) {
        return GetType(typeName, false, false);
    }

    public static Type GetType(String typeName, boolean throwOnError) {
        return GetType(typeName, throwOnError, false);
    }

    private static boolean isEscapedAt(String text, int index) {
        int backslashes = 0;
        for (int previous = index - 1; previous >= 0 && text.charAt(previous) == '\\'; previous--) {
            backslashes++;
        }
        return (backslashes & 1) != 0;
    }

    private static java.util.ArrayList<String> splitAssemblyParts(String assembly) {
        java.util.ArrayList<String> parts = new java.util.ArrayList<>();
        StringBuilder part = new StringBuilder();
        char quote = 0;
        for (int offset = 0; offset < assembly.length(); offset++) {
            char character = assembly.charAt(offset);
            if ((character == '"' || character == '\'')
                    && !isEscapedAt(assembly, offset)
                    && (quote == 0 || quote == character)) {
                quote = quote == 0 ? character : 0;
            }
            if (character == ',' && quote == 0 && !isEscapedAt(assembly, offset)) {
                parts.add(part.toString());
                part.setLength(0);
            } else {
                part.append(character);
            }
        }
        parts.add(part.toString());
        return parts;
    }

    private static Type resolveSelectedCoreLibGeneric(String name, boolean ignoreCase) {
        if (name.endsWith("&")) {
            Type element = resolveSelectedCoreLibGeneric(name.substring(0, name.length() - 1), ignoreCase);
            return element == null ? null : element.MakeByRefType();
        }
        if (name.endsWith("*")) {
            Type element = resolveSelectedCoreLibGeneric(name.substring(0, name.length() - 1), ignoreCase);
            return element == null ? null : element.MakePointerType();
        }
        if (name.endsWith("[]")) {
            Type element = resolveSelectedCoreLibGeneric(name.substring(0, name.length() - 2), ignoreCase);
            return element == null ? null : element.MakeArrayType();
        }
        if (name.endsWith("[,]")) {
            Type element = resolveSelectedCoreLibGeneric(name.substring(0, name.length() - 3), ignoreCase);
            return element == null ? null : element.MakeArrayType(2);
        }
        if (name.endsWith("[,,]")) {
            Type element = resolveSelectedCoreLibGeneric(name.substring(0, name.length() - 4), ignoreCase);
            return element == null ? null : element.MakeArrayType(3);
        }
        if (name.endsWith("[*]")) {
            Type element = resolveSelectedCoreLibGeneric(name.substring(0, name.length() - 3), ignoreCase);
            return element == null ? null : element.MakeArrayType(1);
        }
        int start = name.indexOf("[[");
        if (start < 0 || !name.endsWith("]]")) {
            return null;
        }
        String definitionName = name.substring(0, start);
        if (ignoreCase && !definitionName.chars().allMatch(character -> character < 128)) {
            return null;
        }
        String selectedDefinition = ignoreCase ? definitionName.toLowerCase(Locale.ROOT) : definitionName;
        int arity = switch (selectedDefinition) {
            case "System.Collections.Generic.List`1", "system.collections.generic.list`1" -> 1;
            case "System.Collections.Generic.Dictionary`2", "system.collections.generic.dictionary`2" -> 2;
            case "System.Collections.Generic.Dictionary`2+Entry",
                    "system.collections.generic.dictionary`2+entry" -> 2;
            default -> 0;
        };
        if (arity == 0) {
            return null;
        }
        String argumentText = name.substring(start + 2, name.length() - 2);
        java.util.ArrayList<String> argumentNames = new java.util.ArrayList<>();
        int depth = 0;
        int argumentStart = 0;
        for (int offset = 0; offset < argumentText.length(); offset++) {
            char character = argumentText.charAt(offset);
            if (character == '[') {
                depth++;
            } else if (character == ']') {
                if (depth > 0) {
                    depth--;
                } else if (argumentText.startsWith("],[", offset)) {
                    argumentNames.add(argumentText.substring(argumentStart, offset));
                    offset += 2;
                    argumentStart = offset + 1;
                } else {
                    return null;
                }
            }
        }
        if (depth != 0) {
            return null;
        }
        argumentNames.add(argumentText.substring(argumentStart));
        if (argumentNames.size() != arity) {
            if (selectedDefinition.endsWith("+Entry") || selectedDefinition.endsWith("+entry")) {
                throw new ArgumentException("Generic argument count does not match nested type arity");
            }
            return null;
        }
        Type[] arguments = new Type[arity];
        for (int index = 0; index < arity; index++) {
            String argumentName = argumentNames.get(index);
            Type argument = GetType(argumentName, false, ignoreCase);
            String canonicalName = argument == null ? null : argument.get_AssemblyQualifiedName();
            if (canonicalName == null || ignoreCase
                    && (!argumentName.chars().allMatch(character -> character < 128)
                            || !argumentName.equalsIgnoreCase(canonicalName))
                    || !ignoreCase && !argumentName.equals(canonicalName)) {
                return null;
            }
            arguments[index] = argument;
        }
        String canonicalDefinitionName = arity == 1
                ? "System.Collections.Generic.List`1"
                : selectedDefinition.endsWith("+Entry") || selectedDefinition.endsWith("+entry")
                        ? "System.Collections.Generic.Dictionary`2+Entry"
                        : "System.Collections.Generic.Dictionary`2";
        return GetType(canonicalDefinitionName).MakeGenericType(arguments);
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
            java.util.ArrayList<String> attributes = splitAssemblyParts(assembly);
            String assemblyName = attributes.get(0).trim();
            if (assemblyName.equalsIgnoreCase("\"System.Private.CoreLib,Extra\"")
                    || assemblyName.equalsIgnoreCase("'System.Private.CoreLib,Extra'")) {
                assemblyName = "System.Private.CoreLib";
            }
            if (assemblyName.isEmpty() && assembly.indexOf(',') >= 0) {
                if (throwOnError) {
                    throw new ArgumentException("Invalid assembly name",
                            "typeName@" + typeName.indexOf(',', assemblySeparator + 1));
                }
                return null;
            }
            boolean endsDoubleQuote = assemblyName.endsWith("\"")
                    && !isEscapedAt(assemblyName, assemblyName.length() - 1);
            boolean endsSingleQuote = assemblyName.endsWith("'")
                    && !isEscapedAt(assemblyName, assemblyName.length() - 1);
            if (assemblyName.startsWith("\"") != endsDoubleQuote
                    || assemblyName.startsWith("'") != endsSingleQuote) {
                throw new FileLoadException("Unbalanced assembly name quotes: " + assembly);
            }
            if (assemblyName.indexOf('=') >= 0 && !assemblyName.startsWith("\"")
                    && !assemblyName.startsWith("'")) {
                throw new FileLoadException("Invalid assembly name: " + assembly);
            }
            if (assemblyName.length() >= 2
                    && (assemblyName.startsWith("\"") && assemblyName.endsWith("\"")
                            || assemblyName.startsWith("'") && assemblyName.endsWith("'"))) {
                assemblyName = assemblyName.substring(1, assemblyName.length() - 1);
            }
            if (assemblyName.equalsIgnoreCase("System.Private.CoreLib\\,Extra")) {
                assemblyName = "System.Private.CoreLib";
            }
            boolean asciiAssemblyName = assemblyName.chars().allMatch(character -> character < 128);
            if (asciiAssemblyName && assemblyName.equalsIgnoreCase("System.Private.CoreLib.dll")) {
                assemblyName = assemblyName.substring(0, assemblyName.length() - 4);
            }
            boolean knownAssembly = asciiAssemblyName
                    && (assemblyName.equalsIgnoreCase("System.Private.CoreLib")
                            || assemblyName.equalsIgnoreCase("mscorlib"));
                java.util.HashSet<String> seen = new java.util.HashSet<>();
                String invalidCulture = null;
                for (int index = 1; index < attributes.size(); index++) {
                    String[] attribute = attributes.get(index).trim().split("=", 2);
                    String key = attribute[0].trim().toLowerCase(Locale.ROOT);
                    String value = attribute.length == 2 ? attribute[1].trim() : "";
                    boolean extraEquals = value.indexOf('=') >= 0;
                    boolean quotedValue = value.length() >= 2 && value.startsWith("\"")
                            && value.endsWith("\"");
                    if (quotedValue) {
                        value = value.substring(1, value.length() - 1);
                    }
                    boolean recognized = key.equals("version") || key.equals("culture")
                            || key.equals("publickeytoken") || key.equals("publickey")
                            || key.equals("processorarchitecture")
                            || key.equals("retargetable") || key.equals("contenttype");
                    if (attribute.length != 2 || key.isEmpty() || value.isEmpty() && !quotedValue
                            || extraEquals && (!quotedValue || recognized)
                            || value.contains("\"\"")
                            || !quotedValue && value.indexOf('"') >= 0
                            || recognized && !seen.add(key)
                            || recognized && !key.equals("culture")
                                    && !value.chars().allMatch(character -> character < 128)
                            || key.equals("publickey") && seen.contains("publickeytoken")
                            || key.equals("publickeytoken") && seen.contains("publickey")
                            || key.equals("version") && !value.matches("[0-9]+(\\.[0-9]+){1,3}")
                            || key.equals("publickeytoken") && !value.equalsIgnoreCase("null")
                                    && !value.matches("[0-9a-fA-F]{16}")
                            || key.equals("publickey") && !value.equalsIgnoreCase("null")
                                    && !value.matches("(?i)([0-9a-f]{2})+")
                            || key.equals("processorarchitecture")
                                    && !value.equalsIgnoreCase("MSIL")
                                    && !value.equalsIgnoreCase("X86")
                                    && !value.equalsIgnoreCase("Amd64")
                            || key.equals("retargetable")
                                    && !value.equalsIgnoreCase("Yes")
                                    && !value.equalsIgnoreCase("No")
                            || key.equals("contenttype")
                                    && !value.equalsIgnoreCase("WindowsRuntime")) {
                        throw new FileLoadException("Invalid assembly identity: " + assembly);
                    }
                    if (key.equals("version")) {
                        for (String component : value.split("\\.")) {
                            String significant = component.replaceFirst("^0+(?!$)", "");
                            if (significant.length() > 5 || Integer.parseInt(significant) > 65534) {
                                throw new FileLoadException("Invalid assembly version: " + assembly);
                            }
                        }
                    }
                    if (key.equals("culture") && (!value.isEmpty()
                            && !value.matches("[A-Za-z][A-Za-z0-9_]*(?:-[A-Za-z0-9_]+)*")
                            || value.equalsIgnoreCase("invariant") || value.equalsIgnoreCase("null"))) {
                        invalidCulture = value;
                    }
                }
                if (invalidCulture != null) {
                    throw new CultureNotFoundException("name", invalidCulture, "Culture is not supported");
                }
            if (knownAssembly) {
                name = typeName.substring(0, assemblySeparator).stripLeading();
            } else if (throwOnError) {
                throw new FileNotFoundException("Could not load assembly: " + assembly);
            }
        }
        String key = ignoreCase ? name.toLowerCase(Locale.ROOT) : name;
        Type resolved = switch (key) {
            case "System.String" -> fromJavaClass(String.class);
            case "System.Boolean" -> fromJavaClass(Boolean.class);
            case "System.Char" -> fromJavaClass(Character.class);
            case "System.Int16" -> fromJavaClass(Short.class);
            case "System.Int64" -> fromJavaClass(Long.class);
            case "System.Single" -> fromJavaClass(Float.class);
            case "System.Double" -> fromJavaClass(Double.class);
            case "System.Byte" -> fromJavaClass(Byte.class);
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
            case "System.Reflection.MemberInfo" -> fromJavaClass(MemberInfo.class);
            case "System.Reflection.MethodBase" -> fromJavaClass(MethodBase.class);
            case "System.Reflection.MethodInfo" -> fromJavaClass(MethodInfo.class);
            case "System.Void" -> fromJavaClass(Void.class);
            case "System.Exception" -> fromJavaClass(Exception.class);
            case "System.SystemException" -> fromJavaClass(SystemException.class);
            case "System.ArgumentException" -> fromJavaClass(ArgumentException.class);
            case "System.ArgumentNullException" -> fromJavaClass(ArgumentNullException.class);
            case "System.TypeLoadException" -> fromJavaClass(TypeLoadException.class);
            case "System.IndexOutOfRangeException" -> fromJavaClass(IndexOutOfRangeException.class);
            case "System.IO.IOException" -> fromJavaClass(IOException.class);
            case "System.IO.FileNotFoundException" -> fromJavaClass(FileNotFoundException.class);
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
            case "System.Reflection.BindingFlags" -> fromJavaClass(BindingFlags.class);
            case "System.Reflection.GenericParameterAttributes" ->
                    fromJavaClass(GenericParameterAttributes.class);
            case "System.Enum" -> fromJavaClass(Enum.class);
            case "System.Collections.Generic.List`1" -> fromJavaClass(java.util.List.class);
            case "System.Collections.Generic.Dictionary`2" -> fromJavaClass(java.util.Map.class);
            case "System.Collections.Generic.Dictionary`2+Entry" ->
                    fromJavaClass(java.util.Map.Entry.class);
            case "System.Collections.Generic.Dictionary`2+Entry[]" ->
                    fromJavaClass(java.util.Map.Entry.class).MakeArrayType();
            case "System.String[]" -> fromJavaClass(String[].class);
            case "System.Boolean[]" -> fromJavaClass(Boolean.class).MakeArrayType();
            case "System.Char[]" -> fromJavaClass(Character.class).MakeArrayType();
            case "System.Byte[]" -> fromJavaClass(Byte.class).MakeArrayType();
            case "System.Int16[]" -> fromJavaClass(Short.class).MakeArrayType();
            case "System.Int64[]" -> fromJavaClass(Long.class).MakeArrayType();
            case "System.Single[]" -> fromJavaClass(Float.class).MakeArrayType();
            case "System.Double[]" -> fromJavaClass(Double.class).MakeArrayType();
            case "System.Boolean[,]" -> fromJavaClass(Boolean.class).MakeArrayType(2);
            case "System.Char[,]" -> fromJavaClass(Character.class).MakeArrayType(2);
            case "System.Byte[,]" -> fromJavaClass(Byte.class).MakeArrayType(2);
            case "System.Int16[,]" -> fromJavaClass(Short.class).MakeArrayType(2);
            case "System.Int64[,]" -> fromJavaClass(Long.class).MakeArrayType(2);
            case "System.Single[,]" -> fromJavaClass(Float.class).MakeArrayType(2);
            case "System.Double[,]" -> fromJavaClass(Double.class).MakeArrayType(2);
            case "System.Boolean[,,]" -> fromJavaClass(Boolean.class).MakeArrayType(3);
            case "System.Char[,,]" -> fromJavaClass(Character.class).MakeArrayType(3);
            case "System.Byte[,,]" -> fromJavaClass(Byte.class).MakeArrayType(3);
            case "System.Int16[,,]" -> fromJavaClass(Short.class).MakeArrayType(3);
            case "System.Int64[,,]" -> fromJavaClass(Long.class).MakeArrayType(3);
            case "System.Single[,,]" -> fromJavaClass(Float.class).MakeArrayType(3);
            case "System.Double[,,]" -> fromJavaClass(Double.class).MakeArrayType(3);
            case "System.Boolean[*]" -> fromJavaClass(Boolean.class).MakeArrayType(1);
            case "System.Char[*]" -> fromJavaClass(Character.class).MakeArrayType(1);
            case "System.Byte[*]" -> fromJavaClass(Byte.class).MakeArrayType(1);
            case "System.Int16[*]" -> fromJavaClass(Short.class).MakeArrayType(1);
            case "System.Int64[*]" -> fromJavaClass(Long.class).MakeArrayType(1);
            case "System.Single[*]" -> fromJavaClass(Float.class).MakeArrayType(1);
            case "System.Double[*]" -> fromJavaClass(Double.class).MakeArrayType(1);
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
            case "system.boolean" -> ignoreCase ? fromJavaClass(Boolean.class) : null;
            case "system.char" -> ignoreCase ? fromJavaClass(Character.class) : null;
            case "system.byte" -> ignoreCase ? fromJavaClass(Byte.class) : null;
            case "system.int16" -> ignoreCase ? fromJavaClass(Short.class) : null;
            case "system.int64" -> ignoreCase ? fromJavaClass(Long.class) : null;
            case "system.single" -> ignoreCase ? fromJavaClass(Float.class) : null;
            case "system.double" -> ignoreCase ? fromJavaClass(Double.class) : null;
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
            case "system.reflection.memberinfo" -> ignoreCase ? fromJavaClass(MemberInfo.class) : null;
            case "system.reflection.methodbase" -> ignoreCase ? fromJavaClass(MethodBase.class) : null;
            case "system.reflection.methodinfo" -> ignoreCase ? fromJavaClass(MethodInfo.class) : null;
            case "system.void" -> ignoreCase ? fromJavaClass(Void.class) : null;
            case "system.exception" -> ignoreCase ? fromJavaClass(Exception.class) : null;
            case "system.systemexception" -> ignoreCase ? fromJavaClass(SystemException.class) : null;
            case "system.argumentexception" -> ignoreCase ? fromJavaClass(ArgumentException.class) : null;
            case "system.argumentnullexception" -> ignoreCase ? fromJavaClass(ArgumentNullException.class) : null;
            case "system.typeloadexception" -> ignoreCase ? fromJavaClass(TypeLoadException.class) : null;
            case "system.indexoutofrangeexception" -> ignoreCase ? fromJavaClass(IndexOutOfRangeException.class) : null;
            case "system.io.ioexception" -> ignoreCase ? fromJavaClass(IOException.class) : null;
            case "system.io.filenotfoundexception" -> ignoreCase ? fromJavaClass(FileNotFoundException.class) : null;
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
            case "system.reflection.bindingflags" -> ignoreCase ? fromJavaClass(BindingFlags.class) : null;
            case "system.reflection.genericparameterattributes" -> ignoreCase
                    ? fromJavaClass(GenericParameterAttributes.class) : null;
            case "system.enum" -> ignoreCase ? fromJavaClass(Enum.class) : null;
            case "system.collections.generic.list`1" -> ignoreCase ? fromJavaClass(java.util.List.class) : null;
            case "system.collections.generic.dictionary`2" -> ignoreCase ? fromJavaClass(java.util.Map.class) : null;
            case "system.collections.generic.dictionary`2+entry" -> ignoreCase
                    ? fromJavaClass(java.util.Map.Entry.class) : null;
            case "system.collections.generic.dictionary`2+entry[]" -> ignoreCase
                    ? fromJavaClass(java.util.Map.Entry.class).MakeArrayType() : null;
            case "system.string[]" -> ignoreCase ? fromJavaClass(String[].class) : null;
            case "system.boolean[]" -> ignoreCase ? fromJavaClass(Boolean.class).MakeArrayType() : null;
            case "system.char[]" -> ignoreCase ? fromJavaClass(Character.class).MakeArrayType() : null;
            case "system.byte[]" -> ignoreCase ? fromJavaClass(Byte.class).MakeArrayType() : null;
            case "system.int16[]" -> ignoreCase ? fromJavaClass(Short.class).MakeArrayType() : null;
            case "system.int64[]" -> ignoreCase ? fromJavaClass(Long.class).MakeArrayType() : null;
            case "system.single[]" -> ignoreCase ? fromJavaClass(Float.class).MakeArrayType() : null;
            case "system.double[]" -> ignoreCase ? fromJavaClass(Double.class).MakeArrayType() : null;
            case "system.boolean[,]" -> ignoreCase ? fromJavaClass(Boolean.class).MakeArrayType(2) : null;
            case "system.char[,]" -> ignoreCase ? fromJavaClass(Character.class).MakeArrayType(2) : null;
            case "system.byte[,]" -> ignoreCase ? fromJavaClass(Byte.class).MakeArrayType(2) : null;
            case "system.int16[,]" -> ignoreCase ? fromJavaClass(Short.class).MakeArrayType(2) : null;
            case "system.int64[,]" -> ignoreCase ? fromJavaClass(Long.class).MakeArrayType(2) : null;
            case "system.single[,]" -> ignoreCase ? fromJavaClass(Float.class).MakeArrayType(2) : null;
            case "system.double[,]" -> ignoreCase ? fromJavaClass(Double.class).MakeArrayType(2) : null;
            case "system.boolean[,,]" -> ignoreCase ? fromJavaClass(Boolean.class).MakeArrayType(3) : null;
            case "system.char[,,]" -> ignoreCase ? fromJavaClass(Character.class).MakeArrayType(3) : null;
            case "system.byte[,,]" -> ignoreCase ? fromJavaClass(Byte.class).MakeArrayType(3) : null;
            case "system.int16[,,]" -> ignoreCase ? fromJavaClass(Short.class).MakeArrayType(3) : null;
            case "system.int64[,,]" -> ignoreCase ? fromJavaClass(Long.class).MakeArrayType(3) : null;
            case "system.single[,,]" -> ignoreCase ? fromJavaClass(Float.class).MakeArrayType(3) : null;
            case "system.double[,,]" -> ignoreCase ? fromJavaClass(Double.class).MakeArrayType(3) : null;
            case "system.boolean[*]" -> ignoreCase ? fromJavaClass(Boolean.class).MakeArrayType(1) : null;
            case "system.char[*]" -> ignoreCase ? fromJavaClass(Character.class).MakeArrayType(1) : null;
            case "system.byte[*]" -> ignoreCase ? fromJavaClass(Byte.class).MakeArrayType(1) : null;
            case "system.int16[*]" -> ignoreCase ? fromJavaClass(Short.class).MakeArrayType(1) : null;
            case "system.int64[*]" -> ignoreCase ? fromJavaClass(Long.class).MakeArrayType(1) : null;
            case "system.single[*]" -> ignoreCase ? fromJavaClass(Float.class).MakeArrayType(1) : null;
            case "system.double[*]" -> ignoreCase ? fromJavaClass(Double.class).MakeArrayType(1) : null;
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
            default -> resolveSelectedCoreLibGeneric(name, ignoreCase);
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
            if (this.definition == java.util.Map.class
                    || this.definition == java.util.Map.Entry.class) {
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
        if (this.definition == Boolean.class) return "Boolean";
        if (this.definition == Character.class) return "Char";
        if (this.definition == Short.class) return "Int16";
        if (this.definition == Long.class) return "Int64";
        if (this.definition == Float.class) return "Single";
        if (this.definition == Double.class) return "Double";
        if (this.definition == Byte.class) return "Byte";
        if (this.definition == Void.class) return "Void";
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
        Type declaring = this.get_DeclaringType();
        String baseName = declaring == null
                ? this.get_Namespace() + "." + this.get_Name()
                : declaring.get_FullName() + "+" + this.get_Name();
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
            constructed.append('[').append(argument).append(", ")
                    .append(CORELIB_IDENTITY).append(']');
        }
        return constructed.append(']').toString();
    }

    public String get_AssemblyQualifiedName() {
        String fullName = this.get_FullName();
        return fullName == null ? null : fullName + ", " + CORELIB_IDENTITY;
    }

    public String get_Namespace() {
        if (this instanceof ArrayType array) {
            return array.elementType.get_Namespace();
        }
        if (this.get_IsByRef() || this.get_IsPointer() || this.definition.isArray()) {
            return this.GetElementType().get_Namespace();
        }
        if (this.parameterIndex < 0 && this.definition.getDeclaringClass() != null) {
            return fromJavaClass(this.definition.getDeclaringClass()).get_Namespace();
        }
        if (this.definition == java.util.List.class || this.definition == java.util.Map.class) {
            return "System.Collections.Generic";
        }
        if (this.definition == String.class || this.definition == Boolean.class
                || this.definition == Character.class
                || this.definition == Short.class
                || this.definition == Long.class
                || this.definition == Float.class
                || this.definition == Double.class
                || this.definition == Byte.class
                || this.definition == Void.class
                || this.definition == Int32.class
                || this.definition == Object.class || this.definition == Number.class
                || this.definition == java.lang.reflect.Array.class || this.definition == Enum.class) {
            return "System";
        }
        return this.definition.getPackageName();
    }

    @Override
    public Type get_DeclaringType() {
        if (this.parameterIndex >= 0) {
            return fromJavaClass(this.definition);
        }
        Class<?> declaring = this.get_HasElementType() ? null : this.definition.getDeclaringClass();
        return declaring == null ? null : fromJavaClass(declaring);
    }

    @Override
    public Type get_ReflectedType() {
        return this.get_DeclaringType();
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
        if (this.definition == Int32.class || this.definition == Void.class
                || this.definition == Boolean.class
                || this.definition == Character.class || this.definition == Short.class
                || this.definition == Long.class || this.definition == Float.class
                || this.definition == Double.class || this.definition == Byte.class) {
            return fromJavaClass(Number.class);
        }
        if (this.definition == Decimal.class || this.definition == DateTime.class) {
            return fromJavaClass(Number.class);
        }
        if (this.definition == MemberTypes.class || this.definition == BindingFlags.class
                || this.definition == GenericParameterAttributes.class
                || this.definition == TypeCode.class
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

    public Type get_UnderlyingSystemType() {
        return this;
    }

    public boolean get_IsValueType() {
        return this.parameterIndex < 0
                && (this.definition == Int32.class || this.definition == Void.class
                        || this.definition == Boolean.class
                        || this.definition == Character.class
                        || this.definition == Short.class
                        || this.definition == Long.class
                        || this.definition == Float.class
                        || this.definition == Double.class
                        || this.definition == Byte.class
                        || this.definition == Decimal.class
                        || this.definition == DateTime.class
                        || this.definition == MemberTypes.class
                        || this.definition == BindingFlags.class
                        || this.definition == GenericParameterAttributes.class
                        || this.definition == TypeCode.class || this.definition == NumberStyles.class);
    }

    public boolean get_IsPrimitive() {
        return this.definition == Int32.class || this.definition == Void.class
                || this.definition == Boolean.class
                || this.definition == Character.class || this.definition == Short.class
                || this.definition == Long.class || this.definition == Float.class
                || this.definition == Double.class || this.definition == Byte.class;
    }

    public boolean get_IsAbstract() {
        return this.definition == Type.class || this.definition == Number.class
                || this.definition == Enum.class || this.definition == java.lang.reflect.Array.class
                || this.definition == MemberInfo.class || this.definition == MethodBase.class
                || this.definition == MethodInfo.class
                || this.get_IsInterface();
    }

    public boolean get_IsSealed() {
        return this.definition == String.class || this.definition == Boolean.class
                || this.definition == Character.class
                || this.definition == Short.class
                || this.definition == Long.class
                || this.definition == Float.class
                || this.definition == Double.class
                || this.definition == Byte.class
                || this.definition == Int32.class || this.definition == Void.class
                || this.definition == Decimal.class || this.definition == DateTime.class
                || this.get_IsEnum();
    }

    public boolean get_IsPublic() {
        return this.parameterIndex >= 0 || this instanceof ArrayType
                || this.get_IsByRef() || this.get_IsPointer()
                || !this.get_IsNested()
                        && java.lang.reflect.Modifier.isPublic(this.definition.getModifiers());
    }

    public boolean get_IsNotPublic() {
        return this.parameterIndex < 0 && !this.get_HasElementType()
                && !this.get_IsNested()
                && !java.lang.reflect.Modifier.isPublic(this.definition.getModifiers());
    }

    public boolean get_IsSerializable() {
        if (this.get_IsByRef() || this.get_IsPointer() || this.get_IsGenericParameter()) {
            return false;
        }
        if (this.get_IsArray()) {
            return true;
        }
        return this.definition == String.class || this.definition == Int32.class
                || this.definition == java.util.List.class || this.get_IsEnum()
                || Exception.class.isAssignableFrom(this.definition);
    }

    public boolean get_IsSpecialName() {
        return false;
    }

    public boolean get_IsAnsiClass() {
        return true;
    }

    public boolean get_IsUnicodeClass() {
        return false;
    }

    public boolean get_IsAutoClass() {
        return false;
    }

    public boolean get_IsAutoLayout() {
        return this.definition != Int32.class;
    }

    public boolean get_IsLayoutSequential() {
        return this.definition == Int32.class;
    }

    public boolean get_IsExplicitLayout() {
        return false;
    }

    public boolean get_IsImport() {
        return false;
    }

    public boolean get_IsCOMObject() {
        return false;
    }

    public boolean get_IsContextful() {
        return false;
    }

    public boolean get_IsMarshalByRef() {
        return false;
    }

    public boolean get_IsSignatureType() {
        return false;
    }

    public boolean get_IsFunctionPointer() {
        return false;
    }

    public boolean get_IsUnmanagedFunctionPointer() {
        return false;
    }

    public Type GetFunctionPointerReturnType() {
        throw new InvalidOperationException("Type is not a function pointer");
    }

    public Type[] GetFunctionPointerParameterTypes() {
        throw new InvalidOperationException("Type is not a function pointer");
    }

    public Type[] GetFunctionPointerCallingConventions() {
        throw new InvalidOperationException("Type is not a function pointer");
    }

    public boolean get_IsSecurityCritical() {
        return true;
    }

    public boolean get_IsSecuritySafeCritical() {
        return false;
    }

    public boolean get_IsSecurityTransparent() {
        return false;
    }

    @Override
    public MemberTypes get_MemberType() {
        return MemberTypes.TypeInfo;
    }

    public boolean get_IsVisible() {
        if (this.parameterIndex >= 0) {
            return true;
        }
        if (this.get_HasElementType()) {
            return this.GetElementType().get_IsVisible();
        }
        for (Type argument : this.arguments) {
            if (!argument.get_IsVisible()) {
                return false;
            }
        }
        if (this.get_IsNested()) {
            return this.get_IsNestedPublic() && this.get_DeclaringType().get_IsVisible();
        }
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
        return this.definition == MemberTypes.class || this.definition == BindingFlags.class
                || this.definition == GenericParameterAttributes.class
                || this.definition == TypeCode.class
                || this.definition == NumberStyles.class;
    }

    public Type GetEnumUnderlyingType() {
        if (!this.get_IsEnum()) {
            throw new ArgumentException("Type must be an enum", "enumType");
        }
        return fromJavaClass(Int32.class);
    }

    public String[] GetEnumNames() {
        if (!this.get_IsEnum()) {
            throw new ArgumentException("Type must be an enum", "enumType");
        }
        Object[] constants = this.enumConstants();
        String[] names = new String[constants.length];
        for (int index = 0; index < constants.length; index++) {
            names[index] = enumConstantName(constants[index]);
        }
        return names;
    }

    public Object[] GetEnumValues() {
        if (!this.get_IsEnum()) {
            throw new ArgumentException("Type must be an enum", "enumType");
        }
        return this.enumConstants();
    }

    public int[] GetEnumValuesAsUnderlyingType() {
        if (!this.get_IsEnum()) {
            throw new ArgumentException("Type must be an enum", "enumType");
        }
        Object[] constants = this.enumConstants();
        int[] values = new int[constants.length];
        for (int index = 0; index < constants.length; index++) {
            values[index] = enumNumericValue(constants[index]);
        }
        return values;
    }

    public boolean IsEnumDefined(Object value) {
        if (!this.get_IsEnum()) {
            throw new ArgumentException("Type must be an enum", "enumType");
        }
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        Object[] constants = this.enumConstants();
        if (value instanceof String name) {
            for (Object constant : constants) {
                if (enumConstantName(constant).equals(name)) {
                    return true;
                }
            }
            return false;
        }
        if (value.getClass() == this.definition) {
            if (value instanceof BindingFlags flags) {
                return flags.get_Name() != null;
            }
            if (value instanceof MemberTypes member) {
                return member.get_Name() != null;
            }
            return true;
        }
        if (value instanceof Integer number) {
            for (Object constant : constants) {
                if (enumNumericValue(constant) == number) {
                    return true;
                }
            }
            return false;
        }
        throw new ArgumentException("Value type must match the enum or its underlying type");
    }

    public String GetEnumName(Object value) {
        if (!this.get_IsEnum()) {
            throw new ArgumentException("Type must be an enum", "enumType");
        }
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        if (value instanceof String) {
            throw new ArgumentException("Value must be an enum or its underlying type", "value");
        }
        if (value.getClass() == this.definition) {
            if (value instanceof BindingFlags flags) {
                return flags.get_Name();
            }
            if (value instanceof MemberTypes member) {
                return member.get_Name();
            }
            return ((java.lang.Enum<?>) value).name();
        }
        if (value instanceof java.lang.Enum<?> || value instanceof BindingFlags
                || value instanceof MemberTypes) {
            return null;
        }
        if (value instanceof Integer || value instanceof Long
                || value instanceof Short || value instanceof Byte) {
            long number = ((Number) value).longValue();
            for (Object constant : this.enumConstants()) {
                if (enumNumericValue(constant) == number) {
                    return enumConstantName(constant);
                }
            }
            return null;
        }
        throw new ArgumentException("Value must be an enum or its underlying type", "value");
    }

    private Object[] enumConstants() {
        if (this.definition == BindingFlags.class) {
            return BindingFlags.values();
        }
        if (this.definition == MemberTypes.class) {
            return MemberTypes.values();
        }
        return this.definition.getEnumConstants();
    }

    private static String enumConstantName(Object constant) {
        if (constant instanceof BindingFlags flags) {
            return flags.get_Name();
        }
        if (constant instanceof MemberTypes member) {
            return member.get_Name();
        }
        return ((java.lang.Enum<?>) constant).name();
    }

    private static int enumNumericValue(Object constant) {
        if (constant instanceof TypeCode code) {
            return code.get_Value();
        }
        if (constant instanceof MemberTypes member) {
            return member.get_Value();
        }
        if (constant instanceof BindingFlags flags) {
            return flags.get_Value();
        }
        if (constant instanceof GenericParameterAttributes attributes) {
            return attributes.get_Value();
        }
        if (constant instanceof NumberStyles style) {
            return style.get_Value();
        }
        throw new UnsupportedOperationException("Enum value is not mapped for this candidate type");
    }

    public boolean IsAssignableTo(Type target) {
        return target != null && target.IsAssignableFrom(this);
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

    public MemberInfo[] GetMember(String name) {
        if (name == null) {
            throw new ArgumentNullException("name");
        }
        if (this.definition == String.class && name.equals("Chars")) {
            return new MemberInfo[] {new DefaultPropertyMember("Chars", this)};
        }
        if (this.definition == java.util.List.class && name.equals("Item")) {
            return new MemberInfo[] {new DefaultPropertyMember("Item", this)};
        }
        String interfaceMethod = this.selectedInterfaceMethodName();
        if (interfaceMethod != null && interfaceMethod.equals(name)) {
            return new MemberInfo[] {new DefaultMethodMember(interfaceMethod, this)};
        }
        if (interfaceMethod != null) {
            return new MemberInfo[0];
        }
        if (name.equals("Missing") || this.definition == String.class && name.equals("chars")) {
            return new MemberInfo[0];
        }
        throw new UnsupportedOperationException("Member lookup is not mapped for this candidate name");
    }

    public MemberInfo[] GetMember(String name, BindingFlags flags) {
        if (name == null) {
            throw new ArgumentNullException("name");
        }
        if (flags == null) {
            throw new NullPointerException("flags");
        }
        if (!flags.has(BindingFlags.Public) || !flags.has(BindingFlags.Instance)) {
            return new MemberInfo[0];
        }
        boolean ignoreCase = flags.has(BindingFlags.IgnoreCase);
        if (this.definition == String.class
                && (name.equals("Chars") || ignoreCase && name.equalsIgnoreCase("Chars"))) {
            return new MemberInfo[] {new DefaultPropertyMember("Chars", this)};
        }
        if (this.definition == java.util.List.class
                && (name.equals("Item") || ignoreCase && name.equalsIgnoreCase("Item"))) {
            return new MemberInfo[] {new DefaultPropertyMember("Item", this)};
        }
        String interfaceMethod = this.selectedInterfaceMethodName();
        if (interfaceMethod != null) {
            if (name.equals(interfaceMethod) || ignoreCase && name.equalsIgnoreCase(interfaceMethod)) {
                return new MemberInfo[] {new DefaultMethodMember(interfaceMethod, this)};
            }
            return new MemberInfo[0];
        }
        if (name.equals("Missing") || this.definition == String.class && name.equals("chars")) {
            return new MemberInfo[0];
        }
        throw new UnsupportedOperationException("Flagged member lookup is not mapped for this candidate name");
    }

    public MemberInfo[] GetMember(String name, MemberTypes memberTypes, BindingFlags flags) {
        if (name == null) {
            throw new ArgumentNullException("name");
        }
        if (memberTypes == null) {
            throw new NullPointerException("memberTypes");
        }
        MemberInfo[] matches = this.GetMember(name, flags);
        java.util.ArrayList<MemberInfo> selected = new java.util.ArrayList<>();
        for (MemberInfo member : matches) {
            if (memberTypes.has(member.get_MemberType())) {
                selected.add(member);
            }
        }
        return selected.toArray(new MemberInfo[0]);
    }

    public MemberInfo[] GetMembers() {
        String interfaceMethod = this.selectedInterfaceMethodName();
        if (interfaceMethod != null) {
            return new MemberInfo[] {new DefaultMethodMember(interfaceMethod, this)};
        }
        throw new UnsupportedOperationException("Member enumeration is not mapped for this candidate type");
    }

    public MemberInfo[] GetMembers(BindingFlags flags) {
        if (flags == null) {
            throw new NullPointerException("flags");
        }
        String interfaceMethod = this.selectedInterfaceMethodName();
        if (interfaceMethod != null) {
            if (flags.has(BindingFlags.Public) && flags.has(BindingFlags.Instance)) {
                return new MemberInfo[] {new DefaultMethodMember(interfaceMethod, this)};
            }
            return new MemberInfo[0];
        }
        throw new UnsupportedOperationException("Flagged member enumeration is not mapped for this candidate type");
    }

    public MethodInfo[] GetMethods(BindingFlags flags) {
        if (flags == null) {
            throw new NullPointerException("flags");
        }
        String interfaceMethod = this.selectedInterfaceMethodName();
        if (interfaceMethod != null) {
            if (flags.has(BindingFlags.Public) && flags.has(BindingFlags.Instance)) {
                return new MethodInfo[] {new DefaultMethodMember(interfaceMethod, this)};
            }
            return new MethodInfo[0];
        }
        throw new UnsupportedOperationException("Flagged method enumeration is not mapped for this candidate type");
    }

    public MethodInfo[] GetMethods() {
        return this.GetMethods(BindingFlags.Public.or(BindingFlags.Instance));
    }

    public MethodInfo GetMethod(String name) {
        if (name == null) {
            throw new ArgumentNullException("name");
        }
        String interfaceMethod = this.selectedInterfaceMethodName();
        if (interfaceMethod != null) {
            return name.equals(interfaceMethod) ? new DefaultMethodMember(interfaceMethod, this) : null;
        }
        throw new UnsupportedOperationException("Method lookup is not mapped for this candidate type");
    }

    public MethodInfo GetMethod(String name, BindingFlags flags) {
        if (name == null) {
            throw new ArgumentNullException("name");
        }
        if (flags == null) {
            throw new NullPointerException("flags");
        }
        String interfaceMethod = this.selectedInterfaceMethodName();
        if (interfaceMethod != null) {
            if (flags.has(BindingFlags.Public) && flags.has(BindingFlags.Instance)
                    && (name.equals(interfaceMethod)
                    || flags.has(BindingFlags.IgnoreCase)
                            && name.equalsIgnoreCase(interfaceMethod))) {
                return new DefaultMethodMember(interfaceMethod, this);
            }
            return null;
        }
        throw new UnsupportedOperationException("Flagged method lookup is not mapped for this candidate type");
    }

    public MethodInfo GetMethod(String name, Type[] types) {
        if (name == null) {
            throw new ArgumentNullException("name");
        }
        if (types == null) {
            throw new ArgumentNullException("types");
        }
        for (Type type : types) {
            if (type == null) {
                throw new ArgumentNullException("types");
            }
        }
        String interfaceMethod = this.selectedInterfaceMethodName();
        if (interfaceMethod == null) {
            throw new UnsupportedOperationException("Parameterized method lookup is not mapped for this candidate type");
        }
        if (!name.equals(interfaceMethod)) {
            return null;
        }
        boolean matches = this.definition == IDisposable.class && types.length == 0
                || this.definition == IComparable.class
                    && Arrays.equals(types, new Type[] {fromJavaClass(Object.class)})
                || this.definition == IFormattable.class
                    && Arrays.equals(types, new Type[] {fromJavaClass(String.class),
                        fromJavaClass(IFormatProvider.class)})
                || this.definition == IFormatProvider.class
                    && Arrays.equals(types, new Type[] {fromJavaClass(Type.class)});
        return matches ? new DefaultMethodMember(interfaceMethod, this) : null;
    }

    public MethodInfo GetMethod(String name, BindingFlags flags, Type[] types) {
        if (name == null) {
            throw new ArgumentNullException("name");
        }
        if (types == null) {
            throw new ArgumentNullException("types");
        }
        for (Type type : types) {
            if (type == null) {
                throw new ArgumentNullException("types");
            }
        }
        MethodInfo named = this.GetMethod(name, flags);
        return named == null ? null : this.GetMethod(named.get_Name(), types);
    }

    private String selectedInterfaceMethodName() {
        if (this.definition == IDisposable.class) {
            return "Dispose";
        }
        if (this.definition == IComparable.class) {
            return "CompareTo";
        }
        if (this.definition == IFormattable.class) {
            return "ToString";
        }
        if (this.definition == IFormatProvider.class) {
            return "GetFormat";
        }
        return null;
    }

    public MemberInfo[] GetDefaultMembers() {
        if (this.definition == String.class && !this.get_HasElementType()) {
            return new MemberInfo[] {new DefaultPropertyMember("Chars", this)};
        }
        if (this.definition == java.util.List.class && !this.get_HasElementType()) {
            return new MemberInfo[] {new DefaultPropertyMember("Item", this)};
        }
        if (this.definition == Object.class || this.definition == IDisposable.class
                || this.definition == TypeCode.class) {
            return new MemberInfo[0];
        }
        throw new UnsupportedOperationException("Default members are not mapped for this candidate type");
    }

    public Type[] GetOptionalCustomModifiers() {
        return new Type[0];
    }

    public Type[] GetRequiredCustomModifiers() {
        return new Type[0];
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

    public Type GetNestedType(String name) {
        if (name == null) {
            throw new ArgumentNullException("fullname");
        }
        if (this.get_IsGenericParameter() || this.get_HasElementType()) {
            return null;
        }
        for (Class<?> nested : this.definition.getDeclaredClasses()) {
            if (java.lang.reflect.Modifier.isPublic(nested.getModifiers())
                    && nested.getSimpleName().equals(name)) {
                return fromJavaClass(nested);
            }
        }
        return null;
    }

    public Type GetNestedType(String name, BindingFlags flags) {
        if (name == null) {
            throw new ArgumentNullException("fullname");
        }
        if (flags == null) {
            throw new NullPointerException("flags");
        }
        if (this.get_IsGenericParameter() || this.get_HasElementType()) {
            return null;
        }
        for (Class<?> nested : this.definition.getDeclaredClasses()) {
            boolean isPublic = java.lang.reflect.Modifier.isPublic(nested.getModifiers());
            if ((isPublic && flags.has(BindingFlags.Public)
                    || !isPublic && flags.has(BindingFlags.NonPublic))
                    && (nested.getSimpleName().equals(name)
                    || flags.has(BindingFlags.IgnoreCase)
                            && nested.getSimpleName().equalsIgnoreCase(name))) {
                return fromJavaClass(nested);
            }
        }
        return null;
    }

    public Type[] GetNestedTypes() {
        if (this.get_IsGenericParameter() || this.get_HasElementType()) {
            return new Type[0];
        }
        java.util.ArrayList<Type> result = new java.util.ArrayList<>();
        for (Class<?> nested : this.definition.getDeclaredClasses()) {
            if (java.lang.reflect.Modifier.isPublic(nested.getModifiers())) {
                result.add(fromJavaClass(nested));
            }
        }
        return result.toArray(new Type[0]);
    }

    public Type[] GetNestedTypes(BindingFlags flags) {
        if (flags == null) {
            throw new NullPointerException("flags");
        }
        if (this.get_IsGenericParameter() || this.get_HasElementType()) {
            return new Type[0];
        }
        java.util.ArrayList<Type> result = new java.util.ArrayList<>();
        for (Class<?> nested : this.definition.getDeclaredClasses()) {
            boolean isPublic = java.lang.reflect.Modifier.isPublic(nested.getModifiers());
            if (isPublic && flags.has(BindingFlags.Public)
                    || !isPublic && flags.has(BindingFlags.NonPublic)) {
                result.add(fromJavaClass(nested));
            }
        }
        return result.toArray(new Type[0]);
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

    public boolean get_IsTypeDefinition() {
        return this.parameterIndex < 0 && this.arguments.isEmpty() && !this.get_HasElementType();
    }

    public boolean get_IsByRefLike() {
        return false;
    }

    public boolean get_IsNested() {
        return this.parameterIndex >= 0 || (!this.get_HasElementType()
                && this.definition.getEnclosingClass() != null);
    }

    public boolean get_IsNestedPublic() {
        return this.parameterIndex < 0 && this.get_IsNested()
                && java.lang.reflect.Modifier.isPublic(this.definition.getModifiers());
    }

    public boolean get_IsNestedAssembly() {
        if (this.parameterIndex >= 0 || !this.get_IsNested()) {
            return false;
        }
        int modifiers = this.definition.getModifiers();
        return !java.lang.reflect.Modifier.isPublic(modifiers)
                && !java.lang.reflect.Modifier.isPrivate(modifiers)
                && !java.lang.reflect.Modifier.isProtected(modifiers);
    }

    public boolean get_IsNestedPrivate() {
        return this.parameterIndex < 0 && this.get_IsNested()
                && java.lang.reflect.Modifier.isPrivate(this.definition.getModifiers());
    }

    public boolean get_IsNestedFamily() {
        return this.parameterIndex < 0 && this.get_IsNested()
                && java.lang.reflect.Modifier.isProtected(this.definition.getModifiers());
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

    public boolean get_IsGenericTypeParameter() {
        return this.parameterIndex >= 0;
    }

    public boolean get_IsGenericMethodParameter() {
        return false;
    }

    public GenericParameterAttributes get_GenericParameterAttributes() {
        if (this.parameterIndex < 0) {
            throw new InvalidOperationException("Type is not a generic parameter.");
        }
        return GenericParameterAttributes.None;
    }

    public int get_GenericParameterPosition() {
        if (this.parameterIndex < 0) {
            throw new IllegalStateException("Not a generic parameter");
        }
        return this.parameterIndex;
    }

    public boolean IsEquivalentTo(Type other) {
        return this == other;
    }

    public String ToString() {
        if (this.get_IsGenericParameter()) {
            return this.get_Name();
        }
        if (this instanceof ArrayType array) {
            return array.elementType.ToString() + arraySuffix(array.rank, array.vector);
        }
        if (this.definition.isArray()) {
            return this.GetElementType().ToString() + "[]";
        }
        if (this.get_IsByRef() || this.get_IsPointer()) {
            return this.GetElementType().ToString() + (this.get_IsByRef() ? "&" : "*");
        }
        if (this.get_IsGenericType()) {
            Type[] typeArguments = this.GetGenericArguments();
            StringBuilder result = new StringBuilder(this.get_DeclaringType() == null
                    ? this.get_Namespace() + "." + this.get_Name()
                    : this.get_DeclaringType().get_FullName() + "+" + this.get_Name()).append('[');
            for (int index = 0; index < typeArguments.length; index++) {
                if (index > 0) {
                    result.append(',');
                }
                result.append(typeArguments[index].ToString());
            }
            return result.append(']').toString();
        }
        return this.get_FullName();
    }

    @Override
    public String toString() {
        return this.ToString();
    }

    public boolean Equals(Type other) {
        return this == other;
    }

    private static final class DefaultMethodMember extends MethodInfo {
        private final String name;
        private final Type owner;

        private DefaultMethodMember(String name, Type owner) {
            this.name = name;
            this.owner = owner;
        }

        @Override
        public String get_Name() {
            return this.name;
        }

        @Override
        public MemberTypes get_MemberType() {
            return MemberTypes.Method;
        }

        @Override
        public Type get_ReturnType() {
            return switch (this.name) {
                case "Dispose" -> fromJavaClass(Void.class);
                case "CompareTo" -> fromJavaClass(Int32.class);
                case "ToString" -> fromJavaClass(String.class);
                case "GetFormat" -> fromJavaClass(Object.class);
                default -> throw new UnsupportedOperationException("Method return type is not mapped");
            };
        }

        @Override
        public Type get_DeclaringType() {
            return this.owner;
        }

        @Override
        public Type get_ReflectedType() {
            return this.owner;
        }
    }

    private static final class DefaultPropertyMember extends MemberInfo {
        private final String name;
        private final Type owner;

        private DefaultPropertyMember(String name, Type owner) {
            this.name = name;
            this.owner = owner;
        }

        @Override
        public String get_Name() {
            return this.name;
        }

        @Override
        public MemberTypes get_MemberType() {
            return MemberTypes.Property;
        }

        @Override
        public Type get_DeclaringType() {
            return this.owner;
        }

        @Override
        public Type get_ReflectedType() {
            return this.owner;
        }
    }

    private static final class ResolvedType extends Type {
        private ResolvedType(Class<?> definition, List<Type> arguments) {
            super(definition, arguments);
        }

        @Override
        public String get_Name() {
            return this.nameCore();
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
        public boolean get_IsPointer() {
            return true;
        }

        @Override
        public Type GetElementType() {
            return this.elementType;
        }
    }
}
