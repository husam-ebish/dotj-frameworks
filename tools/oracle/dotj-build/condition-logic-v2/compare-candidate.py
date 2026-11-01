"""Compile the evaluation candidate and compare every logic-v2 case with the native capture."""
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CANDIDATE = ROOT / "dotj-build/evaluation-candidate"
LOGIC = CANDIDATE / "condition-logic-v2"
BASE = Path(r"D:\AI\Implementation\dotj Frameworks")
JDK = BASE / "toolchains/jdk-qualified/jdk-21.0.12.1+1/bin"
CAPTURE = LOGIC / "evidence/native-pass2-capture.json"
OUTPUT = LOGIC / "evidence/candidate-comparison-v1.json"
# The candidate statically validates skipped conditions, so it refuses where MSBuild skips parsing.
# The other three are evaluated values outside the profile, declared in the manifest before native capture.
DECLARED_REFUSALS = {"CL08-skipped-malformed": "CONDITION_PROFILE", "CL04-lazy-exists-2": "IMPORT_PATH_PROFILE",
                     "CL05-scalar-2": "CONDITION_COERCION", "CL05-scalar-4": "CONDITION_PROFILE"}


def fail(message):
    print("FAIL:", message)
    sys.exit(1)


def text(value):
    return base64.b64decode(value).decode("utf-8")


def encode(value):
    return base64.b64encode(value.encode("utf-8")).decode("ascii")


run = BASE / "validation" / sys.argv[1]
run.mkdir(parents=True)
classes = run / "classes"
sources = [str(p) for p in (CANDIDATE / "src").rglob("*.java")]
sources += [str(CANDIDATE / "tests/org/dotj/internal/build/evaluation/ConditionLogicRunner.java")]
environment = dict(os.environ, TEMP=str(run), TMP=str(run))
compiled = subprocess.run([str(JDK / "javac.exe"), "-d", str(classes), "-encoding", "UTF-8", *sources],
                          env=environment, capture_output=True, text=True, timeout=300)
if compiled.returncode != 0:
    fail(compiled.stdout + compiled.stderr)

raw = CAPTURE.read_bytes()
capture = json.loads(raw)
if capture["status"] != "PASS_REFERENCE_LOGIC_V2_CAPTURE":
    fail("capture status")
rows = capture["payload"]["rows"]
fixture_root = capture["fixtureRoot"]
cases = run / "cases.tsv"
cases.write_text("".join("\t".join([row["id"], *[encode(part) for pair in row["globals"].items() for part in pair]]) + "\n"
                         for row in rows), encoding="utf-8", newline="\n")
executed = subprocess.run([str(JDK / "java.exe"), "-Dfile.encoding=UTF-8", "-cp", str(classes),
                           "org.dotj.internal.build.evaluation.ConditionLogicRunner", str(LOGIC / "fixtures"), str(cases)],
                          env=environment, capture_output=True, text=True, timeout=120)
if executed.returncode != 0:
    fail(executed.stdout + executed.stderr)
(run / "java.tsv").write_text(executed.stdout, encoding="utf-8", newline="\n")
java = {}
for line in executed.stdout.splitlines():
    columns = line.split("\t")
    java[columns[0]] = columns[1:]

results, mismatches = [], []
for row in rows:
    identity, native, actual = row["id"], row["evaluation"], java.get(row["id"])
    if actual is None:
        mismatches.append(identity + ": missing Java row")
        continue
    if identity in DECLARED_REFUSALS:
        status = "DECLARED_PROFILE_REFUSAL"
        if actual != ["REJECT", DECLARED_REFUSALS[identity]]:
            mismatches.append(f"{identity}: expected declared refusal, got {actual}")
    elif not native["success"]:
        status = "MATCHED_REFUSAL_OF_NATIVE_FAILURE"
        if actual[0] != "REJECT":
            mismatches.append(f"{identity}: native failure {native['code']} but Java accepted")
    elif actual[0] != "OK":
        status = "MISMATCH"
        mismatches.append(f"{identity}: native succeeded but Java refused {actual}")
    else:
        status = "MATCHED_EVALUATION"
        root = Path(fixture_root) / identity
        imports = "|".join(str(Path(e["owner"]).relative_to(root)) + ">" + str(Path(e["project"]).relative_to(root))
                           + f"@{e['line']}:{e['column']}" for e in native["imports"])
        warnings = "|".join(f"{d['code']}:{Path(d['file']).relative_to(root)}@{d['line']}:{d['column']}:"
                            + d["message"].split('"')[1] for d in row["diagnostics"])
        expected = [native["properties"]["P"], native["properties"]["Q"], imports, warnings]
        observed = [text(actual[1]), text(actual[2]), text(actual[3]), text(actual[4])]
        if expected != observed:
            mismatches.append(f"{identity}: {expected} != {observed}")
    results.append({"id": identity, "status": status, "nativeWarnings": [d["code"] for d in row["diagnostics"]]})

counts = {}
for row in results:
    counts[row["status"]] = counts.get(row["status"], 0) + 1
if mismatches:
    fail("\n".join(mismatches))
OUTPUT.write_text(json.dumps({
    "schemaVersion": 1, "status": "PASS_CONDITION_LOGIC_V2_COMPARISON", "runId": sys.argv[1],
    "captureSha256": hashlib.sha256(raw).hexdigest(), "cases": len(results), "counts": counts,
    "gaps": ["Native failure text and positions are not compared", "Warning message text beyond the condition is not compared"],
    "acceptanceCredit": 0, "results": results}, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"cases": len(results), "counts": counts}))
