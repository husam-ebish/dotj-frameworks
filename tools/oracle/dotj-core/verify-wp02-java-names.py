"""Compile exact-name cancellation declarations as syntax-only probes."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tools/oracle/dotj-core/java-probes/System/Threading"
OUTPUT = ROOT / "dotj-core/dotj-core-01/build/name-probes"
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence/wp02-java-name-probe-v10.0.12.json"
NAMES = ("CancellationToken", "CancellationTokenSource", "CancellationTokenRegistration")


def verify():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    subprocess.run(["javac", "-d", str(OUTPUT), *[str(SOURCE / f"{name}.java") for name in NAMES]], check=True, cwd=ROOT)
    bytecode = {}
    for name in NAMES:
        full_name = "System.Threading." + name
        output = subprocess.check_output(["javap", "-public", "-classpath", str(OUTPUT), full_name], text=True, cwd=ROOT)
        assert f"public final class {full_name}" in output
        bytecode[full_name] = output.strip()
    EVIDENCE.write_text(json.dumps({"schemaVersion": 1, "runtimeProfile": "10.0.12", "compiledNames": list(bytecode), "javap": bytecode, "status": "SYNTAX_ONLY; empty oracle stubs are not product API or behavior"}, indent=2) + "\n", encoding="utf-8")
    return bytecode


if __name__ == "__main__":
    print(f"PASS {len(verify())} exact-name cancellation Java syntax probes")
