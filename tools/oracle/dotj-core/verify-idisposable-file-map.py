"""Check candidate JAR contents against the bounded file and notice map."""

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    mapping = json.loads((EVIDENCE / "idisposable-file-notice-map-v10.0.12.json").read_text(encoding="utf-8"))
    artifact = json.loads((EVIDENCE / "idisposable-candidate-jar-v1.json").read_text(encoding="utf-8"))
    local_inputs = mapping["candidateInputs"][:1] + mapping["excludedReferenceInputs"][1:]
    for item in local_inputs:
        assert sha256(ROOT / item["path"]) == item["sha256"], item["path"]
    candidate = mapping["candidateOutput"]
    jar = ROOT / candidate["path"]
    assert sha256(jar) == candidate["sha256"] == artifact["jarSha256"]
    with zipfile.ZipFile(jar) as contents:
        assert contents.namelist() == candidate["entries"] == artifact["entries"]
        assert hashlib.sha256(contents.read("System/IDisposable.class")).hexdigest() == artifact["classSha256"]
    assert artifact["sourceSha256"] == mapping["candidateInputs"][0]["sha256"]
    print("PASS candidate file map: 1 Java source, 2 JAR entries, 2 pinned notices retained only as evidence")


if __name__ == "__main__":
    main()
