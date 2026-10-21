"""Join candidate source provenance with bounded pinned-upstream comparisons.

This creates review inputs. It cannot determine authorship or notice obligations.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
OUTPUT = EVIDENCE / "foundation-notice-review-queue-v1.json"


def read(name):
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def indexed(rows, key):
    result = {row[key]: row for row in rows}
    assert len(result) == len(rows)
    return result


def main():
    artifact = read("foundation-product-candidate-v1.json")
    rights = read("foundation-rights-inputs-v1.json")
    provenance = read("foundation-source-provenance-v1.json")
    comparison = read("foundation-upstream-text-comparison-v1.json")
    mapping = read("foundation-file-notice-map-v1.json")
    jar_hash = artifact["jarSha256"]
    assert all(record["jarSha256"] == jar_hash
               for record in (rights, provenance, comparison, mapping))
    product = indexed(artifact["productSources"], "path")
    headers = indexed(rights["productSources"], "path")
    introductions = indexed(provenance["sources"], "path")
    upstream = indexed(comparison["rows"], "productPath")
    assert set(product) == set(headers) == set(introductions) == set(upstream)
    assert set(product) == set(mapping["sourceToClasses"])
    assert len(product) == 38

    rows = []
    for path in sorted(product):
        source_hash = product[path]["sha256"]
        assert headers[path]["sha256"] == introductions[path]["sha256"] == source_hash
        assert upstream[path]["productSha256"] == source_hash
        assert headers[path]["headerHasSpdxIdentifier"]
        assert not headers[path]["headerNamesDotNetFoundation"]
        direct_match = upstream[path]["directNameMatchedUpstreamFile"]
        assert direct_match in ("FOUND", "NOT_FOUND_AT_PINNED_PATH")
        if direct_match == "FOUND":
            assert upstream[path]["sharedIdentifierShinglesOfLength12"] == 0
        rows.append({
            "productPath": path,
            "productSha256": source_hash,
            "classEntries": mapping["sourceToClasses"][path],
            "mitSpdxHeaderObserved": True,
            "localIntroductionCommit": introductions[path]["localIntroductionCommit"],
            "directNameMatchedUpstreamFile": direct_match,
            "upstreamPath": upstream[path]["upstreamPath"],
            "upstreamSha256": upstream[path].get("upstreamSha256"),
            "sharedIdentifierShinglesOfLength12": upstream[path].get(
                "sharedIdentifierShinglesOfLength12"),
            "noticeApplicabilityDecision": "REVIEW_REQUIRED",
            "supplementalAdjacencyEvidence": "throw-site-upstream-adjacency-v1.json"
            if path.endswith("/org/dotj/internal/throwing/ThrowSite.java") else None,
        })

    found = sum(row["directNameMatchedUpstreamFile"] == "FOUND" for row in rows)
    record = {
        "schemaVersion": 1,
        "scope": "Built foundation candidate JAR product sources; bounded direct-name comparison only",
        "jarSha256": jar_hash,
        "upstreamCommit": comparison["upstreamCommit"],
        "productLicense": "MIT",
        "sourceCount": len(rows),
        "directNameMatchedCount": found,
        "directNameMissingCount": len(rows) - found,
        "rows": rows,
        "upstreamReferenceNoticePathsExcludedFromJar": [
            item["path"] for item in mapping["upstreamReferenceEvidenceExcludedFromJar"]
        ],
        "limitation": "Git introduction, SPDX labels and zero shared 12-identifier runs do not determine authorship, translated-source overlap or third-party notice applicability.",
        "releaseQualification": "E01_REVIEW_OPEN",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"PASS foundation notice review queue: {len(rows)} sources, "
          f"{found} direct-name upstream files, {len(rows) - found} missing direct path")


if __name__ == "__main__":
    main()
