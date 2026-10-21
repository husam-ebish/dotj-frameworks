"""Assemble a bounded E01 decision packet for the current foundation candidate."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
OUTPUT = EVIDENCE / "foundation-e01-review-packet-v1.json"


def read(name):
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def main():
    baseline = read("baseline-lock.json")
    artifact = read("foundation-product-candidate-v1.json")
    rights = read("foundation-rights-inputs-v1.json")
    queue = read("foundation-notice-review-queue-v1.json")
    adjacency = read("throw-site-upstream-adjacency-v1.json")
    mapping = read("foundation-file-notice-map-v1.json")
    jar_hash = artifact["jarSha256"]
    assert all(record["jarSha256"] == jar_hash
               for record in (rights, queue, adjacency, mapping))
    assert baseline["status"] == "PARTIAL"
    assert rights["selectedProductLicense"] == mapping["productLicense"] == "MIT"
    assert artifact["licensePath"] == mapping["productLicensePath"] == "dotj-core/LICENSE"
    assert artifact["licenseEntry"] == mapping["productLicenseEntry"] == "META-INF/LICENSE"
    assert rights["jarNoticeEntries"] == ["META-INF/LICENSE"]
    assert queue["sourceCount"] == rights["productSourceCount"] == 34
    assert queue["directNameMatchedCount"] == 33
    assert queue["directNameMissingCount"] == 1
    assert all(row["mitSpdxHeaderObserved"] and
               row["noticeApplicabilityDecision"] == "REVIEW_REQUIRED"
               for row in queue["rows"])
    assert len(adjacency["rows"]) == 2
    assert adjacency["noticeApplicabilityDecision"] == "REVIEW_REQUIRED"
    assert baseline["referenceCandidate"]["tagCommit"] == queue["upstreamCommit"]

    record = {
        "schemaVersion": 1,
        "scope": "Current built dotj-core foundation candidate only; no release decision",
        "candidateJarSha256": jar_hash,
        "candidateJarEvidence": "foundation-product-candidate-v1.json",
        "referenceProfile": {
            "release": baseline["referenceCandidate"]["release"],
            "tagCommit": baseline["referenceCandidate"]["tagCommit"],
            "baselineStatus": baseline["status"],
        },
        "jdkToolchain": {
            "distribution": baseline["localJavaToolchain"]["distribution"],
            "version": baseline["localJavaToolchain"]["version"],
            "binaryHashesSha256": baseline["localJavaToolchain"]["binaryHashesSha256"],
        },
        "productLicense": {
            "identifier": "MIT",
            "sourceFile": rights["licensePath"],
            "sourceSha256": rights["licenseSha256"],
            "jarEntry": artifact["licenseEntry"],
            "javaSourcesWithIdentifier": 31,
        },
        "boundedSourceScreen": {
            "productSources": 31,
            "directNameMatchedPinnedFiles": queue["directNameMatchedCount"],
            "missingDirectNamePath": queue["directNameMissingCount"],
            "throwSiteAdjacentFilesCompared": len(adjacency["rows"]),
            "reviewQueueEvidence": "foundation-notice-review-queue-v1.json",
            "throwSiteEvidence": "throw-site-upstream-adjacency-v1.json",
        },
        "upstreamReferenceNoticesNotInJar":
            rights["upstreamReferenceNoticePathsExcludedFromJar"],
        "openDecisions": [
            {
                "id": "SOURCE_AND_NOTICE_APPLICABILITY",
                "status": "OPEN",
                "evidence": "foundation-notice-review-queue-v1.json",
                "question": "Which pinned upstream or third-party notices, if any, apply to the 31 Java source files and compiled classes?",
            },
            {
                "id": "REFERENCE_AND_DEPENDENCY_RIGHTS",
                "status": "OPEN",
                "evidence": "baseline-lock.json",
                "question": "Are the selected reference, generated-output and dependency rights sufficient for the intended distribution profile?",
            },
            {
                "id": "RELEASE_REVIEW",
                "status": "OPEN",
                "evidence": "foundation-rights-inputs-v1.json",
                "question": "Has the required repository licensing review approved this exact candidate and its distribution notices?",
            },
        ],
        "qualification": "E01_OPEN; NOT_RELEASE_QUALIFIED",
        "limitation": "License labels, archive contents, local Git history and bounded source comparisons are technical inputs, not a rights determination.",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("PASS foundation E01 packet: MIT candidate and three explicit open decisions")


if __name__ == "__main__":
    main()
