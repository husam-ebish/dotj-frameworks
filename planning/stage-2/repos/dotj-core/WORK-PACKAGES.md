# Work packages

Status: **DRAFT, INCOMPLETE**. Analysis work may continue under the Stage-2 authorization. Implementation work below is a future plan and requires a later implementation instruction. No time estimates are assigned.

## Remaining detailed-analysis packages

| ID | Work | Prerequisite | Deliverable and acceptance | Status |
|---|---|---|---|---|
| CORE-A01 | Select release/source and oracle toolchain baseline | Current evidence pin | Verified immutable commit/tag, explicit release family or accepted prerelease profile, SDK/runtime versions/checksums; all reference files reconciled | OPEN |
| CORE-A02 | Complete recursive module/source census | Untruncated library root inventory | All 218 directories enumerated; imports/shared/native/generated inputs mapped; every source branch retained or explicitly classified | IN PROGRESS: immediate-child inventory complete |
| CORE-A03 | Semantic public API and test census | A01, A02 | Build/parser-aware symbol and attributed-test inventory with conditions and extraction reproducibility; no regex candidate count labeled as complete | IN PROGRESS: 8 reference files and 12 test files sampled |
| CORE-A04 | Resolve dependency closure and license provenance | A01, A02 | Evaluated MSBuild references for chosen TFMs, build/test/runtime/native separation, notices and source eligibility decisions | OPEN: raw declarations extracted |
| CORE-A05 | Finish cancellation/context state model | A01; inspected token source/tests | State transitions and linearization points for register/cancel/unregister/close/async-close/link/reset/timer races; explicit context adaptation | IN PROGRESS |
| CORE-A06 | Finish DI and scope contracts | A01, A05 | Complete keyed/open-generic/constructor/caching/validation matrix; ownership and disposal failure semantics with test IDs | IN PROGRESS |
| CORE-A07 | Finish configuration/change/options contracts | A01, A05 | Presence/keys/provider ordering/reload failure/re-registration/options startup/cache matrix; async scope tied to release | IN PROGRESS |
| CORE-A08 | Analyze logger/host implementation and native adapters | A01, A06, A07 | Source-backed logging/lifecycle order, failure and shutdown contract; OS adapters separate | OPEN: reference declarations sampled |
| CORE-A09 | Map all remaining BCL and runtime groups | A02, A03 | Per-feature JDK/own-Java/adaptation/feasibility disposition, dependencies and test map; no dropped directories | OPEN |
| CORE-A10 | Reconcile ecosystem ownership and approve contract draft | A05-A09 | Update core/extensions/json/openxml/mail/resilience ownership and artifact DAG; consumers acknowledge compatibility contracts | OPEN |

A01/A04 are readiness gates, not instructions to stop independent source analysis. A02/A09 may require many later increments. This document does not pretend the current foundation slice covers the entire runtime repository.

## Future implementation packages: first foundation slice

All rows have implementation status **NOT STARTED / NOT AUTHORIZED**. Acceptance criteria are proposed and must be frozen after the corresponding analysis packages. The fixture references are from [TEST-PORT-MAP](TEST-PORT-MAP.md).

### CORE-W01: build and independent fixture harness

- Prerequisites: A01, relevant A04 decisions; later implementation authorization.
- Modules/output: JDK-only compilation/package commands, independent assertions, paired C#/Java fixture envelope and deterministic result comparison.
- Acceptance: builds from a clean directory with locked tool inputs; no Java framework dependencies; reports failures independently of .j DI/logging; emits tool versions, revision and environment; reference execution can be disabled without pretending it passed.
- Validation: one controlled pass and one intentional mismatch through the comparison path; no dependence on the code under test to determine success.

### CORE-W02: type identity, context and error vocabulary

- Prerequisites: W01, A05/A06 contract decisions.
- Modules/output: contracts and type-token/service-key vocabulary; explicit .j context carrier; error categories retaining causes and cancellation identity.
- Acceptance: parameterized service types remain distinct; context captures bounded immutable values; mutable thread-local data is not silently copied; raw/null/keyed identities follow the frozen contract; exceptions preserve causes without revealing secrets.
- Validation: type identity and context migration fixtures, including executor boundaries and equality collisions.

### CORE-W03: cancellation state and callback registration

- Prerequisites: W02, completed A05 state model.
- Modules/output: cancellation token/source/registration, cancellation outcome and explicit context dispatch.
- Acceptance: requested state precedes callbacks; sequential callback ordering and exception modes match declared profile; late registration executes synchronously; unregister and close have different completion semantics; self-close does not deadlock; repeated operations follow disposed-state contract.
- Validation: CORE-TEST-001 through 008, plus barrier-controlled races and outer deadlock watchdog. Linked tokens, timers and reset remain in this package scope; do not call it complete after only synchronous callbacks.

### CORE-W04: async ownership and resource disposal

- Prerequisites: W03, A06 disposal matrix.
- Modules/output: async close contract and reusable disposal coordination rules.
- Acceptance: no default blocking of async-only resources; deterministic order/failure aggregation; reference-identity deduplication; borrowed resources not disposed; async completion represents finished cleanup; cancellation does not falsely imply rollback.
- Validation: dual sync/async resources, failing close, duplicate aliases and cancellation during cleanup; scope-specific tests repeated after W06.

### CORE-W05: DI abstractions and immutable registration model

- Prerequisites: W02, W04, A06 keyed/generic/constructor decisions.
- Modules/output: service descriptors, lifetimes, scopes, keyed/unkeyed identities and provider contracts.
- Acceptance: all selected upstream public declarations have a retained/adapted/blocked mapping; registration ordering and ownership are explicit; default DI and Autofac remain separate contracts; no dependency on dotj-container.
- Validation: declaration mapping and multi-registration/required-missing behavior; parameterized keys and constructor ambiguity fixtures.

### CORE-W06: default DI resolution and scope engine

- Prerequisites: W05, complete A06.
- Modules/output: default provider resolution, lifetime caches, validation and close coordination.
- Acceptance: singleton identity under concurrency; correct scope ownership; supplied instances stay caller-owned; scope/root disposal reject later resolution as declared; all owned resources receive cleanup despite failures; optional optimized activation behaves like the reflection path.
- Validation: CORE-TEST-009 through 017 and full selected DI specification suite; constructor failures, factory recursion, scope disposal races and generic constraint cases.

### CORE-W07: change-token primitives

- Prerequisites: W03/W04, A07 notification model.
- Modules/output: token generations, subscriptions and sync/async callback adapters.
- Acceptance: new generation after notification; no re-registration after subscription close; async consumer completion precedes next registration; producer/synchronous/asynchronous error paths follow frozen semantics; no unrelated ambient context capture.
- Validation: CORE-TEST-024 through 026 plus source producer failures and simultaneous disposal.

### CORE-W08: configuration abstractions and root behavior

- Prerequisites: W07, A07 key/presence decisions.
- Modules/output: provider/section/root interfaces, memory provider and configuration root.
- Acceptance: present-null distinct from missing; last provider wins; writes reach all providers; empty-provider write fails; section existence and child ordering match declared profile; reload-token generation changes; partial reload failure semantics documented and tested.
- Validation: CORE-TEST-018 through 023 plus Unicode keys and multi-provider failure scenarios. JSON/XML/file providers are separate adapters, not implicit completed features.

### CORE-W09: named options, validation and cache behavior

- Prerequisites: W06-W08, full A07 including release-specific async validation.
- Modules/output: named options/value/snapshot/monitor contracts, validation and cache integration.
- Acceptance: configure/post-configure/validate order; monitor invalidation by name; no invalid value published; subscription cleanup; interface-specific lifetime/cache behavior; async startup capability only claimed after its full test matrix passes.
- Validation: CORE-TEST-027 through 032 and selected async startup failure/cancellation/cache-race cases. Do not replace sync validation with blocking on arbitrary stages.

### CORE-W10: logging contracts and runtime logger adapters

- Prerequisites: W02 and completed A08 logging analysis.
- Modules/output: logger interfaces, scope/context, provider fan-out and separately packaged DI/configuration integration.
- Acceptance: no dependency from contracts on a concrete logger; formatter/level/filter/scope semantics verified; no accidental Serilog destructuring claim; no scope leaks across reused threads.
- Validation: actual upstream logging tests still need selection. This package is blocked from implementation readiness until those are mapped.

### CORE-W11: host composition and lifecycle

- Prerequisites: W06, W08-W10 and completed A08 hosting analysis.
- Modules/output: host/service abstractions, startup/shutdown coordination and explicit lifetime ownership.
- Acceptance: frozen service order, failure rollback, stop timeout and cancellation semantics; resource cleanup completes or reports bounded failure; OS service integration remains separate and platform-tested.
- Validation: select upstream host lifecycle tests, then add startup failure, stop hangs, repeated stop, JVM process signals and cleanup traces.

### CORE-W12: numeric and time compatibility profiles

- Prerequisites: W01, completed corresponding A09 numeric/time work.
- Modules/output: decimal/unsigned/time representation and conversion adapters for the declared API subset.
- Acceptance: range/overflow/scale/rounding, ticks/Kind/time-zone distinctions and serialization representation are explicit; BigDecimal/Instant use does not erase observable metadata.
- Validation: exact upstream vectors plus cross-runtime overflow, signed-zero/scale, locale parsing and DST cases. This package is not ready for coding while the arithmetic/globalization audit is incomplete.

## Whole-core completion

W01-W12 are only the first foundation workstream. Additional packages must be created for every remaining retained group after A09. No full-core completion percentage is assigned. Whole-core readiness requires the complete module/API/test map, dependency/license decisions and closed cross-product boundaries, followed by separately authorized implementation and actual validation.
