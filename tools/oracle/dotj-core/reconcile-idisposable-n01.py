"""Reconcile the selected IDisposable naming ledger with its compiled product candidate."""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
LEDGER = EVIDENCE / "disposal-n01-v10.0.12.json"
PRODUCT = EVIDENCE / "idisposable-product-v1.json"
RIGHTS = EVIDENCE / "idisposable-rights-v10.0.12.json"
SNAPSHOT = EVIDENCE / "api-shapes-v10.0.12/idisposable.json"
REVISION = EVIDENCE / "idisposable-n01-product-revision-v10.0.12.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    ledger = read(LEDGER)
    product = read(PRODUCT)
    rights = read(RIGHTS)
    snapshot = read(SNAPSHOT)
    source = ROOT / product["sourcePath"]
    if (product["sourceCommit"] != ledger["sourceCommit"] or
            product["sourceCommit"] != rights["upstreamCommit"] or
            product["coreLibSha256"] != ledger["coreLibSha256"] or
            product["snapshotSha256"] != sha256(SNAPSHOT) or
            product["sourceSha256"] != sha256(source)):
        raise ValueError("Pinned source, metadata, or product evidence drift")
    if (snapshot["type"]["fullName"] != "System.IDisposable" or
            [(item["Name"], item["signature"]) for item in snapshot["type"]["methods"]] !=
            [("Dispose", "Void Dispose()")]):
        raise ValueError("Upstream IDisposable metadata changed")
    if (product["binaryName"] != "System.IDisposable" or
            product["publicMembers"] != ["public abstract void Dispose();"] or
            product["jarEntries"] != ["META-INF/MANIFEST.MF", "System/IDisposable.class"] or
            not product["independentConsumer"].startswith("PASS:") or
            not product["productContractConsumer"].startswith("PASS:")):
        raise ValueError("Compiled product interface evidence changed")
    if rights["overallE01Status"] != "OPEN" or rights["selectedSliceStatus"] != "RESEARCH_ELIGIBLE; PUBLIC_RELEASE_BLOCKED":
        raise ValueError("E01 release status changed; review the qualification decision")
    disposable = next(item for item in ledger["symbols"] if item["upstreamFullName"] == "System.IDisposable")
    if len(ledger["symbols"]) != 2 or disposable["javaPackageCandidate"] != "System" or disposable["javaMethodCandidate"] != "Dispose":
        raise ValueError("Selected N01 identity changed")
    expected_status = "EXACT_NAME_JAVA_INTERFACE_COMPILED; BEHAVIOR_AND_RELEASE_UNQUALIFIED"
    if args.write:
        if (disposable["javaSourceStatus"] != "NOT CREATED" or
                disposable["mappingStatus"] != "EXACT-NAME CANDIDATE; compiled Java API and ownership behavior pending" or
                REVISION.exists()):
            raise ValueError("Expected historical ledger state or revision file changed")
        before = sha256(LEDGER)
        previous = {"javaSourceStatus": disposable["javaSourceStatus"],
                    "mappingStatus": disposable["mappingStatus"]}
        disposable["javaSourceStatus"] = "CREATED_AND_COMPILED"
        disposable["javaProductSourcePath"] = product["sourcePath"]
        disposable["javaProductSourceSha256"] = product["sourceSha256"]
        disposable["javaProductEvidence"] = PRODUCT.relative_to(EVIDENCE).as_posix()
        disposable["mappingStatus"] = expected_status
        ledger["limits"][0] = ("This is a selected two-interface ledger, not complete N01-T1/T2 for core. "
                                "IDisposable has a compiled exact-name Java interface candidate; IAsyncDisposable "
                                "and the broader public surface remain unqualified.")
        LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        REVISION.write_text(json.dumps({
            "schemaVersion": 1,
            "sourceCommit": ledger["sourceCommit"],
            "previousLedgerSha256": before,
            "revisedLedgerSha256": sha256(LEDGER),
            "productEvidenceSha256": sha256(PRODUCT),
            "previousStatus": previous,
            "revisedStatus": expected_status,
            "limitation": "No public behavior or release qualification; E01 and broader N01 remain open.",
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        revision = read(REVISION)
        if (revision["revisedLedgerSha256"] != sha256(LEDGER) or
                revision["productEvidenceSha256"] != sha256(PRODUCT) or
                disposable["javaSourceStatus"] != "CREATED_AND_COMPILED" or
                disposable["mappingStatus"] != expected_status or
                disposable["javaProductSourceSha256"] != product["sourceSha256"]):
            raise ValueError("Reconciled IDisposable N01 ledger drift")
    print("PASS: IDisposable exact-name compiled candidate reconciled; E01 and behavior qualification remain open")


if __name__ == "__main__":
    main()
