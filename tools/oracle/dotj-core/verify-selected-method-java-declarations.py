"""Compile bounded Java declaration probes for pinned .NET method metadata.

Generated support types and method bodies are temporary syntax probes, never product APIs.
"""

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
SOURCE = EVIDENCE / "n01-selected-methods-v10.0.12.json"
LEDGER = EVIDENCE / "n01-java-declarations-v10.0.12.json"
PRIMITIVES = {"System.Boolean": "boolean", "System.Int32": "int", "System.Void": "void"}
IDENTIFIER = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*\Z")
TYPE = re.compile(r"(?P<base>[A-Za-z_$][A-Za-z0-9_.$]*)(?:`(?P<arity>[0-9]+)(?:\[(?P<arguments>.*)\])?)?\Z")


def split_arguments(text):
    parts = []
    start = depth = 0
    for position, character in enumerate(text):
        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
            if depth < 0:
                raise ValueError("Unbalanced metadata type arguments")
        elif character == "," and depth == 0:
            parts.append(text[start:position])
            start = position + 1
    if depth:
        raise ValueError("Unbalanced metadata type arguments")
    parts.append(text[start:])
    return [part.strip() for part in parts]


def convert_type(metadata, type_parameters, support, generic_argument=False):
    if metadata.endswith("[]"):
        return convert_type(metadata[:-2], type_parameters, support) + "[]"
    if metadata in PRIMITIVES:
        if generic_argument and metadata != "System.Void":
            support[metadata] = 0
            return metadata.rsplit(".", 1)[-1]
        return PRIMITIVES[metadata]
    if metadata in type_parameters:
        return metadata
    match = TYPE.fullmatch(metadata)
    if not match or not match["base"].startswith("System."):
        raise ValueError("Unsupported metadata type: " + metadata)
    base = match["base"]
    arity = int(match["arity"]) if match["arity"] else 0
    arguments = split_arguments(match["arguments"]) if match["arguments"] else []
    if len(arguments) != arity:
        raise ValueError("Unsupported metadata arity: " + metadata)
    backend = base + ("_" + str(arity) if arity else "")
    support[backend] = arity
    simple = backend.rsplit(".", 1)[-1]
    if arguments:
        simple += "<" + ", ".join(convert_type(arg, type_parameters, support, True) for arg in arguments) + ">"
    return simple


def method_parameters(entry):
    if not entry["genericArity"]:
        return []
    head = entry["signature"].split("(", 1)[0].rsplit(" ", 1)[-1]
    prefix = entry["name"] + "["
    if not head.startswith(prefix) or not head.endswith("]"):
        raise ValueError("Generic method metadata does not match its name")
    names = split_arguments(head[len(prefix):-1])
    if len(names) != entry["genericArity"] or not all(IDENTIFIER.fullmatch(name) for name in names):
        raise ValueError("Unsupported generic method parameter list")
    return names


def build_probe(entry):
    owner = TYPE.fullmatch(entry["declaringType"])
    if not owner or owner["arguments"] is not None:
        raise ValueError("Unexpected declaring type metadata")
    owner_arity = int(owner["arity"]) if owner["arity"] else 0
    if owner_arity > 1:
        raise ValueError("Unsupported declaring type arity")
    owner_name = owner["base"] + ("_1" if owner_arity else "")
    owner_package, owner_simple = owner_name.rsplit(".", 1)
    class_parameters = (["T"] if owner["base"] == "System.Threading.AsyncLocal" else ["TResult"]) if owner_arity else []
    generic_method_parameters = method_parameters(entry)
    all_parameters = set(class_parameters + generic_method_parameters)
    if len(all_parameters) != len(class_parameters) + len(generic_method_parameters):
        raise ValueError("Duplicate generic parameter identity")
    support = {}
    return_type = convert_type(entry["returnType"], all_parameters, support)
    arguments = []
    for parameter in entry["parameters"]:
        if parameter["IsOut"] or parameter["IsOptional"]:
            raise ValueError("By-reference or optional parameter needs separate representation")
        name = parameter["Name"]
        if not IDENTIFIER.fullmatch(name):
            raise ValueError("Unsupported parameter name: " + repr(name))
        arguments.append(convert_type(parameter["type"], all_parameters, support) + " " + name)
    if not IDENTIFIER.fullmatch(entry["name"]):
        raise ValueError("Unsupported method name")
    imported = sorted(name for name in support if name.rsplit(".", 1)[0] != owner_package and name != owner_name)
    simple_names = {}
    for name in imported:
        simple = name.rsplit(".", 1)[-1]
        if simple in simple_names and simple_names[simple] != name:
            raise ValueError("Conflicting Java import name: " + simple)
        if simple == owner_simple:
            raise ValueError("Imported type conflicts with owning declaration")
        simple_names[simple] = name
    # Java static members cannot capture their owning class's type parameter.
    # Lift that parameter to the Java method for a compilable backend shape.
    # This is a lowering candidate, not an exact public metadata identity.
    java_method_parameters = (class_parameters if entry["isStatic"] else []) + generic_method_parameters
    generic_prefix = "<" + ", ".join(java_method_parameters) + "> " if java_method_parameters else ""
    declaration = ("public static " if entry["isStatic"] else "public abstract ") + generic_prefix + return_type
    declaration += " " + entry["name"] + "(" + ", ".join(arguments) + ")"
    declaration += " { throw new UnsupportedOperationException(); }" if entry["isStatic"] else ";"
    class_suffix = "<" + class_parameters[0] + ">" if owner_arity else ""
    source = "package " + owner_package + ";\n"
    source += "".join("import " + name + ";\n" for name in imported)
    source += "public abstract class " + owner_simple + class_suffix + " {\n    " + declaration + "\n}\n"
    support.pop(owner_name, None)
    return owner_name, declaration, source, support


def java_file(root, name, source):
    path = root / (name.replace(".", "/") + ".java")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def compile_probe(owner_name, source, support):
    with tempfile.TemporaryDirectory(prefix="dotj-n01-method-") as directory:
        root = Path(directory)
        files = [java_file(root, owner_name, source)]
        for name, arity in sorted(support.items()):
            package, simple = name.rsplit(".", 1)
            suffix = "<" + ", ".join("T" + str(i) for i in range(1, arity + 1)) + ">" if arity else ""
            files.append(java_file(root, name, "package " + package + "; public class " + simple + suffix + " {}\n"))
        output = root / "classes"
        output.mkdir()
        result = subprocess.run(["javac", "--release", "21", "-d", str(output),
                                 *(str(path) for path in files)], capture_output=True, text=True)
        if result.returncode:
            diagnostic = re.search(r"error: ([^\r\n]+)", result.stderr)
            if not diagnostic:
                raise RuntimeError("Unclassified javac failure for " + owner_name + ": " + result.stderr)
            return diagnostic.group(1)
        class_file = output / (owner_name.replace(".", "/") + ".class")
        if not class_file.is_file():
            raise RuntimeError("javac did not emit the owning class")
        return None


def verify_one(index, entry, source_root):
    source_path = source_root / entry["owningSourcePath"]
    if hashlib.sha256(source_path.read_bytes()).hexdigest() != entry["owningSourceSha256"]:
        raise ValueError("Pinned owning source hash mismatch")
    snapshot = ROOT / entry["snapshot"]
    if hashlib.sha256(snapshot.read_bytes()).hexdigest() != entry["snapshotSha256"]:
        raise ValueError("Pinned metadata snapshot hash mismatch")
    owner, declaration, source, support = build_probe(entry)
    compiler_error = compile_probe(owner, source, support)
    return {
        "index": index,
        "sourceBatch": entry["batch"],
        "declaringType": entry["declaringType"],
        "metadataSignature": entry["signature"],
        "backendOwner": owner,
        "javaDeclaration": declaration,
        "generatedSourceSha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "supportTypes": sorted(support),
        "result": "JAVA_DECLARATION_COMPILED; BEHAVIOR_UNVERIFIED" if compiler_error is None else
                  "BLOCKED_JAVA_DECLARATION; BEHAVIOR_UNVERIFIED",
        "compilerError": compiler_error
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preview-all", action="store_true")
    mode.add_argument("--append-index", type=int)
    mode.add_argument("--verify-ledger", action="store_true")
    args = parser.parse_args()
    selected = json.loads(SOURCE.read_text(encoding="utf-8"))
    entries = selected["entries"]
    if len(entries) != 99:
        raise ValueError("Expected 99 pinned selected method records")
    if args.preview_all:
        blocked = []
        for index, entry in enumerate(entries, 1):
            result = verify_one(index, entry, args.source_root)
            if result["compilerError"]:
                blocked.append((index, result["compilerError"]))
        print(f"PASS: {99 - len(blocked)} selected .NET method declarations compile; {len(blocked)} explicit Java blockers")
        for index, error in blocked:
            print(f"BLOCKED {index}: {error}")
        return
    ledger = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {
        "schemaVersion": 1, "sourceCommit": selected["sourceCommit"],
        "coreLibSha256": selected["coreLibSha256"], "selectedMethodCount": 99,
        "scope": "Compile-only Java declaration feasibility with temporary support stubs; no method behavior or public facade qualification",
        "entries": []}
    if ledger["sourceCommit"] != selected["sourceCommit"] or ledger["selectedMethodCount"] != 99:
        raise ValueError("Ledger baseline mismatch")
    if args.append_index:
        index = args.append_index
        if index < 1 or index > 99 or len(ledger["entries"]) != index - 1:
            raise ValueError("Method append must be sequential")
        result = verify_one(index, entries[index - 1], args.source_root)
        result["batch"] = "Batch-" + str(index + 767)
        ledger["entries"].append(result)
        LEDGER.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
        state = "BLOCKED" if result["compilerError"] else "COMPILED"
        print(f"{state} selected method {index}/99: {result['backendOwner']}.{entries[index - 1]['name']}")
    else:
        for index, observed in enumerate(ledger["entries"], 1):
            expected = verify_one(index, entries[index - 1], args.source_root)
            if observed != {**expected, "batch": "Batch-" + str(index + 767)}:
                raise ValueError("Method ledger entry drift at index " + str(index))
        print(f"PASS: {len(ledger['entries'])}/99 selected method declarations and source hashes")


if __name__ == "__main__":
    main()
