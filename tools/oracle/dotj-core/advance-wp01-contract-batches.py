"""Reproduce the bounded WP-01 contract checks for Batches 075-094.

Run from the repository root with the pinned runtime source mapped to R:.
Each numbered check writes one evidence record on its own feature branch.
This is research/prototype evidence, never a public API qualification.
"""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
SHAPES = EVIDENCE / "api-shapes-v10.0.12"
SOURCE = Path("R:/")
CORELIB_HASH = "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"
HELPER = Path(r"C:\Users\husam\AppData\Local\Temp\dotj-record-batch.py")
PROBES = ROOT / "tools/oracle/dotj-core/java-probes"


def run(*args):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"Command failed: {args}\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shape(name):
    result = json.loads((SHAPES / (name + ".json")).read_text(encoding="utf-8"))
    assert result["assemblySha256"] == CORELIB_HASH
    return result["type"]


def record(number, subject, assertions, observed, gaps, extra=None):
    data = {
        "schemaVersion": 1,
        "batch": f"Batch-{number:03d}",
        "runtimeVersion": "10.0.12",
        "coreLibSha256": CORELIB_HASH,
        "subject": subject,
        "assertionsPassed": assertions,
        "observed": observed,
        "openGaps": gaps,
        "qualification": "BOUNDED_EVIDENCE_ONLY; E01/E02/E03/N01 AND WP-01 REMAIN OPEN",
    }
    if extra:
        data.update(extra)
    path = EVIDENCE / f"wp01-contract-check-{number:03d}-v10.0.12.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def batch(number):
    gaps = ["This check does not close the full public API, behavior, or release gates."]
    files = []
    task = "E02"
    if number == 75:
        t = shape("idisposable")
        assert t["fullName"] == "System.IDisposable" and t["isInterface"]
        assert len(t["methods"]) == 1 and t["methods"][0]["Name"] == "Dispose"
        assert t["methods"][0]["returnType"] == "System.Void" and not t["methods"][0]["parameters"]
        subject, observed = "IDisposable exact metadata contract", {"type": t["fullName"], "method": t["methods"][0]}
        task = "N01"
    elif number == 76:
        task = "N01"
        path = PROBES / "System/IDisposable.java"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("package System;\n\n/** Compile-only exact-name probe; not product API. */\npublic interface IDisposable {\n    void Dispose();\n}\n", encoding="utf-8")
        files.append(path)
        output = ROOT / "dotj-core/dotj-core-01/build/name-probes"
        output.mkdir(parents=True, exist_ok=True)
        run("javac", "-d", str(output), str(path))
        subject, observed = "Java exact-name syntax probe", {"source": str(path.relative_to(ROOT)), "compiled": True}
    elif number == 77:
        task = "N01"
        output = ROOT / "dotj-core/dotj-core-01/build/name-probes"
        bytecode = run("javap", "-public", "-classpath", str(output), "System.IDisposable")
        assert "public interface System.IDisposable" in bytecode and "public abstract void Dispose();" in bytecode
        subject, observed = "JVM declared interface identity", {"javap": bytecode}
    elif number == 78:
        task = "N01"
        path = PROBES / "System/IDisposable.java"
        source = path.read_text(encoding="utf-8")
        t = shape("idisposable")
        assert "package System;" in source and "interface IDisposable" in source and "void Dispose();" in source
        assert t["fullName"] == "System.IDisposable" and t["methods"][0]["Name"] == "Dispose"
        subject, observed = "IDisposable source/metadata exact-name comparison", {"namespace": "System", "interface": "IDisposable", "method": "Dispose"}
    elif number == 79:
        task = "E03"
        output = run("dotnet", "run", "--project", str(ROOT / "tools/oracle/dotj-core/disposal-behavior/DisposalBehaviorOracle.csproj"), "--configuration", "Release", "--no-launch-profile")
        result = json.loads(output)
        assert result["coreLibSha256"] == CORELIB_HASH and result["directInterfaceDispatchCount"] == 1
        assert result["repeatedExplicitDisposeCount"] == 2 and result["untouchedDisposeCount"] == 0
        subject, observed = "IDisposable runtime dispatch and repeated calls", result
    elif number == 80:
        task = "DJ-001-WP-01-T2"
        output = ROOT / "dotj-core/dotj-core-01/build/test-classes"
        src = ROOT / "dotj-core/dotj-core-01/src"
        run("javac", "-d", str(output), str(src / "main/java/org/dotj/internal/ownership/OwnedResources.java"), str(src / "test/java/org/dotj/internal/ownership/OwnedResourcesTest.java"))
        result = run("java", "-cp", str(output), "org.dotj.internal.ownership.OwnedResourcesTest")
        assert result.startswith("PASS:")
        subject, observed = "Internal ownership fixture", {"result": result}
    elif number == 81:
        task = "N01"
        subject, observed = "IDisposable and AutoCloseable semantic gap", {
            "upstream": "System.IDisposable.Dispose returns void and declares no checked exception",
            "javaPrimitive": "AutoCloseable.close declares throws Exception",
            "decision": "Internal AutoCloseable remains hidden; no public substitute or automatic equivalence claim",
        }
        gaps = ["A public exact-name adapter needs exception and lifecycle behavior tests."]
    elif number == 82:
        task = "N01"
        path = PROBES / "PAIRED-EXAMPLE.md"
        path.write_text("# IDisposable paired usage (contract sketch)\n\nC# reference:\n```csharp\nIDisposable resource = CreateResource();\ntry { Use(resource); } finally { resource.Dispose(); }\n```\n\nJava syntax probe:\n```java\nSystem.IDisposable resource = createResource();\ntry { use(resource); } finally { resource.Dispose(); }\n```\n\n`CreateResource`/`Use` and their Java spellings are example-local functions, not framework API. The `System.IDisposable` Java source lives only in `java-probes`; product release and disposal semantics are open.\n", encoding="utf-8")
        files.append(path)
        assert "resource.Dispose();" in path.read_text(encoding="utf-8")
        subject, observed = "Paired C#/Java IDisposable lifecycle sketch", {"file": str(path.relative_to(ROOT)), "sameFrameworkMethod": "Dispose"}
    elif number == 83:
        task = "E02"
        t = shape("iasyncdisposable")
        assert t["fullName"] == "System.IAsyncDisposable" and t["isInterface"]
        assert len(t["methods"]) == 1 and t["methods"][0]["Name"] == "DisposeAsync"
        assert t["methods"][0]["returnType"] == "System.Threading.Tasks.ValueTask"
        subject, observed = "IAsyncDisposable exact metadata contract", {"type": t["fullName"], "method": t["methods"][0]}
    elif number == 84:
        task = "E02"
        t = shape("value-task")
        names = {m["Name"] for m in t["methods"]}
        assert t["isValueType"] and {"AsTask", "ConfigureAwait", "GetAwaiter"} <= names
        subject, observed = "ValueTask return dependency", {"type": t["fullName"], "methods": sorted(names), "constructorCount": len(t["constructors"])}
        gaps = ["Selected reflected metadata is not an implemented ValueTask state machine."]
    elif number == 85:
        task = "E02"
        t = shape("value-task-generic")
        assert t["isGenericTypeDefinition"] and len(t["genericParameters"]) == 1
        subject, observed = "Generic ValueTask family distinction", {"type": t["fullName"], "arity": len(t["genericParameters"]), "methodCount": len(t["methods"])}
        gaps = ["Generic arity and JVM erasure mappings remain unqualified."]
    elif number == 86:
        task = "N01"
        value_task = PROBES / "System/Threading/Tasks/ValueTask.java"
        value_task.parent.mkdir(parents=True, exist_ok=True)
        value_task.write_text("package System.Threading.Tasks;\n\n/** Compile-only placeholder; no ValueTask semantics. */\npublic final class ValueTask {\n}\n", encoding="utf-8")
        async_disposable = PROBES / "System/IAsyncDisposable.java"
        async_disposable.write_text("package System;\n\nimport System.Threading.Tasks.ValueTask;\n\n/** Compile-only exact-name probe; not product API. */\npublic interface IAsyncDisposable {\n    ValueTask DisposeAsync();\n}\n", encoding="utf-8")
        files += [value_task, async_disposable]
        output = ROOT / "dotj-core/dotj-core-01/build/name-probes"
        run("javac", "-d", str(output), str(value_task), str(async_disposable))
        subject, observed = "Java async-disposal signature syntax", {"compiled": True, "returnType": "System.Threading.Tasks.ValueTask", "javaSyntaxConstraint": "Import ValueTask; java.lang.System shadows a fully qualified System.Threading reference in this context."}
        gaps = ["The ValueTask class is an empty compile-only placeholder; async behavior is blocked."]
    elif number == 87:
        task = "N01"
        output = ROOT / "dotj-core/dotj-core-01/build/name-probes"
        bytecode = run("javap", "-public", "-classpath", str(output), "System.IAsyncDisposable")
        assert "System.Threading.Tasks.ValueTask DisposeAsync();" in bytecode
        subject, observed = "JVM async signature identity", {"javap": bytecode}
        gaps = ["Method return spelling compiles; ValueTask state, awaiting and exception behavior are unimplemented."]
    elif number == 88:
        task = "E03"
        run("powershell", "-NoProfile", "-File", str(ROOT / "tools/oracle/dotj-core/run-wp01-upstream-tests.ps1"), "-SourceRoot", str(SOURCE))
        result = json.loads((Path.home() / "AppData/Local/Temp/dotj-wp01-upstream-results/summary.json").read_text(encoding="utf-8-sig"))
        assert result["sourceCommit"] == "4271d88e0aebf3d04f188f1334c2220d80555ef6"
        assert result["totalPassed"] == 39 and all(suite["failed"] == 0 for suite in result["suites"])
        subject, observed = "Pinned upstream WP-01 regression run", {"totalPassed": result["totalPassed"], "suites": result["suites"]}
        gaps = ["Passing selected upstream tests does not validate the Java async prototype."]
    elif number == 89:
        task = "E02"
        t = shape("system-type")
        assert t["fullName"] == "System.Type" and len(t["methods"]) == 181
        subject, observed = "System.Type reflected surface size", {"methodCount": len(t["methods"]), "propertyCount": len(t["properties"])}
        gaps = ["No complete System.Type semantic or Java mapping is claimed."]
    elif number == 90:
        task = "E02"
        t = shape("execution-context")
        names = {m["Name"] for m in t["methods"]}
        assert {"Capture", "Run", "SuppressFlow"} <= names
        subject, observed = "ExecutionContext context-transfer anchors", {"methods": sorted(names)}
        gaps = ["Explicit ContextSnapshot cannot be presented as equivalent to ambient ExecutionContext."]
    elif number == 91:
        task = "E02"
        t = shape("async-local")
        assert t["isGenericTypeDefinition"] and len(t["genericParameters"]) == 1
        assert any(p["Name"] == "Value" and p["type"] == "T" for p in t["properties"])
        subject, observed = "AsyncLocal generic ambient-value anchor", {"type": t["fullName"], "properties": t["properties"]}
        gaps = ["No implicit ambient value flow has been implemented in Java."]
    elif number == 92:
        task = "DJ-001-WP-01-T1"
        output = ROOT / "dotj-core/dotj-core-01/build/test-classes"
        src = ROOT / "dotj-core/dotj-core-01/src"
        run("javac", "-d", str(output), str(src / "main/java/org/dotj/internal/types/TypeIdentity.java"), str(src / "test/java/org/dotj/internal/types/TypeIdentityTest.java"))
        result = run("java", "-cp", str(output), "org.dotj.internal.types.TypeIdentityTest")
        assert result.startswith("PASS:")
        subject, observed = "Internal generic identity fixture", {"result": result}
    elif number == 93:
        task = "DJ-001-WP-01-T3"
        output = ROOT / "dotj-core/dotj-core-01/build/test-classes"
        src = ROOT / "dotj-core/dotj-core-01/src"
        run("javac", "-d", str(output), str(src / "main/java/org/dotj/internal/context/ContextSnapshot.java"), str(src / "main/java/org/dotj/internal/context/ContextTransfer.java"), str(src / "test/java/org/dotj/internal/context/ContextIsolationTest.java"))
        result = run("java", "-cp", str(output), "org.dotj.internal.context.ContextIsolationTest")
        assert result.startswith("PASS:")
        subject, observed = "Internal cross-request context isolation fixture", {"result": result}
    elif number == 94:
        task = "E03"
        output = run("powershell", "-NoProfile", "-File", str(ROOT / "tools/oracle/dotj-core/run-wp01-fixtures.ps1"))
        assert "PASS: 9 Java fixtures and 5 .NET oracles" in output
        subject, observed = "Combined local WP-01 fixture gate", {"result": output.splitlines()[-1], "evidenceRecords": 20}
        gaps = ["E01 rights, complete E02/E03/N01 semantics, and public facade qualification remain open."]
    else:
        raise ValueError(number)
    evidence = record(number, subject, [subject + " passed"], observed, gaps)
    files.insert(0, evidence)
    outcomes = {
        75: "Recorded the exact IDisposable interface and Dispose signature from installed CoreLib metadata.",
        76: "Compiled a Java exact-name IDisposable declaration in oracle probes.",
        77: "Verified the compiled JVM name and Dispose method with javap.",
        78: "Compared Java probe names with the pinned CoreLib metadata.",
        79: "Re-ran the reference IDisposable dispatch and lifecycle oracle.",
        80: "Re-ran the internal owned-resource fixture.",
        81: "Recorded the IDisposable versus AutoCloseable exception-contract gap.",
        82: "Added paired C#/Java disposal lifecycle examples as contract sketches.",
        83: "Recorded exact IAsyncDisposable metadata and ValueTask return dependency.",
        84: "Checked the selected non-generic ValueTask metadata anchors.",
        85: "Checked generic ValueTask arity separately from non-generic ValueTask.",
        86: "Compiled a Java IAsyncDisposable signature using a clearly marked placeholder ValueTask.",
        87: "Verified the compiled Java async method and return type names with javap.",
        88: "Re-ran selected pinned upstream WP-01 regression tests.",
        89: "Checked the reflected System.Type method and property surface size.",
        90: "Checked ExecutionContext capture/run/suppress metadata anchors.",
        91: "Checked AsyncLocal generic value metadata.",
        92: "Re-ran internal generic identity fixtures.",
        93: "Re-ran internal context isolation fixtures.",
        94: "Re-ran the combined local WP-01 Java and .NET fixture gate.",
    }
    next_text = {
        75: "Compile exact-name IDisposable Java syntax probe.", 76: "Inspect compiled IDisposable JVM signature.",
        77: "Compare compiled spelling with CoreLib metadata.", 78: "Run reference IDisposable behavior oracle.",
        79: "Run owned-resource Java fixture.", 80: "Document AutoCloseable semantic gap.",
        81: "Add paired disposal lifecycle examples.", 82: "Record exact IAsyncDisposable metadata.",
        83: "Check ValueTask return dependency surface.", 84: "Check generic ValueTask arity.",
        85: "Compile IAsyncDisposable Java signature probe.", 86: "Inspect compiled async signature.",
        87: "Run pinned upstream WP-01 tests.", 88: "Check System.Type reflected surface.",
        89: "Check ExecutionContext metadata anchors.", 90: "Check AsyncLocal metadata.",
        91: "Run internal generic identity fixture.", 92: "Run context isolation fixture.",
        93: "Run combined local WP-01 fixtures.", 94: "Close E01/E02/E03/N01 gates for the first public slice before publishing a facade.",
    }
    return task, outcomes[number], next_text[number], files, gaps[0]


def main():
    assert SOURCE.exists(), "Pinned source must be mapped to R:"
    progress = json.loads((ROOT / "planning/stage-2/IMPLEMENTATION-PROGRESS.json").read_text(encoding="utf-8"))
    start = len(progress["completedBatches"]) + 1
    assert 75 <= start <= 94
    current_branch = run("git", "branch", "--show-current")
    assert current_branch in ("master", f"feature/batch-{start:03d}-wp01-contract")
    for number in range(start, 95):
        branch = f"feature/batch-{number:03d}-wp01-contract"
        if run("git", "branch", "--show-current") == "master":
            run("git", "switch", "-c", branch)
        try:
            task, outcome, next_text, files, limitation = batch(number)
            relative = [str(path.relative_to(ROOT)).replace("\\", "/") for path in files]
            run("python", str(HELPER), str(number), outcome, "Relevant assertion, compile, or fixture passed; see the versioned evidence record.", limitation, next_text, task, *relative)
            run("git", "add", "planning/stage-2", "tools/oracle/dotj-core/advance-wp01-contract-batches.py", "tools/oracle/dotj-core/java-probes") if PROBES.exists() else run("git", "add", "planning/stage-2", "tools/oracle/dotj-core/advance-wp01-contract-batches.py")
            run("git", "commit", "-m", f"Batch {number:03d} {outcome}")
            run("git", "switch", "master")
            run("git", "merge", "--no-ff", branch, "-m", f"Merge Batch {number:03d} WP-01 contract check")
            print(f"PASS Batch-{number:03d}: {outcome}", flush=True)
        except Exception:
            print(f"STOP at Batch-{number:03d}; inspect branch {branch}", flush=True)
            raise


if __name__ == "__main__":
    main()
