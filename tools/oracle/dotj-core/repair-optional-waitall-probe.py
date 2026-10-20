"""Replace the pinned optional WaitAll syntax limitation with an overload probe."""

import argparse
import hashlib
import json
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
INVENTORY = EVIDENCE / "n01-remaining-methods-v10.0.12.json"
LEDGER = EVIDENCE / "n01-remaining-java-declarations-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-optional-waitall-revision-v10.0.12.json"
PROBE = runpy.run_path(str(Path(__file__).with_name("verify-remaining-method-java-declarations.py")))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    methods = [(batch["batch"], member) for batch in inventory["batches"] for member in batch["members"]]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if len(methods) != 327 or len(ledger["entries"]) != 327:
        raise ValueError("Complete remaining method ledger required")
    old = ledger["entries"][297]
    if (old["index"] != 298 or old["result"] != "PROBE_UNSUPPORTED; BEHAVIOR_UNVERIFIED" or
            old["probeError"] != "By-reference or optional parameter needs separate representation"):
        raise ValueError("Expected historical optional parameter limitation")
    previous_hash = sha256(LEDGER)
    batch, method = methods[297]
    revised = PROBE["verify_method"](298, batch, method, args.source_root)
    if (revised["result"] != "JAVA_DECLARATION_COMPILED; BEHAVIOR_UNVERIFIED" or
            "public static void WaitAll(" not in revised["javaDeclaration"] or
            "new CancellationToken()" not in revised["javaDeclaration"]):
        raise ValueError("Optional token overload did not compile")
    revised["batch"] = old["batch"]
    ledger["entries"][297] = revised
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "sourceCommit": inventory["sourceCommit"],
        "index": 298,
        "previousLedgerSha256": previous_hash,
        "revisedLedgerSha256": sha256(LEDGER),
        "historicalProbeError": old["probeError"],
        "metadataSignature": method["signature"],
        "javaDeclaration": revised["javaDeclaration"],
        "scope": "Compile-only overload candidate. The stub token constructor does not establish .NET default-value behavior or qualify the public API.",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: optional WaitAll overload compiled with pinned source and metadata")


if __name__ == "__main__":
    main()
