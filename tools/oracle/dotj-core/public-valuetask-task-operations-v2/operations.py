"""Fixed-mode operational adapters. Imports are lazy; parsing never dispatches execution."""
import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
FROZEN = Path("D:/AI/Implementation/dotj Frameworks/worktrees/dotj-core-valuetask-task-v1/tools/oracle/dotj-core/public-valuetask-task-v1")
PRODUCT = FROZEN.parent / "public-valuetask-task-product-v1"
VERIFY_PATHS = ("lock", "checkpoint", "receipt", "java-lock", "candidate-jar", "observation-lock")
VERIFY_HASHES = ("lock-sha256", "checkpoint-sha256", "receipt-sha256", "java-lock-sha256", "candidate-sha256", "observation-lock-sha256")
BOUNDARY_PATHS = ("out", "candidate-jar", "java-lock")
BOUNDARY_HASHES = ("candidate-sha256", "java-lock-sha256")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frozen_library():
    return load(FROZEN / "run-comparison.py", "valuetask_frozen_receipts")


def product_library():
    return load(PRODUCT / "product_runner_v3.py", "valuetask_qualified_boundaries")


def parser(kind):
    if kind not in ("verify", "boundaries"):
        raise ValueError("unsupported operational command")
    p = argparse.ArgumentParser(allow_abbrev=False)
    paths = VERIFY_PATHS if kind == "verify" else BOUNDARY_PATHS
    hashes = VERIFY_HASHES if kind == "verify" else BOUNDARY_HASHES
    required = {"lock", "checkpoint", "receipt", "lock-sha256", "checkpoint-sha256", "receipt-sha256"} if kind == "verify" else set(paths + hashes)
    for field in paths:
        p.add_argument("--" + field, type=Path, required=field in required)
    for field in hashes:
        p.add_argument("--" + field, required=field in required)
    if kind == "boundaries":
        p.add_argument("--execute-reviewed", action="store_true", required=True)
    return p


def parse_verify(argv):
    a = parser("verify").parse_args(argv)
    a.mode = "verify"
    return a


def parse_boundaries(argv):
    a = parser("boundaries").parse_args(argv)
    a.mode = "boundaries"
    return a


def verify(argv=None, loader=frozen_library):
    a = parse_verify(argv)
    # Direct receipt validation only: never call the library's CLI/controller/execute.
    return loader().verify_receipt(a)


def boundary_arguments(a):
    # Equals form binds selector-like values to their named options, never as new flags.
    return ["--" + field + "=" + str(getattr(a, field.replace("-", "_")))
            for field in BOUNDARY_PATHS + BOUNDARY_HASHES] + ["--execute-reviewed"]


def boundary_child_argv(a, python):
    code = "import sys;sys.path.insert(0," + repr(str(HERE)) + ");import operations;operations.child_main()"
    return [str(python), "-B", "-c", code, *boundary_arguments(a)]


def validate_boundary_inputs(a, backend):
    c = backend.c
    c.require(a.mode == "boundaries" and a.execute_reviewed, "reviewed fixed boundaries request")
    c.require(c.sha(a.java_lock) == a.java_lock_sha256, "Java lock hash")
    lock = c.read(a.java_lock)
    c.require(lock["candidateJar"] == c.descriptor(a.candidate_jar)
              and c.sha(a.candidate_jar) == a.candidate_sha256, "candidate/Java lock binding")
    for pin in lock["pins"]:
        c.pin(pin)
    qualified = PRODUCT / "ValueTaskTaskBoundaryControls.java"
    c.require(any(Path(pin["path"]).resolve() == qualified.resolve()
                  and pin["sha256"] == c.sha(qualified) for pin in lock["pins"]),
              "qualified Java-only successor must be locked")


def execute_boundaries(a, backend):
    validate_boundary_inputs(a, backend)
    # The qualified coordinator has no native execution mode. Only its boundary
    # group is selected; the original uncompilable fixture is never selected.
    request = SimpleNamespace(mode="groups", only="valuetask-boundaries", out=a.out,
                              jar=a.candidate_jar, jar_sha256=a.candidate_sha256)
    return backend.inner(request)


def boundaries(argv=None, loader=product_library):
    a = parse_boundaries(argv)
    backend = loader()
    validate_boundary_inputs(a, backend)
    c = backend.c
    a.out = c.confined(a.out)
    backend.prepare(a.out)
    c.write(a.out / "inputs.json", backend.inputs(a.candidate_jar))
    argv = boundary_child_argv(a, c.PYTHON)
    c.write(a.out / "controller.json", {"status": "PREPARING", "argv": argv})
    result = backend.launch(argv, a.out, "controller", 600, time.monotonic() + 725,
                            lambda value: c.write(a.out / "controller.json", value))
    c.write(a.out / "controller.json", result)
    c.successful(result)
    receipt = c.read(a.out / "receipt.json")
    c.require(receipt["status"] == "PASS_STAGED_GROUPS"
              and [g["name"] for g in receipt["groups"]] == ["valuetask-boundaries"],
              "only qualified boundary group may complete")
    return {"status": receipt["status"], "receipt": c.descriptor(a.out / "receipt.json")}


def child_main(argv=None, loader=product_library):
    # Private parent protocol: the public command has no --inner option. The same
    # closed parser assigns boundaries again, without receiving any mode selector.
    a = parse_boundaries(argv)
    backend = loader()
    backend.c.require((a.out / "controller.json").is_file(), "owned parent record required")
    result = execute_boundaries(a, backend)
    print(json.dumps({"status": result["status"]}))


def main_verify(argv=None):
    print(json.dumps(verify(argv)))


def main_boundaries(argv=None):
    print(json.dumps(boundaries(argv)))
