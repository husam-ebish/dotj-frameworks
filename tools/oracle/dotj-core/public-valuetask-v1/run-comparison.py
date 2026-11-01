"""Run the selected public nongeneric ValueTask surface on pinned .NET and on the public candidate source, then compare."""
import argparse
import ctypes
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
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("run_id")
parser.add_argument("--candidate-jar", type=Path)
args = parser.parse_args()
RUN_ID = args.run_id
if not RUN_ID or Path(RUN_ID).name != RUN_ID or RUN_ID in (".", ".."):
    parser.error("run_id must be a new validation directory name")
RUN = BASE / "validation" / RUN_ID
candidate_jar = args.candidate_jar.resolve(strict=True) if args.candidate_jar else None
commands = []


def memory_before(label):
    class MemoryStatus(ctypes.Structure):
        _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong)] + [
            (name, ctypes.c_ulonglong) for name in ("totalPhysical", "freePhysical", "totalPageFile",
                "freeVirtual", "totalAddressSpace", "freeAddressSpace", "extendedVirtual")]
    memory = MemoryStatus()
    memory.length = ctypes.sizeof(memory)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
        raise ctypes.WinError()
    result = {"before": label, "freePhysicalBytes": memory.freePhysical, "freeVirtualBytes": memory.freeVirtual}
    if memory.freePhysical < 512 * 1024**2 or memory.freeVirtual < 16 * 1024**3:
        raise RuntimeError("Resource floor not met: " + json.dumps(result))
    return result


def step(arguments, label, timeout=30):
    command = {"label": label, "argv": [str(item) for item in arguments], "timeoutSeconds": timeout,
               "memory": memory_before(label),
               "environmentOverrides": {key: environment[key] for key in (
                   "TEMP", "TMP", "DOTNET_ROOT", "DOTNET_MULTILEVEL_LOOKUP", "DOTNET_CLI_HOME",
                   "DOTNET_CLI_TELEMETRY_OPTOUT", "DOTNET_ROLL_FORWARD", "DOTNET_GCHeapHardLimit",
                   "DOTNET_gcServer", "DOTNET_PROCESSOR_COUNT", "DOTNET_CLI_UI_LANGUAGE", "VSLANG", "NUGET_PACKAGES")}}
    commands.append(command)
    (RUN / "commands.json").write_text(json.dumps(commands, indent=2), encoding="utf-8")
    result = subprocess.run(command["argv"], cwd=RUN, env=environment, capture_output=True, text=True, timeout=timeout)
    command["exitCode"] = result.returncode
    (RUN / "commands.json").write_text(json.dumps(commands, indent=2), encoding="utf-8")
    (RUN / f"{label}.log").write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode != 0:
        print(f"FAIL {label}: {(result.stdout + result.stderr)[-1800:]}")
        sys.exit(1)
    return result.stdout + result.stderr


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def observations(lines, label):
    if not lines:
        raise ValueError(label + ": empty observation set")
    result = {}
    for line in lines:
        key, separator, value = line.partition("=")
        if not separator or not key.strip() or key in result:
            raise ValueError(label + ": malformed, empty or duplicate observation key: " + repr(line))
        result[key] = value
    return result


RUN.mkdir(parents=True)
(RUN / "temp").mkdir()
input_hashes = {
    "oracleSourceSha256": digest(HERE / "PublicValueTaskOracle.cs"),
    "javaFixtureSha256": digest(HERE / "PublicValueTaskFixtures.java"),
    "runnerSha256": digest(Path(__file__)),
    "javaSourceSha256": {path.name: digest(path) for path in MAIN},
    "candidateJar": {"path": str(candidate_jar), "sha256": digest(candidate_jar), "sizeBytes": candidate_jar.stat().st_size} if candidate_jar else None,
}
# Bind implicitly compiled dependencies too; this inventory does not claim the JAR contains them.
source_inventory = {path.relative_to(PUBLIC).as_posix(): digest(path) for path in sorted(PUBLIC.rglob("*.java"))}
(RUN / "java-source-inventory.json").write_text(json.dumps(source_inventory, indent=2), encoding="utf-8")
input_hashes["javaSourceInventorySha256"] = digest(RUN / "java-source-inventory.json")
(RUN / "inputs.json").write_text(json.dumps(input_hashes, indent=2), encoding="utf-8")
environment = {key: value for key, value in os.environ.items()
               if not key.upper().startswith(("DOTNET_", "COMPLUS_", "CORECLR_", "COR_", "MSBUILD"))
               and key not in ("JAVA_TOOL_OPTIONS", "_JAVA_OPTIONS", "JDK_JAVA_OPTIONS")}
environment.update(TEMP=str(RUN / "temp"), TMP=str(RUN / "temp"), DOTNET_ROOT=str(DOTNET),
                   DOTNET_MULTILEVEL_LOOKUP="0", DOTNET_CLI_HOME=str(RUN / "temp"), DOTNET_CLI_TELEMETRY_OPTOUT="1",
                   DOTNET_ROLL_FORWARD="Disable", DOTNET_GCHeapHardLimit="8000000", DOTNET_gcServer="0",
                   DOTNET_PROCESSOR_COUNT="2", DOTNET_CLI_UI_LANGUAGE="en-US", VSLANG="1033",
                   NUGET_PACKAGES=str(RUN / "temp" / "nuget"))
sdk_version = step([DOTNET / "dotnet.exe", "--version"], "sdk-version").strip()
if sdk_version != "10.0.401":
    raise RuntimeError("Unexpected SDK: " + sdk_version)
java_version = step([JDK / "java.exe", "-Xmx128m", "-XX:ActiveProcessorCount=2", "-XX:+UseSerialGC",
                     "-Djava.io.tmpdir=" + str(RUN / "temp"), "-Duser.home=" + str(RUN / "temp"), "-version"], "java-version")
if '"21.0.12.1"' not in java_version:
    raise RuntimeError("Unexpected JDK: " + java_version)
artifact = RUN / "PublicValueTaskOracle.dll"
step([DOTNET / "dotnet.exe", "exec", DOTNET / "sdk/10.0.401/Roslyn/bincore/csc.dll", "-nologo", "-noconfig", "-nostdlib",
      "-target:exe", "-deterministic", "-nullable:enable", "-langversion:14", "-warnaserror", f"-out:{artifact}",
      *[f"-r:{path}" for path in sorted(REFERENCE.glob("*.dll"))], HERE / "PublicValueTaskOracle.cs"], "compile-native")
(RUN / "PublicValueTaskOracle.runtimeconfig.json").write_text(json.dumps({"runtimeOptions": {
    "tfm": "net10.0", "rollForward": "Disable", "framework": {"name": "Microsoft.NETCore.App", "version": "10.0.12"}}}), encoding="utf-8")
native_path, java_path = RUN / "native.txt", RUN / "java.txt"
step([DOTNET / "dotnet.exe", "exec", artifact, native_path], "run-native")
jvm = ["-Xms16m", "-Xmx128m", "-XX:ActiveProcessorCount=2", "-XX:+UseSerialGC",
       "-Djava.io.tmpdir=" + str(RUN / "temp"), "-Duser.home=" + str(RUN / "temp"),
       "-XX:ErrorFile=" + str(RUN / "temp" / "hs_err_pid%p.log"),
       "-XX:HeapDumpPath=" + str(RUN / "temp")]
java_inputs = ["-cp", candidate_jar, "-implicit:none"] if candidate_jar else ["-sourcepath", PUBLIC, *MAIN]
step([JDK / "javac.exe", *["-J" + option for option in jvm], "-d", RUN / "classes", "-encoding", "UTF-8",
      *java_inputs, HERE / "PublicValueTaskFixtures.java"], "compile-java", 120)
classpath = str(RUN / "classes") + (os.pathsep + str(candidate_jar) if candidate_jar else "")
step([JDK / "java.exe", *jvm, "-cp", classpath, "PublicValueTaskFixtures", java_path], "run-java", 120)

native_lines = native_path.read_text(encoding="utf-8").splitlines()
java_lines = java_path.read_text(encoding="utf-8").splitlines()
if not native_lines or native_lines[-1] not in ("runtime=10.0.12.0", "runtime=10.0.12"):
    print("FAIL runtime", native_lines[-1:] )
    sys.exit(1)
native_map = observations(native_lines[:-1], "native")
java_map = observations(java_lines, "java")
differences = [{"key": key, "native": native_map.get(key), "java": java_map.get(key)}
               for key in sorted(set(native_map) | set(java_map)) if native_map.get(key) != java_map.get(key)]
comparison = {"observations": len(native_map), "javaObservations": len(java_map), "differences": differences}
(RUN / "comparison.json").write_text(json.dumps(comparison, indent=2), encoding="utf-8")
print(json.dumps(comparison, indent=1))
if differences:
    sys.exit(2)
if candidate_jar and digest(candidate_jar) != input_hashes["candidateJar"]["sha256"]:
    raise RuntimeError("Candidate JAR changed during comparison")
record = {
    "schemaVersion": 1, "status": "PASS_MATCHED_PUBLIC_VALUETASK", "runId": RUN_ID, "runtime": "10.0.12", "sdk": "10.0.401",
    **input_hashes,
    "qualificationMode": "packaged-candidate" if candidate_jar else "selected-public-source",
    "toolchainSha256": {str(path.relative_to(BASE)): digest(path) for path in (
        DOTNET / "dotnet.exe", DOTNET / "sdk/10.0.401/Roslyn/bincore/csc.dll",
        DOTNET / "shared/Microsoft.NETCore.App/10.0.12/System.Private.CoreLib.dll", JDK / "java.exe", JDK / "javac.exe")},
    "resourceLimits": {"jvmHeapMiB": 128, "nativeHeapMiB": 128, "processors": 2,
                       "javaTimeoutSeconds": 120, "nativeTimeoutSeconds": 30,
                       "minFreePhysicalMiB": 512, "minFreeVirtualGiB": 16},
    "observations": native_map, "acceptanceCredit": 0,
    "boundary": "Selected nongeneric ValueTask over a completed value or IValueTaskSource; no Task, AsTask, Preserve, generic ValueTask or ExecutionContext capture."}
EVIDENCE.write_text(json.dumps(record, indent=2) + chr(10), encoding="utf-8", newline=chr(10))
(RUN / "evidence.json").write_text(json.dumps(record, indent=2) + chr(10), encoding="utf-8")
print("PASS", len(native_map))
