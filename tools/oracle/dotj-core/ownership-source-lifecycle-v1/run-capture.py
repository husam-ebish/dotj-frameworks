"""Compile and run the lifecycle oracle on pinned .NET, then compare it with the Java proof."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = Path(r"D:\AI\Implementation\dotj Frameworks")
DOTNET = BASE / "toolchains/dotnet"
REFERENCE = DOTNET / "packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0"
FIXTURES = BASE / "agents/validation-performance/async-disposal-source-integration/fixtures/async"
JAVA = BASE / ("agents/validation-performance/async-disposal-original-source-fixed-compiler-20261030"
               "/runs/run1/evidence/driver-evidence.json")
JAVA_SHA = "d7caf5682c2fc66608090b4804ae2a882a965fca0922ac2918a737d5bfced838"
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence/ownership-source-lifecycle-v1"
RUN_ID = sys.argv[1]
RUN = BASE / "validation" / RUN_ID


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


RUN.mkdir(parents=True)
(RUN / "temp").mkdir()
environment = dict(os.environ, TEMP=str(RUN / "temp"), TMP=str(RUN / "temp"),
                   DOTNET_ROOT=str(DOTNET), DOTNET_MULTILEVEL_LOOKUP="0", DOTNET_CLI_HOME=str(RUN / "temp"),
                   DOTNET_ROLL_FORWARD="Disable", DOTNET_CLI_TELEMETRY_OPTOUT="1")

EVIDENCE.mkdir(parents=True, exist_ok=True)
contract = EVIDENCE / "lifecycle-input-v1.json"
write_json(contract, {
    "schemaVersion": 1,
    "profile": "ownership-source-lifecycle-v1",
    "reference": {"sdk": "10.0.401", "runtime": "10.0.12"},
    "javaFixtures": {name: digest(FIXTURES / name) for name in
                     ("LifecycleConsumer.java", "Owner.java", "Resource.java", "Producer.java")},
    "javaEvidenceSha256": JAVA_SHA,
    "excluded": {
        "ZeroConsumer": "Blocked: its instance field initializer has no direct C# form (CS0236)",
        "publicApi": "Fixtures run on a private runtime JAR, not the public candidate",
        "contextAndRaces": "Execution context, scheduling flags and concurrency are not in this profile",
    },
})

source = HERE / "LifecycleOracle.cs"
lock = RUN / "lock.json"
input_sha = digest(contract)
write_json(lock, {"schemaVersion": 1, "profile": "ownership-source-lifecycle-v1", "javaEvidenceSha256": JAVA_SHA,
                  "oracleSourceSha256": digest(source), "inputSha256": input_sha})

artifact = RUN / "LifecycleOracle.dll"
references = [f"-r:{path}" for path in sorted(REFERENCE.glob("*.dll"))]
compile_result = subprocess.run(
    [str(DOTNET / "dotnet.exe"), "exec", str(DOTNET / "sdk/10.0.401/Roslyn/bincore/csc.dll"), "-nologo", "-noconfig",
     "-nostdlib", "-target:exe", "-deterministic", "-nullable:enable", "-langversion:14", "-warnaserror",
     f"-out:{artifact}", *references, str(source)],
    env=environment, capture_output=True, text=True, timeout=300)
(RUN / "compile.log").write_text(compile_result.stdout + compile_result.stderr, encoding="utf-8")
print("compile exit", compile_result.returncode, (compile_result.stdout + compile_result.stderr)[-1500:])
if compile_result.returncode != 0:
    sys.exit(1)
write_json(RUN / "LifecycleOracle.runtimeconfig.json", {"runtimeOptions": {
    "tfm": "net10.0", "rollForward": "Disable",
    "framework": {"name": "Microsoft.NETCore.App", "version": "10.0.12"}}})

native = RUN / "native-evidence.json"
timed_out = False
try:
    run = subprocess.run([str(DOTNET / "dotnet.exe"), "exec", str(artifact), str(contract), str(native)],
                         env=environment, capture_output=True, text=True, timeout=120)
    exit_code = run.returncode
    (RUN / "run.log").write_text(run.stdout + run.stderr, encoding="utf-8")
    print("run exit", exit_code, (run.stdout + run.stderr)[-1500:])
except subprocess.TimeoutExpired:
    timed_out, exit_code = True, -1
receipt = RUN / "receipt.json"
write_json(receipt, {"status": "PASS_NATIVE_LIFECYCLE_CAPTURE" if exit_code == 0 and native.exists() else "FAILED",
                     "processLaunched": True, "exitCode": exit_code, "timedOut": timed_out, "runId": RUN_ID,
                     "oracleSourceSha256": digest(source), "inputSha256": input_sha,
                     "nativeEvidenceSha256": digest(native) if native.exists() else "0" * 64,
                     "compiledArtifactSha256": digest(artifact)})

comparison = RUN / "comparison.json"
compared = subprocess.run([str(Path(sys.executable)), "-I", str(HERE / "compare.py"), str(JAVA), str(native),
                           str(receipt), str(lock), str(comparison)],
                          env=environment, capture_output=True, text=True, timeout=120)
print("compare exit", compared.returncode, compared.stdout, compared.stderr)
if compared.returncode != 0:
    sys.exit(1)
for path in (native, receipt, lock, comparison):
    shutil.copyfile(path, EVIDENCE / path.name)
shutil.copyfile(JAVA, EVIDENCE / "java-driver-evidence.json")
print(comparison.read_text(encoding="utf-8"))
