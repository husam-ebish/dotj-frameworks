"""Reconcile individual Java syntax probes with known public-contract blockers."""

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
SELECTED_INVENTORY = EVIDENCE / "n01-selected-methods-v10.0.12.json"
REMAINING_INVENTORY = EVIDENCE / "n01-remaining-methods-v10.0.12.json"
SELECTED_LEDGER = EVIDENCE / "n01-java-declarations-v10.0.12.json"
REMAINING_LEDGER = EVIDENCE / "n01-remaining-java-declarations-v10.0.12.json"
DECLARATION_AUDIT = EVIDENCE / "n01-java-declaration-audit-v10.0.12.json"
COLLISIONS = EVIDENCE / "n01-java-erasure-collisions-v10.0.12.json"
VISIBILITY = EVIDENCE / "n01-erasure-public-visibility-v10.0.12.json"
STATIC = EVIDENCE / "n01-static-generic-probe-revision-v10.0.12.json"
OPTIONAL = EVIDENCE / "n01-optional-waitall-revision-v10.0.12.json"
BOXING = EVIDENCE / "n01-generic-primitive-probe-revision-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-public-method-dispositions-v10.0.12.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(entry):
    return entry["declaringType"], entry["metadataSignature"]


def revision_set(revisions):
    result = {identity(entry) for entry in revisions}
    if len(result) != len(revisions):
        raise ValueError("Duplicate revision identity")
    return result


def main():
    selected_inventory = read(SELECTED_INVENTORY)
    remaining_inventory = read(REMAINING_INVENTORY)
    selected_ledger = read(SELECTED_LEDGER)
    remaining_ledger = read(REMAINING_LEDGER)
    declaration_audit = read(DECLARATION_AUDIT)
    collisions = read(COLLISIONS)
    visibility = read(VISIBILITY)
    static = read(STATIC)
    optional = read(OPTIONAL)
    boxing = read(BOXING)
    baseline = selected_inventory["sourceCommit"]
    for item in (remaining_inventory, selected_ledger, remaining_ledger, declaration_audit,
                 collisions, visibility, static, optional, boxing):
        if item["sourceCommit"] != baseline:
            raise ValueError("Different pinned upstream baselines")
    if (declaration_audit["selectedLedgerSha256"] != sha256(SELECTED_LEDGER) or
            declaration_audit["remainingLedgerSha256"] != sha256(REMAINING_LEDGER) or
            collisions["selectedInventorySha256"] != sha256(SELECTED_INVENTORY) or
            collisions["remainingInventorySha256"] != sha256(REMAINING_INVENTORY) or
            declaration_audit["javaDeclarationsCompiled"] != 426):
        raise ValueError("Pinned declaration evidence changed")
    if visibility["disposition"] != (
            "BLOCKED_PUBLIC_EXACT_NAME: a compiler or backend visibility strategy is needed before the mapped pair can be a qualified public .j contract"):
        raise ValueError("Representative erasure visibility finding changed")
    entries = selected_ledger["entries"] + remaining_ledger["entries"]
    methods = selected_inventory["entries"] + [member for batch in remaining_inventory["batches"]
                                                for member in batch["members"]]
    if len(entries) != 426 or len(methods) != 426:
        raise ValueError("Complete method inventory required")
    inventory = {(method["declaringType"], method["signature"]): method for method in methods}
    if len(inventory) != 426:
        raise ValueError("Duplicate pinned method identity")
    colliding = {(group["declaringType"], row["metadataSignature"])
                 for group in collisions["collisions"] for row in group["members"]}
    if len(collisions["collisions"]) != 12 or len(colliding) != 26:
        raise ValueError("Expected 12 groups with 26 distinct colliding identities")
    static_set = revision_set(static["revisions"])
    boxing_set = revision_set(boxing["revisions"])
    optional_entry = remaining_ledger["entries"][optional["index"] - 1]
    optional_set = {identity(optional_entry)}
    special = [colliding, static_set, boxing_set, optional_set]
    if (len(static_set), len(boxing_set), len(optional_set)) != (3, 4, 1):
        raise ValueError("Unexpected bounded adaptation counts")
    if sum(len(group) for group in special) != len(set().union(*special)):
        raise ValueError("Public disposition groups overlap")
    if optional_entry["metadataSignature"] != optional["metadataSignature"]:
        raise ValueError("Optional member identity changed")
    for revision in static["revisions"]:
        ledger = selected_ledger if revision["probeBatch"] == "Batch-794" else remaining_ledger
        candidate = ledger["entries"][revision["index"] - 1]
        if identity(candidate) != identity(revision) or candidate["javaDeclaration"] != revision["javaDeclaration"]:
            raise ValueError("Static generic revision no longer matches the ledger")
    for revision in boxing["revisions"]:
        candidate = remaining_ledger["entries"][revision["index"] - 1]
        if identity(candidate) != identity(revision) or candidate["javaDeclaration"] != revision["newJavaDeclaration"]:
            raise ValueError("Primitive generic revision no longer matches the ledger")
    dispositions = []
    for entry in entries:
        key = identity(entry)
        method = inventory.get(key)
        if method is None or entry["result"] != "JAVA_DECLARATION_COMPILED; BEHAVIOR_UNVERIFIED":
            raise ValueError("Individual syntax record or inventory identity missing")
        if key in colliding:
            status = "BLOCKED_PUBLIC_EXACT_NAME_JVM_ERASURE"
        elif key in static_set:
            status = "BACKEND_CANDIDATE_STATIC_GENERIC_SCOPE_CHANGE"
        elif key in optional_set:
            status = "BACKEND_CANDIDATE_OPTIONAL_DEFAULT_UNVERIFIED"
        elif key in boxing_set:
            status = "BACKEND_CANDIDATE_BOXED_GENERIC_SEMANTICS_UNVERIFIED"
        else:
            status = "INDIVIDUAL_SYNTAX_ONLY"
        dispositions.append({
            "declaringType": key[0],
            "metadataSignature": key[1],
            "sourceBatch": entry["sourceBatch"],
            "probeBatch": entry["batch"],
            "owningSourceSha256": method["owningSourceSha256"],
            "disposition": status,
            "publicBehaviorQualified": False,
        })
    counts = dict(sorted(Counter(item["disposition"] for item in dispositions).items()))
    expected = {
        "BACKEND_CANDIDATE_BOXED_GENERIC_SEMANTICS_UNVERIFIED": 4,
        "BACKEND_CANDIDATE_OPTIONAL_DEFAULT_UNVERIFIED": 1,
        "BACKEND_CANDIDATE_STATIC_GENERIC_SCOPE_CHANGE": 3,
        "BLOCKED_PUBLIC_EXACT_NAME_JVM_ERASURE": 26,
        "INDIVIDUAL_SYNTAX_ONLY": 392,
    }
    if counts != expected:
        raise ValueError("Unexpected public mapping disposition counts: " + str(counts))
    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "sourceCommit": baseline,
        "coreLibSha256": selected_ledger["coreLibSha256"],
        "selectedLedgerSha256": sha256(SELECTED_LEDGER),
        "remainingLedgerSha256": sha256(REMAINING_LEDGER),
        "erasureCollisionSha256": sha256(COLLISIONS),
        "declarationsIndividuallyCompiled": 426,
        "qualifiedPublicMethods": 0,
        "knownStructuralPublicBlockers": 29,
        "semanticAdaptationsPending": 5,
        "dispositionCounts": counts,
        "scope": "Selected declared-public methods only. Individual compilation is syntax evidence; no method receives public behavior or release qualification.",
        "entries": dispositions,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: 426 dispositions; 29 structural blockers, five semantic adaptations, 392 syntax-only candidates, zero qualified public methods")


if __name__ == "__main__":
    main()
