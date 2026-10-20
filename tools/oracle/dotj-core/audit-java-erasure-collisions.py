"""Find JVM-erased overload conflicts in the 426 pinned N01 method identities."""

import hashlib
import json
import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
SELECTED = EVIDENCE / "n01-selected-methods-v10.0.12.json"
REMAINING = EVIDENCE / "n01-remaining-methods-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-java-erasure-collisions-v10.0.12.json"
GENERIC = re.compile(r"(?P<base>System\.[A-Za-z0-9_.$]+)`(?P<arity>\d+)(?:\[.*\])?\Z")
PRIMITIVES = {"System.Boolean": "boolean", "System.Int32": "int", "System.Void": "void"}


def erase(metadata):
    if metadata.endswith("[]"):
        return erase(metadata[:-2]) + "[]"
    if metadata in ("T", "TResult"):
        return "java.lang.Object"
    if metadata in PRIMITIVES:
        return PRIMITIVES[metadata]
    match = GENERIC.fullmatch(metadata)
    if match:
        return match["base"] + "_" + match["arity"]
    if metadata.startswith("System."):
        return metadata
    raise ValueError("Unsupported parameter metadata: " + metadata)


def verify_javac_duplicate():
    source = """class Task {
    static Task FromException(Exception exception) { return null; }
    static <TResult> Task_1<TResult> FromException(Exception exception) { return null; }
}
class Task_1<TResult> {}
"""
    with tempfile.TemporaryDirectory(prefix="dotj-erasure-") as folder:
        java = Path(folder) / "Task.java"
        java.write_text(source, encoding="utf-8")
        result = subprocess.run(["javac", "--release", "21", str(java)], capture_output=True, text=True)
    if result.returncode == 0 or "FromException(Exception) is already defined" not in result.stderr:
        raise RuntimeError("Expected JVM overload conflict was not reproduced: " + result.stderr)
    return "method FromException(Exception) is already defined in class Task"


def main():
    selected = json.loads(SELECTED.read_text(encoding="utf-8"))
    remaining = json.loads(REMAINING.read_text(encoding="utf-8"))
    rows = [(entry["declaringType"], entry["name"], entry["signature"], entry["parameters"], entry["batch"])
            for entry in selected["entries"]]
    rows += [(entry["declaringType"], entry["method"], entry["signature"], entry["parameters"], batch["batch"])
             for batch in remaining["batches"] for entry in batch["members"]]
    if len(rows) != 426 or len({(owner, signature) for owner, _, signature, _, _ in rows}) != 426:
        raise ValueError("Expected 426 distinct selected method identities")
    if selected["sourceCommit"] != remaining["sourceCommit"] or selected["coreLibSha256"] != remaining["coreLibSha256"]:
        raise ValueError("Selected inventories use different pinned baselines")
    groups = defaultdict(list)
    for owner, name, signature, parameters, batch in rows:
        key = (owner, name, tuple(erase(parameter["type"]) for parameter in parameters))
        groups[key].append({"metadataSignature": signature, "sourceBatch": batch})
    collisions = [{
        "declaringType": owner,
        "method": name,
        "erasedParameterTypes": list(parameters),
        "members": members,
    } for (owner, name, parameters), members in sorted(groups.items()) if len(members) > 1]
    if len(collisions) != 12 or sum(len(group["members"]) for group in collisions) != 26:
        raise ValueError("Unexpected erased overload collision count")
    audit = {
        "schemaVersion": 1,
        "sourceCommit": selected["sourceCommit"],
        "coreLibSha256": selected["coreLibSha256"],
        "selectedInventorySha256": hashlib.sha256(SELECTED.read_bytes()).hexdigest(),
        "remainingInventorySha256": hashlib.sha256(REMAINING.read_bytes()).hexdigest(),
        "methodIdentities": 426,
        "erasedOverloadGroups": len(groups),
        "collisionGroups": len(collisions),
        "collidingMethodIdentities": sum(len(group["members"]) for group in collisions),
        "representativeJavacDiagnostic": verify_javac_duplicate(),
        "scope": "Static JVM-erasure projection of selected declared-public method metadata; candidate conflicts need a source-level API strategy and collective compilation",
        "collisions": collisions,
    }
    OUTPUT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: 426 pinned methods checked; 12 erased overload collision groups involving 26 identities; representative javac rejection reproduced")


if __name__ == "__main__":
    main()
