package System;

import java.util.List;
import java.util.Map;
import System.Reflection.MemberTypes;
import System.Reflection.BindingFlags;
import System.Reflection.CallingConventions;
import System.Reflection.MemberInfo;
import System.Reflection.MethodBase;
import System.Reflection.MethodInfo;
import System.Reflection.ParameterInfo;
import System.Reflection.GenericParameterAttributes;
import System.Globalization.NumberStyles;

/** Exercises selected Type identity and null boundaries against the candidate implementation. */
public final class TypeIdentityCandidateTest {
    static final class NestedAssemblyFixture {
    }

    private static final class NestedPrivateFixture {
    }

    protected static final class NestedFamilyFixture {
    }

    private static final class PrivateOwnerFixture {
        public static final class PublicChild {
        }

        private static final class PrivateChild {
        }
    }

    public static void main(String[] args) {
        Type list = Type.fromJavaClass(List.class);
        Type string = Type.fromJavaClass(String.class);
        Type integer = Type.fromJavaClass(Integer.class);
        Type bindingFlagsType = Type.fromJavaClass(BindingFlags.class);
        Type callingConventionType = Type.fromJavaClass(CallingConventions.class);
        CallingConventions standardInstance = CallingConventions.Standard.or(CallingConventions.HasThis);
        if (Type.GetType("System.Reflection.CallingConventions") != callingConventionType
                || !callingConventionType.get_IsEnum()
                || callingConventionType.GetEnumValues().getClass() != CallingConventions[].class
                || callingConventionType.GetEnumNames().length != 5
                || standardInstance.get_Value() != 33
                || !standardInstance.has(CallingConventions.Standard)
                || !standardInstance.has(CallingConventions.HasThis)
                || callingConventionType.IsEnumDefined(standardInstance)
                || callingConventionType.GetEnumName(standardInstance) != null) {
            throw new AssertionError("Pinned calling-convention values changed");
        }
        int[] bindingValues = bindingFlagsType.GetEnumValuesAsUnderlyingType();
        if (Type.GetType("System.Reflection.BindingFlags") != bindingFlagsType
                || !bindingFlagsType.get_IsEnum() || !bindingFlagsType.get_IsValueType()
                || bindingValues.length != 21 || bindingValues[0] != 0
                || bindingValues[6] != 32 || bindingValues[20] != 33554432
                || !"BindingFlags".equals(bindingFlagsType.get_Name())
                || !"System.Reflection.BindingFlags".equals(bindingFlagsType.get_FullName())
                || !"DoNotWrapExceptions".equals(bindingFlagsType.GetEnumNames()[20])) {
            throw new AssertionError("Pinned BindingFlags identity or values changed");
        }
        BindingFlags publicInstance = BindingFlags.Public.or(BindingFlags.Instance);
        Type methodBaseType = Type.fromJavaClass(MethodBase.class);
        Type methodInfoType = Type.fromJavaClass(MethodInfo.class);
        Type parameterInfoType = Type.fromJavaClass(ParameterInfo.class);
        if (Type.GetType("System.Reflection.ParameterInfo") != parameterInfoType
                || parameterInfoType.get_BaseType() != Type.fromJavaClass(Object.class)
                || parameterInfoType.get_IsAbstract()) {
            throw new AssertionError("Selected ParameterInfo identity changed");
        }
        Type voidType = Type.fromJavaClass(Void.class);
        if (Type.GetType("System.Void") != voidType
                || !"System.Void".equals(voidType.get_FullName())
                || voidType.get_BaseType() != Type.fromJavaClass(Number.class)
                || !voidType.get_IsValueType() || !voidType.get_IsPrimitive()) {
            throw new AssertionError("Pinned Void return Type identity changed");
        }
        if (Type.GetType("System.Reflection.MethodBase") != methodBaseType
                || Type.GetType("System.Reflection.MethodInfo") != methodInfoType
                || methodBaseType.get_BaseType() != Type.fromJavaClass(MemberInfo.class)
                || methodInfoType.get_BaseType() != methodBaseType
                || !methodBaseType.get_IsAbstract() || !methodInfoType.get_IsAbstract()) {
            throw new AssertionError("Selected method descriptor hierarchy changed");
        }
        MemberTypes methodProperty = MemberTypes.Method.or(MemberTypes.Property);
        Type memberTypesType = Type.fromJavaClass(MemberTypes.class);
        if (methodProperty.get_Value() != 24 || !methodProperty.has(MemberTypes.Method)
                || !methodProperty.has(MemberTypes.Property)
                || methodProperty.has(MemberTypes.Field)
                || memberTypesType.IsEnumDefined(methodProperty)
                || memberTypesType.GetEnumName(methodProperty) != null
                || memberTypesType.GetEnumValues().getClass() != MemberTypes[].class
                || MemberTypes.All.has(methodProperty) == false) {
            throw new AssertionError("Pinned MemberTypes combination changed");
        }
        if (publicInstance.get_Value() != 20 || !publicInstance.has(BindingFlags.Public)
                || !publicInstance.has(BindingFlags.Instance)
                || publicInstance.has(BindingFlags.NonPublic)
                || bindingFlagsType.IsEnumDefined(publicInstance)
                || bindingFlagsType.GetEnumName(publicInstance) != null
                || bindingFlagsType.GetEnumValues().getClass() != BindingFlags[].class
                || BindingFlags.Default.or(BindingFlags.Public) != BindingFlags.Public) {
            throw new AssertionError("Pinned BindingFlags composition changed");
        }
        if (Type.fromJavaClass(Object.class).GetDefaultMembers().length != 0
                || Type.fromJavaClass(IDisposable.class).GetDefaultMembers().length != 0
                || Type.fromJavaClass(TypeCode.class).GetDefaultMembers().length != 0) {
            throw new AssertionError("Selected empty default-member queries changed");
        }
        Type closedList = Type.fromJavaClass(List.class)
                .MakeGenericType(new Type[] {string});
        Type[] interfaceOwners = {Type.fromJavaClass(IDisposable.class),
                Type.fromJavaClass(IComparable.class),
                Type.fromJavaClass(IFormattable.class),
                Type.fromJavaClass(IFormatProvider.class)};
        String[] interfaceMethodNames = {"Dispose", "CompareTo", "ToString", "GetFormat"};
        Type[] interfaceMethodReturns = {voidType, integer, string,
                Type.fromJavaClass(Object.class)};
        Type[][] interfaceMethodParameters = {
            new Type[0], {Type.fromJavaClass(Object.class)},
            {string, Type.fromJavaClass(IFormatProvider.class)},
            {Type.fromJavaClass(Type.class)}
        };
        String[][] interfaceParameterNames = {
            {}, {"obj"}, {"format", "formatProvider"}, {"formatType"}
        };
        for (int index = 0; index < interfaceOwners.length; index++) {
            Type owner = interfaceOwners[index];
            MemberInfo[] members = owner.GetMembers();
            if (members.length != 1
                    || !interfaceMethodNames[index].equals(members[0].get_Name())
                    || members[0].get_MemberType() != MemberTypes.Method
                    || members[0].get_DeclaringType() != owner
                    || members[0].get_ReflectedType() != owner
                    || owner.GetMember(interfaceMethodNames[index]).length != 1
                    || members == owner.GetMembers()) {
                throw new AssertionError("Selected interface member inventory changed");
            }
            if (owner.GetMember(interfaceMethodNames[index]
                    .toLowerCase(java.util.Locale.ROOT)).length != 0
                    || owner.GetMember("Missing").length != 0) {
                throw new AssertionError("Interface member case-sensitive miss changed");
            }
            if (owner.GetMembers(publicInstance).length != 1
                    || !interfaceMethodNames[index].equals(owner.GetMembers(publicInstance)[0].get_Name())
                    || owner.GetMembers(BindingFlags.Public).length != 0
                    || owner.GetMembers(BindingFlags.NonPublic.or(BindingFlags.Instance)).length != 0
                    || owner.GetMembers(publicInstance) == owner.GetMembers(publicInstance)) {
                throw new AssertionError("Selected flagged interface member inventory changed");
            }
            MethodInfo[] methods = owner.GetMethods(publicInstance);
            if (methods.length != 1
                    || !interfaceMethodNames[index].equals(methods[0].get_Name())
                    || methods[0].get_MemberType() != MemberTypes.Method
                    || methods[0].get_DeclaringType() != owner
                    || owner.GetMethods(BindingFlags.Public).length != 0
                    || owner.GetMethods(BindingFlags.NonPublic.or(BindingFlags.Instance)).length != 0) {
                throw new AssertionError("Selected flagged interface method inventory changed");
            }
            MethodInfo[] defaultMethods = owner.GetMethods();
            if (defaultMethods.length != 1
                    || !interfaceMethodNames[index].equals(defaultMethods[0].get_Name())
                    || defaultMethods[0].get_MemberType() != MemberTypes.Method
                    || defaultMethods[0].get_DeclaringType() != owner
                    || defaultMethods == owner.GetMethods()) {
                throw new AssertionError("Selected default interface method inventory changed");
            }
            MethodInfo namedMethod = owner.GetMethod(interfaceMethodNames[index]);
            if (namedMethod == null
                    || !interfaceMethodNames[index].equals(namedMethod.get_Name())
                    || namedMethod.get_MemberType() != MemberTypes.Method
                    || namedMethod.get_DeclaringType() != owner
                    || !namedMethod.get_IsPublic() || namedMethod.get_IsStatic()
                    || !namedMethod.get_IsAbstract() || !namedMethod.get_IsVirtual()
                    || namedMethod.get_IsFinal()
                    || namedMethod.get_IsSpecialName()
                    || namedMethod.get_IsConstructor()
                    || namedMethod.get_IsPrivate()
                    || namedMethod.get_IsFamily()
                    || namedMethod.get_IsAssembly()
                    || !namedMethod.get_IsHideBySig()
                    || !namedMethod.get_CallingConvention().equals(standardInstance)
                    || !namedMethod.get_IsSecurityCritical()
                    || namedMethod.get_IsSecuritySafeCritical()
                    || namedMethod.get_IsSecurityTransparent()
                    || namedMethod.get_IsGenericMethod()
                    || namedMethod.get_IsGenericMethodDefinition()
                    || namedMethod.get_ContainsGenericParameters()
                    || namedMethod.GetGenericArguments().length != 0
                    || namedMethod.GetBaseDefinition() != namedMethod
                    || namedMethod.get_ReturnType() != interfaceMethodReturns[index]
                    || owner.GetMethod(interfaceMethodNames[index]
                        .toLowerCase(java.util.Locale.ROOT)) != null
                    || owner.GetMethod("Missing") != null) {
                throw new AssertionError("Selected typed method-name lookup changed");
            }
            ParameterInfo returnParameter = namedMethod.get_ReturnParameter();
            if (returnParameter.get_ParameterType() != interfaceMethodReturns[index]
                    || returnParameter.get_Position() != -1
                    || returnParameter.get_IsOptional()
                    || returnParameter.get_HasDefaultValue()
                    || returnParameter.GetOptionalCustomModifiers().length != 0
                    || returnParameter.GetRequiredCustomModifiers().length != 0
                    || !java.util.Objects.equals(returnParameter.get_Name(),
                        index == 2 ? "" : null)
                    || returnParameter == namedMethod.get_ReturnParameter()) {
                throw new AssertionError("Selected return parameter metadata changed");
            }
            ParameterInfo[] parameters = namedMethod.GetParameters();
            if (parameters.length != interfaceMethodParameters[index].length
                    || parameters == namedMethod.GetParameters()) {
                throw new AssertionError("Selected method parameter inventory changed");
            }
            for (int parameterIndex = 0; parameterIndex < parameters.length; parameterIndex++) {
                if (!interfaceParameterNames[index][parameterIndex]
                        .equals(parameters[parameterIndex].get_Name())
                        || parameters[parameterIndex].get_ParameterType()
                            != interfaceMethodParameters[index][parameterIndex]
                        || parameters[parameterIndex].get_Position() != parameterIndex) {
                    throw new AssertionError("Selected method parameter metadata changed");
                }
                if (parameters[parameterIndex].get_IsOptional()
                        || parameters[parameterIndex].get_HasDefaultValue()
                        || parameters[parameterIndex].GetOptionalCustomModifiers().length != 0
                        || parameters[parameterIndex].GetRequiredCustomModifiers().length != 0) {
                    throw new AssertionError("Selected parameter default flags changed");
                }
            }
            if (!interfaceMethodNames[index].equals(
                    owner.GetMethod(interfaceMethodNames[index], publicInstance).get_Name())
                    || owner.GetMethod(interfaceMethodNames[index], BindingFlags.Public) != null
                    || owner.GetMethod(interfaceMethodNames[index],
                        BindingFlags.NonPublic.or(BindingFlags.Instance)) != null
                    || owner.GetMethod("Missing", publicInstance) != null
                    || !interfaceMethodNames[index].equals(owner.GetMethod(
                        interfaceMethodNames[index].toLowerCase(java.util.Locale.ROOT),
                        publicInstance.or(BindingFlags.IgnoreCase)).get_Name())) {
                throw new AssertionError("Selected flagged typed method lookup changed");
            }
            MethodInfo parameterized = owner.GetMethod(
                    interfaceMethodNames[index], interfaceMethodParameters[index]);
            if (parameterized == null
                    || !interfaceMethodNames[index].equals(parameterized.get_Name())
                    || parameterized.get_DeclaringType() != owner
                    || owner.GetMethod(interfaceMethodNames[index],
                        new Type[] {Type.fromJavaClass(Integer.class)}) != null) {
                throw new AssertionError("Selected method parameter lookup changed");
            }
            if (owner.GetMethod(interfaceMethodNames[index], publicInstance,
                    interfaceMethodParameters[index]) == null
                    || owner.GetMethod(interfaceMethodNames[index], BindingFlags.Public,
                        interfaceMethodParameters[index]) != null
                    || owner.GetMethod(interfaceMethodNames[index], publicInstance,
                        new Type[] {Type.fromJavaClass(Integer.class)}) != null
                    || owner.GetMethod(interfaceMethodNames[index]
                        .toLowerCase(java.util.Locale.ROOT),
                        publicInstance.or(BindingFlags.IgnoreCase),
                        interfaceMethodParameters[index]) == null) {
                throw new AssertionError("Selected flagged method parameter lookup changed");
            }
        }
        for (int index = 0; index < 3; index++) {
            try {
                if (index == 0) {
                    interfaceOwners[0].GetMethod(null, new Type[0]);
                } else if (index == 1) {
                    interfaceOwners[0].GetMethod("Dispose", (Type[]) null);
                } else {
                    interfaceOwners[0].GetMethod("Dispose", new Type[] {null});
                }
                throw new AssertionError("Null method lookup input accepted");
            } catch (ArgumentNullException expected) {
                String expectedName = index == 0 ? "name" : "types";
                if (!expectedName.equals(expected.get_ParamName())) {
                    throw new AssertionError("Null method lookup parameter changed", expected);
                }
            }
        }
        try {
            interfaceOwners[0].GetMethod("Dispose", publicInstance, (Type[]) null);
            throw new AssertionError("Null flagged method parameter array accepted");
        } catch (ArgumentNullException expected) {
            if (!"types".equals(expected.get_ParamName())) {
                throw new AssertionError("Null flagged method parameter name changed", expected);
            }
        }
        try {
            interfaceOwners[0].GetMethod(null);
            throw new AssertionError("Null typed method name accepted");
        } catch (ArgumentNullException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Null typed method name parameter changed", expected);
            }
        }
        try {
            interfaceOwners[0].GetMethod(null, publicInstance);
            throw new AssertionError("Null flagged typed method name accepted");
        } catch (ArgumentNullException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Null flagged typed method name parameter changed", expected);
            }
        }
        if (string.GetMember("Chars").length != 1
                || !"Chars".equals(string.GetMember("Chars")[0].get_Name())
                || string.GetMember("Chars")[0].get_MemberType() != MemberTypes.Property
                || string.GetMember("chars").length != 0
                || string.GetMember("Missing").length != 0
                || Type.fromJavaClass(List.class).GetMember("Item").length != 1
                || Type.fromJavaClass(Object.class).GetMember("Missing").length != 0) {
            throw new AssertionError("Selected member name lookup changed");
        }
        BindingFlags publicInstanceIgnoreCase = publicInstance.or(BindingFlags.IgnoreCase);
        if (string.GetMember("Chars", MemberTypes.Property, publicInstance).length != 1
                || string.GetMember("Chars", MemberTypes.Method, publicInstance).length != 0
                || string.GetMember("Chars", MemberTypes.All, publicInstance).length != 1
                || string.GetMember("Chars", methodProperty, publicInstance).length != 1
                || interfaceOwners[0].GetMember("Dispose", MemberTypes.Method, publicInstance).length != 1
                || interfaceOwners[0].GetMember("Dispose", methodProperty, publicInstance).length != 1
                || interfaceOwners[0].GetMember("Dispose", MemberTypes.Property, publicInstance).length != 0) {
            throw new AssertionError("Selected member-kind filtered lookup changed");
        }
        try {
            string.GetMember(null, MemberTypes.Property, publicInstance);
            throw new AssertionError("Null kind-filtered member name accepted");
        } catch (ArgumentNullException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Null kind-filtered member name parameter changed", expected);
            }
        }
        if (string.GetMember("Chars", publicInstance).length != 1
                || string.GetMember("Chars", publicInstance)[0].get_MemberType() != MemberTypes.Property
                || string.GetMember("Chars", BindingFlags.Public).length != 0
                || string.GetMember("Chars", BindingFlags.Instance).length != 0
                || string.GetMember("Chars", BindingFlags.NonPublic.or(BindingFlags.Instance)).length != 0
                || string.GetMember("chars", publicInstance).length != 0
                || !"Chars".equals(string.GetMember("chars", publicInstanceIgnoreCase)[0].get_Name())
                || !"Dispose".equals(interfaceOwners[0].GetMember("Dispose", publicInstance)[0].get_Name())) {
            throw new AssertionError("Selected flagged member lookup changed");
        }
        try {
            string.GetMember(null, publicInstance);
            throw new AssertionError("Null flagged member name accepted");
        } catch (ArgumentNullException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Null flagged member name parameter changed", expected);
            }
        }
        try {
            string.GetMember(null);
            throw new AssertionError("Null member name accepted");
        } catch (ArgumentNullException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Null member name parameter changed", expected);
            }
        }
        for (Type defaultOwner : new Type[] {string, Type.fromJavaClass(List.class),
                closedList}) {
            MemberInfo[] defaults = defaultOwner.GetDefaultMembers();
            String expectedName = defaultOwner == string ? "Chars" : "Item";
            if (defaults.length != 1 || !expectedName.equals(defaults[0].get_Name())
                    || defaults[0].get_MemberType() != MemberTypes.Property
                    || defaults[0].get_DeclaringType() != defaultOwner
                    || defaults[0].get_ReflectedType() != defaultOwner
                    || defaults == defaultOwner.GetDefaultMembers()) {
                throw new AssertionError("Selected default property member changed");
            }
        }
        for (Type modifierType : new Type[] {string, integer,
                Type.fromJavaClass(List.class),
                Type.fromJavaClass(List.class).GetGenericArguments()[0],
                string.MakeArrayType(), string.MakeByRefType(),
                string.MakePointerType()}) {
            if (modifierType.GetOptionalCustomModifiers().length != 0
                    || modifierType.GetRequiredCustomModifiers().length != 0
                    || modifierType.GetOptionalCustomModifiers()
                            == modifierType.GetOptionalCustomModifiers()) {
                throw new AssertionError("Selected Type custom modifiers changed");
            }
        }
        Type[] characterSetTypes = {string, integer, Type.fromJavaClass(TypeCode.class),
                Type.fromJavaClass(IDisposable.class), Type.fromJavaClass(List.class),
                Type.fromJavaClass(List.class).MakeGenericType(new Type[] {string}),
                Type.fromJavaClass(List.class).GetGenericArguments()[0],
                string.MakeArrayType(), string.MakeByRefType(),
                Type.fromJavaClass(Map.Entry.class)};
        for (Type characterSetType : characterSetTypes) {
            if (!characterSetType.get_IsAnsiClass()
                    || characterSetType.get_IsUnicodeClass()
                    || characterSetType.get_IsAutoClass()) {
                throw new AssertionError("Selected Type character-set flags changed");
            }
        }
        for (Type layoutType : characterSetTypes) {
            boolean sequential = layoutType == integer;
            if (layoutType.get_IsAutoLayout() == sequential
                    || layoutType.get_IsLayoutSequential() != sequential
                    || layoutType.get_IsExplicitLayout()) {
                throw new AssertionError("Selected Type layout flags changed");
            }
        }
        for (Type interopType : new Type[] {string, integer,
                Type.fromJavaClass(Type.class), Type.fromJavaClass(Exception.class),
                Type.fromJavaClass(IDisposable.class), Type.fromJavaClass(List.class),
                Type.fromJavaClass(List.class).GetGenericArguments()[0],
                string.MakeArrayType(), string.MakeByRefType()}) {
            if (interopType.get_IsImport() || interopType.get_IsCOMObject()
                    || interopType.get_IsContextful() || interopType.get_IsMarshalByRef()
                    || interopType.get_IsSignatureType()) {
                throw new AssertionError("Selected Type interop flags changed");
            }
        }
        for (Type pointerKind : new Type[] {string, integer,
                Type.fromJavaClass(TypeCode.class), Type.fromJavaClass(IDisposable.class),
                Type.fromJavaClass(List.class),
                Type.fromJavaClass(List.class).GetGenericArguments()[0],
                string.MakeArrayType(), string.MakePointerType()}) {
            if (pointerKind.get_IsFunctionPointer()
                    || pointerKind.get_IsUnmanagedFunctionPointer()) {
                throw new AssertionError("Selected function-pointer flags changed");
            }
        }
        for (Type nonFunctionPointer : new Type[] {string, string.MakePointerType()}) {
            for (Runnable query : new Runnable[] {
                    () -> nonFunctionPointer.GetFunctionPointerReturnType(),
                    () -> nonFunctionPointer.GetFunctionPointerParameterTypes(),
                    () -> nonFunctionPointer.GetFunctionPointerCallingConventions()}) {
                try {
                    query.run();
                    throw new AssertionError("Non-function-pointer query was accepted");
                } catch (InvalidOperationException expected) {
                    // Matches the pinned CLR exception type.
                }
            }
        }
        for (Type securityType : new Type[] {string, integer,
                Type.fromJavaClass(TypeCode.class), Type.fromJavaClass(IDisposable.class),
                Type.fromJavaClass(Type.class), Type.fromJavaClass(Exception.class),
                Type.fromJavaClass(List.class),
                Type.fromJavaClass(List.class).GetGenericArguments()[0],
                string.MakeArrayType(), string.MakeByRefType()}) {
            if (!securityType.get_IsSecurityCritical()
                    || securityType.get_IsSecuritySafeCritical()
                    || securityType.get_IsSecurityTransparent()) {
                throw new AssertionError("Selected Type security transparency flags changed");
            }
        }
        if (string.get_IsSpecialName()
                || Type.fromJavaClass(TypeCode.class).get_IsSpecialName()
                || Type.fromJavaClass(List.class).get_IsSpecialName()
                || Type.fromJavaClass(List.class).GetGenericArguments()[0].get_IsSpecialName()
                || string.MakeArrayType().get_IsSpecialName()
                || string.MakeByRefType().get_IsSpecialName()
                || Type.fromJavaClass(Map.Entry.class).get_IsSpecialName()) {
            throw new AssertionError("Selected Type special-name flag changed");
        }
        if (!string.get_IsSerializable() || !integer.get_IsSerializable()
                || !Type.fromJavaClass(TypeCode.class).get_IsSerializable()
                || !Type.fromJavaClass(Exception.class).get_IsSerializable()
                || !Type.fromJavaClass(List.class).get_IsSerializable()
                || !Type.fromJavaClass(List.class)
                        .MakeGenericType(new Type[] {string}).get_IsSerializable()
                || !string.MakeArrayType().get_IsSerializable()
                || !Type.fromJavaClass(IDisposable.class).MakeArrayType()
                        .get_IsSerializable()
                || Type.fromJavaClass(IDisposable.class).get_IsSerializable()
                || Type.fromJavaClass(Type.class).get_IsSerializable()
                || Type.fromJavaClass(List.class).GetGenericArguments()[0]
                        .get_IsSerializable()
                || string.MakeByRefType().get_IsSerializable()) {
            throw new AssertionError("Selected Type serializable flag changed");
        }
        if (string.get_MemberType() != MemberTypes.TypeInfo
                || string.MakeArrayType().get_MemberType() != MemberTypes.TypeInfo
                || string.MakeByRefType().get_MemberType() != MemberTypes.TypeInfo
                || string.MakePointerType().get_MemberType() != MemberTypes.TypeInfo
                || Type.fromJavaClass(List.class).GetGenericArguments()[0]
                        .get_MemberType() != MemberTypes.TypeInfo) {
            throw new AssertionError("Selected Type member kind changed");
        }
        Type packagePrivate = Type.fromJavaClass(PackagePrivateTypeFixture.class);
        if (!packagePrivate.get_IsNotPublic() || packagePrivate.get_IsPublic()
                || string.get_IsNotPublic()
                || Type.fromJavaClass(NestedPrivateFixture.class).get_IsNotPublic()
                || string.MakeArrayType().get_IsNotPublic()
                || Type.fromJavaClass(List.class).GetGenericArguments()[0].get_IsNotPublic()) {
            throw new AssertionError("Selected top-level nonpublic Type flag changed");
        }
        Type typeCodeEnum = Type.fromJavaClass(TypeCode.class);
        Type memberTypesEnum = Type.fromJavaClass(MemberTypes.class);
        if (typeCodeEnum.GetEnumUnderlyingType() != integer
                || memberTypesEnum.GetEnumUnderlyingType() != integer) {
            throw new AssertionError("Selected enum underlying Type identity changed");
        }
        try {
            integer.GetEnumUnderlyingType();
            throw new AssertionError("Non-enum underlying Type accepted");
        } catch (ArgumentException expected) {
            if (!"enumType".equals(expected.get_ParamName())) {
                throw new AssertionError("Non-enum underlying Type parameter changed", expected);
            }
        }
        String[] typeCodeNames = typeCodeEnum.GetEnumNames();
        if (typeCodeNames.length != 18 || !"Empty".equals(typeCodeNames[0])
                || !"String".equals(typeCodeNames[17])
                || !java.util.Arrays.equals(memberTypesEnum.GetEnumNames(), new String[] {
                    "Constructor", "Event", "Field", "Method", "Property",
                    "TypeInfo", "Custom", "NestedType", "All"})
                || !java.util.Arrays.equals(Type.fromJavaClass(GenericParameterAttributes.class)
                        .GetEnumNames(), new String[] {"None", "Covariant", "Contravariant",
                            "VarianceMask", "ReferenceTypeConstraint",
                            "NotNullableValueTypeConstraint", "DefaultConstructorConstraint",
                            "SpecialConstraintMask", "AllowByRefLike"})
                || !java.util.Arrays.equals(Type.fromJavaClass(NumberStyles.class)
                        .GetEnumNames(), new String[] {"None", "AllowLeadingWhite",
                            "AllowTrailingWhite", "AllowLeadingSign", "Integer",
                            "AllowTrailingSign", "AllowParentheses", "AllowDecimalPoint",
                            "AllowThousands", "Number", "AllowExponent", "Float",
                            "AllowCurrencySymbol", "Currency", "Any", "AllowHexSpecifier",
                            "HexNumber", "AllowBinarySpecifier", "BinaryNumber"})) {
            throw new AssertionError("Selected enum names changed");
        }
        typeCodeNames[0] = "changed";
        if (!"Empty".equals(typeCodeEnum.GetEnumNames()[0])) {
            throw new AssertionError("Enum name array escaped by reference");
        }
        Object[] typeCodeValues = typeCodeEnum.GetEnumValues();
        if (typeCodeValues.getClass() != TypeCode[].class
                || typeCodeValues.length != 18
                || typeCodeValues[0] != TypeCode.Empty
                || typeCodeValues[17] != TypeCode.String
                || memberTypesEnum.GetEnumValues().getClass() != MemberTypes[].class
                || Type.fromJavaClass(NumberStyles.class).GetEnumValues().length != 19) {
            throw new AssertionError("Selected enum value array changed");
        }
        typeCodeValues[0] = TypeCode.Object;
        if (typeCodeEnum.GetEnumValues()[0] != TypeCode.Empty) {
            throw new AssertionError("Enum value array escaped by reference");
        }
        int[] underlyingValues = typeCodeEnum.GetEnumValuesAsUnderlyingType();
        if (underlyingValues.length != 18 || underlyingValues[0] != 0
                || underlyingValues[17] != 18
                || memberTypesEnum.GetEnumValuesAsUnderlyingType()[8] != 191
                || Type.fromJavaClass(NumberStyles.class)
                        .GetEnumValuesAsUnderlyingType()[18] != 1027) {
            throw new AssertionError("Selected enum underlying values changed");
        }
        underlyingValues[0] = -1;
        if (typeCodeEnum.GetEnumValuesAsUnderlyingType()[0] != 0) {
            throw new AssertionError("Enum underlying value array escaped by reference");
        }
        try {
            integer.GetEnumValuesAsUnderlyingType();
            throw new AssertionError("Non-enum owner accepted underlying values");
        } catch (ArgumentException expected) {
            if (!"enumType".equals(expected.get_ParamName())) {
                throw new AssertionError("Non-enum underlying parameter changed", expected);
            }
        }
        try {
            integer.GetEnumValues();
            throw new AssertionError("Non-enum owner accepted value enumeration");
        } catch (ArgumentException expected) {
            if (!"enumType".equals(expected.get_ParamName())) {
                throw new AssertionError("Non-enum value enumeration parameter changed", expected);
            }
        }
        if (!typeCodeEnum.IsEnumDefined(TypeCode.Empty)
                || !typeCodeEnum.IsEnumDefined(0)
                || !typeCodeEnum.IsEnumDefined("Empty")
                || typeCodeEnum.IsEnumDefined("empty")
                || typeCodeEnum.IsEnumDefined("Missing")
                || typeCodeEnum.IsEnumDefined(17)) {
            throw new AssertionError("Selected enum-defined membership changed");
        }
        if (!"Empty".equals(typeCodeEnum.GetEnumName(TypeCode.Empty))
                || !"Empty".equals(typeCodeEnum.GetEnumName(0))
                || !"Empty".equals(typeCodeEnum.GetEnumName(0L))
                || !"Empty".equals(typeCodeEnum.GetEnumName((byte) 0))
                || typeCodeEnum.GetEnumName(17) != null
                || memberTypesEnum.GetEnumName(TypeCode.Empty) != null) {
            throw new AssertionError("Selected enum name lookup changed");
        }
        try {
            typeCodeEnum.GetEnumName("Empty");
            throw new AssertionError("String accepted as enum name lookup value");
        } catch (ArgumentException expected) {
            if (!"value".equals(expected.get_ParamName())) {
                throw new AssertionError("Enum name lookup parameter identity changed", expected);
            }
        }
        try {
            typeCodeEnum.GetEnumName(null);
            throw new AssertionError("Null enum name lookup value accepted");
        } catch (ArgumentNullException expected) {
            if (!"value".equals(expected.get_ParamName())) {
                throw new AssertionError("Null enum name lookup parameter changed", expected);
            }
        }
        try {
            integer.GetEnumName(0);
            throw new AssertionError("Non-enum owner accepted enum name lookup");
        } catch (ArgumentException expected) {
            if (!"enumType".equals(expected.get_ParamName())) {
                throw new AssertionError("Non-enum name lookup parameter changed", expected);
            }
        }
        try {
            memberTypesEnum.IsEnumDefined(TypeCode.Empty);
            throw new AssertionError("Foreign enum value accepted");
        } catch (ArgumentException expected) {
            if (expected.get_ParamName() != null) {
                throw new AssertionError("Foreign enum parameter identity changed", expected);
            }
        }
        for (Object invalidWidth : new Object[] {0L, (byte) 0}) {
            try {
                typeCodeEnum.IsEnumDefined(invalidWidth);
                throw new AssertionError("Wrong-width enum membership value accepted");
            } catch (ArgumentException expected) {
                if (expected.get_ParamName() != null) {
                    throw new AssertionError("Wrong-width enum parameter changed", expected);
                }
            }
        }
        try {
            typeCodeEnum.IsEnumDefined(null);
            throw new AssertionError("Null enum value accepted");
        } catch (ArgumentNullException expected) {
            if (!"value".equals(expected.get_ParamName())) {
                throw new AssertionError("Null enum parameter identity changed", expected);
            }
        }
        try {
            integer.IsEnumDefined(0);
            throw new AssertionError("Non-enum owner accepted enum value");
        } catch (ArgumentException expected) {
            if (!"enumType".equals(expected.get_ParamName())) {
                throw new AssertionError("Non-enum owner parameter identity changed", expected);
            }
        }
        try {
            integer.GetEnumNames();
            throw new AssertionError("Non-enum GetEnumNames accepted");
        } catch (ArgumentException expected) {
            if (!"enumType".equals(expected.get_ParamName())) {
                throw new AssertionError("Non-enum parameter identity changed", expected);
            }
        }
        if (integer != Type.fromJavaClass(Int32.class) || integer != Type.fromJavaClass(int.class)
                || integer != Type.GetType("System.Int32")) {
            throw new AssertionError("Int32 public facade and primitive backend identities diverged");
        }
        Type integerArray = Type.GetType("System.Int32[]");
        Type dictionary = Type.GetType("System.Collections.Generic.Dictionary`2[System.String,System.Int32]");
        if (integerArray.GetElementType() != integer || integer.MakeArrayType() != integerArray
                || dictionary.GetGenericArguments()[1] != integer
                || integer.MakePointerType() != Type.GetType("System.Int32*")) {
            throw new AssertionError("Int32 array, generic or pointer identity diverged");
        }
        Type longer = Type.fromJavaClass(Long.class);
        Type[] firstArguments = {string};
        Type first = list.MakeGenericType(firstArguments);
        firstArguments[0] = longer;
        Type same = list.MakeGenericType(new Type[] {string});
        Type different = list.MakeGenericType(new Type[] {longer});
        if (first != same || !first.Equals(same) || first.Equals(different)
                || first == different || first.GetGenericTypeDefinition() != list
                || !list.get_IsGenericType() || list.get_IsConstructedGenericType()
                || !first.get_IsConstructedGenericType() || first.GetGenericArguments()[0] != string) {
            throw new AssertionError("Selected closed generic identity changed");
        }
        Type[] returned = first.GetGenericArguments();
        returned[0] = longer;
        if (first.GetGenericArguments()[0] != string) {
            throw new AssertionError("Generic arguments escaped by reference");
        }
        Type map = Type.fromJavaClass(Map.class);
        Type nestedEntry = Type.fromJavaClass(Map.Entry.class);
        if (map.GetNestedType("Entry") != nestedEntry
                || map.GetNestedType("entry") != null
                || map.GetNestedType("Missing") != null
                || string.GetNestedType("Entry") != null) {
            throw new AssertionError("Selected public nested Type lookup changed");
        }
        Type[] nestedTypes = map.GetNestedTypes();
        if (nestedTypes.length != 1 || nestedTypes[0] != nestedEntry
                || string.GetNestedTypes().length != 0
                || map.MakeArrayType().GetNestedTypes().length != 0) {
            throw new AssertionError("Selected public nested Type enumeration changed");
        }
        nestedTypes[0] = string;
        if (map.GetNestedTypes()[0] != nestedEntry) {
            throw new AssertionError("Nested Type enumeration escaped by reference");
        }
        Type closedMap = map.MakeGenericType(new Type[] {string, integer});
        Type[] closedNestedTypes = closedMap.GetNestedTypes();
        if (closedMap.GetNestedType("Entry") != nestedEntry
                || closedMap.GetNestedType("entry") != null
                || closedNestedTypes.length != 1 || closedNestedTypes[0] != nestedEntry) {
            throw new AssertionError("Constructed generic owner nested Type identity changed");
        }
        Type testOwner = Type.fromJavaClass(TypeIdentityCandidateTest.class);
        if (testOwner.GetNestedType("NestedPrivateFixture") != null
                || testOwner.GetNestedType("PrivateOwnerFixture") != null
                || testOwner.GetNestedTypes().length != 0) {
            throw new AssertionError("Nonpublic nested Type escaped public query");
        }
        Type[] elementOwners = {map.MakeArrayType(), map.MakeByRefType(),
                map.MakePointerType(), map.GetGenericArguments()[0]};
        for (Type elementOwner : elementOwners) {
            if (elementOwner.GetNestedType("Entry") != null
                    || elementOwner.GetNestedTypes().length != 0) {
                throw new AssertionError("Element or generic parameter exposed nested Types");
            }
        }
        try {
            map.GetNestedType(null);
            throw new AssertionError("Null nested Type name accepted");
        } catch (ArgumentNullException expected) {
            if (!"fullname".equals(expected.get_ParamName())) {
                throw new AssertionError("Nested Type null parameter identity changed", expected);
            }
        }
        Type[] nestedParameters = nestedEntry.GetGenericArguments();
        if (nestedParameters.length != 2
                || !"TKey".equals(nestedParameters[0].get_Name())
                || !"TValue".equals(nestedParameters[1].get_Name())
                || nestedParameters[0].get_GenericParameterPosition() != 0
                || nestedParameters[1].get_GenericParameterPosition() != 1) {
            throw new AssertionError("Nested generic parameter positions changed");
        }
        for (Type nestedParameter : nestedParameters) {
            if (nestedParameter.get_DeclaringType() != nestedEntry
                    || !nestedParameter.get_IsNested() || nestedParameter.get_IsNestedPublic()
                    || !nestedParameter.get_IsPublic() || !nestedParameter.get_IsVisible()) {
                throw new AssertionError("Nested generic parameter ownership changed");
            }
        }
        if (Type.GetType("System.Collections.Generic.Dictionary`2+entry") != null
                || Type.GetType("System.Collections.Generic.Dictionary`2+Missing") != null) {
            throw new AssertionError("Selected nested Type misses changed");
        }
        try {
            Type.GetType("System.Collections.Generic.Dictionary`2+Entry[[System.String, System.Private.CoreLib]]");
            throw new AssertionError("Wrong nested generic arity was accepted");
        } catch (ArgumentException expected) {
            // The CLR also rejects this arity even with throwOnError=false.
        }
        Type closedEntry = nestedEntry.MakeGenericType(new Type[] {string, integer});
        String lowerEntryQualified = closedEntry.get_AssemblyQualifiedName()
                .toLowerCase(java.util.Locale.ROOT);
        if (Type.GetType(lowerEntryQualified, false, true) != closedEntry
                || Type.GetType(lowerEntryQualified) != null) {
            throw new AssertionError("Constructed nested qualified ignore-case lookup changed");
        }
        if (Type.GetType(closedEntry.get_FullName().toLowerCase(java.util.Locale.ROOT), false, true)
                != closedEntry
                || Type.GetType(closedEntry.get_FullName().toLowerCase(java.util.Locale.ROOT)) != null) {
            throw new AssertionError("Constructed nested ignore-case lookup changed");
        }
        Type closedEntryByRef = closedEntry.MakeByRefType();
        Type closedEntryPointer = closedEntry.MakePointerType();
        Type closedEntryArrayByRef = closedEntry.MakeArrayType().MakeByRefType();
        if (Type.GetType(closedEntryArrayByRef.get_FullName()) != closedEntryArrayByRef
                || Type.GetType(closedEntryArrayByRef.get_AssemblyQualifiedName())
                        != closedEntryArrayByRef) {
            throw new AssertionError("Constructed nested composite lookup changed");
        }
        if (Type.GetType(closedEntryPointer.get_FullName()) != closedEntryPointer
                || Type.GetType(closedEntryPointer.get_AssemblyQualifiedName())
                        != closedEntryPointer) {
            throw new AssertionError("Constructed nested pointer lookup changed");
        }
        if (Type.GetType(closedEntryByRef.get_FullName()) != closedEntryByRef
                || Type.GetType(closedEntryByRef.get_AssemblyQualifiedName()) != closedEntryByRef) {
            throw new AssertionError("Constructed nested by-reference lookup changed");
        }
        Type closedEntryArray = closedEntry.MakeArrayType();
        Type closedEntryRectangle = closedEntry.MakeArrayType(2);
        Type closedEntryRankThree = closedEntry.MakeArrayType(3);
        Type closedEntryVariable = closedEntry.MakeArrayType(1);
        if (Type.GetType(closedEntryVariable.get_FullName()) != closedEntryVariable
                || Type.GetType(closedEntryVariable.get_AssemblyQualifiedName())
                        != closedEntryVariable) {
            throw new AssertionError("Constructed nested variable-bound lookup changed");
        }
        if (Type.GetType(closedEntryRankThree.get_FullName()) != closedEntryRankThree
                || Type.GetType(closedEntryRankThree.get_AssemblyQualifiedName())
                        != closedEntryRankThree) {
            throw new AssertionError("Constructed nested rank-three lookup changed");
        }
        if (Type.GetType(closedEntryRectangle.get_FullName()) != closedEntryRectangle
                || Type.GetType(closedEntryRectangle.get_AssemblyQualifiedName())
                        != closedEntryRectangle) {
            throw new AssertionError("Constructed nested rectangular lookup changed");
        }
        if (Type.GetType(closedEntryArray.get_FullName()) != closedEntryArray
                || Type.GetType(closedEntryArray.get_AssemblyQualifiedName()) != closedEntryArray) {
            throw new AssertionError("Constructed nested array lookup changed");
        }
        if (Type.GetType(closedEntry.get_FullName()) != closedEntry
                || Type.GetType(closedEntry.get_AssemblyQualifiedName()) != closedEntry) {
            throw new AssertionError("Constructed nested Type lookup changed");
        }
        if (closedEntry != nestedEntry.MakeGenericType(new Type[] {string, integer})
                || closedEntry.GetGenericTypeDefinition() != nestedEntry
                || !closedEntry.get_IsConstructedGenericType()
                || !"System.Collections.Generic.Dictionary`2+Entry[System.String,System.Int32]"
                        .equals(closedEntry.ToString())
                || closedEntry.GetGenericArguments()[0] != string
                || closedEntry.GetGenericArguments()[1] != integer) {
            throw new AssertionError("Nested constructed generic identity changed");
        }
        if (Type.GetType(nestedEntry.get_AssemblyQualifiedName()) != nestedEntry
                || Type.GetType(nestedEntry.MakeArrayType().get_AssemblyQualifiedName())
                        != nestedEntry.MakeArrayType()) {
            throw new AssertionError("Nested Type assembly-qualified round trip changed");
        }
        Type privateOwnerChild = Type.fromJavaClass(PrivateOwnerFixture.PublicChild.class);
        Type publicNestedArray = nestedEntry.MakeArrayType();
        Type privateNestedArray = Type.fromJavaClass(NestedPrivateFixture.class).MakeArrayType();
        if (!publicNestedArray.get_IsPublic() || !publicNestedArray.get_IsVisible()
                || publicNestedArray.get_IsNested() || publicNestedArray.get_IsNestedPublic()
                || !privateNestedArray.get_IsPublic() || privateNestedArray.get_IsVisible()
                || privateNestedArray.get_IsNested()) {
            throw new AssertionError("Selected nested array visibility changed");
        }
        if (!privateOwnerChild.get_IsNestedPublic() || privateOwnerChild.get_IsPublic()
                || privateOwnerChild.get_IsVisible()
                || privateOwnerChild.get_DeclaringType().get_IsVisible()) {
            throw new AssertionError("Nested declaring-type visibility changed");
        }
        Type privateArgument = Type.fromJavaClass(NestedPrivateFixture.class);
        Type privateList = list.MakeGenericType(new Type[] {privateArgument});
        if (privateList.get_IsVisible() || privateList.MakeArrayType().get_IsVisible()
                || !list.MakeGenericType(new Type[] {string}).get_IsVisible()) {
            throw new AssertionError("Selected generic argument visibility changed");
        }
        if (nestedEntry.get_IsPublic() || !nestedEntry.get_IsNestedPublic()
                || !nestedEntry.get_IsVisible()
                || Type.fromJavaClass(NestedPrivateFixture.class).get_IsVisible()) {
            throw new AssertionError("Selected nested Type visibility changed");
        }
        if (Type.GetType("System.Collections.Generic.Dictionary`2+Entry") != nestedEntry
                || Type.GetType("System.Collections.Generic.Dictionary`2+Entry[]")
                        != nestedEntry.MakeArrayType()
                || Type.GetType("system.collections.generic.dictionary`2+entry", false, true)
                        != nestedEntry) {
            throw new AssertionError("Selected nested Type lookup changed");
        }
        if (!"Entry".equals(nestedEntry.get_Name())
                || !"System.Collections.Generic".equals(nestedEntry.get_Namespace())
                || !"System.Collections.Generic.Dictionary`2+Entry".equals(nestedEntry.get_FullName())) {
            throw new AssertionError("Selected nested Type names changed");
        }
        if (!"System.Collections.Generic.Dictionary`2+Entry[TKey,TValue]".equals(nestedEntry.ToString())
                || !"System.Collections.Generic.Dictionary`2+Entry[TKey,TValue][]"
                        .equals(nestedEntry.MakeArrayType().ToString())) {
            throw new AssertionError("Selected nested Type text changed");
        }
        if (nestedEntry.get_DeclaringType() != map || nestedEntry.get_ReflectedType() != map
                || string.get_DeclaringType() != null || string.get_ReflectedType() != null
                || nestedEntry.MakeArrayType().get_DeclaringType() != null) {
            throw new AssertionError("Selected nested Type owner changed");
        }
        if (string.get_IsNested() || string.get_IsNestedPublic()
                || list.get_IsNested() || list.get_IsNestedPublic()
                || !list.GetGenericArguments()[0].get_IsNested()
                || list.GetGenericArguments()[0].get_IsNestedPublic()
                || !nestedEntry.get_IsNested() || !nestedEntry.get_IsNestedPublic()) {
            throw new AssertionError("Selected nested Type flags changed");
        }
        Type nestedAssembly = Type.fromJavaClass(NestedAssemblyFixture.class);
        if (string.get_IsNestedAssembly() || list.GetGenericArguments()[0].get_IsNestedAssembly()
                || nestedEntry.get_IsNestedAssembly() || !nestedAssembly.get_IsNestedAssembly()
                || !nestedAssembly.get_IsNested() || nestedAssembly.get_IsNestedPublic()) {
            throw new AssertionError("Selected nested assembly visibility changed");
        }
        Type nestedPrivate = Type.fromJavaClass(NestedPrivateFixture.class);
        Type nestedFixture = Type.fromJavaClass(PrivateOwnerFixture.class);
        if (nestedFixture.GetNestedType("PublicChild", BindingFlags.Public)
                    != Type.fromJavaClass(PrivateOwnerFixture.PublicChild.class)
                || nestedFixture.GetNestedType("PublicChild", BindingFlags.NonPublic) != null
                || nestedFixture.GetNestedType("PrivateChild", BindingFlags.NonPublic)
                    != Type.fromJavaClass(PrivateOwnerFixture.PrivateChild.class)
                || nestedFixture.GetNestedType("PrivateChild", BindingFlags.Public) != null
                || nestedFixture.GetNestedType("publicchild",
                    BindingFlags.Public.or(BindingFlags.IgnoreCase))
                    != Type.fromJavaClass(PrivateOwnerFixture.PublicChild.class)) {
            throw new AssertionError("Selected flagged nested-type lookup changed");
        }
        Type[] publicNested = nestedFixture.GetNestedTypes(BindingFlags.Public);
        Type[] privateNested = nestedFixture.GetNestedTypes(BindingFlags.NonPublic);
        Type[] bothNested = nestedFixture.GetNestedTypes(
                BindingFlags.Public.or(BindingFlags.NonPublic));
        if (publicNested.length != 1
                || publicNested[0] != Type.fromJavaClass(PrivateOwnerFixture.PublicChild.class)
                || privateNested.length != 1
                || privateNested[0] != Type.fromJavaClass(PrivateOwnerFixture.PrivateChild.class)
                || bothNested.length != 2
                || !java.util.Arrays.asList(bothNested).containsAll(
                    java.util.Arrays.asList(publicNested[0], privateNested[0]))
                || nestedFixture.GetNestedTypes(BindingFlags.Default).length != 0
                || nestedFixture.GetNestedTypes(BindingFlags.Public) == publicNested) {
            throw new AssertionError("Selected flagged nested-type enumeration changed");
        }
        try {
            nestedFixture.GetNestedType(null, BindingFlags.Public);
            throw new AssertionError("Null flagged nested name accepted");
        } catch (ArgumentNullException expected) {
            if (!"fullname".equals(expected.get_ParamName())) {
                throw new AssertionError("Null flagged nested name parameter changed", expected);
            }
        }
        if (string.get_IsNestedPrivate() || list.GetGenericArguments()[0].get_IsNestedPrivate()
                || nestedEntry.get_IsNestedPrivate() || nestedAssembly.get_IsNestedPrivate()
                || !nestedPrivate.get_IsNestedPrivate() || !nestedPrivate.get_IsNested()) {
            throw new AssertionError("Selected nested private visibility changed");
        }
        Type nestedFamily = Type.fromJavaClass(NestedFamilyFixture.class);
        if (string.get_IsNestedFamily() || list.GetGenericArguments()[0].get_IsNestedFamily()
                || nestedEntry.get_IsNestedFamily() || nestedAssembly.get_IsNestedFamily()
                || nestedPrivate.get_IsNestedFamily() || !nestedFamily.get_IsNestedFamily()
                || !nestedFamily.get_IsNested()) {
            throw new AssertionError("Selected nested family visibility changed");
        }
        Type[] listParameters = list.GetGenericArguments();
        Type[] mapParameters = map.GetGenericArguments();
        if (listParameters.length != 1 || mapParameters.length != 2
                || !listParameters[0].get_IsGenericParameter()
                || listParameters[0].get_GenericParameterPosition() != 0
                || mapParameters[0].get_GenericParameterPosition() != 0
                || mapParameters[1].get_GenericParameterPosition() != 1
                || listParameters[0] != list.GetGenericArguments()[0]
                || mapParameters[0] == listParameters[0]
                || listParameters[0].get_IsGenericType()) {
            throw new AssertionError("Generic parameter Type identity changed");
        }
        listParameters[0] = string;
        if (!list.GetGenericArguments()[0].get_IsGenericParameter()) {
            throw new AssertionError("Generic parameter array escaped by reference");
        }
        Type nested = map.MakeGenericType(new Type[] {string, first});
        if (nested != map.MakeGenericType(new Type[] {string, same})
                || nested == map.MakeGenericType(new Type[] {string, different})) {
            throw new AssertionError("Nested generic identity changed");
        }
        try {
            list.MakeGenericType(null);
            throw new AssertionError("Null generic arguments accepted");
        } catch (ArgumentNullException expected) {
            if (!"typeArguments".equals(expected.get_ParamName())) {
                throw new AssertionError("Null parameter identity changed", expected);
            }
        }
        try {
            Type.GetType(null);
            throw new AssertionError("Null type name accepted");
        } catch (ArgumentNullException expected) {
            if (!"typeName".equals(expected.get_ParamName())) {
                throw new AssertionError("Null type-name parameter identity changed", expected);
            }
        }
        try {
            list.MakeGenericType(new Type[] {null});
            throw new AssertionError("Null generic argument accepted");
        } catch (NullPointerException expected) {
            if (!"typeArguments[0]".equals(expected.getMessage())) {
                throw new AssertionError("Null element identity changed", expected);
            }
        }
        java.lang.System.out.println("PASS selected System.Type identity, nested arguments, defensive copies and null boundary");
    }
}
