package System;

import java.util.List;
import java.util.Map;
import System.Reflection.MemberTypes;
import System.Reflection.BindingFlags;
import System.Reflection.CallingConventions;
import System.Reflection.MethodImplAttributes;
import System.Reflection.MethodBody;
import System.Reflection.MemberInfo;
import System.Reflection.MethodBase;
import System.Reflection.MethodInfo;
import System.Reflection.ParameterInfo;
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
import System.Runtime.Serialization.StreamingContext;
import System.Runtime.Serialization.StreamingContextStates;
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
        if (Type.GetType("System.DBNull") != Type.fromJavaClass(DBNull.class)
                || DBNull.Value == null
                || !"".equals(DBNull.Value.ToString())
                || !"".equals(DBNull.Value.ToString(null))
                || !"".equals(DBNull.Value.toString())
                || DBNull.Value.GetTypeCode() != TypeCode.DBNull) {
            throw new AssertionError("Selected DBNull identity changed");
        }
        IConvertible convertibleNull = DBNull.Value;
        Type convertibleType = Type.fromJavaClass(IConvertible.class);
        Type dbnullType = Type.fromJavaClass(DBNull.class);
        Type serializableType = Type.fromJavaClass(ISerializable.class);
        Type[] dbnullInterfaces = dbnullType.GetInterfaces();
        if (Type.GetType("System.Runtime.Serialization.ISerializable") != serializableType
                || !serializableType.get_IsInterface()
                || Type.GetType("System.Runtime.Serialization.SerializationInfo")
                    != Type.fromJavaClass(SerializationInfo.class)
                || Type.GetType("System.Runtime.Serialization.StreamingContext")
                    != Type.fromJavaClass(StreamingContext.class)
                || !Type.fromJavaClass(StreamingContext.class).get_IsValueType()
                || dbnullInterfaces.length != 2
                || dbnullInterfaces[0] != serializableType
                || dbnullInterfaces[1] != convertibleType
                || !serializableType.IsAssignableFrom(dbnullType)
                || !serializableType.IsInstanceOfType(DBNull.Value)
                || dbnullType.GetInterface("System.Runtime.Serialization.ISerializable")
                    != serializableType) {
            throw new AssertionError("Selected DBNull serialization interface metadata changed");
        }
        Type converterType = Type.fromJavaClass(IFormatterConverter.class);
        IFormatterConverter converter = (IFormatterConverter) java.lang.reflect.Proxy.newProxyInstance(
                IFormatterConverter.class.getClassLoader(), new Class<?>[] { IFormatterConverter.class },
                (proxy, method, values) -> null);
        SerializationInfo info = new SerializationInfo(dbnullType, converter);
        if (Type.GetType("System.Runtime.Serialization.IFormatterConverter") != converterType
                || !converterType.get_IsInterface()
                || info.get_ObjectType() != dbnullType
                || !"System.DBNull".equals(info.get_FullTypeName())
                || info.get_MemberCount() != 0
                || new SerializationInfo(dbnullType, converter, true).get_ObjectType() != dbnullType) {
            throw new AssertionError("Selected SerializationInfo construction changed");
        }
        try {
            new SerializationInfo(null, converter);
            throw new AssertionError("Null SerializationInfo type was accepted");
        } catch (ArgumentNullException expected) {
            if (!"type".equals(expected.get_ParamName())) {
                throw new AssertionError("Null SerializationInfo type parameter changed");
            }
        }
        try {
            new SerializationInfo(dbnullType, null);
            throw new AssertionError("Null SerializationInfo converter was accepted");
        } catch (ArgumentNullException expected) {
            if (!"converter".equals(expected.get_ParamName())) {
                throw new AssertionError("Null SerializationInfo converter parameter changed");
            }
        }
        FormatterConverter selectedConverter = new FormatterConverter();
        if (Type.GetType("System.Runtime.Serialization.FormatterConverter")
                    != Type.fromJavaClass(FormatterConverter.class)
                || !(selectedConverter instanceof IFormatterConverter)
                || selectedConverter.ToInt32(42) != 42
                || selectedConverter.ToInt32("17") != 17
                || !"42".equals(selectedConverter.ToString(42))
                || !selectedConverter.ToBoolean(1)
                || !Integer.valueOf(17).equals(selectedConverter.Convert("17", Type.GetType("System.Int32")))
                || !Integer.valueOf(17).equals(selectedConverter.Convert("17", TypeCode.Int32))) {
            throw new AssertionError("Selected FormatterConverter behavior changed");
        }
        try {
            selectedConverter.ToInt32(null);
            throw new AssertionError("Null FormatterConverter value was accepted");
        } catch (ArgumentNullException expected) {
            if (!"value".equals(expected.get_ParamName())) {
                throw new AssertionError("Null FormatterConverter parameter changed");
            }
        }
        try {
            selectedConverter.ToInt32("oops");
            throw new AssertionError("Malformed FormatterConverter value was accepted");
        } catch (FormatException expected) {
            // Matches the pinned selected CLR failure type.
        }
        SerializationInfo serializationMembers = new SerializationInfo(dbnullType, selectedConverter);
        serializationMembers.AddValue("age", 42);
        serializationMembers.AddValue("name", "Ada");
        if (serializationMembers.get_MemberCount() != 2 || serializationMembers.GetInt32("age") != 42
                || !"Ada".equals(serializationMembers.GetString("name"))
                || !Integer.valueOf(42).equals(serializationMembers.GetValue("age", Type.GetType("System.Int32")))
                || Type.GetType("System.Runtime.Serialization.SerializationException")
                    != Type.fromJavaClass(SerializationException.class)) {
            throw new AssertionError("Selected SerializationInfo members changed");
        }
        try {
            serializationMembers.AddValue(null, 1);
            throw new AssertionError("Null member name was accepted");
        } catch (ArgumentNullException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Null member name parameter changed");
            }
        }
        try {
            serializationMembers.GetInt32(null);
            throw new AssertionError("Null member lookup was accepted");
        } catch (ArgumentNullException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Null member lookup parameter changed");
            }
        }
        try {
            serializationMembers.AddValue("age", 1);
            throw new AssertionError("Duplicate member was accepted");
        } catch (SerializationException expected) {
            // Matches the pinned selected CLR failure type.
        }
        try {
            serializationMembers.GetInt32("missing");
            throw new AssertionError("Missing member was accepted");
        } catch (SerializationException expected) {
            // Matches the pinned selected CLR failure type.
        }
        SerializationInfoEnumerator entries = serializationMembers.GetEnumerator();
        Type cursorInterface = Type.GetType("System.Collections.IEnumerator");
        Type[] cursorInterfaces = Type.fromJavaClass(SerializationInfoEnumerator.class).GetInterfaces();
        if (cursorInterface != Type.fromJavaClass(IEnumerator.class)
                || !cursorInterface.get_IsInterface()
                || cursorInterfaces.length != 1 || cursorInterfaces[0] != cursorInterface
                || !cursorInterface.IsAssignableFrom(Type.fromJavaClass(SerializationInfoEnumerator.class))
                || !cursorInterface.IsInstanceOfType(entries)
                || !(entries instanceof IEnumerator)) {
            throw new AssertionError("Selected serialization enumerator interface changed");
        }
        Type entryType = Type.fromJavaClass(SerializationEntry.class);
        if (!entryType.get_IsValueType()
                || entryType.get_BaseType() != Type.GetType("System.ValueType")
                || SerializationEntry.class.getConstructors().length != 0) {
            throw new AssertionError("Selected SerializationEntry type shape changed");
        }
        try {
            var constructor = SerializationEntry.class.getDeclaredConstructor();
            constructor.setAccessible(true);
            SerializationEntry defaultEntry = constructor.newInstance();
            if (defaultEntry.get_Name() != null || defaultEntry.get_ObjectType() != null
                    || defaultEntry.get_Value() != null
                    || SerializationEntry.class.getDeclaredMethod("get_Name").getReturnType() != String.class
                    || SerializationEntry.class.getDeclaredMethod("get_ObjectType").getReturnType() != Type.class
                    || SerializationEntry.class.getDeclaredMethod("get_Value").getReturnType() != Object.class) {
                throw new AssertionError("Selected SerializationEntry defaults changed");
            }
        } catch (ReflectiveOperationException failure) {
            throw new AssertionError("Selected SerializationEntry metadata unavailable", failure);
        }
        java.util.ArrayList<Integer> retainedValues = new java.util.ArrayList<>(List.of(1));
        Type listOfInt = Type.fromJavaClass(List.class).MakeGenericType(
                new Type[] {Type.GetType("System.Int32")});
        SerializationInfo retainedInfo = new SerializationInfo(dbnullType, selectedConverter);
        retainedInfo.AddValue("values", retainedValues, listOfInt);
        SerializationInfoEnumerator retainedCursor = retainedInfo.GetEnumerator();
        if (!retainedCursor.MoveNext()) {
            throw new AssertionError("Retained serialization entry was absent");
        }
        SerializationEntry retainedEntry = retainedCursor.get_Current();
        retainedInfo.AddValue("second", 2);
        retainedValues.add(3);
        if (!"values".equals(retainedEntry.get_Name())
                || !listOfInt.get_FullName().equals(retainedEntry.get_ObjectType().get_FullName())
                || retainedEntry.get_Value() != retainedValues
                || retainedValues.size() != 2
                || retainedCursor.MoveNext()
                || retainedInfo.get_MemberCount() != 2) {
            throw new AssertionError("Selected SerializationEntry value snapshot changed");
        }
        Object sharedEntryValue = new Object();
        SerializationInfo firstEntryInfo = new SerializationInfo(dbnullType, selectedConverter);
        firstEntryInfo.AddValue("item", sharedEntryValue);
        SerializationInfo equalEntryInfo = new SerializationInfo(dbnullType, selectedConverter);
        equalEntryInfo.AddValue("item", sharedEntryValue);
        SerializationInfo otherNameInfo = new SerializationInfo(dbnullType, selectedConverter);
        otherNameInfo.AddValue("other", sharedEntryValue);
        SerializationInfo otherValueInfo = new SerializationInfo(dbnullType, selectedConverter);
        otherValueInfo.AddValue("item", new Object());
        SerializationInfoEnumerator firstEntryCursor = firstEntryInfo.GetEnumerator();
        SerializationInfoEnumerator equalEntryCursor = equalEntryInfo.GetEnumerator();
        SerializationInfoEnumerator otherNameCursor = otherNameInfo.GetEnumerator();
        SerializationInfoEnumerator otherValueCursor = otherValueInfo.GetEnumerator();
        firstEntryCursor.MoveNext();
        equalEntryCursor.MoveNext();
        otherNameCursor.MoveNext();
        otherValueCursor.MoveNext();
        SerializationEntry firstEntry = firstEntryCursor.get_Current();
        SerializationEntry equalEntry = equalEntryCursor.get_Current();
        if (!firstEntry.Equals(equalEntry) || !firstEntry.equals(equalEntry)
                || firstEntry.GetHashCode() != equalEntry.GetHashCode()
                || firstEntry.Equals(otherNameCursor.get_Current())
                || firstEntry.Equals(otherValueCursor.get_Current())
                || !"System.Runtime.Serialization.SerializationEntry".equals(firstEntry.ToString())) {
            throw new AssertionError("Selected SerializationEntry equality changed");
        }
        SerializationEntry textEntry = serializationEntry("same", Type.GetType("System.String"));
        SerializationEntry objectTypedEntry = serializationEntry("same", Type.GetType("System.Object"));
        SerializationEntry changedValueEntry = serializationEntry("different", Type.GetType("System.String"));
        SerializationEntry nullEntryA = serializationEntry(null, Type.GetType("System.String"));
        SerializationEntry nullEntryB = serializationEntry(null, Type.GetType("System.String"));
        if (textEntry.Equals(objectTypedEntry) || textEntry.Equals(changedValueEntry)
                || !nullEntryA.Equals(nullEntryB)
                || nullEntryA.GetHashCode() != nullEntryB.GetHashCode()
                || nullEntryA.Equals(textEntry)) {
            throw new AssertionError("Selected SerializationEntry type equality changed");
        }
        SerializationInfo duplicateState = new SerializationInfo(dbnullType, selectedConverter);
        duplicateState.AddValue("item", 42);
        try {
            duplicateState.AddValue("item", 99);
            throw new AssertionError("Duplicate serialization write was accepted");
        } catch (SerializationException expected) {
            // Pinned selected CLR failure type.
        }
        SerializationInfoEnumerator duplicateCursor = duplicateState.GetEnumerator();
        if (duplicateState.get_MemberCount() != 1 || duplicateState.GetInt32("item") != 42
                || !duplicateCursor.MoveNext()
                || !Integer.valueOf(42).equals(duplicateCursor.get_Value())
                || duplicateCursor.MoveNext()) {
            throw new AssertionError("Rejected duplicate changed serialization state");
        }
        SerializationInfo valueOverloads = new SerializationInfo(dbnullType, selectedConverter);
        valueOverloads.AddValue("character", 'Q');
        valueOverloads.AddValue("single", 1.25f);
        valueOverloads.AddValue("decimal", new Decimal(12));
        valueOverloads.AddValue("date", new DateTime(2024, 2, 29));
        SerializationInfoEnumerator valueCursor = valueOverloads.GetEnumerator();
        if (valueOverloads.get_MemberCount() != 4
                || valueOverloads.GetChar("character") != 'Q'
                || valueOverloads.GetSingle("single") != 1.25f
                || !"12".equals(valueOverloads.GetDecimal("decimal").ToString(null))
                || !"2024-02-29".equals(valueOverloads.GetDateTime("date")
                    .ToString("yyyy-MM-dd", null))
                || !valueCursor.MoveNext()
                || !"System.Char".equals(valueCursor.get_ObjectType().get_FullName())
                || !valueCursor.MoveNext()
                || !"System.Single".equals(valueCursor.get_ObjectType().get_FullName())
                || !valueCursor.MoveNext()
                || !"System.Decimal".equals(valueCursor.get_ObjectType().get_FullName())
                || !valueCursor.MoveNext()
                || !"System.DateTime".equals(valueCursor.get_ObjectType().get_FullName())) {
            throw new AssertionError("Selected serialization value overloads changed");
        }
        SerializationInfo numericOverloads = new SerializationInfo(dbnullType, selectedConverter);
        java.math.BigInteger maximumUInt64 = new java.math.BigInteger("18446744073709551615");
        numericOverloads.AddValue("signed", (short) -1234);
        numericOverloads.AddValue("unsigned", maximumUInt64);
        SerializationInfoEnumerator numericCursor = numericOverloads.GetEnumerator();
        Type uint64Type = Type.GetType("System.UInt64");
        if (numericOverloads.get_MemberCount() != 2
                || numericOverloads.GetInt16("signed") != -1234
                || !maximumUInt64.equals(numericOverloads.GetUInt64("unsigned"))
                || Type.GetTypeCode(uint64Type) != TypeCode.UInt64
                || !numericCursor.MoveNext()
                || !"System.Int16".equals(numericCursor.get_ObjectType().get_FullName())
                || !numericCursor.MoveNext()
                || numericCursor.get_ObjectType() != uint64Type) {
            throw new AssertionError("Selected numeric serialization overloads changed");
        }
        SerializationInfo unsignedMembers = new SerializationInfo(dbnullType, selectedConverter);
        unsignedMembers.AddValue("u16", new UInt16(60000));
        unsignedMembers.AddValue("u32", new UInt32(4000000000L));
        SerializationInfoEnumerator unsignedCursor = unsignedMembers.GetEnumerator();
        if (unsignedMembers.get_MemberCount() != 2
                || unsignedMembers.GetUInt16("u16") != 60000
                || unsignedMembers.GetUInt32("u32") != 4000000000L
                || Type.GetTypeCode(Type.GetType("System.UInt16")) != TypeCode.UInt16
                || Type.GetTypeCode(Type.GetType("System.UInt32")) != TypeCode.UInt32
                || !unsignedCursor.MoveNext()
                || !"System.UInt16".equals(unsignedCursor.get_ObjectType().get_FullName())
                || !unsignedCursor.MoveNext()
                || !"System.UInt32".equals(unsignedCursor.get_ObjectType().get_FullName())) {
            throw new AssertionError("Selected unsigned serialization members changed");
        }
        IConvertible uint16Convertible = new UInt16(60000);
        if (!Type.GetType("System.UInt16").IsAssignableTo(Type.GetType("System.IConvertible"))
                || uint16Convertible.GetTypeCode() != TypeCode.UInt16
                || uint16Convertible.ToInt32(null) != 60000
                || uint16Convertible.ToUInt32(null) != 60000L
                || !"60000".equals(uint16Convertible.ToString(null))) {
            throw new AssertionError("Selected UInt16 convertible values changed");
        }
        try {
            uint16Convertible.ToByte(null);
            throw new AssertionError("UInt16 to Byte overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        try {
            uint16Convertible.ToInt16(null);
            throw new AssertionError("UInt16 to Int16 overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        try {
            uint16Convertible.ToDateTime(null);
            throw new AssertionError("UInt16 to DateTime accepted");
        } catch (InvalidCastException expected) {
            // Pinned CLR failure type.
        }
        IConvertible uint32Convertible = new UInt32(4000000000L);
        if (!Type.GetType("System.UInt32").IsAssignableTo(Type.GetType("System.IConvertible"))
                || uint32Convertible.GetTypeCode() != TypeCode.UInt32
                || uint32Convertible.ToInt64(null) != 4000000000L
                || uint32Convertible.ToUInt32(null) != 4000000000L
                || !"4000000000".equals(uint32Convertible.ToUInt64(null).toString())
                || !"4000000000".equals(uint32Convertible.ToDecimal(null).ToString(null))
                || !"4000000000".equals(uint32Convertible.ToString(null))) {
            throw new AssertionError("Selected UInt32 convertible values changed");
        }
        try {
            uint32Convertible.ToInt32(null);
            throw new AssertionError("UInt32 to Int32 overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        try {
            uint32Convertible.ToByte(null);
            throw new AssertionError("UInt32 to Byte overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        try {
            uint32Convertible.ToDateTime(null);
            throw new AssertionError("UInt32 to DateTime accepted");
        } catch (InvalidCastException expected) {
            // Pinned CLR failure type.
        }
        SerializationInfo unsignedText = new SerializationInfo(dbnullType, selectedConverter);
        unsignedText.AddValue("u16Text", "60000");
        unsignedText.AddValue("u32Text", "4000000000");
        if (unsignedText.GetUInt16("u16Text") != 60000
                || unsignedText.GetUInt32("u32Text") != 4000000000L
                || !Integer.valueOf(60000).equals(selectedConverter.Convert(
                    "60000", Type.GetType("System.UInt16")))
                || !Long.valueOf(4000000000L).equals(selectedConverter.Convert(
                    "4000000000", TypeCode.UInt32))) {
            throw new AssertionError("Selected unsigned formatter routes changed");
        }
        for (String value : new String[] {"65536", "-1"}) {
            try {
                selectedConverter.ToUInt16(value);
                throw new AssertionError("UInt16 overflow accepted");
            } catch (OverflowException expected) {
                // Pinned CLR failure type.
            }
        }
        for (String value : new String[] {"4294967296", "-1"}) {
            try {
                selectedConverter.ToUInt32(value);
                throw new AssertionError("UInt32 overflow accepted");
            } catch (OverflowException expected) {
                // Pinned CLR failure type.
            }
        }
        try {
            selectedConverter.ToUInt16("bad");
            throw new AssertionError("Invalid UInt16 text accepted");
        } catch (FormatException expected) {
            // Pinned CLR failure type.
        }
        try {
            selectedConverter.ToUInt32(null);
            throw new AssertionError("Null UInt32 accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        if (uint16Convertible.ToType(Type.GetType("System.UInt16"), null) != uint16Convertible
                || uint32Convertible.ToType(Type.GetType("System.UInt32"), null) != uint32Convertible
                || ((UInt32) uint16Convertible.ToType(Type.GetType("System.UInt32"), null)).get_Value() != 60000L
                || ((Int32) uint16Convertible.ToType(Type.GetType("System.Int32"), null)).get_Value() != 60000
                || !Long.valueOf(4000000000L).equals(uint32Convertible.ToType(
                    Type.GetType("System.Int64"), null))
                || !"4000000000".equals(((Decimal) uint32Convertible.ToType(
                    Type.GetType("System.Decimal"), null)).ToString(null))
                || !"4000000000".equals(uint32Convertible.ToType(
                    Type.GetType("System.String"), null))) {
            throw new AssertionError("Selected unsigned ToType values changed");
        }
        try {
            uint32Convertible.ToType(Type.GetType("System.Int32"), null);
            throw new AssertionError("UInt32 ToType Int32 overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        try {
            uint32Convertible.ToType(Type.GetType("System.UInt16"), null);
            throw new AssertionError("UInt32 ToType UInt16 overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        try {
            uint16Convertible.ToType(null, null);
            throw new AssertionError("Null UInt16 conversion target accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        SerializationInfo signedFloatText = new SerializationInfo(dbnullType, selectedConverter);
        signedFloatText.AddValue("int16Text", "-1234");
        signedFloatText.AddValue("singleText", "1.25");
        if (signedFloatText.GetInt16("int16Text") != -1234
                || signedFloatText.GetSingle("singleText") != 1.25f
                || !Short.valueOf((short) -1234).equals(selectedConverter.Convert(
                    "-1234", Type.GetType("System.Int16")))
                || !Float.valueOf(1.25f).equals(selectedConverter.Convert(
                    "1.25", TypeCode.Single))) {
            throw new AssertionError("Selected Int16/Single formatter routes changed");
        }
        for (String value : new String[] {"32768", "-32769"}) {
            try {
                selectedConverter.ToInt16(value);
                throw new AssertionError("Int16 overflow accepted");
            } catch (OverflowException expected) {
                // Pinned CLR failure type.
            }
        }
        try {
            selectedConverter.ToInt16("bad");
            throw new AssertionError("Invalid Int16 text accepted");
        } catch (FormatException expected) {
            // Pinned CLR failure type.
        }
        try {
            selectedConverter.ToSingle("bad");
            throw new AssertionError("Invalid Single text accepted");
        } catch (FormatException expected) {
            // Pinned CLR failure type.
        }
        try {
            selectedConverter.ToSingle(null);
            throw new AssertionError("Null Single accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        String maximumUnsignedText = "18446744073709551615";
        SerializationInfo unsigned64Text = new SerializationInfo(dbnullType, selectedConverter);
        unsigned64Text.AddValue("u64Text", maximumUnsignedText);
        if (!maximumUnsignedText.equals(unsigned64Text.GetUInt64("u64Text").toString())
                || !maximumUnsignedText.equals(selectedConverter.Convert(
                    maximumUnsignedText, Type.GetType("System.UInt64")).toString())
                || !maximumUnsignedText.equals(selectedConverter.Convert(
                    maximumUnsignedText, TypeCode.UInt64).toString())) {
            throw new AssertionError("Selected UInt64 formatter routes changed");
        }
        for (String value : new String[] {"18446744073709551616", "-1"}) {
            try {
                selectedConverter.ToUInt64(value);
                throw new AssertionError("UInt64 overflow accepted");
            } catch (OverflowException expected) {
                // Pinned CLR failure type.
            }
        }
        try {
            selectedConverter.ToUInt64("bad");
            throw new AssertionError("Invalid UInt64 text accepted");
        } catch (FormatException expected) {
            // Pinned CLR failure type.
        }
        try {
            selectedConverter.ToUInt64(null);
            throw new AssertionError("Null UInt64 accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        SerializationInfo decimalText = new SerializationInfo(dbnullType, selectedConverter);
        decimalText.AddValue("decimalText", "12.5");
        if (!"12.5".equals(decimalText.GetDecimal("decimalText").ToString(null))
                || !"12.5".equals(((Decimal) selectedConverter.Convert(
                    "12.5", Type.GetType("System.Decimal"))).ToString(null))
                || !"12.5".equals(((Decimal) selectedConverter.Convert(
                    "12.5", TypeCode.Decimal)).ToString(null))
                || !"42".equals(selectedConverter.ToDecimal(42).ToString(null))) {
            throw new AssertionError("Selected Decimal formatter routes changed");
        }
        try {
            selectedConverter.ToDecimal("bad");
            throw new AssertionError("Invalid Decimal text accepted");
        } catch (FormatException expected) {
            // Pinned CLR failure type.
        }
        try {
            selectedConverter.ToDecimal(null);
            throw new AssertionError("Null Decimal accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        SerializationInfo dateText = new SerializationInfo(dbnullType, selectedConverter);
        dateText.AddValue("dateText", "2024-02-29");
        if (!"2024-02-29".equals(dateText.GetDateTime("dateText").ToString("yyyy-MM-dd", null))
                || !"2024-02-29".equals(((DateTime) selectedConverter.Convert(
                    "2024-02-29", Type.GetType("System.DateTime"))).ToString("yyyy-MM-dd", null))
                || !"2024-02-29".equals(((DateTime) selectedConverter.Convert(
                    "2024-02-29", TypeCode.DateTime)).ToString("yyyy-MM-dd", null))) {
            throw new AssertionError("Selected DateTime formatter routes changed");
        }
        for (String value : new String[] {"bad", "2023-02-29"}) {
            try {
                selectedConverter.ToDateTime(value);
                throw new AssertionError("Invalid DateTime text accepted");
            } catch (FormatException expected) {
                // Pinned CLR failure type.
            }
        }
        try {
            selectedConverter.ToDateTime(null);
            throw new AssertionError("Null DateTime accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        SerializationInfo charText = new SerializationInfo(dbnullType, selectedConverter);
        charText.AddValue("charText", "Q");
        if (charText.GetChar("charText") != 'Q'
                || !Character.valueOf('Q').equals(selectedConverter.Convert(
                    "Q", Type.GetType("System.Char")))
                || !Character.valueOf('Q').equals(selectedConverter.Convert(
                    "Q", TypeCode.Char))
                || selectedConverter.ToChar(65) != 'A') {
            throw new AssertionError("Selected Char formatter routes changed");
        }
        for (String value : new String[] {"", "AB"}) {
            try {
                selectedConverter.ToChar(value);
                throw new AssertionError("Invalid Char text accepted");
            } catch (FormatException expected) {
                // Pinned CLR failure type.
            }
        }
        try {
            selectedConverter.ToChar(null);
            throw new AssertionError("Null Char accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        Object convertibleObject = Integer.valueOf(42);
        Object plainObject = new Object();
        if (selectedConverter.Convert(convertibleObject, Type.GetType("System.Object")) != convertibleObject
                || selectedConverter.Convert(convertibleObject, TypeCode.Object) != convertibleObject
                || selectedConverter.Convert(plainObject, Type.GetType("System.Object")) != plainObject
                || !Integer.valueOf(42).equals(selectedConverter.Convert(42, TypeCode.Object))) {
            throw new AssertionError("Selected formatter Object routes changed");
        }
        try {
            selectedConverter.Convert(plainObject, TypeCode.Object);
            throw new AssertionError("Plain object accepted as TypeCode.Object");
        } catch (InvalidCastException expected) {
            // Pinned CLR failure type.
        }
        try {
            selectedConverter.Convert(null, Type.GetType("System.Object"));
            throw new AssertionError("Null Object Type conversion accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        try {
            selectedConverter.Convert(null, TypeCode.Object);
            throw new AssertionError("Null Object TypeCode conversion accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        if (selectedConverter.Convert(DBNull.Value, Type.GetType("System.DBNull")) != DBNull.Value) {
            throw new AssertionError("Selected DBNull Type conversion changed");
        }
        for (Object value : new Object[] {DBNull.Value, Integer.valueOf(42)}) {
            for (TypeCode code : new TypeCode[] {TypeCode.DBNull, TypeCode.Empty}) {
                try {
                    selectedConverter.Convert(value, code);
                    throw new AssertionError("Unsupported TypeCode conversion accepted");
                } catch (InvalidCastException expected) {
                    // Pinned CLR failure type.
                }
            }
        }
        try {
            selectedConverter.Convert(null, TypeCode.DBNull);
            throw new AssertionError("Null DBNull TypeCode conversion accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        SerializationInfo crossTypeMembers = new SerializationInfo(dbnullType, selectedConverter);
        crossTypeMembers.AddValue("u64", new java.math.BigInteger("18446744073709551615"));
        crossTypeMembers.AddValue("u32", new UInt32(4000000000L));
        crossTypeMembers.AddValue("byte", new Byte(200));
        crossTypeMembers.AddValue("dateText", "2024-02-29");
        if (!"18446744073709551615".equals(crossTypeMembers.GetValue(
                    "u64", Type.GetType("System.String")))
                || !"4000000000".equals(crossTypeMembers.GetValue(
                    "u32", Type.GetType("System.String")))
                || !"200".equals(crossTypeMembers.GetValue(
                    "byte", Type.GetType("System.String")))
                || !"2024-02-29".equals(((DateTime) crossTypeMembers.GetValue(
                    "dateText", Type.GetType("System.DateTime"))).ToString("yyyy-MM-dd", null))) {
            throw new AssertionError("Selected GetValue cross-type conversions changed");
        }
        try {
            crossTypeMembers.GetValue("u32", Type.GetType("System.Int32"));
            throw new AssertionError("UInt32 GetValue narrowing accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        DateTime leapDay = new DateTime(2024, 2, 29);
        IConvertible dateConvertible = leapDay;
        DateTime dateCopy = dateConvertible.ToDateTime(null);
        DateTime dateTypeCopy = (DateTime) dateConvertible.ToType(Type.GetType("System.DateTime"), null);
        if (!Type.GetType("System.DateTime").IsAssignableTo(Type.GetType("System.IConvertible"))
                || dateConvertible.GetTypeCode() != TypeCode.DateTime
                || dateCopy == leapDay || dateTypeCopy == leapDay
                || !"2024-02-29".equals(dateCopy.ToString("yyyy-MM-dd", null))
                || !"02/29/2024 00:00:00".equals(dateConvertible.ToString(null))) {
            throw new AssertionError("Selected DateTime IConvertible values changed");
        }
        try {
            dateConvertible.ToInt32(null);
            throw new AssertionError("DateTime to Int32 accepted");
        } catch (InvalidCastException expected) {
            // Pinned CLR failure type.
        }
        try {
            dateConvertible.ToBoolean(null);
            throw new AssertionError("DateTime to Boolean accepted");
        } catch (InvalidCastException expected) {
            // Pinned CLR failure type.
        }
        try {
            dateConvertible.ToByte(null);
            throw new AssertionError("DateTime to Byte accepted");
        } catch (InvalidCastException expected) {
            // Pinned CLR failure type.
        }
        IConvertible decimalConvertible = Decimal.Parse("12.5");
        if (!Type.GetType("System.Decimal").IsAssignableTo(Type.GetType("System.IConvertible"))
                || decimalConvertible.GetTypeCode() != TypeCode.Decimal
                || decimalConvertible.ToInt32(null) != 12
                || Decimal.Parse("13.5").ToInt32(null) != 14
                || decimalConvertible.ToDouble(null) != 12.5d
                || !decimalConvertible.ToBoolean(null)
                || !"12.5".equals(decimalConvertible.ToString(null))
                || !"12.5".equals(decimalConvertible.ToDecimal(null).ToString(null))) {
            throw new AssertionError("Selected Decimal IConvertible values changed");
        }
        try {
            decimalConvertible.ToChar(null);
            throw new AssertionError("Decimal to Char accepted");
        } catch (InvalidCastException expected) {
            // Pinned CLR failure type.
        }
        try {
            decimalConvertible.ToDateTime(null);
            throw new AssertionError("Decimal to DateTime accepted");
        } catch (InvalidCastException expected) {
            // Pinned CLR failure type.
        }
        java.math.BigInteger maxUnsigned64 = new java.math.BigInteger("18446744073709551615");
        SerializationInfo crossUnsigned = new SerializationInfo(dbnullType, selectedConverter);
        crossUnsigned.AddValue("u64", maxUnsigned64);
        if (!"18446744073709551615".equals(selectedConverter.ToDecimal(maxUnsigned64).ToString(null))
                || !"18446744073709551615".equals(((Decimal) crossUnsigned.GetValue(
                    "u64", Type.GetType("System.Decimal"))).ToString(null))
                || selectedConverter.ToInt64(java.math.BigInteger.valueOf(42)) != 42L) {
            throw new AssertionError("Selected UInt64 cross conversions changed");
        }
        try {
            selectedConverter.ToInt64(maxUnsigned64);
            throw new AssertionError("UInt64 to Int64 overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        try {
            selectedConverter.ToUInt32(maxUnsigned64);
            throw new AssertionError("UInt64 to UInt32 overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        SerializationInfo byteMembers = new SerializationInfo(dbnullType, selectedConverter);
        byteMembers.AddValue("byte", new Byte(200));
        byteMembers.AddValue("sbyte", new SByte(-5));
        SerializationInfoEnumerator byteCursor = byteMembers.GetEnumerator();
        if (byteMembers.get_MemberCount() != 2
                || byteMembers.GetByte("byte") != 200
                || byteMembers.GetSByte("sbyte") != -5
                || Type.GetTypeCode(Type.GetType("System.Byte")) != TypeCode.Byte
                || Type.GetTypeCode(Type.GetType("System.SByte")) != TypeCode.SByte
                || !byteCursor.MoveNext()
                || !"System.Byte".equals(byteCursor.get_ObjectType().get_FullName())
                || !byteCursor.MoveNext()
                || !"System.SByte".equals(byteCursor.get_ObjectType().get_FullName())) {
            throw new AssertionError("Selected byte serialization members changed");
        }
        IConvertible byteConvertible = new Byte(200);
        IConvertible sbyteConvertible = new SByte(-5);
        if (!Type.GetType("System.Byte").IsAssignableTo(Type.GetType("System.IConvertible"))
                || !Type.GetType("System.SByte").IsAssignableTo(Type.GetType("System.IConvertible"))
                || byteConvertible.GetTypeCode() != TypeCode.Byte
                || sbyteConvertible.GetTypeCode() != TypeCode.SByte
                || byteConvertible.ToInt32(null) != 200
                || sbyteConvertible.ToInt32(null) != -5
                || !"200".equals(byteConvertible.ToString(null))
                || !"-5".equals(sbyteConvertible.ToString(null))) {
            throw new AssertionError("Selected byte convertible contract changed");
        }
        try {
            byteConvertible.ToSByte(null);
            throw new AssertionError("Byte to SByte overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        try {
            sbyteConvertible.ToByte(null);
            throw new AssertionError("SByte to Byte overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        try {
            byteConvertible.ToDateTime(null);
            throw new AssertionError("Byte to DateTime accepted");
        } catch (InvalidCastException expected) {
            // Pinned CLR failure type.
        }
        if (byteConvertible.ToType(Type.GetType("System.Byte"), null) != byteConvertible
                || sbyteConvertible.ToType(Type.GetType("System.SByte"), null) != sbyteConvertible
                || !Integer.valueOf(200).equals(((Int32) byteConvertible.ToType(
                    Type.GetType("System.Int32"), null)).get_Value())
                || !Integer.valueOf(-5).equals(((Int32) sbyteConvertible.ToType(
                    Type.GetType("System.Int32"), null)).get_Value())
                || !"200".equals(byteConvertible.ToType(Type.GetType("System.String"), null))
                || !"-5".equals(sbyteConvertible.ToType(Type.GetType("System.String"), null))
                || !"200".equals(((Decimal) byteConvertible.ToType(
                    Type.GetType("System.Decimal"), null)).ToString(null))
                || !"-5".equals(((Decimal) sbyteConvertible.ToType(
                    Type.GetType("System.Decimal"), null)).ToString(null))) {
            throw new AssertionError("Selected Byte/SByte ToType values changed");
        }
        try {
            byteConvertible.ToType(Type.GetType("System.SByte"), null);
            throw new AssertionError("Byte ToType overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        try {
            sbyteConvertible.ToType(Type.GetType("System.Byte"), null);
            throw new AssertionError("SByte ToType overflow accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
        try {
            byteConvertible.ToType(null, null);
            throw new AssertionError("Null Byte conversion target accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        SerializationInfo byteConversions = new SerializationInfo(dbnullType, selectedConverter);
        byteConversions.AddValue("byteText", "255");
        byteConversions.AddValue("sbyteText", "-128");
        if (byteConversions.GetByte("byteText") != 255
                || byteConversions.GetSByte("sbyteText") != -128
                || selectedConverter.ToByte(200) != 200
                || selectedConverter.ToSByte(-5) != -5
                || !Short.valueOf((short) 200).equals(selectedConverter.Convert("200", Type.GetType("System.Byte")))
                || !java.lang.Byte.valueOf((byte) -5).equals(selectedConverter.Convert("-5", TypeCode.SByte))) {
            throw new AssertionError("Selected byte conversions changed");
        }
        for (Object value : new Object[] {"256", -1}) {
            try {
                selectedConverter.ToByte(value);
                throw new AssertionError("Byte overflow accepted");
            } catch (OverflowException expected) {
                // Pinned CLR failure type.
            }
        }
        for (Object value : new Object[] {"128", -129}) {
            try {
                selectedConverter.ToSByte(value);
                throw new AssertionError("SByte overflow accepted");
            } catch (OverflowException expected) {
                // Pinned CLR failure type.
            }
        }
        try {
            selectedConverter.ToByte("bad");
            throw new AssertionError("Invalid Byte text accepted");
        } catch (FormatException expected) {
            // Pinned CLR failure type.
        }
        try {
            selectedConverter.ToSByte("bad");
            throw new AssertionError("Invalid SByte text accepted");
        } catch (FormatException expected) {
            // Pinned CLR failure type.
        }
        try {
            selectedConverter.ToByte(null);
            throw new AssertionError("Null Byte value accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR failure type.
        }
        if (Type.GetType("System.Runtime.Serialization.SerializationEntry")
                    != Type.fromJavaClass(SerializationEntry.class)
                || Type.GetType("System.Runtime.Serialization.SerializationInfoEnumerator")
                    != Type.fromJavaClass(SerializationInfoEnumerator.class)
                || !entries.MoveNext() || !"age".equals(entries.get_Name())
                || !"System.Int32".equals(entries.get_ObjectType().get_FullName())
                || !Integer.valueOf(42).equals(entries.get_Value())
                || !"age".equals(entries.get_Current().get_Name())
                || !entries.MoveNext() || !"name".equals(entries.get_Name())
                || !"System.String".equals(entries.get_ObjectType().get_FullName())
                || !"Ada".equals(entries.get_Value())
                || entries.MoveNext()) {
            throw new AssertionError("Selected serialization enumeration changed");
        }
        entries.Reset();
        if (!entries.MoveNext() || !"age".equals(entries.get_Name())) {
            throw new AssertionError("Serialization enumeration reset changed");
        }
        SerializationInfoEnumerator cursorBoundary = serializationMembers.GetEnumerator();
        assertEnumeratorOutsideMember(cursorBoundary);
        SerializationInfo mutationMembers = new SerializationInfo(dbnullType, selectedConverter);
        mutationMembers.AddValue("first", 1);
        SerializationInfoEnumerator snapshotCursor = mutationMembers.GetEnumerator();
        mutationMembers.AddValue("second", 2);
        if (mutationMembers.get_MemberCount() != 2 || !snapshotCursor.MoveNext()
                || !"first".equals(snapshotCursor.get_Name()) || snapshotCursor.MoveNext()) {
            throw new AssertionError("Serialization enumerator snapshot changed");
        }
        snapshotCursor.Reset();
        if (!snapshotCursor.MoveNext() || !"first".equals(snapshotCursor.get_Name())
                || snapshotCursor.MoveNext()) {
            throw new AssertionError("Serialization enumerator reset snapshot changed");
        }
        SerializationInfoEnumerator freshCursor = mutationMembers.GetEnumerator();
        if (!freshCursor.MoveNext() || !"first".equals(freshCursor.get_Name())
                || !freshCursor.MoveNext() || !"second".equals(freshCursor.get_Name())
                || freshCursor.MoveNext()) {
            throw new AssertionError("Fresh serialization enumeration changed");
        }
        SerializationInfo emptyMembers = new SerializationInfo(dbnullType, selectedConverter);
        SerializationInfoEnumerator emptyCursor = emptyMembers.GetEnumerator();
        if (emptyCursor.MoveNext()) {
            throw new AssertionError("Empty serialization cursor advanced");
        }
        emptyCursor.Reset();
        if (emptyCursor.MoveNext()) {
            throw new AssertionError("Reset empty serialization cursor advanced");
        }
        emptyMembers.AddValue("added", 1);
        if (emptyMembers.get_MemberCount() != 1 || emptyCursor.MoveNext()) {
            throw new AssertionError("Empty cursor changed after AddValue");
        }
        assertEnumeratorOutsideMember(emptyCursor);
        SerializationInfoEnumerator afterEmptyAdd = emptyMembers.GetEnumerator();
        if (!afterEmptyAdd.MoveNext() || !"added".equals(afterEmptyAdd.get_Name())) {
            throw new AssertionError("Fresh cursor after empty AddValue changed");
        }
        SerializationInfo primitives = new SerializationInfo(dbnullType, selectedConverter);
        primitives.AddValue("flag", true);
        primitives.AddValue("large", 5000000000L);
        primitives.AddValue("ratio", 1.5d);
        SerializationInfoEnumerator primitiveCursor = primitives.GetEnumerator();
        if (primitives.get_MemberCount() != 3 || !primitives.GetBoolean("flag")
                || primitives.GetInt64("large") != 5000000000L
                || primitives.GetDouble("ratio") != 1.5d
                || !primitiveCursor.MoveNext()
                || !"System.Boolean".equals(primitiveCursor.get_ObjectType().get_FullName())
                || !primitiveCursor.MoveNext()
                || !"System.Int64".equals(primitiveCursor.get_ObjectType().get_FullName())
                || !primitiveCursor.MoveNext()
                || !"System.Double".equals(primitiveCursor.get_ObjectType().get_FullName())) {
            throw new AssertionError("Selected primitive serialization members changed");
        }
        SerializationInfo convertedPrimitives = new SerializationInfo(dbnullType, selectedConverter);
        convertedPrimitives.AddValue("one", 1);
        convertedPrimitives.AddValue("integerText", "17");
        convertedPrimitives.AddValue("decimalText", "1.5");
        convertedPrimitives.AddValue("long", 5L);
        if (!convertedPrimitives.GetBoolean("one")
                || convertedPrimitives.GetInt64("integerText") != 17L
                || convertedPrimitives.GetDouble("decimalText") != 1.5d
                || convertedPrimitives.GetInt32("long") != 5
                || !Long.valueOf(17).equals(convertedPrimitives.GetValue(
                    "integerText", Type.GetType("System.Int64")))
                || !Double.valueOf(1.5d).equals(selectedConverter.Convert("1.5", TypeCode.Double))) {
            throw new AssertionError("Selected primitive serialization conversions changed");
        }
        try {
            selectedConverter.ToInt64("oops");
            throw new AssertionError("Malformed Int64 conversion was accepted");
        } catch (FormatException expected) {
            // Pinned selected CLR failure type.
        }
        try {
            selectedConverter.ToInt64("9223372036854775808");
            throw new AssertionError("Overflowing Int64 conversion was accepted");
        } catch (OverflowException expected) {
            // Pinned selected CLR failure type.
        }
        try {
            selectedConverter.ToInt32(5000000000L);
            throw new AssertionError("Overflowing Int32 conversion was accepted");
        } catch (OverflowException expected) {
            // Pinned selected CLR failure type.
        }
        try {
            selectedConverter.ToDouble("oops");
            throw new AssertionError("Malformed Double conversion was accepted");
        } catch (FormatException expected) {
            // Pinned selected CLR failure type.
        }
        try {
            selectedConverter.ToInt64(null);
            throw new AssertionError("Null Int64 conversion was accepted");
        } catch (ArgumentNullException expected) {
            if (!"value".equals(expected.get_ParamName())) {
                throw new AssertionError("Null Int64 parameter changed");
            }
        }
        try {
            selectedConverter.ToDouble(null);
            throw new AssertionError("Null Double conversion was accepted");
        } catch (ArgumentNullException expected) {
            if (!"value".equals(expected.get_ParamName())) {
                throw new AssertionError("Null Double parameter changed");
            }
        }
        SerializationInfo objects = new SerializationInfo(dbnullType, selectedConverter);
        Object objectMarker = new Object();
        objects.AddValue("item", objectMarker);
        objects.AddValue("empty", (Object) null);
        objects.AddValue("typedEmpty", null, Type.GetType("System.String"));
        SerializationInfoEnumerator objectEntries = objects.GetEnumerator();
        if (objects.get_MemberCount() != 3
                || objects.GetValue("item", Type.GetType("System.Object")) != objectMarker
                || objects.GetValue("empty", Type.GetType("System.Object")) != null
                || objects.GetValue("empty", Type.GetType("System.String")) != null
                || objects.GetString("typedEmpty") != null
                || !objectEntries.MoveNext()
                || !"System.Object".equals(objectEntries.get_ObjectType().get_FullName())
                || !objectEntries.MoveNext()
                || !"System.Object".equals(objectEntries.get_ObjectType().get_FullName())
                || !objectEntries.MoveNext()
                || !"System.String".equals(objectEntries.get_ObjectType().get_FullName())) {
            throw new AssertionError("Selected object serialization members changed");
        }
        SerializationInfo getValueTypes = new SerializationInfo(dbnullType, selectedConverter);
        Object typeMarker = new Object();
        getValueTypes.AddValue("text", "hello");
        getValueTypes.AddValue("marker", typeMarker);
        if (!"hello".equals(getValueTypes.GetValue("text", Type.GetType("System.Object")))
                || !"hello".equals(getValueTypes.GetValue("text", Type.GetType("System.IComparable")))
                || getValueTypes.GetValue("marker", Type.GetType("System.Object")) != typeMarker) {
            throw new AssertionError("Assignable serialization GetValue changed");
        }
        try {
            getValueTypes.GetValue("marker", Type.GetType("System.String"));
            throw new AssertionError("Incompatible marker conversion was accepted");
        } catch (InvalidCastException expected) {
            // Pinned selected CLR failure type.
        }
        try {
            getValueTypes.GetValue(null, Type.GetType("System.Object"));
            throw new AssertionError("Null GetValue name was accepted");
        } catch (ArgumentNullException expected) {
            if (!"name".equals(expected.get_ParamName())) {
                throw new AssertionError("Null GetValue name parameter changed");
            }
        }
        SerializationInfo namedMembers = new SerializationInfo(dbnullType, selectedConverter);
        namedMembers.AddValue("", 1);
        namedMembers.AddValue("Name", 2);
        namedMembers.AddValue("name", 3);
        if (namedMembers.get_MemberCount() != 3 || namedMembers.GetInt32("") != 1
                || namedMembers.GetInt32("Name") != 2
                || namedMembers.GetInt32("name") != 3) {
            throw new AssertionError("Selected serialization member names changed");
        }
        try {
            namedMembers.AddValue("Name", 4);
            throw new AssertionError("Duplicate case-sensitive member was accepted");
        } catch (SerializationException expected) {
            // Pinned selected CLR failure type.
        }
        try {
            namedMembers.GetInt32("NAME");
            throw new AssertionError("Wrong-case member lookup was accepted");
        } catch (SerializationException expected) {
            // Pinned selected CLR failure type.
        }
        SerializationInfoEnumerator resetCycles = namedMembers.GetEnumerator();
        if (!resetCycles.MoveNext() || !"".equals(resetCycles.get_Name())) {
            throw new AssertionError("First reset-cycle member changed");
        }
        resetCycles.Reset();
        assertEnumeratorOutsideMember(resetCycles);
        if (!resetCycles.MoveNext() || !"".equals(resetCycles.get_Name())
                || !resetCycles.MoveNext() || !"Name".equals(resetCycles.get_Name())
                || !resetCycles.MoveNext() || !"name".equals(resetCycles.get_Name())
                || resetCycles.MoveNext()) {
            throw new AssertionError("Serialization reset cycle order changed");
        }
        resetCycles.Reset();
        if (!resetCycles.MoveNext() || !"".equals(resetCycles.get_Name())) {
            throw new AssertionError("Second serialization reset changed");
        }
        while (cursorBoundary.MoveNext()) {
            // Traverse both selected members.
        }
        if (cursorBoundary.MoveNext()) {
            throw new AssertionError("Exhausted serialization cursor advanced");
        }
        assertEnumeratorOutsideMember(cursorBoundary);
        SerializationInfo typedMembers = new SerializationInfo(dbnullType, selectedConverter);
        typedMembers.AddValue("text", "17", Type.GetType("System.String"));
        typedMembers.AddValue("typed", 42, Type.GetType("System.Object"));
        SerializationInfoEnumerator typedEntries = typedMembers.GetEnumerator();
        if (typedMembers.get_MemberCount() != 2 || typedMembers.GetInt32("text") != 17
                || !Integer.valueOf(17).equals(typedMembers.GetValue("text", Type.GetType("System.Int32")))
                || !Integer.valueOf(42).equals(typedMembers.GetValue("typed", Type.GetType("System.Object")))
                || !typedEntries.MoveNext()
                || !"System.String".equals(typedEntries.get_ObjectType().get_FullName())
                || !typedEntries.MoveNext()
                || !"System.Object".equals(typedEntries.get_ObjectType().get_FullName())) {
            throw new AssertionError("Selected typed serialization members changed");
        }
        try {
            typedMembers.AddValue("bad", 1, null);
            throw new AssertionError("Null declared member type was accepted");
        } catch (ArgumentNullException expected) {
            if (!"type".equals(expected.get_ParamName())) {
                throw new AssertionError("Null declared member type parameter changed");
            }
        }
        try {
            typedMembers.GetValue("text", null);
            throw new AssertionError("Null requested member type was accepted");
        } catch (ArgumentNullException expected) {
            if (!"type".equals(expected.get_ParamName())) {
                throw new AssertionError("Null requested member type parameter changed");
            }
        }
        SerializationInfo boundaryMembers = new SerializationInfo(dbnullType, selectedConverter);
        boundaryMembers.AddValue("number", 42);
        boundaryMembers.AddValue("bad", "oops");
        boundaryMembers.AddValue("empty", null, Type.GetType("System.String"));
        if (!"42".equals(boundaryMembers.GetValue("number", Type.GetType("System.String")))
                || boundaryMembers.GetString("empty") != null
                || boundaryMembers.GetValue("empty", Type.GetType("System.String")) != null) {
            throw new AssertionError("Selected serialization conversion boundaries changed");
        }
        try {
            boundaryMembers.GetInt32("bad");
            throw new AssertionError("Malformed serialized integer was accepted");
        } catch (FormatException expected) {
            // Matches the pinned selected CLR failure type.
        }
        try {
            boundaryMembers.GetValue("number", Type.GetType("System.DateTime"));
            throw new AssertionError("Incompatible serialized type was accepted");
        } catch (InvalidCastException expected) {
            // Matches the pinned selected CLR failure type.
        }
        try {
            boundaryMembers.GetInt32("empty");
            throw new AssertionError("Null serialized integer was accepted");
        } catch (ArgumentNullException expected) {
            // Matches the pinned selected CLR failure type.
        }
        SerializationInfo metadata = new SerializationInfo(dbnullType, selectedConverter);
        String corelibName = "System.Private.CoreLib, Version=10.0.0.0, "
                + "Culture=neutral, PublicKeyToken=7cec85d7bea7798e";
        if (!"System.DBNull".equals(metadata.get_FullTypeName())
                || !corelibName.equals(metadata.get_AssemblyName())
                || metadata.get_IsFullTypeNameSetExplicit()
                || metadata.get_IsAssemblyNameSetExplicit()) {
            throw new AssertionError("Initial serialization type metadata changed");
        }
        metadata.SetType(Type.GetType("System.String"));
        if (!"System.String".equals(metadata.get_ObjectType().get_FullName())
                || !"System.String".equals(metadata.get_FullTypeName())
                || !corelibName.equals(metadata.get_AssemblyName())
                || metadata.get_IsFullTypeNameSetExplicit()
                || metadata.get_IsAssemblyNameSetExplicit()) {
            throw new AssertionError("SetType serialization metadata changed");
        }
        metadata.set_FullTypeName("custom.Record");
        metadata.set_AssemblyName("custom.assembly");
        if (!"custom.Record".equals(metadata.get_FullTypeName())
                || !"custom.assembly".equals(metadata.get_AssemblyName())
                || !metadata.get_IsFullTypeNameSetExplicit()
                || !metadata.get_IsAssemblyNameSetExplicit()) {
            throw new AssertionError("Explicit serialization metadata changed");
        }
        try {
            metadata.SetType(null);
            throw new AssertionError("Null serialization type was accepted");
        } catch (ArgumentNullException expected) {
            if (!"type".equals(expected.get_ParamName())) {
                throw new AssertionError("Null serialization type parameter changed");
            }
        }
        SerializationInfo names = new SerializationInfo(dbnullType, selectedConverter);
        try {
            names.set_FullTypeName(null);
            throw new AssertionError("Null serialization full name was accepted");
        } catch (ArgumentNullException expected) {
            if (!"value".equals(expected.get_ParamName())) {
                throw new AssertionError("Null serialization full name parameter changed");
            }
        }
        try {
            names.set_AssemblyName(null);
            throw new AssertionError("Null serialization assembly name was accepted");
        } catch (ArgumentNullException expected) {
            if (!"value".equals(expected.get_ParamName())) {
                throw new AssertionError("Null serialization assembly name parameter changed");
            }
        }
        names.set_FullTypeName("");
        names.set_AssemblyName("");
        if (!"".equals(names.get_FullTypeName()) || !"".equals(names.get_AssemblyName())
                || !names.get_IsFullTypeNameSetExplicit()
                || !names.get_IsAssemblyNameSetExplicit()) {
            throw new AssertionError("Empty serialization names changed");
        }
        SerializationInfo typeReset = new SerializationInfo(dbnullType, selectedConverter);
        typeReset.set_FullTypeName("custom.Record");
        typeReset.set_AssemblyName("custom.assembly");
        typeReset.SetType(dbnullType);
        if (!"custom.Record".equals(typeReset.get_FullTypeName())
                || !"custom.assembly".equals(typeReset.get_AssemblyName())
                || !typeReset.get_IsFullTypeNameSetExplicit()
                || !typeReset.get_IsAssemblyNameSetExplicit()) {
            throw new AssertionError("Same-type serialization metadata changed");
        }
        typeReset.SetType(Type.GetType("System.String"));
        if (!"System.String".equals(typeReset.get_ObjectType().get_FullName())
                || !"System.String".equals(typeReset.get_FullTypeName())
                || !corelibName.equals(typeReset.get_AssemblyName())
                || typeReset.get_IsFullTypeNameSetExplicit()
                || typeReset.get_IsAssemblyNameSetExplicit()) {
            throw new AssertionError("Different-type serialization metadata reset changed");
        }
        Type contextStatesType = Type.fromJavaClass(StreamingContextStates.class);
        StreamingContext defaultContext = new StreamingContext();
        StreamingContext processContext = new StreamingContext(StreamingContextStates.CrossProcess);
        StreamingContext markerContext = new StreamingContext(StreamingContextStates.Other, "marker");
        if (Type.GetType("System.Runtime.Serialization.StreamingContextStates") != contextStatesType
                || !contextStatesType.get_IsEnum()
                || contextStatesType.GetEnumNames().length != 9
                || defaultContext.get_State().get_Value() != 0
                || defaultContext.get_Context() != null
                || processContext.get_State() != StreamingContextStates.CrossProcess
                || processContext.get_Context() != null
                || markerContext.get_State() != StreamingContextStates.Other
                || !"marker".equals(markerContext.get_Context())) {
            throw new AssertionError("Selected StreamingContext state changed");
        }
        Object sharedContextMarker = new Object();
        StreamingContext sameA = new StreamingContext(StreamingContextStates.Other,
                sharedContextMarker);
        StreamingContext sameB = new StreamingContext(StreamingContextStates.Other,
                sharedContextMarker);
        if (!defaultContext.Equals(new StreamingContext())
                || !sameA.Equals(sameB) || !sameA.equals(sameB)
                || sameA.GetHashCode() != sameB.GetHashCode()
                || sameA.Equals(new StreamingContext(StreamingContextStates.Other, new Object()))
                || sameA.Equals(new StreamingContext(StreamingContextStates.CrossProcess,
                    sharedContextMarker))
                || !"System.Runtime.Serialization.StreamingContext".equals(sameA.ToString())
                || !"System.Runtime.Serialization.StreamingContext".equals(
                    defaultContext.toString())) {
            throw new AssertionError("Selected StreamingContext equality changed");
        }
        try {
            ((ISerializable) DBNull.Value).GetObjectData(null, new StreamingContext());
            throw new AssertionError("Null DBNull serialization info was accepted");
        } catch (NullReferenceException expected) {
            // Pinned null-info failure type.
        }
        if (!convertibleType.IsAssignableFrom(dbnullType)
                || !convertibleType.IsInstanceOfType(DBNull.Value)
                || dbnullType.GetInterface("System.IConvertible") != convertibleType
                || dbnullType.GetInterface("system.iconvertible") != null
                || dbnullType.GetInterface("system.iconvertible", true) != convertibleType) {
            throw new AssertionError("Selected DBNull IConvertible metadata changed");
        }
        if (!"".equals(convertibleNull.ToType(Type.fromJavaClass(String.class), null))
                || convertibleNull.ToType(Type.fromJavaClass(DBNull.class), null) != DBNull.Value) {
            throw new AssertionError("Selected DBNull ToType outcomes changed");
        }
        try {
            convertibleNull.ToType(null, null);
            throw new AssertionError("Null DBNull target type was accepted");
        } catch (ArgumentNullException expected) {
            if (!"targetType".equals(expected.get_ParamName())) {
                throw new AssertionError("Null DBNull target parameter changed");
            }
        }
        Runnable[] invalidDbNullConversions = {
            () -> convertibleNull.ToBoolean(null),
            () -> convertibleNull.ToChar(null),
            () -> convertibleNull.ToSByte(null),
            () -> convertibleNull.ToByte(null),
            () -> convertibleNull.ToInt16(null),
            () -> convertibleNull.ToUInt16(null),
            () -> convertibleNull.ToInt32(null),
            () -> convertibleNull.ToUInt32(null),
            () -> convertibleNull.ToInt64(null),
            () -> convertibleNull.ToUInt64(null),
            () -> convertibleNull.ToSingle(null),
            () -> convertibleNull.ToDouble(null),
            () -> convertibleNull.ToDecimal(null),
            () -> convertibleNull.ToDateTime(null)
        };
        for (Runnable conversion : invalidDbNullConversions) {
            try {
                conversion.run();
                throw new AssertionError("DBNull numeric or date conversion succeeded");
            } catch (InvalidCastException expected) {
                // Pinned invalid cast behavior.
            }
        }
        if (string.get_IsCollectible()
                || Type.fromJavaClass(List.class).get_IsCollectible()) {
            throw new AssertionError("Selected type collectibility changed");
        }
        Type integer = Type.fromJavaClass(Integer.class);
        Type bindingFlagsType = Type.fromJavaClass(BindingFlags.class);
        Type callingConventionType = Type.fromJavaClass(CallingConventions.class);
        Type implementationType = Type.fromJavaClass(MethodImplAttributes.class);
        if (Type.GetType("System.Reflection.MethodImplAttributes") != implementationType
                || !implementationType.get_IsEnum()
                || implementationType.GetEnumValues().getClass() != MethodImplAttributes[].class
                || implementationType.GetEnumNames().length != 18
                || MethodImplAttributes.IL.get_Value() != 0
                || MethodImplAttributes.Managed.get_Value() != 0
                || MethodImplAttributes.Async.get_Value() != 8192) {
            throw new AssertionError("Pinned method implementation values changed");
        }
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
        Type parameterAttributesType = Type.fromJavaClass(ParameterAttributes.class);
        if (Type.GetType("System.Attribute") != Type.fromJavaClass(Attribute.class)
                || !Type.fromJavaClass(Attribute.class).get_IsAbstract()
                || Type.GetType("System.Runtime.CompilerServices.NullableAttribute")
                    != Type.fromJavaClass(NullableAttribute.class)
                || Type.fromJavaClass(NullableAttribute.class).get_BaseType()
                    != Type.fromJavaClass(Attribute.class)) {
            throw new AssertionError("Selected attribute hierarchy changed");
        }
        byte[] nullableFlags = { 1, 2 };
        NullableAttribute nullableArray = new NullableAttribute(nullableFlags);
        if (nullableArray.NullableFlags != nullableFlags) {
            throw new AssertionError("Nullable array constructor lost array identity");
        }
        nullableFlags[0] = 3;
        if (nullableArray.NullableFlags[0] != 3 || nullableArray.NullableFlags[1] != 2) {
            throw new AssertionError("Nullable array constructor mutation behavior changed");
        }
        if (Type.GetType("System.Reflection.ParameterAttributes") != parameterAttributesType
                || !parameterAttributesType.get_IsEnum()
                || parameterAttributesType.GetEnumNames().length != 11
                || ParameterAttributes.None.get_Value() != 0
                || ParameterAttributes.ReservedMask.get_Value() != 61440) {
            throw new AssertionError("Pinned ParameterAttributes values changed");
        }
        Type methodBodyType = Type.fromJavaClass(MethodBody.class);
        if (Type.GetType("System.Reflection.MethodBody") != methodBodyType
                || methodBodyType.get_BaseType() != Type.fromJavaClass(Object.class)
                || methodBodyType.get_IsAbstract()) {
            throw new AssertionError("Selected MethodBody identity changed");
        }
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
        String[] interfaceMethodTexts = {
            "Void Dispose()", "Int32 CompareTo(System.Object)",
            "System.String ToString(System.String, System.IFormatProvider)",
            "System.Object GetFormat(System.Type)"
        };
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
        String[][] interfaceParameterTexts = {
            {"Void"}, {"System.Object obj", "Int32"},
            {"System.String format", "System.IFormatProvider formatProvider", "System.String "},
            {"System.Type formatType", "System.Object"}
        };
        for (int index = 0; index < interfaceOwners.length; index++) {
            Type owner = interfaceOwners[index];
            MemberInfo[] members = owner.GetMembers();
            if (!members[0].HasSameMetadataDefinitionAs(
                    owner.GetMethod(interfaceMethodNames[index]))
                    || members[0].HasSameMetadataDefinitionAs(
                        Type.fromJavaClass(String.class))) {
                throw new AssertionError("Selected method metadata identity changed");
            }
            if (index == 0) {
                if (members[0].HasSameMetadataDefinitionAs(
                        Type.fromJavaClass(IComparable.class).GetMethod("CompareTo"))) {
                    throw new AssertionError("Distinct methods share metadata identity");
                }
                try {
                    members[0].HasSameMetadataDefinitionAs(null);
                    throw new AssertionError("Null member metadata comparison was accepted");
                } catch (ArgumentNullException expected) {
                    if (!"other".equals(expected.get_ParamName())) {
                        throw new AssertionError("Null member comparison parameter changed");
                    }
                }
            }
            if (members.length != 1
                    || !interfaceMethodNames[index].equals(members[0].get_Name())
                    || members[0].get_MemberType() != MemberTypes.Method
                    || members[0].get_DeclaringType() != owner
                    || members[0].get_ReflectedType() != owner
                    || members[0].get_IsCollectible()
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
                    || namedMethod.get_IsFamilyAndAssembly()
                    || namedMethod.get_IsFamilyOrAssembly()
                    || namedMethod.get_IsAssembly()
                    || !namedMethod.get_IsHideBySig()
                    || !namedMethod.get_CallingConvention().equals(standardInstance)
                    || !namedMethod.get_IsSecurityCritical()
                    || namedMethod.get_IsSecuritySafeCritical()
                    || namedMethod.get_IsSecurityTransparent()
                    || namedMethod.GetMethodImplementationFlags().get_Value() != 0
                    || namedMethod.get_IsGenericMethod()
                    || namedMethod.get_IsGenericMethodDefinition()
                    || namedMethod.get_IsConstructedGenericMethod()
                    || namedMethod.get_ContainsGenericParameters()
                    || namedMethod.GetGenericArguments().length != 0
                    || namedMethod.GetBaseDefinition() != namedMethod
                    || !interfaceMethodTexts[index].equals(namedMethod.ToString())
                    || !interfaceMethodTexts[index].equals(namedMethod.toString())
                    || namedMethod.get_ReturnType() != interfaceMethodReturns[index]
                    || owner.GetMethod(interfaceMethodNames[index]
                        .toLowerCase(java.util.Locale.ROOT)) != null
                    || owner.GetMethod("Missing") != null) {
                throw new AssertionError("Selected typed method-name lookup changed");
            }
            ParameterInfo returnParameter = namedMethod.get_ReturnParameter();
            if (namedMethod.GetCustomAttributes(false).length != 0
                    || namedMethod.GetCustomAttributes(true).length != 0
                    || namedMethod.GetCustomAttributes(Type.fromJavaClass(Attribute.class), false).length != 0
                    || namedMethod.GetCustomAttributes(Type.fromJavaClass(Attribute.class), true).length != 0
                    || namedMethod.IsDefined(Type.fromJavaClass(Attribute.class), false)
                    || namedMethod.IsDefined(Type.fromJavaClass(Attribute.class), true)
                    || namedMethod.GetCustomAttributes(false)
                        == namedMethod.GetCustomAttributes(false)) {
                throw new AssertionError("Selected method custom attributes changed");
            }
            try {
                namedMethod.GetCustomAttributes(null, false);
                throw new AssertionError("Null method attribute type was accepted");
            } catch (ArgumentNullException expected) {
                if (!"attributeType".equals(expected.get_ParamName())) {
                    throw new AssertionError("Null method attribute type parameter changed");
                }
            }
            try {
                namedMethod.IsDefined(null, false);
                throw new AssertionError("Null method IsDefined type was accepted");
            } catch (ArgumentNullException expected) {
                if (!"attributeType".equals(expected.get_ParamName())) {
                    throw new AssertionError("Null method IsDefined parameter changed");
                }
            }
            Object[] returnAttributes = returnParameter.GetCustomAttributes(false);
            Object[] inheritedReturnAttributes = returnParameter.GetCustomAttributes(true);
            Object[] filteredReturnAttributes = returnParameter.GetCustomAttributes(
                    Type.fromJavaClass(Attribute.class), false);
            if (index == 2) {
                if (returnAttributes.length != 1
                        || inheritedReturnAttributes.length != 1
                        || filteredReturnAttributes.length != 1
                        || !(returnAttributes[0] instanceof NullableAttribute annotation)
                        || annotation.NullableFlags.length != 1
                        || annotation.NullableFlags[0] != 1
                        || returnAttributes[0] == inheritedReturnAttributes[0]
                        || !annotation.Equals(inheritedReturnAttributes[0])
                        || !annotation.Match(inheritedReturnAttributes[0])
                        || annotation.get_TypeId()
                            != Type.fromJavaClass(NullableAttribute.class)
                        || annotation.IsDefaultAttribute()
                        || !(inheritedReturnAttributes[0] instanceof NullableAttribute)) {
                    throw new AssertionError("Selected nullable return attribute changed");
                }
            } else if (returnAttributes.length != 0 || inheritedReturnAttributes.length != 0
                    || filteredReturnAttributes.length != 0) {
                throw new AssertionError("Unexpected selected return attribute");
            }
            if (index == 2) {
                if (returnParameter.GetCustomAttributes(
                        Type.fromJavaClass(NullableAttribute.class), true).length != 1
                        || !returnParameter.IsDefined(Type.fromJavaClass(Attribute.class), false)
                        || !returnParameter.IsDefined(Type.fromJavaClass(NullableAttribute.class), true)
                        || namedMethod.GetParameters()[0].IsDefined(
                            Type.fromJavaClass(Attribute.class), false)
                        || namedMethod.GetParameters()[0].GetCustomAttributes(
                            Type.fromJavaClass(Attribute.class), false).length != 0) {
                    throw new AssertionError("Selected attribute type filtering changed");
                }
                try {
                    returnParameter.GetCustomAttributes(null, false);
                    throw new AssertionError("Null attribute type was accepted");
                } catch (ArgumentNullException expected) {
                    if (!"attributeType".equals(expected.get_ParamName())) {
                        throw new AssertionError("Null attribute type parameter changed");
                    }
                }
                try {
                    returnParameter.IsDefined(null, false);
                    throw new AssertionError("Null IsDefined attribute type was accepted");
                } catch (ArgumentNullException expected) {
                    if (!"attributeType".equals(expected.get_ParamName())) {
                        throw new AssertionError("Null IsDefined parameter changed");
                    }
                }
            }
            if (namedMethod.GetMethodBody() != null) {
                throw new AssertionError("Abstract interface method supplied a body");
            }
            try {
                namedMethod.GetGenericMethodDefinition();
                throw new AssertionError("Nongeneric method supplied a generic definition");
            } catch (InvalidOperationException expected) {
                // Pinned nongeneric operation error.
            }
            try {
                namedMethod.MakeGenericMethod(new Type[0]);
                throw new AssertionError("Nongeneric method accepted generic arguments");
            } catch (InvalidOperationException expected) {
                // Pinned nongeneric operation error.
            }
            try {
                namedMethod.MakeGenericMethod(null);
                throw new AssertionError("Null method instantiation was accepted");
            } catch (ArgumentNullException expected) {
                if (!"methodInstantiation".equals(expected.get_ParamName())) {
                    throw new AssertionError("Null method instantiation parameter changed");
                }
            }
            try {
                namedMethod.MakeGenericMethod(new Type[] { Type.fromJavaClass(String.class) });
                throw new AssertionError("Nongeneric method accepted a type argument");
            } catch (InvalidOperationException expected) {
                // Pinned nongeneric operation error.
            }
            if (returnParameter.get_ParameterType() != interfaceMethodReturns[index]
                    || returnParameter.get_Member() != namedMethod
                    || returnParameter.get_Position() != -1
                    || returnParameter.get_IsOptional()
                    || returnParameter.get_HasDefaultValue()
                    || returnParameter.get_DefaultValue() != DBNull.Value
                    || returnParameter.get_RawDefaultValue() != DBNull.Value
                    || returnParameter.get_IsIn() || returnParameter.get_IsOut()
                    || returnParameter.get_IsRetval() || returnParameter.get_IsLcid()
                    || returnParameter.get_Attributes() != ParameterAttributes.None
                    || returnParameter.GetOptionalCustomModifiers().length != 0
                    || returnParameter.GetRequiredCustomModifiers().length != 0
                    || !java.util.Objects.equals(returnParameter.get_Name(),
                        index == 2 ? "" : null)
                    || !interfaceParameterTexts[index][interfaceParameterTexts[index].length - 1]
                        .equals(returnParameter.ToString())
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
                        || parameters[parameterIndex].get_Member() != namedMethod
                        || parameters[parameterIndex].get_ParameterType()
                            != interfaceMethodParameters[index][parameterIndex]
                        || parameters[parameterIndex].get_Position() != parameterIndex) {
                    throw new AssertionError("Selected method parameter metadata changed");
                }
                if (!interfaceParameterTexts[index][parameterIndex]
                        .equals(parameters[parameterIndex].ToString())) {
                    throw new AssertionError("Selected parameter signature text changed");
                }
                if (parameters[parameterIndex].get_IsOptional()
                        || parameters[parameterIndex].get_HasDefaultValue()
                        || parameters[parameterIndex].get_DefaultValue() != DBNull.Value
                        || parameters[parameterIndex].get_RawDefaultValue() != DBNull.Value
                        || parameters[parameterIndex].get_IsIn()
                        || parameters[parameterIndex].get_IsOut()
                        || parameters[parameterIndex].get_IsRetval()
                        || parameters[parameterIndex].get_IsLcid()
                        || parameters[parameterIndex].get_Attributes() != ParameterAttributes.None
                        || parameters[parameterIndex].GetCustomAttributes(false).length != 0
                        || parameters[parameterIndex].GetCustomAttributes(true).length != 0
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
                    || !defaults[0].HasSameMetadataDefinitionAs(
                        defaultOwner.GetDefaultMembers()[0])
                    || defaults[0].get_MemberType() != MemberTypes.Property
                    || defaults[0].get_DeclaringType() != defaultOwner
                    || defaults[0].get_ReflectedType() != defaultOwner
                    || defaults[0].get_IsCollectible()
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

    private static void assertEnumeratorOutsideMember(SerializationInfoEnumerator cursor) {
        try {
            cursor.get_Current();
            throw new AssertionError("Current was available outside a member");
        } catch (InvalidOperationException expected) {
            // Pinned selected CLR failure type.
        }
        try {
            cursor.get_Name();
            throw new AssertionError("Name was available outside a member");
        } catch (InvalidOperationException expected) {
            // Pinned selected CLR failure type.
        }
        try {
            cursor.get_ObjectType();
            throw new AssertionError("ObjectType was available outside a member");
        } catch (InvalidOperationException expected) {
            // Pinned selected CLR failure type.
        }
        try {
            cursor.get_Value();
            throw new AssertionError("Value was available outside a member");
        } catch (InvalidOperationException expected) {
            // Pinned selected CLR failure type.
        }
    }

    private static SerializationEntry serializationEntry(Object value, Type declaredType) {
        SerializationInfo info = new SerializationInfo(Type.GetType("System.DBNull"),
                new FormatterConverter());
        info.AddValue("item", value, declaredType);
        SerializationInfoEnumerator cursor = info.GetEnumerator();
        cursor.MoveNext();
        return cursor.get_Current();
    }
}
