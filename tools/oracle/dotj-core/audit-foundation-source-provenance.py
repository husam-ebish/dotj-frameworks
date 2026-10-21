"""Record local Git introduction evidence for the product Java source inventory."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
ARTIFACT = EVIDENCE / "foundation-product-candidate-v1.json"
RIGHTS = EVIDENCE / "foundation-rights-inputs-v1.json"
OUTPUT = EVIDENCE / "foundation-source-provenance-v1.json"


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def main():
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    rights = json.loads(RIGHTS.read_text(encoding="utf-8"))
    assert rights["jarSha256"] == artifact["jarSha256"]
    source_hashes = {item["path"]: item["sha256"] for item in artifact["productSources"]}
    assert set(source_hashes) == {item["path"] for item in rights["productSources"]}
    rows = []
    for path in sorted(source_hashes):
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == source_hashes[path]
        introductions = git("log", "--diff-filter=A", "--format=%H", "--", path).splitlines()
        assert len(introductions) == 1, (path, introductions)
        commit = introductions[0]
        introduced_paths = git("show", "--format=", "--name-only", commit, "--", path).splitlines()
        assert path in introduced_paths
        rows.append({
            "path": path,
            "sha256": source_hashes[path],
            "localIntroductionCommit": commit,
            "introductionEvidence": "Git add event in this repository; not an authorship or originality determination",
        })
    assert len(rows) == rights["productSourceCount"] == 55
    assert all(item["headerHasSpdxIdentifier"] and
               not item["headerHasCopyrightNotice"] and
               not item["headerNamesDotNetFoundation"]
               for item in rights["productSources"])
    record = {
        "schemaVersion": 1,
        "scope": "55 hashed Java product sources in the built foundation candidate JAR",
        "artifactEvidence": ARTIFACT.name,
        "jarSha256": artifact["jarSha256"],
        "sourceCount": len(rows),
        "sources": rows,
        "headerObservation": "MIT SPDX identifier in first 30 lines of all 55 current Java files; no inline copyright or .NET Foundation text",
        "upstreamNoticeApplicability": "UNRESOLVED: local Git introductions and source headers do not prove independent authorship or exclude embedded upstream material",
        "releaseQualification": "E01_OPEN",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"PASS local Git introductions recorded for {len(rows)} candidate Java sources")


if __name__ == "__main__":
    main()
