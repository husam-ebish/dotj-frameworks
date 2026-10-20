"""Capture a bounded LibraryImportGenerator build-chain notice review."""

import argparse
import hashlib
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(source: Path, target: Path, evidence_root: Path) -> dict:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return {
        "path": target.relative_to(evidence_root).as_posix(),
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
    }


def package_names(assets: dict) -> set[str]:
    return {
        name
        for name, data in assets["targets"]["netstandard2.0"].items()
        if data["type"] == "package"
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    source_root = args.source_root.resolve()
    evidence_root = Path(__file__).resolve().parent
    base_evidence = repo_root / "planning/stage-2/repos/dotj-core/evidence"
    prior_root = base_evidence / "libraryimport-package-graph-v10.0.12"
    prior_manifest_path = prior_root / "manifest.json"
    prior = json.loads(prior_manifest_path.read_text(encoding="utf-8"))
    library_assets = json.loads((prior_root / "project.assets.json.raw").read_text(encoding="utf-8"))
    source_assets_path = source_root / "artifacts/obj/Microsoft.Interop.SourceGeneration/project.assets.json"
    source_assets = json.loads(source_assets_path.read_text(encoding="utf-8"))
    source_assets_snapshot = snapshot(source_assets_path, evidence_root / "source-generation.assets.json.raw", evidence_root)
    library_packages = package_names(library_assets)
    source_packages = package_names(source_assets)
    if len(library_packages) != 33 or len(source_packages) != 36:
        raise ValueError("Unexpected restored package count")
    if not library_packages.issubset(source_packages):
        raise ValueError("Unexpected package identities outside referenced project graph")
    package_root = Path(next(iter(source_assets["packageFolders"]))).resolve()
    extras = []
    for identity in sorted(source_packages - library_packages):
        package_id, version = identity.split("/", 1)
        cache_dir = package_root / package_id.lower() / version
        nuspecs = list(cache_dir.glob("*.nuspec"))
        if len(nuspecs) != 1:
            raise ValueError(f"Expected one nuspec for {identity}")
        package_snapshot_dir = evidence_root / "additional-packages" / package_id.lower() / version
        nuspec_snapshot = snapshot(nuspecs[0], package_snapshot_dir / nuspecs[0].name, evidence_root)
        xml = ET.parse(nuspecs[0]).getroot()
        license_element = xml.find("./{*}metadata/{*}license")
        notice_files = []
        for file in sorted(cache_dir.rglob("*")):
            if file.is_file() and re.search(r"license|licence|notice|third.?party|copyright|credits", file.name, re.I):
                relative = file.relative_to(cache_dir)
                notice_files.append(snapshot(file, package_snapshot_dir / relative, evidence_root))
        extras.append({
            "identity": identity,
            "nuspec": nuspec_snapshot,
            "licenseType": license_element.get("type") if license_element is not None else None,
            "licenseValue": license_element.text if license_element is not None else None,
            "noticeLikeFiles": notice_files,
            "sha512FromAssets": source_assets["libraries"][identity]["sha512"],
        })

    project_paths = {
        "generatorProject": "src/libraries/System.Runtime.InteropServices/gen/LibraryImportGenerator/LibraryImportGenerator.csproj",
        "sourceGenerationProject": "src/libraries/System.Runtime.InteropServices/gen/Microsoft.Interop.SourceGeneration/Microsoft.Interop.SourceGeneration.csproj",
        "generatorTargets": "eng/generators.targets",
    }
    projects = {key: {"sourcePath": path, **snapshot(source_root / path, evidence_root / "source" / (Path(path).name + ".raw"), evidence_root)} for key, path in project_paths.items()}

    generator_project = ET.parse(source_root / project_paths["generatorProject"]).getroot()
    referenced_project = ET.parse(source_root / project_paths["sourceGenerationProject"]).getroot()
    targets = ET.parse(source_root / project_paths["generatorTargets"]).getroot()
    direct_references = []
    for label, project in (("LibraryImportGenerator", generator_project), ("Microsoft.Interop.SourceGeneration", referenced_project)):
        for element in project.iter("PackageReference"):
            direct_references.append({"project": label, "package": element.get("Include"), "privateAssets": element.get("PrivateAssets")})
    analyzer_references = []
    for element in targets.iter("ProjectReference"):
        include = element.get("Include", "")
        if include.endswith("\\LibraryImportGenerator\\LibraryImportGenerator.csproj") or include.endswith("\\Microsoft.Interop.SourceGeneration\\Microsoft.Interop.SourceGeneration.csproj"):
            analyzer_references.append({
                "include": include,
                "outputItemType": element.get("OutputItemType"),
                "referenceOutputAssembly": element.get("ReferenceOutputAssembly"),
            })

    generated_path = base_evidence / "corelib-generated-v10.0.12/LibraryImport.LibraryImports.g.cs.raw"
    generated_text = generated_path.read_text(encoding="utf-8-sig")
    scan_terms = [r"copyright", r"licen[sc]ed?", r"third[- ]party", r"Microsoft\.CodeAnalysis", r"Humanizer", r"StyleCop", r"Workspaces"]
    literal_scan = {term: len(re.findall(term, generated_text, re.I)) for term in scan_terms}
    prior_notices = [file for package in prior["packages"] for file in package["noticeLikeFiles"]]
    extra_notices = [file for package in extras for file in package["noticeLikeFiles"]]
    distinct_hashes = {file["sha256"] for file in prior_notices + extra_notices}
    manifest = {
        "schemaVersion": 1,
        "recordedDate": "2026-10-20",
        "scope": "Bounded notice and artifact-boundary review for the pinned LibraryImportGenerator build chain and captured CoreLib generated output",
        "status": "BUILD_CHAIN_INVENTORIED; FILE_TO_NOTICE_AND_FUTURE_DISTRIBUTION_APPLICABILITY_OPEN",
        "sourceCommit": "4271d88e0aebf3d04f188f1334c2220d80555ef6",
        "priorGraphManifest": {"path": "../libraryimport-package-graph-v10.0.12/manifest.json"},
        "sourceGenerationAssets": source_assets_snapshot,
        "sourceFiles": projects,
        "directPackageReferences": direct_references,
        "analyzerProjectReferences": analyzer_references,
        "libraryImportTargetPackageCount": len(library_packages),
        "sourceGenerationTargetPackageCount": len(source_packages),
        "unionPackageCount": len(library_packages | source_packages),
        "additionalPackages": extras,
        "noticeLikeFileCountAcrossUnion": len(prior_notices) + len(extra_notices),
        "distinctNoticeLikeContentHashes": len(distinct_hashes),
        "generatedOutput": {
            "priorEvidencePath": "../corelib-generated-v10.0.12/LibraryImport.LibraryImports.g.cs.raw",
            "bytes": generated_path.stat().st_size,
            "sha256": sha256(generated_path),
            "firstLine": generated_text.splitlines()[0],
            "boundedLiteralScanCounts": literal_scan,
        },
        "artifactBoundaries": [
            {"scope": "Local C# oracle build", "observation": "NuGet packages are in the isolated local cache; the pinned targets use LibraryImportGenerator and Microsoft.Interop.SourceGeneration as analyzer project references. This is build use, not proof of artifact inclusion."},
            {"scope": "Committed planning evidence", "observation": "The repository copies nuspec and notice-like files, plus the generated C# source, as evidence. Preserve the original texts and provenance while assessing any repository redistribution."},
            {"scope": "Future .j product distribution", "observation": "No .j runtime or SDK artifact manifest exists. Package inclusion and notice obligations for a future product cannot be determined from this build graph."},
        ],
        "reviewFindings": [
            "PrivateAssets=all limits PackageReference propagation; it does not determine rights in code that a generator emits or in separately copied evidence files.",
            "The captured generated output has an auto-generated marker and no hit for the bounded license/package-name scan. This does not prove that no third-party text or templates contributed to it.",
            "The root runtime MIT license and third-party notice are retained in earlier evidence; their file-level application to generated output and future adaptations remains open.",
            "All 57 filename-selected package notice-like files are retained across the two manifests; the three added Roslyn packages declare MIT in their nuspecs. No package notice is assigned to generated output solely because its package appears in a restore graph.",
        ],
        "unresolved": [
            "Trace generator emission pathways and templates against a bounded sample of LibraryImports.g.cs before assigning copied-source provenance.",
            "Determine the actual .j release artifact contents and notice bundle when an artifact exists.",
            "Review legacy license URLs, embedded or differently named notices, and package-specific terms before any rights clearance or redistribution decision.",
        ],
        "primaryReferences": [
            "https://github.com/dotnet/runtime/blob/v10.0.12/LICENSE.TXT",
            "https://github.com/dotnet/runtime/blob/v10.0.12/THIRD-PARTY-NOTICES.TXT",
            "https://github.com/dotnet/runtime/blob/v10.0.12/docs/project/licensing-assets.md",
            "https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files",
        ],
    }
    (evidence_root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Union packages: {manifest['unionPackageCount']}; added: {len(extras)}; notice-like files: {manifest['noticeLikeFileCountAcrossUnion']}")


if __name__ == "__main__":
    main()
