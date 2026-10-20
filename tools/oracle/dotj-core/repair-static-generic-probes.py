"""Recheck the three pinned static generic-owner methods with Java type-parameter lifting."""

import argparse
import hashlib
import json
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
PROBE = runpy.run_path(str(Path(__file__).with_name("verify-selected-method-java-declarations.py")))
REMAINING_PROBE = runpy.run_path(str(Path(__file__).with_name("verify-remaining-method-java-declarations.py")))
SELECTED_METHODS = EVIDENCE / "n01-selected-methods-v10.0.12.json"
REMAINING_METHODS = EVIDENCE / "n01-remaining-methods-v10.0.12.json"
SELECTED_LEDGER = EVIDENCE / "n01-java-declarations-v10.0.12.json"
REMAINING_LEDGER = EVIDENCE / "n01-remaining-java-declarations-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-static-generic-probe-revision-v10.0.12.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def update(ledger, index, expected):
    old = ledger["entries"][index - 1]
    if old["index"] != index or old["result"] != "BLOCKED_JAVA_DECLARATION; BEHAVIOR_UNVERIFIED":
        raise ValueError("Expected historical static-generic blocker at " + str(index))
    if old["compilerError"] != "non-static type variable TResult cannot be referenced from a static context":
        raise ValueError("Unexpected historical diagnostic at " + str(index))
    expected["batch"] = old["batch"]
    if expected["result"] != "JAVA_DECLARATION_COMPILED; BEHAVIOR_UNVERIFIED" or expected["compilerError"] is not None:
        raise ValueError("Lifted Java method did not compile at " + str(index))
    if not expected["javaDeclaration"].startswith("public static <TResult> "):
        raise ValueError("Expected Java method-level TResult at " + str(index))
    ledger["entries"][index - 1] = expected
    return {
        "index": index,
        "sourceBatch": expected["sourceBatch"],
        "probeBatch": old["batch"],
        "declaringType": expected["declaringType"],
        "metadataSignature": expected["metadataSignature"],
        "previousCompilerError": old["compilerError"],
        "javaDeclaration": expected["javaDeclaration"],
        "sourceSha256": expected["generatedSourceSha256"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    selected = json.loads(SELECTED_METHODS.read_text(encoding="utf-8"))
    remaining = json.loads(REMAINING_METHODS.read_text(encoding="utf-8"))
    methods = [(batch["batch"], member) for batch in remaining["batches"] for member in batch["members"]]
    if len(selected["entries"]) != 99 or len(methods) != 327:
        raise ValueError("Complete pinned method inventories required")
    selected_ledger = json.loads(SELECTED_LEDGER.read_text(encoding="utf-8"))
    remaining_ledger = json.loads(REMAINING_LEDGER.read_text(encoding="utf-8"))
    if len(selected_ledger["entries"]) != 99 or len(remaining_ledger["entries"]) != 327:
        raise ValueError("Complete historical probe ledgers required")
    before = {"selected": sha256(SELECTED_LEDGER), "remaining": sha256(REMAINING_LEDGER)}
    revisions = [update(selected_ledger, 27,
                        PROBE["verify_one"](27, selected["entries"][26], args.source_root))]
    for index in (256, 257):
        batch, method = methods[index - 1]
        revisions.append(update(remaining_ledger, index,
                                REMAINING_PROBE["verify_method"](index, batch, method, args.source_root)))
    for path, ledger in ((SELECTED_LEDGER, selected_ledger), (REMAINING_LEDGER, remaining_ledger)):
        path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "sourceCommit": selected["sourceCommit"],
        "previousLedgerSha256": before,
        "revisedLedgerSha256": {"selected": sha256(SELECTED_LEDGER), "remaining": sha256(REMAINING_LEDGER)},
        "scope": "Java static method type-parameter lifting is a compile-only backend candidate. It changes the Java generic method arity and does not qualify exact .NET public metadata or behavior.",
        "revisions": revisions,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: three pinned static generic-owner declarations compile with method-level TResult")


if __name__ == "__main__":
    main()
