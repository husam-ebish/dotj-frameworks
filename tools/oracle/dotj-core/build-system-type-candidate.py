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
                     ("Exception", "SystemException", "ArgumentException", "ArgumentNullException", "TypeLoadException", "IndexOutOfRangeException", "OverflowException", "InvalidCastException", "InvalidOperationException", "FormatException")]
EXCEPTION_SOURCES += [SOURCE.parent / "IO" / (name + ".java") for name in
                      ("IOException", "FileNotFoundException", "FileLoadException")]
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MemberInfo.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MemberTypes.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/GenericParameterAttributes.java")
EXCEPTION_SOURCES.append(SOURCE.with_name("TypeCode.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("Decimal.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("DateTime.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("Int32.java"))
EXCEPTION_SOURCES.append(SOURCE.parent / "Globalization/NumberStyles.java")
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
        "System.Type[] GetGenericParameterConstraints()",
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
    assert len(selected_corelib_types) == 29
    assert all(item["qualifiedNameRoundTripSameReference"] and
               item["assemblyQualifiedName"] == item["fullName"] + corelib_identity
               for item in selected_corelib_types)
    corelib_case = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedCoreLibCaseLookup"]
    assert len(corelib_case) == 29
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
        "public static System.TypeCode GetTypeCode(System.Type);",
        "public static System.Type[] GetTypeArray(java.lang.Object[]);",
        "public int GetHashCode();",
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
        "public boolean get_IsVisible();",
        "public boolean get_IsClass();",
        "public boolean get_IsInterface();",
        "public boolean get_IsEnum();",
        "public System.Type GetEnumUnderlyingType();",
        "public boolean IsAssignableTo(System.Type);",
        "public boolean IsAssignableFrom(System.Type);",
        "public boolean IsSubclassOf(System.Type);",
        "public boolean IsInstanceOfType(java.lang.Object);",
        "public System.Type[] GetInterfaces();",
        "public System.Type GetInterface(java.lang.String);",
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
        "public boolean get_ContainsGenericParameters();",
        "public boolean get_IsConstructedGenericType();",
        "public boolean get_IsGenericParameter();",
        "public boolean get_IsGenericTypeParameter();",
        "public boolean get_IsGenericMethodParameter();",
        "public System.Reflection.GenericParameterAttributes get_GenericParameterAttributes();",
        "public int get_GenericParameterPosition();",
        "public boolean IsEquivalentTo(System.Type);",
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
