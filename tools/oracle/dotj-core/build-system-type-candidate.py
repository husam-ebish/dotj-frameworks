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
                     ("Exception", "SystemException", "ArgumentException", "ArgumentNullException", "TypeLoadException", "IndexOutOfRangeException")]
EXCEPTION_SOURCES += [SOURCE.parent / "IO" / (name + ".java") for name in
                      ("IOException", "FileNotFoundException")]
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
    }
    signatures = {method["signature"] for method in metadata["methods"]}
    assert selected <= signatures
    assert any(method["signature"] == "System.Type GetType(System.String)" and method["isStatic"]
               for method in metadata["methods"])
    properties = {item["Name"] for item in metadata["properties"]}
    assert {"GenericTypeArguments", "IsGenericType", "IsConstructedGenericType",
            "IsGenericParameter", "GenericParameterPosition", "IsArray", "IsByRef", "IsPointer"} <= properties
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
    array_observations = json.loads(FOUNDATION_METADATA.read_text(encoding="utf-8"))["selectedArrayBehavior"]
    assert [(item["IsArray"], item["rank"], item["error"]) for item in array_observations] == [
        (False, None, "System.ArgumentException"),
        (True, 1, None), (True, 1, None), (True, 2, None), (True, 3, None), (True, 1, None),
    ]

    CLASSES.mkdir(parents=True, exist_ok=True)
    TEST_CLASSES.mkdir(parents=True, exist_ok=True)
    run("javac", "--release", "21", "-d", str(CLASSES),
        *(str(path) for path in [SOURCE, *EXCEPTION_SOURCES]))
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
