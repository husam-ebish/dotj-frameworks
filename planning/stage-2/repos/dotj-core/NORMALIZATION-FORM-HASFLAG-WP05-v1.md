# NormalizationForm selected HasFlag behavior

Batch 2230 adds the selected CLR Enum argument projection for HasFlag on the provisional Int32 NormalizationForm carrier. Matching values compare all 32 bits, including sign bits. Zero flag is always included. The operation is supported even though the native enum has no Flags attribute. Null flag is rejected with the flag parameter; unrelated native enum types report the selected type-specific ArgumentException. The Java Object argument is an adapter for that selected CLR Enum domain, not a complete source ABI claim.

The pinned native fixture records 484 ordered pairs across 22 values and 66 null/DayOfWeek/DateTimeKind controls. It covers both Int32 limits, negative masks, zero, named combinations and high bits. The packaged consumer compares 550 results or exact exception type/message/HResult/parameter records. The fixture explicitly records that FlagsAttribute is absent.

The class inventory remains 97 Java sources. Builders, owned-map binding, distribution/rights-input checks, compiled API audit and retained generic/UTF8/default/custom/stateful and normalization consumers remain required. CoreLib, producer, fixture, consumer and candidate hashes bind the evidence, with LF source/evidence attributes. No new product runtime library is introduced.

This is selected HasFlag behavior. Parsing, full enum ABI, normalization transforms, E01 applicability, task acceptance and framework qualification remain open. No acceptance credit is claimed. Next is a source-pinned review of UnicodeEncoding/UTF-16 and remaining foundation acceptance work, establishing the concrete codec implementation and qualification plan without inventing a project-wide batch total.
