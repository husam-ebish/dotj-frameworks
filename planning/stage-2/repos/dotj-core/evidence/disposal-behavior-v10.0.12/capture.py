"""Build and retain independent .NET 10 synchronous disposal observations."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


CORELIB_SHA256 = "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"
EXPECTED = {
    "directInterfaceDispatchCount": 1,
    "normalUsingDisposeCount": 1,
    "bodyFailureDisposeCount": 1,
    "bodyFailureObserved": "body",
    "disposeFailureDisposeCount": 1,
    "disposeFailureObserved": "dispose",
    "repeatedExplicitDisposeCount": 2,
    "untouchedDisposeCount": 0,
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    project = args.repo_root / "tools/oracle/dotj-core/disposal-behavior"
    evidence = Path(__file__).parent
    build = subprocess.run(["dotnet", "build", "-c", "Release"], cwd=project,
                           capture_output=True, text=True, check=True)
    assert "0 Warning(s)" in build.stdout and "0 Error(s)" in build.stdout
    run = subprocess.run(["dotnet", "run", "--no-build", "-c", "Release"], cwd=project,
                         capture_output=True, text=True, check=True)
    output = json.loads(run.stdout)
    assert output["runtimeVersion"] == "10.0.12"
    assert output["coreLibSha256"] == CORELIB_SHA256
    assert all(output[key] == value for key, value in EXPECTED.items())

    log = build.stdout.replace("\r\n", "\n")
    output_bytes = (json.dumps(output, indent=2) + "\n").encode("utf-8")
    (evidence / "build-log.txt").write_text(log, encoding="utf-8", newline="\n")
    (evidence / "oracle-output.json").write_bytes(output_bytes)
    manifest = {
        "schemaVersion": 1,
        "scope": "Independent synchronous IDisposable/using behavior oracle on installed .NET 10.0.12",
        "projectSha256": sha((project / "DisposalBehaviorOracle.csproj").read_bytes()),
        "programSha256": sha((project / "Program.cs").read_bytes()),
        "countingDisposableSha256": sha((project / "CountingDisposable.cs").read_bytes()),
        "buildCommand": "dotnet build -c Release",
        "runCommand": "dotnet run --no-build -c Release",
        "buildWarnings": 0,
        "buildErrors": 0,
        "buildLogSha256": sha(log.encode("utf-8")),
        "oracleOutputSha256": sha(output_bytes),
        "coreLibSha256": CORELIB_SHA256,
        "observations": EXPECTED,
        "limits": [
            "This independently tests C# interface dispatch and using/finally behavior; the mapped upstream xUnit suite was not executed.",
            "Repeated Dispose count of two demonstrates this sample implementation is not idempotent; the interface alone does not enforce the source comment guidance.",
            "The oracle does not establish designed F01-03 caller ownership, F01-04 cross-request context isolation, or asynchronous ValueTask behavior.",
        ],
    }
    (evidence / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("PASS: zero-warning build and eight synchronous disposal observations")


if __name__ == "__main__":
    main()
