"""Inventory package rights declarations from the pinned generator restore graph.

Usage: py inventory.py <restore-graph-manifest> <packages-root>
The output directory is this script's directory. This is evidence collection, not
a legal interpretation or redistribution clearance.
"""

import hashlib
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def child_text(parent: ET.Element, name: str) -> str | None:
    child = next((item for item in parent if item.tag.rsplit("}", 1)[-1] == name), None)
    return child.text.strip() if child is not None and child.text else None


def child_element(parent: ET.Element, name: str) -> ET.Element | None:
    return next((item for item in parent if item.tag.rsplit("}", 1)[-1] == name), None)


def main() -> None:
    graph_path = Path(sys.argv[1])
    package_root = Path(sys.argv[2])
    output = Path(__file__).parent
    nuspec_output = output / "nuspecs"
    nuspec_output.mkdir(parents=True, exist_ok=True)
    notice_output = output / "notices"
    notice_output.mkdir(parents=True, exist_ok=True)
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    records = []
    name_pattern = re.compile(r"license|licence|notice|third.?party|copyright|credits", re.I)

    for identity in graph["restore"]["resolvedPackages"]:
        package_id, version = identity.split("/", 1)
        folder = package_root / package_id.lower() / version.lower()
        nuspec = folder / (package_id.lower() + ".nuspec")
        if not nuspec.is_file():
            raise FileNotFoundError(nuspec)
        metadata = child_element(ET.parse(nuspec).getroot(), "metadata")
        if metadata is None:
            raise ValueError(f"Missing nuspec metadata: {identity}")
        license_element = child_element(metadata, "license")
        license_declaration = None
        if license_element is not None:
            license_declaration = {
                "type": license_element.attrib.get("type"),
                "value": (license_element.text or "").strip(),
            }

        notice_files = []
        for path in folder.rglob("*"):
            if path.is_file() and name_pattern.search(path.name):
                relative = path.relative_to(folder)
                snapshot = notice_output / f"{package_id.lower()}.{version.lower()}" / relative
                snapshot.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, snapshot)
                notice_files.append({
                    "path": relative.as_posix(),
                    "snapshot": snapshot.relative_to(output).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                })
        notice_files.sort(key=lambda item: item["path"].lower())

        snapshot = nuspec_output / f"{package_id.lower()}.{version.lower()}.nuspec.raw"
        shutil.copyfile(nuspec, snapshot)
        records.append({
            "identity": identity,
            "nuspecSnapshot": snapshot.relative_to(output).as_posix(),
            "nuspecSha256": sha256(nuspec),
            "declaredLicense": license_declaration,
            "licenseUrl": child_text(metadata, "licenseUrl"),
            "copyright": child_text(metadata, "copyright"),
            "authors": child_text(metadata, "authors"),
            "noticeLikeFiles": notice_files,
        })

    manifest = {
        "schemaVersion": 1,
        "recordedDate": "2026-10-19",
        "scope": "dotj-core E01, 20 resolved packages in the pinned netstandard2.0 generator restore graph",
        "sourceGraph": "../restore-graph-v10.0.12-netstandard2.0/manifest.json",
        "status": "DECLARATION_AND_FILENAME_INVENTORY_ONLY; RIGHTS_CLEARANCE_OPEN",
        "method": "Parse cached package nuspec metadata; snapshot each nuspec; hash extracted files whose names contain license, licence, notice, third-party, copyright or credits.",
        "packageCount": len(records),
        "withLicenseDeclarationCount": sum(bool(r["declaredLicense"]) for r in records),
        "withoutLicenseDeclaration": [r["identity"] for r in records if not r["declaredLicense"]],
        "withNoticeLikeFilesCount": sum(bool(r["noticeLikeFiles"]) for r in records),
        "withoutNoticeLikeFiles": [r["identity"] for r in records if not r["noticeLikeFiles"]],
        "packages": records,
        "limitations": [
            "A nuspec expression or license URL is a package declaration, not independent verification of every contained file or right.",
            "Filename matching may miss notices in other files, bundled assets or external references.",
            "This inventory does not determine which build-time packages or generated outputs will be redistributed in dotj artifacts.",
            "No legal clearance or product release eligibility is claimed.",
        ],
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "packages": len(records),
        "withLicenseDeclaration": sum(bool(r["declaredLicense"]) for r in records),
        "withNoticeLikeFiles": sum(bool(r["noticeLikeFiles"]) for r in records),
        "withoutLicenseDeclaration": [r["identity"] for r in records if not r["declaredLicense"]],
    }, indent=2))


if __name__ == "__main__":
    main()
