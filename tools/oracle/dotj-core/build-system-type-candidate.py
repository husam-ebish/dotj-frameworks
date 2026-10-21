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
                     ("Exception", "SystemException", "ArgumentException", "ArgumentNullException", "TypeLoadException", "IndexOutOfRangeException", "OverflowException", "InvalidCastException", "FormatException")]
EXCEPTION_SOURCES += [SOURCE.parent / "IO" / (name + ".java") for name in
                      ("IOException", "FileNotFoundException")]
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MemberInfo.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MemberTypes.java")
EXCEPTION_SOURCES.append(SOURCE.with_name("TypeCode.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("Decimal.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("DateTime.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("Int32.java"))
EXCEPTION_SOURCES.append(SOURCE.parent / "Globalization/NumberStyles.java")
IDISPOSABLE_SOURCE = SOURCE.with_name("IDisposable.java")
ICOMPARABLE_SOURCE = SOURCE.with_name("IComparable.java")
IFORMATTABLE_SOURCE = SOURCE.with_name("IFormattable.java")
IFORMATPROVIDER_SOURCE = SOURCE.with_name("IFormatProvider.java")
ISPANFORMATTABLE_SOURCE = SOURCE.with_name("ISpanFormattable.java")
IUTF8SPANFORMATTABLE_SOURCE = SOURCE.with_name("IUtf8SpanFormattable.java")
ICONVERTIBLE_SOURCE = SOURCE.with_name("IConvertible.java")
TEST = ROOT / "dotj-core/dotj-core-public/src/test/java/System/TypeIdentityCandidateTest.java"
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
    return subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True).stdout


def main():
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    assert sha256(SNAPSHOT) == provenance["snapshotSha256"]
    assert snapshot["assemblySha256"] == provenance["installedCoreLibSha256"]
    metadata = snapshot["type"]
    assert metadata["fullName"] == "System.Type"
    selected = {
        "Boolean Equals(System.Type)",
        "System.Type GetGenericTypeDefinition()",
        "System.Type[] GetGenericArguments()",
        "System.Type MakeGenericType(System.Type[])",
        "System.Type GetType(System.String)",
        "System.Type GetEnumUnderlyingType()",
        "Boolean IsAssignableFrom(System.Type)",
        "Boolean IsSubclassOf(System.Type)",
        "Boolean IsInstanceOfType(System.Object)",
        "System.Type[] GetInterfaces()",
        "System.Type GetInterface(System.String)",
        "System.Type GetInterface(System.String, Boolean)",
    }
    signatures = {method["signature"] for method in metadata["methods"]}
    assert selected <= signatures
    assert any(method["signature"] == "System.Type GetType(System.String)" and method["isStatic"]
               for method in metadata["methods"])
    properties = {item["Name"] for item in metadata["properties"]}
    assert {"GenericTypeArguments", "IsGenericType", "IsConstructedGenericType",
            "IsGenericParameter", "GenericParameterPosition", "IsArray", "IsByRef", "IsPointer",
            "FullName", "Namespace", "BaseType", "IsClass", "IsValueType",
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
    owners = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedMemberOwnerBehavior"]
    assert len(owners) == 7
    assert all(item["declaringType"] is None and item["reflectedType"] is None
               for index, item in enumerate(owners) if index != 3)
    assert owners[3]["name"] == "T"
    assert owners[3]["declaringType"] == owners[3]["reflectedType"] == "System.Collections.Generic.List`1"
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
        str(TEST), str(CONCURRENCY_TEST), str(LOADER_FIXTURE), str(EXTERNAL))
    assert not (TEST_CLASSES / "System/TypeCandidateFactory.class").exists()
    public = run("javap", "-public", "-classpath", str(CLASSES), "System.Type")
    assert "public abstract class System.Type" in public
    members = [line.strip() for line in public.splitlines() if line.strip().endswith(";")]
    assert members == [
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
        "public System.Type[] get_GenericTypeArguments();",
        "public java.lang.String get_FullName();",
        "public java.lang.String get_Namespace();",
        "public System.Type get_DeclaringType();",
        "public System.Type get_ReflectedType();",
        "public System.Type get_BaseType();",
        "public boolean get_IsValueType();",
        "public boolean get_IsClass();",
        "public boolean get_IsInterface();",
        "public boolean get_IsEnum();",
        "public System.Type GetEnumUnderlyingType();",
        "public boolean IsAssignableFrom(System.Type);",
        "public boolean IsSubclassOf(System.Type);",
        "public boolean IsInstanceOfType(java.lang.Object);",
        "public System.Type[] GetInterfaces();",
        "public System.Type GetInterface(java.lang.String);",
        "public System.Type GetInterface(java.lang.String, boolean);",
        "public boolean get_IsArray();",
        "public boolean get_IsByRef();",
        "public boolean get_IsPointer();",
        "public System.Type GetElementType();",
        "public int GetArrayRank();",
        "public boolean get_IsGenericType();",
        "public boolean get_IsConstructedGenericType();",
        "public boolean get_IsGenericParameter();",
        "public int get_GenericParameterPosition();",
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
