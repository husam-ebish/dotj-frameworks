"""Compare six compiled Java candidate types with pinned selected CoreLib metadata."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
METADATA = EVIDENCE / "foundation-selected-metadata-v10.0.12.json"
ARTIFACT = EVIDENCE / "foundation-product-candidate-v1.json"
OUTPUT = EVIDENCE / "foundation-public-candidate-ledger-v1.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    pinned = json.loads(METADATA.read_text(encoding="utf-8"))
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    jar = ROOT / artifact["jarPath"]
    assert sha256(jar) == artifact["jarSha256"]
    assert pinned["coreLibSha256"] == "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"
    records = []
    for upstream in pinned["types"]:
        name = upstream["fullName"]
        output = subprocess.run(["javap", "-public", "-classpath", str(jar), name],
                                cwd=ROOT, capture_output=True, text=True, check=True).stdout
        lines = [line.strip() for line in output.splitlines()]
        header = next(line for line in lines if line.startswith("public ") and line.endswith("{"))
        declarations = [line for line in lines if line.startswith("public ") and line.endswith(";")]
        if name == "System.IDisposable":
            assert declarations == ["public abstract void Dispose();"]
            disposition = "EXACT_SELECTED_INTERFACE_MEMBER; behavior and release unqualified"
        elif name == "System.Type":
            assert "public abstract class System.Type" in header
            assert any(" MakeGenericType(System.Type[]);" in line for line in declarations)
            disposition = "PARTIAL_PUBLIC_SURFACE; MemberInfo base, Java property lowering and semantics open"
        else:
            assert header.startswith("public class " + name)
            disposition = "PARTIAL_EXCEPTION_SURFACE; selected inheritance/constructors only"
        records.append({
            "upstreamFullName": name,
            "upstreamBaseType": upstream["baseType"],
            "upstreamIsInterface": upstream["isInterface"],
            "upstreamIsAbstract": upstream["isAbstract"],
            "upstreamDeclaredNonAccessorMethods": upstream["declaredPublicMethodCount"],
            "upstreamDeclaredProperties": upstream["declaredPublicPropertyCount"],
            "upstreamPublicConstructors": len(upstream["publicConstructors"]),
            "javaPublicHeader": header,
            "javaPublicDeclarations": declarations,
            "disposition": disposition,
            "qualified": False,
        })
    assert len(records) == 6
    assert records[1]["upstreamDeclaredNonAccessorMethods"] == 109
    assert records[1]["upstreamDeclaredProperties"] == 70
    snapshot = json.loads((EVIDENCE / "api-shapes-v10.0.12/system-type.json").read_text(encoding="utf-8"))
    assert len(snapshot["type"]["methods"]) == 181
    assert len(snapshot["type"]["properties"]) == 70
    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "coreLibSha256": pinned["coreLibSha256"],
        "metadataEvidence": METADATA.name,
        "candidateEvidence": ARTIFACT.name,
        "candidateJarSha256": artifact["jarSha256"],
        "typeCount": len(records),
        "typeMethodCountNote": "The earlier Type snapshot lists 181 declared methods including property accessors; this oracle counts 109 non-accessor methods and 70 properties.",
        "types": records,
        "acceptedN01TaskCredit": False,
        "status": "SELECTED_COMPILED_CANDIDATES_ONLY; complete E01/E02/E03/N01 public API and behavior qualification OPEN",
    }, indent=2) + "\n", encoding="utf-8")
    print("PASS six selected CoreLib identities mapped to compiled Java candidate declarations")


if __name__ == "__main__":
    main()
