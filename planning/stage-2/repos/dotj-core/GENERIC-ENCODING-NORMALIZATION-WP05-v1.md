# Generic Encoding normalization queries

Batch 2226 adds the nonvirtual parameterless IsAlwaysNormalized facade and virtual NormalizationForm overload. The facade passes FormC to the override. The base overload returns false for every supplied form without validating the enum value, matching the selected native implementation. UTF8Encoding inherits that result. A selected Int32 carrier exposes the four named normalization forms while retaining arbitrary integer values for the query contract.

The pinned .NET fixture records 220 cases across generic and UTF8 instances, three custom override behaviors, cloned objects, eleven defined/undefined integer values and both query routes. The packaged consumer checks outcomes and the form observed by the override. It also verifies the four names and values and selected Type identity, array, base-type and underlying-type queries: 460 groups. A negative compile control rejects overriding the nonvirtual facade. The native producer uses Enum.ToObject for undefined values so PowerShell conversion errors cannot enter the evidence.

Both candidate builders explicitly include the new source and class. The owned source-to-class map adds its single class. The product has 97 Java sources and remains JDK-only. CoreLib, producer, fixture, consumer and artifact hashes bind the evidence; LF attributes cover new source and evidence files. Shared verification scratch is serialized across preflight and canonical runs.

The value carrier is provisional. Normalization transforms, complete enum conversions/formatting/interfaces, metadata/source ABI, E01 applicability, task acceptance and framework qualification remain open. No acceptance credit is claimed.

Next is native-selected NormalizationForm formatting, including G/F/D/X, undefined values, provider behavior and invalid format exceptions.
