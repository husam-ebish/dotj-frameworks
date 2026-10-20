"""Demonstrate one Java binary-name collision for a pinned async type pair."""

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
PACKAGE = "System.Threading.Tasks"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("family", choices=("Task", "TaskCompletionSource", "ValueTask"))
    args = parser.parse_args()
    ledger = json.loads((EVIDENCE / "task-family-arity-v10.0.12.json").read_text(encoding="utf-8"))
    family = next(item for item in ledger["families"] if item["family"] == args.family)
    assert family["nonGeneric"] == PACKAGE + "." + args.family
    assert family["generic"] == family["nonGeneric"] + "`1"
    work = ROOT / "dotj-core/dotj-core-01/build/java-name-collisions" / args.family
    sources = []
    for arity, declaration in ((0, f"public class {args.family} {{}}"),
                               (1, f"public class {args.family}<TResult> {{}}")):
        path = work / str(arity) / "System/Threading/Tasks" / f"{args.family}.java"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"package {PACKAGE};\n{declaration}\n", encoding="utf-8")
        sources.append(path)
    result = subprocess.run(["javac", "--release", "21", "-d", str(work / "classes"),
                             *(str(path) for path in sources)], cwd=ROOT, capture_output=True, text=True)
    diagnostic = result.stdout + result.stderr
    assert result.returncode != 0 and "duplicate class: " + PACKAGE + "." + args.family in diagnostic, diagnostic
    output = {
        "schemaVersion": 1,
        "upstreamNonGeneric": family["nonGeneric"],
        "upstreamGeneric": family["generic"],
        "javaPackage": PACKAGE,
        "javaSimpleName": args.family,
        "javacExitCode": result.returncode,
        "expectedDiagnostic": "duplicate class: " + PACKAGE + "." + args.family,
        "conclusion": "Two separate exact-name top-level Java declarations cannot coexist in one package",
        "scope": "Syntax feasibility probe only; no public representation or behavioral equivalence selected",
    }
    path = EVIDENCE / f"java-name-collision-{args.family.lower()}-v10.0.12.json"
    path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print("PASS expected Java name collision:", args.family)


if __name__ == "__main__":
    main()
