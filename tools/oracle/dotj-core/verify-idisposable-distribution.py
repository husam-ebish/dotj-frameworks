"""Verify the recorded IDisposable product candidate distribution inventory."""

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
NOTICE_MAP = EVIDENCE / "idisposable-file-notice-map-v10.0.12.json"
PRODUCT = EVIDENCE / "idisposable-product-v1.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    mapping = json.loads(NOTICE_MAP.read_text(encoding="utf-8"))
    product = json.loads(PRODUCT.read_text(encoding="utf-8"))
    source = mapping["productInputs"][0]
    output = mapping["productOutput"]

    assert source["path"] == product["sourcePath"]
    assert source["sha256"] == product["sourceSha256"] == sha256(ROOT / source["path"])
    assert output["sha256"] == product["jarSha256"] == sha256(ROOT / output["path"])
    assert output["entries"] == product["jarEntries"]
    with zipfile.ZipFile(ROOT / output["path"]) as archive:
        assert archive.namelist() == output["entries"]
        assert hashlib.sha256(archive.read("System/IDisposable.class")).hexdigest() == product["classSha256"]
    assert output["distributionStatus"] == "BUILT_CANDIDATE_NOT_RELEASED"
    assert mapping["releaseQualification"].startswith("OPEN:")
    print("PASS IDisposable product candidate source, JAR hash, entries and class hash")


if __name__ == "__main__":
    main()
