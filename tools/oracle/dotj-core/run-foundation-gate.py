"""Run bounded WP-01/WP-02 local and pinned-reference checks."""

import hashlib
import json
import subprocess
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ORACLE = ROOT / "tools/oracle/dotj-core"
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
CORELIB_HASH = "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"


def run(*args, contains):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode or contains not in result.stdout:
        raise RuntimeError(f"Failed {args}: {result.returncode}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def gate(source):
    assert source.is_dir(), "A pinned source root is required"
    wp01 = run("powershell", "-NoProfile", "-File", str(ORACLE / "run-wp01-fixtures.ps1"), contains="PASS: 16 Java fixtures and 5 .NET oracles")
    wp02 = run("powershell", "-NoProfile", "-File", str(ORACLE / "run-wp02-java-fixtures.ps1"), contains="PASS: 15 internal WP-02 Java fixtures")
    async_output = run("powershell", "-NoProfile", "-File", str(ORACLE / "run-async-java-fixtures.ps1"),
                       contains="PASS: internal timed wait cases")
    assert async_output.count("PASS:") == 5
    reference = json.loads(run("dotnet", "run", "--project", str(ORACLE / "cancellation-behavior/CancellationBehaviorOracle.csproj"), "--configuration", "Release", "--no-build", "--no-launch-profile", contains="\"runtimeVersion\""))
    assert reference["coreLibSha256"] == CORELIB_HASH and len(reference["cases"]) == 10
    assert reference == json.loads((EVIDENCE / "cancellation-behavior-v10.0.12/oracle-output.json").read_text(encoding="utf-8"))
    run("python", str(ORACLE / "verify-selected-api-shapes.py"), "--source-root", str(source), contains="PASS")
    run("python", str(ORACLE / "verify-wp02-api-shapes.py"), "--source-root", str(source), contains="PASS 7")
    run("python", str(ORACLE / "verify-wp02-test-map.py"), "--source-root", str(source), contains="PASS 10")
    run("python", str(ORACLE / "verify-wp02-java-names.py"), contains="PASS 3")
    run("python", str(ORACLE / "verify-task-family-arity.py"), "--source-root", str(source), contains="PASS 3 pinned async family arity pairs")
    for family in ("Task", "TaskCompletionSource", "ValueTask"):
        run("python", str(ORACLE / "verify-async-java-name-collision.py"), family,
            contains=f"PASS expected Java name collision: {family}")
    run("python", str(ORACLE / "run-task-behavior-oracle.py"),
        contains="PASS 57 selected Task/ValueTask reference cases on pinned CoreLib")
    task_reference = json.loads((EVIDENCE / "task-behavior-v10.0.12/oracle-output.json").read_text(encoding="utf-8"))
    assert task_reference["coreLibSha256"] == CORELIB_HASH and len(task_reference["cases"]) == 57
    run("powershell", "-NoProfile", "-File", str(ORACLE / "run-wp02-upstream-tests.ps1"), "-SourceRoot", str(source), contains="Passed:    10")
    upstream = json.loads((Path.home() / "AppData/Local/Temp/dotj-wp02-upstream-results/summary.json").read_text(encoding="utf-8-sig"))
    assert upstream["passed"] == 10 and upstream["sourceCommit"] == "4271d88e0aebf3d04f188f1334c2220d80555ef6"
    run("powershell", "-NoProfile", "-File", str(ORACLE / "build-internal-core.ps1"), contains="internal sources and")
    jar = ROOT / "dotj-core/dotj-core-01/build/dotj-core-internal-v1.jar"
    jar_hash = hashlib.sha256(jar.read_bytes()).hexdigest()
    jar_manifest = json.loads((EVIDENCE / "internal-core-jar-v1.json").read_text(encoding="utf-8-sig"))
    assert jar_manifest["jarSha256"] == jar_hash
    manifest = {
        "schemaVersion": 1,
        "sourceCommit": upstream["sourceCommit"],
        "runtimeVersion": "10.0.12",
        "coreLibSha256": CORELIB_HASH,
        "wp01JavaFixtures": 16,
        "wp01DotnetOracles": 5,
        "wp02InternalJavaFixtures": 15,
        "wp02ReferenceCases": 10,
        "wp02SelectedUpstreamTestsPassed": 10,
        "selectedApiShapePairs": 14,
        "asyncFamilyArityPairs": 3,
        "asyncJavaNameCollisions": 3,
        "selectedTaskValueTaskReferenceCases": 57,
        "internalAsyncStateFixtures": 5,
        "internalAsyncRaceRounds": 200,
        "internalAsyncWaitRaceRounds": 200,
        "internalTimedWaitRaceRoundsPerMode": 100,
        "internalTimedWaitRaceModes": 5,
        "waitCancellationListenerCleanup": True,
        "internalJarSha256": jar_hash,
        "status": "BOUNDED_PASS; E01/E02/E03/N01 AND PUBLIC WP-01/WP-02 QUALIFICATION OPEN",
        "limitations": ["The internal cancellation and async state prototypes do not cover full Task/ValueTask public semantics.", "The selected Task/ValueTask cases and five internal Java fixtures are bounded observations, not public Java parity or upstream xUnit tests.", "Timed waits use a private removable signal, daemon scheduler and Java TimeoutException; they do not implement .NET cancellation tokens, awaiters or public Task.WaitAsync.", "Internal Task-family arity lowering has no .j source binder or qualified public facade.", "The coordinated races do not exhaust all interleavings or publication conditions.", "Selected upstream tests and fixtures are not exhaustive concurrency or platform validation.", "Only one public IDisposable candidate exists; full .j facade and product release are not qualified."],
    }
    output = EVIDENCE / "foundation-gate-v10.0.12.json"
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("PASS bounded foundation gate: WP-01 16+5, WP-02 15 Java + 10 upstream, async 3 pairs + 3 collisions + 57 reference cases + 5 Java fixtures")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=Path("R:/"))
    gate(parser.parse_args().source_root)
