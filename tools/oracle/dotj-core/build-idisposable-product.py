"""Build and exercise the first public dotj-core interface against pinned metadata."""

import hashlib
import json
import os
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "dotj-core/dotj-core-public/src/main/java/System/IDisposable.java"
SNAPSHOT = ROOT / "planning/stage-2/repos/dotj-core/evidence/api-shapes-v10.0.12/idisposable.json"
PROVENANCE = SNAPSHOT.with_name("idisposable-provenance.json")
CONSUMER = ROOT / "tools/oracle/dotj-core/java-probes/consumer/IndependentDisposableConsumer.java"
PRODUCT_CONSUMER = ROOT / "dotj-core/dotj-core-public/src/test/java/consumer/ProductDisposableContractConsumer.java"
BUILD = ROOT / "dotj-core/dotj-core-public/build/idisposable-v1"
CLASSES = BUILD / "classes"
JAR = BUILD / "dotj-core-idisposable-v1.jar"
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence/idisposable-product-v1.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*command):
    return subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True).stdout


def main():
    metadata = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    assert sha256(SNAPSHOT) == provenance["snapshotSha256"]
    assert metadata["assemblySha256"] == provenance["installedCoreLibSha256"]
    declaration = metadata["type"]
    assert declaration["fullName"] == "System.IDisposable"
    assert declaration["isInterface"] and not declaration["constructors"]
    assert not declaration["properties"] and not declaration["events"] and not declaration["fields"]
    assert [(m["Name"], m["signature"], m["returnType"], m["parameters"]) for m in declaration["methods"]] == [
        ("Dispose", "Void Dispose()", "System.Void", [])]

    CLASSES.mkdir(parents=True, exist_ok=True)
    run("javac", "--release", "21", "-d", str(CLASSES), str(SOURCE))
    class_path = CLASSES / "System/IDisposable.class"
    public = run("javap", "-public", "-classpath", str(CLASSES), "System.IDisposable")
    members = [line.strip() for line in public.splitlines() if line.strip().endswith(";")]
    assert "public interface System.IDisposable" in public
    assert members == ["public abstract void Dispose();"], members

    manifest = b"Manifest-Version: 1.0\r\nCreated-By: dotj-core public bootstrap\r\n\r\n"
    with zipfile.ZipFile(JAR, "w") as archive:
        for name, data in (("META-INF/MANIFEST.MF", manifest),
                           ("System/IDisposable.class", class_path.read_bytes())):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 20, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 0
            info.external_attr = 0
            archive.writestr(info, data)
    with zipfile.ZipFile(JAR) as archive:
        assert archive.namelist() == ["META-INF/MANIFEST.MF", "System/IDisposable.class"]
        assert archive.read("System/IDisposable.class") == class_path.read_bytes()

    consumer_classes = BUILD / "consumer-classes"
    consumer_classes.mkdir(parents=True, exist_ok=True)
    run("javac", "--release", "21", "-cp", str(JAR), "-d", str(consumer_classes),
        str(CONSUMER), str(PRODUCT_CONSUMER))
    consumer_result = run("java", "-cp", os.pathsep.join((str(consumer_classes), str(JAR))),
                          "consumer.IndependentDisposableConsumer").strip()
    assert consumer_result == "PASS: independent IDisposable candidate consumer"
    product_result = run("java", "-cp", os.pathsep.join((str(consumer_classes), str(JAR))),
                         "consumer.ProductDisposableContractConsumer").strip()
    assert product_result == "PASS: product IDisposable shape, explicit dispatch, borrowed ownership and failure propagation"

    result = {
        "schemaVersion": 1,
        "sourcePath": SOURCE.relative_to(ROOT).as_posix(),
        "sourceSha256": sha256(SOURCE),
        "sourceCommit": provenance["sourceCommit"],
        "coreLibSha256": metadata["assemblySha256"],
        "snapshotSha256": sha256(SNAPSHOT),
        "binaryName": "System.IDisposable",
        "publicMembers": members,
        "jarEntries": ["META-INF/MANIFEST.MF", "System/IDisposable.class"],
        "classSha256": sha256(class_path),
        "jarSha256": sha256(JAR),
        "independentConsumer": consumer_result,
        "productContractConsumer": product_result,
        "status": "PUBLIC_INTERFACE_CANDIDATE; broader N01, E01 release rights and behavior qualification OPEN",
    }
    EVIDENCE.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS product IDisposable exact public member and independent JDK consumer")


if __name__ == "__main__":
    main()
