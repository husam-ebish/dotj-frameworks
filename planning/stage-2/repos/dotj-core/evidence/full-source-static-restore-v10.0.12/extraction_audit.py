"""Audit and repair the pinned runtime ZIP extraction on Windows.

Usage: py extraction_audit.py <archive.zip> <extraction-root>
The extraction root is the directory containing the archive's runtime-* folder.
"""

import json
import os
import shutil
import sys
import zipfile
from pathlib import Path, PurePosixPath


def extended(path: Path) -> str:
    return "\\\\?\\" + str(path.resolve())


def main() -> None:
    archive = Path(sys.argv[1])
    root = Path(sys.argv[2]).resolve()
    failures = []
    repaired = 0
    with zipfile.ZipFile(archive) as zipped:
        members = [item for item in zipped.infolist() if not item.is_dir()]
        for item in members:
            name = PurePosixPath(item.filename)
            if name.is_absolute() or ".." in name.parts:
                raise ValueError(f"Unsafe archive path: {item.filename}")
            target = root.joinpath(*name.parts)
            destination = extended(target)
            if os.path.isfile(destination):
                continue
            try:
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                with zipped.open(item) as source, open(destination, "wb") as sink:
                    shutil.copyfileobj(source, sink)
                repaired += 1
            except (OSError, ValueError) as error:
                failures.append({"path": item.filename, "error": str(error)})

        missing = []
        for item in members:
            target = root.joinpath(*PurePosixPath(item.filename).parts)
            if not os.path.isfile(extended(target)):
                missing.append(item.filename)

    report = {
        "archiveFileCount": len(members),
        "repairedFileCount": repaired,
        "remainingMissingCount": len(missing),
        "remainingMissing": missing,
        "repairFailures": failures,
    }
    output = Path(__file__).parent / "extraction-audit.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("archiveFileCount", "repairedFileCount", "remainingMissingCount")}, indent=2))


if __name__ == "__main__":
    main()
