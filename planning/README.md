# .j Frameworks: Stage-1 planning package

Pronounced “dot jay frameworks.” Planning date: 2026-10-18.

**66 main plans written. Detailed analysis and implementation have not started. No release is ready.** Reconnaissance is scoped/partial as shown below; unresolved source, license and platform decisions remain visible. Main plans are ready to guide detailed analysis, not to authorize coding.

## Reading order

1. [Complete repository and Java foundation inventories](00-repository-inventory.md)
2. [Ecosystem architecture](01-ecosystem-main-plan.md)
3. [Dependency map and bootstrap cycles](02-dependency-map.md)
4. [Java foundation and dependency policy](03-java-foundation-and-dependency-policy.md)
5. [Compatibility and testing](04-compatibility-and-testing-strategy.md)
6. [Upstream provenance and license status](05-upstream-provenance-and-license-status.md)
7. [Implementation waves](06-implementation-waves.md)
8. [Open decisions and blockers](07-open-decisions-and-blockers.md)
9. [Detailed-planning handoff](08-detailed-planning-handoff.md)
10. [Actual source ownership and discovered dependencies](09-source-ownership-and-discovered-dependencies.md)
11. [Package validation report](VALIDATION.md)

## Linked plan/status index

“Written” is a main-plan status. “Scoped” means selected README/tree/metadata/license material was inspected; it is not an exhaustive audit. “Partial” identifies specific missing or limited evidence in the plan and manifest. Later-stage statuses are independent.

| ID | Product and main plan | Main plan | Reconnaissance | Detailed analysis | Implementation | Release |
|---|---|---|---|---|---|---|
| DJ-001 | [.j Core](repos/dotj-core/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-002 | [.j SDK](repos/dotj-sdk/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-003 | [.j Code](repos/dotj-code/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-004 | [.j Razor](repos/dotj-razor/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-005 | [.j Build](repos/dotj-build/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-006 | [.j Extensions](repos/dotj-extensions/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-007 | [.j Diagnostics](repos/dotj-diagnostics/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-008 | [.j Interactive](repos/dotj-interactive/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-009 | [.j Scaffold](repos/dotj-scaffold/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-010 | [.j Templates](repos/dotj-templates/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-011 | [.j Containers](repos/dotj-containers/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-012 | [.j Web](repos/dotj-web/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-013 | [.j Aspire](repos/dotj-aspire/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-014 | [.j Proxy](repos/dotj-proxy/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-015 | [.j Actors](repos/dotj-actors/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-016 | [.j Auth](repos/dotj-auth/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-017 | [.j Service Client](repos/dotj-service-client/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-018 | [.j Services](repos/dotj-services/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-019 | [.j Entity](repos/dotj-entity/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-020 | [.j SQL](repos/dotj-sql/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-021 | [.j PostgreSQL](repos/dotj-postgresql/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-022 | [.j Redis](repos/dotj-redis/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-023 | [.j JSON](repos/dotj-json/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-024 | [.j Mapster](repos/dotj-mapster/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-025 | [.j Container](repos/dotj-container/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-026 | [.j Validation](repos/dotj-validation/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-027 | [.j Resilience](repos/dotj-resilience/MAIN-PLAN.md) | Written | Scoped reconnaissance | Not started | Not started | Not ready |
| DJ-028 | [.j Reactive](repos/dotj-reactive/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-029 | [.j Jobs](repos/dotj-jobs/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-030 | [.j Scheduler](repos/dotj-scheduler/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-031 | [.j Mail](repos/dotj-mail/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-032 | [.j REST](repos/dotj-rest/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-033 | [.j Refit](repos/dotj-refit/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-034 | [.j MQTT](repos/dotj-mqtt/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-035 | [.j Versioning](repos/dotj-versioning/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-036 | [.j Swagger](repos/dotj-swagger/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-037 | [.j OpenAPI](repos/dotj-openapi/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-038 | [.j Graph Platform](repos/dotj-graph-platform/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-039 | [.j GraphQL](repos/dotj-graphql/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-040 | [.j Presentation](repos/dotj-presentation/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-041 | [.j Forms](repos/dotj-forms/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-042 | [.j MultiUI](repos/dotj-multiui/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-043 | [.j Avalonia](repos/dotj-avalonia/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-044 | [.j Uno](repos/dotj-uno/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-045 | [.j Toolkit](repos/dotj-toolkit/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-046 | [.j Material](repos/dotj-material/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-047 | [.j Components](repos/dotj-components/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-048 | [.j Structured Log](repos/dotj-structured-log/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-049 | [.j Log](repos/dotj-log/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-050 | [.j XTest](repos/dotj-xtest/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-051 | [.j Test](repos/dotj-test/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-052 | [.j Mock](repos/dotj-mock/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-053 | [.j Substitute](repos/dotj-substitute/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-054 | [.j Coverage](repos/dotj-coverage/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-055 | [.j Benchmark](repos/dotj-benchmark/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-056 | [.j Testcontainers](repos/dotj-testcontainers/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-057 | [.j Excel](repos/dotj-excel/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-058 | [.j OpenXML](repos/dotj-openxml/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-059 | [.j Markdown](repos/dotj-markdown/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-060 | [.j ML](repos/dotj-ml/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-061 | [.j Semantic](repos/dotj-semantic/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-062 | [.j Packages](repos/dotj-packages/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-063 | [.j Registry](repos/dotj-registry/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-064 | [.j Automap](repos/dotj-automap/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-065 | [.j Mediator](repos/dotj-mediator/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |
| DJ-066 | [.j Bus](repos/dotj-bus/MAIN-PLAN.md) | Written | Partial reconnaissance | Not started | Not started | Not ready |

Evidence manifests contain immutable source links, retrieved-file hashes, declared upstream references and access gaps. No upstream application source or target implementation is included in this package.
