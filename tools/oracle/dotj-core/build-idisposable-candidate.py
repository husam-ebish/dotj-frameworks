"""Build a compile-only, independently authored IDisposable shape candidate.

The resulting JAR is development evidence, not a qualified product package.
"""

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tools/oracle/dotj-core/java-probes/System/IDisposable.java"
BUILD = ROOT / "dotj-core/dotj-core-01/build/idisposable-candidate"
CLASS = BUILD / "classes/System/IDisposable.class"
JAR = BUILD / "idisposable-candidate.jar"
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence/idisposable-candidate-jar-v1.json"
EXPECTED_ENTRIES = ["META-INF/MANIFEST.MF", "System/IDisposable.class"]


def hash_bytes(value):
    return hashlib.sha256(value).hexdigest()


def archive_entry(name, contents):
    info = zipfile.ZipInfo(name, date_time=(2026, 10, 20, 0, 0, 0))
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 0
    info.external_attr = 0
    return info, contents


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(["javac", "--release", "21", "-d", str(BUILD / "classes"), str(SOURCE)],
                            cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    class_bytes = CLASS.read_bytes()
    manifest_bytes = b"Manifest-Version: 1.0\r\nCreated-By: dotj compile-only oracle\r\n\r\n"
    with zipfile.ZipFile(JAR, "w") as archive:
        for name, contents in [archive_entry(EXPECTED_ENTRIES[0], manifest_bytes),
                               archive_entry(EXPECTED_ENTRIES[1], class_bytes)]:
            archive.writestr(name, contents)
    with zipfile.ZipFile(JAR) as archive:
        entries = archive.namelist()
        assert entries == EXPECTED_ENTRIES, entries
        assert archive.read(EXPECTED_ENTRIES[1]) == class_bytes
    output = subprocess.run(["javap", "-public", "-classpath", str(JAR), "System.IDisposable"],
                            cwd=ROOT, capture_output=True, text=True, check=True).stdout
    assert "public interface System.IDisposable" in output
    assert "public abstract void Dispose();" in output
    result = {
        "schemaVersion": 1,
        "purpose": "Compile-only exact-name and distribution-content candidate; not a product package",
        "sourcePath": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "sourceSha256": hash_bytes(SOURCE.read_bytes()),
        "entries": entries,
        "classSha256": hash_bytes(class_bytes),
        "jarSha256": hash_bytes(JAR.read_bytes()),
        "javapAsserted": ["public interface System.IDisposable", "public abstract void Dispose();"],
        "releaseQualification": "OPEN: E01 notice/license review, E02/E03/N01, public behavior and packaging",
    }
    EVIDENCE.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS compile-only IDisposable candidate:", result["jarSha256"])


if __name__ == "__main__":
    main()
