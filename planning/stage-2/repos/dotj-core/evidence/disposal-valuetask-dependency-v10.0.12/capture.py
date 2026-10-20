"""Capture the direct ValueTask dependency of IAsyncDisposable."""

import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


COMMIT = "4271d88e0aebf3d04f188f1334c2220d80555ef6"
ARCHIVE_SHA256 = "ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115"
PREFIX = f"runtime-{COMMIT}/"
SOURCE = "src/libraries/System.Private.CoreLib/src/System/Threading/Tasks/ValueTask.cs"
SHARED = "src/libraries/System.Private.CoreLib/src/System.Private.CoreLib.Shared.projitems"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    raw_archive = args.archive.read_bytes()
    assert len(raw_archive) == 136239366 and sha(raw_archive) == ARCHIVE_SHA256
    with zipfile.ZipFile(args.archive) as archive:
        raw = archive.read(PREFIX + SOURCE)
        text = raw.decode("utf-8-sig")
        source_lines = text.splitlines()
        observations = {
            "nongenericDeclaration": "public readonly struct ValueTask : IEquatable<ValueTask>",
            "genericDeclaration": "public readonly struct ValueTask<TResult> : IEquatable<ValueTask<TResult>>",
            "taskConversion": "public Task AsTask()",
            "awaiter": "public ValueTaskAwaiter GetAwaiter()",
            "sourceBacker": "IValueTaskSource",
        }
        for needle in observations.values():
            assert needle in text
        shared_raw = archive.read(PREFIX + SHARED)
        shared = ET.fromstring(shared_raw)
        include = r"$(MSBuildThisFileDirectory)System\Threading\Tasks\ValueTask.cs"
        matches = [(group, item) for group in shared.findall(".//ItemGroup")
                   for item in group.findall("Compile") if item.get("Include") == include]
        assert len(matches) == 1
        assert "Condition" not in matches[0][0].attrib and "Condition" not in matches[0][1].attrib
        async_source = archive.read(PREFIX + "src/libraries/System.Private.CoreLib/src/System/IAsyncDisposable.cs")
        assert b"ValueTask DisposeAsync();" in async_source

    manifest = {
        "schemaVersion": 1,
        "sourceCommit": COMMIT,
        "sourceArchiveSha256": ARCHIVE_SHA256,
        "scope": "Direct return-type dependency of System.IAsyncDisposable.DisposeAsync",
        "valueTaskSource": {"path": SOURCE, "bytes": len(raw), "sha256": sha(raw)},
        "sharedProject": {"path": SHARED, "sha256": sha(shared_raw), "compileInclude": include, "directCondition": None},
        "iAsyncDisposableSourceSha256": sha(async_source),
        "observedSourceTokens": observations,
        "sourceLineCount": len(source_lines),
        "disposition": "IAsyncDisposable exact Java API deferred until the ValueTask lifecycle/awaiter representation and behavior oracle are resolved; CompletableFuture is not assumed equivalent.",
        "limits": [
            "This maps the immediate source dependency and selected source tokens, not the full ValueTask transitive dependency graph or semantics.",
            "No Java public IAsyncDisposable declaration or .j behavior is implemented in this batch.",
        ],
    }
    Path(__file__).with_name("manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("PASS: pinned IAsyncDisposable -> non-generic ValueTask direct dependency mapped")


if __name__ == "__main__":
    main()
