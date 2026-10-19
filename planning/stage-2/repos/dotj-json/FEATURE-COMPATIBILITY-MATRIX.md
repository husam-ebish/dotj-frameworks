# DJ-023 .j JSON: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Distinguish Newtonsoft extensions from strict JSON: dates, comments, reference identity, type metadata and number coercion need declared modes.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Token reader and writer | Internal planning vocabulary (verify upstream public identity): JsonToken, JsonReader, JsonWriter | Split multibyte input parses correctly; malformed numbers fail at stable locations; configured depth limits prevent exhaustion | Planned; evidence gates open |
| WP-02 | Object contracts and converters | Internal planning vocabulary (verify upstream public identity): JsonContract, TypeResolver, Converter | Recursive converter mistakes are detected; untrusted type names cannot instantiate arbitrary classes; missing/default values follow the chosen profile | Planned; evidence gates open |
| WP-03 | DOM and query operations | Internal planning vocabulary (verify upstream public identity): JToken, JObject, JArray, JsonPath | Duplicate property policy is explicit; deep clones share no mutable children; invalid query expressions fail without executing host code | Planned; evidence gates open |
| WP-04 | Reference identity dates and legacy behaviors | Internal planning vocabulary (verify upstream public identity): ReferenceResolver, DatePolicy, CompatibilityProfile | Cycles terminate under declared policy; timezone/precision differences are recorded; strict output never emits nonstandard tokens silently | Planned; evidence gates open |
| WP-05 | Schema of settings and compatibility corpus | Internal planning vocabulary (verify upstream public identity): SerializerSettings, JsonCompatibilityCase, StreamingBenchmark | Newtonsoft and System.Text.Json expectations are never merged; every deviation is named; serialization memory scales with documented buffering policy | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Do not automatically instantiate arbitrary types from input metadata. Schema functionality may live in separately licensed repositories.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
