"""Compile a bounded source-call lowering for the pinned Task.FromException pair."""

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
OUTPUT = EVIDENCE / "n01-task-fromexception-call-lowering-v10.0.12.json"
SNAPSHOT = EVIDENCE / "wp02-api-shapes-v10.0.12/task.json"
SOURCE_RELATIVE = "src/libraries/System.Private.CoreLib/src/System/Threading/Tasks/Task.cs"
CALL = re.compile(r"Task\.(?:<(?P<type>[A-Za-z_$][A-Za-z0-9_$]*)>)?FromException\(exception\)\Z")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_java(root, name, source):
    path = root / (name.replace(".", "/") + ".java")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def lower(call, by_arity):
    match = CALL.fullmatch(call)
    if match is None:
        raise ValueError("Unsupported Task.FromException source-call shape")
    arity = 1 if match["type"] else 0
    backend = by_arity[arity]
    if arity:
        return "Task.<" + match["type"] + ">" + backend + "(exception)"
    return "Task." + backend + "(exception)"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    groups = [group for group in mapping["groups"]
              if group["declaringType"] == "System.Threading.Tasks.Task"
              and group["method"] == "FromException"]
    if len(groups) != 1 or len(groups[0]["members"]) != 2:
        raise ValueError("Expected pinned Task.FromException collision pair")
    members = groups[0]["members"]
    exact = {
        0: "System.Threading.Tasks.Task FromException(System.Exception)",
        1: "System.Threading.Tasks.Task`1[TResult] FromException[TResult](System.Exception)",
    }
    by_arity = {}
    source = args.source_root / SOURCE_RELATIVE
    if sha256(source) != members[0]["sourceSha256"] or sha256(SNAPSHOT) != members[0]["snapshotSha256"]:
        raise ValueError("Pinned source or metadata snapshot hash mismatch")
    for arity, signature in exact.items():
        member = next((item for item in members if item["metadataSignature"] == signature), None)
        if member is None or member["sourceSha256"] != members[0]["sourceSha256"]:
            raise ValueError("Pinned overload identity changed")
        digest = hashlib.sha256((groups[0]["declaringType"] + "\0" + signature).encode("utf-8")).hexdigest()[:12]
        expected = "FromException__dotj_" + digest
        if member["backendName"] != expected:
            raise ValueError("Backend name map drift")
        by_arity[arity] = expected
    calls = ["Task.FromException(exception)", "Task.<String>FromException(exception)"]
    lowered = [lower(call, by_arity) for call in calls]
    for invalid in ("Task.FromException(exception, exception)", "Task.<String>FromException()",
                    "Task.FromExceptionAsync(exception)"):
        try:
            lower(invalid, by_arity)
        except ValueError:
            pass
        else:
            raise ValueError("Unsupported source call was accepted: " + invalid)
    with tempfile.TemporaryDirectory(prefix="dotj-fromexception-calls-") as folder:
        root = Path(folder)
        files = [
            write_java(root, "System.Exception", "package System; public class Exception extends java.lang.Exception {}\n"),
            write_java(root, "System.Threading.Tasks.Task_1",
                       "package System.Threading.Tasks; public class Task_1<TResult> {}\n"),
            write_java(root, "System.Threading.Tasks.Task",
                       "package System.Threading.Tasks; import System.Exception; public class Task {\n"
                       + " public static Task " + by_arity[0] + "(Exception exception) { return null; }\n"
                       + " public static <TResult> Task_1<TResult> " + by_arity[1]
                       + "(Exception exception) { return null; }\n}\n"),
            write_java(root, "fixture.Consumer",
                       "package fixture; import System.Exception; import System.Threading.Tasks.Task;"
                       + " import System.Threading.Tasks.Task_1; class Consumer {"
                       + " static void call(Exception exception) { Task plain = " + lowered[0] + ";"
                       + " Task_1<String> generic = " + lowered[1] + "; } }\n"),
        ]
        output = root / "classes"
        output.mkdir()
        compiler = subprocess.run(["javac", "--release", "21", "-d", str(output),
                                   *(str(file) for file in files)], capture_output=True, text=True)
        if compiler.returncode or not (output / "fixture/Consumer.class").exists():
            raise RuntimeError("Lowered Java consumer did not compile: " + compiler.stderr)
    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "sourceCommit": mapping["sourceCommit"],
        "erasureMappingSha256": sha256(MAPPING),
        "sourcePath": SOURCE_RELATIVE,
        "sourceSha256": members[0]["sourceSha256"],
        "snapshotSha256": members[0]["snapshotSha256"],
        "sourceCalls": [{"source": call, "lowered": target} for call, target in zip(calls, lowered)],
        "invalidCallsRejected": 3,
        "consumerCompilation": "PASS: javac --release 21",
        "scope": "Bounded syntax proof for two Task.FromException calls after method generic arity is known. No .j compiler, general overload resolution, Task behavior, or public API qualification.",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: two pinned Task.FromException call forms lowered and compiled; three unsupported forms rejected")


if __name__ == "__main__":
    main()
