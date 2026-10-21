"""Bounded token-overlap screen for the candidate source inventory."""

from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import re
from urllib.error import HTTPError
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
ARTIFACT = EVIDENCE / "foundation-product-candidate-v1.json"
OUTPUT = EVIDENCE / "foundation-upstream-text-comparison-v1.json"
COMMIT = "4271d88e0aebf3d04f188f1334c2220d80555ef6"
BASE = "https://raw.githubusercontent.com/dotnet/runtime/" + COMMIT + "/"
UPSTREAM = "src/libraries/System.Private.CoreLib/src/"
PRODUCT = "dotj-core/dotj-core-public/src/main/java/"
SHINGLE_SIZE = 12


def identifiers(data):
    return re.findall(r"[A-Za-z_][A-Za-z_0-9]*", data.decode("utf-8"))


def shingles(tokens):
    return {tuple(tokens[index:index + SHINGLE_SIZE])
            for index in range(len(tokens) - SHINGLE_SIZE + 1)}


def compare(item):
    product_path, expected_hash = item
    relative = product_path.removeprefix(PRODUCT).removesuffix(".java")
    upstream_path = UPSTREAM + relative + ".cs"
    product_bytes = (ROOT / product_path).read_bytes()
    assert hashlib.sha256(product_bytes).hexdigest() == expected_hash
    row = {
        "productPath": product_path,
        "productSha256": expected_hash,
        "upstreamPath": upstream_path,
        "upstreamUrl": BASE + upstream_path,
    }
    try:
        with urllib.request.urlopen(BASE + upstream_path, timeout=30) as response:
            upstream_bytes = response.read()
    except HTTPError as error:
        if error.code != 404:
            raise
        row["directNameMatchedUpstreamFile"] = "NOT_FOUND_AT_PINNED_PATH"
        return row
    product_tokens = identifiers(product_bytes)
    upstream_tokens = identifiers(upstream_bytes)
    shared = shingles(product_tokens) & shingles(upstream_tokens)
    row.update({
        "directNameMatchedUpstreamFile": "FOUND",
        "upstreamSha256": hashlib.sha256(upstream_bytes).hexdigest(),
        "productIdentifierCount": len(product_tokens),
        "upstreamIdentifierCount": len(upstream_tokens),
        "sharedIdentifierShinglesOfLength12": len(shared),
    })
    return row


def main():
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    current_hashes = {item["path"]: item["sha256"] for item in artifact["productSources"]}
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = sorted(pool.map(compare, current_hashes.items()), key=lambda row: row["productPath"])
    assert len(rows) == len(current_hashes) == 50
    record = {
        "schemaVersion": 1,
        "scope": "All 50 candidate Java paths; direct name-matched pinned upstream paths only",
        "upstreamCommit": COMMIT,
        "artifactEvidence": ARTIFACT.name,
        "jarSha256": artifact["jarSha256"],
        "method": "Case-sensitive C#/Java identifier tokenization; count shared contiguous runs of 12 identifiers",
        "rows": rows,
        "interpretationLimit": "A missing direct path does not mean no upstream analogue. This screen misses transformed or translated source, other upstream files and dependencies, and cannot determine authorship, notice applicability, or release rights.",
        "releaseQualification": "E01_OPEN",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    found = sum(row["directNameMatchedUpstreamFile"] == "FOUND" for row in rows)
    print(f"PASS bounded text comparison for {found} pinned direct-name upstream files among 50 product sources")


if __name__ == "__main__":
    main()
