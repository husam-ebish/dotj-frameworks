"""Join pinned JVM-erasure collision groups to independent compiler outcomes."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
COLLISIONS = EVIDENCE / "n01-java-erasure-collisions-v10.0.12.json"
SELECTED = EVIDENCE / "n01-java-declarations-v10.0.12.json"
REMAINING = EVIDENCE / "n01-remaining-java-declarations-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-java-erasure-outcomes-v10.0.12.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    collision_audit = read(COLLISIONS)
    selected = read(SELECTED)
    remaining = read(REMAINING)
    if len(selected["entries"]) != 99 or len(remaining["entries"]) != 327:
        raise ValueError("Both individual declaration ledgers must be complete")
    if len(collision_audit["collisions"]) != 12:
        raise ValueError("Expected twelve pinned erasure groups")
    lookup = {(entry["declaringType"], entry["metadataSignature"]): entry
              for entry in selected["entries"] + remaining["entries"]}
    if len(lookup) != 426:
        raise ValueError("Individual method identities are not unique")
    joined = []
    for group in collision_audit["collisions"]:
        members = []
        for method in group["members"]:
            key = (group["declaringType"], method["metadataSignature"])
            if key not in lookup:
                raise ValueError("Collision member has no individual probe: " + str(key))
            entry = lookup[key]
            members.append({
                "metadataSignature": method["metadataSignature"],
                "sourceBatch": method["sourceBatch"],
                "individualProbeBatch": entry["batch"],
                "individualResult": entry["result"],
            })
        joined.append({
            "declaringType": group["declaringType"],
            "method": group["method"],
            "erasedParameterTypes": group["erasedParameterTypes"],
            "members": members,
        })
    colliding = [member for group in joined for member in group["members"]]
    if len(colliding) != 26 or not all(member["individualResult"] == "JAVA_DECLARATION_COMPILED; BEHAVIOR_UNVERIFIED"
                                      for member in colliding):
        raise ValueError("Unexpected individual outcomes in erasure groups")
    audit = {
        "schemaVersion": 1,
        "sourceCommit": collision_audit["sourceCommit"],
        "erasureAuditSha256": sha256(COLLISIONS),
        "selectedLedgerSha256": sha256(SELECTED),
        "remainingLedgerSha256": sha256(REMAINING),
        "erasureCollisionGroups": len(joined),
        "collidingMethodIdentities": len(colliding),
        "individuallyCompilableCollidingIdentities": len(colliding),
        "representativeCollectiveJavacDiagnostic": collision_audit["representativeJavacDiagnostic"],
        "qualification": "All 26 methods compile in isolation, while their twelve projected Java overload groups have erased signature conflicts; exact collective public API representation remains blocked",
        "groups": joined,
    }
    OUTPUT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: 12 erasure groups; all 26 colliding identities individually compile, so collective mapping remains unresolved")


if __name__ == "__main__":
    main()
