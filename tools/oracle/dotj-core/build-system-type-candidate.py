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
TEST = ROOT / "dotj-core/dotj-core-public/src/test/java/System/TypeIdentityCandidateTest.java"
EXTERNAL = ROOT / "dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java"
BUILD = ROOT / "dotj-core/dotj-core-public/build/type-identity-candidate-v2"
CLASSES = BUILD / "product-classes"
TEST_CLASSES = BUILD / "test-classes"
EVIDENCE = EVIDENCE_ROOT / "system-type-identity-candidate-v1.json"


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
    assert {"GenericTypeArguments", "IsGenericType", "IsConstructedGenericType"} <= properties

    CLASSES.mkdir(parents=True, exist_ok=True)
    TEST_CLASSES.mkdir(parents=True, exist_ok=True)
    run("javac", "--release", "21", "-d", str(CLASSES), str(SOURCE))
    assert not (CLASSES / "System/TypeCandidateFactory.class").exists()
    run("javac", "--release", "21", "-cp", str(CLASSES), "-d", str(TEST_CLASSES),
        str(TEST), str(EXTERNAL))
    assert not (TEST_CLASSES / "System/TypeCandidateFactory.class").exists()
    public = run("javap", "-public", "-classpath", str(CLASSES), "System.Type")
    assert "public abstract class System.Type" in public
    members = [line.strip() for line in public.splitlines() if line.strip().endswith(";")]
    assert members == [
        "public static System.Type GetType(java.lang.String);",
        "public System.Type MakeGenericType(System.Type[]);",
        "public System.Type GetGenericTypeDefinition();",
        "public System.Type[] GetGenericArguments();",
        "public System.Type[] get_GenericTypeArguments();",
        "public boolean get_IsGenericType();",
        "public boolean get_IsConstructedGenericType();",
        "public boolean Equals(System.Type);",
    ], members
    classpath = os.pathsep.join((str(CLASSES), str(TEST_CLASSES)))
    result = run("java", "-cp", classpath, "System.TypeIdentityCandidateTest").strip()
    assert result.startswith("PASS selected System.Type identity")
    external_result = run("java", "-cp", classpath, "consumer.ProductTypeIdentityConsumer").strip()
    assert external_result == "PASS external System.Type selected identity consumer"
    EVIDENCE.write_text(json.dumps({
        "schemaVersion": 1,
        "upstreamFullName": "System.Type",
        "sourceCommit": provenance["sourceCommit"],
        "coreLibSha256": snapshot["assemblySha256"],
        "snapshotSha256": sha256(SNAPSHOT),
        "sourcePath": SOURCE.relative_to(ROOT).as_posix(),
        "sourceSha256": sha256(SOURCE),
        "testPath": TEST.relative_to(ROOT).as_posix(),
        "testSha256": sha256(TEST),
        "externalConsumerPath": EXTERNAL.relative_to(ROOT).as_posix(),
        "externalConsumerSha256": sha256(EXTERNAL),
        "publicMembers": members,
        "testResult": result,
        "externalConsumerResult": external_result,
        "status": "SELECTED_IDENTITY_CANDIDATE; complete 181-method/70-property System.Type surface, MemberInfo inheritance, generic-parameter Types, public null/error mapping and release qualification OPEN",
    }, indent=2) + "\n", encoding="utf-8")
    print(result)
    print(external_result)


if __name__ == "__main__":
    main()
