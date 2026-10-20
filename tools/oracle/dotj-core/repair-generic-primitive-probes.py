"""Reconcile four pinned N01 probes after boxing primitive generic arguments."""

import argparse
import hashlib
import json
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
INVENTORY = EVIDENCE / "n01-remaining-methods-v10.0.12.json"
LEDGER = EVIDENCE / "n01-remaining-java-declarations-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-generic-primitive-probe-revision-v10.0.12.json"
PROBE = runpy.run_path(str(Path(__file__).with_name("verify-remaining-method-java-declarations.py")))
INDICES = (217, 218, 219, 293)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    methods = [(batch["batch"], method) for batch in inventory["batches"] for method in batch["members"]]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if len(methods) != 327 or len(ledger["entries"]) != 327:
        raise ValueError("Complete remaining-method ledger required")
    original_hash = hashlib.sha256(LEDGER.read_bytes()).hexdigest()
    revisions = []
    for index in INDICES:
        source_batch, method = methods[index - 1]
        previous = ledger["entries"][index - 1]
        if previous["index"] != index or previous["compilerError"] != "unexpected type":
            raise ValueError("Expected original primitive-in-generic javac error at " + str(index))
        updated = PROBE["verify_method"](index, source_batch, method, args.source_root)
        updated["batch"] = previous["batch"]
        if updated["result"] != "JAVA_DECLARATION_COMPILED; BEHAVIOR_UNVERIFIED" or updated["compilerError"] is not None:
            raise ValueError("Boxed exact-name generic argument did not compile at " + str(index))
        ledger["entries"][index - 1] = updated
        revisions.append({
            "index": index,
            "originalProbeBatch": previous["batch"],
            "declaringType": previous["declaringType"],
            "metadataSignature": previous["metadataSignature"],
            "previousCompilerError": previous["compilerError"],
            "newJavaDeclaration": updated["javaDeclaration"],
            "newResult": updated["result"],
        })
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = {
        "schemaVersion": 1,
        "sourceCommit": inventory["sourceCommit"],
        "previousLedgerSha256": original_hash,
        "revisedLedgerSha256": hashlib.sha256(LEDGER.read_bytes()).hexdigest(),
        "reason": "Java generic arguments must be reference types; the original temporary syntax probe incorrectly emitted primitive boolean or int in four generic type arguments",
        "scope": "Compile-only correction to four evidence records; no behavior or public facade qualification",
        "revisions": revisions,
    }
    OUTPUT.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: four exact-name boxed generic declaration probes compiled; historical compiler failures retained in revision evidence")


if __name__ == "__main__":
    main()
