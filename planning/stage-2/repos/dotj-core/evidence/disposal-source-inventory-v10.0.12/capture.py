"""Capture bounded source and project inclusion facts for disposal interfaces."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile


COMMIT = "4271d88e0aebf3d04f188f1334c2220d80555ef6"
ARCHIVE_SHA256 = "ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115"
PREFIX = f"runtime-{COMMIT}/"
SHARED = "src/libraries/System.Private.CoreLib/src/System.Private.CoreLib.Shared.projitems"
CORECLR = "src/coreclr/System.Private.CoreLib/System.Private.CoreLib.csproj"
TYPES = {
    "IDisposable": {
        "source": "src/libraries/System.Private.CoreLib/src/System/IDisposable.cs",
        "method": "void Dispose();",
    },
    "IAsyncDisposable": {
        "source": "src/libraries/System.Private.CoreLib/src/System/IAsyncDisposable.cs",
        "method": "ValueTask DisposeAsync();",
    },
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    raw_archive = args.archive.read_bytes()
    assert len(raw_archive) == 136239366 and sha(raw_archive) == ARCHIVE_SHA256
    with zipfile.ZipFile(args.archive) as archive:
        shared_bytes = archive.read(PREFIX + SHARED)
        coreclr_bytes = archive.read(PREFIX + CORECLR)
        shared = ET.fromstring(shared_bytes)
        coreclr = ET.fromstring(coreclr_bytes)
        imports = [item.attrib for item in coreclr.findall(".//Import") if "Shared.projitems" in item.get("Project", "")]
        assert len(imports) == 1 and "Condition" not in imports[0]
        entries = []
        for name, info in TYPES.items():
            raw = archive.read(PREFIX + info["source"])
            text = raw.decode("utf-8-sig")
            assert "The .NET Foundation licenses this file to you under the MIT license." in text
            assert re.search(r"\bnamespace System\b", text)
            assert re.search(r"\bpublic interface " + name + r"\b", text)
            assert info["method"] in text
            include = f"$(MSBuildThisFileDirectory)System\\{name}.cs"
            groups = [group for group in shared.findall(".//ItemGroup")
                      if any(item.get("Include") == include for item in group.findall("Compile"))]
            assert len(groups) == 1 and "Condition" not in groups[0].attrib
            items = [item for item in groups[0].findall("Compile") if item.get("Include") == include]
            assert len(items) == 1 and "Condition" not in items[0].attrib
            entries.append({
                "type": "System." + name,
                "sourcePath": info["source"],
                "sourceBytes": len(raw),
                "sourceSha256": sha(raw),
                "namespace": "System",
                "declaration": "public interface " + name,
                "memberDeclaration": info["method"],
                "sharedCompileInclude": include,
                "sharedCompileCondition": None,
                "sharedItemGroupCondition": None,
            })

    manifest = {
        "schemaVersion": 1,
        "sourceTag": "v10.0.12",
        "sourceCommit": COMMIT,
        "sourceArchiveSha256": ARCHIVE_SHA256,
        "scope": "Bounded WP-01 disposal interface source identity and direct CoreLib shared project inclusion",
        "coreclrProject": {"path": CORECLR, "sha256": sha(coreclr_bytes), "sharedImport": imports[0]},
        "sharedProject": {"path": SHARED, "sha256": sha(shared_bytes)},
        "interfaces": entries,
        "limits": [
            "Source declarations and immediate XML inclusion are verified; effective evaluated compiler inputs, reference-assembly metadata and generated or forwarded symbols remain open.",
            "IDisposable comments describe guidance, not a runtime-enforced idempotence or nonthrowing guarantee for all implementations.",
            "IAsyncDisposable's ValueTask dependency and Java representation require separate E02/N01 analysis.",
        ],
    }
    Path(__file__).with_name("manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print("Verified two pinned disposal declarations and their direct shared project includes")


if __name__ == "__main__":
    main()
