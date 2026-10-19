# Architecture decision records

All decisions below are **provisional planning proposals**. They are not owner approval of unresolved scope/licensing or frozen public APIs.

| ADR | Proposal | Reason | Consequence / validation needed |
|---|---|---|---|
| CORE-ADR-001 | Keep the JDK JVM; adapt libraries independently | Rebuilding CLR is a separate undertaking | CoreCLR/Mono/AOT remain explicit feasibility tracks, not completed ports |
| CORE-ADR-002 | Use independent core artifacts | Avoid a universal dependency and cyclic optional providers | Validate JPMS/artifact graph at module level |
| CORE-ADR-003 | Keep default DI in core and Autofac port in container | Actual upstream ownership differs | Both use shared DI interfaces only where contracts align |
| CORE-ADR-004 | Use explicit type tokens and keyed-service identities | Java erasure cannot represent all .NET service keys with Class alone | Generic variance, open generics and null-key behavior need acceptance fixtures |
| CORE-ADR-005 | Use explicit cancellation/context contracts | Java interruption/future cancellation differ from .NET | No wholesale ExecutionContext parity; preserve observed callback semantics where declared |
| CORE-ADR-006 | Distinguish async close from AutoCloseable | Blocking an async-only resource can deadlock or change behavior | Document sync-versus-async disposal preference and failure aggregation |
| CORE-ADR-007 | Preserve mutable configuration compatibility profile | Observed reload/set behavior is not an atomic snapshot API | Any snapshot API is a separately labeled Java extension |
| CORE-ADR-008 | Keep System.Text.Json and Newtonsoft.Json profiles distinct | Different upstream sources and behavior | Shared codec ownership requires later design; never silently substitute dotj-json |
| CORE-ADR-009 | Keep source pin for analysis; defer release baseline | Snapshot declares a prerelease SDK | Select release tag or explicitly accept prerelease scope before implementation readiness |
| CORE-ADR-010 | Separate declared dependencies from restored closure | MSBuild imports/conditions are unevaluated | Build-aware dependency extraction is a remaining work package |
| CORE-ADR-011 | Record inventory directories before claiming API completeness | Root tree truncation previously obscured scope | All 218 directory entries retained; unsampled groups remain pending |

Rejected as planning defaults: a new JVM; wrappers around existing Java frameworks; replacing default DI with Autofac semantics; using Java Optional for present-null configuration; treating all core JSON behavior as Newtonsoft behavior; inferring stable-release support from a development source snapshot.
