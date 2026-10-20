"""Verify compile-only Java representations of the pinned remaining N01 methods.

Each entry is independently compiled against temporary support declarations. A
successful probe establishes syntax feasibility only, never behavior or a
qualified product API.
"""

import argparse
import hashlib
import json
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
SOURCE = EVIDENCE / "n01-remaining-methods-v10.0.12.json"
LEDGER = EVIDENCE / "n01-remaining-java-declarations-v10.0.12.json"
PROBE = runpy.run_path(str(Path(__file__).with_name("verify-selected-method-java-declarations.py")))


def batch_for_index(index):
    # Batch 1001 is the collective-erasure audit between the two probe runs.
    return f"Batch-{index + (867 if index <= 132 else 869)}"


def method_inventory():
    inventory = json.loads(SOURCE.read_text(encoding="utf-8"))
    methods = [(batch["batch"], method) for batch in inventory["batches"] for method in batch["members"]]
    if len(methods) != 327 or len({(m["declaringType"], m["signature"]) for _, m in methods}) != 327:
        raise ValueError("Remaining method inventory must contain 327 distinct identities")
    return inventory, methods


def verify_method(index, source_batch, method, source_root):
    source = source_root / method["owningSourcePath"]
    snapshot = ROOT / method["snapshot"]
    if hashlib.sha256(source.read_bytes()).hexdigest() != method["owningSourceSha256"]:
        raise ValueError(f"Pinned owning source hash mismatch at remaining method {index}")
    if hashlib.sha256(snapshot.read_bytes()).hexdigest() != method["snapshotSha256"]:
        raise ValueError(f"Pinned metadata snapshot hash mismatch at remaining method {index}")
    normalized = {**method, "name": method["method"], "batch": source_batch}
    try:
        result = PROBE["verify_one"](index, normalized, source_root)
    except ValueError as error:
        return {
            "index": index,
            "sourceBatch": source_batch,
            "declaringType": method["declaringType"],
            "metadataSignature": method["signature"],
            "result": "PROBE_UNSUPPORTED; BEHAVIOR_UNVERIFIED",
            "probeError": str(error),
        }
    result["sourceBatch"] = source_batch
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preview-count", type=int)
    mode.add_argument("--append-index", type=int)
    mode.add_argument("--verify-ledger", action="store_true")
    args = parser.parse_args()
    inventory, methods = method_inventory()
    ledger = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {
        "schemaVersion": 1,
        "sourceCommit": inventory["sourceCommit"],
        "coreLibSha256": inventory["coreLibSha256"],
        "remainingMethodCount": len(methods),
        "scope": "Independent compile-only Java declaration probes with temporary support types; no product behavior or public facade qualification",
        "entries": [],
    }
    if ledger["sourceCommit"] != inventory["sourceCommit"] or ledger["remainingMethodCount"] != len(methods):
        raise ValueError("Remaining-method baseline mismatch")
    if args.preview_count is not None:
        if args.preview_count < 1 or args.preview_count > len(methods):
            raise ValueError("Preview count out of range")
        results = [verify_method(i, batch, method, args.source_root) for i, (batch, method) in enumerate(methods[:args.preview_count], 1)]
        from collections import Counter
        print("PREVIEW", args.preview_count, dict(Counter(result["result"] for result in results)))
        for result in results:
            if result["result"] != "JAVA_DECLARATION_COMPILED; BEHAVIOR_UNVERIFIED":
                print("BLOCKED", result["index"], result.get("compilerError") or result.get("probeError"))
        return
    if args.append_index is not None:
        index = args.append_index
        if index < 1 or index > len(methods) or len(ledger["entries"]) != index - 1:
            raise ValueError("Remaining method append must be sequential")
        source_batch, method = methods[index - 1]
        result = verify_method(index, source_batch, method, args.source_root)
        result["batch"] = batch_for_index(index)
        ledger["entries"].append(result)
        LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(result["result"].split(";", 1)[0], index, result["declaringType"], result["metadataSignature"])
        return
    for index, observed in enumerate(ledger["entries"], 1):
        source_batch, method = methods[index - 1]
        expected = verify_method(index, source_batch, method, args.source_root)
        if observed != {**expected, "batch": batch_for_index(index)}:
            raise ValueError(f"Remaining method ledger drift at index {index}")
    print(f"PASS: {len(ledger['entries'])}/{len(methods)} remaining method declarations and source hashes")


if __name__ == "__main__":
    main()
