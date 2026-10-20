"""Compile every pinned erased overload group with deterministic backend method names."""

import argparse
import hashlib
import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
PROBE = runpy.run_path(str(Path(__file__).with_name("verify-selected-method-java-declarations.py")))
COLLISIONS = EVIDENCE / "n01-java-erasure-collisions-v10.0.12.json"
SELECTED = EVIDENCE / "n01-selected-methods-v10.0.12.json"
REMAINING = EVIDENCE / "n01-remaining-methods-v10.0.12.json"
SELECTED_LEDGER = EVIDENCE / "n01-java-declarations-v10.0.12.json"
REMAINING_LEDGER = EVIDENCE / "n01-remaining-java-declarations-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-java-erasure-lowering-v10.0.12.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def backend_name(owner, method, signature):
    digest = hashlib.sha256((owner + "\0" + signature).encode("utf-8")).hexdigest()[:12]
    return method + "__dotj_" + digest


def group_source(owner, members, rename):
    package, simple = owner.rsplit(".", 1)
    imports = set()
    support = {}
    declarations = []
    for member in members:
        owner_name, declaration, source, stubs = PROBE["build_probe"](member["inventory"])
        if owner_name != owner or hashlib.sha256(source.encode("utf-8")).hexdigest() != member["ledger"]["generatedSourceSha256"]:
            raise ValueError("Pinned individual declaration drift")
        imports.update(re.findall(r"^import ([^;]+);$", source, re.M))
        for name, arity in stubs.items():
            if name in support and support[name] != arity:
                raise ValueError("Conflicting temporary support type arity")
            support[name] = arity
        if rename:
            name = member["inventory"]["name"]
            lowered = backend_name(owner, name, member["inventory"]["signature"])
            needle = " " + name + "("
            if declaration.count(needle) != 1:
                raise ValueError("Expected one declaration method name")
            declaration = declaration.replace(needle, " " + lowered + "(", 1)
        declarations.append(declaration)
    source = "package " + package + ";\n"
    source += "".join("import " + name + ";\n" for name in sorted(imports))
    source += "public abstract class " + simple + " {\n"
    source += "".join("    " + declaration + "\n" for declaration in declarations)
    source += "}\n"
    return source, support


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    selected = read(SELECTED)
    remaining = read(REMAINING)
    selected_ledger = read(SELECTED_LEDGER)
    remaining_ledger = read(REMAINING_LEDGER)
    collisions = read(COLLISIONS)
    if (len(selected["entries"]) != 99 or len(selected_ledger["entries"]) != 99 or
            len(remaining_ledger["entries"]) != 327 or len(collisions["collisions"]) != 12):
        raise ValueError("Complete pinned collision and method records required")
    methods = [dict(entry) for entry in selected["entries"]]
    methods += [dict(member, name=member["method"], batch=batch["batch"])
                for batch in remaining["batches"] for member in batch["members"]]
    ledgers = selected_ledger["entries"] + remaining_ledger["entries"]
    lookup = {(method["declaringType"], method["signature"]): {"inventory": method, "ledger": ledger}
              for method, ledger in zip(methods, ledgers)}
    if len(lookup) != 426:
        raise ValueError("Expected 426 unique pinned identities")
    outcomes = []
    all_names = set()
    for group in collisions["collisions"]:
        owner = group["declaringType"]
        members = []
        for row in group["members"]:
            member = lookup[(owner, row["metadataSignature"])]
            method = member["inventory"]
            source = args.source_root / method["owningSourcePath"]
            snapshot = ROOT / method["snapshot"]
            if sha256(source) != method["owningSourceSha256"] or sha256(snapshot) != method["snapshotSha256"]:
                raise ValueError("Pinned source or metadata hash drift: " + row["metadataSignature"])
            members.append(member)
        original, support = group_source(owner.replace("`1", "_1"), members, False)
        error = PROBE["compile_probe"](owner.replace("`1", "_1"), original, support)
        if not error or ("already defined" not in error and "name clash" not in error):
            raise ValueError("Expected original JVM erasure collision: " + str(error))
        lowered, support = group_source(owner.replace("`1", "_1"), members, True)
        if PROBE["compile_probe"](owner.replace("`1", "_1"), lowered, support) is not None:
            raise ValueError("Mapped overload group did not compile: " + owner + "." + group["method"])
        mappings = []
        for member in members:
            method = member["inventory"]
            backend = backend_name(owner.replace("`1", "_1"), method["name"], method["signature"])
            key = (owner, backend)
            if key in all_names:
                raise ValueError("Duplicate backend method name")
            all_names.add(key)
            mappings.append({"metadataSignature": method["signature"], "sourceBatch": method["batch"],
                             "backendName": backend, "sourceSha256": method["owningSourceSha256"],
                             "snapshotSha256": method["snapshotSha256"]})
        outcomes.append({"declaringType": owner, "method": group["method"],
                         "originalCompilerError": error, "mappedCompilerResult": "COMPILED",
                         "mappedSourceSha256": hashlib.sha256(lowered.encode("utf-8")).hexdigest(),
                         "members": mappings})
    if len(all_names) != 26:
        raise ValueError("Expected 26 unique mapped backend methods")
    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "sourceCommit": selected["sourceCommit"],
        "selectedLedgerSha256": sha256(SELECTED_LEDGER),
        "remainingLedgerSha256": sha256(REMAINING_LEDGER),
        "collisionAuditSha256": sha256(COLLISIONS),
        "collisionGroups": len(outcomes),
        "mappedMethods": len(all_names),
        "scope": "All twelve colliding groups compile with deterministic internal backend names. Source-level .j calls still require overload resolution and lowering; public Java API and behavior remain unqualified.",
        "groups": outcomes,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: all 12 pinned collision groups rejected unchanged and compiled with 26 unique backend names")


if __name__ == "__main__":
    main()
