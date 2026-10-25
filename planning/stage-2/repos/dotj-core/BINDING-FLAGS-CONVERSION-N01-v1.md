# BindingFlags conversions: bounded N01 projection

Batch 2098 adds IConvertible to the BindingFlags Java carrier. Numeric conversions delegate to the checked Int32 conversion implementation, including overflow and invalid-cast boundaries. GetTypeCode returns Int32. ToType preserves the carrier for Object, Enum and BindingFlags, formats its enum text for String, and rejects a null target with ArgumentNullException("targetType"). Providers are ignored by the selected enum conversion contracts.

The pinned .NET 10.0.12 reference covers 40 values, 640 direct conversions and 1,000 target conversions. The packaged Java consumer checks 3,281 groups, including Type interface projection. Earlier formatting and comparison consumers are retained. This bounded profile does not establish CLR enum identity, complete public API qualification, or implementation acceptance. E01 and project acceptance remain open.

Product code uses JDK APIs only. Python, PowerShell and the pinned .NET runtime are development/reference tools. All temporary artifacts remain under D:\AI\Implementation\dotj Frameworks.
