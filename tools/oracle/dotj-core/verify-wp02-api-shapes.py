"""Check the seven selected WP-02 source and CoreLib artifact snapshots."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path("R:/")
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence/wp02-api-shapes-v10.0.12"
KEYS = (
    "cancellation-token",
    "cancellation-source",
    "cancellation-registration",
    "task",
    "task-generic",
    "task-completion-source",
    "task-completion-source-generic",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    records = []
    for key in KEYS:
        provenance = json.loads((EVIDENCE / f"{key}-provenance.json").read_text(encoding="utf-8"))
        snapshot_path = EVIDENCE / provenance["snapshotPath"]
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        source_path = SOURCE / provenance["sourcePath"]
        assert source_path.is_file()
        assert provenance["sourceDeclarationAnchor"] in source_path.read_text(encoding="utf-8-sig")
        assert digest(source_path) == provenance["sourceSha256"]
        assert digest(snapshot_path) == provenance["snapshotSha256"]
        assert snapshot["assemblySha256"] == provenance["artifactSha256"]
        assert len(snapshot["type"]["methods"]) == provenance["publicDeclaredMethodCount"]
        assert len(snapshot["type"]["properties"]) == provenance["publicDeclaredPropertyCount"]
        records.append({"key": key, "fullName": snapshot["type"]["fullName"], "sourceSha256": provenance["sourceSha256"], "snapshotSha256": provenance["snapshotSha256"]})
    return records


if __name__ == "__main__":
    result = verify()
    print(f"PASS {len(result)} selected WP-02 source/artifact shape pairs")
