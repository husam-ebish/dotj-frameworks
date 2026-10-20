"""Audit the two bounded N01 Java declaration probe ledgers."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
SELECTED = EVIDENCE / "n01-java-declarations-v10.0.12.json"
REMAINING = EVIDENCE / "n01-remaining-java-declarations-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-java-declaration-audit-v10.0.12.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    selected = read(SELECTED)
    remaining = read(REMAINING)
    a = selected["entries"]
    b = remaining["entries"]
    if selected["sourceCommit"] != remaining["sourceCommit"] or selected["coreLibSha256"] != remaining["coreLibSha256"]:
        raise ValueError("Probe ledgers have different immutable upstream baselines")
    if len(a) != 99 or len(b) != 327 or remaining["remainingMethodCount"] != 327:
        raise ValueError("Unexpected bounded method counts")
    if [entry["index"] for entry in a] != list(range(1, 100)):
        raise ValueError("Selected indices are not contiguous")
    if [entry["index"] for entry in b] != list(range(1, 328)):
        raise ValueError("Remaining indices are not contiguous")
    if [entry["batch"] for entry in a] != [f"Batch-{number}" for number in range(768, 867)]:
        raise ValueError("Selected batch IDs drifted")
    expected_remaining_batches = ([f"Batch-{number}" for number in range(868, 1000)] +
                                  [f"Batch-{number}" for number in range(1002, 1197)])
    if [entry["batch"] for entry in b] != expected_remaining_batches:
        raise ValueError("Remaining batch IDs drifted")
    identities = [(entry["declaringType"], entry["metadataSignature"]) for entry in a + b]
    if len(set(identities)) != 426:
        raise ValueError("Duplicate declaration identity across ledgers")
    compiled = [entry for entry in a + b if entry["result"] == "JAVA_DECLARATION_COMPILED; BEHAVIOR_UNVERIFIED"]
    blocked = [entry for entry in a + b if entry["result"] == "BLOCKED_JAVA_DECLARATION; BEHAVIOR_UNVERIFIED"]
    unsupported = [entry for entry in a + b if entry["result"] == "PROBE_UNSUPPORTED; BEHAVIOR_UNVERIFIED"]
    if (len(compiled) != 422 or len(blocked) != 3 or len(unsupported) != 1 or
            {entry["batch"] for entry in blocked} != {
                "Batch-794", "Batch-1125", "Batch-1126"} or
            unsupported[0]["batch"] != "Batch-1167"):
        raise ValueError("Unexpected declaration result counts")
    audit = {
        "schemaVersion": 1,
        "sourceCommit": selected["sourceCommit"],
        "coreLibSha256": selected["coreLibSha256"],
        "selectedLedgerSha256": sha256(SELECTED),
        "remainingLedgerSha256": sha256(REMAINING),
        "selectedMethodsProbed": 99,
        "remainingMethodsInventoried": 327,
        "remainingMethodsRecorded": 327,
        "remainingMethodsWithoutCompilerResult": len(unsupported),
        "distinctMethodsRecorded": 426,
        "javaDeclarationsCompiled": len(compiled),
        "javaDeclarationsBlocked": len(blocked),
        "javaProbesUnsupported": len(unsupported),
        "blockedIdentities": [{
            "declaringType": entry["declaringType"],
            "metadataSignature": entry["metadataSignature"],
            "compilerError": entry["compilerError"],
            "sourceBatch": entry["sourceBatch"],
            "probeBatch": entry["batch"],
        } for entry in blocked],
        "unsupportedIdentities": [{
            "declaringType": entry["declaringType"],
            "metadataSignature": entry["metadataSignature"],
            "probeError": entry["probeError"],
            "sourceBatch": entry["sourceBatch"],
            "probeBatch": entry["batch"],
        } for entry in unsupported],
        "scope": "Independent syntax probes with temporary support types; no collective overload, behavior, public facade, or release qualification",
    }
    OUTPUT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: 426 distinct pinned method records; 422 compile, three Java blockers, one probe limitation")


if __name__ == "__main__":
    main()
