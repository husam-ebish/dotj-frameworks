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
    "IDisposable", "IComparable", "IFormattable", "IFormatProvider", "ISpanFormattable", "IUtf8SpanFormattable", "IConvertible", "TypeCode", "Decimal", "DateTime", "Int32", "ReadOnlySpan", "Span", "UInt16", "UInt32", "Byte", "SByte", "Type", "DBNull", "Attribute", "Exception", "SystemException", "ArgumentException", "ArgumentNullException", "ArgumentOutOfRangeException", "ArithmeticException", "DivideByZeroException", "ValueTuple", "TypeLoadException", "IndexOutOfRangeException", "OverflowException", "InvalidCastException", "InvalidOperationException", "NullReferenceException", "FormatException")]
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
    "ProductInt32BitConsumer", "ProductInt32ArithmeticConsumer", "ProductInt32SpanConsumer")]
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

    CLASSES.mkdir(parents=True, exist_ok=True)
    CONSUMER_CLASSES.mkdir(parents=True, exist_ok=True)
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
    assert disposal_result.startswith("PASS: product IDisposable shape")
    assert type_result == "PASS external System.Type selected identity consumer"
    assert exception_result == "PASS external selected Exception constructors and inner identity"
    assert int32_result == "PASS external selected Int32 bit helpers"
    assert arithmetic_result == "PASS external selected Int32 signed arithmetic"
    assert span_result == "PASS external selected Int32 span parsing and formatting"
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
