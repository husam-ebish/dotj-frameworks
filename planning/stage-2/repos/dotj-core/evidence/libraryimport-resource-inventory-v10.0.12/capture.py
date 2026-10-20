"""Inventory pinned non-C# generator inputs without copying source into evidence."""

import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


COMMIT = "4271d88e0aebf3d04f188f1334c2220d80555ef6"
ARCHIVE_SHA256 = "ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115"
OUTPUT_SHA256 = "094c3ccc4a4de9fe3a146af0964b784ca8c04542f32729b86786e0d644ae248b"
PREFIX = f"runtime-{COMMIT}/src/libraries/System.Runtime.InteropServices/gen/"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()

    archive_bytes = args.archive.read_bytes()
    assert len(archive_bytes) == 136239366
    assert digest(archive_bytes) == ARCHIVE_SHA256

    with zipfile.ZipFile(args.archive) as archive:
        names = sorted(
            name for name in archive.namelist()
            if name.startswith(PREFIX) and not name.endswith("/")
        )
        entries = []
        for name in names:
            relative = name.removeprefix(PREFIX)
            if relative.lower().endswith(".cs"):
                continue
            data = archive.read(name)
            entries.append({"path": relative, "bytes": len(data), "sha256": digest(data)})

        def read(relative: str) -> bytes:
            return archive.read(PREFIX + relative)

        library_project = ET.fromstring(read("LibraryImportGenerator/LibraryImportGenerator.csproj"))
        source_project = ET.fromstring(read("Microsoft.Interop.SourceGeneration/Microsoft.Interop.SourceGeneration.csproj"))
        directory_props = ET.fromstring(read("Directory.Build.props"))
        resources = ET.fromstring(read("Common/Resources/Strings.resx"))
        paths = [
            project.findtext(".//StringResourcesPath")
            for project in (library_project, source_project)
        ]
        assert paths == ["../Common/Resources/Strings.resx"] * 2
        project_refs = [node.attrib["Include"] for node in library_project.findall(".//ProjectReference")]
        assert project_refs == [r"..\Microsoft.Interop.SourceGeneration\Microsoft.Interop.SourceGeneration.csproj"]
        assert directory_props.findtext(".//UsingToolXliff") == "true"
        assert directory_props.findtext(".//EnableDefaultEmbeddedResourceItems") == "false"

        strings = [node.findtext("value") or "" for node in resources.findall("data")]
        output_path = args.repo_root / "planning/stage-2/repos/dotj-core/evidence/corelib-generated-v10.0.12/LibraryImport.LibraryImports.g.cs.raw"
        output_bytes = output_path.read_bytes()
        assert len(output_bytes) == 645008 and digest(output_bytes) == OUTPUT_SHA256
        output_text = output_bytes.decode("utf-8-sig")
        candidate_strings = [value for value in strings if len(value) >= 32]
        exact_hits = sum(value in output_text for value in candidate_strings)

    manifest = {
        "schemaVersion": 1,
        "sourceTag": "v10.0.12",
        "sourceCommit": COMMIT,
        "archiveBytes": len(archive_bytes),
        "archiveSha256": ARCHIVE_SHA256,
        "scope": "Non-C# files under the pinned System.Runtime.InteropServices/gen directory; two-project LibraryImport generator resource links",
        "generatorDirectoryFileCount": len(names),
        "nonCSharpFileCount": len(entries),
        "nonCSharpFiles": entries,
        "libraryProjectReference": project_refs[0],
        "projectStringResourcesPaths": paths,
        "usingToolXliff": True,
        "enableDefaultEmbeddedResourceItems": False,
        "resxDataCount": len(strings),
        "resxValuesAtLeast32Characters": len(candidate_strings),
        "exactLongResxValuesInGeneratedOutput": exact_hits,
        "generatedOutputSha256": OUTPUT_SHA256,
        "limits": [
            "This inventories archive paths and direct project/props declarations; it does not establish every imported build target or effective resource inclusion.",
            "The exact literal scan uses complete resx values of at least 32 characters; shorter, formatted or transformed text can still contribute to output.",
            "Localization XLF files and resource text are build inputs or candidates, not a file-to-notice or redistribution determination.",
        ],
    }
    target = Path(__file__).with_name("manifest.json")
    target.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Captured {len(entries)} non-C# entries; {len(strings)} resx values; {exact_hits} exact long-value output hits")


if __name__ == "__main__":
    main()
