"""Compare pinned declared public metadata with the bounded Java candidate surface."""

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
METADATA = EVIDENCE / "foundation-selected-metadata-v10.0.12.json"
LEDGER = EVIDENCE / "foundation-public-candidate-ledger-v1.json"
OUTPUT = EVIDENCE / "foundation-semantic-surface-v1.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def java_method_names(declarations, full_name):
    return [declaration.split("(", 1)[0].split()[-1].split(".")[-1]
            for declaration in declarations if "(" in declaration
            and not declaration.startswith("public " + full_name + "(")]


def main():
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    upstream = {item["fullName"]: item for item in metadata["completeDeclaredSurface"]}
    java = {item["upstreamFullName"]: item for item in ledger["types"]}
    targets = [item["fullName"] for item in metadata["types"]]
    assert len(targets) == len(set(targets)) == 30
    assert set(upstream) == set(java) == set(targets)
    assert len(upstream["System.Type"]["methods"]) == 181
    assert len(upstream["System.Type"]["properties"]) == 70
    assert len(upstream["System.Exception"]["constructors"]) == 3
    records = []
    for name in targets:
        observed = upstream[name]
        candidate = java[name]
        methods = [method for method in observed["methods"] if not method["isSpecialName"]]
        upstream_counts = Counter(method["name"] for method in methods)
        java_names = java_method_names(candidate["javaPublicDeclarations"], name)
        java_counts = Counter(java_names)
        public_getters = [prop["name"] for prop in observed["properties"] if prop["publicGetter"]]
        records.append({
            "fullName": name,
            "upstreamDeclaredMethodCountIncludingAccessors": len(observed["methods"]),
            "upstreamDeclaredNonAccessorMethodCount": len(methods),
            "upstreamDeclaredPropertyCount": len(observed["properties"]),
            "upstreamDeclaredConstructorCount": len(observed["constructors"]),
            "upstreamDeclaredFieldCount": len(observed["fields"]),
            "upstreamDeclaredEventCount": len(observed["events"]),
            "upstreamDeclaredNestedPublicTypeCount": len(observed["nestedPublicTypes"]),
            "upstreamDeclaredSurface": observed,
            "javaCandidatePublicHeader": candidate["javaPublicHeader"],
            "javaCandidateDeclaredPublicDeclarations": candidate["javaPublicDeclarations"],
            "nameLevelComparison": {
                "upstreamNonAccessorOverloads": dict(sorted(upstream_counts.items())),
                "javaCandidateDeclaredMethodOverloads": dict(sorted(java_counts.items())),
                "upstreamMethodNamesAbsentFromJavaDeclarations": sorted(set(upstream_counts) - set(java_counts)),
                "upstreamPublicPropertyGettersAbsentFromJavaDeclarations": sorted(
                    name for name in public_getters if "get_" + name not in java_counts),
                "limitation": "Name-only, declared-member comparison; inherited Java methods, JVM type adaptation, overload signatures, conditional source attribution and behavior require separate review",
            },
        })
    missing_methods = sum(len(record["nameLevelComparison"]["upstreamMethodNamesAbsentFromJavaDeclarations"])
                          for record in records)
    missing_getters = sum(len(record["nameLevelComparison"]["upstreamPublicPropertyGettersAbsentFromJavaDeclarations"])
                          for record in records)
    output = {
        "schemaVersion": 1,
        "profile": ".NET 10.0.12 CoreLib and Java 21 foundation candidate",
        "coreLibSha256": metadata["coreLibSha256"],
        "oracleEvidence": METADATA.name,
        "oracleEvidenceSha256": sha256(METADATA),
        "javaCandidateEvidence": LEDGER.name,
        "javaCandidateEvidenceSha256": sha256(LEDGER),
        "selectedTypeCount": len(records),
        "nameLevelMissingMethodCount": missing_methods,
        "nameLevelMissingPublicGetterCount": missing_getters,
        "types": records,
        "status": "DECLARED_PUBLIC_METADATA_EXTRACTED_FOR_30_TYPES; E02_SOURCE_ATTRIBUTION_AND_N01_EXACT_MAPPING_OPEN",
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"PASS declared public semantic surface: {len(records)} types; "
          f"{missing_methods} method names and {missing_getters} public getters absent at name level")


if __name__ == "__main__":
    main()
