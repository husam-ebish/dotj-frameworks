"""Run the F02 fixtures on pinned .NET and on the internal Java cancellation source, then compare."""
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
MAIN = ROOT / "dotj-core/dotj-core-01/src/main/java/org/dotj/internal/cancellation"
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence/cancellation-fixtures-v1.json"
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
artifact = RUN / "CancellationOracle.dll"
step([DOTNET / "dotnet.exe", "exec", DOTNET / "sdk/10.0.401/Roslyn/bincore/csc.dll", "-nologo", "-noconfig", "-nostdlib",
      "-target:exe", "-deterministic", "-nullable:enable", "-langversion:14", "-warnaserror", f"-out:{artifact}",
      *[f"-r:{path}" for path in sorted(REFERENCE.glob("*.dll"))], HERE / "CancellationOracle.cs"], "compile-native")
(RUN / "CancellationOracle.runtimeconfig.json").write_text(json.dumps({"runtimeOptions": {
    "tfm": "net10.0", "rollForward": "Disable", "framework": {"name": "Microsoft.NETCore.App", "version": "10.0.12"}}}), encoding="utf-8")
native_path, java_path = RUN / "native.txt", RUN / "java.txt"
step([DOTNET / "dotnet.exe", "exec", artifact, native_path], "run-native", 120)
step([JDK / "javac.exe", "-d", RUN / "classes", "-encoding", "UTF-8", *sorted(MAIN.glob("*.java")),
      HERE / "org/dotj/internal/cancellation/CancellationFixtures.java"], "compile-java")
step([JDK / "java.exe", "-cp", RUN / "classes", "org.dotj.internal.cancellation.CancellationFixtures", java_path], "run-java", 120)

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
EVIDENCE.write_text(json.dumps({
    "schemaVersion": 1, "status": "PASS_MATCHED_CANCELLATION_FIXTURES", "runId": RUN_ID, "runtime": "10.0.12", "sdk": "10.0.401",
    "fixtures": ["DJ-001-F02-01", "DJ-001-F02-02", "DJ-001-F02-03", "DJ-001-F02-04", "DJ-001-F02-05"],
    "oracleSourceSha256": digest(HERE / "CancellationOracle.cs"),
    "javaSourceSha256": {path.name: digest(path) for path in sorted(MAIN.glob("*.java"))},
    "observations": native_map, "acceptanceCredit": 0,
    "boundary": "Internal package-private Java source; not a public System.Threading API."}, indent=2) + "\n",
    encoding="utf-8", newline="\n")
print("PASS", len(native_map))
