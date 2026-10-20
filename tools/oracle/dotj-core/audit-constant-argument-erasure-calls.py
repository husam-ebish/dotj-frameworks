"""Check bounded Task/ValueTask constant-argument overload call lowering."""

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
MAPPING = EVIDENCE / "n01-java-erasure-lowering-v10.0.12.json"
SELECTED = EVIDENCE / "n01-selected-methods-v10.0.12.json"
REMAINING = EVIDENCE / "n01-remaining-methods-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-constant-argument-erasure-calls-v10.0.12.json"
CALL = re.compile(r"(?P<owner>Task|ValueTask)\.(?:<(?P<generic>String)>)?"
                  r"(?P<method>FromException|FromCanceled)\((?P<argument>exception|token)\)\Z")
ARGUMENT = {"FromException": ("exception", "System.Exception"),
            "FromCanceled": ("token", "System.Threading.CancellationToken")}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_java(root, name, source):
    path = root / (name.replace(".", "/") + ".java")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def lower(call, backend):
    match = CALL.fullmatch(call)
    if match is None or match["argument"] != ARGUMENT[match["method"]][0]:
        raise ValueError("Unsupported or mistyped bounded source call")
    arity = 1 if match["generic"] else 0
    name = backend[(match["owner"], match["method"], arity)]
    prefix = match["owner"] + (".<String>" if arity else ".")
    return prefix + name + "(" + match["argument"] + ")"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    mapping = read(MAPPING)
    selected = read(SELECTED)
    remaining = read(REMAINING)
    inventories = selected["entries"] + [member for batch in remaining["batches"] for member in batch["members"]]
    identities = {(item["declaringType"], item["signature"]): item for item in inventories}
    if len(identities) != 426:
        raise ValueError("Expected complete distinct method inventory")
    groups = [group for group in mapping["groups"]
              if group["declaringType"] in ("System.Threading.Tasks.Task", "System.Threading.Tasks.ValueTask")
              and group["method"] in ARGUMENT]
    if len(groups) != 4:
        raise ValueError("Expected four pinned constant-argument erasure groups")
    backend = {}
    verified = []
    for group in groups:
        owner = group["declaringType"]
        simple = owner.rsplit(".", 1)[-1]
        method = group["method"]
        _, parameter_type = ARGUMENT[method]
        if len(group["members"]) != 2:
            raise ValueError("Expected plain and generic overloads")
        for arity in (0, 1):
            return_type = owner + ("`1[TResult]" if arity else "")
            generic = "[TResult]" if arity else ""
            signature = f"{return_type} {method}{generic}({parameter_type})"
            member = next((item for item in group["members"] if item["metadataSignature"] == signature), None)
            identity = identities.get((owner, signature))
            if member is None or identity is None:
                raise ValueError("Pinned overload identity missing: " + signature)
            source = args.source_root / identity["owningSourcePath"]
            snapshot = ROOT / identity["snapshot"]
            if (sha256(source) != identity["owningSourceSha256"] or
                    sha256(snapshot) != identity["snapshotSha256"] or
                    member["sourceSha256"] != identity["owningSourceSha256"] or
                    member["snapshotSha256"] != identity["snapshotSha256"]):
                raise ValueError("Pinned source or metadata hash drift: " + signature)
            expected = method + "__dotj_" + hashlib.sha256((owner + "\0" + signature).encode()).hexdigest()[:12]
            if member["backendName"] != expected:
                raise ValueError("Backend name map drift: " + signature)
            backend[(simple, method, arity)] = expected
            verified.append({"metadataSignature": signature, "backendName": expected,
                             "sourceSha256": identity["owningSourceSha256"],
                             "snapshotSha256": identity["snapshotSha256"]})
    calls = []
    for owner in ("Task", "ValueTask"):
        for method in ARGUMENT:
            argument = ARGUMENT[method][0]
            for arity in (0, 1):
                source = owner + (".<String>" if arity else ".") + method + "(" + argument + ")"
                calls.append({"source": source, "lowered": lower(source, backend),
                              "resultType": owner + ("_1<String>" if arity else "")})
    for invalid in ("Task.FromException(token)", "ValueTask.FromCanceled(exception)",
                    "Task.<String>FromCanceled(exception)", "ValueTask.FromException()"):
        try:
            lower(invalid, backend)
        except ValueError:
            pass
        else:
            raise ValueError("Mistyped or unsupported call was accepted: " + invalid)
    with tempfile.TemporaryDirectory(prefix="dotj-constant-overloads-") as folder:
        root = Path(folder)
        files = [
            write_java(root, "System.Exception", "package System; public class Exception extends java.lang.Exception {}\n"),
            write_java(root, "System.Threading.CancellationToken",
                       "package System.Threading; public class CancellationToken {}\n"),
        ]
        for owner in ("Task", "ValueTask"):
            files.append(write_java(root, "System.Threading.Tasks." + owner + "_1",
                                    "package System.Threading.Tasks; public class " + owner + "_1<TResult> {}\n"))
            declarations = []
            for method, (_, parameter_type) in ARGUMENT.items():
                parameter = parameter_type.rsplit(".", 1)[-1]
                for arity in (0, 1):
                    result = owner + ("_1<TResult>" if arity else "")
                    generic = "<TResult> " if arity else ""
                    declarations.append(" public static " + generic + result + " " + backend[(owner, method, arity)]
                                        + "(" + parameter + " value) { return null; }")
            source = ("package System.Threading.Tasks; import System.Exception;"
                      " import System.Threading.CancellationToken; public class " + owner + " {\n"
                      + "\n".join(declarations) + "\n}\n")
            files.append(write_java(root, "System.Threading.Tasks." + owner, source))
        assignments = [" " + item["resultType"] + " result" + str(index) + " = " + item["lowered"] + ";"
                       for index, item in enumerate(calls)]
        consumer = ("package fixture; import System.Exception; import System.Threading.CancellationToken;"
                    " import System.Threading.Tasks.Task; import System.Threading.Tasks.Task_1;"
                    " import System.Threading.Tasks.ValueTask; import System.Threading.Tasks.ValueTask_1;"
                    " class Consumer { static void call(Exception exception, CancellationToken token) {"
                    + "".join(assignments) + " } }\n")
        files.append(write_java(root, "fixture.Consumer", consumer))
        output = root / "classes"
        output.mkdir()
        result = subprocess.run(["javac", "--release", "21", "-d", str(output),
                                 *(str(file) for file in files)], capture_output=True, text=True)
        if result.returncode or not (output / "fixture/Consumer.class").is_file():
            raise RuntimeError("Eight-call Java consumer did not compile: " + result.stderr)
    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "sourceCommit": mapping["sourceCommit"],
        "erasureMappingSha256": sha256(MAPPING),
        "groups": len(groups),
        "identities": verified,
        "sourceCalls": calls,
        "mistypedCallsRejected": 4,
        "consumerCompilation": "PASS: javac --release 21",
        "scope": "Eight bounded call-shape compilations after generic arity is known. No production .j compiler, general overload resolution, behavior, or public API qualification.",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: eight Task/ValueTask FromException/FromCanceled calls lowered and compiled")


if __name__ == "__main__":
    main()
