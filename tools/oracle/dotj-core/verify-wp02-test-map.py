"""Validate selected upstream cancellation test IDs against the pinned source."""

import hashlib
import json
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence/wp02-upstream-test-map-v10.0.12.json"


def verify(source_root):
    mapping = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    source = source_root / mapping["sourcePath"]
    project = source_root / mapping["projectPath"]
    assert hashlib.sha256(source.read_bytes()).hexdigest() == mapping["sourceSha256"]
    assert hashlib.sha256(project.read_bytes()).hexdigest() == mapping["projectSha256"]
    text = source.read_text(encoding="utf-8-sig")
    names = [case["upstreamMethod"] for case in mapping["cases"]]
    assert len(names) == 10 and len(set(names)) == 10
    assert all(f" {name}(" in text for name in names)
    assert all(case["oracleCase"] and case["mapping"] for case in mapping["cases"])
    return names


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=Path("R:/"))
    print(f"PASS {len(verify(parser.parse_args().source_root))} pinned WP-02 upstream method IDs")
