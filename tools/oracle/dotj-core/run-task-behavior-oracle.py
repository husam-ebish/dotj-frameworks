"""Run selected Task/ValueTask reference assertions against the pinned CoreLib."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "tools/oracle/dotj-core/task-behavior/TaskBehaviorOracle.csproj"
OUTPUT = ROOT / "planning/stage-2/repos/dotj-core/evidence/task-behavior-v10.0.12/oracle-output.json"
CORELIB = "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"


def main():
    result = subprocess.run(["dotnet", "run", "--project", str(PROJECT), "--configuration", "Release",
                             "--no-launch-profile"], cwd=ROOT, capture_output=True, text=True, check=True)
    lines = [line for line in result.stdout.splitlines() if line.startswith("{") and line.endswith("}")]
    assert lines, result.stdout + result.stderr
    record = json.loads(lines[-1])
    assert record["runtimeVersion"] == "10.0.12"
    assert record["coreLibSha256"] == CORELIB
    assert len(record["cases"]) == len(set(record["cases"]))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"PASS {len(record['cases'])} selected Task/ValueTask reference cases on pinned CoreLib")


if __name__ == "__main__":
    main()
