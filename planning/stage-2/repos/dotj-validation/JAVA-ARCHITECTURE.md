# DJ-026 .j Validation: Java architecture and contracts

Provide fluent rules, composed validators and contextual validation results.

Product type: JVM validation library. Proposed Java package root: `org.dotj.validation`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-validation-01 | Validator, Rule, PropertyPath, RuleSet | Rule model and fluent construction |
| dotj-validation-02 | Constraint, ComparisonContext, MessageArgument | Built-in validators and comparisons |
| dotj-validation-03 | ValidationContext, AsyncRule, ChildValidator | Asynchronous and child validation |
| dotj-validation-04 | MessageCatalog, CustomValidator, FailureFormatter | Messages localization and extensibility |
| dotj-validation-05 | ValidationAdapter, ValidationResult, RuleCoverage | Web integration and regression acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Property paths and lambda-based member discovery need generated accessors or explicit paths; avoid fragile serialized-lambda inspection.

## Feature contracts and invariants

### WP-01: Rule model and fluent construction

Contract vocabulary: `Validator`, `Rule`, `PropertyPath`, `RuleSet`.

Define property accessors rule chains conditions and dependent rules. Specify cascade modes and severity/error-code metadata. Freeze or isolate mutable builder configuration before concurrent use.

Required observable invariant: Rule ordering is deterministic; nested paths preserve collection indices; concurrent validations do not share mutable request state.

### WP-02: Built-in validators and comparisons

Contract vocabulary: `Constraint`, `ComparisonContext`, `MessageArgument`.

Map null empty length range regex email and comparison semantics. Define culture Unicode and numeric conversion policies. Bound expensive regex and custom validation operations.

Required observable invariant: Null-versus-empty behavior matches its profile; locale changes do not alter invariant constraints; pathological patterns obey declared resource limits.

### WP-03: Asynchronous and child validation

Contract vocabulary: `ValidationContext`, `AsyncRule`, `ChildValidator`.

Propagate cancellation through asynchronous validators. Compose child/collection validation with clear stop policies. Distinguish validation failures from validator execution errors.

Required observable invariant: Cancellation prevents later rules where promised; child failures retain paths; thrown application errors are not misreported as ordinary invalid input.

### WP-04: Messages localization and extensibility

Contract vocabulary: `MessageCatalog`, `CustomValidator`, `FailureFormatter`.

Define placeholder expansion and localized catalogs. Permit custom validators through stable context interfaces. Keep sensitive property values out of default error serialization.

Required observable invariant: Missing translations use documented fallback; custom failures preserve codes/severity; passwords are not included in default messages.

### WP-05: Web integration and regression acceptance

Contract vocabulary: `ValidationAdapter`, `ValidationResult`, `RuleCoverage`.

Integrate endpoint/model binding as an optional web adapter. Port rule-order culture async and collection regression cases. Expose machine-readable failures independently of HTTP formatting.

Required observable invariant: Core validation runs without web dependencies; API responses retain stable field paths; upstream unsupported rules remain explicit inventory entries.

## Bootstrap and dependency boundaries

Functional interfaces, regex, resource bundles and CompletionStage.

Proposed .j dependencies: core;web(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing FluentValidation usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `Validator` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Rule ordering is deterministic; nested paths preserve collection indices; concurrent validations do not share mutable request state. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
