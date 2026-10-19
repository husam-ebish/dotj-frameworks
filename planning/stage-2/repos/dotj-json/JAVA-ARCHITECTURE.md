# DJ-023 .j JSON: Java architecture and contracts

Build an owned JSON reader/writer, object mapper and token DOM.

Product type: JVM serialization library. Proposed Java package root: `org.dotj.json`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-json-01 | JsonToken, JsonReader, JsonWriter | Token reader and writer |
| dotj-json-02 | JsonContract, TypeResolver, Converter | Object contracts and converters |
| dotj-json-03 | JToken, JObject, JArray, JsonPath | DOM and query operations |
| dotj-json-04 | ReferenceResolver, DatePolicy, CompatibilityProfile | Reference identity dates and legacy behaviors |
| dotj-json-05 | SerializerSettings, JsonCompatibilityCase, StreamingBenchmark | Schema of settings and compatibility corpus |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Distinguish Newtonsoft extensions from strict JSON: dates, comments, reference identity, type metadata and number coercion need declared modes.

## Feature contracts and invariants

### WP-01: Token reader and writer

Contract vocabulary: `JsonToken`, `JsonReader`, `JsonWriter`.

Specify streaming tokens depth limits comments and number syntax. Define incremental input and error line/column behavior. Preserve writer escaping formatting and cancellation rules.

Required observable invariant: Split multibyte input parses correctly; malformed numbers fail at stable locations; configured depth limits prevent exhaustion.

### WP-02: Object contracts and converters

Contract vocabulary: `JsonContract`, `TypeResolver`, `Converter`.

Define property naming constructors fields defaults and null policies. Specify converter precedence recursion and generic type resolution. Constrain polymorphic activation through an allowlisted resolver.

Required observable invariant: Recursive converter mistakes are detected; untrusted type names cannot instantiate arbitrary classes; missing/default values follow the chosen profile.

### WP-03: DOM and query operations

Contract vocabulary: `JToken`, `JObject`, `JArray`, `JsonPath`.

Define DOM ownership mutation equality and numeric comparison. Parse JSONPath with explicit supported operator semantics. Support clone merge and change notifications with deterministic order.

Required observable invariant: Duplicate property policy is explicit; deep clones share no mutable children; invalid query expressions fail without executing host code.

### WP-04: Reference identity dates and legacy behaviors

Contract vocabulary: `ReferenceResolver`, `DatePolicy`, `CompatibilityProfile`.

Preserve graph identity through configurable reference handling. Map .NET date decimal and special-number conventions explicitly. Separate strict JSON from Newtonsoft compatibility extensions.

Required observable invariant: Cycles terminate under declared policy; timezone/precision differences are recorded; strict output never emits nonstandard tokens silently.

### WP-05: Schema of settings and compatibility corpus

Contract vocabulary: `SerializerSettings`, `JsonCompatibilityCase`, `StreamingBenchmark`.

Version settings independently from core System.Text.Json profile. Port serializer reader writer and regression fixtures by behavior. Measure large-stream memory use and hostile payload limits.

Required observable invariant: Newtonsoft and System.Text.Json expectations are never merged; every deviation is named; serialization memory scales with documented buffering policy.

## Bootstrap and dependency boundaries

Reader/Writer, reflection, MethodHandles, BigDecimal and java.time; no Jackson/Gson.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Newtonsoft.Json usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `JsonToken` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Split multibyte input parses correctly; malformed numbers fail at stable locations; configured depth limits prevent exhaustion. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
