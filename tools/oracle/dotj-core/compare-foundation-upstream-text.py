"""Bounded token-overlap screen against four pinned upstream CoreLib files."""

import hashlib
import json
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
ARTIFACT = EVIDENCE / "foundation-product-candidate-v1.json"
OUTPUT = EVIDENCE / "foundation-upstream-text-comparison-v1.json"
COMMIT = "4271d88e0aebf3d04f188f1334c2220d80555ef6"
BASE = "https://raw.githubusercontent.com/dotnet/runtime/" + COMMIT + "/"
UPSTREAM = "src/libraries/System.Private.CoreLib/src/System/"
PRODUCT = "dotj-core/dotj-core-public/src/main/java/System/"
NAMES = ("Type", "Exception", "Int32", "IDisposable")
SHINGLE_SIZE = 12


def identifiers(data):
    return re.findall(r"[A-Za-z_][A-Za-z_0-9]*", data.decode("utf-8"))


def shingles(tokens):
    return {tuple(tokens[index:index + SHINGLE_SIZE])
            for index in range(len(tokens) - SHINGLE_SIZE + 1)}


def main():
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    current_hashes = {item["path"]: item["sha256"] for item in artifact["productSources"]}
    rows = []
    for name in NAMES:
        product_path = PRODUCT + name + ".java"
        upstream_path = UPSTREAM + name + ".cs"
        product_bytes = (ROOT / product_path).read_bytes()
        assert hashlib.sha256(product_bytes).hexdigest() == current_hashes[product_path]
        with urllib.request.urlopen(BASE + upstream_path, timeout=30) as response:
            upstream_bytes = response.read()
        product_tokens = identifiers(product_bytes)
        upstream_tokens = identifiers(upstream_bytes)
        shared = shingles(product_tokens) & shingles(upstream_tokens)
        rows.append({
            "productPath": product_path,
            "productSha256": current_hashes[product_path],
            "upstreamPath": upstream_path,
            "upstreamUrl": BASE + upstream_path,
            "upstreamSha256": hashlib.sha256(upstream_bytes).hexdigest(),
            "productIdentifierCount": len(product_tokens),
            "upstreamIdentifierCount": len(upstream_tokens),
            "sharedIdentifierShinglesOfLength12": len(shared),
        })
    record = {
        "schemaVersion": 1,
        "scope": "Four name-matched pairs among 30 candidate Java sources; screening only",
        "upstreamCommit": COMMIT,
        "artifactEvidence": ARTIFACT.name,
        "jarSha256": artifact["jarSha256"],
        "method": "Case-sensitive C#/Java identifier tokenization; count shared contiguous runs of 12 identifiers",
        "rows": rows,
        "interpretationLimit": "This screen misses transformed or translated source, ignores other upstream files and dependencies, and cannot determine authorship, notice applicability, or release rights.",
        "releaseQualification": "E01_OPEN",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("PASS bounded text comparison for four pinned upstream and product source pairs")


if __name__ == "__main__":
    main()
