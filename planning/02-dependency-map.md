# Preliminary dependency map

Arrows mean consumer depends on provider. All .j edges below are **PROPOSED**, not observed implementations. Confirmed upstream declarations are a separate dataset: [declared references](evidence/declared-upstream-references.json). PackageVersion catalogs are not runtime edges. Resolve conditions and restored assets in Stage 2.

| Consumer | Proposed providers / integration edges |
|---|---|
| [dotj-core](repos/dotj-core/MAIN-PLAN.md) | - |
| [dotj-sdk](repos/dotj-sdk/MAIN-PLAN.md) | build,templates,packages |
| [dotj-code](repos/dotj-code/MAIN-PLAN.md) | core |
| [dotj-razor](repos/dotj-razor/MAIN-PLAN.md) | code |
| [dotj-build](repos/dotj-build/MAIN-PLAN.md) | core |
| [dotj-extensions](repos/dotj-extensions/MAIN-PLAN.md) | core |
| [dotj-diagnostics](repos/dotj-diagnostics/MAIN-PLAN.md) | core |
| [dotj-interactive](repos/dotj-interactive/MAIN-PLAN.md) | json,packages |
| [dotj-scaffold](repos/dotj-scaffold/MAIN-PLAN.md) | code,templates,web,entity |
| [dotj-templates](repos/dotj-templates/MAIN-PLAN.md) | core,json |
| [dotj-containers](repos/dotj-containers/MAIN-PLAN.md) | sdk |
| [dotj-web](repos/dotj-web/MAIN-PLAN.md) | core,razor,json |
| [dotj-aspire](repos/dotj-aspire/MAIN-PLAN.md) | extensions,web,containers |
| [dotj-proxy](repos/dotj-proxy/MAIN-PLAN.md) | web,resilience,extensions |
| [dotj-actors](repos/dotj-actors/MAIN-PLAN.md) | core,json,extensions |
| [dotj-auth](repos/dotj-auth/MAIN-PLAN.md) | web,json,core |
| [dotj-service-client](repos/dotj-service-client/MAIN-PLAN.md) | core |
| [dotj-services](repos/dotj-services/MAIN-PLAN.md) | service-client,web,extensions |
| [dotj-entity](repos/dotj-entity/MAIN-PLAN.md) | core,postgresql |
| [dotj-sql](repos/dotj-sql/MAIN-PLAN.md) | postgresql,core |
| [dotj-postgresql](repos/dotj-postgresql/MAIN-PLAN.md) | core |
| [dotj-redis](repos/dotj-redis/MAIN-PLAN.md) | core |
| [dotj-json](repos/dotj-json/MAIN-PLAN.md) | core |
| [dotj-mapster](repos/dotj-mapster/MAIN-PLAN.md) | core;entity(optional) |
| [dotj-container](repos/dotj-container/MAIN-PLAN.md) | core |
| [dotj-validation](repos/dotj-validation/MAIN-PLAN.md) | core;web(optional) |
| [dotj-resilience](repos/dotj-resilience/MAIN-PLAN.md) | core |
| [dotj-reactive](repos/dotj-reactive/MAIN-PLAN.md) | core |
| [dotj-jobs](repos/dotj-jobs/MAIN-PLAN.md) | core,postgresql,scheduler;web(optional) |
| [dotj-scheduler](repos/dotj-scheduler/MAIN-PLAN.md) | core;postgresql(optional) |
| [dotj-mail](repos/dotj-mail/MAIN-PLAN.md) | core |
| [dotj-rest](repos/dotj-rest/MAIN-PLAN.md) | json,core |
| [dotj-refit](repos/dotj-refit/MAIN-PLAN.md) | rest,json;code(dev-optional) |
| [dotj-mqtt](repos/dotj-mqtt/MAIN-PLAN.md) | core;web(optional) |
| [dotj-versioning](repos/dotj-versioning/MAIN-PLAN.md) | web |
| [dotj-swagger](repos/dotj-swagger/MAIN-PLAN.md) | web,openapi |
| [dotj-openapi](repos/dotj-openapi/MAIN-PLAN.md) | json;code(dev-optional) |
| [dotj-graph-platform](repos/dotj-graph-platform/MAIN-PLAN.md) | web,json,core |
| [dotj-graphql](repos/dotj-graphql/MAIN-PLAN.md) | core,json;web(optional) |
| [dotj-presentation](repos/dotj-presentation/MAIN-PLAN.md) | core,toolkit |
| [dotj-forms](repos/dotj-forms/MAIN-PLAN.md) | core |
| [dotj-multiui](repos/dotj-multiui/MAIN-PLAN.md) | core,toolkit;presentation(optional) |
| [dotj-avalonia](repos/dotj-avalonia/MAIN-PLAN.md) | core,toolkit |
| [dotj-uno](repos/dotj-uno/MAIN-PLAN.md) | core,toolkit;web(optional) |
| [dotj-toolkit](repos/dotj-toolkit/MAIN-PLAN.md) | core |
| [dotj-material](repos/dotj-material/MAIN-PLAN.md) | web,validation |
| [dotj-components](repos/dotj-components/MAIN-PLAN.md) | web |
| [dotj-structured-log](repos/dotj-structured-log/MAIN-PLAN.md) | core |
| [dotj-log](repos/dotj-log/MAIN-PLAN.md) | core |
| [dotj-xtest](repos/dotj-xtest/MAIN-PLAN.md) | core |
| [dotj-test](repos/dotj-test/MAIN-PLAN.md) | core |
| [dotj-mock](repos/dotj-mock/MAIN-PLAN.md) | core |
| [dotj-substitute](repos/dotj-substitute/MAIN-PLAN.md) | core;mock(optional-spi) |
| [dotj-coverage](repos/dotj-coverage/MAIN-PLAN.md) | core |
| [dotj-benchmark](repos/dotj-benchmark/MAIN-PLAN.md) | core;diagnostics(optional) |
| [dotj-testcontainers](repos/dotj-testcontainers/MAIN-PLAN.md) | core |
| [dotj-excel](repos/dotj-excel/MAIN-PLAN.md) | openxml,core |
| [dotj-openxml](repos/dotj-openxml/MAIN-PLAN.md) | core |
| [dotj-markdown](repos/dotj-markdown/MAIN-PLAN.md) | core |
| [dotj-ml](repos/dotj-ml/MAIN-PLAN.md) | core |
| [dotj-semantic](repos/dotj-semantic/MAIN-PLAN.md) | json,rest,extensions |
| [dotj-packages](repos/dotj-packages/MAIN-PLAN.md) | core,json |
| [dotj-registry](repos/dotj-registry/MAIN-PLAN.md) | web,packages,postgresql,auth |
| [dotj-automap](repos/dotj-automap/MAIN-PLAN.md) | core;entity(optional) |
| [dotj-mediator](repos/dotj-mediator/MAIN-PLAN.md) | core;container(optional) |
| [dotj-bus](repos/dotj-bus/MAIN-PLAN.md) | core,json,resilience;postgresql(optional);scheduler(optional) |

Provider names in this table omit the common `dotj-` prefix. `optional` marks an integration artifact; `dev-optional` marks a potential development-only tool. Unmarked edges are preliminary prerequisites, still subject to module-level decomposition. No graph claims an existing implementation.

## Cycles and ownership resolutions

| Potential cycle | Proposed resolution |
|---|---|
| core configuration JSON ↔ json → core | core configuration contracts stand alone; JSON provider adapter depends on json, not the core foundation artifact |
| extensions resilience/proxy integrations ↔ web/proxy consumers | split extension contracts from adapters; web/proxy depend only on core contracts, while extension adapters may depend on proxy/resilience |
| sdk ↔ build/packages/templates | JDK CLI bootstrap builds lower tools independently; SDK orchestrates them only after validation |
| packages ↔ registry | packages owns protocol models/client; registry uses those models. A live registry is not required to build or test package resolution |
| tests ↔ mocking/coverage | plain Java independent runner first; test frameworks do not require mock or coverage to execute |
| code generation ↔ compiler/toolchain | javac/annotation processors bootstrap; generated runtime artifacts contain no compiler service dependency |
| web ↔ razor | compiler/IR in Razor; runtime renderer in web; compile-time interface submodule avoids web runtime dependency from Razor |
| service-client ↔ services | neutral wire submodule owned by service-client; no client dependency on service host |
| entity ↔ mappers | projection adapter depends on entity IR; entity does not depend on mapper products |
| auth ↔ registry/entity stores | auth store SPI in auth; optional adapters depend on storage, core protocol module does not |
| jobs ↔ scheduler | scheduler owns generic time/trigger semantics; jobs owns durable invocation/dashboard and depends on scheduler, never the reverse |
| mock ↔ substitute | optional neutral proxy module in mock; no dependence on each other's setup/verification semantics |
| graphql ↔ graph-platform | independent engines; only explicitly approved neutral syntax reuse, one-way and optional |
| UI toolkits ↔ UI frameworks | toolkit remains independent of concrete renderers and native SDKs |

At artifact level, dependency edges must form a DAG for bootstrap. Repository-level optional adapters can create apparent cycles; split artifacts rather than hide them. A new reverse dependency requires a decision record and graph review. No runtime cycle is accepted merely because it can compile.
