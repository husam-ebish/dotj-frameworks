"""Compile two bounded .j throw forms through the foundation throw-site hook."""

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE_ROOT = ROOT / "planning/stage-2/repos/dotj-core/evidence"
ARTIFACT = EVIDENCE_ROOT / "foundation-product-candidate-v1.json"
EVIDENCE = EVIDENCE_ROOT / "throw-selected-lowering-v1.json"
BUILD = ROOT / "dotj-core/dotj-core-public/build/throw-selected-v1"
VARIABLE = re.compile(r"\s*throw\s+([A-Za-z][A-Za-z0-9]*)\s*;\s*")
CONSTRUCTOR = re.compile(r'\s*throw\s+new\s+System\.Exception\("([^"\\]*)"\)\s*;\s*')


def lower(source):
    variable = VARIABLE.fullmatch(source)
    if variable is not None:
        if variable.group(1) in {"null", "new", "true", "false"}:
            raise ValueError("Unsupported .j throw operand")
        return f"throw ThrowSite.capture({variable.group(1)});"
    constructor = CONSTRUCTOR.fullmatch(source)
    if constructor is not None:
        message = json.dumps(constructor.group(1), ensure_ascii=True)
        return f"throw ThrowSite.capture(new Exception({message}));"
    raise ValueError("Unsupported .j throw source form")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source_calls = ["throw reused;", 'throw new System.Exception("fresh");']
    lowered = [lower(call) for call in source_calls]
    rejected = [
        "throw;", "throw reused.GetBaseException();", "throw java.lang.RuntimeException;",
        'throw new System.Exception("escaped\\n");', "throw reused; extra", "throw null;",
    ]
    for call in rejected:
        try:
            lower(call)
        except ValueError:
            pass
        else:
            raise AssertionError("Unsupported throw source was accepted: " + call)

    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    jar = ROOT / artifact["jarPath"]
    assert sha256(jar) == artifact["jarSha256"]
    generated = BUILD / "consumer/SelectedThrowLoweringConsumer.java"
    classes = BUILD / "classes"
    generated.parent.mkdir(parents=True, exist_ok=True)
    classes.mkdir(parents=True, exist_ok=True)
    generated.write_text("\n".join([
        "package consumer;",
        "import System.Exception;",
        "import org.dotj.internal.throwing.ThrowSite;",
        "public final class SelectedThrowLoweringConsumer {",
        "  public static void main(String[] args) {",
        '    Exception reused = new Exception("reused");',
        '    if (reused.get_StackTrace() != null) throw new AssertionError("prethrow stack");',
        "    try { " + lowered[0] + " } catch (Exception caught) {",
        '      if (caught != reused || caught.get_StackTrace() == null)',
        '        throw new AssertionError("variable throw identity or stack");',
        "    }",
        "    try { " + lowered[1] + " } catch (Exception caught) {",
        '      if (!"fresh".equals(caught.get_Message()) || caught.get_StackTrace() == null)',
        '        throw new AssertionError("constructor throw message or stack");',
        "    }",
        '    java.lang.System.out.println("PASS selected .j throw lowering consumer");',
        "  }",
        "}",
        "",
    ]), encoding="utf-8")
    subprocess.run(["javac", "--release", "21", "-cp", str(jar), "-d", str(classes),
                    str(generated)], cwd=ROOT, check=True)
    classpath = os.pathsep.join((str(classes), str(jar)))
    result = subprocess.run(["java", "-cp", classpath,
                             "consumer.SelectedThrowLoweringConsumer"],
                            cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    assert result == "PASS selected .j throw lowering consumer"
    EVIDENCE.write_text(json.dumps({
        "schemaVersion": 1,
        "sourceCalls": [{"source": source, "lowered": expression}
                        for source, expression in zip(source_calls, lowered)],
        "unsupportedFormsRejected": len(rejected),
        "jarSha256": artifact["jarSha256"],
        "generatedConsumerSha256": sha256(generated),
        "result": result,
        "qualification": "BOUNDED_LOWERING_PROTOTYPE; general .j parser, rethrow and CLR frame mapping OPEN",
    }, indent=2) + "\n", encoding="utf-8")
    print(result)


if __name__ == "__main__":
    main()
