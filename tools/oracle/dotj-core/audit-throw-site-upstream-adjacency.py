"""Bounded lexical comparison for the candidate helper without a direct C# path."""

import hashlib
import json
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
OUTPUT = EVIDENCE / "throw-site-upstream-adjacency-v1.json"
SOURCE = "dotj-core/dotj-core-public/src/main/java/org/dotj/internal/throwing/ThrowSite.java"
PINNED_PATHS = (
    "src/libraries/System.Private.CoreLib/src/System/ThrowHelper.cs",
    "src/libraries/System.Private.CoreLib/src/System/Exception.cs",
)
PINNED_SHA256 = (
    "5c21b9149ef32e1f68396d060e6fc70311324c9829ed40328c33f6d5f859a757",
    "3f44c5b9eb6851301091fc65ce6dd6671e1a750f8a7f120837bc09021ecf12ab",
)
SHINGLE_SIZE = 12


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def shingles(data):
    tokens = re.findall(r"[A-Za-z_][A-Za-z_0-9]*", data.decode("utf-8"))
    return {tuple(tokens[index:index + SHINGLE_SIZE])
            for index in range(len(tokens) - SHINGLE_SIZE + 1)}


def main():
    queue = json.loads((EVIDENCE / "foundation-notice-review-queue-v1.json").read_text(
        encoding="utf-8"))
    comparison = json.loads((EVIDENCE / "foundation-upstream-text-comparison-v1.json").read_text(
        encoding="utf-8"))
    assert queue["jarSha256"] == comparison["jarSha256"]
    source_row = next(row for row in queue["rows"] if row["productPath"] == SOURCE)
    assert source_row["directNameMatchedUpstreamFile"] == "NOT_FOUND_AT_PINNED_PATH"
    source = (ROOT / SOURCE).read_bytes()
    assert sha256(source) == source_row["productSha256"]
    commit = comparison["upstreamCommit"]
    base = "https://raw.githubusercontent.com/dotnet/runtime/" + commit + "/"
    product_shingles = shingles(source)
    rows = []
    for path, expected_hash in zip(PINNED_PATHS, PINNED_SHA256, strict=True):
        url = base + path
        with urllib.request.urlopen(url, timeout=30) as response:
            upstream = response.read()
        assert sha256(upstream) == expected_hash
        rows.append({
            "upstreamPath": path,
            "upstreamUrl": url,
            "upstreamSha256": sha256(upstream),
            "sharedIdentifierShinglesOfLength12": len(product_shingles & shingles(upstream)),
        })
    record = {
        "schemaVersion": 1,
        "scope": "ThrowSite.java versus two selected pinned CoreLib exception/throw helpers",
        "jarSha256": queue["jarSha256"],
        "upstreamCommit": commit,
        "productPath": SOURCE,
        "productSha256": sha256(source),
        "rows": rows,
        "interpretationLimit": "These two adjacent files are not an exhaustive source search. Lexical overlap cannot determine derivation, authorship, notice applicability or release rights.",
        "noticeApplicabilityDecision": "REVIEW_REQUIRED",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("PASS ThrowSite bounded upstream adjacency: " + ", ".join(
        f"{row['upstreamPath'].rsplit('/', 1)[-1]}={row['sharedIdentifierShinglesOfLength12']}"
        for row in rows))


if __name__ == "__main__":
    main()
