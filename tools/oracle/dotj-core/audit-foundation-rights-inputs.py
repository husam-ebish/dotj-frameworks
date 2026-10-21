"""Capture bounded rights-review inputs for the foundation candidate JAR."""

import hashlib
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
ARTIFACT = EVIDENCE / "foundation-product-candidate-v1.json"
MAPPING = EVIDENCE / "foundation-file-notice-map-v1.json"
OUTPUT = EVIDENCE / "foundation-rights-inputs-v1.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    jar = ROOT / artifact["jarPath"]
    assert sha256(jar) == artifact["jarSha256"] == mapping["jarSha256"]
    license_file = ROOT / artifact["licensePath"]
    assert artifact["licensePath"] == "dotj-core/LICENSE"
    assert sha256(license_file) == artifact["licenseSha256"]
    assert license_file.read_text(encoding="utf-8").startswith("MIT License\n\nCopyright (c) 2026 dotj Frameworks contributors")
    sources = {item["path"]: item["sha256"] for item in artifact["productSources"]}
    assert set(sources) == set(mapping["sourceToClasses"])
    source_rows = []
    for relative_path in sorted(sources):
        path = ROOT / relative_path
        assert sha256(path) == sources[relative_path]
        text = path.read_text(encoding="utf-8")
        header = "\n".join(text.splitlines()[:30])
        assert text.startswith("// SPDX-License-Identifier: MIT\n\n"), relative_path
        source_rows.append({
            "path": relative_path,
            "sha256": sources[relative_path],
            "classCount": len(mapping["sourceToClasses"][relative_path]),
            "headerHasSpdxIdentifier": "SPDX-License-Identifier:" in header,
            "headerHasCopyrightNotice": bool(re.search(r"(?i)copyright", header)),
            "headerNamesDotNetFoundation": ".NET Foundation" in header,
        })
    license_names = {"license", "license.txt", "license.md", "notice", "notice.txt", "notice.md"}
    product_directories = (ROOT, ROOT / "dotj-core", ROOT / "dotj-core/dotj-core-public")
    product_license_files = sorted(
        path.relative_to(ROOT).as_posix()
        for directory in product_directories
        for path in directory.iterdir()
        if path.is_file() and path.name.lower() in license_names
    )
    with zipfile.ZipFile(jar) as archive:
        entries = archive.namelist()
        assert archive.read(artifact["licenseEntry"]) == license_file.read_bytes()
    notice_entries = [entry for entry in entries
                      if "LICENSE" in entry.upper() or "NOTICE" in entry.upper()]
    assert entries == artifact["jarEntries"]
    assert notice_entries == mapping["jarNoticeEntries"]
    assert product_license_files == ["dotj-core/LICENSE"]
    assert notice_entries == ["META-INF/LICENSE"]
    record = {
        "schemaVersion": 1,
        "scope": "Built foundation candidate JAR only; technical inputs for a licensing decision, not clearance",
        "artifactEvidence": ARTIFACT.name,
        "jarSha256": artifact["jarSha256"],
        "selectedProductLicense": "MIT",
        "licensePath": artifact["licensePath"],
        "licenseSha256": artifact["licenseSha256"],
        "productSourceCount": len(source_rows),
        "productSources": source_rows,
        "localSourceIntroductionEvidence": "foundation-source-provenance-v1.json",
        "productLicenseFilesAtCandidateRoots": product_license_files,
        "jarNoticeEntries": notice_entries,
        "observedJdkModuleDependencies": mapping["observedJdkModuleDependencies"],
        "upstreamReferenceNoticePathsExcludedFromJar": [
            item["path"] for item in mapping["upstreamReferenceEvidenceExcludedFromJar"]
        ],
        "decisionInputs": mapping["decisionInputs"],
        "status": "MIT_PRODUCT_LICENSE_PACKAGED; E01_UPSTREAM_APPLICABILITY_AND_RELEASE_REVIEW_OPEN",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"PASS foundation rights-review inputs: {len(source_rows)} product sources, "
          f"{len(product_license_files)} root license/notice files, {len(notice_entries)} JAR notices")


if __name__ == "__main__":
    main()
