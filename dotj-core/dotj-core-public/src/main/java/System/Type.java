// SPDX-License-Identifier: MIT

package System;

import System.Reflection.TypeFilter;
import System.Reflection.MemberFilter;
import System.Reflection.FieldInfo;
import System.Reflection.TargetException;
import System.Reflection.FieldAttributes;

import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.math.BigInteger;
import java.util.concurrent.ConcurrentHashMap;
import System.IO.FileNotFoundException;
import System.IO.FileLoadException;
import System.IO.IOException;
import System.Diagnostics.Stopwatch;
import System.Text.Encoding;
import System.Text.NormalizationForm;
import System.Globalization.DigitShapes;
import System.Text.Encoder;
import System.Text.Decoder;
import System.Text.EncoderFallback;
import System.Text.DecoderFallback;
import System.Text.EncoderReplacementFallback;
import System.Text.DecoderReplacementFallback;
import System.Text.EncoderExceptionFallback;
import System.Text.DecoderExceptionFallback;
import System.Text.EncoderFallbackBuffer;
import System.Text.DecoderFallbackBuffer;
import System.Text.UTF8Encoding;
import System.Text.UnicodeEncoding;
import System.Text.EncoderFallbackException;
import System.Text.DecoderFallbackException;
import System.Reflection.MemberInfo;
import System.Reflection.MethodBase;
import System.Reflection.MethodInfo;
import System.Reflection.ParameterInfo;
import System.Reflection.MemberTypes;
import System.Reflection.BindingFlags;
import System.Reflection.CallingConventions;
import System.Reflection.MethodImplAttributes;
import System.Reflection.MethodBody;
import System.Reflection.GenericParameterAttributes;
import System.Reflection.ParameterAttributes;
import System.Runtime.CompilerServices.NullableAttribute;
import System.Runtime.Serialization.ISerializable;
import System.Runtime.Serialization.IFormatterConverter;
import System.Runtime.Serialization.FormatterConverter;
import System.Runtime.Serialization.SerializationInfo;
import System.Runtime.Serialization.SerializationException;
import System.Runtime.Serialization.SerializationEntry;
import System.Runtime.Serialization.SerializationInfoEnumerator;
import System.Collections.IEnumerator;
import System.Collections.IEnumerable;
import System.Collections.ICollection;
import System.Collections.IDictionary;
import System.Collections.IDictionaryEnumerator;
import System.Collections.DictionaryEntry;
import System.Runtime.Serialization.StreamingContext;
import System.Runtime.Serialization.StreamingContextStates;
import System.Globalization.NumberStyles;
import System.Globalization.TimeSpanStyles;
import System.Globalization.DateTimeStyles;
import System.Globalization.NumberFormatInfo;
import System.Globalization.CultureNotFoundException;

/** Bounded candidate for closed generic identity; not a complete System.Type surface. */
public abstract class Type extends MemberInfo {
    private static final FieldInfo[] EMPTY_FIELDS = new FieldInfo[0];
    private static final ConcurrentHashMap<List<Object>, FieldInfo> literalFields = new ConcurrentHashMap<>();
    private static final Type[] EMPTY_INTERFACE_TYPES = new Type[0];
    private static final Type[] EMPTY_FIELD_MODIFIERS = new Type[0];
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
    private static final MemberInfo[] EMPTY_DEFAULT_MEMBERS = new MemberInfo[0];
    private static final ConcurrentHashMap<List<Object>, MemberInfo> defaultPropertyMembers = new ConcurrentHashMap<>();
    private static final ConcurrentHashMap<List<Object>, MethodInfo> interfaceMethodMembers = new ConcurrentHashMap<>();

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
                ? Int32.class : definition == java.lang.Byte.class || definition == byte.class
                ? Byte.class : definition;
        return canonical.get(backend).computeIfAbsent(List.of(), key -> new ResolvedType(backend, key));
    }

    static MethodBase capturedMethod(StackTraceElement frame) {
        try {
            Class<?> owner = Class.forName(frame.getClassName(), false,
                    Thread.currentThread().getContextClassLoader());
            for (java.lang.reflect.Method method : owner.getDeclaredMethods()) {
                if (method.getName().equals(frame.getMethodName())) {
                    return new DefaultMethodMember(method, fromJavaClass(owner));
                }
            }
            throw new IllegalStateException("Captured method was not found: " + frame.getMethodName());
        } catch (ClassNotFoundException error) {
            throw new IllegalStateException("Captured type was not found: " + frame.getClassName(), error);
        }
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
        if (type.get_IsSignatureType()) throw new NotSupportedException("This method is not supported on signature types.");
        if (type.get_IsEnum()) {
            return GetTypeCode(type.GetEnumUnderlyingType());
        }
        if (type.definition == String.class) return TypeCode.String;
        if (type.definition == Boolean.class || type.definition == boolean.class) return TypeCode.Boolean;
        if (type.definition == Character.class || type.definition == char.class) return TypeCode.Char;
        if (type.definition == Byte.class || type.definition == java.lang.Byte.class
                || type.definition == byte.class) return TypeCode.Byte;
        if (type.definition == SByte.class) return TypeCode.SByte;
        if (type.definition == Short.class || type.definition == short.class) return TypeCode.Int16;
        if (type.definition == Int32.class) return TypeCode.Int32;
        if (type.definition == Long.class || type.definition == long.class) return TypeCode.Int64;
        if (type.definition == BigInteger.class) return TypeCode.UInt64;
        if (type.definition == UInt16.class) return TypeCode.UInt16;
        if (type.definition == UInt32.class) return TypeCode.UInt32;
        if (type.definition == Float.class || type.definition == float.class) return TypeCode.Single;
        if (type.definition == Double.class || type.definition == double.class) return TypeCode.Double;
        if (type.definition == Decimal.class) return TypeCode.Decimal;
        if (type.definition == DateTime.class) return TypeCode.DateTime;
        if (type.definition == DBNull.class) return TypeCode.DBNull;
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

    @Override
    public boolean get_IsCollectible() {
        return false;
    }

    public int GetHashCode() {
        return this.hashCode();
    }

    public static Type MakeGenericMethodParameter(int position) {
        if (position < 0) {
            throw new ArgumentOutOfRangeException("position", position,
                    "position ('" + position + "') must be a non-negative value.");
        }
        return new SignatureMethodParameter(position);
    }

    public static Type MakeGenericSignatureType(Type genericTypeDefinition, Type[] typeArguments) {
        if (genericTypeDefinition == null) throw new ArgumentNullException("genericTypeDefinition");
        if (typeArguments == null) throw new ArgumentNullException("typeArguments");
        if (!genericTypeDefinition.get_IsGenericTypeDefinition()) {
            throw new ArgumentException(genericTypeDefinition.ToString()
                    + " is not a GenericTypeDefinition. MakeGenericType may only be called on a type for which Type.IsGenericTypeDefinition is true.", "genericTypeDefinition");
        }
        return new SignatureConstructedType(genericTypeDefinition, typeArguments);
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
            Type element = GetType(name.substring(0, name.length() - 1), false, ignoreCase);
            return element == null ? null : element.MakeByRefType();
        }
        if (name.endsWith("*")) {
            Type element = GetType(name.substring(0, name.length() - 1), false, ignoreCase);
            return element == null ? null : element.MakePointerType();
        }
        if (name.endsWith("[]")) {
            Type element = GetType(name.substring(0, name.length() - 2), false, ignoreCase);
            return element == null ? null : element.MakeArrayType();
        }
        if (name.endsWith("]")) {
            int opening = name.lastIndexOf('[');
            if (opening >= 0 && opening < name.length() - 2) {
                String dimensions = name.substring(opening + 1, name.length() - 1);
                if (dimensions.chars().allMatch(character -> character == ',')) {
                    Type element = GetType(name.substring(0, opening), false, ignoreCase);
                    return element == null ? null : element.MakeArrayType(dimensions.length() + 1);
                }
            }
        }
        if (name.endsWith("[*]")) {
            Type element = GetType(name.substring(0, name.length() - 3), false, ignoreCase);
            return element == null ? null : element.MakeArrayType(1);
        }
        int nullableOpening = name.indexOf('[');
        if (nullableOpening > 0 && name.endsWith("]") && name.charAt(nullableOpening + 1) != '[') {
            String nullableName = name.substring(0, nullableOpening);
            if (nullableName.equals("System.Nullable`1")
                    || ignoreCase && nullableName.equalsIgnoreCase("System.Nullable`1")) {
                String argumentName = name.substring(nullableOpening + 1, name.length() - 1);
                if (argumentName.indexOf(',') < 0) {
                    Type argument = GetType(argumentName, false, ignoreCase);
                    return argument == null ? null : fromJavaClass(java.util.Optional.class)
                            .MakeGenericType(new Type[] {argument});
                }
            }
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
            case "System.Nullable`1", "system.nullable`1",
                    "System.Collections.Generic.List`1", "system.collections.generic.list`1" -> 1;
            case "System.ValueTuple`2", "system.valuetuple`2",
                    "System.Collections.Generic.Dictionary`2", "system.collections.generic.dictionary`2" -> 2;
            case "System.Collections.Generic.Dictionary`2+Entry",
                    "system.collections.generic.dictionary`2+entry" -> 2;
            default -> 0;
        };
        boolean nullable = selectedDefinition.equalsIgnoreCase("System.Nullable`1");
        if (nullable && !ignoreCase && !definitionName.equals("System.Nullable`1")) return null;
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
            if (canonicalName == null || !nullable && (ignoreCase
                    && (!argumentName.chars().allMatch(character -> character < 128)
                            || !argumentName.equalsIgnoreCase(canonicalName))
                    || !ignoreCase && !argumentName.equals(canonicalName))) {
                return null;
            }
            arguments[index] = argument;
        }
        String canonicalDefinitionName = selectedDefinition.equalsIgnoreCase("System.ValueTuple`2")
                ? "System.ValueTuple`2" : nullable ? "System.Nullable`1" : arity == 1
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
            case "System.UInt64" -> fromJavaClass(BigInteger.class);
            case "System.UInt16" -> fromJavaClass(UInt16.class);
            case "System.UInt32" -> fromJavaClass(UInt32.class);
            case "System.Single" -> fromJavaClass(Float.class);
            case "System.Double" -> fromJavaClass(Double.class);
            case "System.Byte" -> fromJavaClass(Byte.class);
            case "System.SByte" -> fromJavaClass(SByte.class);
            case "System.Int32" -> fromJavaClass(Int32.class);
            case "System.Object" -> fromJavaClass(Object.class);
            case "System.ValueType" -> fromJavaClass(Number.class);
            case "System.Array" -> fromJavaClass(java.lang.reflect.Array.class);
            case "System.IDisposable" -> fromJavaClass(IDisposable.class);
            case "System.IComparable" -> fromJavaClass(IComparable.class);
            case "System.ICloneable" -> fromJavaClass(ICloneable.class);
            case "System.IFormattable" -> fromJavaClass(IFormattable.class);
            case "System.ISpanFormattable" -> fromJavaClass(ISpanFormattable.class);
            case "System.IUtf8SpanFormattable" -> fromJavaClass(IUtf8SpanFormattable.class);
            case "System.IFormatProvider" -> fromJavaClass(IFormatProvider.class);
            case "System.IConvertible" -> fromJavaClass(IConvertible.class);
            case "System.TypeCode" -> fromJavaClass(TypeCode.class);
            case "System.Type" -> fromJavaClass(Type.class);
            case "System.DBNull" -> fromJavaClass(DBNull.class);
            case "System.NullReferenceException" -> fromJavaClass(NullReferenceException.class);
            case "System.Runtime.Serialization.ISerializable" -> fromJavaClass(ISerializable.class);
            case "System.Collections.IEnumerable" -> fromJavaClass(IEnumerable.class);
            case "System.Collections.ICollection" -> fromJavaClass(ICollection.class);
            case "System.Collections.IDictionary" -> fromJavaClass(IDictionary.class);
            case "System.Collections.IDictionaryEnumerator" -> fromJavaClass(IDictionaryEnumerator.class);
            case "System.Collections.DictionaryEntry" -> fromJavaClass(DictionaryEntry.class);
            case "System.Runtime.Serialization.IFormatterConverter" ->
                    fromJavaClass(IFormatterConverter.class);
            case "System.Runtime.Serialization.FormatterConverter" ->
                    fromJavaClass(FormatterConverter.class);
            case "System.Runtime.Serialization.SerializationInfo" -> fromJavaClass(SerializationInfo.class);
            case "System.Runtime.Serialization.SerializationException" ->
                    fromJavaClass(SerializationException.class);
            case "System.Runtime.Serialization.SerializationEntry" ->
                    fromJavaClass(SerializationEntry.class);
            case "System.Runtime.Serialization.SerializationInfoEnumerator" ->
                    fromJavaClass(SerializationInfoEnumerator.class);
            case "System.Collections.IEnumerator" -> fromJavaClass(IEnumerator.class);
            case "System.Runtime.Serialization.StreamingContext" -> fromJavaClass(StreamingContext.class);
            case "System.Runtime.Serialization.StreamingContextStates" ->
                    fromJavaClass(StreamingContextStates.class);
            case "System.Attribute" -> fromJavaClass(Attribute.class);
            case "System.Runtime.CompilerServices.NullableAttribute" ->
                    fromJavaClass(NullableAttribute.class);
            case "System.Reflection.FieldInfo" -> fromJavaClass(FieldInfo.class);
            case "System.Reflection.MemberInfo" -> fromJavaClass(MemberInfo.class);
            case "System.Reflection.MethodBase" -> fromJavaClass(MethodBase.class);
            case "System.Reflection.MethodInfo" -> fromJavaClass(MethodInfo.class);
            case "System.Reflection.MethodBody" -> fromJavaClass(MethodBody.class);
            case "System.Reflection.ParameterInfo" -> fromJavaClass(ParameterInfo.class);
            case "System.Void" -> fromJavaClass(Void.class);
            case "System.Exception" -> fromJavaClass(Exception.class);
            case "System.MemberAccessException" -> fromJavaClass(MemberAccessException.class);
            case "System.FieldAccessException" -> fromJavaClass(FieldAccessException.class);
            case "System.ApplicationException" -> fromJavaClass(ApplicationException.class);
            case "System.Reflection.TargetException" -> fromJavaClass(TargetException.class);
            case "System.SystemException" -> fromJavaClass(SystemException.class);
            case "System.NotImplementedException" -> fromJavaClass(NotImplementedException.class);
            case "System.ArgumentException" -> fromJavaClass(ArgumentException.class);
            case "System.ArgumentNullException" -> fromJavaClass(ArgumentNullException.class);
            case "System.ArgumentOutOfRangeException" -> fromJavaClass(ArgumentOutOfRangeException.class);
            case "System.ArithmeticException" -> fromJavaClass(ArithmeticException.class);
            case "System.DivideByZeroException" -> fromJavaClass(DivideByZeroException.class);
            case "System.ValueTuple`2" -> fromJavaClass(ValueTuple.class);
            case "System.TypeLoadException" -> fromJavaClass(TypeLoadException.class);
            case "System.IndexOutOfRangeException" -> fromJavaClass(IndexOutOfRangeException.class);
            case "System.IO.IOException" -> fromJavaClass(IOException.class);
            case "System.IO.FileNotFoundException" -> fromJavaClass(FileNotFoundException.class);
            case "System.Decimal" -> fromJavaClass(Decimal.class);
            case "System.DateTime" -> fromJavaClass(DateTime.class);
            case "System.TimeSpan" -> fromJavaClass(TimeSpan.class);
            case "System.Diagnostics.Stopwatch" -> fromJavaClass(Stopwatch.class);
            case "System.Text.NormalizationForm" -> fromJavaClass(NormalizationForm.class);
            case "System.Globalization.DigitShapes" -> fromJavaClass(DigitShapes.class);
            case "System.Text.NormalizationForm[]" -> fromJavaClass(NormalizationForm.class).MakeArrayType();
            case "System.Globalization.DigitShapes[]" -> fromJavaClass(DigitShapes.class).MakeArrayType();
            case "System.Text.Encoding" -> fromJavaClass(Encoding.class);
            case "System.Text.Encoder" -> fromJavaClass(Encoder.class);
            case "System.Text.Decoder" -> fromJavaClass(Decoder.class);
            case "System.Text.EncoderFallback" -> fromJavaClass(EncoderFallback.class);
            case "System.Text.DecoderFallback" -> fromJavaClass(DecoderFallback.class);
            case "System.Text.EncoderReplacementFallback" -> fromJavaClass(EncoderReplacementFallback.class);
            case "System.Text.DecoderReplacementFallback" -> fromJavaClass(DecoderReplacementFallback.class);
            case "System.Text.EncoderExceptionFallback" -> fromJavaClass(EncoderExceptionFallback.class);
            case "System.Text.DecoderExceptionFallback" -> fromJavaClass(DecoderExceptionFallback.class);
            case "System.Text.EncoderFallbackBuffer" -> fromJavaClass(EncoderFallbackBuffer.class);
            case "System.Text.DecoderFallbackBuffer" -> fromJavaClass(DecoderFallbackBuffer.class);
            case "System.Text.UTF8Encoding" -> fromJavaClass(UTF8Encoding.class);
            case "System.Text.UnicodeEncoding" -> fromJavaClass(UnicodeEncoding.class);
            case "System.Text.EncoderFallbackException" -> fromJavaClass(EncoderFallbackException.class);
            case "System.Text.DecoderFallbackException" -> fromJavaClass(DecoderFallbackException.class);
            case "System.DateTimeKind" -> fromJavaClass(DateTimeKind.class);
            case "System.MidpointRounding" -> fromJavaClass(MidpointRounding.class);
            case "System.DayOfWeek" -> fromJavaClass(DayOfWeek.class);
            case "System.OverflowException" -> fromJavaClass(OverflowException.class);
            case "System.OutOfMemoryException" -> fromJavaClass(OutOfMemoryException.class);
            case "System.NotSupportedException" -> fromJavaClass(NotSupportedException.class);
            case "System.InvalidCastException" -> fromJavaClass(InvalidCastException.class);
            case "System.InvalidOperationException" -> fromJavaClass(InvalidOperationException.class);
            case "System.IO.FileLoadException" -> fromJavaClass(FileLoadException.class);
            case "System.FormatException" -> fromJavaClass(FormatException.class);
            case "System.Globalization.NumberStyles" -> fromJavaClass(NumberStyles.class);
            case "System.Globalization.DateTimeStyles" -> fromJavaClass(DateTimeStyles.class);
            case "System.Globalization.TimeSpanStyles" -> fromJavaClass(TimeSpanStyles.class);
            case "System.Globalization.TimeSpanStyles[]" -> fromJavaClass(TimeSpanStyles.class).MakeArrayType();
            case "System.Globalization.NumberFormatInfo" -> fromJavaClass(NumberFormatInfo.class);
            case "System.Globalization.CultureNotFoundException" -> fromJavaClass(CultureNotFoundException.class);
            case "System.Reflection.FieldAttributes" -> fromJavaClass(FieldAttributes.class);
            case "System.Reflection.MemberTypes" -> fromJavaClass(MemberTypes.class);
            case "System.Reflection.BindingFlags" -> fromJavaClass(BindingFlags.class);
            case "System.Reflection.CallingConventions" -> fromJavaClass(CallingConventions.class);
            case "System.Reflection.MethodImplAttributes" -> fromJavaClass(MethodImplAttributes.class);
            case "System.Reflection.GenericParameterAttributes" ->
                    fromJavaClass(GenericParameterAttributes.class);
            case "System.Reflection.ParameterAttributes" -> fromJavaClass(ParameterAttributes.class);
            case "System.Enum" -> fromJavaClass(Enum.class);
            case "System.Nullable`1" -> fromJavaClass(java.util.Optional.class);
            case "system.nullable`1" -> ignoreCase ? fromJavaClass(java.util.Optional.class) : null;
            case "system.nullable`1[system.int32]" -> ignoreCase ? fromJavaClass(java.util.Optional.class).MakeGenericType(new Type[] {fromJavaClass(Int32.class)}) : null;
            case "System.Nullable`1[System.Int32]" -> fromJavaClass(java.util.Optional.class).MakeGenericType(new Type[] {fromJavaClass(Int32.class)});
            case "System.Collections.Generic.List`1" -> fromJavaClass(java.util.List.class);
            case "System.Collections.Generic.Dictionary`2" -> fromJavaClass(java.util.Map.class);
            case "System.Collections.Generic.Dictionary`2+Entry" ->
                    fromJavaClass(java.util.Map.Entry.class);
            case "System.Collections.Generic.Dictionary`2+Entry[]" ->
                    fromJavaClass(java.util.Map.Entry.class).MakeArrayType();
            case "System.String[]" -> fromJavaClass(String[].class);
            case "System.DateTime[]" -> fromJavaClass(DateTime.class).MakeArrayType();
            case "System.TimeSpan[]" -> fromJavaClass(TimeSpan.class).MakeArrayType();
            case "System.Diagnostics.Stopwatch[]" -> fromJavaClass(Stopwatch.class).MakeArrayType();
            case "System.DateTimeKind[]" -> fromJavaClass(DateTimeKind.class).MakeArrayType();
            case "System.MidpointRounding[]" -> fromJavaClass(MidpointRounding.class).MakeArrayType();
            case "System.DayOfWeek[]" -> fromJavaClass(DayOfWeek.class).MakeArrayType();
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
            case "system.sbyte" -> ignoreCase ? fromJavaClass(SByte.class) : null;
            case "system.int16" -> ignoreCase ? fromJavaClass(Short.class) : null;
            case "system.int64" -> ignoreCase ? fromJavaClass(Long.class) : null;
            case "system.uint64" -> ignoreCase ? fromJavaClass(BigInteger.class) : null;
            case "system.uint16" -> ignoreCase ? fromJavaClass(UInt16.class) : null;
            case "system.uint32" -> ignoreCase ? fromJavaClass(UInt32.class) : null;
            case "system.single" -> ignoreCase ? fromJavaClass(Float.class) : null;
            case "system.double" -> ignoreCase ? fromJavaClass(Double.class) : null;
            case "system.int32" -> ignoreCase ? fromJavaClass(Int32.class) : null;
            case "system.object" -> ignoreCase ? fromJavaClass(Object.class) : null;
            case "system.valuetype" -> ignoreCase ? fromJavaClass(Number.class) : null;
            case "system.array" -> ignoreCase ? fromJavaClass(java.lang.reflect.Array.class) : null;
            case "system.idisposable" -> ignoreCase ? fromJavaClass(IDisposable.class) : null;
            case "system.icomparable" -> ignoreCase ? fromJavaClass(IComparable.class) : null;
            case "system.icloneable" -> ignoreCase ? fromJavaClass(ICloneable.class) : null;
            case "system.iformattable" -> ignoreCase ? fromJavaClass(IFormattable.class) : null;
            case "system.ispanformattable" -> ignoreCase ? fromJavaClass(ISpanFormattable.class) : null;
            case "system.iutf8spanformattable" -> ignoreCase ? fromJavaClass(IUtf8SpanFormattable.class) : null;
            case "system.iformatprovider" -> ignoreCase ? fromJavaClass(IFormatProvider.class) : null;
            case "system.iconvertible" -> ignoreCase ? fromJavaClass(IConvertible.class) : null;
            case "system.typecode" -> ignoreCase ? fromJavaClass(TypeCode.class) : null;
            case "system.type" -> ignoreCase ? fromJavaClass(Type.class) : null;
            case "system.dbnull" -> ignoreCase ? fromJavaClass(DBNull.class) : null;
            case "system.nullreferenceexception" -> ignoreCase
                    ? fromJavaClass(NullReferenceException.class) : null;
            case "system.runtime.serialization.iserializable" -> ignoreCase
                    ? fromJavaClass(ISerializable.class) : null;
            case "system.collections.ienumerable" -> ignoreCase
                    ? fromJavaClass(IEnumerable.class) : null;
            case "system.collections.icollection" -> ignoreCase
                    ? fromJavaClass(ICollection.class) : null;
            case "system.collections.idictionary" -> ignoreCase
                    ? fromJavaClass(IDictionary.class) : null;
            case "system.collections.idictionaryenumerator" -> ignoreCase
                    ? fromJavaClass(IDictionaryEnumerator.class) : null;
            case "system.collections.dictionaryentry" -> ignoreCase
                    ? fromJavaClass(DictionaryEntry.class) : null;
            case "system.runtime.serialization.iformatterconverter" -> ignoreCase
                    ? fromJavaClass(IFormatterConverter.class) : null;
            case "system.runtime.serialization.formatterconverter" -> ignoreCase
                    ? fromJavaClass(FormatterConverter.class) : null;
            case "system.runtime.serialization.serializationinfo" -> ignoreCase
                    ? fromJavaClass(SerializationInfo.class) : null;
            case "system.runtime.serialization.serializationexception" -> ignoreCase
                    ? fromJavaClass(SerializationException.class) : null;
            case "system.runtime.serialization.serializationentry" -> ignoreCase
                    ? fromJavaClass(SerializationEntry.class) : null;
            case "system.runtime.serialization.serializationinfoenumerator" -> ignoreCase
                    ? fromJavaClass(SerializationInfoEnumerator.class) : null;
            case "system.collections.ienumerator" -> ignoreCase
                    ? fromJavaClass(IEnumerator.class) : null;
            case "system.runtime.serialization.streamingcontext" -> ignoreCase
                    ? fromJavaClass(StreamingContext.class) : null;
            case "system.runtime.serialization.streamingcontextstates" -> ignoreCase
                    ? fromJavaClass(StreamingContextStates.class) : null;
            case "system.attribute" -> ignoreCase ? fromJavaClass(Attribute.class) : null;
            case "system.runtime.compilerservices.nullableattribute" -> ignoreCase
                    ? fromJavaClass(NullableAttribute.class) : null;
            case "system.reflection.fieldinfo" -> ignoreCase ? fromJavaClass(FieldInfo.class) : null;
            case "system.reflection.memberinfo" -> ignoreCase ? fromJavaClass(MemberInfo.class) : null;
            case "system.reflection.methodbase" -> ignoreCase ? fromJavaClass(MethodBase.class) : null;
            case "system.reflection.methodinfo" -> ignoreCase ? fromJavaClass(MethodInfo.class) : null;
            case "system.reflection.methodbody" -> ignoreCase ? fromJavaClass(MethodBody.class) : null;
            case "system.reflection.parameterinfo" -> ignoreCase ? fromJavaClass(ParameterInfo.class) : null;
            case "system.void" -> ignoreCase ? fromJavaClass(Void.class) : null;
            case "system.exception" -> ignoreCase ? fromJavaClass(Exception.class) : null;
            case "system.memberaccessexception" -> ignoreCase ? fromJavaClass(MemberAccessException.class) : null;
            case "system.fieldaccessexception" -> ignoreCase ? fromJavaClass(FieldAccessException.class) : null;
            case "system.applicationexception" -> ignoreCase ? fromJavaClass(ApplicationException.class) : null;
            case "system.reflection.targetexception" -> ignoreCase ? fromJavaClass(TargetException.class) : null;
            case "system.systemexception" -> ignoreCase ? fromJavaClass(SystemException.class) : null;
            case "system.notimplementedexception" -> ignoreCase ? fromJavaClass(NotImplementedException.class) : null;
            case "system.argumentexception" -> ignoreCase ? fromJavaClass(ArgumentException.class) : null;
            case "system.argumentnullexception" -> ignoreCase ? fromJavaClass(ArgumentNullException.class) : null;
            case "system.argumentoutofrangeexception" -> ignoreCase
                    ? fromJavaClass(ArgumentOutOfRangeException.class) : null;
            case "system.arithmeticexception" -> ignoreCase ? fromJavaClass(ArithmeticException.class) : null;
            case "system.dividebyzeroexception" -> ignoreCase
                    ? fromJavaClass(DivideByZeroException.class) : null;
            case "system.valuetuple`2" -> ignoreCase ? fromJavaClass(ValueTuple.class) : null;
            case "system.typeloadexception" -> ignoreCase ? fromJavaClass(TypeLoadException.class) : null;
            case "system.indexoutofrangeexception" -> ignoreCase ? fromJavaClass(IndexOutOfRangeException.class) : null;
            case "system.io.ioexception" -> ignoreCase ? fromJavaClass(IOException.class) : null;
            case "system.io.filenotfoundexception" -> ignoreCase ? fromJavaClass(FileNotFoundException.class) : null;
            case "system.decimal" -> ignoreCase ? fromJavaClass(Decimal.class) : null;
            case "system.datetime" -> ignoreCase ? fromJavaClass(DateTime.class) : null;
            case "system.timespan" -> ignoreCase ? fromJavaClass(TimeSpan.class) : null;
            case "system.diagnostics.stopwatch" -> ignoreCase ? fromJavaClass(Stopwatch.class) : null;
            case "system.text.normalizationform" -> ignoreCase ? fromJavaClass(NormalizationForm.class) : null;
            case "system.globalization.digitshapes" -> ignoreCase ? fromJavaClass(DigitShapes.class) : null;
            case "system.text.normalizationform[]" -> ignoreCase ? fromJavaClass(NormalizationForm.class).MakeArrayType() : null;
            case "system.globalization.digitshapes[]" -> ignoreCase ? fromJavaClass(DigitShapes.class).MakeArrayType() : null;
            case "system.text.encoding" -> ignoreCase ? fromJavaClass(Encoding.class) : null;
            case "system.text.encoder" -> ignoreCase ? fromJavaClass(Encoder.class) : null;
            case "system.text.decoder" -> ignoreCase ? fromJavaClass(Decoder.class) : null;
            case "system.text.encoderfallback" -> ignoreCase ? fromJavaClass(EncoderFallback.class) : null;
            case "system.text.decoderfallback" -> ignoreCase ? fromJavaClass(DecoderFallback.class) : null;
            case "system.text.encoderreplacementfallback" -> ignoreCase ? fromJavaClass(EncoderReplacementFallback.class) : null;
            case "system.text.decoderreplacementfallback" -> ignoreCase ? fromJavaClass(DecoderReplacementFallback.class) : null;
            case "system.text.encoderexceptionfallback" -> ignoreCase ? fromJavaClass(EncoderExceptionFallback.class) : null;
            case "system.text.decoderexceptionfallback" -> ignoreCase ? fromJavaClass(DecoderExceptionFallback.class) : null;
            case "system.text.encoderfallbackbuffer" -> ignoreCase ? fromJavaClass(EncoderFallbackBuffer.class) : null;
            case "system.text.decoderfallbackbuffer" -> ignoreCase ? fromJavaClass(DecoderFallbackBuffer.class) : null;
            case "system.text.utf8encoding" -> ignoreCase ? fromJavaClass(UTF8Encoding.class) : null;
            case "system.text.unicodeencoding" -> ignoreCase ? fromJavaClass(UnicodeEncoding.class) : null;
            case "system.text.encoderfallbackexception" -> ignoreCase ? fromJavaClass(EncoderFallbackException.class) : null;
            case "system.text.decoderfallbackexception" -> ignoreCase ? fromJavaClass(DecoderFallbackException.class) : null;
            case "system.datetimekind" -> ignoreCase ? fromJavaClass(DateTimeKind.class) : null;
            case "system.midpointrounding" -> ignoreCase ? fromJavaClass(MidpointRounding.class) : null;
            case "system.dayofweek" -> ignoreCase ? fromJavaClass(DayOfWeek.class) : null;
            case "system.overflowexception" -> ignoreCase ? fromJavaClass(OverflowException.class) : null;
            case "system.outofmemoryexception" -> ignoreCase ? fromJavaClass(OutOfMemoryException.class) : null;
            case "system.notsupportedexception" -> ignoreCase ? fromJavaClass(NotSupportedException.class) : null;
            case "system.invalidcastexception" -> ignoreCase ? fromJavaClass(InvalidCastException.class) : null;
            case "system.invalidoperationexception" -> ignoreCase
                    ? fromJavaClass(InvalidOperationException.class) : null;
            case "system.io.fileloadexception" -> ignoreCase ? fromJavaClass(FileLoadException.class) : null;
            case "system.formatexception" -> ignoreCase ? fromJavaClass(FormatException.class) : null;
            case "system.globalization.numberstyles" -> ignoreCase ? fromJavaClass(NumberStyles.class) : null;
            case "system.globalization.datetimestyles" -> ignoreCase ? fromJavaClass(DateTimeStyles.class) : null;
            case "system.globalization.timespanstyles" -> ignoreCase ? fromJavaClass(TimeSpanStyles.class) : null;
            case "system.globalization.timespanstyles[]" -> ignoreCase ? fromJavaClass(TimeSpanStyles.class).MakeArrayType() : null;
            case "system.globalization.numberformatinfo" ->
                    ignoreCase ? fromJavaClass(NumberFormatInfo.class) : null;
            case "system.globalization.culturenotfoundexception" -> ignoreCase
                    ? fromJavaClass(CultureNotFoundException.class) : null;
            case "system.reflection.fieldattributes" -> ignoreCase ? fromJavaClass(FieldAttributes.class) : null;
            case "system.reflection.membertypes" -> ignoreCase ? fromJavaClass(MemberTypes.class) : null;
            case "system.reflection.bindingflags" -> ignoreCase ? fromJavaClass(BindingFlags.class) : null;
            case "system.reflection.callingconventions" -> ignoreCase
                    ? fromJavaClass(CallingConventions.class) : null;
            case "system.reflection.methodimplattributes" -> ignoreCase
                    ? fromJavaClass(MethodImplAttributes.class) : null;
            case "system.reflection.genericparameterattributes" -> ignoreCase
                    ? fromJavaClass(GenericParameterAttributes.class) : null;
            case "system.reflection.parameterattributes" -> ignoreCase
                    ? fromJavaClass(ParameterAttributes.class) : null;
            case "system.enum" -> ignoreCase ? fromJavaClass(Enum.class) : null;
            case "system.collections.generic.list`1" -> ignoreCase ? fromJavaClass(java.util.List.class) : null;
            case "system.collections.generic.dictionary`2" -> ignoreCase ? fromJavaClass(java.util.Map.class) : null;
            case "system.collections.generic.dictionary`2+entry" -> ignoreCase
                    ? fromJavaClass(java.util.Map.Entry.class) : null;
            case "system.collections.generic.dictionary`2+entry[]" -> ignoreCase
                    ? fromJavaClass(java.util.Map.Entry.class).MakeArrayType() : null;
            case "system.string[]" -> ignoreCase ? fromJavaClass(String[].class) : null;
            case "system.datetime[]" -> ignoreCase ? fromJavaClass(DateTime.class).MakeArrayType() : null;
            case "system.timespan[]" -> ignoreCase ? fromJavaClass(TimeSpan.class).MakeArrayType() : null;
            case "system.diagnostics.stopwatch[]" -> ignoreCase ? fromJavaClass(Stopwatch.class).MakeArrayType() : null;
            case "system.datetimekind[]" -> ignoreCase ? fromJavaClass(DateTimeKind.class).MakeArrayType() : null;
            case "system.midpointrounding[]" -> ignoreCase ? fromJavaClass(MidpointRounding.class).MakeArrayType() : null;
            case "system.dayofweek[]" -> ignoreCase ? fromJavaClass(DayOfWeek.class).MakeArrayType() : null;
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
            throw new TypeLoadException("Could not resolve selected type: " + typeName, null, selectedMissingTypeName(name, ignoreCase));
        }
        return resolved;
    }

    private static String selectedMissingTypeName(String name, boolean ignoreCase) {
        String missing = selectedUnresolvedTypeName(name, ignoreCase, 0);
        return missing == null ? selectedTypeNameCore(name) : missing;
    }

    private static String selectedTypeNameCore(String name) {
        name = name.stripLeading();
        int bracketDepth = 0;
        for (int index = 0; index < name.length(); index++) {
            char character = name.charAt(index);
            if (character == '[') bracketDepth++;
            else if (character == ']') bracketDepth--;
            else if (character == ',' && bracketDepth == 0) {
                name = name.substring(0, index);
                break;
            }
        }
        boolean changed;
        do {
            changed = false;
            if (name.endsWith("*") || name.endsWith("&")) {
                name = name.substring(0, name.length() - 1);
                changed = true;
            } else if (name.endsWith("]")) {
                int open = name.lastIndexOf('[');
                if (open >= 0 && name.substring(open + 1, name.length() - 1).chars()
                        .allMatch(character -> character == ',' || character == '*')) {
                    name = name.substring(0, open);
                    changed = true;
                }
            }
        } while (changed);
        return name;
    }

    private static String selectedUnresolvedTypeName(String name, boolean ignoreCase, int depth) {
        name = selectedTypeNameCore(name);
        if (depth > 32) return name;
        int genericStart = name.indexOf('[');
        if (genericStart < 0 || !name.endsWith("]")) {
            return GetType(name, false, ignoreCase) == null ? name : null;
        }
        String definition = name.substring(0, genericStart);
        if (GetType(definition, false, ignoreCase) == null) return definition;
        java.util.ArrayList<String> arguments = selectedGenericArgumentNames(
                name.substring(genericStart + 1, name.length() - 1));
        if (arguments == null) return name;
        for (String argument : arguments) {
            String missing = selectedUnresolvedTypeName(argument, ignoreCase, depth + 1);
            if (missing != null) return missing;
        }
        return null;
    }

    private static java.util.ArrayList<String> selectedGenericArgumentNames(String body) {
        java.util.ArrayList<String> arguments = new java.util.ArrayList<>();
        if (body.startsWith("[")) {
            int cursor = 0;
            while (cursor < body.length()) {
                if (body.charAt(cursor) != '[') return null;
                int start = ++cursor;
                int depth = 1;
                while (cursor < body.length() && depth != 0) {
                    char character = body.charAt(cursor++);
                    if (character == '[') depth++;
                    else if (character == ']') depth--;
                }
                if (depth != 0) return null;
                arguments.add(body.substring(start, cursor - 1));
                if (cursor == body.length()) break;
                if (body.charAt(cursor++) != ',') return null;
                while (cursor < body.length() && body.charAt(cursor) == ' ') cursor++;
            }
        } else {
            int depth = 0;
            int start = 0;
            for (int index = 0; index < body.length(); index++) {
                char character = body.charAt(index);
                if (character == '[') depth++;
                else if (character == ']') depth--;
                else if (character == ',' && depth == 0) {
                    arguments.add(body.substring(start, index));
                    start = index + 1;
                }
            }
            arguments.add(body.substring(start));
        }
        return arguments;
    }

    private Type makeNullableType(Type[] typeArguments) {
        if (typeArguments == null) throw new ArgumentNullException("typeArguments");
        if (typeArguments.length != 1) {
            throw new ArgumentException("The number of generic arguments provided doesn't equal the arity of the generic type definition.", "typeArguments");
        }
        Type argument = typeArguments[0];
        if (argument == null) throw new ArgumentNullException();
        String display = argument.get_IsGenericParameter() ? argument.get_Name() : argument.get_FullName();
        if (argument.definition == java.util.Optional.class && argument.parameterIndex < 0) {
            String inner = argument.arguments.isEmpty() ? "T" : argument.arguments.get(0).get_FullName();
            display = "System.Nullable`1[" + inner + "]";
        }
        if (argument.definition == Void.class || argument.get_IsPointer() || argument.get_IsByRef()) {
            throw new ArgumentException("The type '" + display + "' may not be used as a type argument.");
        }
        if (!argument.get_IsValueType()
                || argument.definition == java.util.Optional.class && argument.parameterIndex < 0) {
            throw new ArgumentException("GenericArguments[0], '" + display
                    + "', on 'System.Nullable`1[T]' violates the constraint of type 'T'.");
        }
        if (argument == genericParameters.get(java.util.Optional.class)[0]) return fromJavaClass(java.util.Optional.class);
        List<Type> key = List.of(argument);
        return canonical.get(java.util.Optional.class).computeIfAbsent(key,
                arguments -> new ResolvedType(java.util.Optional.class, arguments));
    }

    public Type MakeGenericType(Type[] typeArguments) {
        if (typeArguments == null) {
            throw new ArgumentNullException("typeArguments");
        }
        if (this.parameterIndex >= 0 || !this.arguments.isEmpty()
                || this.definition.getTypeParameters().length == 0) {
            throw new InvalidOperationException(this.ToString()
                    + " is not a GenericTypeDefinition. MakeGenericType may only be called on a type for which Type.IsGenericTypeDefinition is true.");
        }
        if (typeArguments.length != this.definition.getTypeParameters().length) {
            throw new ArgumentException("The number of generic arguments provided doesn't equal the arity of the generic type definition.", "typeArguments");
        }
        for (int index = 0; index < typeArguments.length; index++) {
            if (typeArguments[index] == null) {
                throw new ArgumentNullException();
            }
        }
        boolean signature = false;
        for (Type argument : typeArguments) signature |= argument.get_IsSignatureType();
        if (signature) return new SignatureConstructedType(this, typeArguments);
        if (this.definition == java.util.Optional.class) return this.makeNullableType(typeArguments);
        for (Type argument : typeArguments) {
            if (argument.definition == Void.class || argument.get_IsPointer() || argument.get_IsByRef()) {
                throw new ArgumentException("The type '" + argument.ToString() + "' may not be used as a type argument.");
            }
        }
        if (Arrays.equals(typeArguments, genericParameters.get(this.definition))) return fromJavaClass(this.definition);
        List<Type> key = List.copyOf(Arrays.asList(typeArguments.clone()));
        return canonical.get(this.definition).computeIfAbsent(key, arguments -> new ResolvedType(this.definition, arguments));
    }

    public Type MakeArrayType() {
        if (this.get_IsByRef() || this.definition == Void.class) {
            throw new TypeLoadException("Array element type cannot be Void or by-reference");
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
        if (rank < 1) { throw new IndexOutOfRangeException("Array rank is out of range"); }
        if (rank > 32 || this.get_IsByRef() || this.definition == Void.class) {
            throw new TypeLoadException("Array rank or element type is not supported");
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
        if (this.definition == java.util.Optional.class) return new Type[] {fromJavaClass(Number.class)};
        return new Type[0];
    }

    public Type[] get_GenericTypeArguments() {
        return this.arguments.isEmpty() ? EMPTY_FIELD_MODIFIERS : this.arguments.toArray(Type[]::new);
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
        if (this.definition == java.util.Optional.class) return "Nullable`1";
        if (this.definition == String.class) return "String";
        if (this.definition == Boolean.class) return "Boolean";
        if (this.definition == Character.class) return "Char";
        if (this.definition == Short.class) return "Int16";
        if (this.definition == Long.class) return "Int64";
        if (this.definition == BigInteger.class) return "UInt64";
        if (this.definition == UInt16.class) return "UInt16";
        if (this.definition == UInt32.class) return "UInt32";
        if (this.definition == Float.class) return "Single";
        if (this.definition == Double.class) return "Double";
        if (this.definition == Byte.class || this.definition == java.lang.Byte.class) return "Byte";
        if (this.definition == SByte.class) return "SByte";
        if (this.definition == Void.class) return "Void";
        if (this.definition == Int32.class) return "Int32";
        if (this.definition == Object.class) return "Object";
        if (this.definition == Number.class) return "ValueType";
        if (this.definition == java.lang.reflect.Array.class) return "Array";
        if (this.definition == Enum.class) return "Enum";
        if (this.definition == java.util.List.class) return "List`1";
        if (this.definition == java.util.Map.class) return "Dictionary`2";
        if (this.definition == ValueTuple.class) return "ValueTuple`2";
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
                || this.definition == Long.class || this.definition == BigInteger.class
                || this.definition == Float.class
                || this.definition == Double.class
                || this.definition == Byte.class || this.definition == SByte.class
                || this.definition == Void.class
                || this.definition == Int32.class
                || this.definition == java.util.Optional.class
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
        if (this.definition == java.util.Optional.class) return fromJavaClass(Number.class);
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
                || this.definition == Long.class || this.definition == BigInteger.class
                || this.definition == UInt16.class || this.definition == UInt32.class
                || this.definition == Float.class
                || this.definition == Double.class || this.definition == Byte.class
                || this.definition == SByte.class) {
            return fromJavaClass(Number.class);
        }
        if (this.definition == Decimal.class || this.definition == DateTime.class || this.definition == TimeSpan.class
                || this.definition == StreamingContext.class
                || this.definition == SerializationEntry.class
                || this.definition == DictionaryEntry.class
                || this.definition == ValueTuple.class) {
            return fromJavaClass(Number.class);
        }
        if ((this.definition == MemberTypes.class || this.definition == FieldAttributes.class) || this.definition == BindingFlags.class
                || this.definition == CallingConventions.class
                || this.definition == MethodImplAttributes.class
                || this.definition == StreamingContextStates.class
                || this.definition == GenericParameterAttributes.class
                || this.definition == ParameterAttributes.class
                || this.definition == DigitShapes.class || this.definition == NormalizationForm.class || this.definition == TypeCode.class
                || this.definition == NumberStyles.class || this.definition == TimeSpanStyles.class || this.definition == DateTimeStyles.class
                || this.definition == MidpointRounding.class || this.definition == DateTimeKind.class || this.definition == DayOfWeek.class) {
            return fromJavaClass(Enum.class);
        }
        if (this.definition == Enum.class) {
            return fromJavaClass(Number.class);
        }
        if (this.parameterIndex >= 0 || this.definition == String.class
                || this.definition == java.util.List.class || this.definition == java.util.Map.class
                || this.definition == Number.class || this.definition == Exception.class
                || this.definition == java.lang.reflect.Array.class) {
            return fromJavaClass(Object.class);
        }
        Class<?> parent = this.definition.getSuperclass();
        return parent == null ? null : fromJavaClass(parent);
    }

    public Type get_UnderlyingSystemType() {
        return this;
    }

    public boolean get_IsValueType() {
        if (this.parameterIndex >= 0 && this.definition == java.util.Optional.class) return true;
        return this.parameterIndex < 0
                && (this.definition == java.util.Optional.class || this.definition == Int32.class || this.definition == Void.class
                        || this.definition == Boolean.class
                        || this.definition == Character.class
                        || this.definition == Short.class
                        || this.definition == Long.class
                        || this.definition == BigInteger.class
                        || this.definition == UInt16.class || this.definition == UInt32.class
                        || this.definition == Float.class
                        || this.definition == Double.class
                        || this.definition == Byte.class || this.definition == SByte.class
                        || this.definition == Decimal.class
                        || this.definition == DateTime.class
                        || this.definition == TimeSpan.class
                        || this.definition == StreamingContext.class
                        || this.definition == SerializationEntry.class
                        || this.definition == DictionaryEntry.class
                        || this.definition == ValueTuple.class
                        || (this.definition == MemberTypes.class || this.definition == FieldAttributes.class)
                        || this.definition == BindingFlags.class
                        || this.definition == CallingConventions.class
                        || this.definition == MethodImplAttributes.class
                        || this.definition == StreamingContextStates.class
                        || this.definition == GenericParameterAttributes.class
                        || this.definition == ParameterAttributes.class
                        || this.definition == DigitShapes.class || this.definition == NormalizationForm.class || this.definition == TypeCode.class || this.definition == NumberStyles.class || this.definition == TimeSpanStyles.class || this.definition == DateTimeStyles.class
                        || this.definition == MidpointRounding.class || this.definition == DateTimeKind.class || this.definition == DayOfWeek.class);
    }

    public boolean get_IsPrimitive() {
        return this.definition == Int32.class
                || this.definition == Boolean.class
                || this.definition == Character.class || this.definition == Short.class
                || this.definition == Long.class || this.definition == BigInteger.class
                || this.definition == UInt16.class || this.definition == UInt32.class
                || this.definition == Float.class
                || this.definition == Double.class || this.definition == Byte.class
                || this.definition == SByte.class;
    }

    public boolean get_IsAbstract() {
        return this.definition == Encoder.class || this.definition == Decoder.class
                || this.definition == EncoderFallback.class || this.definition == DecoderFallback.class || this.definition == EncoderFallbackBuffer.class || this.definition == DecoderFallbackBuffer.class
                || this.definition == Encoding.class || this.definition == Type.class || this.definition == Number.class
                || this.definition == Enum.class || this.definition == java.lang.reflect.Array.class
                || this.definition == FieldInfo.class || this.definition == MemberInfo.class || this.definition == MethodBase.class
                || this.definition == MethodInfo.class
                || this.definition == Attribute.class
                || this.get_IsInterface();
    }

    public boolean get_IsSealed() {
        if (this.parameterIndex >= 0 && this.definition == java.util.Optional.class) return false;
        return this.get_IsArray() || this.get_IsValueType() || this.definition == String.class
                || this.definition == DBNull.class || this.definition == NumberFormatInfo.class
                || this.definition == SerializationInfo.class
                || this.definition == SerializationInfoEnumerator.class
                || this.definition == EncoderReplacementFallback.class || this.definition == DecoderReplacementFallback.class || this.definition == EncoderExceptionFallback.class || this.definition == DecoderExceptionFallback.class
                || this.definition == EncoderFallbackException.class || this.definition == DecoderFallbackException.class
                || this.definition == NullableAttribute.class || this.definition == IndexOutOfRangeException.class;
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
        return this.definition == java.util.Optional.class || this.definition == Object.class || this.definition == java.lang.reflect.Array.class
                || this.definition == Number.class
                || this.definition == Enum.class || this.definition == String.class
                || this.definition == DBNull.class || this.get_IsPrimitive() || this.get_IsEnum()
                || this.definition == Decimal.class || this.definition == DateTime.class
                || this.definition == TimeSpan.class || this.definition == DictionaryEntry.class
                || this.definition == ValueTuple.class
                || this.definition == java.util.List.class || this.definition == java.util.Map.class
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
        return this.definition == ICloneable.class || this.definition == IDisposable.class || this.definition == IComparable.class
                || this.definition == IFormattable.class || this.definition == IFormatProvider.class
                || this.definition == IConvertible.class || this.definition == ISerializable.class
                || this.definition == IFormatterConverter.class
                || this.definition == ISpanFormattable.class
                || this.definition == IUtf8SpanFormattable.class
                || this.definition == IEnumerator.class
                || this.definition == IEnumerable.class || this.definition == ICollection.class
                || this.definition == IDictionary.class
                || this.definition == IDictionaryEnumerator.class;
    }

    public boolean get_IsEnum() {
        return (this.definition == MemberTypes.class || this.definition == FieldAttributes.class) || this.definition == BindingFlags.class
                || this.definition == CallingConventions.class
                || this.definition == MethodImplAttributes.class
                || this.definition == StreamingContextStates.class
                || this.definition == GenericParameterAttributes.class
                || this.definition == ParameterAttributes.class
                || this.definition == DigitShapes.class || this.definition == NormalizationForm.class || this.definition == TypeCode.class
                || this.definition == NumberStyles.class || this.definition == TimeSpanStyles.class || this.definition == DateTimeStyles.class
                || this.definition == MidpointRounding.class || this.definition == DateTimeKind.class || this.definition == DayOfWeek.class;
    }

    public Type GetEnumUnderlyingType() {
        if (!this.get_IsEnum()) {
            throw new ArgumentException("Type provided must be an Enum.", "enumType");
        }
        return fromJavaClass(Int32.class);
    }

    public String[] GetEnumNames() {
        if (!this.get_IsEnum()) {
            throw new ArgumentException("Type provided must be an Enum.", "enumType");
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
            throw new ArgumentException("Type provided must be an Enum.", "enumType");
        }
        return this.enumConstants();
    }

    public int[] GetEnumValuesAsUnderlyingType() {
        if (!this.get_IsEnum()) {
            throw new ArgumentException("Type provided must be an Enum.", "enumType");
        }
        Object[] constants = this.enumConstants();
        int[] values = new int[constants.length];
        for (int index = 0; index < constants.length; index++) {
            values[index] = enumNumericValue(constants[index]);
        }
        return values;
    }

    private static BigInteger enumLookupNumber(Object value) {
        if (value instanceof Int32 number) return BigInteger.valueOf(number.get_Value());
        if (value instanceof SByte number) return BigInteger.valueOf(number.get_Value());
        if (value instanceof Byte number) return BigInteger.valueOf(number.get_Value());
        if (value instanceof UInt16 number) return BigInteger.valueOf(number.get_Value());
        if (value instanceof UInt32 number) return BigInteger.valueOf(number.get_Value());
        if (value instanceof Character character) return BigInteger.valueOf(character);
        if (value instanceof Integer || value instanceof Long || value instanceof Short || value instanceof java.lang.Byte) {
            return BigInteger.valueOf(((Number)value).longValue());
        }
        if (value instanceof BigInteger number) return number;
        return null;
    }

    public boolean IsEnumDefined(Object value) {
        if (value == null) throw new ArgumentNullException("value");
        if (!this.get_IsEnum()) throw new ArgumentException("Type provided must be an Enum.", "enumType");
        Object[] constants = this.enumConstants();
        if (value instanceof String name) {
            for (Object constant : constants) if (enumConstantName(constant).equals(name)) return true;
            return false;
        }
        Type valueType = fromJavaClass(value.getClass());
        if (valueType.get_IsEnum()) {
            if (value.getClass() != this.definition) {
                throw new ArgumentException("Object must be the same type as the enum. The type passed in was '" + valueType.get_FullName() + "'; the enum type was '" + this.get_FullName() + "'.");
            }
            int number = enumNumericValue(value);
            for (Object constant : constants) if (enumNumericValue(constant) == number) return true;
            return false;
        }
        BigInteger number = enumLookupNumber(value);
        if (number != null) {
            if (!(value instanceof Integer || value instanceof Int32)) {
                String name = value instanceof java.lang.Byte ? "System.SByte" : valueType.get_FullName();
                throw new ArgumentException("Enum underlying type and the object must be same type or object must be a String. Type passed in was '" + name + "'; the enum underlying type was 'System.Int32'.");
            }
            for (Object constant : constants) if (number.equals(BigInteger.valueOf(enumNumericValue(constant)))) return true;
            return false;
        }
        throw new InvalidOperationException("Unknown enum type.");
    }

    public String GetEnumName(Object value) {
        if (value == null) throw new ArgumentNullException("value");
        Type valueType = fromJavaClass(value.getClass());
        BigInteger number = valueType.get_IsEnum() ? BigInteger.valueOf(enumNumericValue(value)) : enumLookupNumber(value);
        if (number == null) {
            throw new ArgumentException("The value passed in must be an enum base or an underlying type for an enum, such as an Int32.", "value");
        }
        if (!this.get_IsEnum()) throw new ArgumentException("Type provided must be an Enum.", "enumType");
        for (Object constant : this.enumConstants()) {
            if (number.equals(BigInteger.valueOf(enumNumericValue(constant)))) return enumConstantName(constant);
        }
        return null;
    }

    private Object[] enumConstants() {
        if (this.definition == NormalizationForm.class) return NormalizationForm.values();
        if (this.definition == DigitShapes.class) return DigitShapes.values();
        if (this.definition == GenericParameterAttributes.class) return GenericParameterAttributes.values();
        if (this.definition == DateTimeStyles.class) return DateTimeStyles.values();
        if (this.definition == TimeSpanStyles.class) {
            return TimeSpanStyles.values();
        }
        if (this.definition == NumberStyles.class) {
            return NumberStyles.values();
        }
        if (this.definition == BindingFlags.class) {
            return BindingFlags.values();
        }
        if (this.definition == FieldAttributes.class) {
            return FieldAttributes.values();
        }
        if (this.definition == MemberTypes.class) {
            return MemberTypes.values();
        }
        if (this.definition == CallingConventions.class) {
            return CallingConventions.values();
        }
        if (this.definition == MethodImplAttributes.class) {
            return MethodImplAttributes.values();
        }
        if (this.definition == StreamingContextStates.class) {
            return StreamingContextStates.values();
        }
        return this.definition.getEnumConstants();
    }

    private static String enumConstantName(Object constant) {
        if (constant instanceof FieldAttributes attributes) return attributes.get_Name();
        if (constant instanceof NormalizationForm form) return form.get_Name();
        if (constant instanceof DigitShapes form) return form.get_Name();
        if (constant instanceof GenericParameterAttributes attributes) return attributes.get_Name();
        if (constant instanceof DateTimeStyles styles) return styles.get_Name();
        if (constant instanceof TimeSpanStyles styles) {
            return styles.get_Name();
        }
        if (constant instanceof NumberStyles style) {
            return style.get_Name();
        }
        if (constant instanceof BindingFlags flags) {
            return flags.get_Name();
        }
        if (constant instanceof MemberTypes member) {
            return member.get_Name();
        }
        if (constant instanceof CallingConventions convention) {
            return convention.get_Name();
        }
        if (constant instanceof MethodImplAttributes attributes) {
            return attributes.get_Name();
        }
        if (constant instanceof StreamingContextStates state) {
            return state.get_Name();
        }
        return ((java.lang.Enum<?>) constant).name();
    }

    private static int enumNumericValue(Object constant) {
        if (constant instanceof FieldAttributes attributes) return attributes.get_Value();
        if (constant instanceof NormalizationForm form) return form.get_Value();
        if (constant instanceof MidpointRounding rounding) return rounding.get_Value();
        if (constant instanceof DigitShapes form) return form.get_Value();
        if (constant instanceof DateTimeStyles styles) return styles.get_Value();
        if (constant instanceof TimeSpanStyles styles) {
            return styles.get_Value();
        }
        if (constant instanceof DateTimeKind || constant instanceof DayOfWeek) {
            return ((java.lang.Enum<?>) constant).ordinal();
        }
        if (constant instanceof TypeCode code) {
            return code.get_Value();
        }
        if (constant instanceof MemberTypes member) {
            return member.get_Value();
        }
        if (constant instanceof BindingFlags flags) {
            return flags.get_Value();
        }
        if (constant instanceof CallingConventions convention) {
            return convention.get_Value();
        }
        if (constant instanceof MethodImplAttributes attributes) {
            return attributes.get_Value();
        }
        if (constant instanceof StreamingContextStates state) {
            return state.get_Value();
        }
        if (constant instanceof GenericParameterAttributes attributes) {
            return attributes.get_Value();
        }
        if (constant instanceof ParameterAttributes attributes) {
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
        if (candidate instanceof ModifiedFieldType modified) return this.IsAssignableFrom(modified.underlying);
        if (candidate != null && candidate.selectedPrimitiveBackingFields()
                && (this.definition == IComparable.class || this.definition == IConvertible.class
                    || candidate.definition != Boolean.class && (this.definition == IFormattable.class
                        || this.definition == ISpanFormattable.class || this.definition == IUtf8SpanFormattable.class))) return true;
        if (candidate != null && candidate.get_IsSignatureType()) return false;
        if (this.definition == java.util.Optional.class && this.arguments.size() == 1
                && candidate == this.arguments.get(0)) return true;
        if (candidate == null) {
            return false;
        }
        if (this.get_IsArray() && candidate.get_IsArray()) {
            if (this.GetArrayRank() != candidate.GetArrayRank()
                    || this.get_IsSZArray() && !candidate.get_IsSZArray()) { return false; }
            Type targetElement = this.GetElementType();
            Type sourceElement = candidate.GetElementType();
            if (targetElement.get_IsValueType() || sourceElement.get_IsValueType()) {
                return targetElement == sourceElement;
            }
            return targetElement.IsAssignableFrom(sourceElement);
        }
        if ((candidate.definition == DateTime.class || candidate.definition == TimeSpan.class)
                && (this.definition == IComparable.class || this.definition == IFormattable.class
                    || this.definition == ISpanFormattable.class || this.definition == IUtf8SpanFormattable.class)) {
            return true;
        }
        if (this == candidate) {
            return true;
        }
        if (this.definition == IFormatProvider.class && candidate.definition == NumberFormatInfo.class) {
            return true;
        }
        if (this.definition == ICloneable.class && ICloneable.class.isAssignableFrom(candidate.definition)) {
            return true;
        }
        if ((this.definition == IEnumerable.class || this.definition == ICollection.class)
                && (candidate.get_IsArray() || candidate.definition == java.lang.reflect.Array.class)) {
            return true;
        }
        if ((this.definition == IEnumerable.class || this.definition == ICollection.class
                || this.definition == IDictionary.class || this.definition == IDictionaryEnumerator.class
                || this.definition == IEnumerator.class)
                && this.definition.isAssignableFrom(candidate.definition)) {
            return true;
        }
        if (this.definition == IEnumerator.class
                && candidate.definition == SerializationInfoEnumerator.class) {
            return true;
        }
        if (candidate.definition == NormalizationForm.class && (this.definition == IFormattable.class || this.definition == IConvertible.class || this.definition == IComparable.class || this.definition == ISpanFormattable.class)) return true;
        if (candidate.definition == DigitShapes.class && (this.definition == IFormattable.class || this.definition == IConvertible.class || this.definition == IComparable.class || this.definition == ISpanFormattable.class)) return true;
        if (candidate.definition == MidpointRounding.class && (this.definition == IFormattable.class || this.definition == IConvertible.class || this.definition == IComparable.class || this.definition == ISpanFormattable.class)) return true;
        if ((this.definition == IComparable.class || this.definition == ICloneable.class) && candidate.definition == String.class) {
            return true;
        }
        if (this.definition == IComparable.class && (candidate.definition == Int32.class || candidate.definition == DateTimeStyles.class || candidate.definition == TimeSpanStyles.class || candidate.definition == NumberStyles.class || candidate.definition == BindingFlags.class || (candidate.definition == MemberTypes.class || candidate.definition == FieldAttributes.class) || candidate.definition == CallingConventions.class || candidate.definition == MethodImplAttributes.class || candidate.definition == StreamingContextStates.class || candidate.definition == GenericParameterAttributes.class || candidate.definition == Byte.class || candidate.definition == SByte.class || candidate.definition == UInt16.class || candidate.definition == UInt32.class)) {
            return true;
        }
        if (this.definition == IFormattable.class && (candidate.definition == Int32.class || candidate.definition == DateTimeStyles.class || candidate.definition == TimeSpanStyles.class || candidate.definition == NumberStyles.class || candidate.definition == BindingFlags.class || (candidate.definition == MemberTypes.class || candidate.definition == FieldAttributes.class) || candidate.definition == CallingConventions.class || candidate.definition == MethodImplAttributes.class || candidate.definition == StreamingContextStates.class || candidate.definition == SByte.class || candidate.definition == GenericParameterAttributes.class || candidate.definition == Byte.class || candidate.definition == UInt16.class || candidate.definition == UInt32.class)) {
            return true;
        }
        if (this.definition == IConvertible.class && (candidate.definition == Int32.class || candidate.definition == DateTimeStyles.class || candidate.definition == TimeSpanStyles.class || candidate.definition == NumberStyles.class || candidate.definition == BindingFlags.class || (candidate.definition == MemberTypes.class || candidate.definition == FieldAttributes.class) || candidate.definition == CallingConventions.class || candidate.definition == MethodImplAttributes.class || candidate.definition == StreamingContextStates.class || candidate.definition == GenericParameterAttributes.class)) {
            return true;
        }
        if (this.definition == IConvertible.class && candidate.definition == String.class) {
            return true;
        }
        if (this.definition == IConvertible.class
                && (candidate.definition == Byte.class || candidate.definition == SByte.class)) {
            return true;
        }
        if (this.definition == IConvertible.class
                && (candidate.definition == UInt16.class || candidate.definition == UInt32.class)) {
            return true;
        }
        if (this.definition == IConvertible.class && candidate.definition == DateTime.class) {
            return true;
        }
        if ((this.definition == IConvertible.class || this.definition == IComparable.class || this.definition == IFormattable.class || this.definition == ISpanFormattable.class || this.definition == IUtf8SpanFormattable.class) && candidate.definition == Decimal.class) {
            return true;
        }
        if (this.definition == IConvertible.class && candidate.definition == DBNull.class) {
            return true;
        }
        if (this.definition == ISerializable.class
                && (candidate.definition == DBNull.class || Exception.class.isAssignableFrom(candidate.definition))) {
            return true;
        }
        if (this.definition == ISpanFormattable.class && (candidate.definition == Int32.class || candidate.definition == DateTimeStyles.class || candidate.definition == TimeSpanStyles.class || candidate.definition == NumberStyles.class || candidate.definition == BindingFlags.class || (candidate.definition == MemberTypes.class || candidate.definition == FieldAttributes.class) || candidate.definition == CallingConventions.class || candidate.definition == MethodImplAttributes.class || candidate.definition == StreamingContextStates.class || candidate.definition == GenericParameterAttributes.class || candidate.definition == SByte.class || candidate.definition == Byte.class || candidate.definition == UInt16.class || candidate.definition == UInt32.class)) {
            return true;
        }
        if (this.definition == IUtf8SpanFormattable.class && (candidate.definition == Int32.class || candidate.definition == SByte.class || candidate.definition == Byte.class || candidate.definition == UInt16.class || candidate.definition == UInt32.class)) {
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
        if ((this.get_IsByRef() || this.get_IsPointer()) && parent == fromJavaClass(Object.class)) {
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
        if (this.definition == java.util.Optional.class) {
            return this.arguments.size() == 1 && this.arguments.get(0).IsInstanceOfType(value);
        }
        if (value == null || this.get_IsByRef() || this.get_IsPointer()) {
            return false;
        }
        if (this.get_IsArray()) {
            if (this.GetArrayRank() != 1 || !value.getClass().isArray()) { return false; }
            Type targetElement = this.GetElementType();
            Type component = runtimeArrayComponent(value.getClass().getComponentType());
            if (targetElement.get_IsValueType() || component.get_IsValueType()) {
                return targetElement == component;
            }
            return targetElement.IsAssignableFrom(component);
        }
        if ((this.definition == IEnumerable.class || this.definition == ICollection.class)
                && value.getClass().isArray()) {
            return true;
        }
        if (this.definition == Object.class) {
            return true;
        }
        if (this.definition == Number.class) {
            return fromJavaClass(value.getClass()).get_IsValueType();
        }
        if (this.definition == Enum.class) {
            return fromJavaClass(value.getClass()).get_IsEnum();
        }
        if (this.definition == java.lang.reflect.Array.class) {
            return value.getClass().isArray();
        }
        if (this.definition == IComparable.class) {
            return value instanceof String || value instanceof Integer || value instanceof Int32
                    || value instanceof DateTime || value instanceof TimeSpan || value instanceof DateTimeStyles || value instanceof TimeSpanStyles || value instanceof NumberStyles || value instanceof BindingFlags || value instanceof MemberTypes || value instanceof CallingConventions || value instanceof MethodImplAttributes || value instanceof StreamingContextStates || value instanceof GenericParameterAttributes || value instanceof Byte || value instanceof SByte || value instanceof UInt16 || value instanceof UInt32;
        }
        if (this.definition == IFormattable.class) {
            return value instanceof Integer || value instanceof Int32 || value instanceof DateTime || value instanceof TimeSpan || value instanceof DateTimeStyles || value instanceof TimeSpanStyles || value instanceof NumberStyles || value instanceof BindingFlags || value instanceof MemberTypes || value instanceof CallingConventions || value instanceof MethodImplAttributes || value instanceof StreamingContextStates || value instanceof SByte || value instanceof GenericParameterAttributes || value instanceof Byte || value instanceof UInt16 || value instanceof UInt32;
        }
        if (this.definition == IConvertible.class) {
            return value instanceof String || value instanceof Integer || value instanceof Int32 || value instanceof DBNull
                    || value instanceof Byte || value instanceof SByte
                    || value instanceof UInt16 || value instanceof UInt32
                    || value instanceof DateTime || value instanceof Decimal || value instanceof DateTimeStyles || value instanceof TimeSpanStyles || value instanceof NumberStyles || value instanceof BindingFlags || value instanceof MemberTypes || value instanceof CallingConventions || value instanceof MethodImplAttributes || value instanceof StreamingContextStates || value instanceof GenericParameterAttributes;
        }
        if (this.definition == ISerializable.class) {
            return value instanceof DBNull || value instanceof Exception;
        }
        if (this.definition == ISpanFormattable.class) {
            return value instanceof Integer || value instanceof Int32 || value instanceof DateTime || value instanceof TimeSpan || value instanceof DateTimeStyles || value instanceof TimeSpanStyles || value instanceof NumberStyles || value instanceof BindingFlags || value instanceof MemberTypes || value instanceof CallingConventions || value instanceof MethodImplAttributes || value instanceof StreamingContextStates || value instanceof GenericParameterAttributes || value instanceof SByte || value instanceof Byte || value instanceof UInt16 || value instanceof UInt32;
        }
        if (this.definition == IUtf8SpanFormattable.class) {
            return value instanceof Integer || value instanceof Int32 || value instanceof DateTime || value instanceof TimeSpan || value instanceof SByte || value instanceof Byte || value instanceof UInt16 || value instanceof UInt32;
        }
        if (this.definition == Int32.class && value instanceof Integer) {
            return true;
        }
        if (this.definition == java.lang.reflect.Array.class) {
            return value.getClass().isArray();
        }
        if (this.definition == java.util.List.class
                || this.definition == java.util.Map.class) {
            return false;
        }
        return this.definition.isInstance(value);
    }

    private static Type runtimeArrayComponent(Class<?> component) {
        if (component.isArray()) { return runtimeArrayComponent(component.getComponentType()).MakeArrayType(); }
        if (component == boolean.class) { return fromJavaClass(Boolean.class); }
        if (component == char.class) { return fromJavaClass(Character.class); }
        if (component == short.class) { return fromJavaClass(Short.class); }
        if (component == long.class) { return fromJavaClass(Long.class); }
        if (component == float.class) { return fromJavaClass(Float.class); }
        if (component == double.class) { return fromJavaClass(Double.class); }
        return fromJavaClass(component);
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
            return new MemberInfo[] {selectedMethodMember(interfaceMethod, this)};
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
                return new MemberInfo[] {selectedMethodMember(interfaceMethod, this)};
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
            return new MemberInfo[] {selectedMethodMember(interfaceMethod, this)};
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
                return new MemberInfo[] {selectedMethodMember(interfaceMethod, this)};
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
                return new MethodInfo[] {selectedMethodMember(interfaceMethod, this)};
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
            return name.equals(interfaceMethod) ? selectedMethodMember(interfaceMethod, this) : null;
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
                return selectedMethodMember(interfaceMethod, this);
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
        boolean matches = this.selectedParameterTypesMatch(types, false);
        return matches ? selectedMethodMember(interfaceMethod, this) : null;
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
        return named != null && this.selectedParameterTypesMatch(types, flags.has(BindingFlags.ExactBinding)) ? named : null;
    }

    private boolean selectedParameterTypesMatch(Type[] types, boolean exact) {
        Type[] parameters = this.definition == IDisposable.class || this.definition == ICloneable.class
                ? new Type[0] : this.definition == IComparable.class
                ? new Type[] { fromJavaClass(Object.class) } : this.definition == IFormattable.class
                ? new Type[] { fromJavaClass(String.class), fromJavaClass(IFormatProvider.class) }
                : new Type[] { fromJavaClass(Type.class) };
        if (types.length != parameters.length) return false;
        for (int i = 0; i < types.length; i++) {
            if (parameters[i].Equals(types[i])) continue;
            if (exact) return false;
            if (parameters[i].Equals(fromJavaClass(Object.class))) continue;
            if (types[i].get_IsSignatureType() || !parameters[i].IsAssignableFrom(types[i])) return false;
        }
        return true;
    }

    private static MethodInfo selectedMethodMember(String name, Type owner) {
        return interfaceMethodMembers.computeIfAbsent(List.of(owner, name),
                ignored -> new DefaultMethodMember(name, owner));
    }

    private String selectedInterfaceMethodName() {
        if (this.definition == ICloneable.class) return "Clone";
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

    private static MemberInfo selectedDefaultProperty(String name, Type owner) {
        return defaultPropertyMembers.computeIfAbsent(List.of(owner, name),
                ignored -> new DefaultPropertyMember(name, owner));
    }

    public MemberInfo[] GetDefaultMembers() {
        if (this.definition == String.class && !this.get_HasElementType()) {
            return new MemberInfo[] {selectedDefaultProperty("Chars", this)};
        }
        if (this.definition == java.util.List.class && !this.get_HasElementType()) {
            return new MemberInfo[] {selectedDefaultProperty("Item", this)};
        }
        if (this.definition == Object.class || this.definition == Stopwatch.class || this.definition == IDisposable.class || this.definition == ICloneable.class
                || this.definition == MidpointRounding.class || this.definition == DigitShapes.class || this.definition == NormalizationForm.class || this.definition == TypeCode.class) {
            return EMPTY_DEFAULT_MEMBERS;
        }
        throw new UnsupportedOperationException("Default members are not mapped for this candidate type");
    }

    public Type[] GetOptionalCustomModifiers() {
        return new Type[0];
    }

    public Type[] GetRequiredCustomModifiers() {
        return new Type[0];
    }

    private boolean selectedTextProtocolType() {
        return this.definition == Encoder.class || this.definition == Decoder.class
                || this.definition == EncoderFallback.class
                || this.definition == DecoderFallback.class
                || this.definition == EncoderReplacementFallback.class
                || this.definition == DecoderReplacementFallback.class
                || this.definition == EncoderExceptionFallback.class
                || this.definition == DecoderExceptionFallback.class
                || this.definition == EncoderFallbackBuffer.class
                || this.definition == DecoderFallbackBuffer.class;
    }

    private boolean selectedIntegerFields() {
        return !this.get_HasElementType() && this.parameterIndex < 0 && (this.definition == Int32.class || this.definition == Byte.class
                || this.definition == SByte.class || this.definition == UInt16.class || this.definition == UInt32.class);
    }

    private boolean selectedPrimitiveBackingFields() {
        return !this.get_HasElementType() && this.parameterIndex < 0 && (this.definition == Boolean.class || this.definition == Character.class
                || this.definition == Short.class || this.definition == Long.class || this.definition == BigInteger.class
                || this.definition == Float.class || this.definition == Double.class);
    }

    public FieldInfo[] GetFields() {
        return this.GetFields(BindingFlags.Public.or(BindingFlags.Instance).or(BindingFlags.Static));
    }

    public FieldInfo[] GetFields(BindingFlags flags) {
        if (flags == null) throw new NullPointerException("flags");
        if (this.get_HasElementType()) return EMPTY_FIELDS;
        if ((this.definition == NumberStyles.class || this.definition == DateTimeStyles.class || this.definition == TimeSpanStyles.class || this.definition == MethodImplAttributes.class || this.definition == FieldAttributes.class || this.definition == BindingFlags.class || this.definition == MemberTypes.class) && !this.get_HasElementType()) {
            if (!flags.has(BindingFlags.Public) || !flags.has(BindingFlags.Instance) && !flags.has(BindingFlags.Static)) return EMPTY_FIELDS;
            String[] names = this.definition == MethodImplAttributes.class ? new String[] {"CodeTypeMask", "IL", "Native", "OPTIL", "Runtime", "ManagedMask", "Unmanaged", "Managed", "ForwardRef", "PreserveSig", "InternalCall", "Synchronized", "NoInlining", "AggressiveInlining", "NoOptimization", "AggressiveOptimization", "Async", "MaxMethodImplVal"} : this.definition == TimeSpanStyles.class ? new String[] {"None", "AssumeNegative"} : this.definition == DateTimeStyles.class ? new String[] {"None", "AllowLeadingWhite", "AllowTrailingWhite", "AllowInnerWhite", "AllowWhiteSpaces", "NoCurrentDateDefault", "AdjustToUniversal", "AssumeLocal", "AssumeUniversal", "RoundtripKind"} : this.definition == NumberStyles.class ? new String[] {"None", "AllowLeadingWhite", "AllowTrailingWhite", "AllowLeadingSign", "AllowTrailingSign", "AllowParentheses", "AllowDecimalPoint", "AllowThousands", "AllowExponent", "AllowCurrencySymbol", "AllowHexSpecifier", "AllowBinarySpecifier", "Integer", "HexNumber", "BinaryNumber", "Number", "Float", "Currency", "Any"} : this.definition == MemberTypes.class ? new String[] {"Constructor", "Event", "Field", "Method", "Property", "TypeInfo", "Custom", "NestedType", "All"} : this.definition == BindingFlags.class ? new String[] {"Default", "IgnoreCase", "DeclaredOnly", "Instance", "Static", "Public", "NonPublic", "FlattenHierarchy", "InvokeMethod", "CreateInstance", "GetField", "SetField", "GetProperty", "SetProperty", "PutDispProperty", "PutRefDispProperty", "ExactBinding", "SuppressChangeType", "OptionalParamBinding", "IgnoreReturn", "DoNotWrapExceptions"} : new String[] {"FieldAccessMask", "PrivateScope", "Private", "FamANDAssem", "Assembly", "Family", "FamORAssem", "Public", "Static", "InitOnly", "Literal", "NotSerialized", "SpecialName", "PinvokeImpl", "RTSpecialName", "HasFieldMarshal", "HasDefault", "HasFieldRVA", "ReservedMask"};
            List<FieldInfo> result = new java.util.ArrayList<>();
            if (flags.has(BindingFlags.Instance)) result.add(this.selectedEnumValueField());
            if (flags.has(BindingFlags.Static)) for (String name : names) result.add(this.selectedLiteralField(name));
            return result.toArray(new FieldInfo[0]);
        }
        if (this.selectedPrimitiveBackingFields()) {
            List<FieldInfo> result = new java.util.ArrayList<>();
            if (flags.has(BindingFlags.NonPublic) && flags.has(BindingFlags.Instance)) result.add(this.selectedPrimitiveValueField());
            if (flags.has(BindingFlags.Public) && flags.has(BindingFlags.Static)) {
                String[] names = this.definition == Boolean.class ? new String[] {"TrueString", "FalseString"}
                        : this.definition == Float.class || this.definition == Double.class ? new String[] {"MinValue", "MaxValue", "Epsilon", "NegativeInfinity", "PositiveInfinity", "NaN", "NegativeZero", "E", "Pi", "Tau"}
                        : new String[] {"MaxValue", "MinValue"};
                for (String name : names) result.add(this.selectedPrimitiveStaticField(name));
            }
            return result.isEmpty() ? EMPTY_FIELDS : result.toArray(new FieldInfo[0]);
        }
        if (this.selectedIntegerFields()) {
            List<FieldInfo> result = new java.util.ArrayList<>();
            if (flags.has(BindingFlags.NonPublic) && flags.has(BindingFlags.Instance)) result.add(this.selectedIntegerValueField());
            if (flags.has(BindingFlags.Public) && flags.has(BindingFlags.Static)) {
                result.add(this.selectedLiteralField("MaxValue")); result.add(this.selectedLiteralField("MinValue"));
            }
            return result.isEmpty() ? EMPTY_FIELDS : result.toArray(new FieldInfo[0]);
        }
        if (this.selectedInterfaceMethodName() != null) return EMPTY_FIELDS;
        throw new UnsupportedOperationException("Field inventory is not mapped for this candidate type");
    }

    public FieldInfo GetField(String name) {
        return this.GetField(name, BindingFlags.Public.or(BindingFlags.Instance).or(BindingFlags.Static));
    }

    public FieldInfo GetField(String name, BindingFlags flags) {
        if (name == null) throw new ArgumentNullException("name");
        if (flags == null) throw new NullPointerException("flags");
        if (this.definition == FieldAttributes.class && !this.get_HasElementType()) {
            if (flags.has(BindingFlags.Public) && flags.has(BindingFlags.Static)) {
                for (FieldAttributes value : FieldAttributes.values()) {
                    if (name.equals(value.get_Name()) || flags.has(BindingFlags.IgnoreCase) && name.equalsIgnoreCase(value.get_Name())) return this.selectedLiteralField(value.get_Name());
                }
            }
            if (flags.has(BindingFlags.Public) && flags.has(BindingFlags.Instance)
                    && (name.equals("value__") || flags.has(BindingFlags.IgnoreCase) && name.equalsIgnoreCase("value__"))) {
                return this.selectedEnumValueField();
            }
            return null;
        }
        for (FieldInfo field : this.GetFields(flags)) {
            if (name.equals(field.get_Name()) || flags.has(BindingFlags.IgnoreCase) && name.equalsIgnoreCase(field.get_Name())) return field;
        }
        return null;
    }

    private FieldInfo selectedPrimitiveStaticField(String name) {
        return literalFields.computeIfAbsent(List.of(this, name), ignored -> new PrimitiveStaticFieldMember(this, name));
    }

    private FieldInfo selectedPrimitiveValueField() {
        return literalFields.computeIfAbsent(List.of(this, "m_value"), ignored -> new PrimitiveValueFieldMember(this));
    }

    private FieldInfo selectedIntegerValueField() {
        return literalFields.computeIfAbsent(List.of(this, "m_value"), ignored -> new IntegerValueFieldMember(this));
    }

    private static String fieldTargetTypeName(Object target) {
        return target instanceof Type ? "System.RuntimeType" : fromJavaClass(target.getClass()).get_FullName();
    }

    private FieldInfo selectedEnumValueField() {
        return literalFields.computeIfAbsent(List.of(this, "value__"), ignored -> new EnumValueFieldMember(this));
    }

    private FieldInfo selectedLiteralField(String name) {
        return literalFields.computeIfAbsent(List.of(this, name), ignored -> new DefaultFieldMember(this, name));
    }

    public MemberInfo GetMemberWithSameMetadataDefinitionAs(MemberInfo member) {
        if (member == null) throw new ArgumentNullException("member");
        if (!this.get_IsSignatureType() && member instanceof PrimitiveStaticFieldMember field) {
            if (this.Equals(field.owner)) return this.selectedPrimitiveStaticField(field.name);
            throw new ArgumentException("A MemberInfo that matches '" + member.get_Name() + "' could not be found.", "member");
        }
        if (!this.get_IsSignatureType() && member instanceof PrimitiveValueFieldMember field) {
            if (this.Equals(field.owner)) return this.selectedPrimitiveValueField();
            throw new ArgumentException("A MemberInfo that matches '" + member.get_Name() + "' could not be found.", "member");
        }
        if (!this.get_IsSignatureType() && member instanceof IntegerValueFieldMember field) {
            if (this.Equals(field.owner)) return this.selectedIntegerValueField();
            throw new ArgumentException("A MemberInfo that matches '" + member.get_Name() + "' could not be found.", "member");
        }
        if (!this.get_IsSignatureType() && member instanceof EnumValueFieldMember field) {
            if (this.Equals(field.owner)) return this.selectedEnumValueField();
            throw new ArgumentException("A MemberInfo that matches '" + member.get_Name() + "' could not be found.", "member");
        }
        if (!this.get_IsSignatureType() && member instanceof DefaultFieldMember field) {
            if (this.Equals(field.owner)) return this.selectedLiteralField(field.name);
            throw new ArgumentException("A MemberInfo that matches '" + member.get_Name() + "' could not be found.", "member");
        }
        if (!this.get_IsSignatureType() && member instanceof DefaultMethodMember method) {
            if (this.Equals(method.owner)) return selectedMethodMember(method.name, this);
            throw new ArgumentException("A MemberInfo that matches '" + member.get_Name() + "' could not be found.", "member");
        }
        if (!this.get_IsSignatureType() && member instanceof Type && member.get_MemberType().get_Value() == MemberTypes.TypeInfo.get_Value()) {
            throw new ArgumentException("A MemberInfo that matches '" + member.get_Name() + "' could not be found.", "member");
        }
        if (!this.get_IsSignatureType() && member instanceof DefaultPropertyMember) {
            if (!this.get_HasElementType() && (this.definition == String.class || this.definition == java.util.List.class)) {
                for (MemberInfo candidate : this.GetDefaultMembers()) {
                    if (candidate.HasSameMetadataDefinitionAs(member)) return candidate;
                }
            }
            throw new ArgumentException("A MemberInfo that matches '" + member.get_Name() + "' could not be found.", "member");
        }
        BindingFlags all = BindingFlags.Public.or(BindingFlags.NonPublic).or(BindingFlags.Static).or(BindingFlags.Instance);
        for (MemberInfo candidate : this.GetMembers(all)) {
            if (candidate.HasSameMetadataDefinitionAs(member)) return candidate;
        }
        throw new ArgumentException("A MemberInfo that matches '" + member.get_Name() + "' could not be found.", "member");
    }

    public MemberInfo[] FindMembers(MemberTypes memberType, BindingFlags flags, MemberFilter filter, Object filterCriteria) {
        if (memberType == null) throw new NullPointerException("memberType");
        if (flags == null) throw new NullPointerException("flags");
        if (this.selectedInterfaceMethodName() == null) {
            boolean fieldOwner = this.selectedIntegerFields() || this.selectedPrimitiveBackingFields()
                    || (this.definition == NumberStyles.class || this.definition == DateTimeStyles.class || this.definition == TimeSpanStyles.class || this.definition == MethodImplAttributes.class || this.definition == FieldAttributes.class || this.definition == BindingFlags.class || this.definition == MemberTypes.class) && !this.get_HasElementType()
                    || this.get_HasElementType();
            if (fieldOwner && (memberType.get_Value() & 155) == 0) {
                List<MemberInfo> fields = new java.util.ArrayList<>();
                if (memberType.has(MemberTypes.Field)) {
                    for (FieldInfo field : this.GetFields(flags)) {
                        if (filter == null || filter.Invoke(field, filterCriteria)) fields.add(field);
                    }
                }
                return fields.toArray(new MemberInfo[0]);
            }
            throw new UnsupportedOperationException("Filtered member inventory is not mapped for this candidate type");
        }
        List<MemberInfo> members = new java.util.ArrayList<>();
        if (memberType.has(MemberTypes.Method)) {
            for (MethodInfo method : this.GetMethods(flags)) {
                if (filter == null || filter.Invoke(method, filterCriteria)) members.add(method);
            }
        }
        return members.toArray(new MemberInfo[0]);
    }

    public Type[] FindInterfaces(TypeFilter filter, Object filterCriteria) {
        if (filter == null) throw new ArgumentNullException("filter");
        Type[] interfaces = this.GetInterfaces();
        int count = 0;
        for (int i = 0; i < interfaces.length; i++) {
            if (filter.Invoke(interfaces[i], filterCriteria)) count++;
            else interfaces[i] = null;
        }
        if (count == interfaces.length) return interfaces;
        Type[] result = new Type[count];
        int index = 0;
        for (Type type : interfaces) if (type != null) result[index++] = type;
        return result;
    }

    public Type[] GetInterfaces() {
        if (!get_HasElementType() && selectedTextProtocolType()) return EMPTY_INTERFACE_TYPES;
        if (this.definition == ICloneable.class) return EMPTY_INTERFACE_TYPES;
        if (this.definition == NumberFormatInfo.class) {
            return new Type[] {fromJavaClass(IFormatProvider.class), fromJavaClass(ICloneable.class)};
        }
        if (!this.get_IsArray() && Encoding.class.isAssignableFrom(this.definition)) {
            return new Type[] {fromJavaClass(ICloneable.class)};
        }
        if (this.get_IsArray() || this.definition == java.lang.reflect.Array.class) {
            return new Type[] {fromJavaClass(ICollection.class), fromJavaClass(IEnumerable.class)};
        }

        if (this.definition == String.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == Int32.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(IConvertible.class),
                    fromJavaClass(IFormattable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IUtf8SpanFormattable.class)};
        }

        if (this.definition == MidpointRounding.class || this.definition == DigitShapes.class || this.definition == NormalizationForm.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == BindingFlags.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == FieldAttributes.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == MemberTypes.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == CallingConventions.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == MethodImplAttributes.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == StreamingContextStates.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == NumberStyles.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == TimeSpanStyles.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == DateTimeStyles.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == DateTime.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(IFormattable.class),
                    fromJavaClass(IConvertible.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IUtf8SpanFormattable.class)};
        }
        if (this.definition == TimeSpan.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(IFormattable.class),
                    fromJavaClass(ISpanFormattable.class), fromJavaClass(IUtf8SpanFormattable.class)};
        }
        if (this.definition == IDictionary.class) {
            return new Type[] {fromJavaClass(ICollection.class), fromJavaClass(IEnumerable.class)};
        }
        if (this.definition == ICollection.class) {
            return new Type[] {fromJavaClass(IEnumerable.class)};
        }
        if (this.definition == IDictionaryEnumerator.class) {
            return new Type[] {fromJavaClass(IEnumerator.class)};
        }
        if (this.definition == IEnumerable.class || this.definition == DictionaryEntry.class) {
            return EMPTY_INTERFACE_TYPES;
        }
        if (Exception.class.isAssignableFrom(this.definition)) {
            return new Type[] {fromJavaClass(ISerializable.class)};
        }
        if (this.definition == SerializationInfoEnumerator.class) {
            return new Type[] {fromJavaClass(IEnumerator.class)};
        }
        if (this.definition == DBNull.class) {
            return new Type[] {fromJavaClass(ISerializable.class),
                    fromJavaClass(IConvertible.class)};
        }
        if (this.definition == GenericParameterAttributes.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class)};
        }
        if (this.definition == Decimal.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IConvertible.class), fromJavaClass(IUtf8SpanFormattable.class)};
        }
        if (this.definition == SByte.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(IConvertible.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IUtf8SpanFormattable.class)};
        }
        if (this.definition == Byte.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(IConvertible.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IUtf8SpanFormattable.class)};
        }
        if (this.definition == UInt16.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(IConvertible.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IUtf8SpanFormattable.class)};
        }
        if (this.definition == UInt32.class) {
            return new Type[] {fromJavaClass(IComparable.class), fromJavaClass(IConvertible.class), fromJavaClass(ISpanFormattable.class), fromJavaClass(IFormattable.class), fromJavaClass(IUtf8SpanFormattable.class)};
        }
        if (this.definition == Byte.class || this.definition == SByte.class
                || this.definition == UInt16.class || this.definition == UInt32.class
                || this.definition == Decimal.class) {
            return new Type[] {fromJavaClass(IConvertible.class)};
        }
        if (this.definition == Object.class || this.definition == Stopwatch.class || this.definition == IDisposable.class
                || this.definition == IUtf8SpanFormattable.class || this.definition == IConvertible.class
                || this.definition == IComparable.class || this.definition == IFormattable.class || this.definition == IFormatProvider.class
                || this.definition == ISerializable.class || this.definition == IEnumerator.class
                || this.definition == IFormatterConverter.class) {
            return EMPTY_INTERFACE_TYPES;
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
        if (fullname == null) throw new ArgumentNullException("fullname");
        if (this.definition == MidpointRounding.class || this.definition == DigitShapes.class || this.definition == NormalizationForm.class || selectedTextProtocolType() || this.definition == ICloneable.class || this.definition == NumberFormatInfo.class || Encoding.class.isAssignableFrom(this.definition)
                || this.get_IsArray() || this.definition == java.lang.reflect.Array.class
                || this.definition == String.class || this.definition == Int32.class
                || this.definition == Byte.class || this.definition == SByte.class
                || this.definition == UInt16.class || this.definition == UInt32.class
                || this.definition == Decimal.class || this.definition == DBNull.class
                || this.definition == DateTime.class || this.definition == TimeSpan.class || this.definition == DateTimeStyles.class || this.definition == TimeSpanStyles.class || this.definition == NumberStyles.class || this.definition == BindingFlags.class || (this.definition == MemberTypes.class || this.definition == FieldAttributes.class) || this.definition == CallingConventions.class || this.definition == MethodImplAttributes.class || this.definition == StreamingContextStates.class || this.definition == GenericParameterAttributes.class
                || this.definition == Object.class || this.definition == Stopwatch.class
                || this.definition == IConvertible.class || this.definition == IComparable.class || this.definition == IFormattable.class
                || this.definition == IFormatProvider.class || this.definition == ISerializable.class
                || this.definition == IDisposable.class || this.definition == ISpanFormattable.class
                || this.definition == IUtf8SpanFormattable.class || this.definition == IEnumerable.class
                || this.definition == IEnumerator.class || this.definition == ICollection.class
                || this.definition == IDictionary.class || this.definition == IDictionaryEnumerator.class
                || this.definition == DictionaryEntry.class || this.definition == SerializationInfoEnumerator.class
                || this.definition == IFormatterConverter.class
                || Exception.class.isAssignableFrom(this.definition)) {
            int separator = fullname.lastIndexOf('.');
            String namespace = separator < 0 ? null : fullname.substring(0, separator);
            String name = fullname.substring(separator + 1);
            for (Type contract : GetInterfaces()) {
                if ((namespace == null || namespace.equals(contract.get_Namespace()))
                        && (name.equals(contract.get_Name()) || ignoreCase && asciiInterfaceNameEquals(name, contract.get_Name()))) {
                    return contract;
                }
            }
            return null;
        }
        throw new UnsupportedOperationException("Interface lookup is not mapped for this candidate type");
    }

    private static boolean asciiInterfaceNameEquals(String left, String right) {
        if (left.length() != right.length()) return false;
        for (int index = 0; index < left.length(); index++) {
            char actual = left.charAt(index), expected = right.charAt(index);
            if (actual >= 'A' && actual <= 'Z') actual = (char) (actual + ('a' - 'A'));
            if (expected >= 'A' && expected <= 'Z') expected = (char) (expected + ('a' - 'A'));
            if (actual != expected) return false;
        }
        return true;
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
        return element == null ? null : runtimeArrayComponent(element);
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

    public boolean get_IsNestedFamANDAssem() {
        return false;
    }

    public boolean get_IsNestedFamORAssem() {
        return false;
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
        if (this.definition == java.util.Optional.class) return GenericParameterAttributes.FromInt32(24);
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

    private boolean selectedCoreLibMetadataModule() {
        Type owner = this;
        while (owner.get_HasElementType()) owner = owner.GetElementType();
        if (owner.get_IsGenericParameter()) owner = owner.get_DeclaringType();
        if (owner == null) return false;
        if (owner.get_IsGenericType()) owner = owner.GetGenericTypeDefinition();
        String name = owner.get_FullName();
        return name != null && GetType(name, false, false) == owner;
    }

    @Override
    public boolean HasSameMetadataDefinitionAs(MemberInfo other) {
        if (other instanceof ModifiedFieldType) return false;
        if (other == null) throw new ArgumentNullException("other");
        if (this == other) return true;
        if (!(other instanceof Type type) || type.get_IsSignatureType()) return false;
        if (this.get_HasElementType() || type.get_HasElementType()) {
            return this.get_HasElementType() && type.get_HasElementType()
                    && this.selectedCoreLibMetadataModule() && type.selectedCoreLibMetadataModule();
        }
        return this.definition == type.definition && this.parameterIndex == type.parameterIndex;
    }

    public boolean Equals(Type other) {
        return this == other || other instanceof ModifiedFieldType modified && this == modified.underlying;
    }

    private static final class DefaultMethodMember extends MethodInfo {
        @Override
        public boolean HasSameMetadataDefinitionAs(MemberInfo other) {
            if (other == null) throw new ArgumentNullException("other");
            return other instanceof DefaultMethodMember method && this.name.equals(method.name)
                    && this.owner.HasSameMetadataDefinitionAs(method.owner)
                    && java.util.Objects.equals(this.captured, method.captured);
        }

        @Override
        public boolean get_IsCollectible() { return false; }
        private static final ParameterInfo[] EMPTY_PARAMETERS = new ParameterInfo[0];
        private volatile ParameterInfo[] parameters;
        private volatile ParameterInfo returnParameter;
        private final String name;
        private final Type owner;
        private final java.lang.reflect.Method captured;

        private DefaultMethodMember(String name, Type owner) {
            this.name = name;
            this.owner = owner;
            this.captured = null;
        }

        private DefaultMethodMember(java.lang.reflect.Method captured, Type owner) {
            this.name = captured.getName();
            this.owner = owner;
            this.captured = captured;
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
        public boolean get_IsPublic() {
            return this.captured == null
                    || java.lang.reflect.Modifier.isPublic(this.captured.getModifiers());
        }

        @Override
        public boolean get_IsStatic() {
            return this.captured != null
                    && java.lang.reflect.Modifier.isStatic(this.captured.getModifiers());
        }

        @Override
        public boolean get_IsAbstract() {
            return this.captured == null
                    || java.lang.reflect.Modifier.isAbstract(this.captured.getModifiers());
        }

        @Override
        public boolean get_IsVirtual() {
            return this.captured == null || (!this.get_IsStatic()
                    && !this.get_IsPrivate() && !this.get_IsFinal());
        }

        @Override
        public boolean get_IsFinal() {
            return this.captured != null
                    && java.lang.reflect.Modifier.isFinal(this.captured.getModifiers());
        }

        @Override
        public boolean get_IsSpecialName() {
            return false;
        }

        @Override
        public boolean get_IsConstructor() {
            return false;
        }

        @Override
        public boolean get_IsPrivate() {
            return this.captured != null
                    && java.lang.reflect.Modifier.isPrivate(this.captured.getModifiers());
        }

        @Override
        public boolean get_IsFamily() {
            return this.captured != null
                    && java.lang.reflect.Modifier.isProtected(this.captured.getModifiers());
        }

        @Override
        public boolean get_IsFamilyAndAssembly() {
            return false;
        }

        @Override
        public boolean get_IsFamilyOrAssembly() {
            return this.get_IsFamily();
        }

        @Override
        public boolean get_IsAssembly() {
            return this.captured != null && !this.get_IsPublic()
                    && !this.get_IsPrivate() && !this.get_IsFamily();
        }

        @Override
        public boolean get_IsHideBySig() {
            return true;
        }

        @Override
        public CallingConventions get_CallingConvention() {
            return this.get_IsStatic() ? CallingConventions.Standard
                    : CallingConventions.Standard.or(CallingConventions.HasThis);
        }

        @Override
        public boolean get_IsSecurityCritical() {
            return true;
        }

        @Override
        public boolean get_IsSecuritySafeCritical() {
            return false;
        }

        @Override
        public boolean get_IsSecurityTransparent() {
            return false;
        }

        @Override
        public MethodImplAttributes GetMethodImplementationFlags() {
            return MethodImplAttributes.IL;
        }

        @Override
        public MethodBody GetMethodBody() {
            return null;
        }

        @Override
        public boolean get_IsGenericMethod() {
            return false;
        }

        @Override
        public boolean get_IsGenericMethodDefinition() {
            return false;
        }

        @Override
        public boolean get_IsConstructedGenericMethod() {
            return false;
        }

        @Override
        public boolean get_ContainsGenericParameters() {
            return false;
        }

        @Override
        public Type[] GetGenericArguments() {
            return new Type[0];
        }

        @Override
        public MethodInfo GetBaseDefinition() {
            return this;
        }

        @Override
        public String ToString() {
            Type result = this.get_ReturnType();
            String resultName = result == fromJavaClass(Void.class)
                    || result == fromJavaClass(Int32.class)
                    ? result.get_Name() : result.get_FullName();
            StringBuilder text = new StringBuilder(resultName).append(' ')
                    .append(this.name).append('(');
            ParameterInfo[] parameters = this.GetParameters();
            for (int index = 0; index < parameters.length; index++) {
                if (index > 0) {
                    text.append(", ");
                }
                text.append(parameters[index].get_ParameterType().get_FullName());
            }
            return text.append(')').toString();
        }

        @Override
        public Type get_ReturnType() {
            if (this.captured != null) {
                return fromJavaClass(this.captured.getReturnType());
            }
            return switch (this.name) {
                case "Dispose" -> fromJavaClass(Void.class);
                case "CompareTo" -> fromJavaClass(Int32.class);
                case "ToString" -> fromJavaClass(String.class);
                case "GetFormat", "Clone" -> fromJavaClass(Object.class);
                default -> throw new UnsupportedOperationException("Method return type is not mapped");
            };
        }

        @Override
        public ParameterInfo get_ReturnParameter() {
            ParameterInfo value = this.returnParameter;
            if (value == null) {
                synchronized (this) {
                    value = this.returnParameter;
                    if (value == null) {
                        value = new DefaultParameterInfo(this.name.equals("ToString") ? "" : null,
                                this.get_ReturnType(), -1, this);
                        this.returnParameter = value;
                    }
                }
            }
            return value;
        }

        @Override
        public ParameterInfo[] GetParameters() {
            ParameterInfo[] values = this.parameters;
            if (values == null) {
                synchronized (this) {
                    values = this.parameters;
                    if (values == null) {
                        values = this.createParameters();
                        if (values.length == 0) values = EMPTY_PARAMETERS;
                        this.parameters = values;
                    }
                }
            }
            return values.length == 0 ? values : values.clone();
        }

        private ParameterInfo[] createParameters() {
            if (this.captured != null) {
                java.lang.reflect.Parameter[] parameters = this.captured.getParameters();
                ParameterInfo[] result = new ParameterInfo[parameters.length];
                for (int index = 0; index < parameters.length; index++) {
                    result[index] = new DefaultParameterInfo(parameters[index].getName(),
                            fromJavaClass(parameters[index].getType()), index, this);
                }
                return result;
            }
            return switch (this.name) {
                case "Dispose", "Clone" -> new ParameterInfo[0];
                case "CompareTo" -> new ParameterInfo[] {
                    new DefaultParameterInfo("obj", fromJavaClass(Object.class), 0, this)};
                case "ToString" -> new ParameterInfo[] {
                    new DefaultParameterInfo("format", fromJavaClass(String.class), 0, this),
                    new DefaultParameterInfo("formatProvider", fromJavaClass(IFormatProvider.class), 1, this)};
                case "GetFormat" -> new ParameterInfo[] {
                    new DefaultParameterInfo("formatType", fromJavaClass(Type.class), 0, this)};
                default -> throw new UnsupportedOperationException("Method parameters are not mapped");
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

    private static final class DefaultParameterInfo extends ParameterInfo {
        private DefaultParameterInfo(String name, Type parameterType, int position,
                MemberInfo member) {
            super(name, parameterType, position, member);
        }
    }

    private static final class ModifiedFieldType extends Type {
        private final Type underlying;
        private ModifiedFieldType(Type type) { super(type.definition, type.arguments, type.parameterIndex); this.underlying = type; }
        private NotSupportedException unsupported() { return new NotSupportedException("Modified types do not support this member. Use the UnderlyingSystemType property to call this member."); }
        @Override public boolean get_IsSignatureType() { return this.underlying.get_IsSignatureType(); }
        @Override public boolean get_IsGenericParameter() { return this.underlying.get_IsGenericParameter(); }
        @Override public boolean get_IsGenericTypeParameter() { return this.underlying.get_IsGenericTypeParameter(); }
        @Override public boolean get_IsGenericMethodParameter() { return this.underlying.get_IsGenericMethodParameter(); }
        @Override public boolean get_ContainsGenericParameters() { return this.underlying.get_ContainsGenericParameters(); }
        @Override public boolean get_IsGenericType() { return this.underlying.get_IsGenericType(); }
        @Override public boolean get_IsGenericTypeDefinition() { return this.underlying.get_IsGenericTypeDefinition(); }
        @Override public boolean get_IsConstructedGenericType() { return this.underlying.get_IsConstructedGenericType(); }
        @Override public boolean get_IsTypeDefinition() { return this.underlying.get_IsTypeDefinition(); }
        @Override public boolean get_HasElementType() { return this.underlying.get_HasElementType(); }
        @Override public boolean get_IsArray() { return this.underlying.get_IsArray(); }
        @Override public boolean get_IsSZArray() { return this.underlying.get_IsSZArray(); }
        @Override public boolean get_IsVariableBoundArray() { return this.underlying.get_IsVariableBoundArray(); }
        @Override public boolean get_IsPointer() { return this.underlying.get_IsPointer(); }
        @Override public boolean get_IsByRef() { return this.underlying.get_IsByRef(); }
        @Override public boolean get_IsByRefLike() { return this.underlying.get_IsByRefLike(); }
        @Override public boolean get_IsFunctionPointer() { return this.underlying.get_IsFunctionPointer(); }
        @Override public boolean get_IsUnmanagedFunctionPointer() { return this.underlying.get_IsUnmanagedFunctionPointer(); }
        @Override public boolean get_IsCollectible() { return this.underlying.get_IsCollectible(); }
        @Override public boolean get_IsEnum() { return this.underlying.get_IsEnum(); }
        @Override public boolean get_IsValueType() { return this.underlying.get_IsValueType(); }
        @Override public boolean get_IsPrimitive() { return this.underlying.get_IsPrimitive(); }
        @Override public boolean get_IsClass() { return this.underlying.get_IsClass(); }
        @Override public boolean get_IsInterface() { return this.underlying.get_IsInterface(); }
        @Override public boolean get_IsAbstract() { return this.underlying.get_IsAbstract(); }
        @Override public boolean get_IsSealed() { return true; }
        @Override public boolean get_IsPublic() { return this.underlying.get_IsPublic(); }
        @Override public boolean get_IsNotPublic() { return this.underlying.get_IsNotPublic(); }
        @Override public boolean get_IsNested() { throw unsupported(); }
        @Override public boolean get_IsNestedPublic() { return this.underlying.get_IsNestedPublic(); }
        @Override public boolean get_IsNestedPrivate() { return this.underlying.get_IsNestedPrivate(); }
        @Override public boolean get_IsNestedAssembly() { return this.underlying.get_IsNestedAssembly(); }
        @Override public boolean get_IsNestedFamily() { return this.underlying.get_IsNestedFamily(); }
        @Override public boolean get_IsVisible() { throw unsupported(); }
        @Override public boolean get_IsSerializable() { return true; }
        @Override public boolean get_IsSpecialName() { return this.underlying.get_IsSpecialName(); }
        @Override public boolean get_IsAnsiClass() { return this.underlying.get_IsAnsiClass(); }
        @Override public boolean get_IsUnicodeClass() { return this.underlying.get_IsUnicodeClass(); }
        @Override public boolean get_IsAutoClass() { return this.underlying.get_IsAutoClass(); }
        @Override public boolean get_IsAutoLayout() { return this.underlying.definition == String.class; }
        @Override public boolean get_IsLayoutSequential() { return this.underlying.definition != String.class; }
        @Override public boolean get_IsExplicitLayout() { return this.underlying.get_IsExplicitLayout(); }
        @Override public boolean get_IsImport() { return this.underlying.get_IsImport(); }
        @Override public boolean get_IsCOMObject() { return this.underlying.get_IsCOMObject(); }
        @Override public boolean get_IsContextful() { return this.underlying.get_IsContextful(); }
        @Override public boolean get_IsMarshalByRef() { return this.underlying.get_IsMarshalByRef(); }
        @Override public boolean get_IsSecurityCritical() { return this.underlying.get_IsSecurityCritical(); }
        @Override public boolean get_IsSecuritySafeCritical() { return this.underlying.get_IsSecuritySafeCritical(); }
        @Override public boolean get_IsSecurityTransparent() { return this.underlying.get_IsSecurityTransparent(); }
        @Override public String get_Name() { return this.underlying.get_Name(); }
        @Override public String get_Namespace() { return this.underlying.get_Namespace(); }
        @Override public String get_FullName() { return this.underlying.get_FullName(); }
        @Override public String get_AssemblyQualifiedName() { return this.underlying.get_AssemblyQualifiedName(); }
        @Override public int get_GenericParameterPosition() { throw new InvalidOperationException("Method may only be called on a Type for which Type.IsGenericParameter is true."); }
        @Override public Type get_BaseType() { throw unsupported(); }
        @Override public Type get_DeclaringType() { throw unsupported(); }
        @Override public Type get_ReflectedType() { throw unsupported(); }
        @Override public Type get_UnderlyingSystemType() { return this.underlying; }
        @Override public MemberTypes get_MemberType() { return this.underlying.get_MemberType(); }
        @Override public GenericParameterAttributes get_GenericParameterAttributes() { throw new InvalidOperationException("Method may only be called on a Type for which Type.IsGenericParameter is true."); }
        @Override public Type[] get_GenericTypeArguments() { return this.underlying.get_GenericTypeArguments(); }
        @Override public boolean Equals(Type other) { throw unsupported(); }
        @Override public boolean Equals(Object other) { throw unsupported(); }
        @Override public int GetHashCode() { throw unsupported(); }
        @Override public String ToString() { return this.underlying.ToString(); }
        @Override public boolean IsAssignableFrom(Type other) { if (other == this) return true; if (other instanceof ModifiedFieldType || other != null && other.get_IsSignatureType()) throw unsupported(); return this.underlying.IsAssignableFrom(other); }
        @Override public boolean IsInstanceOfType(Object value) { return this.underlying.IsInstanceOfType(value); }
        @Override public boolean IsEquivalentTo(Type other) { if (other == this) return true; if (other instanceof ModifiedFieldType || other != null && other.get_IsSignatureType()) throw unsupported(); return false; }
        @Override public boolean IsSubclassOf(Type parent) { if (parent == this) return false; throw unsupported(); }
        @Override public Type[] GetGenericArguments() { throw new NotSupportedException("Derived classes must provide an implementation."); }
        @Override public Type GetGenericTypeDefinition() { throw new InvalidOperationException("This operation is only valid on generic types."); }
        @Override public int GetArrayRank() { throw new ArgumentException("Must be an array type."); }
        @Override public Type GetElementType() { return this.underlying.GetElementType(); }
        @Override public Type[] GetGenericParameterConstraints() { throw new InvalidOperationException("Method may only be called on a Type for which Type.IsGenericParameter is true."); }
        @Override public Type GetFunctionPointerReturnType() { throw new InvalidOperationException("Method may only be called on a Type for which Type.IsFunctionPointer is true."); }
        @Override public Type[] GetFunctionPointerParameterTypes() { throw new InvalidOperationException("Method may only be called on a Type for which Type.IsFunctionPointer is true."); }
        @Override public Type[] GetFunctionPointerCallingConventions() { throw new InvalidOperationException("Method may only be called on a Type for which Type.IsFunctionPointer is true."); }
        @Override public Type[] GetInterfaces() { throw unsupported(); }
        @Override public Type[] GetOptionalCustomModifiers() { return new Type[0]; }
        @Override public Type[] GetRequiredCustomModifiers() { return new Type[0]; }
        @Override public MemberInfo[] GetDefaultMembers() { throw new NotImplementedException(); }
        @Override public boolean HasSameMetadataDefinitionAs(MemberInfo other) { throw new NotImplementedException(); }
        @Override public Type MakeGenericType(Type[] arguments) { throw new NotSupportedException("Derived classes must provide an implementation."); }
        @Override public Type MakeArrayType() { throw new NotSupportedException(); }
        @Override public Type MakeArrayType(int rank) { throw new NotSupportedException(); }
        @Override public Type MakeByRefType() { throw new NotSupportedException(); }
        @Override public Type MakePointerType() { throw new NotSupportedException(); }
        @Override public MethodInfo[] GetMethods(BindingFlags flags) { throw unsupported(); }
        @Override public MemberInfo[] GetMembers(BindingFlags flags) { throw unsupported(); }
        @Override public MethodInfo GetMethod(String name, Type[] types) {
            if (name == null) throw new ArgumentNullException("name");
            if (types == null) throw new ArgumentNullException("types");
            for (Type type : types) if (type == null) throw new ArgumentNullException("types");
            throw unsupported();
        }
        @Override public MethodInfo GetMethod(String name, BindingFlags flags, Type[] types) {
            return this.GetMethod(name, types);
        }
        @Override public MemberInfo[] GetMembers() { throw unsupported(); }
        @Override public MemberInfo[] GetMember(String name, MemberTypes kinds, BindingFlags flags) { throw unsupported(); }
        @Override public FieldInfo GetField(String name) { throw unsupported(); }
        @Override public MemberInfo[] FindMembers(MemberTypes kinds, BindingFlags flags, MemberFilter filter, Object criteria) {
            if ((kinds.get_Value() & 159) != 0) throw unsupported();
            return new MemberInfo[0];
        }
        @Override public MethodInfo GetMethod(String name) { if (name == null) throw new ArgumentNullException("name"); throw unsupported(); }
        @Override public MethodInfo GetMethod(String name, BindingFlags flags) { if (name == null) throw new ArgumentNullException("name"); throw unsupported(); }
        @Override public MemberInfo[] GetMember(String name) { throw unsupported(); }
        @Override public MemberInfo[] GetMember(String name, BindingFlags flags) { throw unsupported(); }
        @Override public Type GetNestedType(String name) { throw unsupported(); }
        @Override public Type GetNestedType(String name, BindingFlags flags) { throw unsupported(); }
        @Override public Type GetInterface(String name) { throw unsupported(); }
        @Override public Type GetInterface(String name, boolean ignoreCase) { throw unsupported(); }
        @Override public FieldInfo[] GetFields(BindingFlags flags) { throw unsupported(); }
        @Override public FieldInfo GetField(String name, BindingFlags flags) { throw unsupported(); }
        @Override public MemberInfo GetMemberWithSameMetadataDefinitionAs(MemberInfo member) { throw unsupported(); }
    }

    private static final class PrimitiveStaticFieldMember extends FieldInfo {
        private final Type owner;
        private final String name;
        private PrimitiveStaticFieldMember(Type owner, String name) { this.owner = owner; this.name = name; }
        private boolean readonlyString() { return this.owner.definition == Boolean.class; }
        @Override public boolean get_IsSecurityCritical() { return true; }
        @Override public boolean get_IsSecuritySafeCritical() { return false; }
        @Override public boolean get_IsSecurityTransparent() { return false; }
        @Override public Type[] GetOptionalCustomModifiers() { return this.get_IsLiteral() ? EMPTY_FIELD_MODIFIERS : new Type[0]; }
        @Override public Type[] GetRequiredCustomModifiers() { return this.get_IsLiteral() ? EMPTY_FIELD_MODIFIERS : new Type[0]; }
        @Override public Type GetModifiedFieldType() { if (this.get_IsLiteral()) throw new NotSupportedException(); return new ModifiedFieldType(this.get_FieldType()); }
        @Override public String get_Name() { return this.name; }
        @Override public Type get_DeclaringType() { return this.owner; }
        @Override public Type get_ReflectedType() { return this.owner; }
        @Override public MemberTypes get_MemberType() { return MemberTypes.Field; }
        @Override public Type get_FieldType() { return this.readonlyString() ? Type.GetType("System.String") : this.owner; }
        @Override public FieldAttributes get_Attributes() { return FieldAttributes.FromInt32(this.readonlyString() ? 54 : 32854); }
        @Override public boolean get_IsCollectible() { return false; }
        @Override public String ToString() { return (this.readonlyString() ? "System.String" : this.owner.get_Name()) + " " + this.name; }
        @Override public boolean HasSameMetadataDefinitionAs(MemberInfo other) {
            if (other == null) throw new ArgumentNullException("other");
            return other instanceof PrimitiveStaticFieldMember field && this.name.equals(field.name) && this.owner.HasSameMetadataDefinitionAs(field.owner);
        }
        @SuppressWarnings("removal")
        private Object constant() {
            if (this.readonlyString()) return this.name.equals("TrueString") ? "True" : "False";
            if (this.owner.definition == Character.class) return new Character(this.name.equals("MaxValue") ? Character.MAX_VALUE : Character.MIN_VALUE);
            if (this.owner.definition == Short.class) return new Short(this.name.equals("MaxValue") ? Short.MAX_VALUE : Short.MIN_VALUE);
            if (this.owner.definition == Long.class) return new Long(this.name.equals("MaxValue") ? Long.MAX_VALUE : Long.MIN_VALUE);
            if (this.owner.definition == BigInteger.class) return this.name.equals("MaxValue") ? new BigInteger("18446744073709551615") : new BigInteger("0");
            if (this.owner.definition == Float.class) return new Float(switch(this.name) {
                case "MinValue" -> -Float.MAX_VALUE; case "MaxValue" -> Float.MAX_VALUE; case "Epsilon" -> Float.MIN_VALUE;
                case "NegativeInfinity" -> Float.NEGATIVE_INFINITY; case "PositiveInfinity" -> Float.POSITIVE_INFINITY;
                case "NaN" -> Float.intBitsToFloat(0xffc00000); case "NegativeZero" -> -0.0f; case "E" -> (float) Math.E;
                case "Pi" -> (float) Math.PI; case "Tau" -> (float) (2.0 * Math.PI); default -> throw new UnsupportedOperationException("Unknown floating field");
            });
            return new Double(switch(this.name) {
                case "MinValue" -> -Double.MAX_VALUE; case "MaxValue" -> Double.MAX_VALUE; case "Epsilon" -> Double.MIN_VALUE;
                case "NegativeInfinity" -> Double.NEGATIVE_INFINITY; case "PositiveInfinity" -> Double.POSITIVE_INFINITY;
                case "NaN" -> Double.longBitsToDouble(0xfff8000000000000L); case "NegativeZero" -> -0.0d; case "E" -> Math.E;
                case "Pi" -> Math.PI; case "Tau" -> 2.0 * Math.PI; default -> throw new UnsupportedOperationException("Unknown floating field");
            });
        }
        @Override public Object GetValue(Object target) { return this.constant(); }
        @Override public Object GetRawConstantValue() {
            if (this.readonlyString()) throw new InvalidOperationException("Operation is not valid due to the current state of the object.");
            return this.constant();
        }
        @Override public void SetValue(Object target, Object value) {
            if (this.readonlyString()) throw new FieldAccessException("Cannot set initonly static field '" + this.name + "' after type 'System.Boolean' is initialized.");
            throw new FieldAccessException("Cannot set a constant field.");
        }
    }

    private static final class PrimitiveValueFieldMember extends FieldInfo {
        private final Type owner;
        private PrimitiveValueFieldMember(Type owner) { this.owner = owner; }
        @Override public boolean get_IsSecurityCritical() { return true; }
        @Override public boolean get_IsSecuritySafeCritical() { return false; }
        @Override public boolean get_IsSecurityTransparent() { return false; }
        @Override public Type[] GetOptionalCustomModifiers() { return this.get_IsLiteral() ? EMPTY_FIELD_MODIFIERS : new Type[0]; }
        @Override public Type[] GetRequiredCustomModifiers() { return this.get_IsLiteral() ? EMPTY_FIELD_MODIFIERS : new Type[0]; }
        @Override public Type GetModifiedFieldType() { return new ModifiedFieldType(this.get_FieldType()); }
        @Override public String get_Name() { return "m_value"; }
        @Override public Type get_DeclaringType() { return this.owner; }
        @Override public Type get_ReflectedType() { return this.owner; }
        @Override public MemberTypes get_MemberType() { return MemberTypes.Field; }
        @Override public Type get_FieldType() { return this.owner; }
        @Override public FieldAttributes get_Attributes() { return FieldAttributes.FromInt32(33); }
        @Override public boolean get_IsCollectible() { return false; }
        @Override public String ToString() { return this.owner.get_Name() + " m_value"; }
        @Override public boolean HasSameMetadataDefinitionAs(MemberInfo other) {
            if (other == null) throw new ArgumentNullException("other");
            return other instanceof PrimitiveValueFieldMember field && this.owner.HasSameMetadataDefinitionAs(field.owner);
        }
        @Override public Object GetRawConstantValue() { throw new InvalidOperationException("Operation is not valid due to the current state of the object."); }
        @SuppressWarnings("removal")
        @Override public Object GetValue(Object target) {
            if (target == null) throw new TargetException("Non-static field requires a target.");
            if (!this.owner.Equals(fromJavaClass(target.getClass()))) throw new ArgumentException("Field 'm_value' defined on type '" + this.owner.get_FullName() + "' is not a field on the target object which is of type '" + fieldTargetTypeName(target) + "'.");
            if (target instanceof Boolean value) return new Boolean(value);
            if (target instanceof Character value) return new Character(value);
            if (target instanceof Short value) return new Short(value);
            if (target instanceof Long value) return new Long(value);
            if (target instanceof BigInteger value) return new BigInteger(value.toString());
            if (target instanceof Float value) return new Float(value);
            if (target instanceof Double value) return new Double(value);
            throw new UnsupportedOperationException("Primitive field carrier is not mapped");
        }
        @Override public void SetValue(Object target, Object value) { throw new UnsupportedOperationException("Primitive instance field writes are not mapped for this candidate profile"); }
    }

    private static final class IntegerValueFieldMember extends FieldInfo {
        private final Type owner;
        private IntegerValueFieldMember(Type owner) { this.owner = owner; }
        @Override public boolean get_IsSecurityCritical() { return true; }
        @Override public boolean get_IsSecuritySafeCritical() { return false; }
        @Override public boolean get_IsSecurityTransparent() { return false; }
        @Override public Type[] GetOptionalCustomModifiers() { return this.get_IsLiteral() ? EMPTY_FIELD_MODIFIERS : new Type[0]; }
        @Override public Type[] GetRequiredCustomModifiers() { return this.get_IsLiteral() ? EMPTY_FIELD_MODIFIERS : new Type[0]; }
        @Override public Type GetModifiedFieldType() { return new ModifiedFieldType(this.get_FieldType()); }
        @Override public String get_Name() { return "m_value"; }
        @Override public Type get_DeclaringType() { return this.owner; }
        @Override public Type get_ReflectedType() { return this.owner; }
        @Override public MemberTypes get_MemberType() { return MemberTypes.Field; }
        @Override public Type get_FieldType() { return this.owner; }
        @Override public FieldAttributes get_Attributes() { return FieldAttributes.FromInt32(33); }
        @Override public boolean get_IsCollectible() { return false; }
        @Override public String ToString() { return this.owner.get_Name() + " m_value"; }
        @Override public boolean HasSameMetadataDefinitionAs(MemberInfo other) {
            if (other == null) throw new ArgumentNullException("other");
            return other instanceof IntegerValueFieldMember field && this.owner.HasSameMetadataDefinitionAs(field.owner);
        }
        @Override public Object GetRawConstantValue() { throw new InvalidOperationException("Operation is not valid due to the current state of the object."); }
        @Override public Object GetValue(Object target) {
            if (target == null) throw new TargetException("Non-static field requires a target.");
            if (!this.owner.Equals(fromJavaClass(target.getClass()))) {
                throw new ArgumentException("Field 'm_value' defined on type '" + this.owner.get_FullName() + "' is not a field on the target object which is of type '" + fieldTargetTypeName(target) + "'.");
            }
            if (target instanceof Int32 value) return new Int32(value.get_Value());
            if (target instanceof Integer value) return new Int32(value);
            if (target instanceof Byte value) return new Byte(value.get_Value());
            if (target instanceof SByte value) return new SByte(value.get_Value());
            if (target instanceof java.lang.Byte value) return new Byte(java.lang.Byte.toUnsignedInt(value));
            if (target instanceof UInt16 value) return new UInt16(value.get_Value());
            if (target instanceof UInt32 value) return new UInt32(value.get_Value());
            throw new UnsupportedOperationException("Integer field carrier is not mapped");
        }
        @Override public void SetValue(Object target, Object value) { throw new UnsupportedOperationException("Integer instance field writes are not mapped for this candidate profile"); }
    }

    private static final class EnumValueFieldMember extends FieldInfo {
        private final Type owner;
        private EnumValueFieldMember(Type owner) { this.owner = owner; }
        @Override public boolean get_IsSecurityCritical() { return true; }
        @Override public boolean get_IsSecuritySafeCritical() { return false; }
        @Override public boolean get_IsSecurityTransparent() { return false; }
        @Override public Type[] GetOptionalCustomModifiers() { return this.get_IsLiteral() ? EMPTY_FIELD_MODIFIERS : new Type[0]; }
        @Override public Type[] GetRequiredCustomModifiers() { return this.get_IsLiteral() ? EMPTY_FIELD_MODIFIERS : new Type[0]; }
        @Override public Type GetModifiedFieldType() { return new ModifiedFieldType(this.get_FieldType()); }
        @Override public String get_Name() { return "value__"; }
        @Override public Type get_DeclaringType() { return this.owner; }
        @Override public Type get_ReflectedType() { return this.owner; }
        @Override public MemberTypes get_MemberType() { return MemberTypes.Field; }
        @Override public Type get_FieldType() { return Type.GetType("System.Int32"); }
        @Override public FieldAttributes get_Attributes() { return FieldAttributes.FromInt32(1542); }
        @Override public boolean get_IsCollectible() { return false; }
        @Override public String ToString() { return "Int32 value__"; }
        @Override public boolean HasSameMetadataDefinitionAs(MemberInfo other) {
            if (other == null) throw new ArgumentNullException("other");
            return other instanceof EnumValueFieldMember field && this.owner.HasSameMetadataDefinitionAs(field.owner);
        }
        @Override public Object GetRawConstantValue() { throw new InvalidOperationException("Operation is not valid due to the current state of the object."); }
        @Override public Object GetValue(Object target) {
            if (target == null) throw new TargetException("Non-static field requires a target.");
            if (this.owner.definition == NumberStyles.class && target instanceof NumberStyles value) return new Int32(value.get_Value());
            if (this.owner.definition == DateTimeStyles.class && target instanceof DateTimeStyles value) return new Int32(value.get_Value());
            if (this.owner.definition == TimeSpanStyles.class && target instanceof TimeSpanStyles value) return new Int32(value.get_Value());
            if (this.owner.definition == MethodImplAttributes.class && target instanceof MethodImplAttributes value) return new Int32(value.get_Value());
            if (this.owner.definition == FieldAttributes.class && target instanceof FieldAttributes value) return new Int32(value.get_Value());
            if (this.owner.definition == BindingFlags.class && target instanceof BindingFlags value) return new Int32(value.get_Value());
            if (this.owner.definition == MemberTypes.class && target instanceof MemberTypes value) return new Int32(value.get_Value());
            String name = fieldTargetTypeName(target);
            throw new ArgumentException("Field 'value__' defined on type '" + this.owner.get_FullName() + "' is not a field on the target object which is of type '" + name + "'.");
        }
        @Override public void SetValue(Object target, Object value) { throw new UnsupportedOperationException("Enum instance field writes are not mapped for this candidate profile"); }
    }

    private static final class DefaultFieldMember extends FieldInfo {
        private final Type owner;
        private final String name;
        private DefaultFieldMember(Type owner, String name) { this.owner = owner; this.name = name; }
        @Override public boolean get_IsSecurityCritical() { return true; }
        @Override public boolean get_IsSecuritySafeCritical() { return false; }
        @Override public boolean get_IsSecurityTransparent() { return false; }
        @Override public Type[] GetOptionalCustomModifiers() { return this.get_IsLiteral() ? EMPTY_FIELD_MODIFIERS : new Type[0]; }
        @Override public Type[] GetRequiredCustomModifiers() { return this.get_IsLiteral() ? EMPTY_FIELD_MODIFIERS : new Type[0]; }
        @Override public String get_Name() { return this.name; }
        @Override public Type get_DeclaringType() { return this.owner; }
        @Override public Type get_ReflectedType() { return this.owner; }
        @Override public MemberTypes get_MemberType() { return MemberTypes.Field; }
        @Override public Type get_FieldType() { return this.owner; }
        @Override public FieldAttributes get_Attributes() { return FieldAttributes.FromInt32(32854); }
        @Override public boolean get_IsCollectible() { return false; }
        @Override public boolean HasSameMetadataDefinitionAs(MemberInfo other) {
            if (other == null) throw new ArgumentNullException("other");
            return other instanceof DefaultFieldMember field && this.name.equals(field.name) && this.owner.HasSameMetadataDefinitionAs(field.owner);
        }
        private int enumConstant() {
            if (this.owner.definition == MethodImplAttributes.class) { for (MethodImplAttributes value : MethodImplAttributes.values()) if (value.get_Name().equals(this.name)) return value.get_Value(); }
            if (this.owner.definition == TimeSpanStyles.class) { for (TimeSpanStyles value : TimeSpanStyles.values()) if (value.get_Name().equals(this.name)) return value.get_Value(); }
            if (this.owner.definition == DateTimeStyles.class) { for (DateTimeStyles value : DateTimeStyles.values()) if (value.get_Name().equals(this.name)) return value.get_Value(); }
            if (this.owner.definition == NumberStyles.class) { for (NumberStyles value : NumberStyles.values()) if (value.get_Name().equals(this.name)) return value.get_Value(); }
            if (this.owner.definition == MemberTypes.class) { for (MemberTypes value : MemberTypes.values()) if (value.get_Name().equals(this.name)) return value.get_Value(); }
            if (this.owner.definition == BindingFlags.class) { for (BindingFlags value : BindingFlags.values()) if (value.get_Name().equals(this.name)) return value.get_Value(); }
            for (FieldAttributes value : FieldAttributes.values()) if (value.get_Name().equals(this.name)) return value.get_Value();
            throw new UnsupportedOperationException("Enum field constant is not mapped");
        }
        @Override public Object GetValue(Object target) {
            if (this.owner.definition == MethodImplAttributes.class) return MethodImplAttributes.FromInt32(this.enumConstant());
            if (this.owner.definition == TimeSpanStyles.class) return TimeSpanStyles.FromInt32(this.enumConstant());
            if (this.owner.definition == DateTimeStyles.class) return DateTimeStyles.FromInt32(this.enumConstant());
            if (this.owner.definition == NumberStyles.class) return NumberStyles.FromInt32(this.enumConstant());
            if (this.owner.definition == MemberTypes.class) return MemberTypes.FromInt32(this.enumConstant());
            if (this.owner.definition == BindingFlags.class) return BindingFlags.FromInt32(this.enumConstant());
            return this.owner.definition == FieldAttributes.class ? FieldAttributes.FromInt32(this.enumConstant()) : this.GetRawConstantValue();
        }
        @Override public void SetValue(Object target, Object value) { throw new FieldAccessException("Cannot set a constant field."); }
        @Override public Object GetRawConstantValue() {
            if (this.owner.definition == NumberStyles.class || this.owner.definition == DateTimeStyles.class || this.owner.definition == TimeSpanStyles.class || this.owner.definition == MethodImplAttributes.class || this.owner.definition == FieldAttributes.class || this.owner.definition == BindingFlags.class || this.owner.definition == MemberTypes.class) return new Int32(this.enumConstant());
            boolean max = this.name.equals("MaxValue");
            if (this.owner.definition == Int32.class) return new Int32(max ? Integer.MAX_VALUE : Integer.MIN_VALUE);
            if (this.owner.definition == Byte.class) return new Byte(max ? 255 : 0);
            if (this.owner.definition == SByte.class) return new SByte(max ? 127 : -128);
            if (this.owner.definition == UInt16.class) return new UInt16(max ? 65535 : 0);
            return new UInt32(max ? 4294967295L : 0L);
        }
        @Override public String ToString() { return ((this.owner.definition == NumberStyles.class || this.owner.definition == DateTimeStyles.class || this.owner.definition == TimeSpanStyles.class || this.owner.definition == MethodImplAttributes.class || this.owner.definition == FieldAttributes.class || this.owner.definition == BindingFlags.class || this.owner.definition == MemberTypes.class) ? this.owner.get_FullName() : this.owner.get_Name()) + " " + this.name; }
    }

    private static final class DefaultPropertyMember extends MemberInfo {
        @Override
        public boolean HasSameMetadataDefinitionAs(MemberInfo other) {
            if (other == null) throw new ArgumentNullException("other");
            return other instanceof DefaultPropertyMember property && this.name.equals(property.name)
                    && this.owner.HasSameMetadataDefinitionAs(property.owner);
        }

        @Override
        public boolean get_IsCollectible() { return false; }
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

    private static abstract class SignatureType extends Type {
        @Override public FieldInfo[] GetFields(BindingFlags flags) { throw unsupported(); }
        @Override public FieldInfo GetField(String name, BindingFlags flags) { throw unsupported(); }
        @Override public MemberInfo[] FindMembers(MemberTypes kind, BindingFlags flags, MemberFilter filter, Object criteria) { throw unsupported(); }
        @Override public Type[] FindInterfaces(TypeFilter filter, Object criteria) { throw unsupported(); }
        @Override public boolean get_IsNestedFamANDAssem() { throw unsupported(); }
        @Override public boolean get_IsNestedFamORAssem() { throw unsupported(); }
        protected static final Type[] EMPTY_TYPES = new Type[0];
        protected SignatureType() { super(Object.class, List.of()); }
        protected static NotSupportedException unsupported() { return new NotSupportedException("This method is not supported on signature types."); }
        @Override public boolean get_IsGenericParameter() { return false; }
        @Override public boolean get_IsGenericMethodParameter() { return false; }
        @Override public int get_GenericParameterPosition() { throw new InvalidOperationException("Method may only be called on a Type for which Type.IsGenericParameter is true."); }
        @Override public Type MakeArrayType() { return new SignatureElementType(this, 0, 1, true); }
        @Override public Type MakeArrayType(int rank) {
            if (rank <= 0) throw new IndexOutOfRangeException();
            return new SignatureElementType(this, 0, rank, false);
        }
        @Override public Type MakePointerType() { return new SignatureElementType(this, 1, 0, false); }
        @Override public Type MakeByRefType() { return new SignatureElementType(this, 2, 0, false); }
        @Override public boolean get_IsSignatureType() { return true; }
        @Override public boolean get_IsGenericTypeParameter() { return false; }
        @Override public boolean get_ContainsGenericParameters() { return true; }
        @Override public boolean get_IsGenericType() { return false; }
        @Override public boolean get_IsGenericTypeDefinition() { return false; }
        @Override public boolean get_IsConstructedGenericType() { return false; }
        @Override public boolean get_IsTypeDefinition() { return false; }
        @Override public boolean get_HasElementType() { return false; }
        @Override public boolean get_IsArray() { return false; }
        @Override public boolean get_IsSZArray() { return false; }
        @Override public boolean get_IsVariableBoundArray() { return false; }
        @Override public boolean get_IsPointer() { return false; }
        @Override public boolean get_IsByRef() { return false; }
        @Override public boolean get_IsByRefLike() { return false; }
        @Override public boolean get_IsFunctionPointer() { return false; }
        @Override public boolean get_IsUnmanagedFunctionPointer() { return false; }
        @Override public boolean get_IsCollectible() { return true; }
        @Override public boolean get_IsEnum() { throw unsupported(); }
        @Override public boolean get_IsValueType() { throw unsupported(); }
        @Override public boolean get_IsPrimitive() { throw unsupported(); }
        @Override public boolean get_IsClass() { throw unsupported(); }
        @Override public boolean get_IsInterface() { throw unsupported(); }
        @Override public boolean get_IsAbstract() { throw unsupported(); }
        @Override public boolean get_IsSealed() { throw unsupported(); }
        @Override public boolean get_IsPublic() { throw unsupported(); }
        @Override public boolean get_IsNotPublic() { throw unsupported(); }
        @Override public boolean get_IsNested() { throw unsupported(); }
        @Override public boolean get_IsNestedPublic() { throw unsupported(); }
        @Override public boolean get_IsNestedPrivate() { throw unsupported(); }
        @Override public boolean get_IsNestedAssembly() { throw unsupported(); }
        @Override public boolean get_IsNestedFamily() { throw unsupported(); }
        @Override public boolean get_IsVisible() { return true; }
        @Override public boolean get_IsSerializable() { throw unsupported(); }
        @Override public boolean get_IsSpecialName() { throw unsupported(); }
        @Override public boolean get_IsAnsiClass() { throw unsupported(); }
        @Override public boolean get_IsUnicodeClass() { throw unsupported(); }
        @Override public boolean get_IsAutoClass() { throw unsupported(); }
        @Override public boolean get_IsAutoLayout() { throw unsupported(); }
        @Override public boolean get_IsLayoutSequential() { throw unsupported(); }
        @Override public boolean get_IsExplicitLayout() { throw unsupported(); }
        @Override public boolean get_IsImport() { throw unsupported(); }
        @Override public boolean get_IsCOMObject() { throw unsupported(); }
        @Override public boolean get_IsContextful() { throw unsupported(); }
        @Override public boolean get_IsMarshalByRef() { throw unsupported(); }
        @Override public boolean get_IsSecurityCritical() { throw unsupported(); }
        @Override public boolean get_IsSecuritySafeCritical() { throw unsupported(); }
        @Override public boolean get_IsSecurityTransparent() { throw unsupported(); }
        @Override public String get_Namespace() { return null; }
        @Override public String get_FullName() { return null; }
        @Override public String get_AssemblyQualifiedName() { return null; }
        @Override public Type get_BaseType() { throw unsupported(); }
        @Override public Type get_DeclaringType() { throw unsupported(); }
        @Override public Type get_ReflectedType() { throw unsupported(); }
        @Override public Type get_UnderlyingSystemType() { return this; }
        @Override public MemberTypes get_MemberType() { return MemberTypes.TypeInfo; }
        @Override public GenericParameterAttributes get_GenericParameterAttributes() { throw unsupported(); }
        @Override public Type[] get_GenericTypeArguments() { return EMPTY_TYPES; }
        @Override public Type[] GetGenericArguments() { return EMPTY_TYPES; }
        @Override public Type GetGenericTypeDefinition() { throw new InvalidOperationException("This operation is only valid on generic types."); }
        @Override public int GetArrayRank() { throw new ArgumentException("Must be an array type."); }
        @Override public Type GetElementType() { return null; }
        @Override public Type[] GetFunctionPointerParameterTypes() { throw new NotSupportedException(); }
        @Override public Type[] GetFunctionPointerCallingConventions() { throw new NotSupportedException(); }
        @Override public Type GetFunctionPointerReturnType() { throw new NotSupportedException(); }
        @Override public Type[] GetGenericParameterConstraints() { throw unsupported(); }
        @Override public Type[] GetInterfaces() { throw unsupported(); }
        @Override public boolean IsAssignableFrom(Type other) { throw unsupported(); }
        @Override public boolean IsInstanceOfType(Object value) { throw unsupported(); }
        @Override public boolean IsEquivalentTo(Type other) { throw unsupported(); }
        @Override public boolean IsSubclassOf(Type other) { throw unsupported(); }
        @Override public boolean HasSameMetadataDefinitionAs(MemberInfo other) { throw unsupported(); }
        @Override public Type MakeGenericType(Type[] arguments) { throw unsupported(); }
        @Override public MemberInfo[] GetDefaultMembers() { throw unsupported(); }
        @Override public MethodInfo[] GetMethods(BindingFlags flags) { throw unsupported(); }
        @Override public MemberInfo[] GetMembers(BindingFlags flags) { throw unsupported(); }
        @Override public MemberInfo[] GetMember(String name) { throw unsupported(); }
        @Override public MemberInfo[] GetMember(String name, BindingFlags flags) { throw unsupported(); }
        @Override public MemberInfo[] GetMember(String name, MemberTypes kind, BindingFlags flags) { throw unsupported(); }
        @Override public Type GetNestedType(String name) { throw unsupported(); }
        @Override public Type GetNestedType(String name, BindingFlags flags) { throw unsupported(); }
        @Override public Type[] GetNestedTypes(BindingFlags flags) { throw unsupported(); }
        @Override public Type GetInterface(String name) { throw unsupported(); }
        @Override public Type GetInterface(String name, boolean ignoreCase) { throw unsupported(); }
        @Override public String[] GetEnumNames() { throw unsupported(); }
        @Override public Object[] GetEnumValues() { throw unsupported(); }
        @Override public int[] GetEnumValuesAsUnderlyingType() { throw unsupported(); }
        @Override public Type GetEnumUnderlyingType() { throw unsupported(); }
        @Override public String GetEnumName(Object value) { throw unsupported(); }
        @Override public boolean IsEnumDefined(Object value) { throw unsupported(); }
        @Override public MethodInfo GetMethod(String name) { if (name == null) throw new ArgumentNullException("name"); throw unsupported(); }
        @Override public MethodInfo GetMethod(String name, BindingFlags flags) { if (name == null) throw new ArgumentNullException("name"); throw unsupported(); }
        @Override public MethodInfo GetMethod(String name, Type[] types) { if (name == null) throw new ArgumentNullException("name"); if (types == null) throw new ArgumentNullException("types"); for (Type type : types) if (type == null) throw new ArgumentNullException("types"); throw unsupported(); }
        @Override public MethodInfo GetMethod(String name, BindingFlags flags, Type[] types) { if (name == null) throw new ArgumentNullException("name"); if (types == null) throw new ArgumentNullException("types"); for (Type type : types) if (type == null) throw new ArgumentNullException("types"); throw unsupported(); }
    }

    private static final class SignatureMethodParameter extends SignatureType {
        private final int position;
        private SignatureMethodParameter(int position) { this.position = position; }
        @Override public String get_Name() { return "!!" + this.position; }
        @Override public int get_GenericParameterPosition() { return this.position; }
        @Override public boolean get_IsGenericParameter() { return true; }
        @Override public boolean get_IsGenericMethodParameter() { return true; }
        @Override public String ToString() { return this.get_Name(); }
    }

    private static final class SignatureConstructedType extends SignatureType {
        private final Type genericDefinition;
        private final Type[] genericArguments;
        private SignatureConstructedType(Type genericDefinition, Type[] arguments) {
            this.genericDefinition = genericDefinition;
            this.genericArguments = arguments.clone();
            for (Type argument : this.genericArguments) {
                if (argument == null) throw new ArgumentNullException("typeArguments");
            }
        }
        @Override public String get_Name() { return this.genericDefinition.get_Name(); }
        @Override public String get_Namespace() { return this.genericDefinition.get_Namespace(); }
        @Override public boolean get_IsGenericType() { return true; }
        @Override public boolean get_IsConstructedGenericType() { return true; }
        @Override public boolean get_IsByRefLike() { return this.genericDefinition.get_IsByRefLike(); }
        @Override public boolean get_IsEnum() { return this.genericDefinition.get_IsEnum(); }
        @Override public boolean get_IsValueType() { return this.genericDefinition.get_IsValueType(); }
        @Override public boolean get_IsVisible() { throw unsupported(); }
        @Override public boolean get_ContainsGenericParameters() {
            for (Type argument : this.genericArguments) if (argument.get_ContainsGenericParameters()) return true;
            return false;
        }
        @Override public Type GetGenericTypeDefinition() { return this.genericDefinition; }
        @Override public Type[] GetGenericArguments() { return this.genericArguments.clone(); }
        @Override public Type[] get_GenericTypeArguments() { return this.genericArguments.clone(); }
        @Override public String ToString() {
            StringBuilder text = new StringBuilder(this.genericDefinition.ToString()).append('[');
            for (int index = 0; index < this.genericArguments.length; index++) {
                if (index > 0) text.append(',');
                text.append(this.genericArguments[index].ToString());
            }
            return text.append(']').toString();
        }
    }

    private static final class SignatureElementType extends SignatureType {
        private final SignatureType element;
        private final int kind;
        private final int rank;
        private final boolean vector;
        private SignatureElementType(SignatureType element, int kind, int rank, boolean vector) {
            this.element = element; this.kind = kind; this.rank = rank; this.vector = vector;
        }
        private String suffix() { return this.kind == 0 ? arraySuffix(this.rank, this.vector) : this.kind == 1 ? "*" : "&"; }
        @Override public boolean get_IsVisible() { return this.element.get_IsVisible(); }
        @Override public String get_Name() { return this.element.get_Name() + this.suffix(); }
        @Override public String get_Namespace() { return this.element.get_Namespace(); }
        @Override public String ToString() { return this.element.ToString() + this.suffix(); }
        @Override public boolean get_HasElementType() { return true; }
        @Override public boolean get_IsArray() { return this.kind == 0; }
        @Override public boolean get_IsSZArray() { return this.kind == 0 && this.vector; }
        @Override public boolean get_IsVariableBoundArray() { return this.kind == 0 && !this.vector; }
        @Override public boolean get_IsPointer() { return this.kind == 1; }
        @Override public boolean get_IsByRef() { return this.kind == 2; }
        @Override public boolean get_IsEnum() { return false; }
        @Override public boolean get_IsValueType() { return false; }
        @Override public boolean get_ContainsGenericParameters() { return this.element.get_ContainsGenericParameters(); }
        @Override public Type GetElementType() { return this.element; }
        @Override public int GetArrayRank() { if (this.kind == 0) return this.rank; throw new ArgumentException("Must be an array type."); }
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
