"""Verify the combined foundation candidate artifact and its source/notice map."""

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
ARTIFACT = EVIDENCE / "foundation-product-candidate-v1.json"
MAPPING = EVIDENCE / "foundation-file-notice-map-v1.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    jar = ROOT / artifact["jarPath"]
    assert mapping["artifactEvidence"] == ARTIFACT.name
    assert mapping["jarSha256"] == artifact["jarSha256"] == sha256(jar)
    sources = {item["path"]: item["sha256"] for item in artifact["productSources"]}
    assert set(mapping["sourceToClasses"]) == set(sources)
    for path, digest in sources.items():
        assert sha256(ROOT / path) == digest
    mapped_classes = [entry for entries in mapping["sourceToClasses"].values() for entry in entries]
    assert len(mapped_classes) == len(set(mapped_classes))
    assert sorted(mapped_classes) == sorted(artifact["classSha256"])
    with zipfile.ZipFile(jar) as archive:
        assert archive.namelist() == artifact["jarEntries"]
        assert archive.namelist() == [mapping["manifestEntry"], *sorted(mapped_classes)]
        for entry, digest in artifact["classSha256"].items():
            assert hashlib.sha256(archive.read(entry)).hexdigest() == digest
        notice_entries = [name for name in archive.namelist()
                          if "LICENSE" in name.upper() or "NOTICE" in name.upper()]
        assert notice_entries == mapping["jarNoticeEntries"] == []
    for reference in mapping["upstreamReferenceEvidenceExcludedFromJar"]:
        assert sha256(ROOT / reference["path"]) == reference["sha256"]
    dependencies = subprocess.run(["jdeps", "-summary", str(jar)], cwd=ROOT,
                                  capture_output=True, text=True, check=True).stdout
    observed = sorted({line.split("->", 1)[1].strip() for line in dependencies.splitlines() if "->" in line})
    assert observed == mapping["observedJdkModuleDependencies"] == ["java.base"]
    assert len(mapping["decisionInputs"]) == 3
    assert mapping["status"].endswith("E01_RELEASE_REVIEW_OPEN")
    print("PASS foundation candidate source, archive, notice-input and JDK dependency inventory")


if __name__ == "__main__":
    main()
