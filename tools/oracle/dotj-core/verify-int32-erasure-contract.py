"""Pin the Int32 span erasure boundary and classify extra Java public methods."""

import hashlib
import json
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
AUDIT = EVIDENCE / "int32-declared-signature-audit-v1.json"
OUTPUT = EVIDENCE / "int32-erasure-contract-v1.json"

CONVERSION_METHODS = {
    "ToBoolean", "ToChar", "ToSByte", "ToByte", "ToInt16", "ToUInt16",
    "ToInt32", "ToUInt32", "ToInt64", "ToUInt64", "ToSingle", "ToDouble",
    "ToDecimal", "ToDateTime", "ToType",
}


def prove_erasure():
    source = """class ReadOnlySpan<T> {}
class Probe {
    static int Parse(ReadOnlySpan<Character> value) { return 1; }
    static int Parse(ReadOnlySpan<Byte> value) { return 2; }
}
"""
    with tempfile.TemporaryDirectory(prefix="dotj-int32-erasure-") as folder:
        path = Path(folder) / "Probe.java"
        path.write_text(source, encoding="utf-8")
        result = subprocess.run(
            ["javac", "-J-Duser.language=en", "--release", "21", str(path)],
            cwd=folder, capture_output=True, text=True)
    if result.returncode == 0 or "name clash" not in result.stderr or "same erasure" not in result.stderr:
        raise RuntimeError("Expected JVM generic overload rejection was not reproduced: "
                           + result.stderr)
    return {"javacRejected": True, "diagnostic": "name clash: same erasure"}


def main():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["upstreamMethodCount"] == 53
    assert audit["erasureCollapsedOverloadGroupCount"] == 5
    assert audit["erasureCollapsedUpstreamMethodCount"] == 10
    groups = defaultdict(list)
    for method in audit["methods"]:
        if method["status"] == "ERASURE_COLLAPSED_CARRIER":
            groups[method["collapsedCarrierDeclaration"]].append(method["upstreamSignature"])
    assert len(groups) == 5 and all(len(signatures) == 2 for signatures in groups.values())
    overloads = []
    for carrier, signatures in sorted(groups.items()):
        char = [signature for signature in signatures
                if "System.ReadOnlySpan`1[System.Char]" in signature]
        byte = [signature for signature in signatures
                if "System.ReadOnlySpan`1[System.Byte]" in signature]
        assert len(char) == len(byte) == 1, signatures
        overloads.append({
            "clrCharSignature": char[0],
            "clrByteSignature": byte[0],
            "javaCarrierDeclaration": carrier,
            "requiredResolution": "Select the CLR overload from the source span element type before lowering to this JVM method",
        })
    extras = []
    for declaration in audit["extraJavaPublicMethods"]:
        name = declaration.split("(", 1)[0].split()[-1]
        if name in CONVERSION_METHODS:
            disposition = "JAVA_PUBLIC_INTERFACE_BRIDGE; CLR IConvertible member is explicit"
        elif name == "get_Value":
            disposition = "BOXED_VALUE_CARRIER_ACCESSOR; no CLR Int32 public Value property"
        elif name in {"equals", "hashCode"}:
            disposition = "JAVA_OBJECT_INTEROP_BRIDGE; not a declared CLR Int32 method"
        else:
            raise AssertionError("Unclassified extra public method: " + declaration)
        extras.append({"declaration": declaration, "disposition": disposition})
    assert len(extras) == 18
    output = {
        "schemaVersion": 1,
        "scope": "Selected Int32 ReadOnlySpan overloads and extra Java public declarations",
        "signatureAudit": AUDIT.name,
        "signatureAuditSha256": hashlib.sha256(AUDIT.read_bytes()).hexdigest(),
        "javacErasureProof": prove_erasure(),
        "clrOverloadCount": 10,
        "javaCarrierMethodCount": len(overloads),
        "overloadMappings": overloads,
        "extraJavaPublicMethodCount": len(extras),
        "extraJavaPublicMethods": extras,
        "status": "FRONTEND_TYPE_DIRECTED_LOWERING_AND_PUBLIC_BRIDGE_POLICY_REQUIRED; N01 OPEN",
        "limitation": "This verifies a mapping contract and a javac rejection. No .j compiler consumes the mapping; it does not establish exact overload dispatch or hide extra Java public members.",
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print("PASS Int32 erasure contract: 10 CLR overloads, 5 JVM carriers, "
          "18 classified extra public methods; javac clash reproduced")


if __name__ == "__main__":
    main()
