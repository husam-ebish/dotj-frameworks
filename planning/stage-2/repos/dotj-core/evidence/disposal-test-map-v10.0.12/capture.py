"""Map selected actual upstream disposal tests to the WP-01 fixture needs."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile


COMMIT = "4271d88e0aebf3d04f188f1334c2220d80555ef6"
ARCHIVE_SHA256 = "ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115"
PREFIX = f"runtime-{COMMIT}/"
FILES = {
    "src/libraries/System.Runtime/tests/System.Threading.Tasks.Tests/System.Runtime.CompilerServices/ConfiguredAsyncDisposable.cs": [
        ("Default_GetAsyncEnumerator_Throws", "Fact", 1, "Supplemental default-wrapper failure; no direct F01 case"),
        ("DisposeAsync_InvokesUnderlyingDisposeAsync", "Theory", 2, "Supplemental async dispatch; does not establish caller-owned resource rule F01-03"),
        ("DisposeAsync_ContinuesOnCapturedContextIfExpected", "Theory", 2, "Related to context scheduling, but does not establish F01-04 cross-request isolation"),
    ],
    "src/libraries/System.Runtime/tests/System.IO.Tests/Stream/Stream.DisposeAsync.cs": [
        ("DisposeAsync_MultipleDisposalSuccessful", "Fact", 1, "Stream-specific repeat-disposal; not a guarantee of IAsyncDisposable implementations"),
        ("DisposeAsync_InvokesDisposeSynchronously", "Fact", 1, "Stream-specific default behavior; not general interface behavior"),
    ],
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    raw_archive = args.archive.read_bytes()
    assert len(raw_archive) == 136239366 and sha(raw_archive) == ARCHIVE_SHA256
    files = []
    cases = []
    with zipfile.ZipFile(args.archive) as archive:
        for path, expected in FILES.items():
            raw = archive.read(PREFIX + path)
            lines = raw.decode("utf-8-sig").splitlines()
            files.append({"path": path, "bytes": len(raw), "sha256": sha(raw)})
            for name, attribute, case_count, relevance in expected:
                matches = [i for i, line in enumerate(lines, 1)
                           if re.search(r"\bpublic (?:async Task|void) " + re.escape(name) + r"\(", line)]
                assert len(matches) == 1
                line_number = matches[0]
                preceding = "\n".join(lines[max(0, line_number - 5):line_number - 1])
                assert "[" + attribute + "]" in preceding
                if attribute == "Theory":
                    assert preceding.count("[InlineData(") == case_count
                cases.append({
                    "sourcePath": path,
                    "method": name,
                    "line": line_number,
                    "attribute": attribute,
                    "declaredCaseCount": case_count,
                    "relationToDesignedFixtures": relevance,
                })

    manifest = {
        "schemaVersion": 1,
        "sourceCommit": COMMIT,
        "sourceArchiveSha256": ARCHIVE_SHA256,
        "scope": "Selected pinned upstream disposal tests relevant to WP-01 oracle planning",
        "files": files,
        "testMethods": cases,
        "testMethodCount": len(cases),
        "declaredCaseCount": sum(case["declaredCaseCount"] for case in cases),
        "directCoverageOfDesignedF01Cases": [],
        "executionStatus": "NOT RUN",
        "limits": [
            "These are source-verified test method IDs and declared theory rows, not runtime discovery or executed results.",
            "The selected tests do not directly prove ownership of caller-supplied resources or cross-request context isolation.",
            "This is a bounded mapping, not a complete upstream disposal-test census.",
        ],
    }
    Path(__file__).with_name("manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Mapped {len(cases)} upstream methods and {manifest['declaredCaseCount']} declared cases; none run")


if __name__ == "__main__":
    main()
