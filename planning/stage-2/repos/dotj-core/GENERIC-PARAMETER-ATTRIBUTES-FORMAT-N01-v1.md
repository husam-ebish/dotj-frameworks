# GenericParameterAttributes named and unnamed value carrier

Batch 2126 advances DJ-001-N01-T2 without implementation acceptance credit.

GenericParameterAttributes moves from a JVM enum to an immutable selected CLR-enum value carrier. The nine named fields and their integer values remain available; FromInt32 also preserves unnamed bit patterns. values() returns a fresh named-value array. Existing name()/valueOf(String) convenience routes preserve named lookup. Physical java.lang.Enum inheritance and Java EnumSet/Enum.valueOf integration are no longer supplied; CLR enum/boxing identity remains unqualified.

The carrier implements IFormattable and invariant G/F/D/X formatting, including named composites, unsigned-mask decomposition, signed decimal fallback, eight-digit hexadecimal text, ignored providers and invalid-format exceptions. Type keeps the logical Enum base, IsEnum and Int32 underlying identity while using carrier-aware enum value/name enumeration and the selected IFormattable interface projection.

The pinned CoreLib 10.0.12 reference records 280 default values, 4,200 formatted rows and the nine native names/values. The packaged consumer checks 13,162 groups, including logical enum metadata, fresh value/name arrays, named lookup and unnamed GetEnumName results. Other Enum APIs, native inheritance/boxing, remaining interfaces, generic-constraint execution, language integration and full qualification remain open.

The Java runtime remains JDK-only. Reference/development tools and temporary artifacts stay under D:\AI\Implementation\dotj Frameworks.
