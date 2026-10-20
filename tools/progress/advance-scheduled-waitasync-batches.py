"""Record one scheduled WaitAsync evidence batch on its own feature branch."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "planning/stage-2"
SCHEDULE = json.loads((STAGE / "implementation/WAITASYNC-27-POINTS.json").read_text(encoding="utf-8"))["batches"]
PLAN = "planning/stage-2/implementation/BATCH-PLAN-v3.json"
PROGRAM = "tools/oracle/dotj-core/task-behavior/Program.cs"
GATE = "tools/oracle/dotj-core/run-foundation-gate.py"
EVIDENCE = "planning/stage-2/repos/dotj-core/evidence/task-behavior-v10.0.12/oracle-output.json"


def run(*command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def advance(number):
    assert 225 <= number <= 249
    item = SCHEDULE[number - 224]
    next_item = SCHEDULE[number - 223]
    assert item["batch"] == f"Batch-{number:03d}"
    progress = json.loads((STAGE / "IMPLEMENTATION-PROGRESS.json").read_text(encoding="utf-8"))
    assert len(progress["completedBatches"]) == number - 1
    assert progress["nextProposedBatch"]["id"] == item["batch"]
    assert progress["batchPlan"]["version"] == "stage-2-batches-v3"

    branch = run("git", "branch", "--show-current")
    if branch == "master":
        assert not run("git", "status", "--porcelain"), "Master has uncommitted changes"
        branch = f"feature/batch-{number:03d}-waitasync-evidence"
        run("git", "switch", "-c", branch)
    else:
        assert number == 225 and branch.startswith("feature/batch-225-")
        assert run("git", "status", "--porcelain") == "?? tools/progress/advance-scheduled-waitasync-batches.py"

    print(run(sys.executable, "tools/oracle/dotj-core/append-waitasync-evidence.py", str(number)), flush=True)
    print(run(sys.executable, "tools/oracle/dotj-core/run-task-behavior-oracle.py"), flush=True)
    oracle = json.loads((ROOT / EVIDENCE).read_text(encoding="utf-8"))
    count = number - 193
    assert len(oracle["cases"]) == count and oracle["cases"][-1] == item["case"]

    files = [PROGRAM, GATE, EVIDENCE]
    if number == 225:
        files.append("tools/progress/advance-scheduled-waitasync-batches.py")
    report = f"planning/stage-2/implementation/batches/Batch-{number:03d}.md"
    run(sys.executable, "tools/progress/record-implementation-batch.py",
        "--plan-source", PLAN, str(number), "E03", item["outcome"],
        f"{count} selected Task/ValueTask reference cases passed on pinned CoreLib, including {item['case']}.",
        "This is a bounded .NET reference observation; Java timeout behavior and public Task.WaitAsync parity remain open.",
        "E03", next_item["outcome"], "One scheduled WaitAsync reference case and progress evidence.", *files)
    print(run(sys.executable, "tools/progress/verify-batch-plan.py"), flush=True)
    run("git", "add", *files, "planning/stage-2/IMPLEMENTATION-PROGRESS.json",
        "planning/stage-2/IMPLEMENTATION-STATE.md", report)
    run("git", "-c", "core.whitespace=cr-at-eol", "diff", "--cached", "--check")
    run("git", "commit", "-m", f"Batch {number}: record {item['case']}")
    run("git", "switch", "master")
    run("git", "merge", "--no-ff", branch, "-m", f"Merge {branch}")
    assert not run("git", "status", "--porcelain")
    print(f"MERGED {item['batch']} ({number - 223}/27): {item['case']}", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("batches", nargs="+", type=int)
    args = parser.parse_args()
    assert args.batches == list(range(args.batches[0], args.batches[-1] + 1))
    for number in args.batches:
        advance(number)


if __name__ == "__main__":
    main()
