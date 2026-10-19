# DJ-066 .j Bus: risks and open decisions

| ID | Risk/question | Blocking scope | Owner role | Next action |
|---|---|---|---|---|
| R01 | Analysis pin may not be eligible release | All source-derived implementation | Maintainer / licensing reviewer | Complete E01; record release family and rights; no historical license assumption |
| R02 | Sampled source is not exhaustive API/test/dependency closure | Affected feature claims and first implementation slice | API/build maintainer | Complete E02/E03 for each consumed capability; retain every unassigned module |
| R03 | Version-specific source/license availability and broker client dependencies may block modules. Each transport remains in scope pending an explicit decision. | Product/platform-specific packages | Product architect / platform maintainer | Run the matching feasibility packages; document measured result and alternatives |
| R04 | Broker interoperability is transport-specific; at-least-once delivery and transactional outbox do not imply exactly-once effects. Saga state evolution needs contracts. | Behavioral/API compatibility | Compatibility maintainer | Resolve precise Java contract and source fixture mapping before each slice |
| R05 | Proposed product dependencies are not ready implementations | Integration packages | Integration maintainer | Freeze neutral contracts, bootstrap independently and split optional adapters |
| R06 | The inspected revision contains Apache license text. This observation is specific to the pin and does not establish the terms of every MassTransit release or product. | Source reuse / redistribution | Licensing reviewer | Resolve exact version and source/asset obligations; record evidence without implying clearance |

## Decision defaults

Proceed with the architecture and work breakdown above for planning. Do not pause the entire ecosystem because one native backend, license or provider is blocked. Implementation eligibility is assessed per slice. A failed feasibility experiment may lead to an explicit reduced support profile, alternate owned design or continued blocker; it never silently removes the original capability from the inventory. No invented dates or effort estimates are used.
