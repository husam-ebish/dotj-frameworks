# DJ-043 .j Avalonia: risks and open decisions

| ID | Risk/question | Blocking scope | Owner role | Next action |
|---|---|---|---|---|
| R01 | Analysis pin may not be eligible release | All source-derived implementation | Maintainer / licensing reviewer | Complete E01; record release family and rights; no historical license assumption |
| R02 | Sampled source is not exhaustive API/test/dependency closure | Affected feature claims and first implementation slice | API/build maintainer | Complete E02/E03 for each consumed capability; retain every unassigned module |
| R03 | Skia/HarfBuzz/native window dependencies and optional commercial backends need exact provenance. Backend list must follow inspected release. | Product/platform-specific packages | Product architect / platform maintainer | Run the matching feasibility packages; document measured result and alternatives |
| R04 | Preserve layout/style selector and binding behavior; original compiled bindings and renderer internals need Java adaptations. | Behavioral/API compatibility | Compatibility maintainer | Resolve precise Java contract and source fixture mapping before each slice |
| R05 | Proposed product dependencies are not ready implementations | Integration packages | Integration maintainer | Freeze neutral contracts, bootstrap independently and split optional adapters |
| R06 | Root licence.md contains MIT text; NOTICE contains separate third-party notices. Root license alone does not clear fonts, native binaries, Skia/HarfBuzz, optional commercial backends or all assets. | Source reuse / redistribution | Licensing reviewer | Resolve exact version and source/asset obligations; record evidence without implying clearance |

## Decision defaults

Proceed with the architecture and work breakdown above for planning. Do not pause the entire ecosystem because one native backend, license or provider is blocked. Implementation eligibility is assessed per slice. A failed feasibility experiment may lead to an explicit reduced support profile, alternate owned design or continued blocker; it never silently removes the original capability from the inventory. No invented dates or effort estimates are used.
