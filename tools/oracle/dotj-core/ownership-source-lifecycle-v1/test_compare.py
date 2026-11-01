"""Synthetic comparator controls, never native or product behavior evidence."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

BASE = Path(r"D:\AI\Implementation\dotj Frameworks")
OWNED = BASE / "agents/validation-performance/ownership-source-lifecycle-preparation-20261030/controls"
JAVA = BASE / "agents/validation-performance/async-disposal-original-source-fixed-compiler-20261030/runs/run1/evidence/driver-evidence.json"
JAVA_SHA = "d7caf5682c2fc66608090b4804ae2a882a965fca0922ac2918a737d5bfced838"
SUBJECT = Path(__file__).with_name("compare.py")


def digest(data):
    return hashlib.sha256(data).hexdigest()


class ComparisonControls(unittest.TestCase):
    def setUp(self):
        self.assertEqual(Path(os.environ["TEMP"]).resolve().drive.upper(), "D:")
        self.assertEqual(Path(os.environ["TMP"]).resolve().drive.upper(), "D:")
        self.assertTrue(SUBJECT.is_file(), "Comparator implementation missing")
        spec = importlib.util.spec_from_file_location("ownership_compare", SUBJECT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory(prefix="control-", dir=str(OWNED))
        self.root = Path(self.temp.name).resolve()
        self.assertTrue(self.root.is_relative_to(OWNED.resolve()))
        self.addCleanup(self.temp.cleanup)
        self.java = JAVA.read_bytes()
        self.assertEqual(digest(self.java), JAVA_SHA)
        actual = json.loads(self.java)["invocations"][0]["actual"]
        self.native = {
            "schemaVersion": 1, "profile": "ownership-source-lifecycle-v1",
            "runtimeVersion": "10.0.12", "coreLibSha256": "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678",
            "inputSha256": "b" * 64, "result": actual,
            "routes": {"pending": "IValueTaskSource", "fault": "IValueTaskSource", "cleanup": "IValueTaskSource", "registration": "ConfigureAwait(false).UnsafeOnCompleted", "tokens": [-8, 5, 7], "flags": 0},
            "observations": {
                "syncCompletedSuccessfully": True, "borrowedUntouchedAfterOwner": True,
                "pendingBeforeCompletion": True, "doneBeforeCompletion": 0,
                "registrations": 1, "stateIsAction": True, "doneAfterCompletion": 1,
                "pendingCompletedSuccessfully": True, "beforeReturnSameException": True,
                "faultSameException": True, "faultSameCause": True,
                "cleanupSameException": True, "borrowedUntouchedBeforeCaller": True,
                "failurePhases": ["DisposeAsync-before-return", "GetResult-source-fault", "finally-GetResult-source-fault"]},
            "diagnostics": {"exceptions": [
                {"role": role, "type": "System.Exception", "message": role,
                 "hResult": -2146233088, "innerType": None, "innerMessage": None,
                 "sameAsSupplied": True, "wrappers": []}
                for role in ["beforeReturn", "fault", "cleanup"]],
                "statusCalls": 2, "actionStateSameReference": True}}
        self.lock = {"schemaVersion": 1, "profile": "ownership-source-lifecycle-v1",
                     "javaEvidenceSha256": JAVA_SHA, "oracleSourceSha256": "a" * 64,
                     "inputSha256": "b" * 64}
        self.receipt = {"status": "PASS_NATIVE_LIFECYCLE_CAPTURE", "processLaunched": True,
                        "exitCode": 0, "timedOut": False, "runId": "synthetic-control-only",
                        "oracleSourceSha256": "a" * 64, "inputSha256": "b" * 64,
                        "nativeEvidenceSha256": "", "compiledArtifactSha256": "c" * 64}

    def compare(self):
        data = json.dumps(self.native, ensure_ascii=True).encode()
        self.receipt["nativeEvidenceSha256"] = digest(data)
        files = {"java.json": self.java, "native.json": data,
                 "receipt.json": json.dumps(self.receipt).encode(),
                 "lock.json": json.dumps(self.lock).encode()}
        for name, body in files.items():
            (self.root / name).write_bytes(body)
        return self.module.compare_files(*(self.root / n for n in files))

    def reject(self):
        with self.assertRaises(self.module.ComparisonError):
            self.compare()

    def test_matching_synthetic_envelope(self):
        result = self.compare()
        self.assertEqual(result["status"], "PASS_MATCHED_LIFECYCLE_OBSERVABLES")
        self.assertEqual(result["acceptanceCredit"], 0)

    def test_task_backed_fault_is_rejected(self):
        self.native["routes"]["fault"] = "Task.FromException"
        self.reject()

    def test_historical_pending_route_is_rejected(self):
        self.native["routes"]["tokens"][0] = 0
        self.native["routes"]["flags"] = 3
        self.reject()

    def test_wrong_flags_is_rejected(self):
        self.native["routes"]["flags"] = 2
        self.reject()

    def test_getresult_outside_callback_is_rejected(self):
        self.native["observations"]["doneAfterCompletion"] = 0
        self.reject()

    def test_implicit_borrowed_close_is_rejected(self):
        self.native["result"] = self.native["result"].replace("borrowedCloses=0", "borrowedCloses=1")
        self.reject()

    def test_lost_exception_identity_is_rejected(self):
        self.native["observations"]["faultSameException"] = False
        self.reject()

    def test_lost_cause_identity_is_rejected(self):
        self.native["observations"]["faultSameCause"] = False
        self.reject()

    def test_changed_failure_phase_is_rejected(self):
        self.native["observations"]["failurePhases"][0] = "GetResult-source-fault"
        self.reject()

    def test_boolean_integer_alias_is_rejected(self):
        self.native["routes"]["flags"] = False
        self.reject()

    def test_integer_boolean_alias_is_rejected(self):
        self.native["observations"]["faultSameException"] = 1
        self.reject()

    def test_true_exitcode_alias_is_rejected(self):
        self.receipt["exitCode"] = False
        self.reject()

    def test_no_launch_receipt_is_rejected(self):
        self.receipt["processLaunched"] = False
        self.reject()

    def test_timeout_is_rejected(self):
        self.receipt["timedOut"] = True
        self.reject()

    def test_changed_java_bytes_are_rejected(self):
        self.java += b" "
        self.reject()

    def test_changed_input_hash_is_rejected(self):
        self.native["inputSha256"] = "d" * 64
        self.reject()

    def test_changed_source_receipt_is_rejected(self):
        self.receipt["oracleSourceSha256"] = "d" * 64
        self.reject()

    def test_raw_diagnostic_types_are_preserved(self):
        self.native["diagnostics"]["exceptions"][1]["type"] = "Different.Native.Exception"
        result = self.compare()
        self.assertEqual(result["nativeDiagnostics"]["exceptions"][1]["type"], "Different.Native.Exception")

    def test_unknown_field_is_rejected(self):
        self.native["skipMismatch"] = True
        self.reject()

    def test_duplicate_native_json_key_is_rejected(self):
        self.compare()
        path = self.root / "native.json"
        data = path.read_bytes().replace(b'"flags": 0', b'"flags": 0, "flags": 0')
        path.write_bytes(data)
        self.receipt["nativeEvidenceSha256"] = digest(data)
        (self.root / "receipt.json").write_text(json.dumps(self.receipt), encoding="utf-8")
        with self.assertRaises(self.module.ComparisonError):
            self.module.compare_files(*(self.root / n for n in ["java.json", "native.json", "receipt.json", "lock.json"]))


if __name__ == "__main__":
    unittest.main()
