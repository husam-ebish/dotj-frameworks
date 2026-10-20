"""Compile a bounded .j typeof source form to the selected System.Type backend."""

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "dotj-core/dotj-core-public/src/main/java/System/Type.java"
BUILD = ROOT / "dotj-core/dotj-core-public/build/typeof-selected-v1"
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence/typeof-selected-lowering-v1.json"
NAME = re.compile(r"System(?:\.[A-Za-z][A-Za-z0-9]*)+")
TOKEN = re.compile(r"\s*(typeof|System(?:\.[A-Za-z][A-Za-z0-9]*)+|[<>,()])")
LEAVES = {"System.String", "System.Int32"}
GENERICS = {
    "System.Collections.Generic.List": ("System.Collections.Generic.List`1", 1),
    "System.Collections.Generic.Dictionary": ("System.Collections.Generic.Dictionary`2", 2),
}


def tokenize(source):
    tokens = []
    offset = 0
    while offset < len(source):
        matched = TOKEN.match(source, offset)
        if matched is None:
            raise ValueError("Unsupported typeof source token")
        tokens.append(matched.group(1))
        offset = matched.end()
    return tokens


def lower(source):
    tokens = tokenize(source)
    position = 0

    def consume(expected=None):
        nonlocal position
        if position >= len(tokens):
            raise ValueError("Incomplete typeof source")
        value = tokens[position]
        position += 1
        if expected is not None and value != expected:
            raise ValueError("Unexpected typeof source token")
        return value

    def lower_type():
        name = consume()
        if NAME.fullmatch(name) is None:
            raise ValueError("Expected an exact System type name")
        if position >= len(tokens) or tokens[position] != "<":
            if name not in LEAVES:
                raise ValueError("Unsupported non-generic type")
            return f'Type.GetType("{name}")'
        if name not in GENERICS:
            raise ValueError("Unsupported generic definition")
        consume("<")
        arguments = [lower_type()]
        while position < len(tokens) and tokens[position] == ",":
            consume(",")
            arguments.append(lower_type())
        consume(">")
        backend_name, arity = GENERICS[name]
        if len(arguments) != arity:
            raise ValueError("Generic arity mismatch")
        return (f'Type.GetType("{backend_name}").MakeGenericType('
                f'new Type[] {{{", ".join(arguments)}}})')

    consume("typeof")
    consume("(")
    expression = lower_type()
    consume(")")
    if position != len(tokens):
        raise ValueError("Trailing typeof source")
    return expression


def main():
    source_calls = [
        "typeof(System.Collections.Generic.List<System.String>)",
        "typeof(System.Collections.Generic.List<System.String>)",
        "typeof(System.Collections.Generic.List<System.Int32>)",
        "typeof(System.Collections.Generic.Dictionary<System.String,System.Int32>)",
    ]
    lowered = [lower(call) for call in source_calls]
    rejected = [
        "typeof(System.Unknown)",
        "typeof(System.Collections.Generic.List<System.String,System.Int32>)",
        "typeof(System.Collections.Generic.List<>)",
        "typeof(java.util.List<java.lang.String>)",
        "typeof(System.String)garbage",
        "typeof(System.Collections.Generic.List<System.Unknown>)",
    ]
    for call in rejected:
        try:
            lower(call)
        except ValueError:
            pass
        else:
            raise AssertionError("Unsupported source form was accepted: " + call)

    product_classes = BUILD / "product-classes"
    consumer_classes = BUILD / "consumer-classes"
    generated = BUILD / "consumer/SelectedTypeofLoweringConsumer.java"
    product_classes.mkdir(parents=True, exist_ok=True)
    consumer_classes.mkdir(parents=True, exist_ok=True)
    generated.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "package consumer;",
        "import System.Type;",
        "public final class SelectedTypeofLoweringConsumer {",
        "  public static void main(String[] args) {",
    ]
    lines.extend(f"    Type value{index} = {expression};" for index, expression in enumerate(lowered))
    lines.extend([
        '    if (value0 != value1 || value0 == value2 || value0 == value3)',
        '      throw new AssertionError("Selected typeof identity changed");',
        '    java.lang.System.out.println("PASS selected typeof lowering consumer");',
        "  }",
        "}",
    ])
    generated.write_text("\n".join(lines) + "\n", encoding="utf-8")
    subprocess.run(["javac", "--release", "21", "-d", str(product_classes), str(SOURCE)], check=True)
    subprocess.run(["javac", "--release", "21", "-cp", str(product_classes), "-d",
                    str(consumer_classes), str(generated)], check=True)
    import os
    classpath = os.pathsep.join((str(product_classes), str(consumer_classes)))
    result = subprocess.run(["java", "-cp", classpath, "consumer.SelectedTypeofLoweringConsumer"],
                            check=True, capture_output=True, text=True).stdout.strip()
    assert result == "PASS selected typeof lowering consumer"
    EVIDENCE.write_text(json.dumps({
        "schemaVersion": 1,
        "sourceCalls": [{"source": call, "lowered": expression}
                        for call, expression in zip(source_calls, lowered)],
        "unsupportedFormsRejected": len(rejected),
        "productSourceSha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "generatedConsumerSha256": hashlib.sha256(generated.read_bytes()).hexdigest(),
        "result": result,
        "qualification": "BOUNDED_LOWERING_PROTOTYPE; no general .j parser/compiler, complete System.Type, or public behavior qualification",
    }, indent=2) + "\n", encoding="utf-8")
    print(result)


if __name__ == "__main__":
    main()
