"""Audit every declared Int32 overload against the compiled Java candidate."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
SURFACE = EVIDENCE / "foundation-semantic-surface-v1.json"
OUTPUT = EVIDENCE / "int32-declared-signature-audit-v1.json"

TYPES = {
    "System.Boolean": "boolean",
    "System.Int32": "System.Int32",
    "System.Int64": "long",
    "System.Object": "java.lang.Object",
    "System.String": "java.lang.String",
    "System.TypeCode": "System.TypeCode",
    "System.IFormatProvider": "System.IFormatProvider",
    "System.Globalization.NumberStyles": "System.Globalization.NumberStyles",
    "TOther": "TOther",
}
SPAN_TYPES = {"System.Byte": "byte[]", "System.Char": "char[]"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def java_method(declaration):
    if "(" not in declaration or not declaration.endswith(");"):
        return None
    head, parameters = declaration[:-2].split("(", 1)
    body = head.removeprefix("public ")
    is_static = body.startswith("static ")
    if is_static:
        body = body.removeprefix("static ")
    generic_arity = 1 if body.startswith("<TOther> ") else 0
    if generic_arity:
        body = body.removeprefix("<TOther> ")
    if " " not in body:
        return None  # Public carrier constructor, not a CLR Int32 method.
    return_type, name = body.rsplit(" ", 1)
    return {
        "declaration": declaration,
        "name": name,
        "isStatic": is_static,
        "genericArity": generic_arity,
        "returnType": return_type,
        "parameters": [] if not parameters else parameters.split(", "),
    }


def projected_type(type_name, method_name, parameter_name=None):
    if type_name == "System.Int32&":
        if method_name == "TryFormat":
            return "int[]", "CLR by-reference character count uses a Java int array"
        return "System.Int32[]", "CLR by-reference output uses a Java array"
    if type_name.startswith(("System.ReadOnlySpan`1[[", "System.Span`1[[")):
        assert type_name.endswith("]]"), type_name
        element = type_name.split("[[", 1)[1].split(",", 1)[0]
        assert element in SPAN_TYPES, type_name
        if method_name == "TryFormat" and parameter_name == "format":
            return "java.lang.String", "format span uses a Java String"
        return SPAN_TYPES[element], "CLR span uses a Java array"
    if (type_name.startswith("System.ValueTuple`2[[System.Int32, ")
            and type_name.count("[System.Int32, System.Private.CoreLib, ") == 2
            and type_name.endswith("]]")):
        return "System.ValueTuple<System.Int32, System.Int32>", "CLR value tuple uses a Java carrier"
    assert type_name in TYPES, (method_name, type_name)
    return TYPES[type_name], None


def main():
    surface = json.loads(SURFACE.read_text(encoding="utf-8"))
    assert surface["selectedTypeCount"] == 30
    record = next(item for item in surface["types"] if item["fullName"] == "System.Int32")
    upstream = [item for item in record["upstreamDeclaredSurface"]["methods"]
                if not item["isSpecialName"]]
    assert len(upstream) == 53
    declarations = record["javaCandidateDeclaredPublicDeclarations"]
    candidates = [item for declaration in declarations
                  if (item := java_method(declaration)) is not None]
    matched = set()
    results = []
    for method in upstream:
        return_type, adaptation = projected_type(method["returnType"], method["name"])
        adaptations = [adaptation] if adaptation else []
        if method["name"] == "CompareTo":
            return_type = "int"
            adaptations.append("CLR Int32 return uses a Java primitive")
        parameters = []
        for parameter in method["parameters"]:
            parameter_type, adaptation = projected_type(
                parameter["type"], method["name"], parameter["name"])
            parameters.append(parameter_type)
            if adaptation:
                adaptations.append(adaptation)
        expected = {
            "name": method["name"],
            "isStatic": method["isStatic"],
            "genericArity": method["genericArity"],
            "returnType": return_type,
            "parameters": parameters,
        }
        found = [item for item in candidates
                 if all(item[key] == value for key, value in expected.items())]
        assert len(found) <= 1, (method["signature"], found)
        if found:
            matched.add(found[0]["declaration"])
        results.append({
            "upstreamSignature": method["signature"],
            "projectedJava": expected,
            "candidateDeclaration": found[0]["declaration"] if found else None,
            "projectionAdaptations": sorted(set(adaptations)),
            "status": "PROJECTED_CANDIDATE" if found else "MISSING_PROJECTED_SIGNATURE",
        })
    extra_methods = [item["declaration"] for item in candidates
                     if item["declaration"] not in matched]
    missing = [item for item in results if item["candidateDeclaration"] is None]
    fields = record["upstreamDeclaredSurface"]["fields"]
    assert {field["name"] for field in fields} == {"MinValue", "MaxValue"}
    assert "public static final int MinValue;" in declarations
    assert "public static final int MaxValue;" in declarations
    output = {
        "schemaVersion": 1,
        "scope": "Declared public System.Int32 methods and fields in pinned CoreLib versus compiled Java candidate",
        "surfaceEvidence": SURFACE.name,
        "surfaceSha256": sha256(SURFACE),
        "upstreamMethodCount": len(upstream),
        "projectedCandidateMethodCount": len(results) - len(missing),
        "missingProjectedSignatureCount": len(missing),
        "extraJavaPublicMethodCount": len(extra_methods),
        "upstreamFields": fields,
        "extraJavaPublicMethods": extra_methods,
        "javaPublicConstructors": [item for item in declarations
                                   if item.startswith("public System.Int32(")],
        "methods": results,
        "status": "PROJECTION_AUDIT_ONLY; SPAN/BYREF/VALUE_TYPE_ABI, BEHAVIOR, E02 AND N01 OPEN",
        "limitation": "A projected declaration is a name/staticness/arity/type-shape match, not CLR semantic or JVM ABI equivalence. Extra Java methods include public interface bridges and carrier helpers.",
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"PASS Int32 signature audit: {len(results) - len(missing)}/53 projected; "
          f"{len(missing)} missing, {len(extra_methods)} extra Java public methods")


if __name__ == "__main__":
    main()
