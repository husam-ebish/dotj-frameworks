"""Capture selected cancellation/task public metadata and pinned source provenance."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path("R:/")
OUTPUT = ROOT / "planning/stage-2/repos/dotj-core/evidence/wp02-api-shapes-v10.0.12"
CORELIB_HASH = "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"
PIN = "4271d88e0aebf3d04f188f1334c2220d80555ef6"
BASE = "src/libraries/System.Private.CoreLib/src/System/Threading/"
TYPES = {
    "cancellation-token": ("System.Threading.CancellationToken", BASE + "CancellationToken.cs", "public readonly struct CancellationToken"),
    "cancellation-source": ("System.Threading.CancellationTokenSource", BASE + "CancellationTokenSource.cs", "public class CancellationTokenSource"),
    "cancellation-registration": ("System.Threading.CancellationTokenRegistration", BASE + "CancellationTokenRegistration.cs", "public readonly struct CancellationTokenRegistration"),
    "task": ("System.Threading.Tasks.Task", BASE + "Tasks/Task.cs", "public class Task :"),
    "task-generic": ("System.Threading.Tasks.Task`1", BASE + "Tasks/Future.cs", "public class Task<TResult>"),
    "task-completion-source": ("System.Threading.Tasks.TaskCompletionSource", BASE + "Tasks/TaskCompletionSource.cs", "public class TaskCompletionSource"),
    "task-completion-source-generic": ("System.Threading.Tasks.TaskCompletionSource`1", BASE + "Tasks/TaskCompletionSource_T.cs", "public class TaskCompletionSource<TResult>"),
}


def capture(key):
    full_name, source_path, anchor = TYPES[key]
    source = SOURCE / source_path
    content = source.read_text(encoding="utf-8-sig")
    assert content.startswith("// Licensed to the .NET Foundation")
    assert anchor in content
    oracle = ROOT / "tools/oracle/dotj-core/api-shape/ApiShapeOracle.csproj"
    run = subprocess.run(["dotnet", "run", "--project", str(oracle), "--configuration", "Release", "--no-build", "--no-launch-profile", "--", full_name], cwd=ROOT, text=True, capture_output=True, check=True)
    snapshot = json.loads(run.stdout)
    assert snapshot["assemblySha256"] == CORELIB_HASH
    assert snapshot["type"]["fullName"] == full_name
    assert snapshot["runtimeVersion"] == "10.0.12"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    snapshot_path = OUTPUT / f"{key}.json"
    snapshot_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    provenance = {
        "schemaVersion": 1,
        "sourceRepository": "https://github.com/dotnet/runtime",
        "sourceCommit": PIN,
        "sourcePath": source_path,
        "sourceSha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "sourceDeclarationAnchor": anchor,
        "artifact": "Microsoft.NETCore.App 10.0.12 System.Private.CoreLib",
        "artifactSha256": CORELIB_HASH,
        "snapshotPath": f"{key}.json",
        "snapshotSha256": hashlib.sha256(snapshot_path.read_bytes()).hexdigest(),
        "publicDeclaredMethodCount": len(snapshot["type"]["methods"]),
        "publicDeclaredPropertyCount": len(snapshot["type"]["properties"]),
        "limits": ["Installed CoreLib declared-public metadata only; source conditionals and inherited APIs require separate checks.", "No Java public API or behavior is qualified by this snapshot."],
    }
    provenance_path = OUTPUT / f"{key}-provenance.json"
    provenance_path.write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"PASS {full_name}: {provenance['publicDeclaredMethodCount']} methods, {provenance['publicDeclaredPropertyCount']} properties")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("key", choices=sorted(TYPES))
    capture(parser.parse_args().key)
