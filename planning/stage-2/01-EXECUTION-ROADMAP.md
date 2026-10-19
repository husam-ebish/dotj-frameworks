# Execution roadmap

**Owner requirement:** exact upstream .NET public names, casing and concepts across all 66 repositories. Read [the mandatory naming policy](08-DOTNET-API-COMPATIBILITY-POLICY.md). N01 adds a source-to-Java public API mapping and concept-preservation gate; Java implementation details must not become a replacement learning path.

This is sequencing, not a promise of dates or a claim that one team can implement 66 products at once. Work is selected by artifact-level prerequisites. Research for a later native/runtime wave can happen early; a wave number does not block independent contract work.

## Wave 0: qualify evidence and shared contracts

Complete E01-E03 for the first slice: reference release, rights, exact JVM/.NET toolchain locks, semantic inventory, dependency ownership, actual test IDs and oracle output. Resolve cross-product contract boundaries. Run early feasibility studies for compiler/runtime, native/UI/mobile/browser, instrumentation and external source dependencies. Retain blocked scope visibly.

## Wave 1

Bootstrap core contracts, owned serializers, build/template tools, language services and standalone test runners.

| Repository | Immediate integration prerequisite |
|---|---|
| [dotj-core](repos/dotj-core/WORK-PACKAGES.md) | No product dependency in the base foundation |
| [dotj-code](repos/dotj-code/WORK-PACKAGES.md) | core |
| [dotj-build](repos/dotj-build/WORK-PACKAGES.md) | core |
| [dotj-templates](repos/dotj-templates/WORK-PACKAGES.md) | core,json |
| [dotj-json](repos/dotj-json/WORK-PACKAGES.md) | core |
| [dotj-xtest](repos/dotj-xtest/WORK-PACKAGES.md) | core |
| [dotj-test](repos/dotj-test/WORK-PACKAGES.md) | core |

## Wave 2

Deliver portable libraries, owned clients, formats and local package tooling over narrow core artifacts.

| Repository | Immediate integration prerequisite |
|---|---|
| [dotj-extensions](repos/dotj-extensions/WORK-PACKAGES.md) | core |
| [dotj-postgresql](repos/dotj-postgresql/WORK-PACKAGES.md) | core |
| [dotj-redis](repos/dotj-redis/WORK-PACKAGES.md) | core |
| [dotj-container](repos/dotj-container/WORK-PACKAGES.md) | core |
| [dotj-validation](repos/dotj-validation/WORK-PACKAGES.md) | core;web(optional) |
| [dotj-resilience](repos/dotj-resilience/WORK-PACKAGES.md) | core |
| [dotj-reactive](repos/dotj-reactive/WORK-PACKAGES.md) | core |
| [dotj-toolkit](repos/dotj-toolkit/WORK-PACKAGES.md) | core |
| [dotj-structured-log](repos/dotj-structured-log/WORK-PACKAGES.md) | core |
| [dotj-log](repos/dotj-log/WORK-PACKAGES.md) | core |
| [dotj-openxml](repos/dotj-openxml/WORK-PACKAGES.md) | core |
| [dotj-markdown](repos/dotj-markdown/WORK-PACKAGES.md) | core |
| [dotj-packages](repos/dotj-packages/WORK-PACKAGES.md) | core,json |

## Wave 3

Deliver data access, mapping, scheduling, protocol clients, documents and JVM instrumentation.

| Repository | Immediate integration prerequisite |
|---|---|
| [dotj-service-client](repos/dotj-service-client/WORK-PACKAGES.md) | core |
| [dotj-entity](repos/dotj-entity/WORK-PACKAGES.md) | core,postgresql |
| [dotj-sql](repos/dotj-sql/WORK-PACKAGES.md) | postgresql,core |
| [dotj-mapster](repos/dotj-mapster/WORK-PACKAGES.md) | core;entity(optional) |
| [dotj-scheduler](repos/dotj-scheduler/WORK-PACKAGES.md) | core;postgresql(optional) |
| [dotj-mail](repos/dotj-mail/WORK-PACKAGES.md) | core |
| [dotj-rest](repos/dotj-rest/WORK-PACKAGES.md) | json,core |
| [dotj-refit](repos/dotj-refit/WORK-PACKAGES.md) | rest,json;code(dev-optional) |
| [dotj-mqtt](repos/dotj-mqtt/WORK-PACKAGES.md) | core;web(optional) |
| [dotj-mock](repos/dotj-mock/WORK-PACKAGES.md) | core |
| [dotj-substitute](repos/dotj-substitute/WORK-PACKAGES.md) | core;mock(optional-spi) |
| [dotj-coverage](repos/dotj-coverage/WORK-PACKAGES.md) | core |
| [dotj-benchmark](repos/dotj-benchmark/WORK-PACKAGES.md) | core;diagnostics(optional) |
| [dotj-testcontainers](repos/dotj-testcontainers/WORK-PACKAGES.md) | core |
| [dotj-excel](repos/dotj-excel/WORK-PACKAGES.md) | openxml,core |
| [dotj-automap](repos/dotj-automap/WORK-PACKAGES.md) | core;entity(optional) |
| [dotj-mediator](repos/dotj-mediator/WORK-PACKAGES.md) | core;container(optional) |

## Wave 4

Integrate web, authentication, services, proxies, GraphQL, actors, jobs and messaging.

| Repository | Immediate integration prerequisite |
|---|---|
| [dotj-razor](repos/dotj-razor/WORK-PACKAGES.md) | code |
| [dotj-web](repos/dotj-web/WORK-PACKAGES.md) | core,razor,json |
| [dotj-proxy](repos/dotj-proxy/WORK-PACKAGES.md) | web,resilience,extensions |
| [dotj-actors](repos/dotj-actors/WORK-PACKAGES.md) | core,json,extensions |
| [dotj-auth](repos/dotj-auth/WORK-PACKAGES.md) | web,json,core |
| [dotj-services](repos/dotj-services/WORK-PACKAGES.md) | service-client,web,extensions |
| [dotj-jobs](repos/dotj-jobs/WORK-PACKAGES.md) | core,postgresql,scheduler;web(optional) |
| [dotj-versioning](repos/dotj-versioning/WORK-PACKAGES.md) | web |
| [dotj-swagger](repos/dotj-swagger/WORK-PACKAGES.md) | web,openapi |
| [dotj-openapi](repos/dotj-openapi/WORK-PACKAGES.md) | json;code(dev-optional) |
| [dotj-graph-platform](repos/dotj-graph-platform/WORK-PACKAGES.md) | web,json,core |
| [dotj-graphql](repos/dotj-graphql/WORK-PACKAGES.md) | core,json;web(optional) |
| [dotj-bus](repos/dotj-bus/WORK-PACKAGES.md) | core,json,resilience;postgresql(optional);scheduler(optional) |

## Wave 5

Compose SDK, scaffolding, orchestration, registry, diagnostics and AI workflows after lower-level contracts stabilize.

| Repository | Immediate integration prerequisite |
|---|---|
| [dotj-sdk](repos/dotj-sdk/WORK-PACKAGES.md) | build,templates,packages |
| [dotj-diagnostics](repos/dotj-diagnostics/WORK-PACKAGES.md) | core |
| [dotj-interactive](repos/dotj-interactive/WORK-PACKAGES.md) | json,packages |
| [dotj-scaffold](repos/dotj-scaffold/WORK-PACKAGES.md) | code,templates,web,entity |
| [dotj-containers](repos/dotj-containers/WORK-PACKAGES.md) | sdk |
| [dotj-aspire](repos/dotj-aspire/WORK-PACKAGES.md) | extensions,web,containers |
| [dotj-ml](repos/dotj-ml/WORK-PACKAGES.md) | core |
| [dotj-semantic](repos/dotj-semantic/WORK-PACKAGES.md) | json,rest,extensions |
| [dotj-registry](repos/dotj-registry/WORK-PACKAGES.md) | web,packages,postgresql,auth |

## Wave 6

Qualify native/mobile/browser UI products after backend feasibility; integrate browser component libraries after web/Razor contracts.

| Repository | Immediate integration prerequisite |
|---|---|
| [dotj-presentation](repos/dotj-presentation/WORK-PACKAGES.md) | core,toolkit |
| [dotj-forms](repos/dotj-forms/WORK-PACKAGES.md) | core |
| [dotj-multiui](repos/dotj-multiui/WORK-PACKAGES.md) | core,toolkit;presentation(optional) |
| [dotj-avalonia](repos/dotj-avalonia/WORK-PACKAGES.md) | core,toolkit |
| [dotj-uno](repos/dotj-uno/WORK-PACKAGES.md) | core,toolkit;web(optional) |
| [dotj-material](repos/dotj-material/WORK-PACKAGES.md) | web,validation |
| [dotj-components](repos/dotj-components/WORK-PACKAGES.md) | web |

## First vertical slice and review milestones

1. M0: accepted immutable reference/toolchain/rights records and an independently runnable fixture format.
2. M1: core type tokens, error/context vocabulary and resource ownership (core WP-01), validated with deterministic lifecycle fixtures.
3. M2: cancellation/async contracts (core WP-02), including callback ordering, unregister/close differences, races and failure propagation.
4. M3: default DI and configuration (core WP-03), followed by options/logging/hosting (WP-04). Keep each artifact independently buildable; do not wait for whole-core parity.
5. M4: independent JSON/build/test/tooling slices that consume only the accepted core subset. Bootstrap tools with installed javac/jar and plain process runners.
6. M5: select one end-to-end application flow, such as owned PostgreSQL plus SQL mapper or a minimal web endpoint, only after its actual dependencies pass their gates. A successful example is not full-product parity.
7. M6: release one explicitly bounded capability profile with reproducible artifacts, documented limitations and all required evidence. Remaining capabilities retain their backlog and gate status.

## Integration and completion policy

Each feature PR includes its contract, implementation after authorization, fixture mapping, actual results, dependency/notice changes and migration example. Merge gates apply to the changed capability rather than demanding the entire ecosystem be complete. A repository becomes implementation-complete only when every retained feature is implemented or explicitly dispositioned with a documented decision. Release readiness additionally requires tested platform support, provenance/security review and reproducible artifact evidence.

## SDK integration sequencing

The product waves above describe whole-product dependencies. The [SDK integration milestones](sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md) bring forward a minimal console/library/local-feed slice after its narrow core/build/package/template prerequisites. SDK-I01 contract qualification can start with foundation research; a working public registry is not a prerequisite for local SDK development. Keep the existing first core slice. Do not wait for all 66 products before proving the minimal workflow.
