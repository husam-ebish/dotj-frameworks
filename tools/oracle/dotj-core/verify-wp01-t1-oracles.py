"""Replay the bounded WP-01-T1 null and exception oracles."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence/wp01-t1-null-exception-oracle-v10.0.12.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    record = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert record["qualification"].endswith("PUBLIC_API QUALIFICATION OPEN")
    for oracle in record["oracles"]:
        project = ROOT / oracle["project"]
        source = project.with_name("Program.cs")
        assert sha256(source) == oracle["programSha256"]
        output = subprocess.run(
            ["dotnet", "run", "--project", str(project), "--configuration", "Release", "--no-launch-profile"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        if "type-identity" in oracle["project"]:
            values = dict(line.split("=", 1) for line in output.splitlines() if "=" in line)
            assert values["runtimeVersion"] == record["runtimeVersion"]
            assert values["nullTypeArgumentsParameter"] == oracle["observedParameter"]
        else:
            values = json.loads(output)
            assert values["runtimeVersion"] == record["runtimeVersion"]
            assert values["coreLibSha256"] == record["coreLibSha256"]
            assert values["disposeFailureSameReference"] is oracle["disposeFailureSameReference"]
            assert values["disposeCauseSameReference"] is oracle["disposeCauseSameReference"]
            assert values["disposeFailureObserved"] == oracle["observedMessage"]
    print("PASS pinned WP-01-T1 null and exception oracle replay")


if __name__ == "__main__":
    main()
