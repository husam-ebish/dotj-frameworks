"""Compare one hash-bound Task28 lifecycle proof with a separately captured oracle.

The Java assertion predicates are entailed by its successful unchanged Run method;
raw native exception spellings remain diagnostics. This is private qualification.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

PROFILE = "ownership-source-lifecycle-v1"
JAVA_SHA = "d7caf5682c2fc66608090b4804ae2a882a965fca0922ac2918a737d5bfced838"
CORE_SHA = "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"
COUNTERS = ["syncDisposals", "pendingDisposals", "sourceCallbacks", "sourceResultCalls",
            "sourceToken", "throwDisposals", "faultResultCalls", "cleanupResultCalls",
            "borrowedAfterExplicit", "borrowedCloses"]
# These are original LifecycleConsumer guards, not newly observed native results.
JAVA_GUARDS = {
    "syncCompletedSuccessfully": True, "borrowedUntouchedAfterOwner": True,
    "pendingBeforeCompletion": True, "doneBeforeCompletion": 0,
    "registrations": 1, "stateIsAction": True, "doneAfterCompletion": 1,
    "pendingCompletedSuccessfully": True, "beforeReturnSameException": True,
    "faultSameException": True, "faultSameCause": True, "cleanupSameException": True,
    "borrowedUntouchedBeforeCaller": True,
    "failurePhases": ["DisposeAsync-before-return", "GetResult-source-fault", "finally-GetResult-source-fault"]}
ROUTES = {"pending": "IValueTaskSource", "fault": "IValueTaskSource", "cleanup": "IValueTaskSource",
          "registration": "ConfigureAwait(false).UnsafeOnCompleted", "tokens": [-8, 5, 7], "flags": 0}


class ComparisonError(ValueError):
    pass


def need(ok, message):
    if not ok:
        raise ComparisonError(message)


def strict_equal(actual, expected, field):
    need(type(actual) is type(expected), f"{field}: wrong JSON type")
    if type(expected) is dict:
        need(actual.keys() == expected.keys(), f"{field}: missing or extra keys")
        for key, value in expected.items():
            strict_equal(actual[key], value, f"{field}.{key}")
    elif type(expected) is list:
        need(len(actual) == len(expected), f"{field}: wrong list length")
        for i, value in enumerate(expected):
            strict_equal(actual[i], value, f"{field}[{i}]")
    else:
        need(actual == expected, f"{field}: value mismatch")


def keys(value, names, field):
    need(type(value) is dict and set(value) == set(names), f"{field}: object keys mismatch")


def sha(value, field):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
         f"{field}: lowercase SHA256 required")


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    raw = Path(path).read_bytes()
    try:
        value = json.loads(raw, object_pairs_hook=no_duplicates,
                           parse_constant=lambda x: (_ for _ in ()).throw(ComparisonError(f"invalid JSON number {x}")))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ComparisonError(f"Invalid JSON: {path}") from error
    return value, hashlib.sha256(raw).hexdigest()


def parse_result(value):
    need(type(value) is str, "lifecycle result must be string")
    parts = value.split("|")
    need(len(parts) == 11 and parts[0] == "PASS", "lifecycle result shape mismatch")
    result = {}
    for name, part in zip(COUNTERS, parts[1:]):
        match = re.fullmatch(re.escape(name) + r"=(-?(?:0|[1-9][0-9]*))", part)
        need(match is not None, f"lifecycle counter {name}: invalid/duplicate/out-of-order")
        result[name] = int(match.group(1))
    return result


def native_diagnostics(value):
    keys(value, ["exceptions", "statusCalls", "actionStateSameReference"], "diagnostics")
    need(type(value["statusCalls"]) is int and value["statusCalls"] >= 0, "diagnostic statusCalls type")
    need(type(value["actionStateSameReference"]) is bool, "diagnostic action identity type")
    records = value["exceptions"]
    need(type(records) is list and len(records) == 3, "three native exception diagnostics required")
    for role, row in zip(["beforeReturn", "fault", "cleanup"], records):
        keys(row, ["role", "type", "message", "hResult", "innerType", "innerMessage", "sameAsSupplied", "wrappers"], "exception")
        strict_equal(row["role"], role, "exception.role")
        for field in ["type", "message"]:
            need(type(row[field]) is str, f"exception.{field}: string required")
        need(bool(row["type"]), "exception type must be retained")
        need(type(row["hResult"]) is int, "exception.hResult: integer required")
        for field in ["innerType", "innerMessage"]:
            need(row[field] is None or type(row[field]) is str, f"exception.{field}: string/null required")
        strict_equal(row["sameAsSupplied"], True, "exception.sameAsSupplied")
        # This native fixture uses direct calls, so no reflection wrapper is removed.
        strict_equal(row["wrappers"], [], "exception.wrappers")


def compare_files(java_path, native_path, receipt_path, lock_path):
    lock, _ = read_json(lock_path)
    keys(lock, ["schemaVersion", "profile", "javaEvidenceSha256", "oracleSourceSha256", "inputSha256"], "lock")
    strict_equal(lock["schemaVersion"], 1, "lock.schemaVersion")
    strict_equal(lock["profile"], PROFILE, "lock.profile")
    strict_equal(lock["javaEvidenceSha256"], JAVA_SHA, "lock.javaEvidenceSha256")
    for field in ["oracleSourceSha256", "inputSha256"]:
        sha(lock[field], f"lock.{field}")
    java, java_sha = read_json(java_path)
    need(java_sha == JAVA_SHA, "Java bytes do not match actual reviewed Task28 proof")
    strict_equal(java.get("status"), "PASS_ORIGINAL_SOURCE_SLICE", "Java.status")
    strict_equal(java.get("compileSuccess"), True, "Java.compileSuccess")
    invocations = java.get("invocations")
    need(type(invocations) is list, "Java invocations absent")
    selected = [r for r in invocations if r.get("class") == "asyncfixture.LifecycleConsumer" and r.get("method") == "Run"]
    need(len(selected) == 1, "Exactly one actual lifecycle invocation required")
    row = selected[0]
    strict_equal(row.get("status"), "PASS", "Java invocation status")
    strict_equal(row.get("actual"), row.get("expected"), "Java actual return")
    java_counters = parse_result(row["actual"])

    native, native_sha = read_json(native_path)
    receipt, _ = read_json(receipt_path)
    keys(receipt, ["status", "processLaunched", "exitCode", "timedOut", "runId", "oracleSourceSha256",
                   "inputSha256", "nativeEvidenceSha256", "compiledArtifactSha256"], "receipt")
    for field, expected in [("status", "PASS_NATIVE_LIFECYCLE_CAPTURE"), ("processLaunched", True),
                            ("exitCode", 0), ("timedOut", False)]:
        strict_equal(receipt[field], expected, f"receipt.{field}")
    need(type(receipt["runId"]) is str and bool(receipt["runId"]), "receipt.runId required")
    for field in ["oracleSourceSha256", "inputSha256", "nativeEvidenceSha256", "compiledArtifactSha256"]:
        sha(receipt[field], f"receipt.{field}")
    need(receipt["nativeEvidenceSha256"] == native_sha, "native raw evidence hash mismatch")
    for field in ["oracleSourceSha256", "inputSha256"]:
        need(receipt[field] == lock[field], f"receipt {field} differs from preparation lock")
    keys(native, ["schemaVersion", "profile", "runtimeVersion", "coreLibSha256", "inputSha256",
                  "result", "routes", "observations", "diagnostics"], "native")
    for field, expected in [("schemaVersion", 1), ("profile", PROFILE), ("runtimeVersion", "10.0.12"),
                            ("coreLibSha256", CORE_SHA), ("inputSha256", lock["inputSha256"])]:
        strict_equal(native[field], expected, f"native.{field}")
    strict_equal(native["routes"], ROUTES, "native.routes")
    strict_equal(native["observations"], JAVA_GUARDS, "native.observations")
    strict_equal(parse_result(native["result"]), java_counters, "native counters")
    strict_equal(native["result"], row["actual"], "native actual return")
    native_diagnostics(native["diagnostics"])
    return {"status": "PASS_MATCHED_LIFECYCLE_OBSERVABLES", "profile": PROFILE,
            "javaEvidenceSha256": java_sha, "nativeEvidenceSha256": native_sha,
            "runId": receipt["runId"], "counters": java_counters,
            "nativeDiagnostics": native["diagnostics"], "acceptanceCredit": 0,
            "zeroInitializerPair": "BLOCKED_LANGUAGE_SHAPE_CS0236"}


def main():
    if len(sys.argv) != 6:
        raise ComparisonError("usage: compare.py JAVA NATIVE ROOT_RECEIPT LOCK NEW_OUTPUT")
    result = compare_files(*sys.argv[1:5])
    target = Path(sys.argv[5]).resolve()
    need(target.is_relative_to(Path(r"D:\AI\Implementation\dotj Frameworks").resolve()), "output must be within owned D storage")
    with target.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=True, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    try:
        main()
    except (ComparisonError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
