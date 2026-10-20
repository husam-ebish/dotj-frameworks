"""Capture two bounded LibraryImports.g.cs source-to-output traces."""

import argparse
import hashlib
import json
from pathlib import Path


SOURCE_WINDOWS = [
    ("forwarder-input", "src/coreclr/System.Private.CoreLib/src/Internal/VersionResilientHashCode.CoreCLR.cs", 1, 18),
    ("bool-input", "src/coreclr/System.Private.CoreLib/src/System/Array.CoreCLR.cs", 1, 21),
    ("generator-register", "src/libraries/System.Runtime.InteropServices/gen/LibraryImportGenerator/LibraryImportGenerator.cs", 90, 110),
    ("generator-source-choice", "src/libraries/System.Runtime.InteropServices/gen/LibraryImportGenerator/LibraryImportGenerator.cs", 326, 379),
    ("generator-forwarder", "src/libraries/System.Runtime.InteropServices/gen/LibraryImportGenerator/LibraryImportGenerator.cs", 382, 431),
    ("generator-local-import", "src/libraries/System.Runtime.InteropServices/gen/LibraryImportGenerator/LibraryImportGenerator.cs", 432, 475),
    ("generator-concatenate", "src/libraries/System.Runtime.InteropServices/gen/Microsoft.Interop.SourceGeneration/IncrementalGeneratorInitializationContextExtensions.cs", 69, 98),
    ("body-compose", "src/libraries/System.Runtime.InteropServices/gen/Microsoft.Interop.SourceGeneration/ManagedToNativeStubGenerator.cs", 109, 175),
    ("resolver-compose", "src/libraries/System.Runtime.InteropServices/gen/Microsoft.Interop.SourceGeneration/Marshalling/DefaultMarshallingGeneratorResolver.cs", 23, 36),
    ("resolver-bool", "src/libraries/System.Runtime.InteropServices/gen/Microsoft.Interop.SourceGeneration/Marshalling/MarshalAsMarshallingGeneratorResolver.cs", 75, 85),
    ("bool-expression", "src/libraries/System.Runtime.InteropServices/gen/Microsoft.Interop.SourceGeneration/Marshalling/BoolMarshaller.cs", 51, 82),
    ("bool-values", "src/libraries/System.Runtime.InteropServices/gen/Microsoft.Interop.SourceGeneration/Marshalling/BoolMarshaller.cs", 132, 143),
    ("statement-stages", "src/libraries/System.Runtime.InteropServices/gen/Microsoft.Interop.SourceGeneration/GeneratedStatements.cs", 29, 43),
    ("statement-dispatch", "src/libraries/System.Runtime.InteropServices/gen/Microsoft.Interop.SourceGeneration/GeneratedStatements.cs", 72, 84),
]

OUTPUT_WINDOWS = [
    ("forwarder-output", 2, 9),
    ("bool-output", 90, 109),
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def capture_window(data: bytes, start: int, end: int, path: Path, evidence_root: Path) -> dict:
    lines = data.splitlines(keepends=True)
    if start < 1 or end > len(lines) or start > end:
        raise ValueError(f"Invalid lines {start}-{end}: {path}")
    excerpt = b"".join(lines[start - 1 : end])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(excerpt)
    return {"path": path.relative_to(evidence_root).as_posix(), "lineStart": start, "lineEnd": end, "bytes": len(excerpt), "sha256": sha256(excerpt)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    source_root = args.source_root.resolve()
    evidence_root = Path(__file__).resolve().parent
    output_path = repo_root / "planning/stage-2/repos/dotj-core/evidence/corelib-generated-v10.0.12/LibraryImport.LibraryImports.g.cs.raw"
    output_bytes = output_path.read_bytes()
    if sha256(output_bytes) != "094c3ccc4a4de9fe3a146af0964b784ca8c04542f32729b86786e0d644ae248b":
        raise ValueError("Pinned generated output changed")

    source_records = []
    for label, relative, start, end in SOURCE_WINDOWS:
        source = source_root / relative
        data = source.read_bytes()
        header_data = data.removeprefix(b"\xef\xbb\xbf")
        source_records.append({
            "label": label,
            "sourcePath": relative,
            "sourceSha256": sha256(data),
            "hasNetFoundationMitHeader": header_data.startswith(b"// Licensed to the .NET Foundation under one or more agreements.\n// The .NET Foundation licenses this file to you under the MIT license.") or header_data.startswith(b"// Licensed to the .NET Foundation under one or more agreements.\r\n// The .NET Foundation licenses this file to you under the MIT license."),
            "excerpt": capture_window(data, start, end, evidence_root / "source" / (label + ".raw"), evidence_root),
        })
    output_records = []
    for label, start, end in OUTPUT_WINDOWS:
        output_records.append({"label": label, "excerpt": capture_window(output_bytes, start, end, evidence_root / "output" / (label + ".raw"), evidence_root)})

    sources = {record["label"]: (evidence_root / record["excerpt"]["path"]).read_text(encoding="utf-8-sig") for record in source_records}
    outputs = {record["label"]: (evidence_root / record["excerpt"]["path"]).read_text(encoding="utf-8-sig") for record in output_records}
    assertions = {
        "forwarderInput": 'EntryPoint = "VersionResilientHashCode_TypeHashCode"' in sources["forwarder-input"] and "private static partial int TypeHashCode" in sources["forwarder-input"],
        "forwarderOutput": 'EntryPoint = "VersionResilientHashCode_TypeHashCode"' in outputs["forwarder-output"] and "extern partial int TypeHashCode" in outputs["forwarder-output"],
        "boolInput": 'EntryPoint = "Array_CreateInstance"' in sources["bool-input"] and "[MarshalAs(UnmanagedType.Bool)] bool fromArrayType" in sources["bool-input"],
        "boolOutput": 'EntryPoint = "Array_CreateInstance"' in outputs["bool-output"] and "__fromArrayType_native = (int)(fromArrayType ? 1 : 0);" in outputs["bool-output"],
        "forwarderRoute": "PrintForwarderStub" in sources["generator-source-choice"] and "CreateForwarderDllImport" in sources["generator-forwarder"],
        "boolRoute": "GenerateStubBody" in sources["generator-source-choice"] and "MarshalAsInfo(UnmanagedType.I4 or UnmanagedType.Bool" in sources["resolver-bool"] and "trueValue: 1, falseValue: 0" in sources["bool-values"] and "ConditionalExpression" in sources["bool-expression"],
        "commonEmitter": "RegisterConcatenatedSyntaxOutputs" in sources["generator-register"] and "context.AddSource(fileName, source.ToString())" in sources["generator-concatenate"],
        "outputNoticeMarkersAbsent": not any(token in (outputs["forwarder-output"] + outputs["bool-output"]).casefold() for token in ("copyright", "license", "licence", "third-party", "third party")),
    }
    if not all(assertions.values()):
        raise ValueError(f"Trace anchor missing: {[name for name, ok in assertions.items() if not ok]}")

    manifest = {
        "schemaVersion": 1,
        "recordedDate": "2026-10-20",
        "scope": "Two bounded static source-to-output traces within pinned CoreLib LibraryImports.g.cs",
        "status": "TWO_STUBS_TRACED_STATICALLY; FILE_TO_NOTICE_APPLICABILITY_OPEN",
        "sourceCommit": "4271d88e0aebf3d04f188f1334c2220d80555ef6",
        "generatedOutput": {"priorEvidencePath": "../corelib-generated-v10.0.12/LibraryImport.LibraryImports.g.cs.raw", "bytes": len(output_bytes), "sha256": sha256(output_bytes)},
        "sourceWindows": source_records,
        "outputWindows": output_records,
        "anchorChecks": assertions,
        "traces": [
            {
                "sample": "Internal.VersionResilientHashCode.TypeHashCode",
                "kind": "extern forwarder",
                "input": "forwarder-input",
                "output": "forwarder-output",
                "observedCorrespondence": "The declared method, QCall entry point and parameter type appear in the emitted extern DllImport form.",
                "staticRoute": ["generator-register", "generator-source-choice", "generator-forwarder", "generator-concatenate"],
                "contentClassification": "Input-derived names/signature and generator-constructed C# syntax; no inline notice marker found in this excerpt.",
                "routeLimit": "The output form matches PrintForwarderStub, but this static trace does not prove which of its two caller branches executed.",
            },
            {
                "sample": "System.Array.InternalCreate",
                "kind": "marshalled wrapper with local P/Invoke",
                "input": "bool-input",
                "output": "bool-output",
                "observedCorrespondence": "The input MarshalAs(UnmanagedType.Bool) parameter and Array_CreateInstance entry point correspond to the emitted int temporary, 1/0 conversion and local DllImport.",
                "staticRoute": ["generator-register", "generator-source-choice", "resolver-compose", "resolver-bool", "bool-values", "bool-expression", "statement-stages", "statement-dispatch", "body-compose", "generator-local-import", "generator-concatenate"],
                "contentClassification": "Input-derived identifiers and entry point plus generator-constructed marshalling syntax; no inline notice marker found in this excerpt.",
                "routeLimit": "Static source/output correspondence, not an instrumented generator execution or exhaustive template provenance review.",
            },
        ],
        "noticeCandidates": [
            "The two selected upstream CoreLib declarations and all sampled generator source files have .NET Foundation MIT headers; see sourceWindows and pinned root LICENSE.TXT.",
            "The output excerpt has no inline license header. Source and generator provenance remains relevant even when the emitted file begins only with an auto-generated marker.",
            "The 36-package build-chain graph records build dependencies, but this two-stub trace finds no inline notice marker in either excerpt. It cannot waive or assign package notices for the full output or any future .j artifact.",
        ],
        "limits": [
            "Only two generated stubs and selected source windows were traced; the remaining 645,008-byte generated file was not classified.",
            "The static route is inferred from pinned source and output anchors; no instrumented source-generator execution was performed.",
            "No legal redistribution clearance or .j implementation/API compatibility is claimed.",
        ],
        "relatedEvidence": ["../libraryimport-notice-scope-v10.0.12/manifest.json", "../generated-rights-v10.0.12/manifest.json"],
        "primaryLicense": "https://github.com/dotnet/runtime/blob/v10.0.12/LICENSE.TXT",
    }
    (evidence_root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Captured {len(source_records)} source windows and {len(output_records)} output windows; {sum(assertions.values())} anchors passed")


if __name__ == "__main__":
    main()
