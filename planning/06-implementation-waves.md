# Implementation waves: proposed sequencing, not authorization

All 66 targets remain in scope. Waves are dependency/feasibility groupings, not dates or delivery estimates. A repository may have an early contract/feasibility workstream and later integration work. Starting a later wave requires its actual module prerequisites; numerical grouping alone is not a schedule.

## Wave 0: evidence and feasibility gates across all targets

Select eligible source baselines, resolve source relocations, define minimal core contracts, approve the JDK binary lock, map license obligations and investigate browser/mobile/native execution. Resolve code language scope. Begin no implementation under this Stage-1 assignment. License-blocked products retain their later wave slot while independent planning continues.

## Wave 1

Bootstrap the semantic substrate, parsers, standalone tooling and independent test runners. Use installed JDK tools; do not require SDK or registry. Code language scope is a gate. Templates use a temporary minimal fixture format until JSON is available.

| ID | Target and plan |
|---|---|
| DJ-001 | [dotj-core](repos/dotj-core/MAIN-PLAN.md) |
| DJ-023 | [dotj-json](repos/dotj-json/MAIN-PLAN.md) |
| DJ-005 | [dotj-build](repos/dotj-build/MAIN-PLAN.md) |
| DJ-010 | [dotj-templates](repos/dotj-templates/MAIN-PLAN.md) |
| DJ-003 | [dotj-code](repos/dotj-code/MAIN-PLAN.md) |
| DJ-050 | [dotj-xtest](repos/dotj-xtest/MAIN-PLAN.md) |
| DJ-051 | [dotj-test](repos/dotj-test/MAIN-PLAN.md) |

Exit gate: declared contracts and prerequisites are stable; relevant compatibility fixtures, platform limitations, dependency decisions and migration examples are reviewable. Release readiness is evaluated separately for each artifact.

## Wave 2

Build independent JVM libraries and owned data/format clients on core. Split optional adapters to avoid core/json/extension cycles. Package tooling operates on a local deterministic artifact directory.

| ID | Target and plan |
|---|---|
| DJ-006 | [dotj-extensions](repos/dotj-extensions/MAIN-PLAN.md) |
| DJ-025 | [dotj-container](repos/dotj-container/MAIN-PLAN.md) |
| DJ-026 | [dotj-validation](repos/dotj-validation/MAIN-PLAN.md) |
| DJ-027 | [dotj-resilience](repos/dotj-resilience/MAIN-PLAN.md) |
| DJ-028 | [dotj-reactive](repos/dotj-reactive/MAIN-PLAN.md) |
| DJ-045 | [dotj-toolkit](repos/dotj-toolkit/MAIN-PLAN.md) |
| DJ-048 | [dotj-structured-log](repos/dotj-structured-log/MAIN-PLAN.md) |
| DJ-049 | [dotj-log](repos/dotj-log/MAIN-PLAN.md) |
| DJ-021 | [dotj-postgresql](repos/dotj-postgresql/MAIN-PLAN.md) |
| DJ-022 | [dotj-redis](repos/dotj-redis/MAIN-PLAN.md) |
| DJ-059 | [dotj-markdown](repos/dotj-markdown/MAIN-PLAN.md) |
| DJ-058 | [dotj-openxml](repos/dotj-openxml/MAIN-PLAN.md) |
| DJ-062 | [dotj-packages](repos/dotj-packages/MAIN-PLAN.md) |

Exit gate: declared contracts and prerequisites are stable; relevant compatibility fixtures, platform limitations, dependency decisions and migration examples are reviewable. Release readiness is evaluated separately for each artifact.

## Wave 3

Add higher-level data, mapping, protocols, scheduling, documents and JVM test instrumentation. Entity/SQL depend on owned driver contracts; instrumented tests retain an independent non-instrumented oracle.

| ID | Target and plan |
|---|---|
| DJ-020 | [dotj-sql](repos/dotj-sql/MAIN-PLAN.md) |
| DJ-019 | [dotj-entity](repos/dotj-entity/MAIN-PLAN.md) |
| DJ-024 | [dotj-mapster](repos/dotj-mapster/MAIN-PLAN.md) |
| DJ-064 | [dotj-automap](repos/dotj-automap/MAIN-PLAN.md) |
| DJ-065 | [dotj-mediator](repos/dotj-mediator/MAIN-PLAN.md) |
| DJ-030 | [dotj-scheduler](repos/dotj-scheduler/MAIN-PLAN.md) |
| DJ-031 | [dotj-mail](repos/dotj-mail/MAIN-PLAN.md) |
| DJ-032 | [dotj-rest](repos/dotj-rest/MAIN-PLAN.md) |
| DJ-033 | [dotj-refit](repos/dotj-refit/MAIN-PLAN.md) |
| DJ-034 | [dotj-mqtt](repos/dotj-mqtt/MAIN-PLAN.md) |
| DJ-017 | [dotj-service-client](repos/dotj-service-client/MAIN-PLAN.md) |
| DJ-052 | [dotj-mock](repos/dotj-mock/MAIN-PLAN.md) |
| DJ-053 | [dotj-substitute](repos/dotj-substitute/MAIN-PLAN.md) |
| DJ-054 | [dotj-coverage](repos/dotj-coverage/MAIN-PLAN.md) |
| DJ-055 | [dotj-benchmark](repos/dotj-benchmark/MAIN-PLAN.md) |
| DJ-056 | [dotj-testcontainers](repos/dotj-testcontainers/MAIN-PLAN.md) |
| DJ-057 | [dotj-excel](repos/dotj-excel/MAIN-PLAN.md) |

Exit gate: declared contracts and prerequisites are stable; relevant compatibility fixtures, platform limitations, dependency decisions and migration examples are reviewable. Release readiness is evaluated separately for each artifact.

## Wave 4

Compose web, protocol security, distributed runtimes and web tooling. Define Razor IR before runtime components; web transport/security gates precede proxy/auth/service-host integration. Distributed reliability requires real fault testing.

| ID | Target and plan |
|---|---|
| DJ-004 | [dotj-razor](repos/dotj-razor/MAIN-PLAN.md) |
| DJ-012 | [dotj-web](repos/dotj-web/MAIN-PLAN.md) |
| DJ-016 | [dotj-auth](repos/dotj-auth/MAIN-PLAN.md) |
| DJ-018 | [dotj-services](repos/dotj-services/MAIN-PLAN.md) |
| DJ-014 | [dotj-proxy](repos/dotj-proxy/MAIN-PLAN.md) |
| DJ-035 | [dotj-versioning](repos/dotj-versioning/MAIN-PLAN.md) |
| DJ-037 | [dotj-openapi](repos/dotj-openapi/MAIN-PLAN.md) |
| DJ-036 | [dotj-swagger](repos/dotj-swagger/MAIN-PLAN.md) |
| DJ-039 | [dotj-graphql](repos/dotj-graphql/MAIN-PLAN.md) |
| DJ-038 | [dotj-graph-platform](repos/dotj-graph-platform/MAIN-PLAN.md) |
| DJ-015 | [dotj-actors](repos/dotj-actors/MAIN-PLAN.md) |
| DJ-029 | [dotj-jobs](repos/dotj-jobs/MAIN-PLAN.md) |
| DJ-066 | [dotj-bus](repos/dotj-bus/MAIN-PLAN.md) |

Exit gate: declared contracts and prerequisites are stable; relevant compatibility fixtures, platform limitations, dependency decisions and migration examples are reviewable. Release readiness is evaluated separately for each artifact.

## Wave 5

Integrate SDK, scaffolding, orchestration, registry and advanced AI/diagnostic workflows. Low-level prerequisites must already build independently. Diagnostics and ML native feasibility can be investigated earlier.

| ID | Target and plan |
|---|---|
| DJ-002 | [dotj-sdk](repos/dotj-sdk/MAIN-PLAN.md) |
| DJ-009 | [dotj-scaffold](repos/dotj-scaffold/MAIN-PLAN.md) |
| DJ-008 | [dotj-interactive](repos/dotj-interactive/MAIN-PLAN.md) |
| DJ-007 | [dotj-diagnostics](repos/dotj-diagnostics/MAIN-PLAN.md) |
| DJ-011 | [dotj-containers](repos/dotj-containers/MAIN-PLAN.md) |
| DJ-013 | [dotj-aspire](repos/dotj-aspire/MAIN-PLAN.md) |
| DJ-063 | [dotj-registry](repos/dotj-registry/MAIN-PLAN.md) |
| DJ-060 | [dotj-ml](repos/dotj-ml/MAIN-PLAN.md) |
| DJ-061 | [dotj-semantic](repos/dotj-semantic/MAIN-PLAN.md) |

Exit gate: declared contracts and prerequisites are stable; relevant compatibility fixtures, platform limitations, dependency decisions and migration examples are reviewable. Release readiness is evaluated separately for each artifact.

## Wave 6

Integrate native/mobile/browser UI products after execution and component-runtime feasibility is demonstrated. Core UI research may occur earlier; unsupported platforms remain explicit blockers.

| ID | Target and plan |
|---|---|
| DJ-040 | [dotj-presentation](repos/dotj-presentation/MAIN-PLAN.md) |
| DJ-041 | [dotj-forms](repos/dotj-forms/MAIN-PLAN.md) |
| DJ-042 | [dotj-multiui](repos/dotj-multiui/MAIN-PLAN.md) |
| DJ-043 | [dotj-avalonia](repos/dotj-avalonia/MAIN-PLAN.md) |
| DJ-044 | [dotj-uno](repos/dotj-uno/MAIN-PLAN.md) |
| DJ-046 | [dotj-material](repos/dotj-material/MAIN-PLAN.md) |
| DJ-047 | [dotj-components](repos/dotj-components/MAIN-PLAN.md) |

Exit gate: declared contracts and prerequisites are stable; relevant compatibility fixtures, platform limitations, dependency decisions and migration examples are reviewable. Release readiness is evaluated separately for each artifact.

## Cross-wave integration and release gates

Use contract-only artifacts to permit parallel planning without pretending downstream implementations exist. Optional web dashboards for jobs, auth storage adapters, SDK workloads and native renderer adapters can land after their base modules. Core configuration JSON adapters and extension integrations likewise wait for their providers.

A release candidate requires completed detailed plans, authorized implementation, verified declared capabilities, documented deviations, supported-platform runs, security/provenance review and reproducible artifacts. No wave or repository currently passes these gates.
