"""Compile one consumer of every pinned erased-overload backend mapping."""

import argparse
import hashlib
import json
import re
import runpy
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
SELECTED = EVIDENCE / "n01-selected-methods-v10.0.12.json"
REMAINING = EVIDENCE / "n01-remaining-methods-v10.0.12.json"
SELECTED_LEDGER = EVIDENCE / "n01-java-declarations-v10.0.12.json"
REMAINING_LEDGER = EVIDENCE / "n01-remaining-java-declarations-v10.0.12.json"
LOWERING = EVIDENCE / "n01-java-erasure-lowering-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-all-erasure-call-resolution-v10.0.12.json"
PROBE = runpy.run_path(str(Path(__file__).with_name("verify-selected-method-java-declarations.py")))


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_java(root, name, source):
    path = root / (name.replace(".", "/") + ".java")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def concrete(metadata):
    return metadata.replace("TResult", "System.String")


def exact_candidate(group, sought_arity, sought_parameters, inventory):
    matches = []
    for row in group["members"]:
        candidate = inventory[(group["declaringType"], row["metadataSignature"])]
        if (candidate["genericArity"] == sought_arity and
                [concrete(item["type"]) for item in candidate["parameters"]] == sought_parameters):
            matches.append(row)
    if len(matches) != 1:
        raise ValueError("Exact fixture overload did not resolve uniquely: " + group["method"])
    return matches[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    selected = read(SELECTED)
    remaining = read(REMAINING)
    selected_ledger = read(SELECTED_LEDGER)
    remaining_ledger = read(REMAINING_LEDGER)
    lowering = read(LOWERING)
    methods = selected["entries"] + [dict(member, name=member["method"], batch=batch["batch"])
                                     for batch in remaining["batches"] for member in batch["members"]]
    ledgers = selected_ledger["entries"] + remaining_ledger["entries"]
    inventory = {(method["declaringType"], method["signature"]): method for method in methods}
    probes = {(entry["declaringType"], entry["metadataSignature"]): entry for entry in ledgers}
    if (len(inventory) != 426 or len(probes) != 426 or len(lowering["groups"]) != 12 or
            sum(len(group["members"]) for group in lowering["groups"]) != 26):
        raise ValueError("Expected complete pinned method and erasure inventories")
    owner_declarations = {"Task": [], "ValueTask": []}
    owner_imports = {"Task": set(), "ValueTask": set()}
    support = {}
    consumer_support = {}
    calls = []
    variables = []
    for group in lowering["groups"]:
        owner = group["declaringType"]
        simple = owner.rsplit(".", 1)[-1]
        if simple not in owner_declarations:
            raise ValueError("Unexpected erased overload owner")
        for row in group["members"]:
            key = (owner, row["metadataSignature"])
            method = inventory[key]
            observed = probes[key]
            source = args.source_root / method["owningSourcePath"]
            snapshot = ROOT / method["snapshot"]
            if (sha256(source) != method["owningSourceSha256"] or
                    sha256(snapshot) != method["snapshotSha256"] or
                    row["sourceSha256"] != method["owningSourceSha256"] or
                    row["snapshotSha256"] != method["snapshotSha256"]):
                raise ValueError("Pinned source or metadata drift: " + method["signature"])
            owner_name, declaration, generated, stubs = PROBE["build_probe"](method)
            if (owner_name != owner or
                    hashlib.sha256(generated.encode("utf-8")).hexdigest() != observed["generatedSourceSha256"]):
                raise ValueError("Individual Java probe drift: " + method["signature"])
            expected_name = method["name"] + "__dotj_" + hashlib.sha256(
                (owner + "\0" + method["signature"]).encode("utf-8")).hexdigest()[:12]
            if row["backendName"] != expected_name:
                raise ValueError("Backend method mapping drift")
            needle = " " + method["name"] + "("
            if declaration.count(needle) != 1:
                raise ValueError("Expected one Java method declaration name")
            owner_declarations[simple].append(declaration.replace(needle, " " + expected_name + "(", 1))
            owner_imports[simple].update(re.findall(r"^import ([^;]+);$", generated, re.M))
            for name, arity in stubs.items():
                if name in support and support[name] != arity:
                    raise ValueError("Conflicting support type arity")
                support[name] = arity
            parameter_types = [concrete(item["type"]) for item in method["parameters"]]
            if exact_candidate(group, method["genericArity"], parameter_types, inventory) != row:
                raise ValueError("Exact fixture resolved a different overload")
            argument_names = []
            for position, parameter in enumerate(parameter_types):
                argument_name = "arg" + str(len(calls)) + "_" + str(position)
                argument_type = PROBE["convert_type"](parameter, set(), consumer_support)
                variables.append(" " + argument_type + " " + argument_name + " = null;")
                argument_names.append(argument_name)
            generic = ".<String>" if method["genericArity"] else "."
            arguments = ", ".join(argument_names)
            source_call = simple + generic + method["name"] + "(" + arguments + ")"
            lowered_call = simple + generic + expected_name + "(" + arguments + ")"
            result_type = PROBE["convert_type"](concrete(method["returnType"]), set(), consumer_support)
            variables.append(" " + result_type + " result" + str(len(calls)) + " = " + lowered_call + ";")
            calls.append({"declaringType": owner, "metadataSignature": method["signature"],
                          "sourceCall": source_call, "loweredCall": lowered_call,
                          "backendName": expected_name})
    if len(calls) != 26 or len({item["backendName"] for item in calls}) != 26:
        raise ValueError("Expected 26 distinct lowered source calls")
    for name, arity in consumer_support.items():
        if name in support and support[name] != arity:
            raise ValueError("Consumer support arity conflicts with declaration support")
        support[name] = arity
    with tempfile.TemporaryDirectory(prefix="dotj-all-erasure-calls-") as folder:
        root = Path(folder)
        files = []
        for owner, declarations in owner_declarations.items():
            source = "package System.Threading.Tasks;\n"
            source += "".join("import " + name + ";\n" for name in sorted(owner_imports[owner]))
            source += "public abstract class " + owner + " {\n"
            source += "\n".join("    " + declaration for declaration in declarations) + "\n}\n"
            files.append(write_java(root, "System.Threading.Tasks." + owner, source))
        for name, arity in sorted(support.items()):
            if name in ("System.Threading.Tasks.Task", "System.Threading.Tasks.ValueTask"):
                continue
            package, simple = name.rsplit(".", 1)
            generic = "<" + ", ".join("T" + str(index) for index in range(arity)) + ">" if arity else ""
            files.append(write_java(root, name, "package " + package + "; public class " + simple + generic + " {}\n"))
        imports = set(consumer_support) | {"System.Threading.Tasks.Task", "System.Threading.Tasks.ValueTask"}
        consumer = "package fixture;\n"
        consumer += "".join("import " + name + ";\n" for name in sorted(imports))
        consumer += "public class Consumer { static void call() {\n"
        consumer += "\n".join(variables) + "\n} }\n"
        files.append(write_java(root, "fixture.Consumer", consumer))
        output = root / "classes"
        output.mkdir()
        result = subprocess.run(["javac", "--release", "21", "-d", str(output),
                                 *(str(file) for file in files)], capture_output=True, text=True)
        if result.returncode or not (output / "fixture/Consumer.class").is_file():
            raise RuntimeError("Combined 26-call Java consumer failed: " + result.stderr)
    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "sourceCommit": lowering["sourceCommit"],
        "selectedLedgerSha256": sha256(SELECTED_LEDGER),
        "remainingLedgerSha256": sha256(REMAINING_LEDGER),
        "erasureLoweringSha256": sha256(LOWERING),
        "collisionGroups": len(lowering["groups"]),
        "sourceCallsCompiled": len(calls),
        "consumerCompilation": "PASS: javac --release 21",
        "scope": "Exact-type fixture selection and combined backend-call syntax only; no general .j overload resolution, Task/ValueTask behavior, or public API qualification.",
        "calls": calls,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: exact-type selection and combined compilation for all 26 erased-overload calls")


if __name__ == "__main__":
    main()
