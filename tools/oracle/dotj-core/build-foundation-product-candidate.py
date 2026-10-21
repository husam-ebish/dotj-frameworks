"""Build a deterministic combined public foundation candidate JAR and test it externally."""

import hashlib
import json
import os
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PRODUCT = ROOT / "dotj-core/dotj-core-public"
SOURCES = [PRODUCT / "src/main/java/System" / (name + ".java") for name in (
    "IDisposable", "IComparable", "IFormattable", "IFormatProvider", "ISpanFormattable", "IUtf8SpanFormattable", "IConvertible", "TypeCode", "MidpointRounding", "Decimal", "DateTime", "Int32", "ReadOnlySpan", "Span", "UInt16", "UInt32", "Byte", "SByte", "Type", "DBNull", "Attribute", "Exception", "SystemException", "ArgumentException", "ArgumentNullException", "ArgumentOutOfRangeException", "ArithmeticException", "DivideByZeroException", "ValueTuple", "TypeLoadException", "IndexOutOfRangeException", "OverflowException", "InvalidCastException", "InvalidOperationException", "NullReferenceException", "FormatException")]
SOURCES += [PRODUCT / "src/main/java/System/IO" / (name + ".java") for name in
            ("IOException", "FileNotFoundException", "FileLoadException")]
SOURCES.append(PRODUCT / "src/main/java/System/Collections/IEnumerator.java")
SOURCES += [PRODUCT / "src/main/java/System/Collections" / (name + ".java") for name in
            ("IEnumerable", "ICollection", "IDictionary", "IDictionaryEnumerator", "DictionaryEntry")]
SOURCES.append(PRODUCT / "src/main/java/org/dotj/internal/collections/ExceptionDataDictionary.java")
SOURCES.append(PRODUCT / "src/main/java/System/Globalization/NumberStyles.java")
SOURCES.append(PRODUCT / "src/main/java/System/Globalization/NumberFormatInfo.java")
SOURCES.append(PRODUCT / "src/main/java/System/Globalization/CultureNotFoundException.java")
SOURCES.append(PRODUCT / "src/main/java/System/Runtime/CompilerServices/NullableAttribute.java")
SOURCES += [PRODUCT / "src/main/java/System/Runtime/Serialization" / (name + ".java") for name in
            ("FormatterConverter", "IFormatterConverter", "ISerializable", "SerializationEntry", "SerializationException", "SerializationInfo", "SerializationInfoEnumerator", "StreamingContext", "StreamingContextStates")]
SOURCES.append(PRODUCT / "src/main/java/System/Reflection/MemberInfo.java")
SOURCES.append(PRODUCT / "src/main/java/System/Reflection/MethodBase.java")
SOURCES.append(PRODUCT / "src/main/java/System/Reflection/MethodBody.java")
SOURCES.append(PRODUCT / "src/main/java/System/Reflection/MethodInfo.java")
SOURCES.append(PRODUCT / "src/main/java/System/Reflection/ParameterInfo.java")
SOURCES.append(PRODUCT / "src/main/java/System/Reflection/ParameterAttributes.java")
SOURCES.append(PRODUCT / "src/main/java/System/Reflection/MemberTypes.java")
SOURCES.append(PRODUCT / "src/main/java/System/Reflection/BindingFlags.java")
SOURCES.append(PRODUCT / "src/main/java/System/Reflection/CallingConventions.java")
SOURCES.append(PRODUCT / "src/main/java/System/Reflection/MethodImplAttributes.java")
SOURCES.append(PRODUCT / "src/main/java/System/Reflection/GenericParameterAttributes.java")
SOURCES.append(PRODUCT / "src/main/java/org/dotj/internal/throwing/ThrowSite.java")
CONSUMERS = [PRODUCT / "src/test/java/consumer" / (name + ".java") for name in (
    "ProductDisposableContractConsumer", "ProductTypeIdentityConsumer", "ProductExceptionContractConsumer",
    "ProductInt32BitConsumer", "ProductInt32ArithmeticConsumer", "ProductInt32SpanConsumer",
    "ProductDecimalBitsConsumer")]
BUILD = PRODUCT / "build/foundation-v1"
CLASSES = BUILD / "classes"
CONSUMER_CLASSES = BUILD / "consumer-classes"
JAR = BUILD / "dotj-core-foundation-v1.jar"
LICENSE = ROOT / "dotj-core/LICENSE"
EVIDENCE_ROOT = ROOT / "planning/stage-2/repos/dotj-core/evidence"
EVIDENCE = EVIDENCE_ROOT / "foundation-product-candidate-v1.json"
EXPECTED_CLASSES = [
    "System/ArgumentException.class",
    "System/ArgumentNullException.class",
    "System/ArgumentOutOfRangeException.class",
    "System/ArithmeticException.class",
    "System/Attribute.class",
    "System/Byte.class",
    "System/Collections/DictionaryEntry.class",
    "System/Collections/ICollection.class",
    "System/Collections/IDictionary.class",
    "System/Collections/IDictionaryEnumerator.class",
    "System/Collections/IEnumerable.class",
    "System/Collections/IEnumerator.class",
    "System/DBNull.class",
    "System/DateTime.class",
    "System/Decimal.class",
    "System/DivideByZeroException.class",
    "System/Exception.class",
    "System/FormatException.class",
    "System/Globalization/CultureNotFoundException.class",
    "System/Globalization/NumberFormatInfo.class",
    "System/Globalization/NumberStyles.class",
    "System/IComparable.class",
    "System/IConvertible.class",
    "System/IDisposable.class",
    "System/IFormatProvider.class",
    "System/IFormattable.class",
    "System/IO/FileLoadException.class",
    "System/IO/FileNotFoundException.class",
    "System/IO/IOException.class",
    "System/ISpanFormattable.class",
    "System/IUtf8SpanFormattable.class",
    "System/IndexOutOfRangeException.class",
    "System/Int32.class",
    "System/InvalidCastException.class",
    "System/InvalidOperationException.class",
    "System/MidpointRounding.class",
    "System/NullReferenceException.class",
    "System/OverflowException.class",
    "System/ReadOnlySpan.class",
    "System/Reflection/BindingFlags.class",
    "System/Reflection/CallingConventions.class",
    "System/Reflection/GenericParameterAttributes.class",
    "System/Reflection/MemberInfo.class",
    "System/Reflection/MemberTypes.class",
    "System/Reflection/MethodBase.class",
    "System/Reflection/MethodBody.class",
    "System/Reflection/MethodImplAttributes.class",
    "System/Reflection/MethodInfo.class",
    "System/Reflection/ParameterAttributes.class",
    "System/Reflection/ParameterInfo.class",
    "System/Runtime/CompilerServices/NullableAttribute.class",
    "System/Runtime/Serialization/FormatterConverter$1.class",
    "System/Runtime/Serialization/FormatterConverter.class",
    "System/Runtime/Serialization/IFormatterConverter.class",
    "System/Runtime/Serialization/ISerializable.class",
    "System/Runtime/Serialization/SerializationEntry.class",
    "System/Runtime/Serialization/SerializationException.class",
    "System/Runtime/Serialization/SerializationInfo.class",
    "System/Runtime/Serialization/SerializationInfoEnumerator.class",
    "System/Runtime/Serialization/StreamingContext.class",
    "System/Runtime/Serialization/StreamingContextStates.class",
    "System/SByte.class",
    "System/Span.class",
    "System/SystemException.class",
    "System/Type$1.class",
    "System/Type$2.class",
    "System/Type$ArrayType.class",
    "System/Type$ByRefType.class",
    "System/Type$DefaultMethodMember.class",
    "System/Type$DefaultParameterInfo.class",
    "System/Type$DefaultPropertyMember.class",
    "System/Type$GenericParameterType.class",
    "System/Type$PointerType.class",
    "System/Type$ResolvedType.class",
    "System/Type.class",
    "System/TypeCode.class",
    "System/TypeLoadException.class",
    "System/UInt16.class",
    "System/UInt32.class",
    "System/ValueTuple.class",
    "org/dotj/internal/collections/ExceptionDataDictionary$CollectionView.class",
    "org/dotj/internal/collections/ExceptionDataDictionary$EntryEnumerator.class",
    "org/dotj/internal/collections/ExceptionDataDictionary$ValueEnumerator.class",
    "org/dotj/internal/collections/ExceptionDataDictionary.class",
    "org/dotj/internal/throwing/ThrowSite.class",
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*command):
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=True).stdout


def main():
    type_evidence = json.loads((EVIDENCE_ROOT / "system-type-identity-candidate-v1.json").read_text(encoding="utf-8"))
    disposal_evidence = json.loads((EVIDENCE_ROOT / "idisposable-product-v1.json").read_text(encoding="utf-8"))
    metadata = json.loads((EVIDENCE_ROOT / "foundation-selected-metadata-v10.0.12.json").read_text(encoding="utf-8"))
    decimal_patterns = metadata["selectedDecimalBitPatterns"]
    assert [(entry["input"], entry["bits"], entry["convertedBits"], entry["text"])
            for entry in decimal_patterns["valid"]] == [
        (bits, bits, bits, rendered) for bits, rendered in (
            ([42, 0, 0, 0], "42"),
            ([12345, 0, 0, 0x00020000], "123.45"),
            ([12345, 0, 0, -2147352576], "-123.45"),
            ([0, 0, 0, -2147483648], "0"),
            ([0, 0, 0, -2147352576], "0.00"),
            ([-1, -1, -1, 0], "79228162514264337593543950335"),
            ([-1, -1, -1, -2147483648], "-79228162514264337593543950335"),
            ([1, 0, 0, 0x001c0000], "0.0000000000000000000000000001"),
        )]
    assert decimal_patterns["parsedNegativeZero"] == [0, 0, 0, -2147352576]
    assert decimal_patterns["parsedPositiveZero"] == [0, 0, 0, 0x00020000]
    assert decimal_patterns["invalid"] == {
        "nullArray": {"type": "System.ArgumentNullException", "paramName": "bits"},
        **{name: {"type": "System.ArgumentException", "paramName": None}
           for name in ("threeWords", "fiveWords", "reservedBit", "scale29")},
    }
    word_patterns = metadata["selectedDecimalWordConstructor"]
    assert [(entry["input"], entry["bits"])
            for entry in word_patterns["valid"]] == [
        ([lo, mid, hi, negative, scale],
         [lo, mid, hi, (scale << 16) | (-2147483648 if negative else 0)])
        for lo, mid, hi, negative, scale in (
            (42, 0, 0, False, 0), (12345, 0, 0, False, 2),
            (12345, 0, 0, True, 2), (0, 0, 0, True, 0),
            (0, 0, 0, True, 2), (-1, -1, -1, False, 0),
            (-1, -1, -1, True, 0), (1, 0, 0, False, 28),
            (-1, -1, -1, True, 28),
        )]
    assert word_patterns["scale29"] == {
        "type": "System.ArgumentOutOfRangeException", "paramName": "scale"}
    assert word_patterns["scale255"] == word_patterns["scale29"]
    parse_bounds = metadata["selectedDecimalParseBounds"]
    assert [(entry["text"], entry["bits"], entry["error"])
            for entry in parse_bounds] == [
        ("0", [0, 0, 0, 0], None),
        ("-0.00", [0, 0, 0, -2147352576], None),
        *[(text, [268435456, 1042612833, 542101086, 1835008], None)
          for text in ("1.0000000000000000000000000000",
                       "1.00000000000000000000000000000")],
        ("0.00000000000000000000000000005", [0, 0, 0, 1835008], None),
        ("0.00000000000000000000000000006", [1, 0, 0, 1835008], None),
        ("-0.00000000000000000000000000006", [1, 0, 0, -2145648640], None),
        ("79228162514264337593543950335", [-1, -1, -1, 0], None),
        ("79228162514264337593543950335.0", [-1, -1, -1, 0], None),
        ("79228162514264337593543950336", None, "System.OverflowException"),
        ("79228162514264337593543950335.4", [-1, -1, -1, 0], None),
        ("79228162514264337593543950334.5", [-2, -1, -1, 0], None),
        ("79228162514264337593543950335.5", None, "System.OverflowException"),
    ]
    assert [(entry["input"], entry["result"])
            for entry in metadata["selectedDecimalTruncate"]] == [
        ([12345, 0, 0, 131072], [123, 0, 0, 0]),
        ([12345, 0, 0, -2147352576], [123, 0, 0, -2147483648]),
        ([99, 0, 0, 131072], [0, 0, 0, 0]),
        ([99, 0, 0, -2147352576], [0, 0, 0, -2147483648]),
        ([0, 0, 0, -2147352576], [0, 0, 0, -2147483648]),
        ([1, 0, 0, 1835008], [0, 0, 0, 0]),
        ([-1, -1, -1, 0], [-1, -1, -1, 0]),
        ([-1, -1, -1, -2147483648], [-1, -1, -1, -2147483648]),
        ([12300, 0, 0, 131072], [123, 0, 0, 0]),
        ([1, 0, 0, -2147352576], [0, 0, 0, -2147483648]),
    ]
    floor_ceiling = metadata["selectedDecimalFloorCeiling"]
    assert [entry["input"] for entry in floor_ceiling] == [
        entry["input"] for entry in metadata["selectedDecimalTruncate"]]
    assert [(entry["floor"], entry["ceiling"]) for entry in floor_ceiling] == [
        ([123, 0, 0, 0], [124, 0, 0, 0]),
        ([124, 0, 0, -2147483648], [123, 0, 0, -2147483648]),
        ([0, 0, 0, 0], [1, 0, 0, 0]),
        ([1, 0, 0, -2147483648], [0, 0, 0, -2147483648]),
        ([0, 0, 0, -2147483648], [0, 0, 0, -2147483648]),
        ([0, 0, 0, 0], [1, 0, 0, 0]),
        ([-1, -1, -1, 0], [-1, -1, -1, 0]),
        ([-1, -1, -1, -2147483648], [-1, -1, -1, -2147483648]),
        ([123, 0, 0, 0], [123, 0, 0, 0]),
        ([1, 0, 0, -2147483648], [0, 0, 0, -2147483648]),
    ]
    decimal_round = metadata["selectedDecimalRound"]
    assert [(entry["input"], entry["decimals"], entry["result"])
            for entry in decimal_round["valid"]] == [
        ([125, 0, 0, 131072], 1, [12, 0, 0, 65536]),
        ([135, 0, 0, 131072], 1, [14, 0, 0, 65536]),
        ([125, 0, 0, -2147352576], 1, [12, 0, 0, -2147418112]),
        ([5, 0, 0, 65536], 0, [0, 0, 0, 0]),
        ([5, 0, 0, -2147418112], 0, [0, 0, 0, -2147483648]),
        ([12345, 0, 0, 131072], 0, [123, 0, 0, 0]),
        ([12345, 0, 0, 131072], 1, [1234, 0, 0, 65536]),
        ([12345, 0, 0, 131072], 2, [12345, 0, 0, 131072]),
        ([12345, 0, 0, 131072], 3, [12345, 0, 0, 131072]),
        ([-1, -1, -1, 0], 2, [-1, -1, -1, 0]),
        ([1, 0, 0, 1835008], 27, [0, 0, 0, 1769472]),
        ([6, 0, 0, 1835008], 27, [1, 0, 0, 1769472]),
    ]
    assert decimal_round["negativeDigits"] == {
        "type": "System.ArgumentOutOfRangeException", "paramName": "decimals"}
    assert decimal_round["over28Digits"] == decimal_round["negativeDigits"]
    round_modes = metadata["selectedDecimalRoundModes"]
    assert round_modes["modes"] == [
        {"name": name, "value": value} for value, name in enumerate((
            "ToEven", "AwayFromZero", "ToZero", "ToNegativeInfinity",
            "ToPositiveInfinity"))]
    mode_inputs = ([125, 0, 0, 131072], [125, 0, 0, -2147352576],
                   [126, 0, 0, 131072], [126, 0, 0, -2147352576],
                   [5, 0, 0, -2147352576])
    mode_results = ((12, 13, 12, 12, 13), (12, 13, 12, 13, 12),
                    (13, 13, 12, 12, 13), (13, 13, 12, 13, 12),
                    (0, 1, 0, 1, 0))
    assert [(entry["input"], entry["decimals"], entry["mode"], entry["result"])
            for entry in round_modes["valid"]] == [
        (bits, 1, mode, [result, 0, 0,
                         (65536 | (-2147483648 if bits[3] < 0 else 0))])
        for bits, results in zip(mode_inputs, mode_results)
        for mode, result in enumerate(results)]
    assert round_modes["invalidNegative"] == {
        "type": "System.ArgumentException", "paramName": "mode"}
    assert round_modes["invalidFive"] == round_modes["invalidNegative"]
    round_overloads = metadata["selectedDecimalRoundOverloads"]
    overload_inputs = ([150, 0, 0, 131072], [250, 0, 0, 131072],
                       [150, 0, 0, -2147352576], [250, 0, 0, -2147352576],
                       [50, 0, 0, 131072], [50, 0, 0, -2147352576],
                       [-1, -1, -1, 0], [-1, -1, -1, -2147483648])
    overload_results = ((2, 2, 1, 1, 2), (2, 3, 2, 2, 3),
                        (2, 2, 1, 2, 1), (2, 3, 2, 3, 2),
                        (0, 1, 0, 0, 1), (0, 1, 0, 1, 0))
    expected_overloads = []
    for index, bits in enumerate(overload_inputs):
        expected_modes = ([result, 0, 0,
                           -2147483648 if bits[3] < 0 else 0]
                          for result in overload_results[index]) if index < 6 else (bits for _ in range(5))
        mode_bits = list(expected_modes)
        expected_overloads.append((bits, mode_bits[0], mode_bits))
    assert [(entry["input"], entry["defaultBits"], entry["modeBits"])
            for entry in round_overloads] == expected_overloads
    assert metadata["selectedSpanFormattingBehavior"] == {
        "enough": {"success": True, "charsWritten": 2, "text": "42"},
        "shortBuffer": {"success": False, "charsWritten": 0, "text": ""},
    }
    assert metadata["selectedUtf8SpanFormattingBehavior"] == {
        "enough": {"success": True, "bytesWritten": 2, "text": "42"},
        "shortBuffer": {"success": False, "bytesWritten": 0, "text": ""},
    }
    assert metadata["selectedInt32FormatBehavior"] == {
        "decimal5": "00042", "hexUpper4": "002A", "hexLower4": "002a",
        "negativeDecimal5": "-00042", "negativeHex": "FFFFFFFF",
    }
    assert metadata["selectedInt32ProviderFormatBehavior"] == {
        "grouped": "12_345:00", "negative": "-42:00", "defaultPrecision": "42:000",
    }
    assert metadata["selectedInt32NumberGroupSizes"] == {
        "repeated": "12_34_56_789", "negative": "-12_34_56_789.00",
        "stopped": "1234_56_789", "parsed": 123456789,
    }
    assert metadata["selectedInt32CurrencyPercentGroupSizes"] == {
        "currency": "USD12_34_56_789",
        "negativeCurrency": "(USD12_34_56_789)",
        "percent": "42_00 pct", "negativePercent": "-42_00 pct",
    }
    assert metadata["selectedInt32GroupSizeBoundaries"] == {
        "nullNumber": "System.ArgumentNullException",
        "emptyNumber": None, "zeroNumber": None,
        "negativeNumber": "System.ArgumentException",
        "tenNumber": "System.ArgumentException",
        "interiorZeroNumber": "System.ArgumentException",
        "terminalZeroNumber": None,
        "negativeCurrency": "System.ArgumentException",
        "interiorZeroCurrency": "System.ArgumentException",
        "negativePercent": "System.ArgumentException",
        "interiorZeroPercent": "System.ArgumentException",
    }
    assert metadata["selectedInt32NegativeSignBehavior"] == {
        "customParse": -42, "customSuccess": True, "customValue": -42,
        "standardSuccess": False, "standardValue": 0,
        "negativeFormat": "~42.00",
        "decimalFormat": "~42", "paddedDecimalFormat": "~00042",
        "providerText": "~42",
        "generalFormat": "~42", "lowerGeneral": "~42",
        "generalPrecision": "~42", "roundTrip": "~42",
    }
    assert metadata["selectedInt32CurrencyProviderBehavior"] == {
        "defaultPrecision": "USD12_345:000", "zeroPrecision": "USD12_345",
        "negativeWithSign": "~USD12_345:00",
        "negativeParentheses": "(USD12_345:00)",
    }
    assert metadata["selectedInt32PercentProviderBehavior"] == {
        "defaultPositive": "4_200:000 pct", "defaultNegative": "~4_200:00 pct",
        "compactPositive": "4_200:00pct", "compactNegative": "~4_200:00pct",
    }
    assert metadata["selectedInt32FixedProviderBehavior"] == {
        "defaultPrecision": "~42:000", "explicitPrecision": "~42:0",
        "zeroPrecision": "~42",
    }
    assert metadata["selectedInt32ExponentialProviderBehavior"] == {
        "upper": "~4:20E+001", "lower": "4:2e+001",
        "zeroPrecision": "~4E+001",
    }
    assert metadata["selectedInt32PositiveSignBehavior"] == {
        "customParse": 42, "customSuccess": True, "customValue": 42,
        "standardSuccess": False, "standardValue": 0,
        "positiveExponent": "4.2Eplus001",
        "negativeExponent": "~4.2Eplus001",
    }
    assert metadata["selectedInt32NumberStyleProviderBehavior"] == {
        "grouped": 12345, "decimalZero": 12345, "negative": -12345,
        "positive": 12345, "trailingNegative": -12345,
        "fractionalSuccess": False, "fractionalValue": 0,
        "standardSignSuccess": False, "standardSignValue": 0,
    }
    boundary_texts = ["_123", "123_", "12__345", "42:", "42:0_0", "42:5",
                      "42::0", "12_:00", "42plus", "42~", "~42plus", ":00"]
    boundary_success = [False, True, True, True, False, False,
                        False, True, True, True, False, True]
    boundary_values = [0, 123, 12345, 42, 0, 0, 0, 12, 42, -42, 0, 0]
    assert metadata["selectedInt32NumberStyleBoundaries"] == [
        {"text": text, "success": success, "value": value}
        for text, success, value in zip(boundary_texts, boundary_success, boundary_values)
    ]
    float_texts = ["42", " 42:00 ", "4:2e1", "420e~1", "plus4:2Eplus1",
                   "~4:2eplus1", "12_345", "42:5", "4:2e0", "2147483648",
                   "42plus", "42~", "42:", ":0", "4:2e~1"]
    float_values = [42, 42, 42, 42, 42, -42, 0, 0, 0, 0, 0, 0, 42, 0, 0]
    float_errors = [None] * 6 + ["System.FormatException"] + ["System.OverflowException"] * 3 \
        + ["System.FormatException"] * 2 + [None] * 2 + ["System.OverflowException"]
    assert metadata["selectedInt32FloatStyle"] == [
        {"text": text, "success": error is None, "value": value, "error": error}
        for text, value, error in zip(float_texts, float_values, float_errors)
    ]
    single_styles = {
        "thousands": (
            ["12_345", "_123", "123_", " 123", "~123", "123:00", "12__345"],
            [12345, 0, 123, 0, 0, 0, 12345],
            [None, "Format", None, "Format", "Format", "Format", None]),
        "decimalPoint": (
            ["42:00", "42:5", ":0", "42:", "12_345", " 42", "~42"],
            [42, 0, 0, 42, 0, 0, 0],
            [None, "Overflow", None, None, "Format", "Format", "Format"]),
        "exponent": (
            ["42e1", "420e~1", "4:2e1", "42", " 42", "~42",
             "42eplus1", "42e1plus", "42e~1"],
            [420, 42, 0, 42, 0, 0, 420, 0, 0],
            [None, None, "Format", None, "Format", "Format", None,
             "Format", "Overflow"]),
    }
    assert metadata["selectedInt32SingleStyles"] == {
        name: [
            {"text": text, "success": error is None, "value": value,
             "error": None if error is None else f"System.{error}Exception"}
            for text, value, error in zip(texts, values, errors)
        ]
        for name, (texts, values, errors) in single_styles.items()
    }
    currency_texts = ["USD12_345:00", "(USD12_345:00)", "~USD12_345:00",
                      "plusUSD12_345:00", "12_345:00USD", "USD 12_345:00",
                      "12_345:00 USD", "12_345:00", "12.345=00", "USD12.345=00",
                      "USD42:5", "USD_42", "USD42e1", "  USD42  ", "USD42~", "USD42plus"]
    currency_values = [12345, -12345, -12345, 12345, 12345, 12345, 12345,
                       12345, 12345, 0, 0, 0, 0, 42, -42, 42]
    currency_errors = [None] * 9 + ["Format", "Overflow", "Format", "Format"] \
        + [None] * 3
    assert metadata["selectedInt32CurrencyStyle"] == [
        {"text": text, "success": error is None, "value": value,
         "error": None if error is None else f"System.{error}Exception"}
        for text, value, error in zip(currency_texts, currency_values, currency_errors)
    ]
    any_texts = ["USD12_345:00", "12.345=00", "~USD12_345:00", "42e1",
                 "4:2e1", "4=2e1", "(USD42)", "USD42e1", "USD42:5",
                 "42:5", "42=5", "12_345", "12.345", "42plus", "USD42~",
                 "USD42eplus1", "(42)"]
    any_values = [12345, 12345, -12345, 420, 42, 42, -42, 420, 0, 0, 0,
                  12345, 12345, 42, -42, 420, -42]
    any_errors = [None] * 8 + ["System.OverflowException"] * 3 + [None] * 6
    assert metadata["selectedInt32AnyStyle"] == [
        {"text": text, "success": error is None, "value": value, "error": error}
        for text, value, error in zip(any_texts, any_values, any_errors)
    ]
    combined_styles = {
        "signThousands": (
            68, ["~12_345", "12_345", " 12_345", "12_345~", "12_345:00", "plus12_345"],
            [-12345, 12345, 0, 0, 0, 12345],
            [None, None, "Format", "Format", "Format", None]),
        "paddedThousands": (
            67, [" 12_345 ", "~12_345", "12_345", "12_345:00"],
            [12345, 0, 12345, 0], [None, "Format", None, "Format"]),
        "decimalExponent": (
            160, ["4:2e1", "420e~1", "~4:2e1", " 42", "4:2e0", "42", "12_345"],
            [42, 42, 0, 0, 0, 42, 0],
            [None, None, "Format", "Format", "Overflow", None, "Format"]),
    }
    assert metadata["selectedInt32CombinedStyles"] == {
        key: value
        for name, (flags, texts, values, errors) in combined_styles.items()
        for key, value in (
            (name + "Value", flags),
            (name, [
                {"text": text, "success": error is None, "value": value,
                 "error": None if error is None else f"System.{error}Exception"}
                for text, value, error in zip(texts, values, errors)
            ]),
        )
    }
    more_combined_styles = {
        "signExponent": (132, ["~42e1", "42e~1", "42:0", " 42", "plus42e1"],
                         [-420, 0, 0, 0, 420],
                         [None, "Overflow", "Format", "Format", None]),
        "paddedDecimal": (35, [" 42:00 ", "42:5", "~42", "4:2e1", "42"],
                          [42, 0, 0, 0, 42],
                          [None, "Overflow", "Format", "Format", None]),
        "signDecimalExponent": (164, ["~4:2e1", "plus4:2e1", " 4:2e1",
                                     "4:2e~1", "42"],
                                [-42, 42, 0, 0, 42],
                                [None, None, "Format", "Overflow", None]),
    }
    assert metadata["selectedInt32MoreCombinedStyles"] == {
        key: value
        for name, (flags, texts, values, errors) in more_combined_styles.items()
        for key, value in (
            (name + "Value", flags),
            (name, [
                {"text": text, "success": error is None, "value": value,
                 "error": None if error is None else f"System.{error}Exception"}
                for text, value, error in zip(texts, values, errors)
            ]),
        )
    }
    trailing_styles = {
        "trailing": (8, ["42~", "42plus", "~42"], [-42, 42, 0],
                     [None, None, "Format"]),
        "groupedTrailing": (72, ["12_345~", "12_345plus", "~12_345",
                                 " 12_345~", "12_345:00~", "12__345~"],
                            [-12345, 12345, 0, 0, 0, -12345],
                            [None, None, "Format", "Format", "Format", None]),
        "paddedTrailing": (75, [" 12_345~ ", "12_345plus", "~12_345",
                                "12_345:00~"],
                           [-12345, 12345, 0, 0],
                           [None, None, "Format", "Format"]),
        "bothSigns": (76, ["~12_345", "12_345~", "~12_345~",
                           "plus12_345~", "12_345plus"],
                      [-12345, -12345, 0, 0, 12345],
                      [None, None, "Format", "Format", None]),
    }
    assert metadata["selectedInt32TrailingSignStyles"] == {
        key: value
        for name, (flags, texts, values, errors) in trailing_styles.items()
        for key, value in (
            (name + "Value", flags),
            (name, [
                {"text": text, "success": error is None, "value": value,
                 "error": None if error is None else f"System.{error}Exception"}
                for text, value, error in zip(texts, values, errors)
            ]),
        )
    }
    grouped_decimal_styles = {
        "parentheses": (16, ["(42)", "42", "~42", " (42)", "(42)~"],
                        [-42, 42, 0, 0, 0], [None, None, "Format", "Format", "Format"]),
        "groupedDecimal": (96, ["12_345:00", "12_345:5", " 12_345:00",
                                "~12_345:00", "12_345:0_0"],
                           [12345, 0, 0, 0, 0],
                           [None, "Overflow", "Format", "Format", "Format"]),
        "parenthesizedDecimal": (112, ["(12_345:00)", "(12_345:5)",
                                       "~12_345:00", "(12_345:00)~", "12_345:00"],
                                  [-12345, 0, 0, 0, 12345],
                                  [None, "Overflow", "Format", "Format", None]),
        "groupedExponent": (224, ["12_345:00e1", "1_234:5e1", "12_345:5e0",
                                  "12_345:00e~1", "12_345:00eplus1", "12_345:00"],
                             [123450, 12345, 0, 0, 123450, 12345],
                             [None, None, "Overflow", "Overflow", None, None]),
    }
    assert metadata["selectedInt32GroupedDecimalStyles"] == {
        key: value
        for name, (flags, texts, values, errors) in grouped_decimal_styles.items()
        for key, value in (
            (name + "Value", flags),
            (name, [
                {"text": text, "success": error is None, "value": value,
                 "error": None if error is None else f"System.{error}Exception"}
                for text, value, error in zip(texts, values, errors)
            ]),
        )
    }
    currency_flag_styles = {
        "symbol": (256, ["USD42", "42USD", "USD 42", " USD42", "~USD42",
                         "USD42:00", "42"],
                   [42, 42, 0, 0, 0, 0, 42],
                   [None, None, "Format", "Format", "Format", "Format", None]),
        "symbolGroup": (320, ["USD12_345", "12_345USD", "USD_42",
                              "USD12.345", "  USD12_345", "USD12_345:00"],
                        [12345, 12345, 0, 0, 0, 0],
                        [None, None, "Format", "Format", "Format", "Format"]),
        "symbolDecimal": (288, ["USD42:00", "42:00USD", "USD42:5",
                                "USD42=00", "USD12_345:00", "42"],
                          [42, 42, 0, 0, 0, 42],
                          [None, None, "Overflow", "Format", "Format", None]),
        "symbolExponent": (384, ["USD42e1", "42e1USD", "USD42eplus1",
                                 "USD42:0e1", "~USD42e1", "USD42e~1"],
                           [420, 420, 420, 0, 0, 0],
                           [None, None, None, "Format", "Format", "Overflow"]),
    }
    assert metadata["selectedInt32CurrencyFlagStyles"] == {
        key: value
        for name, (flags, texts, values, errors) in currency_flag_styles.items()
        for key, value in (
            (name + "Value", flags),
            (name, [
                {"text": text, "success": error is None, "value": value,
                 "error": None if error is None else f"System.{error}Exception"}
                for text, value, error in zip(texts, values, errors)
            ]),
        )
    }
    radix_styles = {
        "hex": (["FF", " FF", "FF ", "FFFFFFFF", "100000000", "0xFF"],
                [255, 0, 0, -1, 0, 0],
                [None, "Format", "Format", None, "Overflow", "Format"]),
        "leadingHex": ([" FF", "FF ", "FF", " 100000000"],
                       [255, 0, 255, 0], [None, "Format", None, "Overflow"]),
        "trailingHex": (["FF ", " FF", "FF"], [255, 0, 255],
                        [None, "Format", None]),
        "binary": (["101010", " 101010", "101010 ",
                    "11111111111111111111111111111111",
                    "100000000000000000000000000000000"],
                   [42, 0, 0, -1, 0],
                   [None, "Format", "Format", None, "Overflow"]),
        "leadingBinary": ([" 101010", "101010 ", "101010"],
                          [42, 0, 42], [None, "Format", None]),
        "trailingBinary": (["101010 ", " 101010", "101010"],
                           [42, 0, 42], [None, "Format", None]),
    }
    expected_radix = {
        name: [
            {"text": text, "success": error is None, "value": value,
             "error": None if error is None else f"System.{error}Exception"}
            for text, value, error in zip(texts, values, errors)
        ]
        for name, (texts, values, errors) in radix_styles.items()
    }
    expected_radix["invalid"] = [
        {"value": value, "parseError": "System.ArgumentException",
         "tryParseError": "System.ArgumentException"}
        for value in (516, 1056, 1536, 576)
    ]
    assert metadata["selectedInt32RadixFlagStyles"] == expected_radix
    assert metadata["selectedInt32StyleValidationPrecedence"] == {
        "invalid": [
            {"value": value,
             "nullParse": {"type": "System.ArgumentNullException", "paramName": "s"},
             "nullTryParse": {"type": "System.ArgumentException", "paramName": "style"},
             "overflowParse": {"type": "System.ArgumentException", "paramName": "style"},
             "overflowTryParse": {"type": "System.ArgumentException", "paramName": "style"}}
            for value in (516, 1056, 1536, 576)
        ],
        "validNullParse": {"type": "System.ArgumentNullException", "paramName": "s"},
        "validNullSuccess": False,
        "validNullValue": 0,
    }
    exponent_texts = ["0e1001", "0e999999999", "0e2147483647", "0e2147483648",
                      "1e1001", "1e999999999", "1e~1001", "0e~1001",
                      "0e~999999999", "0e~2147483648", "2147483647",
                      "~2147483648", "2147483648", "~2147483649",
                      "214748364:7e1", "214748364:8e1"]
    exponent_values = [0] * 10 + [2147483647, -2147483648, 0, 0, 2147483647, 0]
    exponent_errors = [None] * 4 + ["Overflow"] * 3 + [None] * 3 \
        + [None] * 2 + ["Overflow"] * 2 + [None, "Overflow"]
    assert metadata["selectedInt32ExponentLimits"] == [
        {"text": text, "success": error is None, "value": value,
         "error": None if error is None else f"System.{error}Exception"}
        for text, value, error in zip(exponent_texts, exponent_values, exponent_errors)
    ]
    general_styles = {
        "signDecimal": (44, ["~42:00", "42:00~", "~42:00~", "42:5", "42"],
                        [-42, -42, 0, 0, 42],
                        [None, None, "Format", "Overflow", None]),
        "groupedExponent": (192, ["12_345e1", "12_345e~1", "~12_345e1",
                                 "12_345:00e1", "12_345"],
                            [123450, 0, 0, 0, 12345],
                            [None, "Overflow", "Format", "Format", None]),
        "parenthesizedExponent": (144, ["(42e1)", "42e1", "~42e1",
                                       "(42e~1)", "(42)"],
                                  [-420, 420, 0, 0, -42],
                                  [None, None, "Format", "Overflow", None]),
        "paddedGroupedExponent": (227, [" 12_345:00e1 ", "~12_345:00e1",
                                         "12_345:5e0", " 42 "],
                                    [123450, 0, 0, 42],
                                    [None, "Format", "Overflow", None]),
        "signedParentheses": (148, ["(~42e1)", "(42e1)", "~42e1",
                                    "plus42e1", "(42e~1)"],
                               [0, -420, -420, 420, 0],
                               ["Format", None, None, None, "Overflow"]),
    }
    assert metadata["selectedInt32GeneralFlagStyles"] == {
        key: value
        for name, (flags, texts, values, errors) in general_styles.items()
        for key, value in (
            (name + "Value", flags),
            (name, [
                {"text": text, "success": error is None, "value": value,
                 "error": None if error is None else f"System.{error}Exception"}
                for text, value, error in zip(texts, values, errors)
            ]),
        )
    }
    assert metadata["selectedBaseExceptionBehavior"] == {
        "standaloneIsSelf": True,
        "rootIsSelf": True,
        "middleReturnsRoot": True,
        "chainReturnsRoot": True,
        "chainInnerPreserved": True,
        "baseType": "System.InvalidOperationException",
        "baseMessage": "root",
    }
    assert metadata["selectedExceptionDataBehavior"] == {
        "startsEmpty": True,
        "sameReference": True,
        "storedValue": "value",
        "countAfterInsert": 1,
        "separateInstance": True,
        "secondStartsEmpty": True,
    }
    assert metadata["selectedExceptionHResultBehavior"] == {
        "parameterless": -2146233088,
        "message": -2146233088,
        "inner": -2146233088,
        "argument": -2147024809,
        "invalidOperation": -2146233079,
    }
    assert metadata["selectedExceptionHelpLinkBehavior"] == {
        "startsNull": True,
        "afterSet": "https://example.invalid/help",
        "afterReset": None,
        "separateInstanceIsNull": True,
    }
    assert metadata["selectedExceptionSourceBehavior"] == {
        "beforeSet": None,
        "afterSet": "selected.component",
        "afterReset": None,
        "separateInstance": None,
    }
    assert metadata["selectedExceptionToStringBehavior"] == {
        "exceptionWithMessage": "System.Exception: message",
        "exceptionWithoutMessage": "System.Exception: Exception of type 'System.Exception' was thrown.",
        "argumentWithParameter": "System.ArgumentException: invalid (Parameter 'value')",
        "invalidOperation": "System.InvalidOperationException: invalid",
    }
    assert metadata["selectedExceptionInnerToStringBehavior"] == {
        "twoLevel": "System.Exception: outer\r\n ---> System.Exception: inner"
                    "\r\n   --- End of inner exception stack trace ---",
        "threeLevel": "System.ArgumentException: outer (Parameter 'value')"
                      "\r\n ---> System.Exception: middle"
                      "\r\n ---> System.InvalidOperationException: root"
                      "\r\n   --- End of inner exception stack trace ---"
                      "\r\n   --- End of inner exception stack trace ---",
    }
    assert metadata["selectedExceptionRuntimeTypeBehavior"] == {
        "baseType": "System.Exception",
        "argumentType": "System.ArgumentException",
        "invalidOperationType": "System.InvalidOperationException",
        "repeatedReference": True,
    }
    assert metadata["selectedExceptionStackBoundary"] == {
        "prethrowStackIsNull": True,
        "prethrowTargetSiteIsNull": True,
        "thrownStackNonEmpty": True,
        "thrownTargetSitePresent": True,
    }
    assert metadata["selectedExceptionRethrowBoundary"] == {
        "sameReference": True,
        "stackBeforeNonEmpty": True,
        "stackAfterNonEmpty": True,
        "stackTextUnchanged": True,
    }
    assert metadata["selectedTypeCodeBehavior"] == {
        "nullType": "Empty",
        "objectType": "Object",
        "stringType": "String",
        "booleanType": "Boolean",
        "charType": "Char",
        "byteType": "Byte",
        "int16Type": "Int16",
        "int32Type": "Int32",
        "int64Type": "Int64",
        "singleType": "Single",
        "doubleType": "Double",
        "decimalType": "Decimal",
        "dateTimeType": "DateTime",
        "enumType": "Int32",
        "arrayType": "Object",
        "genericType": "Object",
    }
    assert metadata["selectedTypeArrayBehavior"] == {
        "mixed": {"result": ["System.String", "System.Int32", "System.Exception"],
                  "exception": None, "paramName": None},
        "empty": {"result": [], "exception": None, "paramName": None},
        "nullArray": {"result": None, "exception": "System.ArgumentNullException",
                      "paramName": "args"},
        "nullElement": {"result": None, "exception": "System.ArgumentException",
                        "paramName": "args"},
        "separateArrays": True,
    }
    assert metadata["selectedTypeHashBehavior"] == {
        "stringRepeatStable": True,
        "stringLookupStable": True,
        "int32RepeatStable": True,
        "genericRepeatStable": True,
    }
    assert metadata["selectedAssignableToBehavior"] == {
        "stringToObject": True,
        "objectToString": False,
        "stringToComparable": True,
        "comparableToString": False,
        "stringToSelf": True,
        "stringToNull": False,
        "int32ToValueType": True,
    }
    assert metadata["selectedEquivalentTypeBehavior"] == {
        "stringSelf": True,
        "stringLookup": True,
        "stringInt32": False,
        "stringNull": False,
        "genericSame": True,
        "genericDifferent": False,
        "vectorRankTwo": False,
    }
    assert type_evidence["sourceSha256"] == sha256(next(path for path in SOURCES if path.name == "Type.java"))
    assert disposal_evidence["sourceSha256"] == sha256(SOURCES[0])

    for output_dir in (CLASSES, CONSUMER_CLASSES):
        output_dir.mkdir(parents=True, exist_ok=True)
        for stale_class in output_dir.rglob("*.class"):
            stale_class.unlink()
    run("javac", "--release", "21", "-d", str(CLASSES), *(str(path) for path in SOURCES))
    class_files = sorted(path.relative_to(CLASSES).as_posix() for path in CLASSES.rglob("*.class"))
    assert class_files == EXPECTED_CLASSES, class_files
    public_type = run("javap", "-public", "-classpath", str(CLASSES), "System.Type")
    members = [line.strip() for line in public_type.splitlines() if line.strip().endswith(";")]
    assert members == type_evidence["publicMembers"]
    public_disposal = run("javap", "-public", "-classpath", str(CLASSES), "System.IDisposable")
    assert "public abstract void Dispose();" in public_disposal

    manifest = b"Manifest-Version: 1.0\r\nCreated-By: dotj-core foundation candidate\r\n\r\n"
    with zipfile.ZipFile(JAR, "w") as archive:
        for name, data in [("META-INF/MANIFEST.MF", manifest),
                           ("META-INF/LICENSE", LICENSE.read_bytes()), *[
            (name, (CLASSES / name).read_bytes()) for name in class_files]]:
            entry = zipfile.ZipInfo(name, date_time=(2026, 10, 21, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_STORED
            entry.create_system = 0
            entry.external_attr = 0
            archive.writestr(entry, data)
    with zipfile.ZipFile(JAR) as archive:
        assert archive.namelist() == ["META-INF/MANIFEST.MF", "META-INF/LICENSE", *class_files]
        assert archive.read("META-INF/LICENSE") == LICENSE.read_bytes()

    run("javac", "--release", "21", "-cp", str(JAR), "-d", str(CONSUMER_CLASSES),
        *(str(path) for path in CONSUMERS))
    classpath = os.pathsep.join((str(CONSUMER_CLASSES), str(JAR)))
    disposal_result = run("java", "-cp", classpath, "consumer.ProductDisposableContractConsumer").strip()
    type_result = run("java", "-cp", classpath, "consumer.ProductTypeIdentityConsumer").strip()
    exception_result = run("java", "-cp", classpath, "consumer.ProductExceptionContractConsumer").strip()
    int32_result = run("java", "-cp", classpath, "consumer.ProductInt32BitConsumer").strip()
    arithmetic_result = run("java", "-cp", classpath, "consumer.ProductInt32ArithmeticConsumer").strip()
    span_result = run("java", "-cp", classpath, "consumer.ProductInt32SpanConsumer").strip()
    decimal_result = run("java", "-cp", classpath, "consumer.ProductDecimalBitsConsumer").strip()
    assert disposal_result.startswith("PASS: product IDisposable shape")
    assert type_result == "PASS external System.Type selected identity consumer"
    assert exception_result == "PASS external selected Exception constructors and inner identity"
    assert int32_result == "PASS external selected Int32 bit helpers"
    assert arithmetic_result == "PASS external selected Int32 signed arithmetic"
    assert span_result == "PASS external selected Int32 span parsing and formatting"
    assert decimal_result == "PASS external selected Decimal bits"
    EVIDENCE.write_text(json.dumps({
        "schemaVersion": 1,
        "productSources": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)} for path in SOURCES],
        "jarPath": JAR.relative_to(ROOT).as_posix(),
        "jarSha256": sha256(JAR),
        "licensePath": LICENSE.relative_to(ROOT).as_posix(),
        "licenseSha256": sha256(LICENSE),
        "licenseEntry": "META-INF/LICENSE",
        "jarEntries": ["META-INF/MANIFEST.MF", "META-INF/LICENSE", *class_files],
        "classSha256": {name: sha256(CLASSES / name) for name in class_files},
        "disposalConsumer": disposal_result,
        "typeConsumer": type_result,
        "exceptionConsumer": exception_result,
        "int32BitConsumer": int32_result,
        "int32ArithmeticConsumer": arithmetic_result,
        "int32SpanConsumer": span_result,
        "decimalBitsConsumer": decimal_result,
        "exceptionStackBoundary": {
            "dotNetPrethrowStackNull": True,
            "dotNetThrownStackNonEmpty": True,
            "javaConstructedThrowableStackNonEmpty": True,
            "mappingStatus": "OPEN: construction and throw capture points differ",
        },
        "status": "BUILT_FOUNDATION_CANDIDATE; complete public API, behavior, E01 release rights and framework qualification OPEN",
    }, indent=2) + "\n", encoding="utf-8")
    print("PASS combined foundation candidate JAR and independent consumers")


if __name__ == "__main__":
    main()
