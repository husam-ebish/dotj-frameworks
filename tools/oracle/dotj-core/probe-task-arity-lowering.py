"""Compile a candidate JVM lowering for the two pinned Task arities."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
WORK = ROOT / "dotj-core/dotj-core-01/build/task-arity-lowering"
PACKAGE = "System.Threading.Tasks"


def run(*args):
    result = subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True)
    return result.stdout


def main():
    family = next(item for item in json.loads((EVIDENCE / "task-family-arity-v10.0.12.json").read_text(encoding="utf-8"))["families"]
                  if item["family"] == "Task")
    assert family["nonGeneric"] == "System.Threading.Tasks.Task"
    assert family["generic"] == "System.Threading.Tasks.Task`1"
    folder = WORK / "src/System/Threading/Tasks"
    folder.mkdir(parents=True, exist_ok=True)
    sources = {
        "Task.java": "package System.Threading.Tasks;\npublic class Task {}\n",
        "Task_1.java": "package System.Threading.Tasks;\npublic class Task_1<TResult> extends Task {}\n",
    }
    for name, content in sources.items():
        (folder / name).write_text(content, encoding="utf-8")
    classes = WORK / "classes"
    classes.mkdir(parents=True, exist_ok=True)
    run("javac", "--release", "21", "-d", str(classes),
        *(str(folder / name) for name in sources))
    compiled = {}
    for name in ("Task", "Task_1"):
        binary = PACKAGE + "." + name
        output = run("javap", "-classpath", str(classes), "-public", binary)
        assert f"class {binary}" in output or f"class {binary}<" in output
        path = classes / "System/Threading/Tasks" / f"{name}.class"
        compiled[binary] = {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "javap": output.strip(),
        }
    assert len(compiled) == 2 and len({item["sha256"] for item in compiled.values()}) == 2
    manifest = {
        "schemaVersion": 1,
        "sourceCommit": "4271d88e0aebf3d04f188f1334c2220d80555ef6",
        "upstreamIdentities": [family["nonGeneric"], family["generic"]],
        "candidateBackendNames": [PACKAGE + ".Task", PACKAGE + ".Task_1"],
        "compiled": compiled,
        "status": "COMPILE_ONLY_CANDIDATE; .j source-level arity resolution and exact public API comparison OPEN",
        "limitations": [
            "Task_1 is an internal backend name, not an approved public .j name.",
            "No .j compiler currently lowers Task<TResult> to this class or preserves both upstream identities.",
            "The empty classes establish only distinct JVM binary identities, not Task behavior or source-level compatibility.",
        ],
    }
    (EVIDENCE / "task-arity-lowering-candidate-v10.0.12.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("PASS compile-only Task arity lowering candidate: 2 distinct JVM binaries")


if __name__ == "__main__":
    main()
