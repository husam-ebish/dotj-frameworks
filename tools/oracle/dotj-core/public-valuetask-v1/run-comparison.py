"""Run the selected public nongeneric ValueTask surface on pinned .NET and on the public candidate source, then compare."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = Path(r"D:\AI\Implementation\dotj Frameworks")
DOTNET = BASE / "toolchains/dotnet"
JDK = BASE / "toolchains/jdk-qualified/jdk-21.0.12.1+1/bin"
REFERENCE = DOTNET / "packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0"
PUBLIC = ROOT / "dotj-core/dotj-core-public/src/main/java"
MAIN = [PUBLIC / "System" / name for name in ("Action_1.java", "IAsyncDisposable.java")]
MAIN += [PUBLIC / "System/Threading/Tasks" / name for name in ("ValueTask.java",)]
MAIN += [PUBLIC / "System/Threading/Tasks/Sources" / name for name in ("IValueTaskSource.java", "ValueTaskSourceStatus.java", "ValueTaskSourceOnCompletedFlags.java")]
MAIN += [PUBLIC / "System/Runtime/CompilerServices" / name for name in ("ValueTaskAwaiter.java", "ConfiguredValueTaskAwaitable.java", "INotifyCompletion.java", "ICriticalNotifyCompletion.java")]
MAIN += [PUBLIC / "org/dotj/internal" / name for name in ("async/ValueTaskBridge.java", "delegates/ActionBody1.java")]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence/public-valuetask-v1.json"
RUN_ID = sys.argv[1]
RUN = BASE / "validation" / RUN_ID


def step(arguments, label, timeout=300):
    result = subprocess.run([str(item) for item in arguments], env=environment, capture_output=True, text=True, timeout=timeout)
    (RUN / f"{label}.log").write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode != 0:
        print(f"FAIL {label}: {(result.stdout + result.stderr)[-1800:]}")
        sys.exit(1)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


RUN.mkdir(parents=True)
(RUN / "temp").mkdir()
environment = dict(os.environ, TEMP=str(RUN / "temp"), TMP=str(RUN / "temp"), DOTNET_ROOT=str(DOTNET),
                   DOTNET_MULTILEVEL_LOOKUP="0", DOTNET_CLI_HOME=str(RUN / "temp"), DOTNET_CLI_TELEMETRY_OPTOUT="1")
artifact = RUN / "PublicValueTaskOracle.dll"
step([DOTNET / "dotnet.exe", "exec", DOTNET / "sdk/10.0.401/Roslyn/bincore/csc.dll", "-nologo", "-noconfig", "-nostdlib",
      "-target:exe", "-deterministic", "-nullable:enable", "-langversion:14", "-warnaserror", f"-out:{artifact}",
      *[f"-r:{path}" for path in sorted(REFERENCE.glob("*.dll"))], HERE / "PublicValueTaskOracle.cs"], "compile-native")
(RUN / "PublicValueTaskOracle.runtimeconfig.json").write_text(json.dumps({"runtimeOptions": {
    "tfm": "net10.0", "rollForward": "Disable", "framework": {"name": "Microsoft.NETCore.App", "version": "10.0.12"}}}), encoding="utf-8")
native_path, java_path = RUN / "native.txt", RUN / "java.txt"
step([DOTNET / "dotnet.exe", "exec", artifact, native_path], "run-native", 120)
step([JDK / "javac.exe", "-d", RUN / "classes", "-encoding", "UTF-8", "-sourcepath", PUBLIC, *MAIN,
      HERE / "PublicValueTaskFixtures.java"], "compile-java")
step([JDK / "java.exe", "-cp", RUN / "classes", "PublicValueTaskFixtures", java_path], "run-java", 120)

native_lines = native_path.read_text(encoding="utf-8").splitlines()
java_lines = java_path.read_text(encoding="utf-8").splitlines()
if native_lines[-1] != "runtime=10.0.12.0" and native_lines[-1] != "runtime=10.0.12":
    print("FAIL runtime", native_lines[-1])
    sys.exit(1)
native_map = dict(line.split("=", 1) for line in native_lines[:-1])
java_map = dict(line.split("=", 1) for line in java_lines)
differences = [{"key": key, "native": native_map.get(key), "java": java_map.get(key)}
               for key in sorted(set(native_map) | set(java_map)) if native_map.get(key) != java_map.get(key)]
print(json.dumps({"observations": len(native_map), "differences": differences}, indent=1))
if differences:
    sys.exit(2)
record = {
    "schemaVersion": 1, "status": "PASS_MATCHED_PUBLIC_VALUETASK", "runId": RUN_ID, "runtime": "10.0.12", "sdk": "10.0.401",
    "oracleSourceSha256": digest(HERE / "PublicValueTaskOracle.cs"),
    "javaSourceSha256": {path.name: digest(path) for path in MAIN},
    "observations": native_map, "acceptanceCredit": 0,
    "boundary": "Selected nongeneric ValueTask over a completed value or IValueTaskSource; no Task, AsTask, Preserve, generic ValueTask or ExecutionContext capture."}
EVIDENCE.write_text(json.dumps(record, indent=2) + chr(10), encoding="utf-8", newline=chr(10))
print("PASS", len(native_map))
