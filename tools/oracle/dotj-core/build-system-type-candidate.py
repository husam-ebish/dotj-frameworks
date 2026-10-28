"""Build the bounded System.Type identity candidate against pinned metadata."""

import hashlib
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE_ROOT = ROOT / "planning/stage-2/repos/dotj-core/evidence"
SNAPSHOT = EVIDENCE_ROOT / "api-shapes-v10.0.12/system-type.json"
PROVENANCE = SNAPSHOT.with_name("system-type-provenance.json")
SOURCE = ROOT / "dotj-core/dotj-core-public/src/main/java/System/Type.java"
EXCEPTION_SOURCES = [SOURCE.with_name(name + ".java") for name in
                     ("Exception", "SystemException", "ArgumentException", "ArgumentNullException", "ArgumentOutOfRangeException", "ArithmeticException", "DivideByZeroException", "ValueTuple", "TypeLoadException", "IndexOutOfRangeException", "OverflowException", "InvalidCastException", "InvalidOperationException", "FormatException")]
EXCEPTION_SOURCES += [SOURCE.parent / "IO" / (name + ".java") for name in
                      ("IOException", "FileNotFoundException", "FileLoadException")]
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MemberInfo.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MethodBase.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MethodBody.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MethodInfo.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/ParameterInfo.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/ParameterAttributes.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MemberTypes.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/GenericParameterAttributes.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/BindingFlags.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/CallingConventions.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MethodImplAttributes.java")
EXCEPTION_SOURCES.append(SOURCE.with_name("TypeCode.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("DBNull.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("Attribute.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("NullReferenceException.java"))
EXCEPTION_SOURCES.append(SOURCE.parent / "Runtime/CompilerServices/NullableAttribute.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Collections/IEnumerator.java")
EXCEPTION_SOURCES += [SOURCE.parent / "Collections" / (name + ".java") for name in
                      ("IEnumerable", "ICollection", "IDictionary", "IDictionaryEnumerator", "DictionaryEntry")]
EXCEPTION_SOURCES.append(ROOT / "dotj-core/dotj-core-public/src/main/java/org/dotj/internal/collections/ExceptionDataDictionary.java")
EXCEPTION_SOURCES += [SOURCE.parent / "Runtime/Serialization" / (name + ".java") for name in
                      ("FormatterConverter", "IFormatterConverter", "ISerializable", "SerializationEntry", "SerializationException", "SerializationInfo", "SerializationInfoEnumerator", "StreamingContext", "StreamingContextStates")]
EXCEPTION_SOURCES.append(SOURCE.with_name("Decimal.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("MidpointRounding.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("DateTime.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("DateTimeKind.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("DayOfWeek.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("TimeSpan.java"))
EXCEPTION_SOURCES.append(SOURCE.parent / "Globalization/TimeSpanStyles.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Globalization/DateTimeStyles.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Diagnostics/Stopwatch.java")
EXCEPTION_SOURCES.append(ROOT / "dotj-core/dotj-core-public/src/main/java/org/dotj/internal/text/MarvinStringHash.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Text/DecoderFallbackBuffer.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Text/EncoderFallbackBuffer.java")
EXCEPTION_SOURCES.append(SOURCE.with_name("OutOfMemoryException.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("NotSupportedException.java"))
EXCEPTION_SOURCES.append(SOURCE.parent / "Text/NormalizationForm.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Text/UnicodeEncoding.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Text/Decoder.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Text/Encoder.java")
EXCEPTION_SOURCES += [SOURCE.parent / "Text" / (name + ".java") for name in ('EncoderFallback', 'DecoderFallback', 'EncoderReplacementFallback', 'DecoderReplacementFallback', 'EncoderExceptionFallback', 'DecoderExceptionFallback')]
EXCEPTION_SOURCES.append(SOURCE.with_name("ICloneable.java"))
EXCEPTION_SOURCES += [SOURCE.parent / "Text" / (name + ".java") for name in ('Encoding', 'UTF8Encoding', 'EncoderFallbackException', 'DecoderFallbackException')]
EXCEPTION_SOURCES.append(ROOT / "dotj-core/dotj-core-public/src/main/java/org/dotj/internal/text/Utf8Codec.java")
EXCEPTION_SOURCES.append(SOURCE.with_name("Int32.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("ReadOnlySpan.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("Span.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("UInt16.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("UInt32.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("Byte.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("SByte.java"))
EXCEPTION_SOURCES.append(SOURCE.parent / "Globalization/NumberStyles.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Globalization/NumberFormatInfo.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Globalization/DigitShapes.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Globalization/CultureNotFoundException.java")
EXCEPTION_SOURCES.append(ROOT / "dotj-core/dotj-core-public/src/main/java/org/dotj/internal/throwing/ThrowSite.java")
IDISPOSABLE_SOURCE = SOURCE.with_name("IDisposable.java")
ICOMPARABLE_SOURCE = SOURCE.with_name("IComparable.java")
IFORMATTABLE_SOURCE = SOURCE.with_name("IFormattable.java")
IFORMATPROVIDER_SOURCE = SOURCE.with_name("IFormatProvider.java")
ISPANFORMATTABLE_SOURCE = SOURCE.with_name("ISpanFormattable.java")
IUTF8SPANFORMATTABLE_SOURCE = SOURCE.with_name("IUtf8SpanFormattable.java")
ICONVERTIBLE_SOURCE = SOURCE.with_name("IConvertible.java")
TEST = ROOT / "dotj-core/dotj-core-public/src/test/java/System/TypeIdentityCandidateTest.java"
NOT_PUBLIC_FIXTURE = ROOT / "dotj-core/dotj-core-public/src/test/java/System/PackagePrivateTypeFixture.java"
CONCURRENCY_TEST = ROOT / "dotj-core/dotj-core-public/src/test/java/System/TypeIdentityConcurrencyTest.java"
LOADER_FIXTURE = ROOT / "dotj-core/dotj-core-public/src/test/java/fixture/LoadableType.java"
EXTERNAL = ROOT / "dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java"
BUILD = ROOT / "dotj-core/dotj-core-public/build/type-identity-candidate-v2"
CLASSES = BUILD / "product-classes"
TEST_CLASSES = BUILD / "test-classes"
EVIDENCE = EVIDENCE_ROOT / "system-type-identity-candidate-v1.json"
FOUNDATION_METADATA = EVIDENCE_ROOT / "foundation-selected-metadata-v10.0.12.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"Command failed: {command[0]}\n{result.stderr}")
    return result.stdout


def main():
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    assert sha256(SNAPSHOT) == provenance["snapshotSha256"]
    dbnull = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDBNullBehavior"]
    assert dbnull == {"fullName": "System.DBNull", "sameReference": True,
                      "text": "", "providerText": "", "typeCode": "DBNull"}
    dbnull_conversions = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDBNullConversionBehavior"]
    assert dbnull_conversions["isConvertible"]
    assert all(dbnull_conversions[key] == "System.InvalidCastException" for key in (
        "toBoolean", "toChar", "toSByte", "toByte", "toInt16", "toUInt16",
        "toInt32", "toUInt32", "toInt64", "toUInt64", "toSingle", "toDouble",
        "toDecimal", "toDateTime"))
    assert dbnull_conversions["toTypeString"] is None
    assert dbnull_conversions["toTypeStringText"] == ""
    assert dbnull_conversions["toTypeSelf"] is None
    assert dbnull_conversions["toTypeSelfSameReference"]
    assert dbnull_conversions["toTypeNull"] == "System.ArgumentNullException"
    assert dbnull_conversions["toTypeNullParameter"] == "targetType"
    dbnull_interfaces = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDBNullInterfaceBehavior"]
    assert dbnull_interfaces == {
        "interfaces": ["System.Runtime.Serialization.ISerializable", "System.IConvertible"],
        "convertibleAssignable": True, "convertibleInstance": True,
        "convertibleInterface": "System.IConvertible",
    }
    serialization_contract = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDBNullSerializationContractBehavior"]
    assert serialization_contract == {
        "interfaceName": "System.Runtime.Serialization.ISerializable",
        "methodName": "GetObjectData",
        "parameterTypes": ["System.Runtime.Serialization.SerializationInfo",
                           "System.Runtime.Serialization.StreamingContext"],
        "infoBase": "System.Object", "contextBase": "System.ValueType",
        "nullInfoError": "System.NullReferenceException", "nullInfoParameter": None,
    }
    context = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedStreamingContextBehavior"]
    assert context["values"] == [
        {"name": name, "value": value} for name, value in (
            ("CrossProcess", 1), ("CrossMachine", 2), ("File", 4),
            ("Persistence", 8), ("Remoting", 16), ("Other", 32),
            ("Clone", 64), ("CrossAppDomain", 128), ("All", 255))]
    assert {key: context[key] for key in ("defaultState", "defaultContext",
        "oneArgState", "oneArgContext", "twoArgState", "twoArgContext")} == {
        "defaultState": 0, "defaultContext": None, "oneArgState": 1,
        "oneArgContext": None, "twoArgState": 32, "twoArgContext": "marker"}
    context_equality = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedStreamingContextEqualityBehavior"]
    assert context_equality == {
        "defaultEquals": True, "sameStateSameContext": True,
        "sameStateDifferentContext": False, "differentStateSameContext": False,
        "sameHash": True, "text": "System.Runtime.Serialization.StreamingContext",
        "defaultText": "System.Runtime.Serialization.StreamingContext",
    }
    info_construction = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoConstructionBehavior"]
    assert info_construction["constructors"] == [
        ["System.Type", "System.Runtime.Serialization.IFormatterConverter"],
        ["System.Type", "System.Runtime.Serialization.IFormatterConverter", "System.Boolean"],
    ]
    assert [row["name"] for row in info_construction["converterMethods"]] == [
        "Convert", "Convert", "ToBoolean", "ToByte", "ToChar", "ToDateTime",
        "ToDecimal", "ToDouble", "ToInt16", "ToInt32", "ToInt64", "ToSByte",
        "ToSingle", "ToString", "ToUInt16", "ToUInt32", "ToUInt64",
    ]
    assert info_construction["objectType"] == info_construction["fullTypeName"] == "System.DBNull"
    assert info_construction["memberCount"] == 0
    assert info_construction["threeArgType"] == "System.DBNull"
    assert info_construction["nullTypeError"] == "System.ArgumentNullException"
    assert info_construction["nullTypeParameter"] == "type"
    assert info_construction["nullConverterError"] == "System.ArgumentNullException"
    assert info_construction["nullConverterParameter"] == "converter"
    formatter = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedFormatterConverterBehavior"]
    assert formatter == {
        "constructorCount": 1,
        "interfaceName": "System.Runtime.Serialization.IFormatterConverter",
        "integer": 42, "stringInteger": 17, "integerText": "42",
        "integerBoolean": True, "byType": 17, "byTypeCode": 17,
        "nullIntegerError": "System.ArgumentNullException",
        "nullIntegerParameter": "value",
        "badIntegerError": "System.FormatException",
    }
    info_members = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoMembersBehavior"]
    assert info_members == {
        "count": 2, "age": 42, "name": "Ada", "ageByType": 42,
        "nullAddError": "System.ArgumentNullException", "nullAddParameter": "name",
        "nullGetError": "System.ArgumentNullException", "nullGetParameter": "name",
        "duplicateError": "System.Runtime.Serialization.SerializationException",
        "missingError": "System.Runtime.Serialization.SerializationException",
        "exceptionBase": "System.SystemException",
    }
    enumeration = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoEnumerationBehavior"]
    assert enumeration == {
        "enumeratorType": "System.Runtime.Serialization.SerializationInfoEnumerator",
        "entryType": "System.Runtime.Serialization.SerializationEntry",
        "entries": [
            {"name": "age", "type": "System.Int32", "value": "42", "currentName": "age"},
            {"name": "name", "type": "System.String", "value": "Ada", "currentName": "name"},
        ],
        "afterReset": "age",
    }
    typed_members = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoTypedValuesBehavior"]
    assert typed_members == {
        "count": 2, "parsed": 17, "parsedByType": 17, "typedValue": 42,
        "firstType": "System.String", "secondType": "System.Object",
        "nullAddTypeError": "System.ArgumentNullException",
        "nullAddTypeParameter": "type",
        "nullGetTypeError": "System.ArgumentNullException",
        "nullGetTypeParameter": "type",
    }
    conversion_boundaries = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoConversionBoundariesBehavior"]
    assert conversion_boundaries == {
        "numberAsString": "42", "nullString": None, "nullValue": None,
        "badIntError": "System.FormatException",
        "incompatibleError": "System.InvalidCastException",
        "nullIntError": "System.ArgumentNullException",
    }
    type_metadata = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoTypeMetadataBehavior"]
    corelib_name = "System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e"
    assert type_metadata == {
        "initialType": "System.DBNull", "initialFullName": "System.DBNull",
        "initialAssemblyName": corelib_name,
        "initialFullNameExplicit": False, "initialAssemblyNameExplicit": False,
        "afterSetType": {"objectType": "System.String", "fullTypeName": "System.String",
                         "assemblyName": corelib_name, "fullNameExplicit": False,
                         "assemblyNameExplicit": False},
        "customFullName": "custom.Record", "customAssemblyName": "custom.assembly",
        "customFullNameExplicit": True, "customAssemblyNameExplicit": True,
        "nullSetTypeError": "System.ArgumentNullException",
        "nullSetTypeParameter": "type",
    }
    name_validation = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoNameValidationBehavior"]
    assert name_validation == {
        "nullFullError": "System.ArgumentNullException", "nullFullParameter": "value",
        "emptyFullError": None,
        "nullAssemblyError": "System.ArgumentNullException", "nullAssemblyParameter": "value",
        "emptyAssemblyError": None,
        "fullNameAfterErrors": "", "assemblyNameAfterErrors": "",
        "fullExplicitAfterErrors": True, "assemblyExplicitAfterErrors": True,
    }
    settype_reset = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoSetTypeResetBehavior"]
    assert settype_reset == {
        "sameType": {"fullName": "custom.Record", "assemblyName": "custom.assembly",
                     "fullExplicit": True, "assemblyExplicit": True},
        "differentType": {"objectType": "System.String", "fullName": "System.String",
                          "assemblyName": corelib_name,
                          "fullExplicit": False, "assemblyExplicit": False},
    }
    cursor_boundaries = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoEnumeratorBoundariesBehavior"]
    assert cursor_boundaries == {
        "beforeCurrent": "System.InvalidOperationException",
        "beforeName": "System.InvalidOperationException",
        "beforeType": "System.InvalidOperationException",
        "beforeValue": "System.InvalidOperationException",
        "firstMove": True, "secondMove": False, "thirdMove": False,
        "afterCurrent": "System.InvalidOperationException",
        "afterName": "System.InvalidOperationException",
        "afterType": "System.InvalidOperationException",
        "afterValue": "System.InvalidOperationException",
    }
    mutation = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoEnumeratorMutationBehavior"]
    assert mutation == {"memberCount": 2, "observed": ["first"],
                        "afterReset": ["first"], "freshNames": ["first", "second"]}
    empty_enumeration = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEmptySerializationInfoEnumerationBehavior"]
    assert empty_enumeration == {
        "firstMove": False, "afterReset": False, "afterAdd": False,
        "emptyCurrentError": "System.InvalidOperationException",
        "memberCount": 1, "freshMove": True, "freshName": "added",
    }
    primitive_members = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoPrimitiveMembersBehavior"]
    assert primitive_members == {"count": 3, "flag": True, "large": 5000000000,
                                 "ratio": 1.5,
                                 "types": ["System.Boolean", "System.Int64", "System.Double"]}
    primitive_conversions = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoPrimitiveConversionsBehavior"]
    assert primitive_conversions == {
        "oneAsBoolean": True, "integerTextAsLong": 17,
        "decimalTextAsDouble": 1.5, "longAsInt": 5,
        "integerTextByType": 17, "decimalTextByTypeCode": 1.5,
    }
    primitive_errors = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPrimitiveConversionErrorsBehavior"]
    assert primitive_errors == {
        "malformedLong": "System.FormatException",
        "overflowLong": "System.OverflowException",
        "overflowInt": "System.OverflowException",
        "malformedDouble": "System.FormatException",
        "nullLong": "System.ArgumentNullException", "nullLongParameter": "value",
        "nullDouble": "System.ArgumentNullException", "nullDoubleParameter": "value",
    }
    object_members = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoObjectMembersBehavior"]
    assert object_members == {
        "count": 3, "markerSame": True,
        "emptyObject": None, "emptyString": None, "typedEmptyString": None,
        "types": ["System.Object", "System.Object", "System.String"],
    }
    getvalue_types = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoGetValueTypesBehavior"]
    assert getvalue_types == {
        "textAsObject": "hello", "textAsComparable": "hello",
        "markerAsObjectSame": True,
        "markerAsStringError": "System.InvalidCastException",
        "nullNameError": "System.ArgumentNullException",
        "nullNameParameter": "name",
    }
    member_names = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoMemberNamesBehavior"]
    assert member_names == {
        "count": 3, "empty": 1, "uppercase": 2, "lowercase": 3,
        "duplicateError": "System.Runtime.Serialization.SerializationException",
        "wrongCaseError": "System.Runtime.Serialization.SerializationException",
    }
    reset_cycles = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoEnumeratorResetCyclesBehavior"]
    assert reset_cycles == {
        "firstName": "first", "currentAfterReset": "System.InvalidOperationException",
        "firstAfterReset": "first", "secondAfterReset": "second",
        "exhausted": False, "firstAfterSecondReset": "first",
    }
    cursor_interface = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoEnumeratorInterfaceBehavior"]
    assert cursor_interface == {
        "interfaces": ["System.Collections.IEnumerator"],
        "declaredMethods": [
            {"name": "get_Current", "result": "System.Runtime.Serialization.SerializationEntry"},
            {"name": "get_Name", "result": "System.String"},
            {"name": "get_ObjectType", "result": "System.Type"},
            {"name": "get_Value", "result": "System.Object"},
            {"name": "MoveNext", "result": "System.Boolean"},
            {"name": "Reset", "result": "System.Void"},
        ],
        "currentType": "System.Runtime.Serialization.SerializationEntry",
        "assignable": True, "instance": True,
    }
    entry_shape = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationEntryShapeBehavior"]
    assert entry_shape == {
        "baseType": "System.ValueType", "isValueType": True,
        "publicConstructorCount": 0,
        "properties": [
            {"name": "Name", "type": "System.String"},
            {"name": "ObjectType", "type": "System.Type"},
            {"name": "Value", "type": "System.Object"},
        ],
        "defaultName": None, "defaultObjectType": None, "defaultValue": None,
    }
    entry_value = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationEntryValueSnapshotBehavior"]
    assert entry_value == {
        "entryName": "values",
        "entryType": "System.Collections.Generic.List`1[[System.Int32, System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e]]",
        "sameValueReference": True, "updatedValueCount": 2,
        "entryNameAfterAdd": "values", "cursorHasSecond": False,
        "freshMemberCount": 2,
    }
    entry_equality = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationEntryEqualityBehavior"]
    assert entry_equality == {
        "equalEntries": True, "equalHashes": True,
        "differentNameEqual": False, "differentValueEqual": False,
        "defaultEqual": True,
        "defaultText": "System.Runtime.Serialization.SerializationEntry",
        "populatedText": "System.Runtime.Serialization.SerializationEntry",
    }
    entry_type_equality = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationEntryTypeEqualityBehavior"]
    assert entry_type_equality == {
        "differentDeclaredTypeEqual": False, "differentValueEqual": False,
        "sameNullEqual": True, "sameNullHash": True,
        "nullVersusTextEqual": False,
    }
    duplicate_state = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoDuplicateStateBehavior"]
    assert duplicate_state == {
        "duplicateError": "System.Runtime.Serialization.SerializationException",
        "count": 1, "original": 42, "enumeratedValue": 42,
        "secondMove": False,
    }
    value_overloads = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoValueOverloadsBehavior"]
    assert value_overloads == {
        "count": 4, "character": "Q", "single": 1.25,
        "decimalText": "12", "date": "2024-02-29",
        "types": ["System.Char", "System.Single", "System.Decimal", "System.DateTime"],
    }
    numeric_overloads = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoNumericOverloadsBehavior"]
    assert numeric_overloads == {
        "count": 2, "signed": -1234,
        "unsignedText": "18446744073709551615",
        "types": ["System.Int16", "System.UInt64"],
        "unsignedTypeCode": "UInt64",
    }
    unsigned_members = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoUnsignedMembersBehavior"]
    assert unsigned_members == {
        "count": 2, "u16": 60000, "u32": 4000000000,
        "types": ["System.UInt16", "System.UInt32"],
        "u16TypeCode": "UInt16", "u32TypeCode": "UInt32",
    }
    byte_members = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoByteMembersBehavior"]
    assert byte_members == {
        "count": 2, "byteValue": 200, "sbyteValue": -5,
        "types": ["System.Byte", "System.SByte"],
        "byteTypeCode": "Byte", "sbyteTypeCode": "SByte",
    }
    byte_conversions = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationInfoByteConversionsBehavior"]
    assert byte_conversions == {
        "byteText": 255, "sbyteText": -128,
        "byteInteger": 200, "sbyteInteger": -5,
        "byteType": 200, "sbyteTypeCode": -5,
        "byteOverflowHigh": "System.OverflowException",
        "byteOverflowLow": "System.OverflowException",
        "sbyteOverflowHigh": "System.OverflowException",
        "sbyteOverflowLow": "System.OverflowException",
        "byteFormat": "System.FormatException",
        "sbyteFormat": "System.FormatException",
        "byteNull": "System.ArgumentNullException",
    }
    byte_convertible = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedByteConvertibleContractBehavior"]
    assert byte_convertible == {
        "byteConvertible": True, "sbyteConvertible": True,
        "byteTypeCode": "Byte", "sbyteTypeCode": "SByte",
        "byteToInt32": 200, "sbyteToInt32": -5,
        "byteToString": "200", "sbyteToString": "-5",
        "byteToSByte": "System.OverflowException",
        "sbyteToByte": "System.OverflowException",
        "byteToDateTime": "System.InvalidCastException",
    }
    byte_to_type = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedByteToTypeContractBehavior"]
    assert byte_to_type == {
        "byteSelf": "System.Byte", "sbyteSelf": "System.SByte",
        "byteInt": 200, "sbyteInt": -5,
        "byteString": "200", "sbyteString": "-5",
        "byteDecimal": "200", "sbyteDecimal": "-5",
        "byteToSByte": "System.OverflowException",
        "sbyteToByte": "System.OverflowException",
        "byteNull": "System.ArgumentNullException",
    }
    uint16_convertible = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUInt16ConvertibleContractBehavior"]
    assert uint16_convertible == {
        "implements": True, "typeCode": "UInt16",
        "int32": 60000, "uint32": 60000, "text": "60000",
        "byteOverflow": "System.OverflowException",
        "int16Overflow": "System.OverflowException",
        "dateTime": "System.InvalidCastException",
    }
    uint32_convertible = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUInt32ConvertibleContractBehavior"]
    assert uint32_convertible == {
        "implements": True, "typeCode": "UInt32",
        "int64": 4000000000, "uint32": 4000000000,
        "uint64Text": "4000000000", "decimalText": "4000000000",
        "text": "4000000000",
        "int32Overflow": "System.OverflowException",
        "byteOverflow": "System.OverflowException",
        "dateTime": "System.InvalidCastException",
    }
    unsigned_routes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUnsignedFormatterRoutesBehavior"]
    assert unsigned_routes == {
        "u16Text": 60000, "u32Text": 4000000000,
        "u16Type": 60000, "u32TypeCode": 4000000000,
        "u16Overflow": "System.OverflowException",
        "u32Overflow": "System.OverflowException",
        "negativeOverflow": "System.OverflowException",
        "format": "System.FormatException",
        "nullValue": "System.ArgumentNullException",
    }
    unsigned_to_type = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUnsignedToTypeContractBehavior"]
    assert unsigned_to_type == {
        "u16Self": "System.UInt16", "u32Self": "System.UInt32",
        "u16ToUInt32": 60000, "u16ToInt32": 60000,
        "u32ToInt64": 4000000000, "u32ToDecimal": "4000000000",
        "u32ToString": "4000000000",
        "u32ToInt32": "System.OverflowException",
        "u32ToUInt16": "System.OverflowException",
        "u16Null": "System.ArgumentNullException",
    }
    signed_float_routes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt16SingleFormatterRoutesBehavior"]
    assert signed_float_routes == {
        "int16Text": -1234, "singleText": 1.25,
        "int16Type": -1234, "singleTypeCode": 1.25,
        "int16OverflowHigh": "System.OverflowException",
        "int16OverflowLow": "System.OverflowException",
        "int16Format": "System.FormatException",
        "singleFormat": "System.FormatException",
        "singleNull": "System.ArgumentNullException",
    }
    uint64_routes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUInt64FormatterRoutesBehavior"]
    assert uint64_routes == {
        "text": "18446744073709551615",
        "type": "18446744073709551615",
        "typeCode": "18446744073709551615",
        "overflow": "System.OverflowException",
        "negative": "System.OverflowException",
        "format": "System.FormatException",
        "nullValue": "System.ArgumentNullException",
    }
    decimal_routes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDecimalFormatterRoutesBehavior"]
    assert decimal_routes == {
        "text": "12.5", "type": "12.5", "typeCode": "12.5",
        "integer": "42", "format": "System.FormatException",
        "nullValue": "System.ArgumentNullException",
    }
    date_routes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDateTimeFormatterRoutesBehavior"]
    assert date_routes == {
        "text": "2024-02-29", "type": "2024-02-29",
        "typeCode": "2024-02-29",
        "invalid": "System.FormatException",
        "impossible": "System.FormatException",
        "nullValue": "System.ArgumentNullException",
    }
    char_routes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedCharFormatterRoutesBehavior"]
    assert char_routes == {
        "text": "Q", "type": "Q", "typeCode": "Q",
        "integer": "A", "empty": "System.FormatException",
        "longText": "System.FormatException",
        "nullValue": "System.ArgumentNullException",
    }
    object_routes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedFormatterObjectRoutesBehavior"]
    assert object_routes == {
        "objectTypeSame": True, "objectCodeSame": True,
        "plainObjectType": None,
        "plainObjectCode": "System.InvalidCastException",
        "integerCode": 42,
        "nullType": "System.ArgumentNullException",
        "nullCode": "System.ArgumentNullException",
        "nullTarget": "System.ArgumentNullException",
    }
    typecode_boundaries = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedFormatterTypeCodeBoundariesBehavior"]
    assert typecode_boundaries == {
        "dbNullCode": "System.InvalidCastException",
        "dbNullType": None,
        "integerToDBNull": "System.InvalidCastException",
        "integerToEmpty": "System.InvalidCastException",
        "dbNullToEmpty": "System.InvalidCastException",
        "nullToDBNull": "System.ArgumentNullException",
    }
    getvalue_conversions = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializationGetValueConversionsBehavior"]
    assert getvalue_conversions == {
        "u64String": "18446744073709551615",
        "u32String": "4000000000", "byteString": "200",
        "date": "2024-02-29",
        "u32ToInt32": "System.OverflowException",
    }
    date_convertible = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDateTimeConvertibleContractBehavior"]
    assert date_convertible == {
        "implements": True, "typeCode": "DateTime",
        "dateSame": False, "invariantText": "02/29/2024 00:00:00",
        "int32": "System.InvalidCastException",
        "boolean": "System.InvalidCastException",
        "byteValue": "System.InvalidCastException",
        "selfTypeSame": False,
    }
    decimal_convertible = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDecimalConvertibleContractBehavior"]
    assert decimal_convertible == {
        "implements": True, "typeCode": "Decimal",
        "int32": 12, "roundedUp": 14, "doubleValue": 12.5,
        "boolean": True, "text": "12.5", "selfValue": "12.5",
        "charValue": "System.InvalidCastException",
        "dateTime": "System.InvalidCastException",
    }
    uint64_cross = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUInt64CrossConversionsBehavior"]
    assert uint64_cross == {
        "decimalText": "18446744073709551615",
        "getValueDecimal": "18446744073709551615",
        "maxToInt64": "System.OverflowException",
        "smallToInt64": 42,
        "maxToUInt32": "System.OverflowException",
    }
    unsigned_result_identity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUnsignedConvertResultIdentityBehavior"]
    assert unsigned_result_identity == {
        "types": ["System.Byte", "System.SByte", "System.UInt16", "System.UInt32"],
        "values": ["200", "-5", "60000", "4000000000"],
    }
    uint64_narrowing = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUInt64NarrowingConversionsBehavior"]
    assert uint64_narrowing == {
        "int32Small": 42, "byteSmall": 42, "u16Small": 42,
        "int32Max": "System.OverflowException",
        "byteMax": "System.OverflowException",
        "u16Max": "System.OverflowException",
    }
    int64_narrowing = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt64NarrowingConversionsBehavior"]
    assert int64_narrowing == {
        "byteSmall": 42, "sbyteSmall": 42, "int16Small": 42,
        "u16Small": 42, "u32Small": 42,
        "byteLarge": "System.OverflowException",
        "u32Large": "System.OverflowException",
        "negativeU32": "System.OverflowException",
    }
    int64_widening = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt64WideningConversionsBehavior"]
    assert int64_widening == {
        "text": "5000000000", "decimalText": "5000000000",
        "doubleValue": 5000000000, "boolean": True,
        "uint64Text": "5000000000",
        "negativeUInt64": "System.OverflowException",
    }
    floating_routes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedFloatingFormatterConversionsBehavior"]
    assert floating_routes == {
        "doubleToSingle": 1.25, "singleToDouble": 1.25,
        "doubleToDecimal": "1.25", "singleToDecimal": "1.25",
        "midpointEven": 2, "midpointUp": 4, "doubleBoolean": True,
        "hugeInt32": "System.OverflowException",
    }
    exceptional_floats = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedFloatingExceptionalBoundariesBehavior"]
    assert exceptional_floats == {
        "nanInt32": "System.OverflowException",
        "infinityInt32": "System.OverflowException",
        "nanDecimal": "System.OverflowException",
        "infinityDecimal": "System.OverflowException",
        "nanBoolean": True, "infinitySingle": True, "nanDouble": True,
    }
    floating_text = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedFloatingTextConversionsBehavior"]
    assert floating_text == {
        "nanSingle": True, "nanDouble": True,
        "infinitySingle": True, "infinityDouble": True,
        "nanText": "NaN", "positiveInfinityText": "Infinity",
        "negativeInfinityText": "-Infinity",
    }
    boolean_text = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedBooleanTextConversionsBehavior"]
    assert boolean_text == {
        "paddedTrue": True, "mixedCaseFalse": False, "tabbedTrue": True,
        "numericText": "System.FormatException",
        "emptyText": "System.FormatException",
        "nullValue": "System.ArgumentNullException",
    }
    decimal_limits = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDecimalIntegerLimitsBehavior"]
    assert decimal_limits == {
        "maximum": "79228162514264337593543950335",
        "minimum": "-79228162514264337593543950335",
        "maximumPlusOne": "System.OverflowException",
        "minimumMinusOne": "System.OverflowException",
        "converterOverflow": "System.OverflowException",
    }
    floating_grammar = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedFloatingTextGrammarBehavior"]
    assert floating_grammar == {
        "decimalSingle": 1.25, "exponentDouble": 125,
        "singleSuffix": "System.FormatException",
        "doubleSuffix": "System.FormatException",
        "hexadecimalFloat": "System.FormatException",
    }
    decimal_grouping = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDecimalGroupedTextBehavior"]
    assert decimal_grouping == {
        "grouped": "1234.50", "negativeGrouped": "-1234.50",
    }
    int32_none = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32NoneStyleBehavior"]
    assert int32_none == {
        "digits": 42, "leadingSign": "System.FormatException",
        "leadingSpace": "System.FormatException",
        "trailingSpace": "System.FormatException",
        "tryLeadingSign": False,
    }
    int32_binary = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32BinaryStyleBehavior"]
    assert int32_binary == {
        "value": 42, "padded": 42, "allBits": -1,
        "prefix": "System.FormatException",
        "overflow": "System.OverflowException", "tryPrefix": False,
    }
    datetime_time = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDateTimeTimeOfDayBehavior"]
    assert datetime_time == {
        "constructedHour": 3, "constructedMinute": 4, "constructedSecond": 5,
        "constructedText": "2026-01-02 03:04:05",
        "parsedText": "2026-01-02 03:04:05", "convertedSame": True,
    }
    datetime_millis = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDateTimeMillisecondsBehavior"]
    assert datetime_millis == {
        "constructedMillisecond": 123,
        "constructedText": "2026-01-02 03:04:05.123",
        "parsedMillisecond": 123,
        "parsedText": "2026-01-02 03:04:05.123",
        "convertedMillisecond": 123,
    }
    exception_serialization = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedExceptionSerializationBehavior"]
    assert exception_serialization == {
        "interfaces": ["System.Runtime.Serialization.ISerializable"],
        "count": 12,
        "names": ["ClassName", "Message", "Data", "InnerException", "HelpURL",
                  "StackTraceString", "RemoteStackTraceString", "RemoteStackIndex",
                  "ExceptionMethod", "HResult", "Source", "WatsonBuckets"],
        "className": "System.Exception", "message": "boom", "dataIsNull": True,
        "innerSame": True, "stackTraceString": None,
        "remoteStackTraceString": None, "remoteStackIndex": 0,
        "exceptionMethod": None, "watsonBucketsIsNull": True,
        "hResult": -2146233088, "helpUrl": "https://example.test/help",
        "source": "dotj-test", "nullError": "System.ArgumentNullException",
        "nullParameter": "info",
    }
    target_site = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedExceptionTargetSiteBehavior"]
    assert target_site == {
        "beforeNull": True, "afterExists": True,
        "nameContainsCaller": True, "memberType": "Method", "repeatedSame": True,
    }
    data_dictionary = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedExceptionDataDictionaryBehavior"]
    assert data_dictionary == {
        "interfaceName": "System.Collections.IDictionary",
        "interfaceMethods": ["Contains", "Add", "Clear", "GetEnumerator", "Remove"],
        "interfaceProperties": ["Item", "Keys", "Values", "IsReadOnly", "IsFixedSize"],
        "baseInterfaces": ["System.Collections.ICollection", "System.Collections.IEnumerable"],
        "collectionMethods": ["CopyTo"],
        "collectionProperties": ["Count", "SyncRoot", "IsSynchronized"],
        "enumerableMethods": ["GetEnumerator"],
        "enumeratorProperties": ["Key", "Value", "Entry"],
        "entryIsValueType": True,
        "initialCount": 0, "containsAfterAdd": True, "firstValue": "first",
        "keysCount": 1, "valuesCount": 1, "enumeratorMoved": True,
        "enumeratedKey": "key", "enumeratedValue": "first",
        "copiedKey": "key", "copiedValue": "first",
        "duplicateError": "System.ArgumentException",
        "replacedValue": "second", "countAfterRemove": 0,
        "countAfterClear": 0, "isReadOnly": False, "isFixedSize": False,
    }
    assert json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedExceptionDataBoundaries"] == {
        "nullAdd": "System.ArgumentNullException",
        "nullContains": "System.ArgumentNullException",
        "nullRead": "System.ArgumentNullException",
        "nullWrite": "System.ArgumentNullException",
        "nullRemove": "System.ArgumentNullException",
        "containsNullValue": True,
        "nullValue": None,
        "objectKeyRetained": True,
        "beforeMove": "System.InvalidOperationException",
        "afterEnd": "System.InvalidOperationException",
    }
    mutation = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedExceptionDataEnumeratorMutation"]
    assert set(mutation) == {"add", "replace", "remove", "clear"}
    assert all(value == {
        "firstMoved": True,
        "currentError": None,
        "moveError": "System.InvalidOperationException",
        "resetError": "System.InvalidOperationException",
    } for value in mutation.values())
    views = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedExceptionDataViewEnumeration"]
    assert set(views) == {prefix + action for prefix in ("keys", "values")
                          for action in ("Add", "Replace", "Remove", "Clear")}
    for name, value in views.items():
        assert value == {
            "firstMoved": True,
            "firstCurrent": "first" if name.startswith("keys") else 1,
            "currentError": None,
            "moveError": "System.InvalidOperationException",
            "resetError": "System.InvalidOperationException",
            "liveCount": {"Add": 3, "Replace": 2, "Remove": 1, "Clear": 0}[
                name.removeprefix("keys").removeprefix("values")],
        }
    assert json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedExceptionDataViewProperties"] == {
        "dictionarySynchronized": False,
        "keysSynchronized": False,
        "valuesSynchronized": False,
        "syncRootIsDictionary": True,
        "keySyncRootIsDictionary": True,
        "valueSyncRootIsDictionary": True,
        "keySyncRootIsDictionaryRoot": True,
        "valueSyncRootIsDictionaryRoot": True,
        "repeatedKeyViewSame": False,
        "repeatedValueViewSame": False,
        "keysCount": 1,
        "valuesCount": 1,
    }
    assert json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedExceptionDataCopyToBoundaries"] == {
        "nullArray": "System.ArgumentNullException", "nullArrayParam": "array",
        "negativeIndex": "System.ArgumentOutOfRangeException", "negativeIndexParam": "index",
        "indexAtLength": "System.ArgumentException", "indexAtLengthParam": "index",
        "tooSmall": "System.ArgumentException", "tooSmallParam": "index",
        "wrongElement": "System.InvalidCastException", "wrongElementParam": None,
        "multidimensional": "System.ArgumentException", "multidimensionalParam": None,
        "entryOffsetKey": "key", "entryOffsetValue": 7,
        "keyOffset": "key", "valueOffset": 7,
        "argumentOutOfRangeConstructors": [
            [], ["System.String"], ["System.String", "System.String"],
            ["System.String", "System.Exception"],
            ["System.String", "System.Object", "System.String"],
        ],
        "argumentOutOfRangeHResult": -2146233086,
    }
    assert json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedArgumentOutOfRangeConstructors"] == [
        {"paramName": None, "message": "Specified argument was out of the range of valid values.",
         "actualValue": None, "innerSame": False, "hResult": -2146233086},
        {"paramName": "index", "message": "Specified argument was out of the range of valid values. (Parameter 'index')",
         "actualValue": None, "innerSame": False, "hResult": -2146233086},
        {"paramName": "index", "message": "custom (Parameter 'index')",
         "actualValue": None, "innerSame": False, "hResult": -2146233086},
        {"paramName": None, "message": "custom", "actualValue": None,
         "innerSame": True, "hResult": -2146233086},
        {"paramName": "index", "message": "custom (Parameter 'index')\r\nActual value was 42.",
         "actualValue": 42, "innerSame": False, "hResult": -2146233086},
    ]
    foundation = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))
    bit_helpers = foundation["selectedInt32BitHelpers"]
    assert [(item["value"], item["isEven"], item["isOdd"], item["isNegative"],
             item["isPositive"], item["isPow2"], item["leadingZeroCount"],
             item["trailingZeroCount"], item["popCount"], item["log2"])
            for item in bit_helpers["values"]] == [
                (0, True, False, False, True, False, 32, 32, 0, 0),
                (1, False, True, False, True, True, 31, 0, 1, 0),
                (2, True, False, False, True, True, 30, 1, 1, 1),
                (3, False, True, False, True, False, 30, 0, 2, 1),
                (-1, False, True, True, False, False, 0, 0, 32, None),
                (-2147483648, True, False, True, False, False, 0, 31, 1, None),
                (2147483647, False, True, False, True, False, 1, 0, 31, 30),
                (1073741824, True, False, False, True, True, 1, 30, 1, 30),
            ]
    assert all(item["log2Error"] == ("System.ArgumentOutOfRangeException" if item["value"] < 0 else None)
               and item["log2ErrorParam"] == ("value" if item["value"] < 0 else None)
               for item in bit_helpers["values"])
    assert [(item["value"], item["amount"], item["left"], item["right"])
            for item in bit_helpers["rotations"]] == [
                (1, 1, 2, -2147483648), (-1, 1, -1, -1),
                (-2147483648, 31, 1073741824, 1), (1, 32, 1, 1),
                (1, -1, -2147483648, 2),
            ]
    int32_surface = next(item for item in foundation["completeDeclaredSurface"]
                         if item["fullName"] == "System.Int32")
    assert int32_surface["fields"] == [
        {"name": "MaxValue", "type": "System.Int32", "isStatic": True, "isLiteral": True},
        {"name": "MinValue", "type": "System.Int32", "isStatic": True, "isLiteral": True},
    ]
    expected_bit_names = {"IsEvenInteger", "IsOddInteger", "IsNegative", "IsPositive", "IsPow2",
                          "LeadingZeroCount", "TrailingZeroCount", "PopCount", "Log2",
                          "RotateLeft", "RotateRight"}
    declared_bit_methods = [item for item in int32_surface["methods"] if item["name"] in expected_bit_names]
    assert {item["name"] for item in declared_bit_methods} == expected_bit_names
    assert all(item["isStatic"] and item["returnType"] ==
               ("System.Boolean" if item["name"].startswith("Is") else "System.Int32")
               and [parameter["type"] for parameter in item["parameters"]] ==
               (["System.Int32", "System.Int32"] if item["name"].startswith("Rotate") else ["System.Int32"])
               for item in declared_bit_methods)
    arithmetic = foundation["selectedInt32SignedArithmetic"]
    assert [(item["value"], item["abs"], item["absError"], item["sign"])
            for item in arithmetic["unary"]] == [
                (-2147483648, None, "System.OverflowException", -1),
                (-3, 3, None, -1), (-1, 1, None, -1), (0, 0, None, 0),
                (1, 1, None, 1), (3, 3, None, 1), (2147483647, 2147483647, None, 1),
            ]
    assert [(item["x"], item["y"], item["max"], item["min"],
             item["maxMagnitude"], item["minMagnitude"])
            for item in arithmetic["pairs"]] == [
                (2, 3, 3, 2, 3, 2), (-3, 3, 3, -3, 3, -3),
                (-2147483648, 2147483647, 2147483647, -2147483648,
                 -2147483648, 2147483647),
                (0, 0, 0, 0, 0, 0), (-3, -3, -3, -3, -3, -3),
            ]
    assert [(item["value"], item["min"], item["max"], item["result"],
             item["error"], item["errorParam"])
            for item in arithmetic["clamps"]] == [
                (5, 0, 10, 5, None, None), (-5, 0, 10, 0, None, None),
                (15, 0, 10, 10, None, None), (0, 10, 0, None, "System.ArgumentException", None),
            ]
    assert [(item["value"], item["sign"], item["result"], item["error"])
            for item in arithmetic["copies"]] == [
                (-3, 1, 3, None), (3, -1, -3, None),
                (-2147483648, -1, -2147483648, None),
                (-2147483648, 1, None, "System.OverflowException"), (0, -1, 0, None),
            ]
    arithmetic_names = {"Abs": 1, "Sign": 1, "Max": 2, "Min": 2,
                        "MaxMagnitude": 2, "MinMagnitude": 2, "Clamp": 3, "CopySign": 2}
    declared_arithmetic = [item for item in int32_surface["methods"]
                           if item["name"] in arithmetic_names]
    assert {item["name"] for item in declared_arithmetic} == set(arithmetic_names)
    assert all(item["isStatic"] and item["returnType"] == "System.Int32"
               and [parameter["type"] for parameter in item["parameters"]] ==
               ["System.Int32"] * arithmetic_names[item["name"]]
               for item in declared_arithmetic)
    value_identity = foundation["selectedInt32ValueIdentityAndBigMul"]
    assert {key: value_identity[key] for key in (
        "typedSame", "typedDifferent", "objectSame", "objectDifferentType", "objectNull",
        "zeroHash", "negativeHash", "positiveHash")} == {
        "typedSame": True, "typedDifferent": False, "objectSame": True,
        "objectDifferentType": False, "objectNull": False,
        "zeroHash": 0, "negativeHash": -42, "positiveHash": 42,
    }
    assert [(item["left"], item["right"], item["product"])
            for item in value_identity["products"]] == [
                (-2147483648, 2147483647, -4611686016279904256),
                (2147483647, 2147483647, 4611686014132420609),
                (-3, 7, -21), (0, -2147483648, 0),
            ]
    assert {item["signature"] for item in int32_surface["methods"]
            if item["name"] in {"BigMul", "Equals", "GetHashCode"} and not item["isSpecialName"]} == {
                "Int64 BigMul(Int32, Int32)", "Boolean Equals(Int32)",
                "Boolean Equals(System.Object)", "Int32 GetHashCode()",
            }
    divrem = foundation["selectedInt32DivRem"]
    assert [(item["left"], item["right"], item["quotient"], item["remainder"])
            for item in divrem["pairs"]] == [
                (7, 3, 2, 1), (-7, 3, -2, -1), (7, -3, -2, 1),
                (-2147483648, 3, -715827882, -2), (2147483647, 1, 2147483647, 0),
            ]
    assert {key: divrem[key] for key in (
        "zeroError", "overflowError", "tupleDefinition", "tupleIsValueType",
        "tupleFields", "tupleConstructors", "divideByZeroBase", "divideByZeroConstructors",
        "divideByZeroHResult", "divideByZeroMessage", "arithmeticBase",
        "arithmeticConstructors", "arithmeticHResult", "arithmeticMessage",
        "overflowBase", "overflowHResult", "overflowMessage")} == {
        "zeroError": "System.DivideByZeroException",
        "overflowError": "System.OverflowException",
        "tupleDefinition": "System.ValueTuple`2",
        "tupleIsValueType": True,
        "tupleFields": [
            {"name": "Item1", "type": "System.Int32", "isInitOnly": False},
            {"name": "Item2", "type": "System.Int32", "isInitOnly": False},
        ],
        "tupleConstructors": [["System.Int32", "System.Int32"]],
        "divideByZeroBase": "System.ArithmeticException",
        "divideByZeroConstructors": [[], ["System.String"], ["System.String", "System.Exception"]],
        "divideByZeroHResult": -2147352558,
        "divideByZeroMessage": "Attempted to divide by zero.",
        "arithmeticBase": "System.SystemException",
        "arithmeticConstructors": [[], ["System.String"], ["System.String", "System.Exception"]],
        "arithmeticHResult": -2147024362,
        "arithmeticMessage": "Overflow or underflow in the arithmetic operation.",
        "overflowBase": "System.ArithmeticException",
        "overflowHResult": -2146233066,
        "overflowMessage": "Arithmetic operation resulted in an overflow.",
    }
    assert {item["signature"] for item in int32_surface["methods"]
            if item["name"] == "DivRem" and not item["isSpecialName"]} == {
                "System.ValueTuple`2[System.Int32,System.Int32] DivRem(Int32, Int32)",
            }
    assert foundation["selectedInt32CreateFromInt64"] == [
        {"value": source, "checkedValue": checked, "checkedError": error,
         "saturated": saturated, "truncated": truncated}
        for source, checked, error, saturated, truncated in [
            (-9223372036854775808, None, "System.OverflowException", -2147483648, 0),
            (-2147483649, None, "System.OverflowException", -2147483648, 2147483647),
            (-2147483648, -2147483648, None, -2147483648, -2147483648),
            (-3, -3, None, -3, -3), (0, 0, None, 0, 0), (3, 3, None, 3, 3),
            (2147483647, 2147483647, None, 2147483647, 2147483647),
            (2147483648, None, "System.OverflowException", 2147483647, -2147483648),
            (9223372036854775807, None, "System.OverflowException", 2147483647, -1),
        ]
    ]
    assert {item["signature"] for item in int32_surface["methods"]
            if item["name"] in {"CreateChecked", "CreateSaturating", "CreateTruncating"}
            and not item["isSpecialName"]} == {
                "Int32 CreateChecked[TOther](TOther)",
                "Int32 CreateSaturating[TOther](TOther)",
                "Int32 CreateTruncating[TOther](TOther)",
            }
    assert [(item["value"], item["checkedValue"], item["checkedError"],
             item["saturated"], item["truncated"])
            for item in foundation["selectedInt32CreateFromBigInteger"]] == [
                ("-1208925819614629174706176", None, "System.OverflowException", -2147483648, 0),
                ("-2147483649", None, "System.OverflowException", -2147483648, 2147483647),
                ("-2147483648", -2147483648, None, -2147483648, -2147483648),
                ("-3", -3, None, -3, -3), ("0", 0, None, 0, 0), ("3", 3, None, 3, 3),
                ("2147483647", 2147483647, None, 2147483647, 2147483647),
                ("2147483648", None, "System.OverflowException", 2147483647, -2147483648),
                ("1208925819614629174706176", None, "System.OverflowException", 2147483647, 0),
            ]
    assert [(item["value"], item["checkedValue"], item["checkedError"],
             item["saturated"], item["truncated"])
            for item in foundation["selectedInt32CreateFromDouble"]] == [
                ("-Infinity", None, "System.OverflowException", -2147483648, -2147483648),
                ("-2147483649", None, "System.OverflowException", -2147483648, -2147483648),
                ("-2147483648.75", -2147483648, None, -2147483648, -2147483648),
                ("-2147483648", -2147483648, None, -2147483648, -2147483648),
                ("-3.9", -3, None, -3, -3), ("-0.5", 0, None, 0, 0),
                ("0", 0, None, 0, 0), ("0.5", 0, None, 0, 0),
                ("3.9", 3, None, 3, 3),
                ("2147483647", 2147483647, None, 2147483647, 2147483647),
                ("2147483647.75", 2147483647, None, 2147483647, 2147483647),
                ("2147483648", None, "System.OverflowException", 2147483647, 2147483647),
                ("Infinity", None, "System.OverflowException", 2147483647, 2147483647),
                ("NaN", None, "System.OverflowException", 0, 0),
            ]
    assert [(item["value"], item["checkedValue"], item["checkedError"],
             item["saturated"], item["truncated"])
            for item in foundation["selectedInt32CreateFromSingle"]] == [
                ("-Infinity", None, "System.OverflowException", -2147483648, -2147483648),
                ("-3.4028235E+38", None, "System.OverflowException", -2147483648, -2147483648),
                ("-2.147484E+09", None, "System.OverflowException", -2147483648, -2147483648),
                ("-2.1474836E+09", -2147483648, None, -2147483648, -2147483648),
                ("-3.9", -3, None, -3, -3), ("-0.5", 0, None, 0, 0),
                ("0", 0, None, 0, 0), ("0.5", 0, None, 0, 0),
                ("3.9", 3, None, 3, 3),
                ("2.1474835E+09", 2147483520, None, 2147483520, 2147483520),
                ("2.1474836E+09", None, "System.OverflowException", 2147483647, 2147483647),
                ("3.4028235E+38", None, "System.OverflowException", 2147483647, 2147483647),
                ("Infinity", None, "System.OverflowException", 2147483647, 2147483647),
                ("NaN", None, "System.OverflowException", 0, 0),
            ]
    assert [(item["value"], item["checkedValue"], item["checkedError"],
             item["saturated"], item["truncated"])
            for item in foundation["selectedInt32CreateFromDecimal"]] == [
                ("-79228162514264337593543950335", None, "System.OverflowException", -2147483648, -2147483648),
                ("-2147483649", None, "System.OverflowException", -2147483648, -2147483648),
                ("-2147483648.9", -2147483648, None, -2147483648, -2147483648),
                ("-2147483648", -2147483648, None, -2147483648, -2147483648),
                ("-3.9", -3, None, -3, -3), ("-0.5", 0, None, 0, 0),
                ("0", 0, None, 0, 0), ("0.5", 0, None, 0, 0),
                ("3.9", 3, None, 3, 3),
                ("2147483647", 2147483647, None, 2147483647, 2147483647),
                ("2147483647.9", 2147483647, None, 2147483647, 2147483647),
                ("2147483648", None, "System.OverflowException", 2147483647, 2147483647),
                ("79228162514264337593543950335", None, "System.OverflowException", 2147483647, 2147483647),
            ]
    assert foundation["selectedInt32OrdinaryOverloads"] == {
        "comparisons": [
            {"left": 5, "right": 3, "result": 1},
            {"left": 3, "right": 5, "result": -1},
            {"left": 3, "right": 3, "result": 0},
            {"left": -2147483648, "right": 2147483647, "result": -1},
            {"left": 2147483647, "right": -2147483648, "result": 1},
        ],
        "parseHex": 255, "parseProvider": -7,
        "parseInvalidError": "System.FormatException",
        "parseNullError": "System.ArgumentNullException",
        "tryParsed": -7, "tryInvalid": False, "tryInvalidResult": 0,
        "tryNull": False, "tryNullResult": 0,
        "textDefault": "42", "textFormat": "0042", "textNegative": "-0042",
    }
    assert [(item["sourceType"], item["value"], item["checkedValue"],
             item["checkedError"], item["saturated"], item["truncated"])
            for item in foundation["selectedInt32CreateSmallIntegrals"]] == [
                ("System.Byte", "0", 0, None, 0, 0),
                ("System.Byte", "255", 255, None, 255, 255),
                ("System.SByte", "-128", -128, None, -128, -128),
                ("System.SByte", "127", 127, None, 127, 127),
                ("System.UInt16", "0", 0, None, 0, 0),
                ("System.UInt16", "65535", 65535, None, 65535, 65535),
                ("System.UInt32", "0", 0, None, 0, 0),
                ("System.UInt32", "2147483647", 2147483647, None, 2147483647, 2147483647),
                ("System.UInt32", "2147483648", None, "System.OverflowException", 2147483647, -2147483648),
                ("System.UInt32", "4294967295", None, "System.OverflowException", 2147483647, -1),
            ]
    assert foundation["selectedInt32SpanParse"] == {
        "charParseProvider": -7, "charParseStyled": 255,
        "byteParseProvider": -7, "byteParseStyled": 255,
        "charPlain": True, "charPlainValue": -7,
        "charProvider": True, "charProviderValue": -7,
        "charStyled": True, "charStyledValue": 255,
        "bytePlain": True, "bytePlainValue": -7,
        "byteProvider": True, "byteProviderValue": -7,
        "byteStyled": True, "byteStyledValue": 255,
        "charInvalid": False, "charInvalidValue": 0,
        "byteInvalid": False, "byteInvalidValue": 0,
    }
    assert {
        "Int32 CompareTo(Int32)",
        "Int32 Parse(System.String, System.Globalization.NumberStyles)",
        "Int32 Parse(System.String, System.IFormatProvider)",
        "Boolean TryParse(System.String, System.IFormatProvider, Int32 ByRef)",
        "System.String ToString()", "System.String ToString(System.String)",
    } <= {item["signature"] for item in int32_surface["methods"]}
    assert snapshot["assemblySha256"] == provenance["installedCoreLibSha256"]
    metadata = snapshot["type"]
    assert metadata["fullName"] == "System.Type"
    selected = {
        "Boolean Equals(System.Type)",
        "System.Type GetGenericTypeDefinition()",
        "System.Type[] GetGenericArguments()",
        "System.Type[] GetGenericParameterConstraints()",
        "System.Type MakeGenericType(System.Type[])",
        "System.Type GetType(System.String)",
        "System.Type GetEnumUnderlyingType()",
        "System.String[] GetEnumNames()",
        "System.Array GetEnumValues()",
        "System.Array GetEnumValuesAsUnderlyingType()",
        "Boolean IsEnumDefined(System.Object)",
        "System.String GetEnumName(System.Object)",
        "Boolean IsAssignableFrom(System.Type)",
        "Boolean IsSubclassOf(System.Type)",
        "Boolean IsInstanceOfType(System.Object)",
        "System.Type[] GetInterfaces()",
        "System.Type[] GetOptionalCustomModifiers()",
        "System.Reflection.MemberInfo[] GetDefaultMembers()",
        "System.Reflection.MemberInfo[] GetMember(System.String)",
        "System.Reflection.MemberInfo[] GetMember(System.String, System.Reflection.BindingFlags)",
        "System.Reflection.MemberInfo[] GetMember(System.String, System.Reflection.MemberTypes, System.Reflection.BindingFlags)",
        "System.Reflection.MemberInfo[] GetMembers()",
        "System.Reflection.MemberInfo[] GetMembers(System.Reflection.BindingFlags)",
        "System.Reflection.MethodInfo[] GetMethods(System.Reflection.BindingFlags)",
        "System.Reflection.MethodInfo[] GetMethods()",
        "System.Reflection.MethodInfo GetMethod(System.String)",
        "System.Reflection.MethodInfo GetMethod(System.String, System.Reflection.BindingFlags)",
        "System.Reflection.MethodInfo GetMethod(System.String, System.Type[])",
        "System.Reflection.MethodInfo GetMethod(System.String, System.Reflection.BindingFlags, System.Type[])",
        "System.Type[] GetRequiredCustomModifiers()",
        "System.Type GetInterface(System.String)",
        "System.Type GetInterface(System.String, Boolean)",
        "System.Type GetNestedType(System.String)",
        "System.Type GetNestedType(System.String, System.Reflection.BindingFlags)",
        "System.Type[] GetNestedTypes()",
        "System.Type[] GetNestedTypes(System.Reflection.BindingFlags)",
    }
    signatures = {method["signature"] for method in metadata["methods"]}
    assert selected <= signatures
    assert any(method["signature"] == "System.Type GetType(System.String)" and method["isStatic"]
               for method in metadata["methods"])
    properties = {item["Name"] for item in metadata["properties"]}
    assert {"GenericTypeArguments", "IsGenericType", "IsGenericTypeDefinition", "ContainsGenericParameters", "IsConstructedGenericType",
            "IsGenericParameter", "GenericParameterPosition", "IsArray", "IsSZArray", "IsVariableBoundArray", "HasElementType", "IsByRef", "IsPointer",
            "FullName", "Namespace", "BaseType", "IsClass", "IsValueType", "IsPrimitive", "IsAbstract", "IsSealed", "IsPublic", "IsVisible",
            "IsInterface", "IsEnum"} <= properties
    observed = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedGetTypeBehavior"]
    expected = {
        "exact": {"result": "System.String", "exception": None, "paramName": None},
        "insensitive": {"result": "System.String", "exception": None, "paramName": None},
        "sensitiveMiss": {"result": None, "exception": None, "paramName": None},
        "missing": {"result": None, "exception": None, "paramName": None},
        "missingThrow": {"result": None, "exception": "System.TypeLoadException", "paramName": None},
        "nullName": {"result": None, "exception": "System.ArgumentNullException", "paramName": "typeName"},
    }
    assert {name: observed[name] for name in expected} == expected
    assert observed["coreLibString"]["result"] == "System.String"
    assert observed["coreLibInt32"]["result"] == "System.Int32"
    assert observed["legacyString"]["result"] == "System.String"
    assert observed["unknownAssembly"]["result"] is None
    assert observed["unknownAssemblyThrow"]["exception"] == "System.IO.FileNotFoundException"
    assert observed["emptyName"]["result"] is None
    assert observed["emptyNameThrow"]["exception"] == "System.TypeLoadException"
    assert observed["leadingSpace"]["result"] == "System.String"
    assert observed["trailingSpace"]["result"] is None
    assert observed["qualifierSpace"]["result"] is None
    assert observed["emptyAssembly"]["result"] is None
    assert observed["emptyAssemblyThrow"]["exception"] == "System.ArgumentException"
    assert observed["emptyAssemblyThrow"]["paramName"] == "typeName@13"
    assert observed["stringArray"]["result"] == "System.String[]"
    assert observed["intArray"]["result"] == "System.Int32[]"
    assert observed["stringArrayInsensitive"]["result"] == "System.String[]"
    assert observed["stringArrayQualified"]["result"] == "System.String[]"
    assert observed["listStringSimple"]["result"] == observed["listStringQualified"]["result"]
    assert observed["listStringSimple"]["result"].startswith("System.Collections.Generic.List`1[[System.String,")
    assert observed["dictionarySimple"]["result"] == observed["dictionaryQualified"]["result"]
    assert observed["dictionarySimple"]["result"].startswith("System.Collections.Generic.Dictionary`2[[System.String,")
    assert observed["dictionarySwapped"]["result"] != observed["dictionarySimple"]["result"]
    assert observed["jaggedString"]["result"] == "System.String[][]"
    assert observed["rectangularString"]["result"] == "System.String[,]"
    assert observed["rankThreeString"]["result"] == "System.String[,,]"
    assert observed["arrayOfListString"]["result"].endswith("]]" + "[]")
    assert observed["rankOneNonVector"]["result"] == "System.String[*]"
    make_array = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMakeArrayBehavior"]
    assert [make_array[key] for key in ("vector", "rankOne", "rankTwo", "nestedVector")] == [
        "System.String[]", "System.String[*]", "System.String[,]", "System.String[][]",
    ]
    assert make_array["genericVector"] == observed["arrayOfListString"]["result"]
    assert make_array["rankZeroError"] == "System.IndexOutOfRangeException"
    assert observed["stringByRef"]["result"] == "System.String&"
    assert observed["stringArrayByRef"]["result"] == "System.String[]&"
    by_ref = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedByRefBehavior"]
    assert by_ref == {
        "name": "System.String&", "isByRef": True, "element": "System.String",
        "arrayName": "System.String[]&", "repeatSameIdentity": True,
        "doubleByRefError": "System.TypeLoadException",
    }
    assert observed["stringPointer"]["result"] == "System.String*"
    assert observed["intPointer"]["result"] == "System.Int32*"
    pointer = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPointerBehavior"]
    assert pointer == {
        "name": "System.String*", "intName": "System.Int32*", "isPointer": True,
        "element": "System.String", "repeatSameIdentity": True,
        "pointerToPointer": "System.String**", "byRefError": "System.TypeLoadException",
    }
    names = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedTypeNames"]
    assert [item["Name"] for item in names] == [
        "String", "Int32", "List`1", "List`1", "String[]", "String[,]", "String&", "String*", "T",
    ]
    assert [item["Namespace"] for item in names] == [
        "System", "System", "System.Collections.Generic", "System.Collections.Generic",
        "System", "System", "System", "System", "System.Collections.Generic",
    ]
    assert names[-1]["FullName"] is None
    assert names[3]["FullName"] == observed["listStringSimple"]["result"]
    corelib_identity = ", System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e"
    assert [item["AssemblyQualifiedName"] for item in names] == [
        None if item["FullName"] is None else item["FullName"] + corelib_identity
        for item in names
    ]
    assert [item["roundTripSameReference"] for item in names] == [True] * 8 + [False]
    selected_corelib_types = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["types"]
    assert len(selected_corelib_types) == 30
    assert all(item["qualifiedNameRoundTripSameReference"] and
               item["assemblyQualifiedName"] == item["fullName"] + corelib_identity
               for item in selected_corelib_types)
    corelib_case = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedCoreLibCaseLookup"]
    assert len(corelib_case) == 30
    assert all(item["lowerSensitive"] == {"result": None, "exception": None, "paramName": None}
               and item["lowerInsensitive"] == {
                   "result": item["fullName"], "exception": None, "paramName": None}
               for item in corelib_case)
    assert all(item["lowerQualifiedSensitive"] == {
                   "result": None, "exception": None, "paramName": None}
               and item["lowerQualifiedInsensitive"] == {
                   "result": item["fullName"], "exception": None, "paramName": None}
               for item in corelib_case)
    assert all(item[mode] == {"result": None, "exception": "System.TypeLoadException", "paramName": None}
               for item in corelib_case
               for mode in ("lowerThrowSensitive", "lowerQualifiedThrowSensitive"))
    assert all(item[mode] == {"result": item["fullName"], "exception": None, "paramName": None}
               for item in corelib_case
               for mode in ("lowerThrowInsensitive", "lowerQualifiedThrowInsensitive"))
    dictionary_names = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDictionaryQualifiedRoundTrip"]
    assert len(dictionary_names) == 5
    assert all(item["sameReference"] and item["AssemblyQualifiedName"] ==
               item["FullName"] + corelib_identity for item in dictionary_names)
    assert all(item["lowerSensitive"] == {"result": None, "exception": None, "paramName": None}
               and item["lowerInsensitiveSameReference"] for item in dictionary_names)
    assert dictionary_names[0]["FullName"] == "System.Collections.Generic.Dictionary`2"
    assert "[[System.String, " in dictionary_names[1]["FullName"]
    assert "[[System.Int32, " in dictionary_names[2]["FullName"]
    assert "],[System.String, " in dictionary_names[3]["FullName"]
    assert "],[System.Int32, " in dictionary_names[4]["FullName"]
    nested_names = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedGenericQualifiedRoundTrip"]
    assert len(nested_names) == 3
    assert all(item["sameReference"] and item["AssemblyQualifiedName"] ==
               item["FullName"] + corelib_identity for item in nested_names)
    assert all(item["lowerSensitive"] == {"result": None, "exception": None, "paramName": None}
               and item["lowerInsensitiveSameReference"] for item in nested_names)
    assert nested_names[0]["FullName"].startswith("System.Collections.Generic.List`1[[System.Collections.Generic.List`1[[")
    assert all(item["FullName"].startswith("System.Collections.Generic.Dictionary`2[[")
               for item in nested_names[1:])
    binding_flags = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedBindingFlagsValues"]
    assert binding_flags == [
        {"name": name, "value": value} for name, value in (
            ("Default", 0), ("IgnoreCase", 1), ("DeclaredOnly", 2),
            ("Instance", 4), ("Static", 8), ("Public", 16), ("NonPublic", 32),
            ("FlattenHierarchy", 64), ("InvokeMethod", 256),
            ("CreateInstance", 512), ("GetField", 1024), ("SetField", 2048),
            ("GetProperty", 4096), ("SetProperty", 8192),
            ("PutDispProperty", 16384), ("PutRefDispProperty", 32768),
            ("ExactBinding", 65536), ("SuppressChangeType", 131072),
            ("OptionalParamBinding", 262144), ("IgnoreReturn", 16777216),
            ("DoNotWrapExceptions", 33554432),
        )
    ]
    binding_combination = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedBindingCombinationBehavior"]
    assert binding_combination == {"value": 20, "hasPublic": True,
                                   "hasInstance": True, "named": False, "enumName": None}
    member_type = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMemberTypeBehavior"]
    assert member_type["enumValues"] == [
        {"name": name, "value": value} for name, value in (
            ("Constructor", 1), ("Event", 2), ("Field", 4), ("Method", 8),
            ("Property", 16), ("TypeInfo", 32), ("Custom", 64),
            ("NestedType", 128), ("All", 191),
        )
    ]
    assert all(member_type[key] == "TypeInfo" for key in
               ("stringType", "arrayType", "openGeneric", "genericParameter"))
    assert member_type["memberTypeGetterAbstract"]
    member_type_combination = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMemberTypeCombinationBehavior"]
    assert member_type_combination == {"value": 24, "hasMethod": True,
                                       "hasProperty": True, "named": False, "enumName": None}
    owners = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMemberOwnerBehavior"]
    assert len(owners) == 7
    assert all(item["declaringType"] is None and item["reflectedType"] is None
               for index, item in enumerate(owners) if index != 3)
    assert owners[3]["name"] == "T"
    assert owners[3]["declaringType"] == owners[3]["reflectedType"] == "System.Collections.Generic.List`1"
    collectibility = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMemberCollectibilityBehavior"]
    assert collectibility == {"stringType": False, "genericListType": False,
        "disposableMethod": False, "stringCharsProperty": False}
    metadata_definition = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMemberMetadataDefinitionBehavior"]
    assert metadata_definition == {"sameMethod": True, "differentMethod": False,
        "methodVsType": False, "sameProperty": True,
        "nullError": "System.ArgumentNullException", "nullParameter": "other"}
    nested_owners = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedOwnerBehavior"]
    assert [row["declaringType"] for row in nested_owners] == [
        None, "System.Collections.Generic.List`1", "System.Collections.Generic.Dictionary`2",
        "System.Collections.Generic.List`1", None,
    ]
    assert all(row["reflectedType"] == row["declaringType"] for row in nested_owners)
    interface_misses = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInterfaceMemberMissBehavior"]
    assert len(interface_misses) == 5 and all(
        row["query"] == {"members": [], "exception": None, "paramName": None}
        for row in interface_misses)
    interface_members = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInterfaceMemberEnumeration"]
    assert [(row["owner"], row["members"][0]["name"])
            for row in interface_members] == [
        ("System.IDisposable", "Dispose"),
        ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"),
        ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(len(row["members"]) == 1 and row["members"][0]["kind"] == "Method"
               and row["members"][0]["declaring"] == row["owner"]
               and row["members"][0]["reflected"] == row["owner"]
               for row in interface_members)
    flagged_members = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMembersFlagsBehavior"]
    assert [(row["owner"], row["publicInstance"][0]["name"])
            for row in flagged_members] == [
        ("System.IDisposable", "Dispose"),
        ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"),
        ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(len(row["publicInstance"]) == 1
               and row["publicInstance"][0]["kind"] == "Method"
               and row["publicOnly"] == [] and row["nonPublicInstance"] == []
               for row in flagged_members)
    method_info = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodInfoBehavior"]
    assert method_info == {
        "methodBase": {"name": "System.Reflection.MethodBase",
                       "parent": "System.Reflection.MemberInfo", "isAbstract": True},
        "methodInfo": {"name": "System.Reflection.MethodInfo",
                       "parent": "System.Reflection.MethodBase", "isAbstract": True},
        "disposableMethods": [{"name": "Dispose", "kind": "Method"}],
        "publicOnly": [], "nonPublicInstance": [],
    }
    method_returns = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodReturnBehavior"]
    assert method_returns["voidType"] == {"name": "Void", "fullName": "System.Void",
        "baseType": "System.ValueType", "isValueType": True, "isPrimitive": True}
    assert [(row["owner"], row["name"], row["returnType"])
            for row in method_returns["methods"]] == [
        ("System.IDisposable", "Dispose", "System.Void"),
        ("System.IComparable", "CompareTo", "System.Int32"),
        ("System.IFormattable", "ToString", "System.String"),
        ("System.IFormatProvider", "GetFormat", "System.Object"),
    ]
    parameter_info = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedParameterInfoBehavior"]
    assert parameter_info["type"] == {"name": "System.Reflection.ParameterInfo",
        "parent": "System.Object", "isAbstract": False}
    assert [(row["owner"], row["name"], row["parameters"])
            for row in parameter_info["methods"]] == [
        ("System.IDisposable", "Dispose", []),
        ("System.IComparable", "CompareTo", [
            {"name": "obj", "type": "System.Object", "position": 0}]),
        ("System.IFormattable", "ToString", [
            {"name": "format", "type": "System.String", "position": 0},
            {"name": "formatProvider", "type": "System.IFormatProvider", "position": 1}]),
        ("System.IFormatProvider", "GetFormat", [
            {"name": "formatType", "type": "System.Type", "position": 0}]),
    ]
    return_parameters = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedReturnParameterBehavior"]
    assert [(row["owner"], row["name"], row["parameter"])
            for row in return_parameters] == [
        ("System.IDisposable", "Dispose", {"name": None, "type": "System.Void", "position": -1}),
        ("System.IComparable", "CompareTo", {"name": None, "type": "System.Int32", "position": -1}),
        ("System.IFormattable", "ToString", {"name": "", "type": "System.String", "position": -1}),
        ("System.IFormatProvider", "GetFormat", {"name": None, "type": "System.Object", "position": -1}),
    ]
    parameter_members = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedParameterMemberBehavior"]
    assert [(row["owner"], row["name"], len(row["parameterMembers"]))
            for row in parameter_members] == [
        ("System.IDisposable", "Dispose", 0), ("System.IComparable", "CompareTo", 1),
        ("System.IFormattable", "ToString", 2), ("System.IFormatProvider", "GetFormat", 1),
    ]
    assert all(row["returnMember"] == row["name"] and row["returnSameReference"]
               and all(parameter == {"name": row["name"], "sameReference": True}
                       for parameter in row["parameterMembers"])
               for row in parameter_members)
    parameter_flags = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedParameterFlagBehavior"]
    assert [len(row["parameters"]) for row in parameter_flags] == [1, 2, 3, 2]
    assert [row["parameters"][-1]["position"] for row in parameter_flags] == [-1] * 4
    assert all(not parameter["isOptional"] and not parameter["hasDefaultValue"]
               and not any(parameter[key] for key in ("isIn", "isOut", "isRetval", "isLcid"))
               for row in parameter_flags for parameter in row["parameters"])
    default_values = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedParameterDefaultValueBehavior"]
    assert [len(row["parameters"]) for row in default_values] == [1, 2, 3, 2]
    assert all(parameter["defaultType"] == "System.DBNull"
               and parameter["rawDefaultType"] == "System.DBNull"
               and parameter["sameReference"]
               for row in default_values for parameter in row["parameters"])
    parameter_attributes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedParameterAttributeBehavior"]
    assert parameter_attributes["values"] == [
        {"name": name, "value": value} for name, value in (
            ("None", 0), ("In", 1), ("Out", 2), ("Lcid", 4), ("Retval", 8),
            ("Optional", 16), ("HasDefault", 4096), ("HasFieldMarshal", 8192),
            ("Reserved3", 16384), ("Reserved4", 32768), ("ReservedMask", 61440))]
    assert [len(row["attributes"]) for row in parameter_attributes["methods"]] == [1, 2, 3, 2]
    assert all(attribute["value"] == 0 and attribute["text"] == "None"
               for row in parameter_attributes["methods"]
               for attribute in row["attributes"])
    custom_attributes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedParameterCustomAttributeBehavior"]
    assert [len(row["parameters"]) for row in custom_attributes] == [1, 2, 3, 2]
    assert all(parameter["direct"] == [] and parameter["inherited"] == []
               for row_index, row in enumerate(custom_attributes)
               for parameter_index, parameter in enumerate(row["parameters"])
               if (row_index, parameter_index) != (2, 2))
    assert custom_attributes[2]["parameters"][2] == {
        "position": -1,
        "direct": [{"type": "System.Runtime.CompilerServices.NullableAttribute",
                    "baseType": "System.Attribute", "flags": "AQ=="}],
        "inherited": ["System.Runtime.CompilerServices.NullableAttribute"],
    }
    attribute_instance = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAttributeInstanceBehavior"]
    assert attribute_instance == {"sameReference": False, "equalsRepeat": True,
        "matchesRepeat": True,
        "typeId": "System.Runtime.CompilerServices.NullableAttribute",
        "typeIdEqualsType": True, "isDefault": False}
    nullable_constructor = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNullableAttributeConstructorBehavior"]
    assert nullable_constructor == {
        "constructors": [
            {"parameters": ["System.Byte"], "isPublic": True},
            {"parameters": ["System.Byte[]"], "isPublic": True},
        ],
        "sameArrayReference": True, "firstFlagAfterInputMutation": 3,
        "secondFlag": 2,
    }
    attribute_filter = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedParameterAttributeFilterBehavior"]
    assert attribute_filter == {
        "returnBase": ["System.Runtime.CompilerServices.NullableAttribute"],
        "returnExact": ["System.Runtime.CompilerServices.NullableAttribute"],
        "inputBase": [], "nullError": "System.ArgumentNullException",
        "nullParameter": "attributeType",
    }
    attribute_defined = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedParameterIsDefinedBehavior"]
    assert attribute_defined == {
        "returnBase": True, "returnExact": True, "inputBase": False,
        "nullError": "System.ArgumentNullException", "nullParameter": "attributeType",
    }
    parameter_modifiers = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedParameterModifierBehavior"]
    assert [len(row["parameters"]) for row in parameter_modifiers] == [1, 2, 3, 2]
    assert all(parameter["optional"] == [] and parameter["required"] == []
               for row in parameter_modifiers for parameter in row["parameters"])
    parameter_texts = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedParameterTextBehavior"]
    assert [[parameter["text"] for parameter in row["parameters"]]
            for row in parameter_texts] == [
        ["Void"], ["System.Object obj", "Int32"],
        ["System.String format", "System.IFormatProvider formatProvider", "System.String "],
        ["System.Type formatType", "System.Object"],
    ]
    method_flags = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodFlagBehavior"]
    assert [(row["owner"], row["name"]) for row in method_flags] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(row["isPublic"] and not row["isStatic"]
               and row["isAbstract"] and row["isVirtual"] and not row["isFinal"]
               for row in method_flags)
    generic_methods = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedGenericMethodBehavior"]
    assert [(row["owner"], row["name"]) for row in generic_methods] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(not row["isGenericMethod"] and not row["isGenericMethodDefinition"]
               and not row["isConstructedGenericMethod"]
               and not row["containsGenericParameters"] and row["genericArguments"] == []
               for row in generic_methods)
    classifications = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodClassificationBehavior"]
    assert [(row["owner"], row["name"]) for row in classifications] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(not any(row[key] for key in
                       ("isSpecialName", "isConstructor", "isPrivate", "isFamily",
                        "isFamilyAndAssembly", "isFamilyOrAssembly", "isAssembly"))
               and row["isHideBySig"] for row in classifications)
    calling_conventions = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedCallingConventionBehavior"]
    assert calling_conventions["values"] == [
        {"name": name, "value": value} for name, value in
        (("Standard", 1), ("VarArgs", 2), ("Any", 3),
         ("HasThis", 32), ("ExplicitThis", 64))]
    assert [(row["owner"], row["name"]) for row in calling_conventions["methods"]] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(row["value"] == 33 and row["standard"] and row["hasThis"]
               for row in calling_conventions["methods"])
    base_definitions = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodBaseDefinitionBehavior"]
    assert [(row["owner"], row["name"]) for row in base_definitions] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(row["baseName"] == row["name"] and row["baseOwner"] == row["owner"]
               and row["sameReference"] for row in base_definitions)
    method_security = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodSecurityBehavior"]
    assert [(row["owner"], row["name"]) for row in method_security] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(row["isSecurityCritical"] and not row["isSecuritySafeCritical"]
               and not row["isSecurityTransparent"] for row in method_security)
    implementations = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodImplementationBehavior"]
    assert implementations["values"] == [
        {"name": name, "value": value} for name, value in (
            ("IL", 0), ("Managed", 0), ("Native", 1), ("OPTIL", 2),
            ("CodeTypeMask", 3), ("Runtime", 3), ("ManagedMask", 4),
            ("Unmanaged", 4), ("NoInlining", 8), ("ForwardRef", 16),
            ("Synchronized", 32), ("NoOptimization", 64), ("PreserveSig", 128),
            ("AggressiveInlining", 256), ("AggressiveOptimization", 512),
            ("InternalCall", 4096), ("Async", 8192), ("MaxMethodImplVal", 65535))]
    assert [(row["owner"], row["name"]) for row in implementations["methods"]] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(row["value"] == 0 and row["text"] == "IL"
               for row in implementations["methods"])
    method_texts = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodSignatureTextBehavior"]
    assert [(row["owner"], row["name"], row["text"]) for row in method_texts] == [
        ("System.IDisposable", "Dispose", "Void Dispose()"),
        ("System.IComparable", "CompareTo", "Int32 CompareTo(System.Object)"),
        ("System.IFormattable", "ToString",
         "System.String ToString(System.String, System.IFormatProvider)"),
        ("System.IFormatProvider", "GetFormat", "System.Object GetFormat(System.Type)"),
    ]
    method_attributes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodCustomAttributeBehavior"]
    assert [(row["owner"], row["name"]) for row in method_attributes] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(row["direct"] == [] and row["inherited"] == []
               for row in method_attributes)
    method_attribute_filter = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodAttributeFilterBehavior"]
    assert method_attribute_filter == {"direct": [], "inherited": [],
        "nullError": "System.ArgumentNullException", "nullParameter": "attributeType"}
    method_defined = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodIsDefinedBehavior"]
    assert method_defined == {"direct": False, "inherited": False,
        "nullError": "System.ArgumentNullException", "nullParameter": "attributeType"}
    nongeneric_errors = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNongenericMethodErrorBehavior"]
    assert [(row["owner"], row["name"]) for row in nongeneric_errors] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(row["definitionError"] == "System.InvalidOperationException"
               and row["instantiationError"] == "System.InvalidOperationException"
               and row["nullInstantiationError"] == "System.ArgumentNullException"
               and row["nullInstantiationParameter"] == "methodInstantiation"
               and row["nonemptyInstantiationError"] == "System.InvalidOperationException"
               for row in nongeneric_errors)
    abstract_bodies = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAbstractMethodBodyBehavior"]
    assert abstract_bodies["type"] == {"name": "System.Reflection.MethodBody",
        "parent": "System.Object", "isAbstract": False}
    assert [(row["owner"], row["name"]) for row in abstract_bodies["methods"]] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(not row["hasBody"] for row in abstract_bodies["methods"])
    method_names = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodNameBehavior"]
    assert [(row["owner"], row["query"]["result"])
            for row in method_names[:4]] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(row["query"]["kind"] == "Method"
               and row["query"]["exception"] is None for row in method_names[:4])
    assert all(row["query"] == {"result": None, "kind": None,
                                 "exception": None, "paramName": None}
               for row in method_names[4:6])
    assert method_names[6]["query"] == {"result": None, "kind": None,
        "exception": "System.ArgumentNullException", "paramName": "name"}
    flagged_method = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodFlagsBehavior"]
    for key in ("positive", "ignoreCase"):
        assert flagged_method[key] == {"result": "Dispose", "kind": "Method",
                                       "exception": None, "paramName": None}
    for key in ("publicOnly", "nonPublic", "missing"):
        assert flagged_method[key] == {"result": None, "kind": None,
                                       "exception": None, "paramName": None}
    assert flagged_method["nullName"] == {"result": None, "kind": None,
        "exception": "System.ArgumentNullException", "paramName": "name"}
    default_methods = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodEnumerationBehavior"]
    assert [(row["owner"], row["methods"][0]["name"])
            for row in default_methods] == [
        ("System.IDisposable", "Dispose"), ("System.IComparable", "CompareTo"),
        ("System.IFormattable", "ToString"), ("System.IFormatProvider", "GetFormat"),
    ]
    assert all(len(row["methods"]) == 1
               and row["methods"][0]["kind"] == "Method"
               and row["methods"][0]["declaring"] == row["owner"]
               for row in default_methods)
    method_parameters = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodParameterBehavior"]
    for key, name in (("dispose", "Dispose"), ("compareTo", "CompareTo"),
                      ("toString", "ToString"), ("getFormat", "GetFormat")):
        assert method_parameters[key] == {"result": name, "kind": "Method",
                                          "exception": None, "paramName": None}
    assert method_parameters["wrongTypes"] == {"result": None, "kind": None,
                                                 "exception": None, "paramName": None}
    for key, parameter in (("nullName", "name"), ("nullArray", "types"),
                           ("nullElement", "types")):
        assert method_parameters[key] == {"result": None, "kind": None,
            "exception": "System.ArgumentNullException", "paramName": parameter}
    flagged_parameters = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMethodFlagsParameterBehavior"]
    for key in ("dispose", "ignoreCase"):
        assert flagged_parameters[key] == {"result": "Dispose", "kind": "Method",
                                           "exception": None, "paramName": None}
    for key in ("publicOnly", "wrongTypes"):
        assert flagged_parameters[key] == {"result": None, "kind": None,
                                           "exception": None, "paramName": None}
    for key, parameter in (("nullName", "name"), ("nullArray", "types")):
        assert flagged_parameters[key] == {"result": None, "kind": None,
            "exception": "System.ArgumentNullException", "paramName": parameter}
    member_name = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMemberNameBehavior"]
    for key, name in (("stringChars", "Chars"), ("listItem", "Item")):
        assert member_name[key] == {"members": [{"name": name, "kind": "Property"}],
                                    "exception": None, "paramName": None}
    assert member_name["disposableDispose"] == {
        "members": [{"name": "Dispose", "kind": "Method"}],
        "exception": None, "paramName": None,
    }
    for key in ("stringLower", "stringMissing", "objectMissing"):
        assert member_name[key] == {"members": [], "exception": None, "paramName": None}
    assert member_name["nullName"] == {
        "members": None, "exception": "System.ArgumentNullException", "paramName": "name",
    }
    member_flags = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMemberFlagsBehavior"]
    for key in ("stringChars", "ignoreCase"):
        assert member_flags[key] == {
            "members": [{"name": "Chars", "kind": "Property"}],
            "exception": None, "paramName": None,
        }
    assert member_flags["disposableDispose"] == {
        "members": [{"name": "Dispose", "kind": "Method"}],
        "exception": None, "paramName": None,
    }
    for key in ("publicOnly", "instanceOnly", "nonPublic"):
        assert member_flags[key] == {"members": [], "exception": None, "paramName": None}
    assert member_flags["nullName"] == {
        "members": None, "exception": "System.ArgumentNullException", "paramName": "name",
    }
    member_kinds = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMemberKindsBehavior"]
    for key in ("property", "all"):
        assert member_kinds[key] == {"members": [{"name": "Chars", "kind": "Property"}],
                                     "exception": None, "paramName": None}
    assert member_kinds["disposeMethod"] == {
        "members": [{"name": "Dispose", "kind": "Method"}],
        "exception": None, "paramName": None,
    }
    for key in ("methodMiss", "disposePropertyMiss"):
        assert member_kinds[key] == {"members": [], "exception": None, "paramName": None}
    assert member_kinds["nullName"] == {
        "members": None, "exception": "System.ArgumentNullException", "paramName": "name",
    }
    default_members = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDefaultMemberBehavior"]
    assert [row["members"] for row in default_members[:3]] == [[], [], []]
    assert [row["members"][0]["name"] for row in default_members[3:]] == ["Chars", "Item", "Item"]
    assert all(len(row["members"]) == 1
               and row["members"][0]["kind"] == "Property"
               and row["members"][0]["declaring"] == row["name"]
               and row["members"][0]["reflected"] == row["name"]
               for row in default_members[3:])
    custom_modifiers = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedCustomModifierBehavior"]
    assert len(custom_modifiers) == 7 and all(
        row["optional"] == [] and row["required"] == [] for row in custom_modifiers)
    security_flags = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSecurityTransparencyBehavior"]
    assert len(security_flags) == 10 and all(
        row["isSecurityCritical"] and not row["isSecuritySafeCritical"]
        and not row["isSecurityTransparent"] for row in security_flags)
    non_function_pointer = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNonFunctionPointerQueryBehavior"]
    assert [row["name"] for row in non_function_pointer] == ["System.String", "System.String*"]
    assert all(row[key] == "System.InvalidOperationException"
               for row in non_function_pointer
               for key in ("returnTypeError", "parameterTypesError", "callingConventionsError"))
    function_pointer_flags = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedFunctionPointerFlagBehavior"]
    assert len(function_pointer_flags) == 8 and all(
        not row["isFunctionPointer"] and not row["isUnmanagedFunctionPointer"]
        for row in function_pointer_flags)
    interop_flags = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInteropTypeFlagBehavior"]
    assert len(interop_flags) == 9 and all(
        not any(row[key] for key in ("isImport", "isCOMObject", "isContextful",
                                     "isMarshalByRef", "isSignatureType"))
        for row in interop_flags)
    layout = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedLayoutBehavior"]
    assert [(row["isAutoLayout"], row["isLayoutSequential"], row["isExplicitLayout"])
            for row in layout] == [
        (True, False, False), (False, True, False),
        *[(True, False, False)] * 8,
    ]
    character_set = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedCharacterSetBehavior"]
    assert len(character_set) == 10 and all(
        row["isAnsiClass"] and not row["isUnicodeClass"] and not row["isAutoClass"]
        for row in character_set)
    special_name = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSpecialNameBehavior"]
    assert len(special_name) == 7 and all(not row["isSpecialName"] for row in special_name)
    serializable = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSerializableBehavior"]
    assert [row["isSerializable"] for row in serializable] == [
        True, True, True, False, False, True, True, True,
        False, True, True, False,
    ]
    not_public = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNotPublicBehavior"]
    assert [(row["isPublic"], row["isNotPublic"], row["isNested"])
            for row in not_public] == [
        (True, False, False), (False, True, False), (False, False, True),
        (True, False, False), (True, False, True),
    ]
    nested_names = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedNameBehavior"]
    assert nested_names == [
        {"name": name, "fullName": full_name, "namespace": "System.Collections.Generic"}
        for name, full_name in (
            ("Entry", "System.Collections.Generic.Dictionary`2+Entry"),
            ("KeyCollection", "System.Collections.Generic.Dictionary`2+KeyCollection"),
            ("Enumerator", "System.Collections.Generic.List`1+Enumerator"),
        )
    ]
    nested_definition_text = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedDefinitionStringBehavior"]
    assert [row["text"] for row in nested_definition_text] == [
        "System.Collections.Generic.Dictionary`2+Entry[TKey,TValue]",
        "System.Collections.Generic.Dictionary`2+Entry[TKey,TValue][]",
    ]
    nested_lookup = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedLookupBehavior"]
    assert [row["resolved"] for row in nested_lookup] == [
        "System.Collections.Generic.Dictionary`2+Entry",
        "System.Collections.Generic.Dictionary`2+Entry[]",
        "System.Collections.Generic.Dictionary`2+Entry",
    ]
    nested_name_only = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedNameOnlyQueryBehavior"]
    enum_names = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEnumNamesBehavior"]
    number_style_values = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNumberStylesFullValues"]
    assert [row["value"] for row in number_style_values] == [
        0, 1, 2, 4, 7, 8, 16, 32, 64, 111, 128, 167, 256, 383, 511,
        512, 515, 1024, 1027,
    ]
    assert [row["name"] for row in number_style_values] == enum_names["numberStyles"]["names"]
    enum_defined = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEnumDefinedBehavior"]
    for key in ("enumValue", "integerValue", "exactName"):
        assert enum_defined[key] == {"result": True, "exception": None, "paramName": None}
    for key in ("lowerName", "missingName", "missingValue"):
        assert enum_defined[key] == {"result": False, "exception": None, "paramName": None}
    assert enum_defined["wrongEnumType"] == {"result": None, "exception": "System.ArgumentException", "paramName": None}
    assert enum_defined["nullValue"] == {"result": None, "exception": "System.ArgumentNullException", "paramName": "value"}
    assert enum_defined["nonEnumOwner"] == {"result": None, "exception": "System.ArgumentException", "paramName": "enumType"}
    for key in ("longValue", "byteValue"):
        assert enum_defined[key] == {"result": None, "exception": "System.ArgumentException", "paramName": None}
    enum_name = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEnumNameBehavior"]
    for key in ("enumValue", "integerValue", "longValue", "byteValue"):
        assert enum_name[key] == {"result": "Empty", "exception": None, "paramName": None}
    for key in ("missingValue", "wrongEnumType"):
        assert enum_name[key] == {"result": None, "exception": None, "paramName": None}
    assert enum_name["stringValue"] == {"result": None, "exception": "System.ArgumentException", "paramName": "value"}
    assert enum_name["nullValue"] == {"result": None, "exception": "System.ArgumentNullException", "paramName": "value"}
    assert enum_name["nonEnumOwner"] == {"result": None, "exception": "System.ArgumentException", "paramName": "enumType"}
    enum_values = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEnumValuesBehavior"]
    for key, array_type, numeric_values in (
            ("typeCode", "System.TypeCode[]", list(range(17)) + [18]),
            ("memberTypes", "System.Reflection.MemberTypes[]", [1, 2, 4, 8, 16, 32, 64, 128, 191]),
            ("numberStyles", "System.Globalization.NumberStyles[]", [row["value"] for row in number_style_values])):
        assert enum_values[key] == {
            "arrayType": array_type, "names": enum_names[key]["names"],
            "values": numeric_values, "exception": None, "paramName": None,
        }
    assert enum_values["nonEnum"] == {
        "arrayType": None, "names": None, "values": None,
        "exception": "System.ArgumentException", "paramName": "enumType",
    }
    underlying_values = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEnumUnderlyingValuesBehavior"]
    for key in ("typeCode", "memberTypes", "numberStyles"):
        assert underlying_values[key] == {
            "arrayType": "System.Int32[]", "values": enum_values[key]["values"],
            "exception": None, "paramName": None,
        }
    assert underlying_values["nonEnum"] == {
        "arrayType": None, "values": None,
        "exception": "System.ArgumentException", "paramName": "enumType",
    }
    underlying_type = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEnumUnderlyingTypeBehavior"]
    for key in ("typeCode", "memberTypes"):
        assert underlying_type[key] == {"result": "System.Int32", "exception": None, "paramName": None}
    assert underlying_type["nonEnum"] == {
        "result": None, "exception": "System.ArgumentException", "paramName": "enumType",
    }
    assert enum_names == {
        "typeCode": {"names": ["Empty", "Object", "DBNull", "Boolean", "Char", "SByte", "Byte",
                               "Int16", "UInt16", "Int32", "UInt32", "Int64", "UInt64", "Single",
                               "Double", "Decimal", "DateTime", "String"],
                     "exception": None, "paramName": None},
        "memberTypes": {"names": ["Constructor", "Event", "Field", "Method", "Property",
                                  "TypeInfo", "Custom", "NestedType", "All"],
                        "exception": None, "paramName": None},
        "genericParameterAttributes": {"names": ["None", "Covariant", "Contravariant",
            "VarianceMask", "ReferenceTypeConstraint", "NotNullableValueTypeConstraint",
            "DefaultConstructorConstraint", "SpecialConstraintMask", "AllowByRefLike"],
            "exception": None, "paramName": None},
        "numberStyles": {"names": ["None", "AllowLeadingWhite", "AllowTrailingWhite",
            "AllowLeadingSign", "Integer", "AllowTrailingSign", "AllowParentheses",
            "AllowDecimalPoint", "AllowThousands", "Number", "AllowExponent", "Float",
            "AllowCurrencySymbol", "Currency", "Any", "AllowHexSpecifier", "HexNumber",
            "AllowBinarySpecifier", "BinaryNumber"],
                         "exception": None, "paramName": None},
        "nonEnum": {"names": None, "exception": "System.ArgumentException", "paramName": "enumType"},
    }
    assert nested_name_only == {
        "positive": {"result": "System.Collections.Generic.Dictionary`2+KeyCollection", "exception": None, "paramName": None},
        "lowerMiss": {"result": None, "exception": None, "paramName": None},
        "missing": {"result": None, "exception": None, "paramName": None},
        "nullName": {"result": None, "exception": "System.ArgumentNullException", "paramName": "fullname"},
    }
    nested_enumeration = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedEnumerationBehavior"]
    assert nested_enumeration == [
        {"owner": "System.Collections.Generic.List`1", "publicNested": ["System.Collections.Generic.List`1+Enumerator"]},
        {"owner": "System.Object", "publicNested": []},
        {"owner": "System.Collections.Generic.Dictionary`2", "publicNested": [
            "System.Collections.Generic.Dictionary`2+AlternateLookup`1",
            "System.Collections.Generic.Dictionary`2+Enumerator",
            "System.Collections.Generic.Dictionary`2+KeyCollection",
            "System.Collections.Generic.Dictionary`2+ValueCollection",
        ]},
    ]
    constructed_nested = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedConstructedNestedQueryBehavior"]
    assert constructed_nested == {
        "open": "System.Collections.Generic.Dictionary`2+KeyCollection",
        "closed": "System.Collections.Generic.Dictionary`2+KeyCollection",
        "sameReference": True,
        "closedEnumeration": nested_enumeration[2]["publicNested"],
    }
    nonpublic_nested = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNonpublicNestedQueryBehavior"]
    assert nonpublic_nested == {
        "publicOnly": {"result": None, "exception": None, "paramName": None},
        "nonpublic": "System.Collections.Generic.Dictionary`2+Entry",
        "publicEnumerationContainsEntry": False,
    }
    element_nested = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedElementNestedQueryBehavior"]
    assert element_nested == [
        {"owner": owner,
         "query": {"result": None, "exception": None, "paramName": None},
         "enumerationLength": 0}
        for owner in ("System.Collections.Generic.Dictionary`2[]",
                      "System.Collections.Generic.Dictionary`2&",
                      "System.Collections.Generic.Dictionary`2*", "TKey")
    ]
    nested_visibility = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedPublicVisibilityBehavior"]
    assert [(row["isPublic"], row["isNestedPublic"], row["isVisible"])
            for row in nested_visibility] == [
        (True, False, True), (True, False, True), (False, False, False),
        (False, True, True), (False, True, True),
    ]
    generic_visibility = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedGenericArgumentVisibilityBehavior"]
    assert [row["isVisible"] for row in generic_visibility] == [True, False, False]
    parent_visibility = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedParentVisibilityBehavior"]
    assert [(row["isPublic"], row["isNestedPublic"], row["isVisible"], row["declaringVisible"])
            for row in parent_visibility] == [
        (False, True, True, True), (False, True, False, False),
    ]
    nested_arrays = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedArrayVisibilityBehavior"]
    assert [(row["isPublic"], row["isVisible"], row["isNested"])
            for row in nested_arrays] == [(True, True, False), (True, False, False)]
    nested_qualified = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedQualifiedRoundTripBehavior"]
    assert [row["sameReference"] for row in nested_qualified] == [True, True]
    assert [row["qualified"].split(", ", 1)[0] for row in nested_qualified] == [
        "System.Collections.Generic.Dictionary`2+Entry",
        "System.Collections.Generic.Dictionary`2+Entry[]",
    ]
    nested_constructed = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedConstructedIdentityBehavior"]
    assert len(nested_constructed) == 1
    assert nested_constructed[0]["text"] == "System.Collections.Generic.Dictionary`2+Entry[System.String,System.Int32]"
    assert nested_constructed[0]["isConstructed"]
    assert nested_constructed[0]["definition"] == "System.Collections.Generic.Dictionary`2+Entry"
    assert nested_constructed[0]["arguments"] == ["System.String", "System.Int32"]
    nested_constructed_lookup = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedConstructedLookupBehavior"]
    assert len(nested_constructed_lookup) == 1
    assert nested_constructed_lookup[0]["name"].startswith(
        "System.Collections.Generic.Dictionary`2+Entry[[System.String,")
    assert nested_constructed_lookup[0]["fullNameSameReference"]
    assert nested_constructed_lookup[0]["qualifiedSameReference"]
    nested_array_lookup = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedConstructedArrayLookupBehavior"]
    assert len(nested_array_lookup) == 1
    assert nested_array_lookup[0]["name"].endswith("]][]")
    assert nested_array_lookup[0]["fullNameSameReference"]
    assert nested_array_lookup[0]["qualifiedSameReference"]
    nested_rectangle_lookup = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedConstructedRectangleLookupBehavior"]
    assert len(nested_rectangle_lookup) == 1
    assert nested_rectangle_lookup[0]["name"].endswith("]][,]")
    assert nested_rectangle_lookup[0]["fullNameSameReference"]
    assert nested_rectangle_lookup[0]["qualifiedSameReference"]
    nested_rank_three_lookup = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedConstructedRankThreeLookupBehavior"]
    assert len(nested_rank_three_lookup) == 1
    assert nested_rank_three_lookup[0]["name"].endswith("]][,,]")
    assert nested_rank_three_lookup[0]["fullNameSameReference"]
    assert nested_rank_three_lookup[0]["qualifiedSameReference"]
    nested_variable_lookup = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedConstructedVariableLookupBehavior"]
    assert len(nested_variable_lookup) == 1
    assert nested_variable_lookup[0]["name"].endswith("]][*]")
    assert nested_variable_lookup[0]["fullNameSameReference"]
    assert nested_variable_lookup[0]["qualifiedSameReference"]
    nested_byref_lookup = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedConstructedByRefLookupBehavior"]
    assert len(nested_byref_lookup) == 1
    assert nested_byref_lookup[0]["name"].endswith("]]&")
    assert nested_byref_lookup[0]["fullNameSameReference"]
    assert nested_byref_lookup[0]["qualifiedSameReference"]
    nested_pointer_lookup = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedConstructedPointerLookupBehavior"]
    assert len(nested_pointer_lookup) == 1
    assert nested_pointer_lookup[0]["name"].endswith("]]*")
    assert nested_pointer_lookup[0]["fullNameSameReference"]
    assert nested_pointer_lookup[0]["qualifiedSameReference"]
    nested_composite_lookup = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedCompositeLookupBehavior"]
    assert len(nested_composite_lookup) == 1
    assert nested_composite_lookup[0]["name"].endswith("]][]&")
    assert nested_composite_lookup[0]["fullNameSameReference"]
    assert nested_composite_lookup[0]["qualifiedSameReference"]
    nested_misses = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedLookupMissBehavior"]
    assert [row["outcome"] for row in nested_misses] == [
        "null", "null", "System.ArgumentException",
    ]
    nested_ignore_case = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedConstructedIgnoreCaseBehavior"]
    assert len(nested_ignore_case) == 1
    assert nested_ignore_case[0]["exactMiss"]
    assert nested_ignore_case[0]["insensitiveSameReference"]
    nested_qualified_ignore = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedQualifiedIgnoreCaseBehavior"]
    assert len(nested_qualified_ignore) == 1
    assert nested_qualified_ignore[0]["exactMiss"]
    assert nested_qualified_ignore[0]["insensitiveSameReference"]
    nested_parameters = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedGenericParameterOwnerBehavior"]
    assert [(row["name"], row["position"], row["declaring"], row["isNested"],
             row["isNestedPublic"], row["isPublic"], row["isVisible"])
            for row in nested_parameters] == [
        (name, position, "System.Collections.Generic.Dictionary`2+Entry", True, False, True, True)
        for position, name in enumerate(("TKey", "TValue"))
    ]
    bases = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedBaseTypeBehavior"]
    assert [item["baseType"] for item in bases] == [
        None, "System.Object", "System.ValueType", "System.Object", "System.Object",
        "System.Object", "System.Array", "System.Array", None, None,
    ]
    kind_flags = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedKindFlags"]
    assert len(kind_flags) == 14
    assert [item["IsClass"] for item in kind_flags] == [
        True, True, False, True, True, True, True, True, True, True, True, True,
        False, False,
    ]
    assert [item["IsValueType"] for item in kind_flags] == [
        False, False, True, False, False, False, False, False, False, False, False, False,
        False, True,
    ]
    assert [item["IsInterface"] for item in kind_flags] == [False] * 12 + [True, False]
    assert [item["IsEnum"] for item in kind_flags] == [False] * 13 + [True]
    primitives = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPrimitiveBehavior"]
    assert [item["name"] for item in primitives] == [
        "System.Object", "System.String", "System.Int32", "System.Decimal",
        "System.DateTime", "System.TypeCode", "System.Array", "System.IDisposable",
        "System.String[]", "System.Collections.Generic.List`1",
    ]
    assert [item["isPrimitive"] for item in primitives] == [
        False, False, True, False, False, False, False, False, False, False,
    ]
    abstract = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAbstractBehavior"]
    assert [item["name"] for item in abstract] == [
        "System.Object", "System.String", "System.Int32", "System.Type",
        "System.ValueType", "System.Enum", "System.Array", "System.IDisposable",
        "System.IComparable", "System.Collections.Generic.List`1",
    ]
    assert [item["isAbstract"] for item in abstract] == [
        False, False, False, True, True, True, True, True, True, False,
    ]
    sealed = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSealedBehavior"]
    assert [item["name"] for item in sealed] == [
        "System.Object", "System.String", "System.Int32", "System.Type",
        "System.ValueType", "System.Array", "System.IDisposable", "System.TypeCode",
        "System.Decimal", "System.Collections.Generic.List`1",
    ]
    assert [item["isSealed"] for item in sealed] == [
        False, True, True, False, False, False, False, True, True, False,
    ]
    public = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPublicBehavior"]
    assert [item["name"] for item in public[:7]] == [
        "System.Object", "System.String", "System.Int32", "System.ValueType",
        "System.Array", "System.IComparable", "System.Collections.Generic.List`1",
    ]
    assert public[7]["name"].startswith("System.Collections.Generic.List`1[[System.String,")
    assert [item["name"] for item in public[8:]] == ["System.String[]", "System.String&"]
    assert [item["isPublic"] for item in public] == [True] * 10
    visible = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedVisibleBehavior"]
    assert [item["name"] for item in visible[:6]] == [
        "System.Object", "System.String", "System.Int32", "System.Type",
        "System.IDisposable", "System.Collections.Generic.List`1",
    ]
    assert visible[6]["name"].startswith("System.Collections.Generic.List`1[[System.String,")
    assert [item["name"] for item in visible[7:]] == [
        "System.String[]", "System.String&", "System.String*", "T",
    ]
    assert [item["isVisible"] for item in visible] == [True] * 11
    assert [item["isPublic"] for item in visible] == [True] * 11
    generic_definitions = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedGenericDefinitionBehavior"]
    assert [item["name"] for item in generic_definitions[:3]] == [
        "System.Object", "System.Int32", "System.Collections.Generic.List`1",
    ]
    assert generic_definitions[3]["name"].startswith("System.Collections.Generic.List`1[[System.String,")
    assert generic_definitions[4]["name"] == "System.Collections.Generic.Dictionary`2"
    assert generic_definitions[5]["name"].startswith("System.Collections.Generic.Dictionary`2[[System.String,")
    assert [item["name"] for item in generic_definitions[6:]] == ["T", "System.String[]"]
    assert [item["isGenericTypeDefinition"] for item in generic_definitions] == [
        False, False, True, False, True, False, False, False,
    ]
    definition_errors = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedGenericDefinitionErrorBehavior"]
    assert definition_errors == {
        "objectType": "System.InvalidOperationException",
        "stringType": "System.InvalidOperationException",
        "parameter": "System.InvalidOperationException",
        "array": "System.InvalidOperationException",
    }
    argument_copies = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedGenericArgumentCopyBehavior"]
    assert argument_copies == {
        "openNames": ["TKey", "TValue"], "positions": [0, 1],
        "distinctArrays": True, "stableElements": True, "mutationIsolated": True,
        "closedNames": ["System.String", "System.Int32"],
        "openTypeArgumentsLength": 0,
        "closedTypeArguments": ["System.String", "System.Int32"],
        "arrayArgumentsLength": 0,
    }
    constraints = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedGenericParameterConstraintBehavior"]
    assert [item["name"] for item in constraints] == [
        "T", "TKey", "TValue", "System.Object", "System.Collections.Generic.List`1",
    ]
    assert [item["observation"] for item in constraints[:3]] == [
        {"constraints": [], "exception": None}] * 3
    assert [item["observation"] for item in constraints[3:]] == [
        {"constraints": None, "exception": "System.InvalidOperationException"}] * 2
    sz_arrays = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSzArrayBehavior"]
    assert [item["name"] for item in sz_arrays[:6]] == [
        "System.Object", "System.String[]", "System.String[][]",
        "System.String[*]", "System.String[,]", "System.String[,,]",
    ]
    assert sz_arrays[6]["name"].startswith("System.Collections.Generic.List`1[[System.String,")
    assert sz_arrays[6]["name"].endswith("]][]")
    assert [item["isSzArray"] for item in sz_arrays] == [
        False, True, True, False, False, False, True,
    ]
    variable_arrays = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedVariableBoundArrayBehavior"]
    assert [item["name"] for item in variable_arrays] == [item["name"] for item in sz_arrays]
    assert [item["isVariableBoundArray"] for item in variable_arrays] == [
        False, False, False, True, True, True, False,
    ]
    elements = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedHasElementTypeBehavior"]
    assert [item["name"] for item in elements[:3]] == [
        "System.Object", "System.Int32", "System.Collections.Generic.List`1",
    ]
    assert elements[3]["name"].startswith("System.Collections.Generic.List`1[[System.String,")
    assert [item["name"] for item in elements[4:]] == [
        "System.String[]", "System.String[,]", "System.String[*]",
        "System.String&", "System.String*",
    ]
    assert [item["hasElementType"] for item in elements] == [False] * 4 + [True] * 5
    assert [item["elementType"] for item in elements] == [None] * 4 + ["System.String"] * 5
    construction = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedTypeConstructionBoundaryBehavior"]
    assert construction == {
        "byRefVector": {"result": None, "exception": "System.TypeLoadException"},
        "byRefRankTwo": {"result": None, "exception": "System.TypeLoadException"},
        "pointerVector": {"result": "System.String*[]", "exception": None},
        "pointerByRef": {"result": "System.String*&", "exception": None},
        "arrayByRef": {"result": "System.String[]&", "exception": None},
        "byRefPointer": {"result": None, "exception": "System.TypeLoadException"},
    }
    nested_names = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedTypeNameBehavior"]
    nested_type_flags = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedTypeFlagsBehavior"]
    for key, name in (("publicChild", "PublicChild"),
                      ("privateChild", "PrivateChild"), ("ignoreCase", "PublicChild")):
        assert nested_type_flags[key] == {"result": name, "exception": None, "paramName": None}
    for key in ("publicChildNonPublic", "privateChildPublic"):
        assert nested_type_flags[key] == {"result": None, "exception": None, "paramName": None}
    assert nested_type_flags["nullName"] == {
        "result": None, "exception": "System.ArgumentNullException", "paramName": "fullname",
    }
    nested_types_flags = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedTypesFlagsBehavior"]
    assert nested_types_flags == {
        "publicTypes": ["PublicChild"], "nonPublicTypes": ["PrivateChild"],
        "both": ["PrivateChild", "PublicChild"], "none": [],
    }
    assert nested_names == {
        "pointerArray": {"result": "System.String*[]", "exception": None, "paramName": None},
        "pointerByRef": {"result": "System.String*&", "exception": None, "paramName": None},
        "arrayByRef": {"result": "System.String[]&", "exception": None, "paramName": None},
        "doublePointer": {"result": "System.String**", "exception": None, "paramName": None},
        "byRefArray": {"result": None, "exception": "System.TypeLoadException", "paramName": None},
        "byRefArrayThrow": {"result": None, "exception": "System.TypeLoadException", "paramName": None},
    }
    qualified_nested = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedQualifiedNestedNameBehavior"]
    assert qualified_nested == {
        "coreLibArray": {"result": "System.String*[]", "exception": None, "paramName": None},
        "insensitiveArray": {"result": "System.String*[]", "exception": None, "paramName": None},
        "sensitiveMiss": {"result": None, "exception": None, "paramName": None},
        "legacyByRef": {"result": "System.String*&", "exception": None, "paramName": None},
        "coreLibDoublePointer": {"result": "System.String**", "exception": None, "paramName": None},
        "invalidByRefArray": {"result": None, "exception": "System.TypeLoadException", "paramName": None},
    }
    case_boundaries = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedCaseBoundaryBehavior"]
    assert case_boundaries == {
        "typeInsensitive": {"result": "System.Type", "exception": None, "paramName": None},
        "typeSensitive": {"result": None, "exception": None, "paramName": None},
        "operationInsensitive": {"result": "System.InvalidOperationException", "exception": None, "paramName": None},
        "operationSensitive": {"result": None, "exception": None, "paramName": None},
        "invalidNestedInsensitive": {"result": None, "exception": "System.TypeLoadException", "paramName": None},
        "invalidNestedSensitive": {"result": None, "exception": None, "paramName": None},
    }
    assembly_case = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyCaseBehavior"]
    assert assembly_case == {
        "coreLibLower": {"result": "System.String", "exception": None, "paramName": None},
        "coreLibUpper": {"result": "System.String", "exception": None, "paramName": None},
        "legacyUpper": {"result": "System.String", "exception": None, "paramName": None},
        "legacyMixed": {"result": "System.String", "exception": None, "paramName": None},
        "unknown": {"result": None, "exception": None, "paramName": None},
        "unknownThrow": {"result": None, "exception": "System.IO.FileNotFoundException",
                         "paramName": None},
    }
    assembly_identity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyIdentityBehavior"]
    assert assembly_identity == {
        key: {"result": "System.String", "exception": None, "paramName": None}
        for key in ("canonical", "versionMismatch", "cultureMismatch", "tokenMismatch",
                    "legacy", "mismatchThrow")
    }
    invalid_attributes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInvalidAssemblyAttributeBehavior"]
    assert invalid_attributes == {
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("invalidVersion", "emptyCulture", "invalidToken", "duplicateVersion")},
        "unknownAttribute": {"result": "System.String", "exception": None, "paramName": None},
    }
    attribute_casing = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyAttributeCasingBehavior"]
    assert attribute_casing == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("versionLower", "cultureUpper", "tokenMixed", "spacesAroundEquals", "spacesAfterComma")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("unknownEmpty", "duplicateCulture", "versionOnePart", "versionFivePart")},
    }
    attribute_delimiters = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyAttributeDelimiterBehavior"]
    assert attribute_delimiters == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("quotedCulture", "quotedVersion", "unknownQuoted", "tokenQuoted")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("trailingComma", "doubleComma", "emptyAttribute", "extraEquals")},
    }
    version_culture = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyVersionCultureBoundBehavior"]
    assert version_culture == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("versionTwoPart", "versionThreePart", "cultureUnderscore", "cultureUnknown")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("versionMaxComponent", "versionOverflow", "versionNegative")},
        "cultureNumeric": {"result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"},
    }
    token_bounds = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPublicKeyTokenBoundBehavior"]
    assert token_bounds == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("upperHex", "zeroHex", "upperNull", "quotedHex")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("shortHex", "longHex", "nonHex")},
    }
    attribute_order = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyAttributeOrderBehavior"]
    assert attribute_order == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("reversedKnown", "unknownBeforeKnown", "unknownAfterKnown", "duplicateUnknown")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("duplicateToken", "duplicateVersionMixedCase")},
    }
    simple_name_bounds = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblySimpleNameBoundaryBehavior"]
    assert simple_name_bounds == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("extraOuterSpace", "quotedName", "fileExtension", "legacyOuterSpace")},
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("embeddedSpace", "leadingDot", "emptyBeforeAttribute")},
    }
    legacy_aliases = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedLegacyAssemblyAliasBehavior"]
    assert legacy_aliases == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("legacyQuoted", "coreLibUpperDll")},
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("legacyDll", "legacyQuotedDll", "legacyExe", "legacyWithVersion")},
    }
    throw_bounds = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyThrowBoundaryBehavior"]
    assert throw_bounds == {
        **{key: {"result": None, "exception": "System.IO.FileNotFoundException", "paramName": None}
           for key in ("legacyDllThrow", "embeddedSpaceThrow")},
        "emptyBeforeAttributeThrow": {"result": None, "exception": "System.ArgumentException", "paramName": "typeName@15"},
        "invalidVersionThrow": {"result": None, "exception": "System.IO.FileLoadException", "paramName": None},
        "numericCultureThrow": {"result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"},
        "acceptedUnknownThrow": {"result": "System.String", "exception": None, "paramName": None},
    }
    value_whitespace = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyValueWhitespaceBehavior"]
    assert value_whitespace == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("versionOuterSpaces", "cultureOuterSpaces", "tokenOuterSpaces", "unknownInnerSpace")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("versionInnerSpace", "tokenInnerSpace")},
        "cultureInnerSpace": {"result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"},
    }
    quoted_bounds = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedQuotedAssemblyValueBoundaryBehavior"]
    assert quoted_bounds == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("emptyQuotedCulture", "emptyQuotedUnknown", "quotedUnknownWithComma")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("unclosedCulture", "trailingQuoteCulture")},
        "quotedCultureWithSpace": {"result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"},
    }
    quoted_delimiters = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedQuotedAssemblyDelimiterBehavior"]
    assert quoted_delimiters == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("unknownManyCommas", "unknownEquals")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("versionComma", "tokenComma")},
        "cultureComma": {"result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"},
    }
    escaped_quotes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEscapedAssemblyQuoteBehavior"]
    assert escaped_quotes == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("unknownBackslashQuote", "unknownBackslash")},
        "unknownDoubledQuote": {"result": None, "exception": "System.IO.FileLoadException", "paramName": None},
        "cultureBackslashQuote": {"result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"},
    }
    key_bounds = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyAttributeKeyBoundaryBehavior"]
    assert key_bounds == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("versionKeySpaces", "cultureKeySpaces", "tokenKeySpaces",
                       "unknownKeySpace", "unknownKeyDot", "versionKeyHyphen")},
        "emptyKey": {"result": None, "exception": "System.IO.FileLoadException", "paramName": None},
    }
    unknown_values = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUnknownAssemblyAttributeValueBehavior"]
    assert unknown_values == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("colon", "slash", "semicolon", "question", "duplicateMixedCase")},
        "unquotedEquals": {"result": None, "exception": "System.IO.FileLoadException", "paramName": None},
    }
    architectures = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedProcessorArchitectureAttributeBehavior"]
    assert architectures == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("msil", "x86", "amd64")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("none", "unknown", "duplicate")},
    }
    retargetable = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedRetargetableAttributeBehavior"]
    assert retargetable == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("yes", "no")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("trueValue", "falseValue", "numeric", "duplicate")},
    }
    content_types = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedContentTypeAttributeBehavior"]
    assert content_types == {
        "windowsRuntime": {"result": "System.String", "exception": None, "paramName": None},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("defaultValue", "lowerDefault", "unknown", "numeric", "duplicate")},
    }
    mixed_identity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMixedAssemblyIdentityBehavior"]
    assert mixed_identity == {
        "allValid": {"result": "System.String", "exception": None, "paramName": None},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("invalidVersionFirst", "invalidCultureFirst", "unknownAssemblyInvalidVersion",
                       "unknownAssemblyInvalidVersionThrow", "invalidContentFirst")},
    }
    unknown_assembly_attributes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUnknownAssemblyAttributeBehavior"]
    assert unknown_assembly_attributes == {
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("validVersion", "unknownAttribute")},
        **{key: {"result": None, "exception": "System.IO.FileNotFoundException", "paramName": None}
           for key in ("validVersionThrow", "unknownAttributeThrow")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("invalidToken", "duplicateVersion")},
        "invalidCulture": {"result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"},
    }
    attribute_aliases = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyAttributeAliasBehavior"]
    assert attribute_aliases == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("lowerArchitecture", "upperRetargetable", "lowerContentType",
                       "publicKeyNull", "cultureInfoAlias")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("publicKeyGarbage", "duplicateRetargetableCase")},
    }
    public_keys = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPublicKeyValueBehavior"]
    assert public_keys == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("zeroByte", "twoBytes", "eightBytes", "sixteenBytes", "upperNull")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("oneNibble", "nonHex")},
    }
    key_token = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPublicKeyTokenInteractionBehavior"]
    assert key_token == {
        key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
        for key in ("bothNull", "keyThenNullToken", "tokenThenKey", "keyThenToken",
                    "tokenThenInvalidKey", "invalidTokenThenKey")
    }
    culture_names = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedCultureNameBoundaryBehavior"]
    assert culture_names == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("titleNeutral", "upperNeutral", "lowerLocale", "upperLocale", "shortLocale")},
        **{key: {"result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"}
           for key in ("invariant", "nullText")},
    }
    culture_separators = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedCultureSeparatorBehavior"]
    assert culture_separators == {
        "underscore": {"result": "System.String", "exception": None, "paramName": None},
        **{key: {"result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"}
           for key in ("dot", "doubleHyphen", "trailingHyphen", "leadingHyphen", "slash", "atSign")},
    }
    culture_unicode = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedCultureUnicodeBoundaryBehavior"]
    assert culture_unicode == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("swissFrench", "scriptTag", "japanese")},
        **{key: {"result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"}
           for key in ("numericTag", "arabicDigits", "accentedName")},
    }
    version_components = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedVersionComponentBoundaryBehavior"]
    assert version_components == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("leadingZeros", "zeroPair", "maxPair", "manyLeadingZeros")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("overflowPair", "integerOverflow")},
    }
    version_grammar = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedVersionGrammarBoundaryBehavior"]
    assert version_grammar == {
        "fourParts": {"result": "System.String", "exception": None, "paramName": None},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("plusSign", "negativeSign", "spaceBeforeDot", "spaceAfterDot",
                       "fiveParts", "emptyMiddle")},
    }
    known_order = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedKnownAssemblyAttributeOrderBehavior"]
    assert known_order == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("contentThenRetargetable", "retargetableThenContent",
                       "architectureThenRetargetable", "retargetableThenVersion")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("cultureThenInvalidToken", "invalidTokenThenCulture")},
    }
    collisions = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyAttributeCollisionBehavior"]
    assert collisions == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("cultureAndCultureInfo", "versionAndHyphenAlias")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("duplicateTokenCase", "duplicateArchitectureCase", "duplicatePublicKeyCase",
                       "duplicateContentCase")},
    }
    name_quotes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblySimpleNameQuoteBehavior"]
    assert name_quotes == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("quotedOuterSpaces", "quotedDll", "singleQuotes")},
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("quotedInnerSpaces", "spaceBeforeDll", "quotedUnknown")},
    }
    unbalanced_names = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUnbalancedAssemblyQuoteBehavior"]
    assert unbalanced_names == {
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("missingDoubleClose", "missingDoubleOpen", "missingSingleClose", "missingSingleOpen")},
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("nestedDoubleInSingle", "nestedSingleInDouble")},
    }
    name_punctuation = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyNamePunctuationBehavior"]
    assert name_punctuation == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("quotedComma", "canonicalWithVersion")},
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("quotedEquals", "semicolon", "slash")},
        "unquotedEquals": {"result": None, "exception": "System.IO.FileLoadException", "paramName": None},
    }
    unicode_case = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyUnicodeCaseBehavior"]
    assert unicode_case == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("asciiUpper", "asciiMixed")},
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("dotlessI", "dottedUpperI", "accentedE", "fullwidthM")},
    }
    unicode_keys = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyAttributeUnicodeKeyBehavior"]
    assert unicode_keys == {
        key: {"result": "System.String", "exception": None, "paramName": None}
        for key in ("dotlessVersion", "dottedUpperVersion", "dotlessToken",
                    "accentedRetargetable", "unicodeThenVersion", "versionThenUnicode")
    }
    unicode_values = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyAttributeUnicodeValueBehavior"]
    assert unicode_values == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("asciiContent", "unicodeUnknown")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("accentedRetargetable", "dottedArchitecture", "dotlessContent", "accentedTokenNull")},
    }
    alias_suffixes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyAliasSuffixBehavior"]
    assert alias_suffixes == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("upperDll", "lowerDll", "quotedUpperDll", "singleQuotedDll")},
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("legacyUpperDll", "legacySingleQuotedDll")},
    }
    quoted_name_attributes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedQuotedAssemblyNameAttributeBehavior"]
    assert quoted_name_attributes == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("doubleVersion", "singleVersion", "quotedDllVersion",
                       "quotedUnknownAttribute", "quotedCommaVersion")},
        "quotedInvalidVersion": {"result": None, "exception": "System.IO.FileLoadException", "paramName": None},
    }
    quoted_name_punctuation = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedQuotedAssemblyNamePunctuationBehavior"]
    assert quoted_name_punctuation == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("singleQuotedComma", "commaUnknownAttribute", "quotedCommaToken")},
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("quotedEqualsVersion", "singleQuotedEquals")},
        "commaInvalidVersion": {"result": None, "exception": "System.IO.FileLoadException", "paramName": None},
    }
    escaped_name_separators = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEscapedAssemblyNameSeparatorBehavior"]
    assert escaped_name_separators == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("quotedEscapedComma", "singleEscapedComma", "unquotedEscapedComma")},
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("quotedEscapedEquals", "quotedBackslash")},
    }
    escaped_name_attributes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEscapedAssemblyNameAttributeBehavior"]
    assert escaped_name_attributes == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("unquotedVersion", "doubleQuotedVersion", "singleQuotedVersion", "unquotedUnknown")},
        "unquotedInvalidVersion": {"result": None, "exception": "System.IO.FileLoadException", "paramName": None},
    }
    escaped_name_quotes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEscapedAssemblyNameQuoteBehavior"]
    assert escaped_name_quotes == {
        key: {"result": None, "exception": None, "paramName": None}
        for key in ("doubleEmbedded", "singleEmbedded", "unquotedDouble",
                    "unquotedSingle", "doubleWithVersion", "singleWithVersion")
    }
    separator_parity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblySeparatorEscapeParityBehavior"]
    assert separator_parity == {
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("unquotedTwo", "unquotedFour")},
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("unquotedThree", "quotedTwo", "quotedThree", "singleTwo")},
    }
    quote_parity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyQuoteEscapeParityBehavior"]
    assert quote_parity == {
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("doubleThree", "singleThree", "unquotedDoubleTwo")},
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("doubleTwo", "singleTwo", "unquotedDoubleThree")},
    }
    attribute_parity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssemblyAttributeEscapeParityBehavior"]
    assert attribute_parity == {
        **{key: {"result": "System.String", "exception": None, "paramName": None}
           for key in ("quotedTwo", "unquotedTwo", "quotedCommaTwo", "quotedCommaThree")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("quotedThree", "unquotedThree")},
    }
    missing_assembly_precedence = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEscapedMissingAssemblyAttributePrecedence"]
    assert missing_assembly_precedence == {
        **{key: {"result": None, "exception": None, "paramName": None}
           for key in ("quotedValid", "escapedCommaValid")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("quotedInvalidVersion", "escapedCommaInvalidVersion", "evenBackslashInvalidVersion")},
        "evenBackslashInvalidCulture": {
            "result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"},
    }
    escaped_throw = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEscapedAssemblyThrowOnErrorBehavior"]
    assert escaped_throw == {
        **{key: {"result": None, "exception": "System.IO.FileNotFoundException", "paramName": None}
           for key in ("quotedMissing", "escapedCommaMissing")},
        **{key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
           for key in ("quotedInvalidVersion", "escapedCommaInvalidVersion")},
        "evenBackslashInvalidCulture": {
            "result": None, "exception": "System.Globalization.CultureNotFoundException", "paramName": "name"},
        "escapedAlias": {"result": "System.String", "exception": None, "paramName": None},
    }
    escaped_mixed_errors = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEscapedAssemblyMixedErrorPrecedence"]
    assert escaped_mixed_errors == {
        key: {"result": None, "exception": "System.IO.FileLoadException", "paramName": None}
        for key in ("cultureThenVersion", "versionThenCulture", "unknownEqualsThenCulture",
                    "escapedAliasMixed", "evenBackslashMixed", "cultureThenUnknownEquals")
    }
    contains_parameters = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedContainsGenericParametersBehavior"]
    assert contains_parameters[0]["name"] == "System.Object"
    assert contains_parameters[1]["name"] == "System.Collections.Generic.List`1"
    assert contains_parameters[2]["name"].startswith("System.Collections.Generic.List`1[[System.String,")
    assert contains_parameters[3]["name"] == "System.Collections.Generic.Dictionary`2"
    assert contains_parameters[4]["name"].startswith("System.Collections.Generic.Dictionary`2[[System.String,")
    assert [item["name"] for item in contains_parameters[5:]] == [
        "T", "System.Collections.Generic.List`1[]", "System.Collections.Generic.List`1",
    ]
    assert [item["containsGenericParameters"] for item in contains_parameters] == [
        False, True, False, True, False, True, True, True,
    ]
    enum_base = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedEnumBaseBehavior"]
    assert enum_base == {
        "enumBase": "System.Enum", "baseBase": "System.ValueType",
        "underlying": "System.Int32", "nonEnumError": "System.ArgumentException",
    }
    type_codes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedTypeCodeValues"]
    assert [(item["name"], item["number"]) for item in type_codes] == [
        ("Empty", 0), ("Object", 1), ("DBNull", 2), ("Boolean", 3), ("Char", 4),
        ("SByte", 5), ("Byte", 6), ("Int16", 7), ("UInt16", 8), ("Int32", 9),
        ("UInt32", 10), ("Int64", 11), ("UInt64", 12), ("Single", 13),
        ("Double", 14), ("Decimal", 15), ("DateTime", 16), ("String", 18),
    ]
    decimal = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDecimalBehavior"]
    assert decimal == {"intText": "42", "fractionalText": "4.2",
                       "intBits": [42, 0, 0, 0], "isValueType": True,
                       "baseType": "System.ValueType"}
    date_time = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDateTimeBehavior"]
    assert date_time == {"year": 2026, "month": 1, "day": 2,
                         "text": "2026-01-02", "isValueType": True,
                         "baseType": "System.ValueType"}
    int32 = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32Behavior"]
    assert int32 == {"typeCode": "Int32", "booleanValue": True,
                     "charValue": "*", "intValue": 42, "decimalText": "42",
                     "text": "42", "formattedText": "42", "compareTo41": 1}
    formats = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32FormatBehavior"]
    assert formats == {"decimal5": "00042", "hexUpper4": "002A",
                       "hexLower4": "002a", "negativeDecimal5": "-00042",
                       "negativeHex": "FFFFFFFF"}
    format_errors = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32FormatErrors"]
    assert format_errors == {"unknownSpecifier": "System.FormatException",
                             "negativeDecimalPrecision": None,
                             "negativeHexPrecision": None,
                             "hugePrecision": "System.FormatException"}
    odd_formats = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32OddFormatResults"]
    assert odd_formats == {"negativeDecimalPrecision": "D-1",
                           "negativeHexPrecision": "X-1"}
    number_formats = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32NumberFormatBehavior"]
    assert number_formats == {"groupedInteger": "12,345",
                              "groupedTwoDecimals": "12,345.00",
                              "lowerCase": "12,345.00",
                              "negative": "-12,345.00",
                              "defaultPrecision": "42.00"}
    currency_formats = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32CurrencyFormatBehavior"]
    assert currency_formats == {"defaultPrecision": "\u00a412,345.00",
                                "zeroPrecision": "\u00a412,345",
                                "lowerCase": "\u00a412,345.00",
                                "negative": "(\u00a412,345.00)",
                                "small": "\u00a442.00"}
    fixed_formats = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32FixedFormatBehavior"]
    assert fixed_formats == {"zeroPrecision": "12345",
                             "twoDecimals": "12345.00",
                             "lowerCase": "12345.00",
                             "negative": "-12345.00",
                             "defaultPrecision": "42.00"}
    percent_formats = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32PercentFormatBehavior"]
    assert percent_formats == {"defaultPrecision": "12,300.00 %",
                               "zeroPrecision": "12,300 %",
                               "lowerCase": "12,300.00 %",
                               "negative": "-12,300.00 %",
                               "small": "4,200.00 %"}
    general_formats = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32GeneralFormatBehavior"]
    assert general_formats == {"defaultFormat": "42", "paddedPrecision": "42",
                               "lowerCase": "42", "zeroPrecision": "42",
                               "negative": "-42"}
    binary_formats = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32BinaryFormatBehavior"]
    assert binary_formats == {"binary": "101010", "binary8": "00101010",
                              "lowerCase": "00101010",
                              "negative": "11111111111111111111111111111111",
                              "roundTripError": None, "roundTripResult": "42"}
    exponential_formats = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32ExponentialFormatBehavior"]
    assert exponential_formats == {"defaultPrecision": "4.200000E+001",
                                   "twoDecimals": "1.23E+004",
                                   "lowerCase": "1.23e+004",
                                   "negative": "-4.2E+001",
                                   "zero": "0.00E+000"}
    exponential_rounding = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32ExponentialRoundingBehavior"]
    assert exponential_rounding == {"exponentCarry": "1.0E+003",
                                    "midpointCarry": "1.0E+003",
                                    "midpointEven": "9.9E+002",
                                    "belowMidpoint": "9.5E+002",
                                    "maximum": "2.15E+009",
                                    "minimum": "-2.15E+009"}
    custom_formats = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32CustomFormatBehavior"]
    assert custom_formats == {"padded": "000042", "negativePadded": "-000042",
                              "grouped": "12,345", "groupedFixed": "12,345.00",
                              "fixedTwo": "42.00"}
    custom_sections = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32CustomSectionBehavior"]
    assert custom_sections == {"positive": "42", "negative": "(42)", "zero": "zero"}
    escaped_percent = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32EscapedPercentBehavior"]
    assert escaped_percent == {"escaped": "42%", "active": "4200%",
                               "negativeEscaped": "-42%", "negativeActive": "-4200%"}
    per_mille = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32PerMilleBehavior"]
    assert per_mille == {"escaped": "42\u2030", "active": "42000\u2030",
                         "negativeEscaped": "-42\u2030", "negativeActive": "-42000\u2030"}
    comma_scaling = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32CommaScalingBehavior"]
    assert comma_scaling == {"single": "12", "doubleScale": "1", "grouped": "1,235",
                             "negative": "-12", "halfway": "1000"}
    scaled_fraction = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32ScaledFractionBehavior"]
    assert scaled_fraction == {"onePlace": "12.3", "twoPlaces": "12.35",
                               "grouped": "1,234.6", "negative": "-12.3", "halfway": "1.3"}
    optional_fraction = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32OptionalFractionBehavior"]
    assert optional_fraction == {"integer": "42", "scaled": "12.35", "exact": "12",
                                 "grouped": "1,234.57", "negative": "-12.35"}
    quoted_literal = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32QuotedLiteralBehavior"]
    assert quoted_literal == {"prefix": "item 42", "suffix": "42 units", "both": "[42]",
                              "negative": "-item 42", "zero": "item 0"}
    quoted_sections = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32QuotedSectionBehavior"]
    assert quoted_sections == {"positive": "42", "negative": "[42]", "zero": "none",
                               "unsignedNegative": "42", "labeledNegative": "minus 42"}
    bracket_literals = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32BracketLiteralBehavior"]
    assert bracket_literals == {"above": "[>=115]0", "boundary": "[>=110]0",
                                "below": "[>=104]2", "negative": "[<4]neg 2",
                                "zero": "small 0"}
    near_zero = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32ScaledNearZeroBehavior"]
    assert near_zero == {"negativeWhole": "0", "negativeFixed": "0.0",
                         "negativeOptional": "0", "negativeHalfway": "-0.1",
                         "positiveHalfway": "0.1"}
    scaled_sections = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32ScaledSectionBehavior"]
    assert scaled_sections == {"positive": "12", "negative": "(12)", "zero": "zero",
                               "negativeSmall": "zero", "negativeFraction": "(1.3)"}
    errors = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32ConversionErrors"]
    assert errors == {"byteOverflow": "System.OverflowException",
                      "unsignedOverflow": "System.OverflowException",
                      "charOverflow": "System.OverflowException",
                      "invalidDateTime": "System.InvalidCastException"}
    parsed = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32ParseBehavior"]
    assert parsed == {
        "number": {"result": 42, "exception": None, "paramName": None},
        "padded": {"result": 42, "exception": None, "paramName": None},
        "invalid": {"result": None, "exception": "System.FormatException", "paramName": None},
        "overflow": {"result": None, "exception": "System.OverflowException", "paramName": None},
        "nullValue": {"result": None, "exception": "System.ArgumentNullException", "paramName": "s"},
    }
    try_parsed = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32TryParseBehavior"]
    assert try_parsed == {
        "number": {"success": True, "value": 42},
        "padded": {"success": True, "value": 42},
        "negative": {"success": True, "value": -7},
        "invalid": {"success": False, "value": 0},
        "overflow": {"success": False, "value": 0},
        "nullValue": {"success": False, "value": 0},
    }
    number_styles = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNumberStylesValues"]
    assert number_styles == {"none": 0, "integer": 7,
                             "allowHexSpecifier": 512, "hexNumber": 515}
    hexadecimal = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32HexParseBehavior"]
    assert hexadecimal == {
        "uppercase": {"result": 255, "exception": None, "paramName": None},
        "padded": {"result": 255, "exception": None, "paramName": None},
        "allBits": {"result": -1, "exception": None, "paramName": None},
        "overflow": {"result": None, "exception": "System.OverflowException", "paramName": None},
        "prefix": {"result": None, "exception": "System.FormatException", "paramName": None},
        "nullValue": {"result": None, "exception": "System.ArgumentNullException", "paramName": "s"},
    }
    hex_try = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt32HexTryParseBehavior"]
    assert hex_try == {
        "uppercase": {"success": True, "value": 255},
        "padded": {"success": True, "value": 255},
        "allBits": {"success": True, "value": -1},
        "overflow": {"success": False, "value": 0},
        "prefix": {"success": False, "value": 0},
        "nullValue": {"success": False, "value": 0},
    }
    assignability = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedAssignability"]
    underlying = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUnderlyingSystemTypeBehavior"]
    assert set(underlying) == {"stringSelf", "int32Self", "genericDefinitionSelf",
                               "closedGenericSelf", "arraySelf", "genericParameterSelf"}
    assert all(underlying.values())
    parameter_kind = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedGenericParameterKindBehavior"]
    assert parameter_kind == {
        "stringIsTypeParameter": False, "stringIsMethodParameter": False,
        "listParameterIsTypeParameter": True, "listParameterIsMethodParameter": False,
        "convertAllParameterIsTypeParameter": False, "convertAllParameterIsMethodParameter": True,
    }
    boolean_identity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedBooleanTypeIdentityBehavior"]
    assert boolean_identity == {
        "name": "Boolean", "fullName": "System.Boolean", "baseType": "System.ValueType",
        "isPrimitive": True, "isValueType": True, "isSealed": True, "isClass": False,
        "isAssignableToValueType": True, "typeCode": "Boolean",
    }
    char_identity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedCharTypeIdentityBehavior"]
    assert char_identity == {
        "name": "Char", "fullName": "System.Char", "baseType": "System.ValueType",
        "isPrimitive": True, "isValueType": True, "isSealed": True, "isClass": False,
        "isAssignableToValueType": True, "typeCode": "Char",
    }
    int16_identity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt16TypeIdentityBehavior"]
    assert int16_identity == {
        "name": "Int16", "fullName": "System.Int16", "baseType": "System.ValueType",
        "isPrimitive": True, "isValueType": True, "isSealed": True, "isClass": False,
        "isAssignableToValueType": True, "typeCode": "Int16",
    }
    int64_identity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInt64TypeIdentityBehavior"]
    assert int64_identity == {
        "name": "Int64", "fullName": "System.Int64", "baseType": "System.ValueType",
        "isPrimitive": True, "isValueType": True, "isSealed": True, "isClass": False,
        "isAssignableToValueType": True, "typeCode": "Int64",
    }
    single_identity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSingleTypeIdentityBehavior"]
    assert single_identity == {
        "name": "Single", "fullName": "System.Single", "baseType": "System.ValueType",
        "isPrimitive": True, "isValueType": True, "isSealed": True, "isClass": False,
        "isAssignableToValueType": True, "typeCode": "Single",
    }
    double_identity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedDoubleTypeIdentityBehavior"]
    assert double_identity == {
        "name": "Double", "fullName": "System.Double", "baseType": "System.ValueType",
        "isPrimitive": True, "isValueType": True, "isSealed": True, "isClass": False,
        "isAssignableToValueType": True, "typeCode": "Double",
    }
    byte_identity = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedByteTypeIdentityBehavior"]
    assert byte_identity == {
        "name": "Byte", "fullName": "System.Byte", "baseType": "System.ValueType",
        "isPrimitive": True, "isValueType": True, "isSealed": True, "isClass": False,
        "isAssignableToValueType": True, "typeCode": "Byte",
    }
    primitive_lookup = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPrimitiveLookupBehavior"]
    assert [row["name"] for row in primitive_lookup] == [
        "System.Boolean", "System.Char", "System.Byte", "System.Int16",
        "System.Int64", "System.Single", "System.Double",
    ]
    assert all(row["exact"] == row["lowerInsensitive"] == row["qualified"]
               == row["qualifiedLowerInsensitive"] == row["name"]
               and row["lowerSensitive"] is None for row in primitive_lookup)
    primitive_vectors = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPrimitiveVectorBehavior"]
    assert [row["elementFullName"] for row in primitive_vectors] == [
        "System.Boolean", "System.Char", "System.Byte", "System.Int16",
        "System.Int64", "System.Single", "System.Double",
    ]
    assert all(row["name"] == row["elementFullName"].removeprefix("System.") + "[]"
               and row["fullName"] == row["elementFullName"] + "[]"
               and row["rank"] == 1 and row["isVector"]
               and row["typeCode"] == "Object"
               and row["lookupIdentity"] and row["assemblyLookupIdentity"]
               and row["insensitiveLookupIdentity"] for row in primitive_vectors)
    primitive_rectangles = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPrimitiveRectangularBehavior"]
    assert [row["elementFullName"] for row in primitive_rectangles] == [
        "System.Boolean", "System.Char", "System.Byte", "System.Int16",
        "System.Int64", "System.Single", "System.Double",
    ]
    assert all(row["name"] == row["elementFullName"].removeprefix("System.") + "[,]"
               and row["fullName"] == row["elementFullName"] + "[,]"
               and row["rank"] == 2 and not row["isVector"]
               and row["isVariableBound"] and row["typeCode"] == "Object"
               and row["lookupIdentity"] and row["assemblyLookupIdentity"]
               and row["insensitiveLookupIdentity"] for row in primitive_rectangles)
    primitive_rank_three = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPrimitiveRankThreeBehavior"]
    assert [row["elementFullName"] for row in primitive_rank_three] == [
        "System.Boolean", "System.Char", "System.Byte", "System.Int16",
        "System.Int64", "System.Single", "System.Double",
    ]
    assert all(row["name"] == row["elementFullName"].removeprefix("System.") + "[,,]"
               and row["fullName"] == row["elementFullName"] + "[,,]"
               and row["rank"] == 3 and not row["isVector"]
               and row["isVariableBound"] and row["typeCode"] == "Object"
               and row["lookupIdentity"] and row["assemblyLookupIdentity"]
               and row["insensitiveLookupIdentity"] for row in primitive_rank_three)
    primitive_variable = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPrimitiveVariableBoundBehavior"]
    assert [row["elementFullName"] for row in primitive_variable] == [
        "System.Boolean", "System.Char", "System.Byte", "System.Int16",
        "System.Int64", "System.Single", "System.Double",
    ]
    assert all(row["name"] == row["elementFullName"].removeprefix("System.") + "[*]"
               and row["fullName"] == row["elementFullName"] + "[*]"
               and row["rank"] == 1 and not row["isVector"]
               and row["isVariableBound"] and row["typeCode"] == "Object"
               and row["lookupIdentity"] and row["assemblyLookupIdentity"]
               and row["insensitiveLookupIdentity"] for row in primitive_variable)
    type_texts = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedTypeToStringBehavior"]
    assert [row["text"] for row in type_texts] == [
        "System.String", "System.Int32", "System.String[]", "System.String[,]",
        "System.String&", "System.String*", "System.Collections.Generic.List`1[T]",
        "T", "System.Collections.Generic.List`1[System.String]",
        "System.Collections.Generic.Dictionary`2[System.String,System.Int32]",
    ]
    nested_texts = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedTypeToStringBehavior"]
    assert [row["text"] for row in nested_texts] == [
        "System.Collections.Generic.List`1[System.String][]",
        "System.Collections.Generic.List`1[System.String][,]",
        "System.Collections.Generic.List`1[System.Collections.Generic.List`1[System.String]]",
        "System.Collections.Generic.Dictionary`2[System.String,System.Collections.Generic.List`1[System.Int32]]",
        "System.Collections.Generic.List`1[T][]", "T[]",
    ]
    definition_kinds = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedTypeDefinitionBehavior"]
    assert [row["result"] for row in definition_kinds] == [True] * 5 + [False] * 7
    byref_like = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedByRefLikeBehavior"]
    assert [row["result"] for row in byref_like] == [False] * 6 + [True] * 2
    nested_flags = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedTypeFlagBehavior"]
    assert [row["isNested"] for row in nested_flags] == [False] * 2 + [True] * 3
    assert [row["isNestedPublic"] for row in nested_flags] == [False] * 3 + [True] * 2
    nested_assembly = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedAssemblyBehavior"]
    assert [row["result"] for row in nested_assembly] == [False] * 3 + [True]
    nested_private = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedPrivateBehavior"]
    assert [row["result"] for row in nested_private] == [False] * 3 + [True]
    nested_family = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedNestedFamilyBehavior"]
    assert [row["result"] for row in nested_family] == [False] * 3 + [True]
    primitive_array_texts = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedPrimitiveArrayToStringBehavior"]
    assert [row["name"] for row in primitive_array_texts] == [
        "System.Boolean", "System.Char", "System.Byte", "System.Int16",
        "System.Int64", "System.Single", "System.Double",
    ]
    assert all(row["vector"] == row["name"] + "[]"
               and row["variableBound"] == row["name"] + "[*]"
               and row["rankTwo"] == row["name"] + "[,]"
               and row["rankThree"] == row["name"] + "[,,]"
               for row in primitive_array_texts)
    parameter_attributes = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedGenericParameterAttributeBehavior"]
    assert parameter_attributes == {
        "stringType": {"value": None, "exception": "System.InvalidOperationException"},
        "listParameter": {"value": 0, "exception": None},
        "dictionaryKeyParameter": {"value": 0, "exception": None},
        "convertAllParameter": {"value": 0, "exception": None},
    }
    attribute_values = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedGenericParameterAttributeValues"]
    assert attribute_values == {
        "None": 0, "Covariant": 1, "Contravariant": 2, "VarianceMask": 3,
        "ReferenceTypeConstraint": 4, "NotNullableValueTypeConstraint": 8,
        "DefaultConstructorConstraint": 16, "SpecialConstraintMask": 28,
        "AllowByRefLike": 32,
    }
    attribute_type = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedGenericParameterAttributesTypeIdentity"]
    assert attribute_type == {
        "name": "GenericParameterAttributes",
        "fullName": "System.Reflection.GenericParameterAttributes",
        "baseType": "System.Enum", "isEnum": True, "isValueType": True,
        "isSealed": True, "underlyingType": "System.Int32", "typeCode": "Int32",
        "qualifiedLookup": True, "insensitiveLookup": True,
    }
    assert [item["result"] for item in assignability] == [
        True, True, True, True, False, False, True, True, False, True, False,
        True, False, False, True, False, True, True, True, True, True, True,
    ]
    subclass = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSubclassBehavior"]
    assert [item["observation"]["result"] for item in subclass] == [
        True, True, True, True, True, True, True, False, False, None,
    ]
    assert subclass[-1]["observation"]["exception"] == "System.ArgumentNullException"
    assert subclass[-1]["observation"]["paramName"] == "type"
    instances = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInstanceBehavior"]
    assert [item["result"] for item in instances] == [
        True, True, False, True, False, True, False, True, True, True, True,
        True, False, False, True, True, True, True, True, True,
    ]
    interfaces = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedInterfaceBehavior"]
    assert interfaces["objectInterfaces"] == interfaces["disposableInterfaces"] == []
    assert all(interfaces[key]["result"] is None and interfaces[key]["exception"] is None
               for key in ("objectMiss", "disposableSelf", "emptyName"))
    assert interfaces["nullName"] == {
        "result": None, "exception": "System.ArgumentNullException", "paramName": "fullname",
    }
    assert interfaces["stringComparable"]["result"] == "System.IComparable"
    assert interfaces["stringComparableIgnoreCase"]["result"] == "System.IComparable"
    assert interfaces["stringComparableShort"]["result"] == "System.IComparable"
    assert all(interfaces[key]["result"] is None for key in
               ("stringInsensitive", "stringSensitiveMiss", "stringDisposableMiss"))
    assert interfaces["intFormattable"]["result"] == "System.IFormattable"
    assert interfaces["intFormattableShort"]["result"] == "System.IFormattable"
    assert interfaces["intFormattableLower"]["result"] is None
    assert interfaces["stringFormattableMiss"]["result"] is None
    assert interfaces["intConvertible"]["result"] == "System.IConvertible"
    assert interfaces["intConvertibleShort"]["result"] == "System.IConvertible"
    assert interfaces["intConvertibleLower"]["result"] is None
    assert interfaces["objectConvertibleMiss"]["result"] is None
    assert len(interfaces["intInterfaces"]) == 32
    assert interfaces["intInterfaces"][:4] == [
        "System.IComparable", "System.IConvertible", "System.ISpanFormattable",
        "System.IFormattable"]
    assert interfaces["intComparable"]["result"] == "System.IComparable"
    assert interfaces["intComparableShort"]["result"] == "System.IComparable"
    assert interfaces["intComparableLower"]["result"] is None
    assert interfaces["spanFormattableInterfaces"] == ["System.IFormattable"]
    assert interfaces["intSpanFormattable"]["result"] == "System.ISpanFormattable"
    assert interfaces["intSpanFormattableShort"]["result"] == "System.ISpanFormattable"
    assert interfaces["intSpanFormattableLower"]["result"] is None
    span_format = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedSpanFormattingBehavior"]
    assert span_format == {"enough": {"success": True, "charsWritten": 2, "text": "42"},
                           "shortBuffer": {"success": False, "charsWritten": 0, "text": ""}}
    assert interfaces["utf8SpanFormattableInterfaces"] == []
    assert interfaces["intUtf8SpanFormattable"]["result"] == "System.IUtf8SpanFormattable"
    assert interfaces["intUtf8SpanFormattableShort"]["result"] == "System.IUtf8SpanFormattable"
    assert interfaces["intUtf8SpanFormattableLower"]["result"] is None
    utf8_format = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedUtf8SpanFormattingBehavior"]
    assert utf8_format == {"enough": {"success": True, "bytesWritten": 2, "text": "42"},
                           "shortBuffer": {"success": False, "bytesWritten": 0, "text": ""}}
    array_observations = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedArrayBehavior"]
    assert [(item["IsArray"], item["rank"], item["error"]) for item in array_observations] == [
        (False, None, "System.ArgumentException"),
        (True, 1, None), (True, 1, None), (True, 2, None), (True, 3, None), (True, 1, None),
    ]

    CLASSES.mkdir(parents=True, exist_ok=True)
    TEST_CLASSES.mkdir(parents=True, exist_ok=True)
    run("javac", "--release", "21", "-d", str(CLASSES),
        *(str(path) for path in [SOURCE, *EXCEPTION_SOURCES, IDISPOSABLE_SOURCE, ICOMPARABLE_SOURCE,
                                 IFORMATTABLE_SOURCE, IFORMATPROVIDER_SOURCE, ICONVERTIBLE_SOURCE,
                                 ISPANFORMATTABLE_SOURCE, IUTF8SPANFORMATTABLE_SOURCE]))
    assert not (CLASSES / "System/TypeCandidateFactory.class").exists()
    run("javac", "--release", "21", "-cp", str(CLASSES), "-d", str(TEST_CLASSES),
        str(TEST), str(NOT_PUBLIC_FIXTURE), str(CONCURRENCY_TEST), str(LOADER_FIXTURE), str(EXTERNAL))
    assert not (TEST_CLASSES / "System/TypeCandidateFactory.class").exists()
    public = run("javap", "-public", "-classpath", str(CLASSES), "System.Type")
    assert "public abstract class System.Type" in public
    members = [line.strip() for line in public.splitlines() if line.strip().endswith(";")]
    assert members == [
        "public static System.TypeCode GetTypeCode(System.Type);",
        "public static System.Type[] GetTypeArray(java.lang.Object[]);",
        "public boolean get_IsCollectible();",
        "public int GetHashCode();",
        "public static System.Type MakeGenericMethodParameter(int);",
        "public static System.Type MakeGenericSignatureType(System.Type, System.Type[]);",
        "public static System.Type GetType(java.lang.String);",
        "public static System.Type GetType(java.lang.String, boolean);",
        "public static System.Type GetType(java.lang.String, boolean, boolean);",
        "public System.Type MakeGenericType(System.Type[]);",
        "public System.Type MakeArrayType();",
        "public System.Type MakeArrayType(int);",
        "public System.Type MakeByRefType();",
        "public System.Type MakePointerType();",
        "public System.Type GetGenericTypeDefinition();",
        "public System.Type[] GetGenericArguments();",
        "public System.Type[] GetGenericParameterConstraints();",
        "public System.Type[] get_GenericTypeArguments();",
        "public java.lang.String get_FullName();",
        "public java.lang.String get_AssemblyQualifiedName();",
        "public java.lang.String get_Namespace();",
        "public System.Type get_DeclaringType();",
        "public System.Type get_ReflectedType();",
        "public System.Type get_BaseType();",
        "public System.Type get_UnderlyingSystemType();",
        "public boolean get_IsValueType();",
        "public boolean get_IsPrimitive();",
        "public boolean get_IsAbstract();",
        "public boolean get_IsSealed();",
        "public boolean get_IsPublic();",
        "public boolean get_IsNotPublic();",
        "public boolean get_IsSerializable();",
        "public boolean get_IsSpecialName();",
        "public boolean get_IsAnsiClass();",
        "public boolean get_IsUnicodeClass();",
        "public boolean get_IsAutoClass();",
        "public boolean get_IsAutoLayout();",
        "public boolean get_IsLayoutSequential();",
        "public boolean get_IsExplicitLayout();",
        "public boolean get_IsImport();",
        "public boolean get_IsCOMObject();",
        "public boolean get_IsContextful();",
        "public boolean get_IsMarshalByRef();",
        "public boolean get_IsSignatureType();",
        "public boolean get_IsFunctionPointer();",
        "public boolean get_IsUnmanagedFunctionPointer();",
        "public System.Type GetFunctionPointerReturnType();",
        "public System.Type[] GetFunctionPointerParameterTypes();",
        "public System.Type[] GetFunctionPointerCallingConventions();",
        "public boolean get_IsSecurityCritical();",
        "public boolean get_IsSecuritySafeCritical();",
        "public boolean get_IsSecurityTransparent();",
        "public System.Reflection.MemberTypes get_MemberType();",
        "public boolean get_IsVisible();",
        "public boolean get_IsClass();",
        "public boolean get_IsInterface();",
        "public boolean get_IsEnum();",
        "public System.Type GetEnumUnderlyingType();",
        "public java.lang.String[] GetEnumNames();",
        "public java.lang.Object[] GetEnumValues();",
        "public int[] GetEnumValuesAsUnderlyingType();",
        "public boolean IsEnumDefined(java.lang.Object);",
        "public java.lang.String GetEnumName(java.lang.Object);",
        "public boolean IsAssignableTo(System.Type);",
        "public boolean IsAssignableFrom(System.Type);",
        "public boolean IsSubclassOf(System.Type);",
        "public boolean IsInstanceOfType(java.lang.Object);",
        "public System.Reflection.MemberInfo[] GetMember(java.lang.String);",
        "public System.Reflection.MemberInfo[] GetMember(java.lang.String, System.Reflection.BindingFlags);",
        "public System.Reflection.MemberInfo[] GetMember(java.lang.String, System.Reflection.MemberTypes, System.Reflection.BindingFlags);",
        "public System.Reflection.MemberInfo[] GetMembers();",
        "public System.Reflection.MemberInfo[] GetMembers(System.Reflection.BindingFlags);",
        "public System.Reflection.MethodInfo[] GetMethods(System.Reflection.BindingFlags);",
        "public System.Reflection.MethodInfo[] GetMethods();",
        "public System.Reflection.MethodInfo GetMethod(java.lang.String);",
        "public System.Reflection.MethodInfo GetMethod(java.lang.String, System.Reflection.BindingFlags);",
        "public System.Reflection.MethodInfo GetMethod(java.lang.String, System.Type[]);",
        "public System.Reflection.MethodInfo GetMethod(java.lang.String, System.Reflection.BindingFlags, System.Type[]);",
        "public System.Reflection.MemberInfo[] GetDefaultMembers();",
        "public System.Type[] GetOptionalCustomModifiers();",
        "public System.Type[] GetRequiredCustomModifiers();",
        "public System.Type[] GetInterfaces();",
        "public System.Type GetInterface(java.lang.String);",
        "public System.Type GetNestedType(java.lang.String);",
        "public System.Type GetNestedType(java.lang.String, System.Reflection.BindingFlags);",
        "public System.Type[] GetNestedTypes();",
        "public System.Type[] GetNestedTypes(System.Reflection.BindingFlags);",
        "public System.Type GetInterface(java.lang.String, boolean);",
        "public boolean get_IsArray();",
        "public boolean get_IsSZArray();",
        "public boolean get_IsVariableBoundArray();",
        "public boolean get_HasElementType();",
        "public boolean get_IsByRef();",
        "public boolean get_IsPointer();",
        "public System.Type GetElementType();",
        "public int GetArrayRank();",
        "public boolean get_IsGenericType();",
        "public boolean get_IsGenericTypeDefinition();",
        "public boolean get_IsTypeDefinition();",
        "public boolean get_IsByRefLike();",
        "public boolean get_IsNested();",
        "public boolean get_IsNestedPublic();",
        "public boolean get_IsNestedAssembly();",
        "public boolean get_IsNestedPrivate();",
        "public boolean get_IsNestedFamily();",
        "public boolean get_IsNestedFamANDAssem();",
        "public boolean get_IsNestedFamORAssem();",
        "public boolean get_ContainsGenericParameters();",
        "public boolean get_IsConstructedGenericType();",
        "public boolean get_IsGenericParameter();",
        "public boolean get_IsGenericTypeParameter();",
        "public boolean get_IsGenericMethodParameter();",
        "public System.Reflection.GenericParameterAttributes get_GenericParameterAttributes();",
        "public int get_GenericParameterPosition();",
        "public boolean IsEquivalentTo(System.Type);",
        "public java.lang.String ToString();",
        "public java.lang.String toString();",
        "public boolean HasSameMetadataDefinitionAs(System.Reflection.MemberInfo);",
        "public boolean Equals(System.Type);",
    ], members
    null_exception = run("javap", "-public", "-classpath", str(CLASSES),
                         "System.ArgumentNullException")
    assert "public class System.ArgumentNullException extends System.ArgumentException" in null_exception
    classpath = os.pathsep.join((str(CLASSES), str(TEST_CLASSES)))
    result = run("java", "-cp", classpath, "System.TypeIdentityCandidateTest").strip()
    assert result.startswith("PASS selected System.Type identity")
    external_result = run("java", "-cp", classpath, "consumer.ProductTypeIdentityConsumer").strip()
    assert external_result == "PASS external System.Type selected identity consumer"
    concurrency_result = run("java", "-cp", classpath, "System.TypeIdentityConcurrencyTest",
                             str(TEST_CLASSES / "fixture/LoadableType.class")).strip()
    assert concurrency_result == "PASS System.Type isolated loader and 1600 concurrent canonical constructions"
    EVIDENCE.write_text(json.dumps({
        "schemaVersion": 1,
        "upstreamFullName": "System.Type",
        "sourceCommit": provenance["sourceCommit"],
        "coreLibSha256": snapshot["assemblySha256"],
        "snapshotSha256": sha256(SNAPSHOT),
        "selectedGetTypeBehavior": observed,
        "sourcePath": SOURCE.relative_to(ROOT).as_posix(),
        "sourceSha256": sha256(SOURCE),
        "idisposableSourceSha256": sha256(IDISPOSABLE_SOURCE),
        "icomparableSourceSha256": sha256(ICOMPARABLE_SOURCE),
        "iformattableSourceSha256": sha256(IFORMATTABLE_SOURCE),
        "iformatproviderSourceSha256": sha256(IFORMATPROVIDER_SOURCE),
        "iconvertibleSourceSha256": sha256(ICONVERTIBLE_SOURCE),
        "ispanformattableSourceSha256": sha256(ISPANFORMATTABLE_SOURCE),
        "iutf8spanformattableSourceSha256": sha256(IUTF8SPANFORMATTABLE_SOURCE),
        "exceptionSources": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}
                             for path in EXCEPTION_SOURCES],
        "testPath": TEST.relative_to(ROOT).as_posix(),
        "testSha256": sha256(TEST),
        "externalConsumerPath": EXTERNAL.relative_to(ROOT).as_posix(),
        "externalConsumerSha256": sha256(EXTERNAL),
        "concurrencyTestPath": CONCURRENCY_TEST.relative_to(ROOT).as_posix(),
        "concurrencyTestSha256": sha256(CONCURRENCY_TEST),
        "loaderFixturePath": LOADER_FIXTURE.relative_to(ROOT).as_posix(),
        "loaderFixtureSha256": sha256(LOADER_FIXTURE),
        "publicMembers": members,
        "testResult": result,
        "externalConsumerResult": external_result,
        "concurrencyResult": concurrency_result,
        "status": "SELECTED_IDENTITY_CANDIDATE; complete 181-method/70-property System.Type surface, MemberInfo inheritance, generic-parameter Types, public null/error mapping and release qualification OPEN",
    }, indent=2) + "\n", encoding="utf-8")
    print(result)
    print(external_result)
    print(concurrency_result)


if __name__ == "__main__":
    main()
