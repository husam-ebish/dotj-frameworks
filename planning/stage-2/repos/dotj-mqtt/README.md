# DJ-034 .j MQTT: Stage-2 plan

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide MQTT clients, managed connection workflows and broker capabilities where present upstream.

**Written plan coverage: complete for the capability groups below. Source audit: sampled; exhaustive API/test/dependency closure remains open. Implementation: not started.**

| Document | Purpose |
|---|---|
| [PINNED-UPSTREAM](PINNED-UPSTREAM.md) | Source identity, revision and limitations |
| [MODULE-AND-API-INVENTORY](MODULE-AND-API-INVENTORY.md) | Observed source structure and candidate declarations |
| [FEATURE-COMPATIBILITY-MATRIX](FEATURE-COMPATIBILITY-MATRIX.md) | Retained behavior and Java adaptations |
| [DEPENDENCIES-AND-LICENSES](DEPENDENCIES-AND-LICENSES.md) | Proposed dependencies, observed references and rights gates |
| [JAVA-ARCHITECTURE](JAVA-ARCHITECTURE.md) | Module boundaries, contracts, ownership and examples |
| [ADRS](ADRS.md) | Provisional decisions and reopening evidence |
| [TEST-PORT-MAP](TEST-PORT-MAP.md) | Source tests, designed fixtures and oracle method |
| [WORK-PACKAGES](WORK-PACKAGES.md) | Executable task order, outputs and acceptance criteria |
| [RISKS-AND-OPEN-DECISIONS](RISKS-AND-OPEN-DECISIONS.md) | Blocking scope and next actions |
| [API-COMPATIBILITY](API-COMPATIBILITY.md) | Exact .NET names, concepts and N01 gate |
| [READINESS](READINESS.md) | What is written, audited, implementable and releasable |

Feature work packages: **5**. Proposed integration wave: **3**, with evidence/feasibility work allowed earlier. Start with E01-E03 in [WORK-PACKAGES.md](WORK-PACKAGES.md), then the first eligible feature slice.

[All 66 repositories](../../00-REPOSITORY-INDEX.md) | [Shared contracts](../../02-SHARED-CONTRACTS.md)

[API-COMPATIBILITY.md](API-COMPATIBILITY.md) is mandatory before freezing any public contract. It adds four named N01 tasks and three naming/concept acceptance cases.
