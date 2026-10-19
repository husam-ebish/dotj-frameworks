# DJ-053 .j Substitute: risks and open decisions

| ID | Risk/question | Blocking scope | Owner role | Next action |
|---|---|---|---|---|
| R01 | Analysis pin may not be eligible release | All source-derived implementation | Maintainer / licensing reviewer | Complete E01; record release family and rights; no historical license assumption |
| R02 | Sampled source is not exhaustive API/test/dependency closure | Affected feature claims and first implementation slice | API/build maintainer | Complete E02/E03 for each consumed capability; retain every unassigned module |
| R03 | Reuse only a neutral proxy submodule if suitable; preserve distinct public semantics and avoid dependency cycles with mock. | Product/platform-specific packages | Product architect / platform maintainer | Run the matching feasibility packages; document measured result and alternatives |
| R04 | Thread-local recording and fluent setup must avoid consuming production calls; Java primitive defaults and overloads need a documented DSL. | Behavioral/API compatibility | Compatibility maintainer | Resolve precise Java contract and source fixture mapping before each slice |
| R05 | Proposed product dependencies are not ready implementations | Integration packages | Integration maintainer | Freeze neutral contracts, bootstrap independently and split optional adapters |
| R06 | Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release. | Source reuse / redistribution | Licensing reviewer | Resolve exact version and source/asset obligations; record evidence without implying clearance |

## Decision defaults

Proceed with the architecture and work breakdown above for planning. Do not pause the entire ecosystem because one native backend, license or provider is blocked. Implementation eligibility is assessed per slice. A failed feasibility experiment may lead to an explicit reduced support profile, alternate owned design or continued blocker; it never silently removes the original capability from the inventory. No invented dates or effort estimates are used.
