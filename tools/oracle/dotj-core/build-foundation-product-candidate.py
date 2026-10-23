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
    "ProductDecimalBitsConsumer", "ProductDecimalMultiplyConsumer",
    "ProductDecimalDivideConsumer", "ProductDecimalRemainderConsumer",
    "ProductDecimalCompareConsumer", "ProductDecimalEqualsConsumer",
    "ProductDecimalHashConsumer", "ProductDecimalInstanceEqualityConsumer",
    "ProductDecimalCompareToConsumer", "ProductDecimalToInt32Consumer",
    "ProductDecimalSignConsumer", "ProductDecimalIntegerPredicateConsumer",
    "ProductDecimalToInt64Consumer", "ProductDecimalToUInt32Consumer",
    "ProductDecimalToUInt64Consumer", "ProductDecimalSmallIntegerConsumer",
    "ProductDecimalFloatingConsumer", "ProductDecimalCopySignConsumer",
    "ProductDecimalMaxMinConsumer", "ProductDecimalClampConsumer", "ProductDecimalMagnitudeConsumer",
    "ProductDecimalOACurrencyConsumer",
    "ProductDecimalFromOACurrencyConsumer",
    "ProductDecimalFormattingConsumer",
    "ProductDecimalProviderFormattingConsumer",
    "ProductDecimalFixedProviderFormattingConsumer",
    "ProductDecimalFixedPrecision100Consumer",
    "ProductDecimalStandardPrecision100Consumer",
    "ProductDecimalPrecisionOverflowConsumer",
    "ProductDecimalGeneralPrecisionConsumer",
    "ProductDecimalRoundtripFormatConsumer",
    "ProductGeneralFormatInvalidBoundariesConsumer",
    "ProductDecimalNumberProviderFormattingConsumer",
    "ProductDecimalPercentProviderFormattingConsumer",
    "ProductDecimalCurrencyProviderFormattingConsumer",
    "ProductDecimalExponentialProviderFormattingConsumer",
    "ProductDecimalCustomProviderFormattingConsumer",
    "ProductDecimalNumberGroupSizesConsumer",
    "ProductDecimalCurrencyGroupSizesConsumer",
    "ProductDecimalPercentGroupSizesConsumer",
    "ProductDecimalCurrencyNegativePatternsConsumer",
    "ProductDecimalPercentPositivePatternsConsumer",
    "ProductDecimalPercentNegativePatternsConsumer",
    "ProductDecimalNumberNegativePatternsConsumer",
    "ProductDecimalNumberNegativeRoundingConsumer",
    "ProductDecimalGetFormatProviderConsumer",
    "ProductDecimalCurrencyPositivePatternsConsumer",
    "ProductInt32CurrencyPositivePatternsConsumer",
    "ProductInt32CurrencyNegativePatternsConsumer",
    "ProductInt32PercentPositivePatternsConsumer",
    "ProductInt32PercentNegativePatternsConsumer",
    "ProductInt32NumberNegativePatternsConsumer",
    "ProductInt32NumberHighPrecisionConsumer",
    "ProductInt32DecimalHighPrecisionConsumer",
    "ProductInt32RadixHighPrecisionConsumer",
    "ProductInt32FixedHighPrecisionConsumer",
    "ProductInt32CurrencyHighPrecisionConsumer",
    "ProductInt32PercentHighPrecisionConsumer",
    "ProductInt32ExponentialHighPrecisionConsumer",
    "ProductInt32StandardPrecision2049Consumer",
    "ProductInt32GeneralPrecisionConsumer",
    "ProductInt32RoundtripFormatConsumer",
    "ProductNumberNegativePatternBoundariesConsumer",
    "ProductDecimalFormatStringsConsumer",
    "ProductDecimalFixedPrecisionConsumer",
    "ProductDecimalNumberFormattingConsumer",
    "ProductDecimalPercentFormattingConsumer",
    "ProductDecimalExponentialFormattingConsumer",
    "ProductDecimalCurrencyFormattingConsumer",
    "ProductDecimalCustomZeroFormattingConsumer",
    "ProductDecimalCustomOptionalFormattingConsumer",
    "ProductDecimalFloatStyleParseConsumer",
    "ProductDecimalNumberStyleParseConsumer",
    "ProductDecimalIntegerStyleParseConsumer",
    "ProductDecimalCurrencyStyleParseConsumer",
    "ProductDecimalAnyStyleParseConsumer",
    "ProductDecimalCustomProviderParseConsumer",
    "ProductDecimalCustomCurrencyProviderParseConsumer",
    "ProductDecimalAnyCustomProviderParseConsumer",
    "ProductDecimalNoneStyleParseConsumer",
    "ProductDecimalThousandsStyleParseConsumer",
    "ProductDecimalPointStyleParseConsumer",
    "ProductDecimalExponentStyleParseConsumer",
    "ProductDecimalLeadingSignStyleParseConsumer",
    "ProductDecimalTrailingSignStyleParseConsumer",
    "ProductDecimalParenthesesStyleParseConsumer",
    "ProductDecimalLeadingWhiteStyleParseConsumer",
    "ProductDecimalTrailingWhiteStyleParseConsumer",
    "ProductDecimalCurrencySymbolStyleParseConsumer",
    "ProductDecimalComposedStyleParseConsumer",
    "ProductDecimalCustomCurrencySymbolParseConsumer",
    "ProductDecimalTryParseConsumer",
    "ProductDecimalProviderTryParseConsumer",
    "ProductDecimalSpanTryParseConsumer",
    "ProductDecimalUtf8SpanParseConsumer",
    "ProductDecimalSpanProviderTryParseConsumer",
    "ProductDecimalParseProviderConsumer",
    "ProductDecimalCanonicalConsumer")]
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
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {command[0]}\n{result.stderr}")
    return result.stdout


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
    float_style_vectors = metadata["selectedDecimalFloatStyleParse"]
    assert len(float_style_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in float_style_vectors)
    assert float_style_vectors[0]["bits"] == [100, 0, 0, 0]
    assert float_style_vectors[6]["bits"] == [0, 0, 0, 1835008]
    assert float_style_vectors[10]["error"] == "System.OverflowException"
    number_style_vectors = metadata["selectedDecimalNumberStyleParse"]
    assert len(number_style_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in number_style_vectors)
    assert number_style_vectors[0]["bits"] == [123450, 0, 0, 131072]
    assert number_style_vectors[5]["error"] == "System.FormatException"
    assert number_style_vectors[17]["error"] == "System.OverflowException"
    integer_style_vectors = metadata["selectedDecimalIntegerStyleParse"]
    assert len(integer_style_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in integer_style_vectors)
    assert integer_style_vectors[1]["bits"] == [0, 0, 0, -2147483648]
    assert integer_style_vectors[7]["error"] == "System.FormatException"
    assert integer_style_vectors[13]["error"] == "System.OverflowException"
    currency_style_vectors = metadata["selectedDecimalCurrencyStyleParse"]
    assert len(currency_style_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in currency_style_vectors)
    assert currency_style_vectors[4]["bits"] == [125, 0, 0, -2147352576]
    assert currency_style_vectors[10]["error"] == "System.FormatException"
    assert currency_style_vectors[17]["error"] == "System.OverflowException"
    any_style_vectors = metadata["selectedDecimalAnyStyleParse"]
    assert len(any_style_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in any_style_vectors)
    assert any_style_vectors[0]["bits"] == [100, 0, 0, 0]
    assert any_style_vectors[12]["error"] == "System.OverflowException"
    assert any_style_vectors[14]["error"] == "System.FormatException"
    custom_provider_vectors = metadata["selectedDecimalCustomProviderParse"]
    assert len(custom_provider_vectors) == 20
    assert all(entry["style"] in ("Number", "Float") and
               ((entry["bits"] is not None and len(entry["bits"]) == 4
                 and entry["error"] is None)
                or (entry["bits"] is None and entry["error"] in
                    ("System.FormatException", "System.OverflowException")))
               for entry in custom_provider_vectors)
    assert custom_provider_vectors[0]["bits"] == [123450, 0, 0, 131072]
    assert custom_provider_vectors[5]["error"] == "System.FormatException"
    assert custom_provider_vectors[17]["error"] == "System.OverflowException"
    custom_currency_vectors = metadata["selectedDecimalCustomCurrencyProviderParse"]
    assert len(custom_currency_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in custom_currency_vectors)
    assert custom_currency_vectors[0]["bits"] == [123450, 0, 0, 131072]
    assert custom_currency_vectors[8]["error"] == "System.FormatException"
    assert custom_currency_vectors[17]["error"] == "System.OverflowException"
    any_custom_provider_vectors = metadata["selectedDecimalAnyCustomProviderParse"]
    assert len(any_custom_provider_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in any_custom_provider_vectors)
    assert any_custom_provider_vectors[0]["bits"] == [123450, 0, 0, 131072]
    assert any_custom_provider_vectors[6]["error"] == "System.FormatException"
    assert any_custom_provider_vectors[19]["error"] == "System.OverflowException"
    none_style_vectors = metadata["selectedDecimalNoneStyleParse"]
    assert len(none_style_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in none_style_vectors)
    assert none_style_vectors[0]["bits"] == [0, 0, 0, 0]
    assert none_style_vectors[3]["error"] == "System.FormatException"
    assert none_style_vectors[14]["error"] == "System.OverflowException"
    thousands_style_vectors = metadata["selectedDecimalThousandsStyleParse"]
    assert len(thousands_style_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in thousands_style_vectors)
    assert thousands_style_vectors[2]["bits"] == [1234, 0, 0, 0]
    assert thousands_style_vectors[6]["bits"] == [12, 0, 0, 0]
    assert thousands_style_vectors[16]["error"] == "System.OverflowException"
    point_style_vectors = metadata["selectedDecimalPointStyleParse"]
    assert len(point_style_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in point_style_vectors)
    assert point_style_vectors[1]["bits"] == [125, 0, 0, 131072]
    assert point_style_vectors[4]["error"] == "System.FormatException"
    assert point_style_vectors[16]["error"] == "System.OverflowException"
    exponent_style_vectors = metadata["selectedDecimalExponentStyleParse"]
    assert len(exponent_style_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in exponent_style_vectors)
    assert exponent_style_vectors[2]["bits"] == [100, 0, 0, 0]
    assert exponent_style_vectors[5]["error"] == "System.FormatException"
    assert exponent_style_vectors[13]["error"] == "System.OverflowException"
    leading_sign_vectors = metadata["selectedDecimalLeadingSignStyleParse"]
    assert len(leading_sign_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in leading_sign_vectors)
    assert leading_sign_vectors[1]["bits"] == [0, 0, 0, -2147483648]
    assert leading_sign_vectors[6]["error"] == "System.FormatException"
    assert leading_sign_vectors[17]["error"] == "System.OverflowException"
    trailing_sign_vectors = metadata["selectedDecimalTrailingSignStyleParse"]
    assert len(trailing_sign_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in trailing_sign_vectors)
    assert trailing_sign_vectors[1]["bits"] == [0, 0, 0, -2147483648]
    assert trailing_sign_vectors[6]["error"] == "System.FormatException"
    assert trailing_sign_vectors[17]["error"] == "System.OverflowException"
    parentheses_vectors = metadata["selectedDecimalParenthesesStyleParse"]
    assert len(parentheses_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in parentheses_vectors)
    assert parentheses_vectors[1]["bits"] == [0, 0, 0, -2147483648]
    assert parentheses_vectors[5]["error"] == "System.FormatException"
    assert parentheses_vectors[18]["error"] == "System.OverflowException"
    leading_white_vectors = metadata["selectedDecimalLeadingWhiteStyleParse"]
    assert len(leading_white_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in leading_white_vectors)
    assert leading_white_vectors[1]["bits"] == [42, 0, 0, 0]
    assert leading_white_vectors[5]["error"] == "System.FormatException"
    assert leading_white_vectors[19]["error"] == "System.OverflowException"
    trailing_white_vectors = metadata["selectedDecimalTrailingWhiteStyleParse"]
    assert len(trailing_white_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in trailing_white_vectors)
    assert trailing_white_vectors[1]["bits"] == [42, 0, 0, 0]
    assert trailing_white_vectors[5]["error"] == "System.FormatException"
    assert trailing_white_vectors[19]["error"] == "System.OverflowException"
    currency_symbol_vectors = metadata["selectedDecimalCurrencySymbolStyleParse"]
    assert len(currency_symbol_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in currency_symbol_vectors)
    assert currency_symbol_vectors[0]["bits"] == [1, 0, 0, 0]
    assert currency_symbol_vectors[2]["error"] == "System.FormatException"
    assert currency_symbol_vectors[17]["error"] == "System.OverflowException"
    composed_style_vectors = metadata["selectedDecimalComposedStyleParse"]
    assert len(composed_style_vectors) == 20
    assert all(entry["style"] in (36, 96, 3) and
               ((entry["bits"] is not None and len(entry["bits"]) == 4
                 and entry["error"] is None)
                or (entry["bits"] is None and entry["error"] in
                    ("System.FormatException", "System.OverflowException")))
               for entry in composed_style_vectors)
    assert composed_style_vectors[0]["bits"] == [125, 0, 0, -2147352576]
    assert composed_style_vectors[9]["bits"] == [125, 0, 0, 65536]
    assert composed_style_vectors[19]["error"] == "System.OverflowException"
    custom_symbol_vectors = metadata["selectedDecimalCustomCurrencySymbolStyleParse"]
    assert len(custom_symbol_vectors) == 20
    assert all((entry["bits"] is not None and len(entry["bits"]) == 4
                and entry["error"] is None)
               or (entry["bits"] is None and entry["error"] in
                   ("System.FormatException", "System.OverflowException"))
               for entry in custom_symbol_vectors)
    assert custom_symbol_vectors[0]["bits"] == [1, 0, 0, 0]
    assert custom_symbol_vectors[4]["error"] == "System.FormatException"
    assert custom_symbol_vectors[18]["error"] == "System.OverflowException"
    decimal_try_vectors = metadata["selectedDecimalTryParse"]
    assert len(decimal_try_vectors) == 20
    assert all(entry["mode"] in ("Simple", "Number", "Float", "Integer")
               and isinstance(entry["success"], bool)
               and len(entry["bits"]) == 4
               for entry in decimal_try_vectors)
    assert decimal_try_vectors[0]["success"] is True
    assert decimal_try_vectors[2]["bits"] == [0, 0, 0, 0]
    assert decimal_try_vectors[14]["bits"] == [0, 0, 0, 1835008]
    provider_try_vectors = metadata["selectedDecimalProviderTryParse"]
    assert len(provider_try_vectors) == 20
    assert all(isinstance(entry["success"], bool)
               and len(entry["bits"]) == 4 for entry in provider_try_vectors)
    assert provider_try_vectors[0]["bits"] == [123450, 0, 0, 131072]
    assert provider_try_vectors[5]["success"] is False
    assert provider_try_vectors[15]["bits"] == [0, 0, 0, 0]
    span_try_vectors = metadata["selectedDecimalSpanTryParse"]
    assert len(span_try_vectors) == 20
    assert all(entry["mode"] in ("Simple", "Number", "Float", "Integer")
               and isinstance(entry["success"], bool)
               and len(entry["bits"]) == 4 for entry in span_try_vectors)
    assert span_try_vectors[0]["bits"] == [42, 0, 0, 0]
    assert span_try_vectors[2]["success"] is False
    assert span_try_vectors[12]["bits"] == [0, 0, 0, 1835008]
    utf8_span_vectors = metadata["selectedDecimalUtf8SpanParse"]
    assert len(utf8_span_vectors) == 20
    assert all(entry["mode"] in ("Simple", "Number", "Float", "Integer")
               and isinstance(entry["success"], bool)
               and len(entry["bits"]) == 4
               and entry["error"] in (None, "System.FormatException",
                                       "System.OverflowException")
               for entry in utf8_span_vectors)
    assert utf8_span_vectors[0]["bits"] == [42, 0, 0, 0]
    assert utf8_span_vectors[2]["error"] == "System.FormatException"
    assert utf8_span_vectors[11]["error"] == "System.OverflowException"
    span_provider_vectors = metadata["selectedDecimalSpanProviderTryParse"]
    assert len(span_provider_vectors) == 20
    assert all(entry["carrier"] in ("Char", "Utf8")
               and isinstance(entry["success"], bool)
               and len(entry["bits"]) == 4 for entry in span_provider_vectors)
    assert span_provider_vectors[0]["bits"] == [123450, 0, 0, 131072]
    assert span_provider_vectors[3]["success"] is False
    assert span_provider_vectors[15]["bits"] == [1, 0, 0, 1835008]
    parse_provider_vectors = metadata["selectedDecimalParseProvider"]
    assert len(parse_provider_vectors) == 20
    assert all(entry["carrier"] in ("String", "Char", "Utf8")
               and ((entry["bits"] is not None and len(entry["bits"]) == 4
                     and entry["error"] is None)
                    or (entry["bits"] is None and entry["error"] in
                        ("System.ArgumentNullException", "System.FormatException",
                         "System.OverflowException")))
               for entry in parse_provider_vectors)
    assert parse_provider_vectors[0]["bits"] == [123450, 0, 0, 131072]
    assert parse_provider_vectors[6]["error"] == "System.ArgumentNullException"
    assert parse_provider_vectors[19]["error"] == "System.OverflowException"
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
    abs_sign = metadata["selectedDecimalAbsSign"]
    abs_sign_inputs = ([0, 0, 0, 0], [0, 0, 0, -2147483648],
                       [0, 0, 0, -2147352576], [12345, 0, 0, 131072],
                       [12345, 0, 0, -2147352576], [1, 0, 0, 1835008],
                       [1, 0, 0, -2145648640], [-1, -1, -1, 0],
                       [-1, -1, -1, -2147483648])
    abs_sign_results = (0, 0, 0, 1, -1, 1, -1, 1, -1)
    assert [(entry["input"], entry["absolute"], entry["sign"])
            for entry in abs_sign] == [
        (bits, [*bits[:3], bits[3] & 0x7fffffff], sign)
        for bits, sign in zip(abs_sign_inputs, abs_sign_results)]
    negate_inputs = (abs_sign_inputs[0], abs_sign_inputs[1],
                     [0, 0, 0, 131072], abs_sign_inputs[2],
                     *abs_sign_inputs[3:])
    assert [(entry["input"], entry["negated"])
            for entry in metadata["selectedDecimalNegate"]] == [
        (bits, [*bits[:3], bits[3] ^ -2147483648]) for bits in negate_inputs]
    add_operands = ([0, 0, 0, 0], [0, 0, 0, -2147352576],
                    [100, 0, 0, 131072], [2, 0, 0, 0],
                    [125, 0, 0, -2147352576], [125, 0, 0, 131072],
                    [1, 0, 0, 1835008], [-1, -1, -1, 0],
                    [1, 0, 0, 0], [1, 0, 0, -2147483648],
                    [-1, -1, -1, -2147483648], [1, 0, 0, 65536],
                    [5, 0, 0, 65536], [5, 0, 0, -2147418112],
                    [200, 0, 0, 131072], [1, 0, 0, -2145648640])
    add_pairs = ((0, 0), (1, 1), (1, 0), (0, 1), (2, 3),
                 (2, 4), (5, 4), (4, 5), (6, 6), (7, 0),
                 (7, 8), (7, 9), (10, 9), (7, 10), (10, 7),
                 (7, 11), (7, 6), (12, 12), (13, 12), (13, 13), (8, 9))
    add_results = ([0, 0, 0, 0], [0, 0, 0, -2147352576],
                   [0, 0, 0, -2147352576], [0, 0, 0, -2147352576],
                   [300, 0, 0, 131072], [25, 0, 0, -2147352576],
                   [0, 0, 0, 131072], [0, 0, 0, -2147352576],
                   [2, 0, 0, 1835008], [-1, -1, -1, 0],
                   None, [-2, -1, -1, 0], None,
                   [0, 0, 0, 0], [0, 0, 0, -2147483648],
                   [-1, -1, -1, 0], [-1, -1, -1, 0],
                   [10, 0, 0, 65536], [0, 0, 0, -2147418112],
                   [10, 0, 0, -2147418112], [0, 0, 0, 0])
    assert [(entry["left"], entry["right"], entry["result"], entry["error"])
            for entry in metadata["selectedDecimalAdd"]] == [
        (add_operands[left], add_operands[right], result,
         "System.OverflowException" if result is None else None)
        for (left, right), result in zip(add_pairs, add_results)]
    subtract_pairs = ((0, 0), (1, 0), (0, 1), (1, 1),
                      (2, 14), (14, 2), (5, 5), (4, 4),
                      (7, 9), (7, 8), (10, 8), (10, 9),
                      (6, 6), (15, 15), (12, 12), (13, 13),
                      (7, 7), (10, 10))
    subtract_results = ([0, 0, 0, 0], [0, 0, 0, -2147352576],
                        [0, 0, 0, 131072], [0, 0, 0, -2147352576],
                        [100, 0, 0, -2147352576], [100, 0, 0, 131072],
                        [0, 0, 0, 131072], [0, 0, 0, -2147352576],
                        None, [-2, -1, -1, 0], None,
                        [-2, -1, -1, -2147483648],
                        [0, 0, 0, 1835008], [0, 0, 0, -2145648640],
                        [0, 0, 0, 65536], [0, 0, 0, -2147418112],
                        [0, 0, 0, 0], [0, 0, 0, -2147483648])
    assert [(entry["left"], entry["right"], entry["result"], entry["error"])
            for entry in metadata["selectedDecimalSubtract"]] == [
        (add_operands[left], add_operands[right], result,
         "System.OverflowException" if result is None else None)
        for (left, right), result in zip(subtract_pairs, subtract_results)]
    multiply_vectors = metadata["selectedDecimalMultiply"]
    assert len(multiply_vectors) == 38
    assert all(len(entry["left"]) == len(entry["right"]) == 4
               and (entry["result"] is None or len(entry["result"]) == 4)
               and (entry["error"] == "System.OverflowException") == (entry["result"] is None)
               for entry in multiply_vectors)
    assert multiply_vectors[7]["result"] == [0, 0, 0, -2147221504]
    assert multiply_vectors[15]["result"] == [0, 0, 0, 0]
    assert multiply_vectors[28]["result"] == [-1, -1, -1, 65536]
    divide_vectors = metadata["selectedDecimalDivide"]
    assert len(divide_vectors) == 20
    assert all(len(entry["left"]) == len(entry["right"]) == 4
               and (entry["result"] is None or len(entry["result"]) == 4)
               and (entry["error"] is None) == (entry["result"] is not None)
               for entry in divide_vectors)
    assert divide_vectors[1]["result"] == [89478485, 347537611, 180700362, 1835008]
    assert divide_vectors[6]["error"] == "System.DivideByZeroException"
    assert divide_vectors[14]["error"] == "System.OverflowException"
    assert divide_vectors[15]["result"] == [0, 0, 0, 0]
    remainder_vectors = metadata["selectedDecimalRemainder"]
    assert len(remainder_vectors) == 20
    assert all(len(entry["left"]) == len(entry["right"]) == 4
               and (entry["result"] is None or len(entry["result"]) == 4)
               and (entry["error"] == "System.DivideByZeroException") == (entry["result"] is None)
               for entry in remainder_vectors)
    assert remainder_vectors[4]["result"] == [25, 0, 0, 131072]
    assert remainder_vectors[9]["result"] == [0, 0, 0, -2147352576]
    assert remainder_vectors[11]["error"] == "System.DivideByZeroException"
    assert remainder_vectors[14]["result"] == [0, 0, 0, 0]
    compare_vectors = metadata["selectedDecimalCompare"]
    assert len(compare_vectors) == 20
    assert all(len(entry["left"]) == len(entry["right"]) == 4
               and entry["result"] in (-1, 0, 1) for entry in compare_vectors)
    assert [entry["result"] for entry in compare_vectors[:9]] == [
        0, 0, 0, 1, -1, -1, 1, 0, 0]
    assert compare_vectors[11]["result"] == 1
    assert compare_vectors[17]["result"] == -1
    equals_vectors = metadata["selectedDecimalEquals"]
    assert len(equals_vectors) == 20
    assert all(len(entry["left"]) == len(entry["right"]) == 4
               and type(entry["result"]) is bool for entry in equals_vectors)
    assert [entry["result"] for entry in equals_vectors[:8]] == [
        True, True, True, True, False, False, True, True]
    assert equals_vectors[16]["result"] is True
    assert equals_vectors[17]["result"] is False
    hash_vectors = metadata["selectedDecimalHashCodes"]
    assert len(hash_vectors) == 20
    assert all(len(entry["bits"]) == 4 and type(entry["result"]) is int
               for entry in hash_vectors)
    hash_values = [entry["result"] for entry in hash_vectors]
    assert hash_values[:7] == [0, 0, 0, 0, 1, 1, 1]
    assert hash_values[7] == hash_values[8] == -2147483647
    assert hash_values[9] == hash_values[10] == 131197
    assert hash_values[12:14] == [-1, 2147483647]
    instance_equals_vectors = metadata["selectedDecimalInstanceEquals"]
    assert len(instance_equals_vectors) == 12
    assert all(len(entry["left"]) == len(entry["right"]) == 4
               and entry["typedResult"] == entry["objectResult"]
               and entry["unrelatedResult"] is False
               and entry["nullResult"] is False
               and entry["hashMatches"] is True
               for entry in instance_equals_vectors)
    assert [entry["typedResult"] for entry in instance_equals_vectors] == [
        True, True, True, True, True, False, True, True, False, False, True, False]
    compare_to_vectors = metadata["selectedDecimalCompareTo"]
    assert len(compare_to_vectors) == 12
    assert all(len(entry["left"]) == len(entry["right"]) == 4
               and entry["typedResult"] == entry["objectResult"]
               and entry["typedResult"] in (-1, 0, 1)
               and entry["nullResult"] == 1
               and entry["wrongTypeError"] == "System.ArgumentException"
               for entry in compare_to_vectors)
    assert [entry["typedResult"] for entry in compare_to_vectors] == [
        0, 0, 1, -1, -1, 0, 1, -1, 1, 1, -1, -1]
    to_int32_vectors = metadata["selectedDecimalToInt32"]
    assert len(to_int32_vectors) == 20
    assert all(len(entry["bits"]) == 4
               and (entry["result"] is None) == (entry["error"] == "System.OverflowException")
               for entry in to_int32_vectors)
    assert [entry["result"] for entry in to_int32_vectors[:9]] == [
        0, 0, 1, -1, 1, -1, 2, -2, 2147483647]
    assert to_int32_vectors[10]["result"] == -2147483648
    assert to_int32_vectors[16]["result"] == 2147483647
    sign_vectors = metadata["selectedDecimalSignPredicates"]
    assert len(sign_vectors) == 12
    assert all(len(entry["bits"]) == 4
               and entry["negative"] is not entry["positive"]
               for entry in sign_vectors)
    assert [(entry["negative"], entry["positive"]) for entry in sign_vectors[:4]] == [
        (False, True), (True, False), (False, True), (True, False)]
    integer_vectors = metadata["selectedDecimalIntegerPredicates"]
    assert len(integer_vectors) == 14
    assert all(len(entry["bits"]) == 4
               and (entry["even"] is False and entry["odd"] is False
                    if entry["integer"] is False else entry["even"] is not entry["odd"])
               for entry in integer_vectors)
    assert [(entry["integer"], entry["even"], entry["odd"])
            for entry in integer_vectors[:5]] == [
        (True, True, False), (True, True, False), (True, False, True),
        (True, False, True), (True, True, False)]
    to_int64_vectors = metadata["selectedDecimalToInt64"]
    assert len(to_int64_vectors) == 20
    assert all(len(entry["bits"]) == 4
               and (entry["result"] is None) == (entry["error"] == "System.OverflowException")
               for entry in to_int64_vectors)
    assert [entry["result"] for entry in to_int64_vectors[:9]] == [
        0, 0, 1, -1, 1, -1, 2, -2, 9223372036854775807]
    assert to_int64_vectors[10]["result"] == -9223372036854775808
    assert to_int64_vectors[16]["result"] == 4294967296
    to_uint32_vectors = metadata["selectedDecimalToUInt32"]
    assert len(to_uint32_vectors) == 20
    assert all(len(entry["bits"]) == 4
               and (entry["result"] is None) == (entry["error"] == "System.OverflowException")
               for entry in to_uint32_vectors)
    assert [entry["result"] for entry in to_uint32_vectors[:5]] == [
        0, 0, 1, None, 1]
    assert to_uint32_vectors[8]["result"] == 4294967295
    assert to_uint32_vectors[16]["result"] == 4294967295
    assert to_uint32_vectors[17]["error"] == "System.OverflowException"
    to_uint64_vectors = metadata["selectedDecimalToUInt64"]
    assert len(to_uint64_vectors) == 20
    assert all(len(entry["bits"]) == 4
               and (entry["result"] is None) == (entry["error"] == "System.OverflowException")
               for entry in to_uint64_vectors)
    assert [entry["result"] for entry in to_uint64_vectors[:5]] == [
        0, 0, 1, None, 1]
    assert to_uint64_vectors[8]["result"] == 18446744073709551615
    assert to_uint64_vectors[16]["result"] == 18446744073709551615
    assert to_uint64_vectors[17]["error"] == "System.OverflowException"
    small_vectors = metadata["selectedDecimalSmallIntegerConversions"]
    assert len(small_vectors) == 20
    small_fields = ("toByte", "toSByte", "toInt16", "toUInt16")
    assert all(len(entry["bits"]) == 4 and all(
        (entry[field]["result"] is None)
        == (entry[field]["error"] == "System.OverflowException")
        for field in small_fields) for entry in small_vectors)
    assert [small_vectors[0][field]["result"] for field in small_fields] == [0, 0, 0, 0]
    assert [small_vectors[7][field]["result"] for field in small_fields] == [
        None, -128, -128, None]
    assert small_vectors[16]["toUInt16"]["result"] == 65535
    floating_vectors = metadata["selectedDecimalFloatingConversions"]
    assert len(floating_vectors) == 20
    assert all(len(entry["bits"]) == 4
               and type(entry["doubleBits"]) is int
               and type(entry["singleBits"]) is int for entry in floating_vectors)
    assert [(entry["doubleBits"], entry["singleBits"])
            for entry in floating_vectors[:4]] == [
        (0, 0), (-9223372036854775808, -2147483648),
        (4607182418800017408, 1065353216),
        (-4616189618054758400, -1082130432)]
    copy_sign_vectors = metadata["selectedDecimalCopySign"]
    assert len(copy_sign_vectors) == 20
    assert all(len(entry["value"]) == len(entry["sign"]) == len(entry["result"]) == 4
               for entry in copy_sign_vectors)
    assert [entry["result"] for entry in copy_sign_vectors[:4]] == [
        [0, 0, 0, 0], [0, 0, 0, -2147483648],
        [0, 0, 0, 131072], [0, 0, 0, -2147352576]]
    assert copy_sign_vectors[12]["result"] == [-1, -1, -1, -2147483648]
    max_min_vectors = metadata["selectedDecimalMaxMin"]
    assert len(max_min_vectors) == 20
    assert all(len(entry["left"]) == len(entry["right"])
               == len(entry["maximum"]) == len(entry["minimum"]) == 4
               for entry in max_min_vectors)
    assert max_min_vectors[0]["maximum"] == [0, 0, 0, 0]
    assert max_min_vectors[0]["minimum"] == [0, 0, 0, -2147352576]
    assert max_min_vectors[2]["maximum"] == [1, 0, 0, 0]
    assert max_min_vectors[2]["minimum"] == [100, 0, 0, 131072]
    clamp_vectors = metadata["selectedDecimalClamp"]
    assert len(clamp_vectors) == 20
    assert all(len(entry["value"]) == len(entry["lower"])
               == len(entry["upper"]) == 4 for entry in clamp_vectors)
    assert all((entry["result"] is not None and len(entry["result"]) == 4
                and entry["exception"] is None)
               or (entry["result"] is None and entry["exception"] == "ArgumentException")
               for entry in clamp_vectors)
    assert clamp_vectors[18]["exception"] == "ArgumentException"
    assert clamp_vectors[19]["exception"] == "ArgumentException"
    oa_currency_vectors = metadata["selectedDecimalOACurrency"]
    assert len(oa_currency_vectors) == 20
    assert all(len(entry["bits"]) == 4 and
               ((type(entry["result"]) is int and entry["exception"] is None)
                or (entry["result"] is None and entry["exception"] == "OverflowException"))
               for entry in oa_currency_vectors)
    assert [entry["result"] for entry in oa_currency_vectors[8:14]] == [0, 0, 2, -2, 2, -2]
    from_oa_currency_vectors = metadata["selectedDecimalFromOACurrency"]
    assert len(from_oa_currency_vectors) == 20
    assert all(type(entry["value"]) is int and len(entry["bits"]) == 4
               for entry in from_oa_currency_vectors)
    assert from_oa_currency_vectors[0]["bits"] == [0, 0, 0, 262144]
    assert from_oa_currency_vectors[9]["bits"] == [1, 0, 0, 0]
    formatting_vectors = metadata["selectedDecimalFormatting"]
    assert len(formatting_vectors) == 20
    assert all(len(entry["bits"]) == 4 and type(entry["invariant"]) is str
               for entry in formatting_vectors)
    assert [entry["invariant"] for entry in formatting_vectors[:4]] == [
        "0", "0", "0.00", "0.00"]
    provider_formatting_vectors = metadata["selectedDecimalProviderFormatting"]
    assert len(provider_formatting_vectors) == 12
    assert all(len(entry["bits"]) == 4 and type(entry["text"]) is str
               and type(entry["general"]) is str for entry in provider_formatting_vectors)
    assert [entry["text"] for entry in provider_formatting_vectors[:4]] == [
        "0", "0", "0@00", "0@00"]
    fixed_provider_vectors = metadata["selectedDecimalFixedProviderFormatting"]
    assert len(fixed_provider_vectors) == 12
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in fixed_provider_vectors)
    assert fixed_provider_vectors[0]["text"] == "0@000"
    number_provider_vectors = metadata["selectedDecimalNumberProviderFormatting"]
    assert len(number_provider_vectors) == 12
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in number_provider_vectors)
    assert number_provider_vectors[0]["text"] == "0@000"
    percent_provider_vectors = metadata["selectedDecimalPercentProviderFormatting"]
    assert len(percent_provider_vectors) == 12
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in percent_provider_vectors)
    assert percent_provider_vectors[0]["text"] == "0@000 pct"
    currency_provider_vectors = metadata["selectedDecimalCurrencyProviderFormatting"]
    assert len(currency_provider_vectors) == 12
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in currency_provider_vectors)
    assert currency_provider_vectors[0]["text"] == "USD0@000"
    exponential_provider_vectors = metadata["selectedDecimalExponentialProviderFormatting"]
    assert len(exponential_provider_vectors) == 12
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in exponential_provider_vectors)
    custom_format_provider_vectors = metadata["selectedDecimalCustomProviderFormatting"]
    assert len(custom_format_provider_vectors) == 12
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in custom_format_provider_vectors)
    number_group_size_vectors = metadata["selectedDecimalNumberGroupSizes"]
    assert len(number_group_size_vectors) == 12
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and entry["mode"] in (0, 1) and type(entry["text"]) is str
               for entry in number_group_size_vectors)
    currency_group_size_vectors = metadata["selectedDecimalCurrencyGroupSizes"]
    assert len(currency_group_size_vectors) == 12
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and entry["mode"] in (0, 1) and type(entry["text"]) is str
               for entry in currency_group_size_vectors)
    percent_group_size_vectors = metadata["selectedDecimalPercentGroupSizes"]
    assert len(percent_group_size_vectors) == 12
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and entry["mode"] in (0, 1) and type(entry["text"]) is str
               for entry in percent_group_size_vectors)
    currency_negative_pattern_vectors = metadata["selectedDecimalCurrencyNegativePatterns"]
    assert len(currency_negative_pattern_vectors) == 12
    assert all(len(entry["bits"]) == 4 and entry["pattern"] in (0, 1, 2, 3)
               and type(entry["text"]) is str
               for entry in currency_negative_pattern_vectors)
    currency_negative_pattern_4to7_vectors = metadata[
        "selectedDecimalCurrencyNegativePatterns4To7"]
    assert len(currency_negative_pattern_4to7_vectors) == 12
    assert all(len(entry["bits"]) == 4 and entry["pattern"] in (4, 5, 6, 7)
               and type(entry["text"]) is str
               for entry in currency_negative_pattern_4to7_vectors)
    currency_negative_pattern_8to11_vectors = metadata[
        "selectedDecimalCurrencyNegativePatterns8To11"]
    assert len(currency_negative_pattern_8to11_vectors) == 12
    assert all(len(entry["bits"]) == 4 and entry["pattern"] in (8, 9, 10, 11)
               and type(entry["text"]) is str
               for entry in currency_negative_pattern_8to11_vectors)
    currency_negative_pattern_12to16_vectors = metadata[
        "selectedDecimalCurrencyNegativePatterns12To16"]
    assert len(currency_negative_pattern_12to16_vectors) == 15
    assert all(len(entry["bits"]) == 4 and entry["pattern"] in (12, 13, 14, 15, 16)
               and type(entry["text"]) is str
               for entry in currency_negative_pattern_12to16_vectors)
    percent_positive_pattern_vectors = metadata["selectedDecimalPercentPositivePatterns"]
    assert len(percent_positive_pattern_vectors) == 12
    assert all(len(entry["bits"]) == 4 and entry["pattern"] in (0, 1, 2, 3)
               and type(entry["text"]) is str for entry in percent_positive_pattern_vectors)
    percent_negative_pattern_0to3_vectors = metadata[
        "selectedDecimalPercentNegativePatterns0To3"]
    assert len(percent_negative_pattern_0to3_vectors) == 12
    assert all(len(entry["bits"]) == 4 and entry["pattern"] in (0, 1, 2, 3)
               and type(entry["text"]) is str
               for entry in percent_negative_pattern_0to3_vectors)
    percent_negative_pattern_4to7_vectors = metadata[
        "selectedDecimalPercentNegativePatterns4To7"]
    assert len(percent_negative_pattern_4to7_vectors) == 12
    assert all(len(entry["bits"]) == 4 and entry["pattern"] in (4, 5, 6, 7)
               and type(entry["text"]) is str
               for entry in percent_negative_pattern_4to7_vectors)
    percent_negative_pattern_8to11_vectors = metadata[
        "selectedDecimalPercentNegativePatterns8To11"]
    assert len(percent_negative_pattern_8to11_vectors) == 12
    assert all(len(entry["bits"]) == 4 and entry["pattern"] in (8, 9, 10, 11)
               and type(entry["text"]) is str
               for entry in percent_negative_pattern_8to11_vectors)
    decimal_number_negative_vectors = metadata["selectedDecimalNumberNegativePatterns"]
    assert len(decimal_number_negative_vectors) == 15
    assert all(len(entry["bits"]) == 4 and entry["pattern"] in range(5)
               and type(entry["text"]) is str for entry in decimal_number_negative_vectors)
    decimal_number_negative_rounding_vectors = metadata["selectedDecimalNumberNegativeRounding"]
    assert len(decimal_number_negative_rounding_vectors) == 20
    assert all(len(entry["bits"]) == 4 and entry["pattern"] in range(5)
               and type(entry["text"]) is str
               for entry in decimal_number_negative_rounding_vectors)
    decimal_fixed_precision_100_vectors = metadata["selectedDecimalFixedPrecision100"]
    assert len(decimal_fixed_precision_100_vectors) == 6
    assert all(len(entry["bits"]) == 4 and entry["precision"] in (100, 101)
               and type(entry["text"]) is str
               for entry in decimal_fixed_precision_100_vectors)
    decimal_number_precision_100_vectors = metadata["selectedDecimalNumberPrecision100"]
    assert len(decimal_number_precision_100_vectors) == 6
    assert all(len(entry["bits"]) == 4 and entry["format"] == "N"
               and entry["precision"] in (100, 101) and type(entry["text"]) is str
               for entry in decimal_number_precision_100_vectors)
    decimal_percent_precision_100_vectors = metadata["selectedDecimalPercentPrecision100"]
    assert len(decimal_percent_precision_100_vectors) == 6
    assert all(len(entry["bits"]) == 4 and entry["format"] == "P"
               and entry["precision"] in (100, 101) and type(entry["text"]) is str
               for entry in decimal_percent_precision_100_vectors)
    decimal_currency_precision_100_vectors = metadata["selectedDecimalCurrencyPrecision100"]
    assert len(decimal_currency_precision_100_vectors) == 6
    assert all(len(entry["bits"]) == 4 and entry["format"] == "C"
               and entry["precision"] in (100, 101) and type(entry["text"]) is str
               for entry in decimal_currency_precision_100_vectors)
    decimal_exponential_precision_100_vectors = metadata["selectedDecimalExponentialPrecision100"]
    assert len(decimal_exponential_precision_100_vectors) == 6
    assert all(len(entry["bits"]) == 4 and entry["format"] == "E"
               and entry["precision"] in (100, 101) and type(entry["text"]) is str
               for entry in decimal_exponential_precision_100_vectors)
    decimal_precision_overflow_vectors = metadata["selectedDecimalPrecisionOverflowErrors"]
    assert len(decimal_precision_overflow_vectors) == 10
    assert {entry["format"] for entry in decimal_precision_overflow_vectors} == {
        "F", "N", "P", "C", "E"}
    assert all(entry["precision"] in ("2147483648", "999999999999999999999999999999")
               and entry["exception"] == "FormatException"
               for entry in decimal_precision_overflow_vectors)
    decimal_leading_zero_precision_vectors = metadata["selectedDecimalLeadingZeroPrecision"]
    assert len(decimal_leading_zero_precision_vectors) == 10
    assert {entry["format"] for entry in decimal_leading_zero_precision_vectors} == {
        "F", "N", "P", "C", "E"}
    assert all(len(entry["bits"]) == 4
               and entry["precision"] in ("000100", "00000000000000000000000000000100")
               and type(entry["text"]) is str and entry["exception"] is None
               for entry in decimal_leading_zero_precision_vectors)
    decimal_standard_precision_1024_vectors = metadata["selectedDecimalStandardPrecision1024"]
    assert len(decimal_standard_precision_1024_vectors) == 10
    assert {entry["format"] for entry in decimal_standard_precision_1024_vectors} == {
        "F", "N", "P", "C", "E"}
    assert all(len(entry["bits"]) == 4 and entry["precision"] == 1024
               and type(entry["text"]) is str
               for entry in decimal_standard_precision_1024_vectors)
    decimal_standard_precision_4097_vectors = metadata["selectedDecimalStandardPrecision4097"]
    assert len(decimal_standard_precision_4097_vectors) == 5
    assert {entry["format"] for entry in decimal_standard_precision_4097_vectors} == {
        "F", "N", "P", "C", "E"}
    assert all(len(entry["bits"]) == 4 and entry["precision"] == 4097
               and type(entry["text"]) is str
               for entry in decimal_standard_precision_4097_vectors)
    decimal_general_precision_vectors = metadata["selectedDecimalGeneralPrecision"]
    assert len(decimal_general_precision_vectors) == 84
    assert all(len(entry["bits"]) == 4 and entry["format"] in ("G", "g")
               and entry["precision"] in (-1, 0, 1, 2, 5, 10, 100)
               and type(entry["text"]) is str and entry["exception"] is None
               for entry in decimal_general_precision_vectors)
    decimal_general_rounding_vectors = metadata["selectedDecimalGeneralRoundingBoundaries"]
    assert len(decimal_general_rounding_vectors) == 42
    assert all(len(entry["bits"]) == 4 and entry["format"] in ("G", "g")
               and entry["precision"] in (1, 2, 3) and type(entry["text"]) is str
               for entry in decimal_general_rounding_vectors)
    decimal_roundtrip_format_vectors = metadata["selectedDecimalRoundtripFormat"]
    assert len(decimal_roundtrip_format_vectors) == 30
    assert all(len(entry["bits"]) == 4
               and entry["format"] in ("R", "r", "R0", "r0", "R1", "r1")
               and type(entry["text"]) is str and entry["exception"] is None
               for entry in decimal_roundtrip_format_vectors)
    decimal_general_extrema_vectors = metadata["selectedDecimalGeneralExtrema"]
    assert len(decimal_general_extrema_vectors) == 24
    assert all(len(entry["bits"]) == 4
               and entry["format"] in ("G0", "G1", "G10", "R0", "R1", "R10")
               and type(entry["text"]) is str for entry in decimal_general_extrema_vectors)
    decimal_general_signed_zero_vectors = metadata["selectedDecimalGeneralSignedZeroScale"]
    assert len(decimal_general_signed_zero_vectors) == 40
    assert all(len(entry["bits"]) == 4
               and entry["format"] in ("G", "g", "G0", "G1", "R", "r", "R0", "R1")
               and type(entry["text"]) is str
               for entry in decimal_general_signed_zero_vectors)
    general_format_invalid_vectors = metadata["selectedGeneralFormatInvalidBoundaries"]
    assert len(general_format_invalid_vectors) == 40
    assert all(entry["target"] in ("Int32", "Decimal")
               and len(entry["bits"]) == 4 and type(entry["intValue"]) is int
               and ((type(entry["text"]) is str and entry["exception"] is None)
                    or (entry["text"] is None and entry["exception"] == "FormatException"))
               for entry in general_format_invalid_vectors)
    letter_only_custom_vectors = metadata["selectedLetterOnlyCustomFormats"]
    assert len(letter_only_custom_vectors) == 32
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("abc", "xyz", "Qx", "hello", "GG", "RR", "ee", "FF")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               and entry["exception"] is None for entry in letter_only_custom_vectors)
    escaped_custom_literal_vectors = metadata["selectedEscapedCustomLiterals"]
    assert len(escaped_custom_literal_vectors) == 32
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("\\Q", "\\%", "\\0", "\\G",
                                       "'abc'", '"abc"', "'0%'", '"hello"')
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               and entry["exception"] is None for entry in escaped_custom_literal_vectors)
    quoted_numeric_custom_vectors = metadata["selectedQuotedNumericCustomFormats"]
    assert len(quoted_numeric_custom_vectors) == 18
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("'item '0", "0' units'", "'['0']'")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in quoted_numeric_custom_vectors)
    escaped_numeric_custom_vectors = metadata["selectedEscapedNumericCustomFormats"]
    assert len(escaped_numeric_custom_vectors) == 24
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("0\\Q", "0\\%", "0\\G", "\\Q0")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in escaped_numeric_custom_vectors)
    numeric_custom_sections_vectors = metadata["selectedNumericCustomSections"]
    assert len(numeric_custom_sections_vectors) == 18
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("0;(0);'zero'", "0;[0];'none'",
                                       "0;'minus '0;'zero'")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in numeric_custom_sections_vectors)
    decimal_place_custom_vectors = metadata["selectedDecimalPlaceCustomFormats"]
    assert len(decimal_place_custom_vectors) == 18
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("0.0", "0.00", "0.##")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in decimal_place_custom_vectors)
    optional_decimal_rounding_vectors = metadata[
        "selectedOptionalDecimalPlaceRoundingBoundaries"]
    assert len(optional_decimal_rounding_vectors) == 27
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("0.##", "0.00", "0.###")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in optional_decimal_rounding_vectors)
    extended_optional_decimal_vectors = metadata["selectedExtendedOptionalDecimalPlaces"]
    assert len(extended_optional_decimal_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("0.####", "0.#####")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in extended_optional_decimal_vectors)
    optional_decimal_precision_extremes = metadata[
        "selectedOptionalDecimalPrecisionExtremes"]
    assert len(optional_decimal_precision_extremes) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("0.######", "0.##########")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in optional_decimal_precision_extremes)
    optional_decimal_scale28_vectors = metadata["selectedOptionalDecimalScale28"]
    assert len(optional_decimal_scale28_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("0.############",
                                       "0.############################")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in optional_decimal_scale28_vectors)
    mandatory_decimal_place_vectors = metadata[
        "selectedMandatoryDecimalPlaceCustomFormats"]
    assert len(mandatory_decimal_place_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("0.000", "0.0000")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in mandatory_decimal_place_vectors)
    mandatory_decimal_precision_vectors = metadata[
        "selectedMandatoryDecimalPrecisionExtremes"]
    assert len(mandatory_decimal_precision_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and len(entry["format"]) in (30, 34)
               and entry["format"].startswith("0.")
               and set(entry["format"][2:]) == {"0"}
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in mandatory_decimal_precision_vectors)
    int32_mandatory_decimal_vectors = metadata["selectedInt32MandatoryDecimalPlaces"]
    assert len(int32_mandatory_decimal_vectors) == 12
    assert all(entry["target"] == "Int32"
               and len(entry["format"]) - 2 in (3, 4, 6, 28)
               and entry["format"].startswith("0.")
               and set(entry["format"][2:]) == {"0"}
               and type(entry["intValue"]) is int and type(entry["text"]) is str
               for entry in int32_mandatory_decimal_vectors)
    int32_optional_decimal_vectors = metadata["selectedInt32OptionalDecimalPlaces"]
    assert len(int32_optional_decimal_vectors) == 15
    assert all(entry["target"] == "Int32"
               and entry["format"] in ("0.#", "0.###", "0.##########")
               and type(entry["intValue"]) is int and type(entry["text"]) is str
               for entry in int32_optional_decimal_vectors)
    int32_zero_padding_vectors = metadata["selectedInt32CustomZeroPadding"]
    assert len(int32_zero_padding_vectors) == 15
    assert all(entry["target"] == "Int32"
               and entry["format"] in ("00", "000", "00000")
               and type(entry["intValue"]) is int and type(entry["text"]) is str
               for entry in int32_zero_padding_vectors)
    decimal_zero_padding_vectors = metadata["selectedDecimalCustomZeroPaddingSelected"]
    assert len(decimal_zero_padding_vectors) == 15
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("00", "000", "00000")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in decimal_zero_padding_vectors)
    optional_integer_vectors = metadata["selectedOptionalIntegerPlaceholders"]
    assert len(optional_integer_vectors) == 18
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#", "##", "###")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in optional_integer_vectors)
    mixed_integer_vectors = metadata["selectedMixedIntegerPlaceholders"]
    assert len(mixed_integer_vectors) == 24
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#0", "0#", "##0", "0##")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in mixed_integer_vectors)
    custom_integer_grouping_vectors = metadata["selectedCustomIntegerGrouping"]
    assert len(custom_integer_grouping_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0", "#,##0.00")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in custom_integer_grouping_vectors)
    grouping_negative_pattern_vectors = metadata[
        "selectedCustomGroupingNegativePatterns"]
    assert len(grouping_negative_pattern_vectors) == 20
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0", "#,##0.00")
               and entry["pattern"] in (0, 1, 2, 3, 4)
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouping_negative_pattern_vectors)
    custom_grouping_sizes_vectors = metadata["selectedCustomGroupingSizes"]
    assert len(custom_grouping_sizes_vectors) == 18
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0", "#,##0.00", "#,##0.000")
               and entry["groupSizes"] in ([2], [3, 2], [4])
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in custom_grouping_sizes_vectors)
    grouping_terminal_sizes_vectors = metadata["selectedCustomGroupingTerminalSizes"]
    assert len(grouping_terminal_sizes_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0", "#,##0.0000")
               and entry["groupSizes"] in ([3, 0], [2, 0], [3, 2, 0])
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouping_terminal_sizes_vectors)
    grouped_custom_precision_vectors = metadata["selectedGroupedCustomPrecision"]
    assert len(grouped_custom_precision_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0.00000", "#,##0.000000")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_custom_precision_vectors)
    grouped_custom_high_precision_vectors = metadata[
        "selectedGroupedCustomHighPrecision"]
    assert len(grouped_custom_high_precision_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0.0000000000",
                                       "#,##0.0000000000000000000000000000")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_custom_high_precision_vectors)
    grouped_optional_fraction_vectors = metadata["selectedGroupedOptionalFractions"]
    assert len(grouped_optional_fraction_vectors) == 18
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0.#", "#,##0.###",
                                       "#,##0.##########")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_optional_fraction_vectors)
    grouped_optional_rounding_vectors = metadata[
        "selectedGroupedOptionalRoundingBoundaries"]
    assert len(grouped_optional_rounding_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("#,##0.##",
                                       "#,##0.############################")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_optional_rounding_vectors)
    grouped_numeric_extrema_vectors = metadata["selectedGroupedNumericExtrema"]
    assert len(grouped_numeric_extrema_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0.0",
                                       "#,##0.############################")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_numeric_extrema_vectors)
    grouped_decimal_signed_zero_vectors = metadata["selectedGroupedDecimalSignedZero"]
    assert len(grouped_decimal_signed_zero_vectors) == 25
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("0", "#,##0", "#,##0.00",
                                       "#,##0.##",
                                       "#,##0.############################")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_decimal_signed_zero_vectors)
    grouped_mixed_fraction_vectors = metadata["selectedGroupedMixedFractions"]
    assert len(grouped_mixed_fraction_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0.0#", "#,##0.00##")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_mixed_fraction_vectors)
    grouped_mixed_rounding_vectors = metadata[
        "selectedGroupedMixedRoundingBoundaries"]
    assert len(grouped_mixed_rounding_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("#,##0.000###", "#,##0.0000####")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_mixed_rounding_vectors)
    grouped_mixed_scale_vectors = metadata["selectedGroupedMixedScaleLimits"]
    assert len(grouped_mixed_scale_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in (
                   "#,##0.0000000000##########",
                   "#,##0.00000000000000##############")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_mixed_scale_vectors)
    ungrouped_mixed_fraction_vectors = metadata["selectedUngroupedMixedFractions"]
    assert len(ungrouped_mixed_fraction_vectors) == 18
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("0.0#", "0.00##", "0.000###")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in ungrouped_mixed_fraction_vectors)
    ungrouped_mixed_rounding_vectors = metadata["selectedUngroupedMixedRounding"]
    assert len(ungrouped_mixed_rounding_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("0.#", "0.000###")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in ungrouped_mixed_rounding_vectors)
    custom_percent_scaling_vectors = metadata["selectedCustomPercentScaling"]
    assert len(custom_percent_scaling_vectors) == 18
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("0%", "0.0%", "0\\%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in custom_percent_scaling_vectors)
    custom_percent_symbol_vectors = metadata["selectedCustomPercentSymbolProvider"]
    assert len(custom_percent_symbol_vectors) == 18
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("0%", "0.0%", "0\\%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in custom_percent_symbol_vectors)
    custom_percent_precision_vectors = metadata["selectedCustomPercentPrecision"]
    assert len(custom_percent_precision_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("0.00%", "0.##%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in custom_percent_precision_vectors)
    custom_percent_rounding_vectors = metadata["selectedCustomPercentRounding"]
    assert len(custom_percent_rounding_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("0.##%",
                                       "0.############################%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in custom_percent_rounding_vectors)
    custom_percent_mixed_vectors = metadata["selectedCustomPercentMixedFractions"]
    assert len(custom_percent_mixed_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("0.0#%", "0.00##%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in custom_percent_mixed_vectors)
    custom_percent_mixed_rounding_vectors = metadata[
        "selectedCustomPercentMixedRounding"]
    assert len(custom_percent_mixed_rounding_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("0.000###%", "0.0000####%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in custom_percent_mixed_rounding_vectors)
    custom_percent_mixed_scale_vectors = metadata[
        "selectedCustomPercentMixedScaleLimits"]
    assert len(custom_percent_mixed_scale_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("0." + "0" * 20 + "#" * 20 + "%",
                                       "0." + "0" * 30 + "#" * 30 + "%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in custom_percent_mixed_scale_vectors)
    custom_grouped_percent_vectors = metadata["selectedCustomGroupedPercent"]
    assert len(custom_grouped_percent_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0%", "#,##0.00%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in custom_grouped_percent_vectors)
    grouped_percent_negative_vectors = metadata[
        "selectedGroupedPercentNegativePatterns"]
    assert len(grouped_percent_negative_vectors) == 20
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0%", "#,##0.00%")
               and entry["pattern"] in (0, 1, 2, 3, 4)
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_negative_vectors)
    grouped_percent_precision_vectors = metadata["selectedGroupedPercentPrecision"]
    assert len(grouped_percent_precision_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0.000%", "#,##0.###%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_precision_vectors)
    grouped_percent_rounding_vectors = metadata["selectedGroupedPercentRounding"]
    assert len(grouped_percent_rounding_vectors) == 14
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("#,##0.000%", "#,##0.###%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_rounding_vectors)
    grouped_percent_mixed_vectors = metadata["selectedGroupedPercentMixed"]
    assert len(grouped_percent_mixed_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0.0#%", "#,##0.00##%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_mixed_vectors)
    grouped_percent_mixed_rounding_vectors = metadata[
        "selectedGroupedPercentMixedRounding"]
    assert len(grouped_percent_mixed_rounding_vectors) == 14
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("#,##0.0#%", "#,##0.00##%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_mixed_rounding_vectors)
    grouped_percent_scale_vectors = metadata["selectedGroupedPercentScaleLimits"]
    assert len(grouped_percent_scale_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("#,##0." + "0" * 20 + "#" * 20 + "%",
                                       "#,##0." + "0" * 30 + "#" * 30 + "%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_scale_vectors)
    grouped_percent_group_sizes_vectors = metadata["selectedGroupedPercentGroupSizes"]
    assert len(grouped_percent_group_sizes_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] == "#,##0.00%"
               and entry["groupSizes"] in ([3, 2], [4])
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_group_sizes_vectors)
    grouped_percent_zero_groups_vectors = metadata[
        "selectedGroupedPercentZeroTerminatedGroups"]
    assert len(grouped_percent_zero_groups_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] == "#,##0.00%"
               and entry["groupSizes"] in ([3, 2, 0], [2, 0])
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_zero_groups_vectors)
    grouped_percent_multichar_vectors = metadata[
        "selectedGroupedPercentMultiCharSeparators"]
    assert len(grouped_percent_multichar_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0.00%", "#,##0.0#%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_multichar_vectors)
    grouped_percent_empty_symbol_vectors = metadata["selectedGroupedPercentEmptySymbol"]
    assert len(grouped_percent_empty_symbol_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0%", "#,##0.00%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_empty_symbol_vectors)
    grouped_percent_empty_separator_vectors = metadata[
        "selectedGroupedPercentEmptyGroupSeparator"]
    assert len(grouped_percent_empty_separator_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] == "#,##0.00%"
               and entry["groupSize"] in (2, 3)
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_empty_separator_vectors)
    grouped_percent_negative_sign_vectors = metadata[
        "selectedGroupedPercentMultiCharNegativeSign"]
    assert len(grouped_percent_negative_sign_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0%", "#,##0.00%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_negative_sign_vectors)
    grouped_percent_digit_width_vectors = metadata["selectedGroupedPercentDigitWidths"]
    assert len(grouped_percent_digit_width_vectors) == 18
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] == "#,##0.0#%"
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_digit_width_vectors)
    grouped_percent_int32_extreme_vectors = metadata["selectedGroupedPercentInt32Extremes"]
    assert len(grouped_percent_int32_extreme_vectors) == 18
    assert all(entry["target"] == "Int32"
               and entry["format"] in ("#,##0%", "#,##0.00%", "#,##0.0#%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_int32_extreme_vectors)
    grouped_percent_decimal_extreme_vectors = metadata[
        "selectedGroupedPercentDecimalExtremes"]
    assert len(grouped_percent_decimal_extreme_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("#,##0.00%", "#,##0.0#%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_decimal_extreme_vectors)
    grouped_percent_pattern_vectors = metadata["selectedGroupedPercentPatternInteraction"]
    assert len(grouped_percent_pattern_vectors) == 20
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("#,##0.0#%", "#,##0.00##%")
               and entry["pattern"] in (0, 1, 2, 3, 4)
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_pattern_vectors)
    grouped_percent_optional_zero_vectors = metadata["selectedGroupedPercentOptionalZero"]
    assert len(grouped_percent_optional_zero_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("#,##0.###%", "#,##0.0#%", "#,##0.00##%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_optional_zero_vectors)
    grouped_percent_high_precision_vectors = metadata[
        "selectedGroupedPercentHighPrecisionRounding"]
    assert len(grouped_percent_high_precision_vectors) == 18
    assert all(entry["target"] == "Decimal"
               and entry["format"] in ("#,##0." + "0" * 20 + "%",
                                       "#,##0." + "#" * 20 + "%")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_high_precision_vectors)
    grouped_percent_literal_vectors = metadata["selectedGroupedPercentLiteralAffixes"]
    assert len(grouped_percent_literal_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ('"pre"#,##0.00%', '#,##0.00%"post"')
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_literal_vectors)
    grouped_percent_paired_vectors = metadata["selectedGroupedPercentPairedAffixes"]
    assert len(grouped_percent_paired_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ('"pre"#,##0.00%"post"',
                                       '"L"#,##0.00%"R"')
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_paired_vectors)
    grouped_percent_escaped_vectors = metadata["selectedGroupedPercentEscapedAffixes"]
    assert len(grouped_percent_escaped_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("\\p#,##0.00%", "#,##0.00%\\s")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_escaped_vectors)
    grouped_percent_paired_escaped_vectors = metadata[
        "selectedGroupedPercentPairedEscapedAffixes"]
    assert len(grouped_percent_paired_escaped_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ("\\p#,##0.00%\\s", "\\L#,##0.00%\\R")
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_paired_escaped_vectors)
    grouped_percent_mixed_literal_vectors = metadata[
        "selectedGroupedPercentMixedLiteralStyles"]
    assert len(grouped_percent_mixed_literal_vectors) == 12
    assert all(entry["target"] in ("Int32", "Decimal")
               and entry["format"] in ('"pre"#,##0.00%\\s',
                                       '\\p#,##0.00%"post"')
               and len(entry["bits"]) == 4 and type(entry["text"]) is str
               for entry in grouped_percent_mixed_literal_vectors)
    get_format_provider_vectors = metadata["selectedDecimalGetFormatProvider"]
    assert len(get_format_provider_vectors) == 12
    assert all(len(entry["bits"]) == 4 and type(entry["text"]) is str
               and type(entry["general"]) is str and type(entry["number"]) is str
               for entry in get_format_provider_vectors)
    currency_positive_pattern_vectors = metadata["selectedDecimalCurrencyPositivePatterns"]
    assert len(currency_positive_pattern_vectors) == 12
    assert all(len(entry["bits"]) == 4 and entry["pattern"] in (0, 1, 2, 3)
               and type(entry["text"]) is str for entry in currency_positive_pattern_vectors)
    int32_currency_positive_pattern_vectors = metadata["selectedInt32CurrencyPositivePatterns"]
    assert len(int32_currency_positive_pattern_vectors) == 12
    assert all(type(entry["value"]) is int and entry["pattern"] in (0, 1, 2, 3)
               and type(entry["text"]) is str
               for entry in int32_currency_positive_pattern_vectors)
    int32_currency_negative_2to5_vectors = metadata[
        "selectedInt32CurrencyNegativePatterns2To5"]
    assert len(int32_currency_negative_2to5_vectors) == 12
    assert all(type(entry["value"]) is int and entry["pattern"] in (2, 3, 4, 5)
               and type(entry["text"]) is str
               for entry in int32_currency_negative_2to5_vectors)
    int32_currency_negative_6to9_vectors = metadata[
        "selectedInt32CurrencyNegativePatterns6To9"]
    assert len(int32_currency_negative_6to9_vectors) == 12
    assert all(type(entry["value"]) is int and entry["pattern"] in (6, 7, 8, 9)
               and type(entry["text"]) is str
               for entry in int32_currency_negative_6to9_vectors)
    int32_currency_negative_10to16_vectors = metadata[
        "selectedInt32CurrencyNegativePatterns10To16"]
    assert len(int32_currency_negative_10to16_vectors) == 21
    assert all(type(entry["value"]) is int and 10 <= entry["pattern"] <= 16
               and type(entry["text"]) is str
               for entry in int32_currency_negative_10to16_vectors)
    int32_percent_positive_pattern_vectors = metadata["selectedInt32PercentPositivePatterns"]
    assert len(int32_percent_positive_pattern_vectors) == 12
    assert all(type(entry["value"]) is int and entry["pattern"] in (0, 1, 2, 3)
               and type(entry["text"]) is str
               for entry in int32_percent_positive_pattern_vectors)
    int32_percent_negative_2to5_vectors = metadata["selectedInt32PercentNegativePatterns2To5"]
    assert len(int32_percent_negative_2to5_vectors) == 12
    assert all(type(entry["value"]) is int and entry["pattern"] in (2, 3, 4, 5)
               and type(entry["text"]) is str for entry in int32_percent_negative_2to5_vectors)
    int32_percent_negative_6to9_vectors = metadata["selectedInt32PercentNegativePatterns6To9"]
    assert len(int32_percent_negative_6to9_vectors) == 12
    assert all(type(entry["value"]) is int and entry["pattern"] in (6, 7, 8, 9)
               and type(entry["text"]) is str for entry in int32_percent_negative_6to9_vectors)
    int32_percent_negative_10to11_vectors = metadata["selectedInt32PercentNegativePatterns10To11"]
    assert len(int32_percent_negative_10to11_vectors) == 12
    assert all(type(entry["value"]) is int and entry["pattern"] in (10, 11)
               and type(entry["text"]) is str for entry in int32_percent_negative_10to11_vectors)
    int32_number_negative_vectors = metadata["selectedInt32NumberNegativePatterns"]
    assert len(int32_number_negative_vectors) == 15
    assert all(type(entry["value"]) is int and entry["pattern"] in range(5)
               and type(entry["text"]) is str for entry in int32_number_negative_vectors)
    int32_number_high_precision_vectors = metadata["selectedInt32NumberHighPrecision"]
    assert len(int32_number_high_precision_vectors) == 6
    assert all(entry["value"] == -42 and entry["pattern"] in (0, 1, 4)
               and entry["precision"] in (1001, 1024) and type(entry["text"]) is str
               for entry in int32_number_high_precision_vectors)
    int32_decimal_high_precision_vectors = metadata["selectedInt32DecimalHighPrecision"]
    assert len(int32_decimal_high_precision_vectors) == 6
    assert all(entry["value"] in (-42, 0, 42)
               and entry["precision"] in (1001, 1024) and type(entry["text"]) is str
               for entry in int32_decimal_high_precision_vectors)
    int32_hex_high_precision_vectors = metadata["selectedInt32HexHighPrecision"]
    assert len(int32_hex_high_precision_vectors) == 12
    assert all(entry["value"] in (-42, 0, 42) and entry["format"] in ("x", "X")
               and entry["precision"] in (1001, 1024) and type(entry["text"]) is str
               for entry in int32_hex_high_precision_vectors)
    int32_binary_high_precision_vectors = metadata["selectedInt32BinaryHighPrecision"]
    assert len(int32_binary_high_precision_vectors) == 6
    assert all(entry["value"] in (-42, 0, 42) and entry["format"] == "B"
               and entry["precision"] in (1001, 1024) and type(entry["text"]) is str
               for entry in int32_binary_high_precision_vectors)
    int32_fixed_high_precision_vectors = metadata["selectedInt32FixedHighPrecision"]
    assert len(int32_fixed_high_precision_vectors) == 6
    assert all(entry["value"] in (-42, 0, 42)
               and entry["precision"] in (1001, 1024) and type(entry["text"]) is str
               for entry in int32_fixed_high_precision_vectors)
    int32_currency_high_precision_vectors = metadata["selectedInt32CurrencyHighPrecision"]
    assert len(int32_currency_high_precision_vectors) == 6
    assert all(entry["value"] in (-42, 0, 42)
               and entry["precision"] in (1001, 1024) and type(entry["text"]) is str
               for entry in int32_currency_high_precision_vectors)
    int32_percent_high_precision_vectors = metadata["selectedInt32PercentHighPrecision"]
    assert len(int32_percent_high_precision_vectors) == 6
    assert all(entry["value"] in (-42, 0, 42)
               and entry["precision"] in (1001, 1024) and type(entry["text"]) is str
               for entry in int32_percent_high_precision_vectors)
    int32_exponential_high_precision_vectors = metadata["selectedInt32ExponentialHighPrecision"]
    assert len(int32_exponential_high_precision_vectors) == 6
    assert all(entry["value"] in (-42, 0, 42)
               and entry["precision"] in (1001, 1024) and type(entry["text"]) is str
               for entry in int32_exponential_high_precision_vectors)
    int32_standard_precision_2049_vectors = metadata["selectedInt32StandardPrecision2049"]
    assert len(int32_standard_precision_2049_vectors) == 8
    assert {entry["format"] for entry in int32_standard_precision_2049_vectors} == {
        "D", "N", "x", "B", "C", "F", "P", "E"}
    assert all(entry["value"] == -42 and entry["precision"] == 2049
               and type(entry["text"]) is str
               for entry in int32_standard_precision_2049_vectors)
    int32_leading_zero_precision_vectors = metadata["selectedInt32LeadingZeroPrecision"]
    assert len(int32_leading_zero_precision_vectors) == 16
    assert {entry["format"] for entry in int32_leading_zero_precision_vectors} == {
        "D", "N", "x", "B", "C", "F", "P", "E"}
    assert all(entry["value"] == -42
               and entry["precision"] in ("000100", "00000000000000000000000000000100")
               and type(entry["text"]) is str and entry["exception"] is None
               for entry in int32_leading_zero_precision_vectors)
    int32_general_precision_vectors = metadata["selectedInt32GeneralPrecision"]
    assert len(int32_general_precision_vectors) == 108
    assert all(entry["format"] in ("G", "g")
               and entry["precision"] in (0, 1, 2, 5, 10, 100)
               and type(entry["text"]) is str
               for entry in int32_general_precision_vectors)
    int32_general_extrema_vectors = metadata["selectedInt32GeneralExtrema"]
    assert len(int32_general_extrema_vectors) == 48
    assert all(entry["format"] in ("G", "g")
               and entry["precision"] in (1, 2, 8, 9)
               and type(entry["text"]) is str
               for entry in int32_general_extrema_vectors)
    int32_roundtrip_format_vectors = metadata["selectedInt32RoundtripFormatBoundary"]
    assert len(int32_roundtrip_format_vectors) == 10
    assert all(entry["format"] in ("R", "r") and type(entry["text"]) is str
               and entry["exception"] is None for entry in int32_roundtrip_format_vectors)
    int32_roundtrip_precision_vectors = metadata["selectedInt32RoundtripPrecisionBoundary"]
    assert len(int32_roundtrip_precision_vectors) == 16
    assert all(entry["format"] in ("R0", "R1", "R2", "R10", "r0", "r1", "r2", "r10")
               and type(entry["text"]) is str and entry["exception"] is None
               for entry in int32_roundtrip_precision_vectors)
    number_negative_boundaries = metadata["selectedNumberNegativePatternBoundaries"]
    assert number_negative_boundaries["initial"] == 1
    assert number_negative_boundaries["accepted"] == list(range(5))
    assert [entry["value"] for entry in number_negative_boundaries["failures"]] == [
        -1, 5, -2147483648, 2147483647]
    assert all(entry["exception"] == "ArgumentOutOfRangeException"
               and entry["retained"] == 4
               for entry in number_negative_boundaries["failures"])
    format_string_vectors = metadata["selectedDecimalFormatStrings"]
    assert len(format_string_vectors) == 20
    assert all(len(entry["bits"]) == 4 and type(entry["general"]) is str
               and type(entry["fixed2"]) is str for entry in format_string_vectors)
    assert format_string_vectors[12]["fixed2"] == "1.01"
    assert format_string_vectors[14]["fixed2"] == "-1.01"
    fixed_precision_vectors = metadata["selectedDecimalFixedPrecision"]
    assert len(fixed_precision_vectors) == 20
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in fixed_precision_vectors)
    assert fixed_precision_vectors[4]["text"] == "2"
    assert fixed_precision_vectors[14]["text"] == "0.0000000000000000000000000001"
    number_format_vectors = metadata["selectedDecimalNumberFormatting"]
    assert len(number_format_vectors) == 20
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in number_format_vectors)
    assert number_format_vectors[5]["text"] == "1,000"
    assert number_format_vectors[16]["text"] == "79,228,162,514,264,337,593,543,950,335"
    percent_format_vectors = metadata["selectedDecimalPercentFormatting"]
    assert len(percent_format_vectors) == 20
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in percent_format_vectors)
    assert percent_format_vectors[0]["text"] == "0.00 %"
    assert percent_format_vectors[14]["text"] == "100,000 %"
    exponential_format_vectors = metadata["selectedDecimalExponentialFormatting"]
    assert len(exponential_format_vectors) == 20
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in exponential_format_vectors)
    assert exponential_format_vectors[10]["text"] == "1.00E+001"
    assert exponential_format_vectors[12]["text"] == "1.00E-028"
    currency_format_vectors = metadata["selectedDecimalCurrencyFormatting"]
    assert len(currency_format_vectors) == 20
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in currency_format_vectors)
    assert currency_format_vectors[0]["text"] == "¤0.00"
    assert currency_format_vectors[3]["text"] == "(¤1.00)"
    custom_zero_vectors = metadata["selectedDecimalCustomZeroFormatting"]
    assert len(custom_zero_vectors) == 20
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in custom_zero_vectors)
    assert custom_zero_vectors[3]["text"] == "-0001.00"
    assert custom_zero_vectors[12]["text"] == "003"
    custom_optional_vectors = metadata["selectedDecimalCustomOptionalFormatting"]
    assert len(custom_optional_vectors) == 20
    assert all(len(entry["bits"]) == 4 and type(entry["format"]) is str
               and type(entry["text"]) is str for entry in custom_optional_vectors)
    assert custom_optional_vectors[0]["text"] == "0"
    assert custom_optional_vectors[14]["text"] == "1.2"
    magnitude_vectors = metadata["selectedDecimalMagnitudeExtrema"]
    assert len(magnitude_vectors) == 22
    assert all(len(entry["left"]) == len(entry["right"])
               == len(entry["maximum"]) == len(entry["minimum"]) == 4
               for entry in magnitude_vectors)
    assert magnitude_vectors[0]["maximum"] == [0, 0, 0, 0]
    assert magnitude_vectors[0]["minimum"] == [0, 0, 0, -2147352576]
    assert magnitude_vectors[3]["maximum"] == [1, 0, 0, 0]
    assert magnitude_vectors[3]["minimum"] == [1, 0, 0, -2147483648]
    assert magnitude_vectors[20]["maximum"] == [100, 0, 0, -2147352576]
    assert magnitude_vectors[20]["minimum"] == [1, 0, 0, -2147483648]
    canonical_vectors = metadata["selectedDecimalIsCanonical"]
    assert len(canonical_vectors) == 20
    assert all(len(entry["bits"]) == 4 and type(entry["canonical"]) is bool
               for entry in canonical_vectors)
    assert [entry["canonical"] for entry in canonical_vectors[:8]] == [
        True, True, False, False, True, True, False, False]
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
    float_style_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in float_style_vectors]
    float_style_result = run("java", "-cp", classpath,
                             "consumer.ProductDecimalFloatStyleParseConsumer",
                             *float_style_args).strip()
    number_style_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in number_style_vectors]
    number_style_result = run("java", "-cp", classpath,
                              "consumer.ProductDecimalNumberStyleParseConsumer",
                              *number_style_args).strip()
    integer_style_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in integer_style_vectors]
    integer_style_result = run("java", "-cp", classpath,
                               "consumer.ProductDecimalIntegerStyleParseConsumer",
                               *integer_style_args).strip()
    currency_style_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in currency_style_vectors]
    currency_style_result = run("java", "-cp", classpath,
                                "consumer.ProductDecimalCurrencyStyleParseConsumer",
                                *currency_style_args).strip()
    any_style_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in any_style_vectors]
    any_style_result = run("java", "-cp", classpath,
                           "consumer.ProductDecimalAnyStyleParseConsumer",
                           *any_style_args).strip()
    custom_provider_args = [
        ":".join((
            entry["style"], entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in custom_provider_vectors]
    custom_provider_result = run("java", "-cp", classpath,
                                 "consumer.ProductDecimalCustomProviderParseConsumer",
                                 *custom_provider_args).strip()
    custom_currency_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in custom_currency_vectors]
    custom_currency_result = run("java", "-cp", classpath,
                                 "consumer.ProductDecimalCustomCurrencyProviderParseConsumer",
                                 *custom_currency_args).strip()
    any_custom_provider_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in any_custom_provider_vectors]
    any_custom_provider_result = run("java", "-cp", classpath,
                                     "consumer.ProductDecimalAnyCustomProviderParseConsumer",
                                     *any_custom_provider_args).strip()
    none_style_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in none_style_vectors]
    none_style_result = run("java", "-cp", classpath,
                            "consumer.ProductDecimalNoneStyleParseConsumer",
                            *none_style_args).strip()
    thousands_style_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in thousands_style_vectors]
    thousands_style_result = run("java", "-cp", classpath,
                                 "consumer.ProductDecimalThousandsStyleParseConsumer",
                                 *thousands_style_args).strip()
    point_style_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in point_style_vectors]
    point_style_result = run("java", "-cp", classpath,
                             "consumer.ProductDecimalPointStyleParseConsumer",
                             *point_style_args).strip()
    exponent_style_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in exponent_style_vectors]
    exponent_style_result = run("java", "-cp", classpath,
                                "consumer.ProductDecimalExponentStyleParseConsumer",
                                *exponent_style_args).strip()
    leading_sign_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in leading_sign_vectors]
    leading_sign_result = run("java", "-cp", classpath,
                              "consumer.ProductDecimalLeadingSignStyleParseConsumer",
                              *leading_sign_args).strip()
    trailing_sign_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in trailing_sign_vectors]
    trailing_sign_result = run("java", "-cp", classpath,
                               "consumer.ProductDecimalTrailingSignStyleParseConsumer",
                               *trailing_sign_args).strip()
    parentheses_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in parentheses_vectors]
    parentheses_result = run("java", "-cp", classpath,
                             "consumer.ProductDecimalParenthesesStyleParseConsumer",
                             *parentheses_args).strip()
    leading_white_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in leading_white_vectors]
    leading_white_result = run("java", "-cp", classpath,
                               "consumer.ProductDecimalLeadingWhiteStyleParseConsumer",
                               *leading_white_args).strip()
    trailing_white_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in trailing_white_vectors]
    trailing_white_result = run("java", "-cp", classpath,
                                "consumer.ProductDecimalTrailingWhiteStyleParseConsumer",
                                *trailing_white_args).strip()
    currency_symbol_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in currency_symbol_vectors]
    currency_symbol_result = run("java", "-cp", classpath,
                                 "consumer.ProductDecimalCurrencySymbolStyleParseConsumer",
                                 *currency_symbol_args).strip()
    composed_style_args = [
        ":".join((
            str(entry["style"]), entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in composed_style_vectors]
    composed_style_result = run("java", "-cp", classpath,
                                "consumer.ProductDecimalComposedStyleParseConsumer",
                                *composed_style_args).strip()
    custom_symbol_args = [
        ":".join((
            entry["text"],
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in custom_symbol_vectors]
    custom_symbol_result = run("java", "-cp", classpath,
                               "consumer.ProductDecimalCustomCurrencySymbolParseConsumer",
                               *custom_symbol_args).strip()
    decimal_try_args = [
        ":".join((
            entry["mode"], entry["text"] if entry["text"] is not None else "<NULL>",
            str(entry["success"]).lower(),
            ",".join(str(word) for word in entry["bits"]),
        )) for entry in decimal_try_vectors]
    decimal_try_result = run("java", "-cp", classpath,
                             "consumer.ProductDecimalTryParseConsumer",
                             *decimal_try_args).strip()
    provider_try_args = [
        ":".join((
            entry["text"] if entry["text"] is not None else "<NULL>",
            str(entry["success"]).lower(),
            ",".join(str(word) for word in entry["bits"]),
        )) for entry in provider_try_vectors]
    provider_try_result = run("java", "-cp", classpath,
                              "consumer.ProductDecimalProviderTryParseConsumer",
                              *provider_try_args).strip()
    span_try_args = [
        ":".join((
            entry["mode"], entry["text"], str(entry["success"]).lower(),
            ",".join(str(word) for word in entry["bits"]),
        )) for entry in span_try_vectors]
    span_try_result = run("java", "-cp", classpath,
                          "consumer.ProductDecimalSpanTryParseConsumer",
                          *span_try_args).strip()
    utf8_span_args = [
        ":".join((
            entry["mode"], entry["text"], str(entry["success"]).lower(),
            ",".join(str(word) for word in entry["bits"]),
            entry["error"] or "",
        )) for entry in utf8_span_vectors]
    utf8_span_result = run("java", "-cp", classpath,
                           "consumer.ProductDecimalUtf8SpanParseConsumer",
                           *utf8_span_args).strip()
    span_provider_args = [
        ":".join((
            entry["carrier"], entry["text"], str(entry["success"]).lower(),
            ",".join(str(word) for word in entry["bits"]),
        )) for entry in span_provider_vectors]
    span_provider_result = run("java", "-cp", classpath,
                               "consumer.ProductDecimalSpanProviderTryParseConsumer",
                               *span_provider_args).strip()
    parse_provider_args = [
        ":".join((
            entry["carrier"],
            entry["text"] if entry["text"] is not None else "<NULL>",
            ",".join(str(word) for word in entry["bits"] or []),
            entry["error"] or "",
        )) for entry in parse_provider_vectors]
    parse_provider_result = run("java", "-cp", classpath,
                                "consumer.ProductDecimalParseProviderConsumer",
                                *parse_provider_args).strip()
    multiply_args = [
        ":".join((
            ",".join(str(word) for word in entry["left"]),
            ",".join(str(word) for word in entry["right"]),
            "OVERFLOW" if entry["result"] is None else
            ",".join(str(word) for word in entry["result"]),
        )) for entry in multiply_vectors]
    multiply_result = run("java", "-cp", classpath,
                          "consumer.ProductDecimalMultiplyConsumer", *multiply_args).strip()
    divide_args = [
        ":".join((
            ",".join(str(word) for word in entry["left"]),
            ",".join(str(word) for word in entry["right"]),
            ("DIVIDE_ZERO" if entry["error"] == "System.DivideByZeroException"
             else "OVERFLOW") if entry["result"] is None else
            ",".join(str(word) for word in entry["result"]),
        )) for entry in divide_vectors]
    divide_result = run("java", "-cp", classpath,
                        "consumer.ProductDecimalDivideConsumer", *divide_args).strip()
    remainder_args = [
        ":".join((
            ",".join(str(word) for word in entry["left"]),
            ",".join(str(word) for word in entry["right"]),
            "DIVIDE_ZERO" if entry["result"] is None else
            ",".join(str(word) for word in entry["result"]),
        )) for entry in remainder_vectors]
    remainder_result = run("java", "-cp", classpath,
                           "consumer.ProductDecimalRemainderConsumer", *remainder_args).strip()
    compare_args = [
        ":".join((
            ",".join(str(word) for word in entry["left"]),
            ",".join(str(word) for word in entry["right"]),
            str(entry["result"]),
        )) for entry in compare_vectors]
    compare_result = run("java", "-cp", classpath,
                         "consumer.ProductDecimalCompareConsumer", *compare_args).strip()
    equals_args = [
        ":".join((
            ",".join(str(word) for word in entry["left"]),
            ",".join(str(word) for word in entry["right"]),
            str(entry["result"]).lower(),
        )) for entry in equals_vectors]
    equals_result = run("java", "-cp", classpath,
                        "consumer.ProductDecimalEqualsConsumer", *equals_args).strip()
    hash_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["result"]),
        )) for entry in hash_vectors]
    hash_result = run("java", "-cp", classpath,
                      "consumer.ProductDecimalHashConsumer", *hash_args).strip()
    instance_equals_args = [
        ":".join((
            ",".join(str(word) for word in entry["left"]),
            ",".join(str(word) for word in entry["right"]),
            *(str(entry[field]).lower() for field in (
                "typedResult", "objectResult", "unrelatedResult", "nullResult", "hashMatches")),
        )) for entry in instance_equals_vectors]
    instance_equals_result = run("java", "-cp", classpath,
                                 "consumer.ProductDecimalInstanceEqualityConsumer",
                                 *instance_equals_args).strip()
    compare_to_args = [
        ":".join((
            ",".join(str(word) for word in entry["left"]),
            ",".join(str(word) for word in entry["right"]),
            str(entry["typedResult"]), str(entry["objectResult"]),
            str(entry["nullResult"]), entry["wrongTypeError"],
        )) for entry in compare_to_vectors]
    compare_to_result = run("java", "-cp", classpath,
                            "consumer.ProductDecimalCompareToConsumer", *compare_to_args).strip()
    to_int32_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            "OVERFLOW" if entry["result"] is None else str(entry["result"]),
        )) for entry in to_int32_vectors]
    to_int32_result = run("java", "-cp", classpath,
                          "consumer.ProductDecimalToInt32Consumer", *to_int32_args).strip()
    sign_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["negative"]).lower(), str(entry["positive"]).lower(),
        )) for entry in sign_vectors]
    sign_result = run("java", "-cp", classpath,
                      "consumer.ProductDecimalSignConsumer", *sign_args).strip()
    integer_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["integer"]).lower(), str(entry["even"]).lower(),
            str(entry["odd"]).lower(),
        )) for entry in integer_vectors]
    integer_result = run("java", "-cp", classpath,
                         "consumer.ProductDecimalIntegerPredicateConsumer", *integer_args).strip()
    to_int64_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            "OVERFLOW" if entry["result"] is None else str(entry["result"]),
        )) for entry in to_int64_vectors]
    to_int64_result = run("java", "-cp", classpath,
                          "consumer.ProductDecimalToInt64Consumer", *to_int64_args).strip()
    to_uint32_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            "OVERFLOW" if entry["result"] is None else str(entry["result"]),
        )) for entry in to_uint32_vectors]
    to_uint32_result = run("java", "-cp", classpath,
                           "consumer.ProductDecimalToUInt32Consumer", *to_uint32_args).strip()
    to_uint64_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            "OVERFLOW" if entry["result"] is None else str(entry["result"]),
        )) for entry in to_uint64_vectors]
    to_uint64_result = run("java", "-cp", classpath,
                           "consumer.ProductDecimalToUInt64Consumer", *to_uint64_args).strip()
    small_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            *("OVERFLOW" if entry[field]["result"] is None
              else str(entry[field]["result"]) for field in small_fields),
        )) for entry in small_vectors]
    small_result = run("java", "-cp", classpath,
                       "consumer.ProductDecimalSmallIntegerConsumer", *small_args).strip()
    floating_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["doubleBits"]), str(entry["singleBits"]),
        )) for entry in floating_vectors]
    floating_result = run("java", "-cp", classpath,
                          "consumer.ProductDecimalFloatingConsumer", *floating_args).strip()
    copy_sign_args = [
        ":".join((
            ",".join(str(word) for word in entry["value"]),
            ",".join(str(word) for word in entry["sign"]),
            ",".join(str(word) for word in entry["result"]),
        )) for entry in copy_sign_vectors]
    copy_sign_result = run("java", "-cp", classpath,
                           "consumer.ProductDecimalCopySignConsumer", *copy_sign_args).strip()
    max_min_args = [
        ":".join((
            ",".join(str(word) for word in entry["left"]),
            ",".join(str(word) for word in entry["right"]),
            ",".join(str(word) for word in entry["maximum"]),
            ",".join(str(word) for word in entry["minimum"]),
        )) for entry in max_min_vectors]
    max_min_result = run("java", "-cp", classpath,
                         "consumer.ProductDecimalMaxMinConsumer", *max_min_args).strip()
    clamp_args = [
        ":".join((
            ",".join(str(word) for word in entry["value"]),
            ",".join(str(word) for word in entry["lower"]),
            ",".join(str(word) for word in entry["upper"]),
            ",".join(str(word) for word in entry["result"] or []),
            entry["exception"] or "none",
        )) for entry in clamp_vectors]
    clamp_result = run("java", "-cp", classpath,
                       "consumer.ProductDecimalClampConsumer", *clamp_args).strip()
    oa_currency_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["result"]) if entry["result"] is not None else "",
            entry["exception"] or "none",
        )) for entry in oa_currency_vectors]
    oa_currency_result = run("java", "-cp", classpath,
                             "consumer.ProductDecimalOACurrencyConsumer",
                             *oa_currency_args).strip()
    from_oa_currency_args = [
        ":".join((
            str(entry["value"]),
            ",".join(str(word) for word in entry["bits"]),
        )) for entry in from_oa_currency_vectors]
    from_oa_currency_result = run("java", "-cp", classpath,
                                  "consumer.ProductDecimalFromOACurrencyConsumer",
                                  *from_oa_currency_args).strip()
    formatting_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["invariant"],
        )) for entry in formatting_vectors]
    formatting_result = run("java", "-cp", classpath,
                            "consumer.ProductDecimalFormattingConsumer",
                            *formatting_args).strip()
    provider_formatting_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["text"], entry["general"],
        )) for entry in provider_formatting_vectors]
    provider_formatting_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalProviderFormattingConsumer",
        *provider_formatting_args).strip()
    fixed_provider_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in fixed_provider_vectors]
    fixed_provider_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalFixedProviderFormattingConsumer",
        *fixed_provider_args).strip()
    number_provider_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in number_provider_vectors]
    number_provider_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalNumberProviderFormattingConsumer",
        *number_provider_args).strip()
    percent_provider_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in percent_provider_vectors]
    percent_provider_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalPercentProviderFormattingConsumer",
        *percent_provider_args).strip()
    currency_provider_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in currency_provider_vectors]
    currency_provider_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalCurrencyProviderFormattingConsumer",
        *currency_provider_args).strip()
    exponential_provider_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in exponential_provider_vectors]
    exponential_provider_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalExponentialProviderFormattingConsumer",
        *exponential_provider_args).strip()
    custom_format_provider_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in custom_format_provider_vectors]
    custom_format_provider_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalCustomProviderFormattingConsumer",
        *custom_format_provider_args).strip()
    number_group_size_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], str(entry["mode"]), entry["text"],
        )) for entry in number_group_size_vectors]
    number_group_size_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalNumberGroupSizesConsumer",
        *number_group_size_args).strip()
    currency_group_size_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], str(entry["mode"]), entry["text"],
        )) for entry in currency_group_size_vectors]
    currency_group_size_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalCurrencyGroupSizesConsumer",
        *currency_group_size_args).strip()
    percent_group_size_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], str(entry["mode"]), entry["text"],
        )) for entry in percent_group_size_vectors]
    percent_group_size_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalPercentGroupSizesConsumer",
        *percent_group_size_args).strip()
    currency_negative_pattern_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["pattern"]), entry["text"],
        )) for entry in currency_negative_pattern_vectors]
    currency_negative_pattern_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalCurrencyNegativePatternsConsumer",
        *currency_negative_pattern_args).strip()
    currency_negative_pattern_4to7_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["pattern"]), entry["text"],
        )) for entry in currency_negative_pattern_4to7_vectors]
    currency_negative_pattern_4to7_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalCurrencyNegativePatternsConsumer",
        *currency_negative_pattern_4to7_args).strip()
    currency_negative_pattern_8to11_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["pattern"]), entry["text"],
        )) for entry in currency_negative_pattern_8to11_vectors]
    currency_negative_pattern_8to11_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalCurrencyNegativePatternsConsumer",
        *currency_negative_pattern_8to11_args).strip()
    currency_negative_pattern_12to16_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["pattern"]), entry["text"],
        )) for entry in currency_negative_pattern_12to16_vectors]
    currency_negative_pattern_12to16_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalCurrencyNegativePatternsConsumer",
        *currency_negative_pattern_12to16_args).strip()
    percent_positive_pattern_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["pattern"]), entry["text"],
        )) for entry in percent_positive_pattern_vectors]
    percent_positive_pattern_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalPercentPositivePatternsConsumer",
        *percent_positive_pattern_args).strip()
    percent_negative_pattern_0to3_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["pattern"]), entry["text"],
        )) for entry in percent_negative_pattern_0to3_vectors]
    percent_negative_pattern_0to3_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalPercentNegativePatternsConsumer",
        *percent_negative_pattern_0to3_args).strip()
    percent_negative_pattern_4to7_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["pattern"]), entry["text"],
        )) for entry in percent_negative_pattern_4to7_vectors]
    percent_negative_pattern_4to7_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalPercentNegativePatternsConsumer",
        *percent_negative_pattern_4to7_args).strip()
    percent_negative_pattern_8to11_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["pattern"]), entry["text"],
        )) for entry in percent_negative_pattern_8to11_vectors]
    percent_negative_pattern_8to11_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalPercentNegativePatternsConsumer",
        *percent_negative_pattern_8to11_args).strip()
    decimal_number_negative_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["pattern"]), entry["text"],
        )) for entry in decimal_number_negative_vectors]
    decimal_number_negative_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalNumberNegativePatternsConsumer",
        *decimal_number_negative_args).strip()
    decimal_number_negative_rounding_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["pattern"]), entry["text"],
        )) for entry in decimal_number_negative_rounding_vectors]
    decimal_number_negative_rounding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalNumberNegativeRoundingConsumer",
        *decimal_number_negative_rounding_args).strip()
    decimal_fixed_precision_100_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["precision"]), entry["text"],
        )) for entry in decimal_fixed_precision_100_vectors]
    decimal_fixed_precision_100_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalFixedPrecision100Consumer",
        *decimal_fixed_precision_100_args).strip()
    decimal_number_precision_100_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], str(entry["precision"]), entry["text"],
        )) for entry in decimal_number_precision_100_vectors]
    decimal_number_precision_100_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalStandardPrecision100Consumer",
        *decimal_number_precision_100_args).strip()
    decimal_percent_precision_100_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], str(entry["precision"]), entry["text"],
        )) for entry in decimal_percent_precision_100_vectors]
    decimal_percent_precision_100_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalStandardPrecision100Consumer",
        *decimal_percent_precision_100_args).strip()
    decimal_currency_precision_100_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], str(entry["precision"]), entry["text"],
        )) for entry in decimal_currency_precision_100_vectors]
    decimal_currency_precision_100_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalStandardPrecision100Consumer",
        *decimal_currency_precision_100_args).strip()
    decimal_exponential_precision_100_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], str(entry["precision"]), entry["text"],
        )) for entry in decimal_exponential_precision_100_vectors]
    decimal_exponential_precision_100_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalStandardPrecision100Consumer",
        *decimal_exponential_precision_100_args).strip()
    decimal_precision_overflow_args = [
        ":".join((entry["format"], entry["precision"], entry["exception"]))
        for entry in decimal_precision_overflow_vectors]
    decimal_precision_overflow_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalPrecisionOverflowConsumer",
        *decimal_precision_overflow_args).strip()
    decimal_leading_zero_precision_args = [
        ":".join((",".join(str(word) for word in entry["bits"]), entry["format"],
                  entry["precision"], entry["text"]))
        for entry in decimal_leading_zero_precision_vectors]
    decimal_leading_zero_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalStandardPrecision100Consumer",
        *decimal_leading_zero_precision_args).strip()
    decimal_standard_precision_1024_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], str(entry["precision"]), entry["text"],
        )) for entry in decimal_standard_precision_1024_vectors]
    decimal_standard_precision_1024_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalStandardPrecision100Consumer",
        *decimal_standard_precision_1024_args).strip()
    decimal_standard_precision_4097_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], str(entry["precision"]), entry["text"],
        )) for entry in decimal_standard_precision_4097_vectors]
    decimal_standard_precision_4097_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalStandardPrecision100Consumer",
        *decimal_standard_precision_4097_args).strip()
    decimal_general_precision_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], str(entry["precision"]), entry["text"],
        )) for entry in decimal_general_precision_vectors]
    decimal_general_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalGeneralPrecisionConsumer",
        *decimal_general_precision_args).strip()
    decimal_general_rounding_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], str(entry["precision"]), entry["text"],
        )) for entry in decimal_general_rounding_vectors]
    decimal_general_rounding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalGeneralPrecisionConsumer",
        *decimal_general_rounding_args).strip()
    decimal_roundtrip_format_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in decimal_roundtrip_format_vectors]
    decimal_roundtrip_format_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalRoundtripFormatConsumer",
        *decimal_roundtrip_format_args).strip()
    decimal_general_extrema_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in decimal_general_extrema_vectors]
    decimal_general_extrema_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalRoundtripFormatConsumer",
        *decimal_general_extrema_args).strip()
    decimal_general_signed_zero_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in decimal_general_signed_zero_vectors]
    decimal_general_signed_zero_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalRoundtripFormatConsumer",
        *decimal_general_signed_zero_args).strip()
    general_format_invalid_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"] or "", entry["exception"] or "none"))
        for entry in general_format_invalid_vectors]
    general_format_invalid_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *general_format_invalid_args).strip()
    letter_only_custom_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none"))
        for entry in letter_only_custom_vectors]
    letter_only_custom_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *letter_only_custom_args).strip()
    escaped_custom_literal_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none"))
        for entry in escaped_custom_literal_vectors]
    escaped_custom_literal_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *escaped_custom_literal_args).strip()
    quoted_numeric_custom_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none"))
        for entry in quoted_numeric_custom_vectors]
    quoted_numeric_custom_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *quoted_numeric_custom_args).strip()
    escaped_numeric_custom_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none"))
        for entry in escaped_numeric_custom_vectors]
    escaped_numeric_custom_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *escaped_numeric_custom_args).strip()
    numeric_custom_sections_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none"))
        for entry in numeric_custom_sections_vectors]
    numeric_custom_sections_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *numeric_custom_sections_args).strip()
    decimal_place_custom_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in decimal_place_custom_vectors]
    decimal_place_custom_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *decimal_place_custom_args).strip()
    optional_decimal_rounding_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in optional_decimal_rounding_vectors]
    optional_decimal_rounding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *optional_decimal_rounding_args).strip()
    extended_optional_decimal_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in extended_optional_decimal_vectors]
    extended_optional_decimal_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *extended_optional_decimal_args).strip()
    optional_decimal_precision_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in optional_decimal_precision_extremes]
    optional_decimal_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *optional_decimal_precision_args).strip()
    optional_decimal_scale28_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in optional_decimal_scale28_vectors]
    optional_decimal_scale28_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *optional_decimal_scale28_args).strip()
    mandatory_decimal_place_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in mandatory_decimal_place_vectors]
    mandatory_decimal_place_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *mandatory_decimal_place_args).strip()
    mandatory_decimal_precision_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in mandatory_decimal_precision_vectors]
    mandatory_decimal_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *mandatory_decimal_precision_args).strip()
    int32_mandatory_decimal_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in int32_mandatory_decimal_vectors]
    int32_mandatory_decimal_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *int32_mandatory_decimal_args).strip()
    int32_optional_decimal_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in int32_optional_decimal_vectors]
    int32_optional_decimal_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *int32_optional_decimal_args).strip()
    int32_zero_padding_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none"))
        for entry in int32_zero_padding_vectors]
    int32_zero_padding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *int32_zero_padding_args).strip()
    decimal_zero_padding_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none"))
        for entry in decimal_zero_padding_vectors]
    decimal_zero_padding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *decimal_zero_padding_args).strip()
    optional_integer_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none"))
        for entry in optional_integer_vectors]
    optional_integer_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *optional_integer_args).strip()
    mixed_integer_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none"))
        for entry in mixed_integer_vectors]
    mixed_integer_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *mixed_integer_args).strip()
    custom_integer_grouping_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_"))
        for entry in custom_integer_grouping_vectors]
    custom_integer_grouping_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *custom_integer_grouping_args).strip()
    grouping_negative_pattern_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", str(entry["pattern"])))
        for entry in grouping_negative_pattern_vectors]
    grouping_negative_pattern_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouping_negative_pattern_args).strip()
    custom_grouping_sizes_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1",
                  ",".join(str(size) for size in entry["groupSizes"])))
        for entry in custom_grouping_sizes_vectors]
    custom_grouping_sizes_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *custom_grouping_sizes_args).strip()
    grouping_terminal_sizes_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1",
                  ",".join(str(size) for size in entry["groupSizes"])))
        for entry in grouping_terminal_sizes_vectors]
    grouping_terminal_sizes_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouping_terminal_sizes_args).strip()
    grouped_custom_precision_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_"))
        for entry in grouped_custom_precision_vectors]
    grouped_custom_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_custom_precision_args).strip()
    grouped_custom_high_precision_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_"))
        for entry in grouped_custom_high_precision_vectors]
    grouped_custom_high_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_custom_high_precision_args).strip()
    grouped_optional_fraction_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_"))
        for entry in grouped_optional_fraction_vectors]
    grouped_optional_fraction_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_optional_fraction_args).strip()
    grouped_optional_rounding_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_"))
        for entry in grouped_optional_rounding_vectors]
    grouped_optional_rounding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_optional_rounding_args).strip()
    grouped_numeric_extrema_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_"))
        for entry in grouped_numeric_extrema_vectors]
    grouped_numeric_extrema_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_numeric_extrema_args).strip()
    grouped_decimal_signed_zero_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_"))
        for entry in grouped_decimal_signed_zero_vectors]
    grouped_decimal_signed_zero_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_decimal_signed_zero_args).strip()
    grouped_mixed_fraction_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_"))
        for entry in grouped_mixed_fraction_vectors]
    grouped_mixed_fraction_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_mixed_fraction_args).strip()
    grouped_mixed_rounding_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_"))
        for entry in grouped_mixed_rounding_vectors]
    grouped_mixed_rounding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_mixed_rounding_args).strip()
    grouped_mixed_scale_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_"))
        for entry in grouped_mixed_scale_vectors]
    grouped_mixed_scale_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_mixed_scale_args).strip()
    ungrouped_mixed_fraction_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in ungrouped_mixed_fraction_vectors]
    ungrouped_mixed_fraction_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *ungrouped_mixed_fraction_args).strip()
    ungrouped_mixed_rounding_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in ungrouped_mixed_rounding_vectors]
    ungrouped_mixed_rounding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *ungrouped_mixed_rounding_args).strip()
    custom_percent_scaling_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@"))
        for entry in custom_percent_scaling_vectors]
    custom_percent_scaling_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *custom_percent_scaling_args).strip()
    custom_percent_symbol_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "3", "pct"))
        for entry in custom_percent_symbol_vectors]
    custom_percent_symbol_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *custom_percent_symbol_args).strip()
    custom_percent_precision_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "3", "pct"))
        for entry in custom_percent_precision_vectors]
    custom_percent_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *custom_percent_precision_args).strip()
    custom_percent_rounding_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "3", "pct"))
        for entry in custom_percent_rounding_vectors]
    custom_percent_rounding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *custom_percent_rounding_args).strip()
    custom_percent_mixed_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "3", "pct"))
        for entry in custom_percent_mixed_vectors]
    custom_percent_mixed_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *custom_percent_mixed_args).strip()
    custom_percent_mixed_rounding_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "3", "pct"))
        for entry in custom_percent_mixed_rounding_vectors]
    custom_percent_mixed_rounding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *custom_percent_mixed_rounding_args).strip()
    custom_percent_mixed_scale_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "3", "pct"))
        for entry in custom_percent_mixed_scale_vectors]
    custom_percent_mixed_scale_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *custom_percent_mixed_scale_args).strip()
    custom_grouped_percent_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in custom_grouped_percent_vectors]
    custom_grouped_percent_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *custom_grouped_percent_args).strip()
    grouped_percent_negative_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", str(entry["pattern"]),
                  "2", "pct", str(entry["pattern"])))
        for entry in grouped_percent_negative_vectors]
    grouped_percent_negative_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_negative_args).strip()
    grouped_percent_precision_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_precision_vectors]
    grouped_percent_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_precision_args).strip()
    grouped_percent_rounding_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_rounding_vectors]
    grouped_percent_rounding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_rounding_args).strip()
    grouped_percent_mixed_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_mixed_vectors]
    grouped_percent_mixed_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_mixed_args).strip()
    grouped_percent_mixed_rounding_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_mixed_rounding_vectors]
    grouped_percent_mixed_rounding_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_mixed_rounding_args).strip()
    grouped_percent_scale_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_scale_vectors]
    grouped_percent_scale_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_scale_args).strip()
    grouped_percent_group_sizes_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1",
                  ",".join(str(size) for size in entry["groupSizes"]), "pct"))
        for entry in grouped_percent_group_sizes_vectors]
    grouped_percent_group_sizes_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_group_sizes_args).strip()
    grouped_percent_zero_groups_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1",
                  ",".join(str(size) for size in entry["groupSizes"]), "pct"))
        for entry in grouped_percent_zero_groups_vectors]
    grouped_percent_zero_groups_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_zero_groups_args).strip()
    grouped_percent_multichar_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@@", "__", "1", "2", "pct"))
        for entry in grouped_percent_multichar_vectors]
    grouped_percent_multichar_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_multichar_args).strip()
    grouped_percent_empty_symbol_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", ""))
        for entry in grouped_percent_empty_symbol_vectors]
    grouped_percent_empty_symbol_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_empty_symbol_args).strip()
    grouped_percent_empty_separator_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "", "1",
                  str(entry["groupSize"]), "pct"))
        for entry in grouped_percent_empty_separator_vectors]
    grouped_percent_empty_separator_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_empty_separator_args).strip()
    grouped_percent_negative_sign_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct", "0", "NEG"))
        for entry in grouped_percent_negative_sign_vectors]
    grouped_percent_negative_sign_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_negative_sign_args).strip()
    grouped_percent_digit_width_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_digit_width_vectors]
    grouped_percent_digit_width_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_digit_width_args).strip()
    grouped_percent_int32_extreme_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_int32_extreme_vectors]
    grouped_percent_int32_extreme_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_int32_extreme_args).strip()
    grouped_percent_decimal_extreme_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_decimal_extreme_vectors]
    grouped_percent_decimal_extreme_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_decimal_extreme_args).strip()
    grouped_percent_pattern_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", str(entry["pattern"]),
                  "2", "pct", str(entry["pattern"])))
        for entry in grouped_percent_pattern_vectors]
    grouped_percent_pattern_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_pattern_args).strip()
    grouped_percent_optional_zero_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_optional_zero_vectors]
    grouped_percent_optional_zero_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_optional_zero_args).strip()
    grouped_percent_high_precision_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_high_precision_vectors]
    grouped_percent_high_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_high_precision_args).strip()
    grouped_percent_literal_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_literal_vectors]
    grouped_percent_literal_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_literal_args).strip()
    grouped_percent_paired_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_paired_vectors]
    grouped_percent_paired_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_paired_args).strip()
    grouped_percent_escaped_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_escaped_vectors]
    grouped_percent_escaped_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_escaped_args).strip()
    grouped_percent_paired_escaped_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_paired_escaped_vectors]
    grouped_percent_paired_escaped_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_paired_escaped_args).strip()
    grouped_percent_mixed_literal_args = [
        ":".join((entry["target"], entry["format"], str(entry["intValue"]),
                  ",".join(str(word) for word in entry["bits"]),
                  entry["text"], "none", "@", "_", "1", "2", "pct"))
        for entry in grouped_percent_mixed_literal_vectors]
    grouped_percent_mixed_literal_result = run(
        "java", "-cp", classpath,
        "consumer.ProductGeneralFormatInvalidBoundariesConsumer",
        *grouped_percent_mixed_literal_args).strip()
    get_format_provider_args = [
        ":".join((
            entry["text"], ",".join(str(word) for word in entry["bits"]),
            entry["general"], entry["number"],
        )) for entry in get_format_provider_vectors]
    get_format_provider_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalGetFormatProviderConsumer",
        *get_format_provider_args).strip()
    currency_positive_pattern_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["pattern"]), entry["text"],
        )) for entry in currency_positive_pattern_vectors]
    currency_positive_pattern_result = run(
        "java", "-cp", classpath,
        "consumer.ProductDecimalCurrencyPositivePatternsConsumer",
        *currency_positive_pattern_args).strip()
    int32_currency_positive_pattern_args = [
        ":".join((str(entry["value"]), str(entry["pattern"]), entry["text"]))
        for entry in int32_currency_positive_pattern_vectors]
    int32_currency_positive_pattern_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32CurrencyPositivePatternsConsumer",
        *int32_currency_positive_pattern_args).strip()
    int32_currency_negative_2to5_args = [
        ":".join((str(entry["value"]), str(entry["pattern"]), entry["text"]))
        for entry in int32_currency_negative_2to5_vectors]
    int32_currency_negative_2to5_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32CurrencyNegativePatternsConsumer",
        *int32_currency_negative_2to5_args).strip()
    int32_currency_negative_6to9_args = [
        ":".join((str(entry["value"]), str(entry["pattern"]), entry["text"]))
        for entry in int32_currency_negative_6to9_vectors]
    int32_currency_negative_6to9_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32CurrencyNegativePatternsConsumer",
        *int32_currency_negative_6to9_args).strip()
    int32_currency_negative_10to16_args = [
        ":".join((str(entry["value"]), str(entry["pattern"]), entry["text"]))
        for entry in int32_currency_negative_10to16_vectors]
    int32_currency_negative_10to16_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32CurrencyNegativePatternsConsumer",
        *int32_currency_negative_10to16_args).strip()
    int32_percent_positive_pattern_args = [
        ":".join((str(entry["value"]), str(entry["pattern"]), entry["text"]))
        for entry in int32_percent_positive_pattern_vectors]
    int32_percent_positive_pattern_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32PercentPositivePatternsConsumer",
        *int32_percent_positive_pattern_args).strip()
    int32_percent_negative_2to5_args = [
        ":".join((str(entry["value"]), str(entry["pattern"]), entry["text"]))
        for entry in int32_percent_negative_2to5_vectors]
    int32_percent_negative_2to5_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32PercentNegativePatternsConsumer",
        *int32_percent_negative_2to5_args).strip()
    int32_percent_negative_6to9_args = [
        ":".join((str(entry["value"]), str(entry["pattern"]), entry["text"]))
        for entry in int32_percent_negative_6to9_vectors]
    int32_percent_negative_6to9_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32PercentNegativePatternsConsumer",
        *int32_percent_negative_6to9_args).strip()
    int32_percent_negative_10to11_args = [
        ":".join((str(entry["value"]), str(entry["pattern"]), entry["text"]))
        for entry in int32_percent_negative_10to11_vectors]
    int32_percent_negative_10to11_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32PercentNegativePatternsConsumer",
        *int32_percent_negative_10to11_args).strip()
    int32_number_negative_args = [
        ":".join((str(entry["value"]), str(entry["pattern"]), entry["text"]))
        for entry in int32_number_negative_vectors]
    int32_number_negative_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32NumberNegativePatternsConsumer",
        *int32_number_negative_args).strip()
    int32_number_high_precision_args = [
        ":".join((str(entry["value"]), str(entry["pattern"]),
                  str(entry["precision"]), entry["text"]))
        for entry in int32_number_high_precision_vectors]
    int32_number_high_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32NumberHighPrecisionConsumer",
        *int32_number_high_precision_args).strip()
    int32_decimal_high_precision_args = [
        ":".join((str(entry["value"]), str(entry["precision"]), entry["text"]))
        for entry in int32_decimal_high_precision_vectors]
    int32_decimal_high_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32DecimalHighPrecisionConsumer",
        *int32_decimal_high_precision_args).strip()
    int32_hex_high_precision_args = [
        ":".join((str(entry["value"]), entry["format"],
                  str(entry["precision"]), entry["text"]))
        for entry in int32_hex_high_precision_vectors]
    int32_hex_high_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32RadixHighPrecisionConsumer",
        *int32_hex_high_precision_args).strip()
    int32_binary_high_precision_args = [
        ":".join((str(entry["value"]), entry["format"],
                  str(entry["precision"]), entry["text"]))
        for entry in int32_binary_high_precision_vectors]
    int32_binary_high_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32RadixHighPrecisionConsumer",
        *int32_binary_high_precision_args).strip()
    int32_fixed_high_precision_args = [
        ":".join((str(entry["value"]), str(entry["precision"]), entry["text"]))
        for entry in int32_fixed_high_precision_vectors]
    int32_fixed_high_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32FixedHighPrecisionConsumer",
        *int32_fixed_high_precision_args).strip()
    int32_currency_high_precision_args = [
        ":".join((str(entry["value"]), str(entry["precision"]), entry["text"]))
        for entry in int32_currency_high_precision_vectors]
    int32_currency_high_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32CurrencyHighPrecisionConsumer",
        *int32_currency_high_precision_args).strip()
    int32_percent_high_precision_args = [
        ":".join((str(entry["value"]), str(entry["precision"]), entry["text"]))
        for entry in int32_percent_high_precision_vectors]
    int32_percent_high_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32PercentHighPrecisionConsumer",
        *int32_percent_high_precision_args).strip()
    int32_exponential_high_precision_args = [
        ":".join((str(entry["value"]), str(entry["precision"]), entry["text"]))
        for entry in int32_exponential_high_precision_vectors]
    int32_exponential_high_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32ExponentialHighPrecisionConsumer",
        *int32_exponential_high_precision_args).strip()
    int32_standard_precision_2049_args = [
        ":".join((str(entry["value"]), entry["format"],
                  str(entry["precision"]), entry["text"]))
        for entry in int32_standard_precision_2049_vectors]
    int32_standard_precision_2049_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32StandardPrecision2049Consumer",
        *int32_standard_precision_2049_args).strip()
    int32_leading_zero_precision_args = [
        ":".join((str(entry["value"]), entry["format"],
                  entry["precision"], entry["text"]))
        for entry in int32_leading_zero_precision_vectors]
    int32_leading_zero_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32StandardPrecision2049Consumer",
        *int32_leading_zero_precision_args).strip()
    int32_general_precision_args = [
        ":".join((str(entry["value"]), entry["format"],
                  str(entry["precision"]), entry["text"]))
        for entry in int32_general_precision_vectors]
    int32_general_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32GeneralPrecisionConsumer",
        *int32_general_precision_args).strip()
    int32_general_extrema_args = [
        ":".join((str(entry["value"]), entry["format"],
                  str(entry["precision"]), entry["text"]))
        for entry in int32_general_extrema_vectors]
    int32_general_extrema_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32GeneralPrecisionConsumer",
        *int32_general_extrema_args).strip()
    int32_roundtrip_format_args = [
        ":".join((str(entry["value"]), entry["format"], entry["text"]))
        for entry in int32_roundtrip_format_vectors]
    int32_roundtrip_format_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32RoundtripFormatConsumer",
        *int32_roundtrip_format_args).strip()
    int32_roundtrip_precision_args = [
        ":".join((str(entry["value"]), entry["format"], entry["text"]))
        for entry in int32_roundtrip_precision_vectors]
    int32_roundtrip_precision_result = run(
        "java", "-cp", classpath,
        "consumer.ProductInt32RoundtripFormatConsumer",
        *int32_roundtrip_precision_args).strip()
    number_negative_boundaries_args = [
        str(number_negative_boundaries["initial"]),
        ",".join(str(value) for value in number_negative_boundaries["accepted"]),
        *[":".join((str(entry["value"]), entry["exception"],
                    str(entry["retained"])))
          for entry in number_negative_boundaries["failures"]],
    ]
    number_negative_boundaries_result = run(
        "java", "-cp", classpath,
        "consumer.ProductNumberNegativePatternBoundariesConsumer",
        *number_negative_boundaries_args).strip()
    format_string_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["general"], entry["fixed2"],
        )) for entry in format_string_vectors]
    format_string_result = run("java", "-cp", classpath,
                               "consumer.ProductDecimalFormatStringsConsumer",
                               *format_string_args).strip()
    fixed_precision_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in fixed_precision_vectors]
    fixed_precision_result = run("java", "-cp", classpath,
                                 "consumer.ProductDecimalFixedPrecisionConsumer",
                                 *fixed_precision_args).strip()
    number_format_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in number_format_vectors]
    number_format_result = run("java", "-cp", classpath,
                               "consumer.ProductDecimalNumberFormattingConsumer",
                               *number_format_args).strip()
    percent_format_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in percent_format_vectors]
    percent_format_result = run("java", "-cp", classpath,
                                "consumer.ProductDecimalPercentFormattingConsumer",
                                *percent_format_args).strip()
    exponential_format_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in exponential_format_vectors]
    exponential_format_result = run("java", "-cp", classpath,
                                    "consumer.ProductDecimalExponentialFormattingConsumer",
                                    *exponential_format_args).strip()
    currency_format_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in currency_format_vectors]
    currency_format_result = run("java", "-cp", classpath,
                                 "consumer.ProductDecimalCurrencyFormattingConsumer",
                                 *currency_format_args).strip()
    custom_zero_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in custom_zero_vectors]
    custom_zero_result = run("java", "-cp", classpath,
                             "consumer.ProductDecimalCustomZeroFormattingConsumer",
                             *custom_zero_args).strip()
    custom_optional_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            entry["format"], entry["text"],
        )) for entry in custom_optional_vectors]
    custom_optional_result = run("java", "-cp", classpath,
                                 "consumer.ProductDecimalCustomOptionalFormattingConsumer",
                                 *custom_optional_args).strip()
    magnitude_args = [
        ":".join((
            ",".join(str(word) for word in entry["left"]),
            ",".join(str(word) for word in entry["right"]),
            ",".join(str(word) for word in entry["maximum"]),
            ",".join(str(word) for word in entry["minimum"]),
        )) for entry in magnitude_vectors]
    magnitude_result = run("java", "-cp", classpath,
                           "consumer.ProductDecimalMagnitudeConsumer", *magnitude_args).strip()
    canonical_args = [
        ":".join((
            ",".join(str(word) for word in entry["bits"]),
            str(entry["canonical"]).lower(),
        )) for entry in canonical_vectors]
    canonical_result = run("java", "-cp", classpath,
                           "consumer.ProductDecimalCanonicalConsumer", *canonical_args).strip()
    assert disposal_result.startswith("PASS: product IDisposable shape")
    assert type_result == "PASS external System.Type selected identity consumer"
    assert exception_result == "PASS external selected Exception constructors and inner identity"
    assert int32_result == "PASS external selected Int32 bit helpers"
    assert arithmetic_result == "PASS external selected Int32 signed arithmetic"
    assert span_result == "PASS external selected Int32 span parsing and formatting"
    assert decimal_result == "PASS external selected Decimal bits"
    assert float_style_result == "PASS external selected Decimal Float-style parsing"
    assert number_style_result == "PASS external selected Decimal Number-style parsing"
    assert integer_style_result == "PASS external selected Decimal Integer-style parsing"
    assert currency_style_result == "PASS external selected Decimal Currency-style parsing"
    assert any_style_result == "PASS external selected Decimal Any-style parsing"
    assert custom_provider_result == "PASS external selected Decimal custom-provider parsing"
    assert custom_currency_result == "PASS external selected Decimal custom-currency-provider parsing"
    assert any_custom_provider_result == "PASS external selected Decimal Any-custom-provider parsing"
    assert none_style_result == "PASS external selected Decimal None-style parsing"
    assert thousands_style_result == "PASS external selected Decimal Thousands-style parsing"
    assert point_style_result == "PASS external selected Decimal Point-style parsing"
    assert exponent_style_result == "PASS external selected Decimal Exponent-style parsing"
    assert leading_sign_result == "PASS external selected Decimal LeadingSign-style parsing"
    assert trailing_sign_result == "PASS external selected Decimal TrailingSign-style parsing"
    assert parentheses_result == "PASS external selected Decimal Parentheses-style parsing"
    assert leading_white_result == "PASS external selected Decimal LeadingWhite-style parsing"
    assert trailing_white_result == "PASS external selected Decimal TrailingWhite-style parsing"
    assert currency_symbol_result == "PASS external selected Decimal CurrencySymbol-style parsing"
    assert composed_style_result == "PASS external selected Decimal composed-style parsing"
    assert custom_symbol_result == "PASS external selected Decimal CustomCurrencySymbol parsing"
    assert decimal_try_result == "PASS external selected Decimal TryParse results"
    assert provider_try_result == "PASS external selected Decimal provider TryParse results"
    assert span_try_result == "PASS external selected Decimal span TryParse results"
    assert utf8_span_result == "PASS external selected Decimal UTF-8 span parsing"
    assert span_provider_result == "PASS external selected Decimal span provider TryParse"
    assert parse_provider_result == "PASS external selected Decimal Parse provider overloads"
    assert multiply_result == "PASS external selected Decimal multiplication"
    assert divide_result == "PASS external selected Decimal division"
    assert remainder_result == "PASS external selected Decimal remainder"
    assert compare_result == "PASS external selected Decimal comparison"
    assert equals_result == "PASS external selected Decimal equality"
    assert hash_result == "PASS external selected Decimal hash codes"
    assert instance_equals_result == "PASS external selected Decimal instance equality"
    assert compare_to_result == "PASS external selected Decimal instance comparison"
    assert to_int32_result == "PASS external selected Decimal ToInt32"
    assert sign_result == "PASS external selected Decimal sign predicates"
    assert integer_result == "PASS external selected Decimal integer predicates"
    assert to_int64_result == "PASS external selected Decimal ToInt64"
    assert to_uint32_result == "PASS external selected Decimal ToUInt32"
    assert to_uint64_result == "PASS external selected Decimal ToUInt64"
    assert small_result == "PASS external selected Decimal small-integer conversions"
    assert floating_result == "PASS external selected Decimal floating conversions"
    assert copy_sign_result == "PASS external selected Decimal CopySign"
    assert max_min_result == "PASS external selected Decimal Max and Min"
    assert magnitude_result == "PASS external selected Decimal magnitude extrema"
    assert clamp_result == "PASS external selected Decimal Clamp"
    assert oa_currency_result == "PASS external selected Decimal ToOACurrency"
    assert from_oa_currency_result == "PASS external selected Decimal FromOACurrency"
    assert formatting_result == "PASS external selected Decimal invariant formatting"
    assert provider_formatting_result == "PASS external selected Decimal provider formatting"
    assert fixed_provider_result == "PASS external selected Decimal fixed provider formatting"
    assert number_provider_result == "PASS external selected Decimal number provider formatting"
    assert percent_provider_result == "PASS external selected Decimal percent provider formatting"
    assert currency_provider_result == "PASS external selected Decimal currency provider formatting"
    assert exponential_provider_result == "PASS external selected Decimal exponential provider formatting"
    assert custom_format_provider_result == "PASS external selected Decimal custom provider formatting"
    assert number_group_size_result == "PASS external selected Decimal number group sizes"
    assert currency_group_size_result == "PASS external selected Decimal currency group sizes"
    assert percent_group_size_result == "PASS external selected Decimal percent group sizes"
    assert currency_negative_pattern_result == "PASS external selected Decimal currency negative patterns"
    assert currency_negative_pattern_4to7_result == "PASS external selected Decimal currency negative patterns"
    assert currency_negative_pattern_8to11_result == "PASS external selected Decimal currency negative patterns"
    assert currency_negative_pattern_12to16_result == "PASS external selected Decimal currency negative patterns"
    assert percent_positive_pattern_result == "PASS external selected Decimal percent positive patterns"
    assert percent_negative_pattern_0to3_result == "PASS external selected Decimal percent negative patterns"
    assert percent_negative_pattern_4to7_result == "PASS external selected Decimal percent negative patterns"
    assert percent_negative_pattern_8to11_result == "PASS external selected Decimal percent negative patterns"
    assert decimal_number_negative_result == "PASS external selected Decimal number negative patterns"
    assert decimal_number_negative_rounding_result == "PASS external Decimal number negative rounding"
    assert decimal_fixed_precision_100_result == "PASS external Decimal fixed precision 100"
    assert decimal_number_precision_100_result == "PASS external Decimal standard precision 100"
    assert decimal_percent_precision_100_result == "PASS external Decimal standard precision 100"
    assert decimal_currency_precision_100_result == "PASS external Decimal standard precision 100"
    assert decimal_exponential_precision_100_result == "PASS external Decimal standard precision 100"
    assert decimal_precision_overflow_result == "PASS external Decimal precision overflow errors"
    assert decimal_leading_zero_precision_result == "PASS external Decimal standard precision 100"
    assert decimal_standard_precision_1024_result == "PASS external Decimal standard precision 100"
    assert decimal_standard_precision_4097_result == "PASS external Decimal standard precision 100"
    assert decimal_general_precision_result == "PASS external Decimal general precision"
    assert decimal_general_rounding_result == "PASS external Decimal general precision"
    assert decimal_roundtrip_format_result == "PASS external Decimal roundtrip format"
    assert decimal_general_extrema_result == "PASS external Decimal roundtrip format"
    assert decimal_general_signed_zero_result == "PASS external Decimal roundtrip format"
    assert general_format_invalid_result == "PASS external general format boundaries"
    assert letter_only_custom_result == "PASS external general format boundaries"
    assert escaped_custom_literal_result == "PASS external general format boundaries"
    assert quoted_numeric_custom_result == "PASS external general format boundaries"
    assert escaped_numeric_custom_result == "PASS external general format boundaries"
    assert numeric_custom_sections_result == "PASS external general format boundaries"
    assert decimal_place_custom_result == "PASS external general format boundaries"
    assert optional_decimal_rounding_result == "PASS external general format boundaries"
    assert extended_optional_decimal_result == "PASS external general format boundaries"
    assert optional_decimal_precision_result == "PASS external general format boundaries"
    assert optional_decimal_scale28_result == "PASS external general format boundaries"
    assert mandatory_decimal_place_result == "PASS external general format boundaries"
    assert mandatory_decimal_precision_result == "PASS external general format boundaries"
    assert int32_mandatory_decimal_result == "PASS external general format boundaries"
    assert int32_optional_decimal_result == "PASS external general format boundaries"
    assert int32_zero_padding_result == "PASS external general format boundaries"
    assert decimal_zero_padding_result == "PASS external general format boundaries"
    assert optional_integer_result == "PASS external general format boundaries"
    assert mixed_integer_result == "PASS external general format boundaries"
    assert custom_integer_grouping_result == "PASS external general format boundaries"
    assert grouping_negative_pattern_result == "PASS external general format boundaries"
    assert custom_grouping_sizes_result == "PASS external general format boundaries"
    assert grouping_terminal_sizes_result == "PASS external general format boundaries"
    assert grouped_custom_precision_result == "PASS external general format boundaries"
    assert grouped_custom_high_precision_result == "PASS external general format boundaries"
    assert grouped_optional_fraction_result == "PASS external general format boundaries"
    assert grouped_optional_rounding_result == "PASS external general format boundaries"
    assert grouped_numeric_extrema_result == "PASS external general format boundaries"
    assert grouped_decimal_signed_zero_result == "PASS external general format boundaries"
    assert grouped_mixed_fraction_result == "PASS external general format boundaries"
    assert grouped_mixed_rounding_result == "PASS external general format boundaries"
    assert grouped_mixed_scale_result == "PASS external general format boundaries"
    assert ungrouped_mixed_fraction_result == "PASS external general format boundaries"
    assert ungrouped_mixed_rounding_result == "PASS external general format boundaries"
    assert custom_percent_scaling_result == "PASS external general format boundaries"
    assert custom_percent_symbol_result == "PASS external general format boundaries"
    assert custom_percent_precision_result == "PASS external general format boundaries"
    assert custom_percent_rounding_result == "PASS external general format boundaries"
    assert custom_percent_mixed_result == "PASS external general format boundaries"
    assert custom_percent_mixed_rounding_result == "PASS external general format boundaries"
    assert custom_percent_mixed_scale_result == "PASS external general format boundaries"
    assert custom_grouped_percent_result == "PASS external general format boundaries"
    assert grouped_percent_negative_result == "PASS external general format boundaries"
    assert grouped_percent_precision_result == "PASS external general format boundaries"
    assert grouped_percent_rounding_result == "PASS external general format boundaries"
    assert grouped_percent_mixed_result == "PASS external general format boundaries"
    assert grouped_percent_mixed_rounding_result == "PASS external general format boundaries"
    assert grouped_percent_scale_result == "PASS external general format boundaries"
    assert grouped_percent_group_sizes_result == "PASS external general format boundaries"
    assert grouped_percent_zero_groups_result == "PASS external general format boundaries"
    assert grouped_percent_multichar_result == "PASS external general format boundaries"
    assert grouped_percent_empty_symbol_result == "PASS external general format boundaries"
    assert grouped_percent_empty_separator_result == "PASS external general format boundaries"
    assert grouped_percent_negative_sign_result == "PASS external general format boundaries"
    assert grouped_percent_digit_width_result == "PASS external general format boundaries"
    assert grouped_percent_int32_extreme_result == "PASS external general format boundaries"
    assert grouped_percent_decimal_extreme_result == "PASS external general format boundaries"
    assert grouped_percent_pattern_result == "PASS external general format boundaries"
    assert grouped_percent_optional_zero_result == "PASS external general format boundaries"
    assert grouped_percent_high_precision_result == "PASS external general format boundaries"
    assert grouped_percent_literal_result == "PASS external general format boundaries"
    assert grouped_percent_paired_result == "PASS external general format boundaries"
    assert grouped_percent_escaped_result == "PASS external general format boundaries"
    assert grouped_percent_paired_escaped_result == "PASS external general format boundaries"
    assert grouped_percent_mixed_literal_result == "PASS external general format boundaries"
    assert get_format_provider_result == "PASS external selected Decimal GetFormat provider"
    assert currency_positive_pattern_result == "PASS external selected Decimal currency positive patterns"
    assert int32_currency_positive_pattern_result == "PASS external selected Int32 currency positive patterns"
    assert int32_currency_negative_2to5_result == "PASS external selected Int32 currency negative patterns"
    assert int32_currency_negative_6to9_result == "PASS external selected Int32 currency negative patterns"
    assert int32_currency_negative_10to16_result == "PASS external selected Int32 currency negative patterns"
    assert int32_percent_positive_pattern_result == "PASS external selected Int32 percent positive patterns"
    assert int32_percent_negative_2to5_result == "PASS external selected Int32 percent negative patterns"
    assert int32_percent_negative_6to9_result == "PASS external selected Int32 percent negative patterns"
    assert int32_percent_negative_10to11_result == "PASS external selected Int32 percent negative patterns"
    assert int32_number_negative_result == "PASS external selected Int32 number negative patterns"
    assert int32_number_high_precision_result == "PASS external Int32 number high precision"
    assert int32_decimal_high_precision_result == "PASS external Int32 decimal high precision"
    assert int32_hex_high_precision_result == "PASS external Int32 radix high precision"
    assert int32_binary_high_precision_result == "PASS external Int32 radix high precision"
    assert int32_fixed_high_precision_result == "PASS external Int32 fixed high precision"
    assert int32_currency_high_precision_result == "PASS external Int32 currency high precision"
    assert int32_percent_high_precision_result == "PASS external Int32 percent high precision"
    assert int32_exponential_high_precision_result == "PASS external Int32 exponential high precision"
    assert int32_standard_precision_2049_result == "PASS external Int32 standard precision 2049"
    assert int32_leading_zero_precision_result == "PASS external Int32 standard precision 2049"
    assert int32_general_precision_result == "PASS external Int32 general precision"
    assert int32_general_extrema_result == "PASS external Int32 general precision"
    assert int32_roundtrip_format_result == "PASS external Int32 roundtrip format"
    assert int32_roundtrip_precision_result == "PASS external Int32 roundtrip format"
    assert number_negative_boundaries_result == "PASS external NumberNegativePattern boundaries"
    assert format_string_result == "PASS external selected Decimal G and F2 formatting"
    assert fixed_precision_result == "PASS external selected Decimal fixed precision formatting"
    assert number_format_result == "PASS external selected Decimal number formatting"
    assert percent_format_result == "PASS external selected Decimal percent formatting"
    assert exponential_format_result == "PASS external selected Decimal exponential formatting"
    assert currency_format_result == "PASS external selected Decimal currency formatting"
    assert custom_zero_result == "PASS external selected Decimal custom zero formatting"
    assert custom_optional_result == "PASS external selected Decimal custom optional formatting"
    assert canonical_result == "PASS external selected Decimal canonical encodings"
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
        "decimalMultiplyConsumer": multiply_result,
        "decimalDivideConsumer": divide_result,
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
