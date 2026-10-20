"""Verify and repair the immutable .NET 10.0.12 source extraction."""

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence/source-archive-v10.0.12.json"


def native_path(path: Path) -> str:
    absolute = str(path)
    if not path.is_absolute():
        raise ValueError("An absolute destination path is required")
    return "\\\\?\\" + absolute if os.name == "nt" else absolute


def verify_archive(path: Path, expected: dict) -> None:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    if path.stat().st_size != expected["bytes"] or digest.hexdigest() != expected["sha256"]:
        raise ValueError("Pinned source archive byte length or SHA-256 mismatch")


def restore(archive: Path, destination: Path) -> dict:
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    verify_archive(archive, evidence["archive"])
    commit = evidence["sourceCommit"]
    root_name = "runtime-" + commit
    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    expected_files = 0
    repaired = 0
    with ZipFile(archive) as bundle:
        for member in bundle.infolist():
            if member.is_dir():
                continue
            parts = member.filename.split("/")
            if parts[0] != root_name or any(part in ("", ".", "..") for part in parts):
                raise ValueError("Unsafe or unexpected archive member: " + repr(member.filename))
            expected_files += 1
            output = native_path(destination.joinpath(*parts))
            if os.path.isfile(output):
                continue
            os.makedirs(os.path.dirname(output), exist_ok=True)
            with bundle.open(member) as source, open(output, "wb") as target:
                shutil.copyfileobj(source, target)
            if not os.path.isfile(output):
                raise OSError("Source file was not written: " + repr(member.filename))
            repaired += 1
    if expected_files != evidence["archive"]["fileCount"]:
        raise ValueError("Archive file count mismatch")
    return {"sourceCommit": commit, "archiveSha256": evidence["archive"]["sha256"],
            "archiveFiles": expected_files, "filesRepairedThisRun": repaired,
            "sourceRoot": str(destination / root_name)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(restore(args.archive, args.destination), indent=2))
