# DJ-023 .j JSON: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Build an owned JSON reader/writer, object mapper and token DOM.

Product type: JVM serialization library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-json-01 | JsonToken, JsonReader, JsonWriter | Token reader and writer |
| dotj-json-02 | JsonContract, TypeResolver, Converter | Object contracts and converters |
| dotj-json-03 | JToken, JObject, JArray, JsonPath | DOM and query operations |
| dotj-json-04 | ReferenceResolver, DatePolicy, CompatibilityProfile | Reference identity dates and legacy behaviors |
| dotj-json-05 | SerializerSettings, JsonCompatibilityCase, StreamingBenchmark | Schema of settings and compatibility corpus |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Distinguish Newtonsoft extensions from strict JSON: dates, comments, reference identity, type metadata and number coercion need declared modes.

## Feature contracts and invariants

### WP-01: Token reader and writer

Internal analysis vocabulary (not permission to rename the public API): `JsonToken`, `JsonReader`, `JsonWriter`.

Specify streaming tokens depth limits comments and number syntax. Define incremental input and error line/column behavior. Preserve writer escaping formatting and cancellation rules.

Required observable invariant: Split multibyte input parses correctly; malformed numbers fail at stable locations; configured depth limits prevent exhaustion.

### WP-02: Object contracts and converters

Internal analysis vocabulary (not permission to rename the public API): `JsonContract`, `TypeResolver`, `Converter`.

Define property naming constructors fields defaults and null policies. Specify converter precedence recursion and generic type resolution. Constrain polymorphic activation through an allowlisted resolver.

Required observable invariant: Recursive converter mistakes are detected; untrusted type names cannot instantiate arbitrary classes; missing/default values follow the chosen profile.

### WP-03: DOM and query operations

Internal analysis vocabulary (not permission to rename the public API): `JToken`, `JObject`, `JArray`, `JsonPath`.

Define DOM ownership mutation equality and numeric comparison. Parse JSONPath with explicit supported operator semantics. Support clone merge and change notifications with deterministic order.

Required observable invariant: Duplicate property policy is explicit; deep clones share no mutable children; invalid query expressions fail without executing host code.

### WP-04: Reference identity dates and legacy behaviors

Internal analysis vocabulary (not permission to rename the public API): `ReferenceResolver`, `DatePolicy`, `CompatibilityProfile`.

Preserve graph identity through configurable reference handling. Map .NET date decimal and special-number conventions explicitly. Separate strict JSON from Newtonsoft compatibility extensions.

Required observable invariant: Cycles terminate under declared policy; timezone/precision differences are recorded; strict output never emits nonstandard tokens silently.

### WP-05: Schema of settings and compatibility corpus

Internal analysis vocabulary (not permission to rename the public API): `SerializerSettings`, `JsonCompatibilityCase`, `StreamingBenchmark`.

Version settings independently from core System.Text.Json profile. Port serializer reader writer and regression fixtures by behavior. Measure large-stream memory use and hostile payload limits.

Required observable invariant: Newtonsoft and System.Text.Json expectations are never merged; every deviation is named; serialization memory scales with documented buffering policy.

## Bootstrap and dependency boundaries

Reader/Writer, reflection, MethodHandles, BigDecimal and java.time; no Jackson/Gson.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Newtonsoft.Json usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `JsonToken` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Split multibyte input parses correctly; malformed numbers fail at stable locations; configured depth limits prevent exhaustion. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
