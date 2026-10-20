"""Verify three async-family arity pairs from pinned source and CoreLib metadata."""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
WP02 = EVIDENCE / "wp02-api-shapes-v10.0.12"
WP01 = EVIDENCE / "api-shapes-v10.0.12"
CORELIB = "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"
PIN = "4271d88e0aebf3d04f188f1334c2220d80555ef6"
FAMILIES = [
    ("Task", (WP02, "task"), (WP02, "task-generic"), False),
    ("TaskCompletionSource", (WP02, "task-completion-source"),
     (WP02, "task-completion-source-generic"), False),
    ("ValueTask", (WP01, "value-task"), (WP01, "value-task-generic"), True),
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_type(directory, name, source_root):
    provenance = json.loads((directory / f"{name}-provenance.json").read_text(encoding="utf-8"))
    snapshot = directory / f"{name}.json"
    source = source_root / provenance["sourcePath"]
    assert provenance["sourceCommit"] == PIN
    assert sha256(source) == provenance["sourceSha256"]
    assert sha256(snapshot) == provenance["snapshotSha256"]
    assert provenance.get("artifactSha256", provenance.get("installedCoreLibSha256")) == CORELIB
    data = json.loads(snapshot.read_text(encoding="utf-8"))
    assert data["assemblySha256"] == CORELIB
    return provenance, data["type"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    records = []
    for name, zero, one, value_type in FAMILIES:
        zero_provenance, zero_type = load_type(*zero, args.source_root)
        one_provenance, one_type = load_type(*one, args.source_root)
        namespace = "System.Threading.Tasks."
        assert zero_type["fullName"] == namespace + name
        assert one_type["fullName"] == namespace + name + "`1"
        assert len(zero_type["genericParameters"]) == 0
        assert len(one_type["genericParameters"]) == 1
        assert zero_type["isValueType"] is value_type and one_type["isValueType"] is value_type
        records.append({
            "family": name,
            "nonGeneric": zero_type["fullName"],
            "generic": one_type["fullName"],
            "genericParameter": one_type["genericParameters"][0]["Name"],
            "valueType": value_type,
            "sourcePaths": [zero_provenance["sourcePath"], one_provenance["sourcePath"]],
            "sourceSha256": [zero_provenance["sourceSha256"], one_provenance["sourceSha256"]],
            "javaCollision": "Two independent Java top-level types with this package and simple name would share one binary name",
        })
    output = {
        "schemaVersion": 1,
        "sourceCommit": PIN,
        "coreLibSha256": CORELIB,
        "families": records,
        "decision": "Exact-name Java representation unresolved; one raw/generic Java class would collapse two source identities",
        "limits": ["Selected declared-public metadata and source hashes, not full Task/ValueTask semantics.",
                   "No public Java Task, TaskCompletionSource, or ValueTask declaration is qualified."],
    }
    path = EVIDENCE / "task-family-arity-v10.0.12.json"
    path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print("PASS 3 pinned async family arity pairs")


if __name__ == "__main__":
    main()
