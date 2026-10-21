"""Rebuild and verify the bounded public foundation candidate and E01 inputs."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ORACLE = Path(__file__).resolve().parent
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
OUTPUT = EVIDENCE / "foundation-public-candidate-gate-v1.json"
CHECKS = (
    "capture-foundation-public-metadata.py",
    "build-idisposable-product.py",
    "build-system-type-candidate.py",
    "build-foundation-product-candidate.py",
    "verify-idisposable-file-map.py",
    "verify-idisposable-distribution.py",
    "audit-foundation-public-candidate.py",
    "build-foundation-semantic-surface.py",
    "lower-selected-typeof.py",
    "lower-selected-throw.py",
    "verify-foundation-distribution.py",
    "audit-foundation-rights-inputs.py",
    "audit-foundation-source-provenance.py",
    "compare-foundation-upstream-text.py",
    "build-foundation-notice-review-queue.py",
    "audit-throw-site-upstream-adjacency.py",
    "build-foundation-e01-review-packet.py",
)


def read(name):
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    for name in CHECKS:
        result = subprocess.run([sys.executable, str(ORACLE / name)], cwd=ROOT,
                                capture_output=True, text=True)
        if result.returncode or "PASS" not in result.stdout:
            raise RuntimeError(f"{name} failed ({result.returncode})\n"
                               f"{result.stdout}{result.stderr}")
        print(result.stdout.strip(), flush=True)

    artifact = read("foundation-product-candidate-v1.json")
    mapping = read("foundation-file-notice-map-v1.json")
    queue = read("foundation-notice-review-queue-v1.json")
    packet = read("foundation-e01-review-packet-v1.json")
    jar_hash = artifact["jarSha256"]
    assert jar_hash == mapping["jarSha256"] == queue["jarSha256"]
    assert jar_hash == packet["candidateJarSha256"]
    assert sha256(ROOT / artifact["jarPath"]) == jar_hash
    assert len(artifact["productSources"]) == queue["sourceCount"] == 47
    assert len(artifact["jarEntries"]) == 59
    assert packet["productLicense"]["identifier"] == "MIT"
    assert packet["qualification"] == "E01_OPEN; NOT_RELEASE_QUALIFIED"
    assert len(packet["openDecisions"]) == 3
    assert all(item["status"] == "OPEN" for item in packet["openDecisions"])

    evidence_files = (
        "foundation-selected-metadata-v10.0.12.json",
        "foundation-product-candidate-v1.json",
        "foundation-rights-inputs-v1.json",
        "foundation-notice-review-queue-v1.json",
        "throw-site-upstream-adjacency-v1.json",
        "foundation-e01-review-packet-v1.json",
    )
    record = {
        "schemaVersion": 1,
        "scope": "Current dotj-core public foundation candidate and bounded E01 inputs",
        "checks": list(CHECKS),
        "candidateJarSha256": jar_hash,
        "productSourceCount": 47,
        "jarEntryCount": 59,
        "evidenceSha256": {
            name: sha256(EVIDENCE / name) for name in evidence_files
        },
        "productLicense": "MIT",
        "openE01DecisionCount": 3,
        "status": "BOUNDED_CANDIDATE_PASS; E01/E02/E03/N01_PUBLIC_QUALIFICATION_OPEN",
        "releaseQualified": False,
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("PASS public foundation candidate gate: 17 checks, 47 sources, MIT, E01 open")


if __name__ == "__main__":
    main()
