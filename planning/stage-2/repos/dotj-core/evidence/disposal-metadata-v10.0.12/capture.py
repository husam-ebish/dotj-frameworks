"""Build and capture the pinned disposal interface metadata oracle."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


CORELIB_SHA256 = "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    project_dir = args.repo_root / "tools/oracle/dotj-core/disposal-metadata"
    evidence = Path(__file__).parent

    build = subprocess.run(
        ["dotnet", "build", "-c", "Release"], cwd=project_dir,
        capture_output=True, text=True, check=True,
    )
    assert "0 Warning(s)" in build.stdout and "0 Error(s)" in build.stdout
    run = subprocess.run(
        ["dotnet", "run", "--no-build", "-c", "Release"], cwd=project_dir,
        capture_output=True, text=True, check=True,
    )
    output = json.loads(run.stdout)
    assert output["runtimeVersion"] == "10.0.12"
    assert output["assemblyName"] == "System.Private.CoreLib"
    assert output["assemblySha256"] == CORELIB_SHA256
    assert [(item["fullName"], [(method["name"], method["returnType"], method["parameterTypes"])
             for method in item["methods"]]) for item in output["interfaces"]] == [
        ("System.IDisposable", [("Dispose", "System.Void", [])]),
        ("System.IAsyncDisposable", [("DisposeAsync", "System.Threading.Tasks.ValueTask", [])]),
    ]
    assert all(item["isPublic"] and item["isInterface"] for item in output["interfaces"])
    assert all(method["isPublic"] and method["isAbstract"]
               for item in output["interfaces"] for method in item["methods"])

    build_log = build.stdout.replace("\r\n", "\n")
    output_bytes = (json.dumps(output, indent=2) + "\n").encode("utf-8")
    (evidence / "build-log.txt").write_text(build_log, encoding="utf-8", newline="\n")
    (evidence / "oracle-output.json").write_bytes(output_bytes)
    manifest = {
        "schemaVersion": 1,
        "scope": "Installed .NET 10.0.12 CoreLib disposal interface metadata",
        "project": "tools/oracle/dotj-core/disposal-metadata/DisposalMetadataOracle.csproj",
        "projectSha256": sha((project_dir / "DisposalMetadataOracle.csproj").read_bytes()),
        "programSha256": sha((project_dir / "Program.cs").read_bytes()),
        "buildCommand": "dotnet build -c Release",
        "runCommand": "dotnet run --no-build -c Release",
        "buildExitCode": build.returncode,
        "runExitCode": run.returncode,
        "buildWarnings": 0,
        "buildErrors": 0,
        "buildLogSha256": sha(build_log.encode("utf-8")),
        "oracleOutputSha256": sha(output_bytes),
        "coreLibSha256": CORELIB_SHA256,
        "interfaceCount": len(output["interfaces"]),
        "limits": [
            "The installed binary hash was previously matched to the official win-x64 runtime artifact; this probes that local profile only.",
            "Metadata confirms signatures, not Dispose or DisposeAsync behavioral semantics, ownership rules or Java representation.",
        ],
    }
    (evidence / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("PASS: zero-warning build; two interface signatures matched pinned CoreLib metadata")


if __name__ == "__main__":
    main()
