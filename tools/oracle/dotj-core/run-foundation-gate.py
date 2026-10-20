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
    wp01 = run("powershell", "-NoProfile", "-File", str(ORACLE / "run-wp01-fixtures.ps1"), contains="PASS: 12 Java fixtures and 5 .NET oracles")
    wp02 = run("powershell", "-NoProfile", "-File", str(ORACLE / "run-wp02-java-fixtures.ps1"), contains="PASS: 15 internal WP-02 Java fixtures")
    run("powershell", "-NoProfile", "-File", str(ORACLE / "run-async-java-fixtures.ps1"),
        contains="PASS: 200 internal async success/fault/cancel races")
    reference = json.loads(run("dotnet", "run", "--project", str(ORACLE / "cancellation-behavior/CancellationBehaviorOracle.csproj"), "--configuration", "Release", "--no-build", "--no-launch-profile", contains="\"runtimeVersion\""))
    assert reference["coreLibSha256"] == CORELIB_HASH and len(reference["cases"]) == 10
    assert reference == json.loads((EVIDENCE / "cancellation-behavior-v10.0.12/oracle-output.json").read_text(encoding="utf-8"))
    run("python", str(ORACLE / "verify-selected-api-shapes.py"), "--source-root", str(SOURCE), contains="PASS")
    run("python", str(ORACLE / "verify-wp02-api-shapes.py"), contains="PASS 7")
    run("python", str(ORACLE / "verify-wp02-test-map.py"), contains="PASS 10")
    run("python", str(ORACLE / "verify-wp02-java-names.py"), contains="PASS 3")
    run("python", str(ORACLE / "verify-task-family-arity.py"), "--source-root", str(SOURCE), contains="PASS 3 pinned async family arity pairs")
    for family in ("Task", "TaskCompletionSource", "ValueTask"):
        run("python", str(ORACLE / "verify-async-java-name-collision.py"), family,
            contains=f"PASS expected Java name collision: {family}")
    run("python", str(ORACLE / "run-task-behavior-oracle.py"),
        contains="PASS 25 selected Task/ValueTask reference cases on pinned CoreLib")
    task_reference = json.loads((EVIDENCE / "task-behavior-v10.0.12/oracle-output.json").read_text(encoding="utf-8"))
    assert task_reference["coreLibSha256"] == CORELIB_HASH and len(task_reference["cases"]) == 25
    run("powershell", "-NoProfile", "-File", str(ORACLE / "run-wp02-upstream-tests.ps1"), "-SourceRoot", str(SOURCE), contains="Passed:    10")
    upstream = json.loads((Path.home() / "AppData/Local/Temp/dotj-wp02-upstream-results/summary.json").read_text(encoding="utf-8-sig"))
    assert upstream["passed"] == 10 and upstream["sourceCommit"] == "4271d88e0aebf3d04f188f1334c2220d80555ef6"
    run("powershell", "-NoProfile", "-File", str(ORACLE / "build-internal-core.ps1"), contains="PASS: 11 internal sources and 11 classes")
    jar = ROOT / "dotj-core/dotj-core-01/build/dotj-core-internal-v1.jar"
    jar_hash = hashlib.sha256(jar.read_bytes()).hexdigest()
    jar_manifest = json.loads((EVIDENCE / "internal-core-jar-v1.json").read_text(encoding="utf-8-sig"))
    assert jar_manifest["jarSha256"] == jar_hash
    manifest = {
        "schemaVersion": 1,
        "sourceCommit": upstream["sourceCommit"],
        "runtimeVersion": "10.0.12",
        "coreLibSha256": CORELIB_HASH,
        "wp01JavaFixtures": 12,
        "wp01DotnetOracles": 5,
        "wp02InternalJavaFixtures": 15,
        "wp02ReferenceCases": 10,
        "wp02SelectedUpstreamTestsPassed": 10,
        "selectedApiShapePairs": 14,
        "asyncFamilyArityPairs": 3,
        "asyncJavaNameCollisions": 3,
        "selectedTaskValueTaskReferenceCases": 25,
        "internalAsyncStateFixtures": 2,
        "internalAsyncRaceRounds": 200,
        "internalJarSha256": jar_hash,
        "status": "BOUNDED_PASS; E01/E02/E03/N01 AND PUBLIC WP-01/WP-02 QUALIFICATION OPEN",
        "limitations": ["The internal cancellation and async state prototypes do not cover full Task/ValueTask public semantics.", "The selected Task/ValueTask cases and two internal Java fixtures are bounded observations, not public Java parity or upstream xUnit tests.", "The three exact-name Java collisions leave public generic/non-generic representation unresolved.", "Two hundred coordinated races do not exhaust all interleavings or publication conditions.", "Selected upstream tests and fixtures are not exhaustive concurrency or platform validation.", "No public .j facade or product release is qualified."],
    }
    output = EVIDENCE / "foundation-gate-v10.0.12.json"
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("PASS bounded foundation gate: WP-01 12+5, WP-02 15 Java + 10 upstream, async 3 pairs + 3 collisions + 25 reference cases + 2 Java fixtures")


if __name__ == "__main__":
    gate()
