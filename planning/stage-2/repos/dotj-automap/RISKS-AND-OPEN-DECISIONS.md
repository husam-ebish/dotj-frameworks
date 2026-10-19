# DJ-064 .j Automap: risks and open decisions

| ID | Risk/question | Blocking scope | Owner role | Next action |
|---|---|---|---|---|
| R01 | Analysis pin may not be eligible release | All source-derived implementation | Maintainer / licensing reviewer | Complete E01; record release family and rights; no historical license assumption |
| R02 | Sampled source is not exhaustive API/test/dependency closure | Affected feature claims and first implementation slice | API/build maintainer | Complete E02/E03 for each consumed capability; retain every unassigned module |
| R03 | Version-specific licensing is a hard source-reuse decision. Inspect selected historical/current tags and notices before derivation. | Product/platform-specific packages | Product architect / platform maintainer | Run the matching feasibility packages; document measured result and alternatives |
| R04 | C# expression trees and flattening conventions need Java equivalents; preserve distinctions from Mapster instead of merging products. | Behavioral/API compatibility | Compatibility maintainer | Resolve precise Java contract and source fixture mapping before each slice |
| R05 | Proposed product dependencies are not ready implementations | Integration packages | Integration maintainer | Freeze neutral contracts, bootstrap independently and split optional adapters |
| R06 | The inspected LICENSE.md offers RPL 1.5 terms or a separate agreement. Earlier MIT history is not clearance for this pin. Source-derived implementation and distribution remain gated on the applicable rights path. | Source reuse / redistribution | Licensing reviewer | Resolve exact version and source/asset obligations; record evidence without implying clearance |

## Decision defaults

Proceed with the architecture and work breakdown above for planning. Do not pause the entire ecosystem because one native backend, license or provider is blocked. Implementation eligibility is assessed per slice. A failed feasibility experiment may lead to an explicit reduced support profile, alternate owned design or continued blocker; it never silently removes the original capability from the inventory. No invented dates or effort estimates are used.
