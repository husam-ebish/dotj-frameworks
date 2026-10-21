"""Verify selected span factories preserve Char and UTF-8 Byte types for Java callers."""

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
ARTIFACT = EVIDENCE / "foundation-product-candidate-v1.json"
OUTPUT = EVIDENCE / "span-factory-types-v1.json"


def main():
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    jar = ROOT / artifact["jarPath"]
    assert hashlib.sha256(jar.read_bytes()).hexdigest() == artifact["jarSha256"]
    declarations = {}
    for name in ("System.Span", "System.ReadOnlySpan"):
        output = subprocess.run(["javap", "-public", "-classpath", str(jar), name],
                                capture_output=True, text=True, check=True).stdout
        lines = [line.strip() for line in output.splitlines()]
        assert not any(line.startswith("public " + name + "(") for line in lines)
        char = [line for line in lines if "OfChars(char[]" in line]
        byte = [line for line in lines if "OfUtf8Bytes(byte[]" in line]
        assert len(char) == len(byte) == 2, (name, char, byte)
        assert all(name + "<java.lang.Character>" in line for line in char)
        assert all(name + "<System.Byte>" in line for line in byte)
        declarations[name] = {"charFactories": char, "byteFactories": byte,
                              "publicConstructors": 0}

    negative_probes = (
        "Span<Character> wrong = Span.OfUtf8Bytes(new byte[1]);",
        "Span<Byte> wrong = Span.OfChars(new char[1]);",
        "ReadOnlySpan<Character> wrong = ReadOnlySpan.OfUtf8Bytes(new byte[1]);",
        "ReadOnlySpan<Byte> wrong = ReadOnlySpan.OfChars(new char[1]);",
    )
    with tempfile.TemporaryDirectory(prefix="dotj-span-factory-") as folder:
        source = Path(folder) / "Probe.java"
        for statement in negative_probes:
            source.write_text("import System.Span;\nimport System.ReadOnlySpan;\n"
                              "import System.Byte;\nclass Probe { " + statement + " }\n",
                              encoding="utf-8")
            result = subprocess.run(["javac", "-J-Duser.language=en", "--release", "21",
                                     "-cp", str(jar), str(source)], cwd=folder,
                                    capture_output=True, text=True)
            if result.returncode == 0 or "incompatible types" not in result.stderr:
                raise AssertionError((statement, result.stderr))

    OUTPUT.write_text(json.dumps({
        "schemaVersion": 1,
        "scope": "Selected Java Span and ReadOnlySpan factory type safety",
        "candidateJarSha256": artifact["jarSha256"],
        "declarations": declarations,
        "negativeCompileProbeCount": len(negative_probes),
        "negativeCompileProbes": list(negative_probes),
        "status": "TYPED_JAVA_FACTORY_BOUNDARY_PASS; CLR_SPAN_AND_FRONTEND_QUALIFICATION_OPEN",
        "limitation": "Java raw types and casts can bypass generic checks. These heap carriers do not implement CLR byref-like lifetime or source overload resolution.",
    }, indent=2) + "\n", encoding="utf-8")
    print("PASS typed Span factories: four mismatched Java assignments rejected")


if __name__ == "__main__":
    main()
