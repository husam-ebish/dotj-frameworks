"""Run bounded WP-01/WP-02 local and pinned-reference checks."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path("R:/")
ORACLE = ROOT / "tools/oracle/dotj-core"
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
CORELIB_HASH = "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"


def run(*args, contains):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode or contains not in result.stdout:
        raise RuntimeError(f"Failed {args}: {result.returncode}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def gate():
    assert SOURCE.is_dir(), "Pinned source must be mapped to R:"
    wp01 = run("powershell", "-NoProfile", "-File", str(ORACLE / "run-wp01-fixtures.ps1"), contains="PASS: 9 Java fixtures and 5 .NET oracles")
    wp02 = run("powershell", "-NoProfile", "-File", str(ORACLE / "run-wp02-java-fixtures.ps1"), contains="PASS: 14 internal WP-02 Java fixtures")
    reference = json.loads(run("dotnet", "run", "--project", str(ORACLE / "cancellation-behavior/CancellationBehaviorOracle.csproj"), "--configuration", "Release", "--no-build", "--no-launch-profile", contains="\"runtimeVersion\""))
    assert reference["coreLibSha256"] == CORELIB_HASH and len(reference["cases"]) == 10
    assert reference == json.loads((EVIDENCE / "cancellation-behavior-v10.0.12/oracle-output.json").read_text(encoding="utf-8"))
    run("python", str(ORACLE / "verify-selected-api-shapes.py"), "--source-root", str(SOURCE), contains="PASS")
    run("python", str(ORACLE / "verify-wp02-api-shapes.py"), contains="PASS 7")
    run("python", str(ORACLE / "verify-wp02-test-map.py"), contains="PASS 10")
    run("python", str(ORACLE / "verify-wp02-java-names.py"), contains="PASS 3")
    run("powershell", "-NoProfile", "-File", str(ORACLE / "run-wp02-upstream-tests.ps1"), "-SourceRoot", str(SOURCE), contains="Passed:    10")
    upstream = json.loads((Path.home() / "AppData/Local/Temp/dotj-wp02-upstream-results/summary.json").read_text(encoding="utf-8-sig"))
    assert upstream["passed"] == 10 and upstream["sourceCommit"] == "4271d88e0aebf3d04f188f1334c2220d80555ef6"
    run("powershell", "-NoProfile", "-File", str(ORACLE / "build-internal-core.ps1"), contains="PASS: 8 internal sources and 8 classes")
    jar = ROOT / "dotj-core/dotj-core-01/build/dotj-core-internal-v1.jar"
    jar_hash = hashlib.sha256(jar.read_bytes()).hexdigest()
    jar_manifest = json.loads((EVIDENCE / "internal-core-jar-v1.json").read_text(encoding="utf-8-sig"))
    assert jar_manifest["jarSha256"] == jar_hash
    manifest = {
        "schemaVersion": 1,
        "sourceCommit": upstream["sourceCommit"],
        "runtimeVersion": "10.0.12",
        "coreLibSha256": CORELIB_HASH,
        "wp01JavaFixtures": 9,
        "wp01DotnetOracles": 5,
        "wp02InternalJavaFixtures": 14,
        "wp02ReferenceCases": 10,
        "wp02SelectedUpstreamTestsPassed": 10,
        "selectedApiShapePairs": 14,
        "internalJarSha256": jar_hash,
        "status": "BOUNDED_PASS; E01/E02/E03/N01 AND PUBLIC WP-01/WP-02 QUALIFICATION OPEN",
        "limitations": ["The internal cancellation implementation does not cover the full Task/ValueTask public semantics.", "Selected upstream tests and fixtures are not exhaustive concurrency or platform validation.", "No public .j facade or product release is qualified."],
    }
    output = EVIDENCE / "foundation-gate-v10.0.12.json"
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("PASS bounded foundation gate: WP-01 9+5, WP-02 14 Java + 10 upstream")


if __name__ == "__main__":
    gate()
