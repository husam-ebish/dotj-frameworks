"""Compile a bounded .j typeof source form to the selected System.Type backend."""

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "dotj-core/dotj-core-public/src/main/java/System/Type.java"
EXCEPTION_SOURCES = [SOURCE.with_name(name + ".java") for name in
                     ("Exception", "SystemException", "ArgumentException", "ArgumentNullException", "TypeLoadException", "IndexOutOfRangeException", "OverflowException", "InvalidCastException", "InvalidOperationException", "FormatException")]
EXCEPTION_SOURCES += [SOURCE.parent / "IO" / (name + ".java") for name in
                      ("IOException", "FileNotFoundException", "FileLoadException")]
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MemberInfo.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MethodBase.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MethodBody.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MethodInfo.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/ParameterInfo.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/ParameterAttributes.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MemberTypes.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/GenericParameterAttributes.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/BindingFlags.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/CallingConventions.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Reflection/MethodImplAttributes.java")
EXCEPTION_SOURCES.append(SOURCE.with_name("TypeCode.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("DBNull.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("Attribute.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("NullReferenceException.java"))
EXCEPTION_SOURCES.append(SOURCE.parent / "Runtime/CompilerServices/NullableAttribute.java")
EXCEPTION_SOURCES += [SOURCE.parent / "Runtime/Serialization" / (name + ".java") for name in
                      ("FormatterConverter", "IFormatterConverter", "ISerializable", "SerializationException", "SerializationInfo", "StreamingContext", "StreamingContextStates")]
EXCEPTION_SOURCES.append(SOURCE.with_name("Decimal.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("DateTime.java"))
EXCEPTION_SOURCES.append(SOURCE.with_name("Int32.java"))
EXCEPTION_SOURCES.append(SOURCE.parent / "Globalization/NumberStyles.java")
EXCEPTION_SOURCES.append(SOURCE.parent / "Globalization/CultureNotFoundException.java")
EXCEPTION_SOURCES.append(ROOT / "dotj-core/dotj-core-public/src/main/java/org/dotj/internal/throwing/ThrowSite.java")
IDISPOSABLE_SOURCE = SOURCE.with_name("IDisposable.java")
ICOMPARABLE_SOURCE = SOURCE.with_name("IComparable.java")
IFORMATTABLE_SOURCE = SOURCE.with_name("IFormattable.java")
IFORMATPROVIDER_SOURCE = SOURCE.with_name("IFormatProvider.java")
ISPANFORMATTABLE_SOURCE = SOURCE.with_name("ISpanFormattable.java")
IUTF8SPANFORMATTABLE_SOURCE = SOURCE.with_name("IUtf8SpanFormattable.java")
ICONVERTIBLE_SOURCE = SOURCE.with_name("IConvertible.java")
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
    subprocess.run(["javac", "--release", "21", "-d", str(product_classes),
                    *(str(path) for path in [SOURCE, *EXCEPTION_SOURCES, IDISPOSABLE_SOURCE,
                                             ICOMPARABLE_SOURCE, IFORMATTABLE_SOURCE,
                                             IFORMATPROVIDER_SOURCE, ICONVERTIBLE_SOURCE,
                                             ISPANFORMATTABLE_SOURCE,
                                             IUTF8SPANFORMATTABLE_SOURCE])], check=True)
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
