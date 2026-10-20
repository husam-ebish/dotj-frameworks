"""Trace generated-code metadata to pinned generator source and output."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile


COMMIT = "4271d88e0aebf3d04f188f1334c2220d80555ef6"
ARCHIVE_SHA256 = "ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115"
OUTPUT_SHA256 = "094c3ccc4a4de9fe3a146af0964b784ca8c04542f32729b86786e0d644ae248b"
PREFIX = f"runtime-{COMMIT}/src/libraries/System.Runtime.InteropServices/gen/"
SOURCE_RANGES = {
    "LibraryImportGenerator/LibraryImportGenerator.cs": (300, 306),
    "Microsoft.Interop.SourceGeneration/SignatureContext.cs": (63, 80),
    "Microsoft.Interop.SourceGeneration/TypeNames.cs": (260, 265),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    archive_bytes = args.archive.read_bytes()
    assert len(archive_bytes) == 136239366 and sha(archive_bytes) == ARCHIVE_SHA256

    sources = []
    with zipfile.ZipFile(args.archive) as archive:
        for path, (start, end) in SOURCE_RANGES.items():
            raw = archive.read(PREFIX + path)
            lines = raw.decode("utf-8-sig").splitlines()
            selected = "\n".join(lines[start - 1:end])
            sources.append({
                "path": "src/libraries/System.Runtime.InteropServices/gen/" + path,
                "bytes": len(raw),
                "sha256": sha(raw),
                "lineStart": start,
                "lineEnd": end,
                "excerptSha256Utf8Lf": sha(selected.encode("utf-8")),
            })
        generator = archive.read(PREFIX + "LibraryImportGenerator/LibraryImportGenerator.cs").decode("utf-8-sig")
        signature = archive.read(PREFIX + "Microsoft.Interop.SourceGeneration/SignatureContext.cs").decode("utf-8-sig")
        names = archive.read(PREFIX + "Microsoft.Interop.SourceGeneration/TypeNames.cs").decode("utf-8-sig")
        assert "typeof(LibraryImportGenerator).Assembly" in generator
        assert "generatorInfoAssembly.GetName().Version.ToString()" in signature
        assert "NameSyntaxes.System_CodeDom_Compiler_GeneratedCodeAttribute" in signature
        assert 'System.CodeDom.Compiler.GeneratedCodeAttribute' in names

    output = args.repo_root / "planning/stage-2/repos/dotj-core/evidence/corelib-generated-v10.0.12/LibraryImport.LibraryImports.g.cs.raw"
    raw = output.read_bytes()
    assert len(raw) == 645008 and sha(raw) == OUTPUT_SHA256
    matches = re.findall(r'GeneratedCodeAttribute\("([^"]+)", "([^"]+)"\)', raw.decode("utf-8-sig"))
    assert len(matches) == 298
    assert set(matches) == {("Microsoft.Interop.LibraryImportGenerator", "42.42.42.42")}

    manifest = {
        "schemaVersion": 1,
        "sourceCommit": COMMIT,
        "sourceArchiveSha256": ARCHIVE_SHA256,
        "generatedOutputSha256": OUTPUT_SHA256,
        "scope": "GeneratedCodeAttribute provenance in captured CoreLib LibraryImports.g.cs",
        "sourceWindows": sources,
        "generatorAssemblyPassedToSignatureContext": True,
        "signatureContextReadsAssemblyNameAndVersion": True,
        "generatedCodeAttributeCount": len(matches),
        "distinctGeneratedCodeMetadata": [
            {"generator": name, "version": version} for name, version in sorted(set(matches))
        ],
        "limits": [
            "This links the emitted metadata shape to source logic; it does not independently rebuild the generator or prove the origin of the assembly's 42.42.42.42 version value.",
            "The captured generator metadata is a development-build observation, not official release-artifact provenance.",
            "No redistribution or file-to-notice applicability determination is made.",
        ],
    }
    Path(__file__).with_name("manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Verified {len(matches)} generated-code attributes from {len(sources)} pinned source files")


if __name__ == "__main__":
    main()
