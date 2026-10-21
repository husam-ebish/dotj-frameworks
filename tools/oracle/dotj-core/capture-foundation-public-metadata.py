"""Capture selected public metadata from the pinned installed CoreLib."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
PROJECT = ROOT / "tools/oracle/dotj-core/foundation-public-metadata/FoundationPublicMetadata.csproj"
PROGRAM = PROJECT.with_name("Program.cs")
OUTPUT = EVIDENCE / "foundation-selected-metadata-v10.0.12.json"


def main():
    result = subprocess.run(["dotnet", "run", "--project", str(PROJECT),
                             "--configuration", "Release", "--no-launch-profile"],
                            cwd=ROOT, capture_output=True, text=True, check=True)
    record = json.loads(result.stdout)
    baseline = json.loads((EVIDENCE / "api-shapes-v10.0.12/system-type.json").read_text(encoding="utf-8"))
    assert record["runtimeVersion"] == "10.0.12"
    assert record["coreLibSha256"] == baseline["assemblySha256"]
    by_name = {item["fullName"]: item for item in record["types"]}
    assert len(by_name) == 22
    assert by_name["System.IDisposable"]["declaredPublicMethodCount"] == 1
    assert by_name["System.Type"]["declaredPublicPropertyCount"] == 70
    assert by_name["System.Type"]["baseType"] == "System.Reflection.MemberInfo"
    assert by_name["System.Reflection.MemberInfo"]["baseType"] == "System.Object"
    assert by_name["System.ArgumentNullException"]["baseType"] == "System.ArgumentException"
    record["oracleProgramSha256"] = hashlib.sha256(PROGRAM.read_bytes()).hexdigest()
    record["scope"] = "Selected CoreLib public identities and declarations; excludes full behavior and conditional-source inventory"
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("PASS pinned twenty-two-type foundation metadata capture")


if __name__ == "__main__":
    main()
