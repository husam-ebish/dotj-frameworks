"""Check the seven selected WP-02 source and CoreLib artifact snapshots."""

import hashlib
import json
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
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


def verify(source_root):
    records = []
    for key in KEYS:
        provenance = json.loads((EVIDENCE / f"{key}-provenance.json").read_text(encoding="utf-8"))
        snapshot_path = EVIDENCE / provenance["snapshotPath"]
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        source_path = source_root / provenance["sourcePath"]
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=Path("R:/"))
    result = verify(parser.parse_args().source_root)
    print(f"PASS {len(result)} selected WP-02 source/artifact shape pairs")
