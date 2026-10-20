"""Bounded Java syntax check for the pinned optional Task.WaitAll token."""

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
INVENTORY = EVIDENCE / "n01-remaining-methods-v10.0.12.json"
LEDGER = EVIDENCE / "n01-remaining-java-declarations-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-optional-waitall-v10.0.12.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compile_java(source):
    with tempfile.TemporaryDirectory(prefix="dotj-optional-waitall-") as directory:
        file = Path(directory) / "Task.java"
        file.write_text(source, encoding="utf-8")
        return subprocess.run(["javac", "--release", "21", str(file)], capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    methods = [entry for batch in inventory["batches"] for entry in batch["members"]]
    method = methods[297]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))["entries"][297]
    if (method["declaringType"] != "System.Threading.Tasks.Task" or method["method"] != "WaitAll" or
            method["parameters"][1]["Name"] != "cancellationToken" or
            method["parameters"][1]["IsOptional"] is not True or
            ledger["result"] != "JAVA_DECLARATION_COMPILED; BEHAVIOR_UNVERIFIED" or
            "new CancellationToken()" not in ledger["javaDeclaration"]):
        raise ValueError("Pinned optional WaitAll method or probe result changed")
    source = args.source_root / method["owningSourcePath"]
    snapshot = ROOT / method["snapshot"]
    if sha256(source) != method["owningSourceSha256"] or sha256(snapshot) != method["snapshotSha256"]:
        raise ValueError("Pinned source or metadata snapshot hash mismatch")
    source_lines = source.read_text(encoding="utf-8-sig").splitlines()
    matching = [(index, line.strip()) for index, line in enumerate(source_lines, 1)
                if "public static void WaitAll(IEnumerable<Task> tasks, CancellationToken cancellationToken = default)" in line]
    if len(matching) != 1:
        raise ValueError("Optional parameter source declaration not found uniquely")
    declaration = """public class Task {
    public static void WaitAll(IEnumerable_1<Task> tasks, CancellationToken cancellationToken) {}
    public static void WaitAll(IEnumerable_1<Task> tasks) { WaitAll(tasks, new CancellationToken()); }
}
class IEnumerable_1<T> {}
class CancellationToken {}
"""
    direct = compile_java(declaration)
    consumer = compile_java(declaration + "class Consumer { static void call(IEnumerable_1<Task> tasks, CancellationToken token) { Task.WaitAll(tasks); Task.WaitAll(tasks, token); } }\n")
    if direct.returncode != 0 or consumer.returncode != 0:
        raise RuntimeError("Expected one- and two-argument Java calls did not compile: " + consumer.stderr)
    audit = {
        "schemaVersion": 1,
        "sourceCommit": inventory["sourceCommit"],
        "declaringType": method["declaringType"],
        "metadataSignature": method["signature"],
        "sourcePath": method["owningSourcePath"],
        "sourceSha256": method["owningSourceSha256"],
        "snapshot": method["snapshot"],
        "snapshotSha256": method["snapshotSha256"],
        "sourceLine": matching[0][0],
        "sourceDeclaration": matching[0][1],
        "metadataOptionalParameter": "cancellationToken",
        "twoArgumentJavaDeclaration": "COMPILED with temporary support types",
        "oneArgumentJavaCall": "COMPILED via explicit Java overload",
        "twoArgumentJavaCall": "COMPILED",
        "qualification": "The one-argument Java overload is a compile-only representation. A temporary token stub does not establish .NET default-value or WaitAll behavior; no public API is qualified",
    }
    OUTPUT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: optional WaitAll token source and metadata pinned; one- and two-argument Java calls compile")


if __name__ == "__main__":
    main()
