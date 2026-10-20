"""Check the Java public-visibility boundary for erased .NET overloads."""

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
LOWERING = EVIDENCE / "n01-java-erasure-lowering-v10.0.12.json"
OUTPUT = EVIDENCE / "n01-erasure-public-visibility-v10.0.12.json"


def java_source(root, name, source):
    path = root / (name.replace(".", "/") + ".java")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def compile_case(sources):
    with tempfile.TemporaryDirectory(prefix="dotj-erasure-visibility-") as folder:
        root = Path(folder)
        files = [java_source(root, name, source) for name, source in sources.items()]
        classes = root / "classes"
        classes.mkdir()
        result = subprocess.run(["javac", "--release", "21", "-d", str(classes),
                                 *(str(file) for file in files)], capture_output=True, text=True)
        visible = None
        if result.returncode == 0:
            inspection = subprocess.run(["javap", "-public", "-classpath", str(classes),
                                         "System.Threading.Tasks.Task"], capture_output=True, text=True)
            if inspection.returncode:
                raise RuntimeError("javap public-surface inspection failed: " + inspection.stderr)
            visible = inspection.stdout
        return result.returncode, result.stderr, visible


def main():
    lowering = json.loads(LOWERING.read_text(encoding="utf-8"))
    groups = [group for group in lowering["groups"]
              if group["declaringType"] == "System.Threading.Tasks.Task"
              and group["method"] == "FromException"]
    if len(groups) != 1 or len(groups[0]["members"]) != 2:
        raise ValueError("Expected pinned Task.FromException overload pair")
    plain = next(item for item in groups[0]["members"] if "[TResult]" not in item["metadataSignature"])
    generic = next(item for item in groups[0]["members"] if "[TResult]" in item["metadataSignature"])
    if not plain["backendName"].startswith("FromException__dotj_"):
        raise ValueError("Backend mapping changed")
    duplicate = {
        "System.Threading.Tasks.Task":
            "package System.Threading.Tasks; public class Task {"
            " public static Task FromException(java.lang.Exception error) { return null; }"
            " public static <TResult> Task_1<TResult> FromException(java.lang.Exception error) { return null; }"
            "}\n",
        "System.Threading.Tasks.Task_1":
            "package System.Threading.Tasks; public class Task_1<TResult> {}\n",
    }
    duplicate_exit, duplicate_error, _ = compile_case(duplicate)
    if duplicate_exit == 0 or "already defined" not in duplicate_error:
        raise RuntimeError("Unchanged public overload pair did not reproduce erasure error")
    hidden = {
        "System.Threading.Tasks.Task":
            "package System.Threading.Tasks; public class Task { static Task " + plain["backendName"]
            + "(java.lang.Exception error) { return null; } }\n",
        "fixture.Consumer":
            "package fixture; import System.Threading.Tasks.Task; public class Consumer {"
            " static void call(java.lang.Exception error) { Task." + plain["backendName"] + "(error); } }\n",
    }
    hidden_exit, hidden_error, _ = compile_case(hidden)
    if hidden_exit == 0 or "cannot be accessed from outside package" not in hidden_error:
        raise RuntimeError("Package-private backend was unexpectedly callable across packages")
    exposed = dict(hidden)
    exposed["System.Threading.Tasks.Task"] = hidden["System.Threading.Tasks.Task"].replace(
        "public class Task { static Task", "public class Task { public static Task")
    exposed_exit, exposed_error, public_surface = compile_case(exposed)
    if exposed_exit or plain["backendName"] not in public_surface:
        raise RuntimeError("Accessible backend did not appear in the public JVM surface: " + exposed_error)
    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "sourceCommit": lowering["sourceCommit"],
        "erasureLoweringSha256": hashlib.sha256(LOWERING.read_bytes()).hexdigest(),
        "representativeOverloads": [plain["metadataSignature"], generic["metadataSignature"]],
        "unchangedExactNamePair": "REJECTED: duplicate erased Java method signature",
        "packagePrivateBackendConsumer": "REJECTED: inaccessible from another package",
        "publicBackendConsumer": "COMPILED",
        "publicBackendVisibleToJavap": plain["backendName"],
        "disposition": "BLOCKED_PUBLIC_EXACT_NAME: a compiler or backend visibility strategy is needed before the mapped pair can be a qualified public .j contract",
        "scope": "Representative javac and javap feasibility check; not a general .j compiler implementation or behavior proof.",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS: exact pair rejected, hidden backend inaccessible, public backend visibly exposes mapped name")


if __name__ == "__main__":
    main()
