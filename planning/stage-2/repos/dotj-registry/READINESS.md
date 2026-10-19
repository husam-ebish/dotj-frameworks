# DJ-063 .j Registry: readiness

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Dimension | Status |
|---|---|
| Stage-1 plan | Previously written; retained as historical input |
| Stage-2 written plan | WRITTEN: architecture, capability breakdown, tasks, acceptance, tests and blockers |
| Capability and integration work packages | 6: 5 existing + 1 SDK integration |
| Pinned source evidence | Retrieved tree and sampled source/API/test files |
| Exhaustive semantic upstream analysis | OPEN: E02/E03 closure remains required |
| Eligible release and licensing | OPEN: E01; see repository-specific evidence |
| Implementation eligibility | Conditional per slice; not blanket approval for every capability |
| Implementation | NOT STARTED by this planning task |
| Java implementation tests | NOT RUN; no implementation exists in this package |
| Release readiness | NOT READY |
| Applied to your Windows/Azure DevOps repository | No; this is a downloadable planning update |

## What you can do next

Commit the planning package and use E01-E03 plus WP-01 to begin the first selected implementation slice once its prerequisites are resolved and implementation is requested. You do not need another planning turn merely to obtain the remaining repositories: all 66 written plans are included. Native/mobile/browser and rights-dependent packages stay gated where specified. A written plan is not evidence that all upstream behavior is already audited or implemented.

## Exact-name requirement

Owner decision: fixed for all public API/concept surfaces. N01 semantic name mapping and language-gap closure: OPEN per slice. Exact-name implementation/conformance: NOT STARTED. This policy update does not pretend all upstream declarations have already been mapped or compiled.

## Detailed SDK integration requirement

[DOTNET-SDK-EXPERIENCE-001](../../10-SDK-AND-DISTRIBUTION-PLAN.md) supplements this repository's existing feature work. The detailed [integration tasks and acceptance cases](../../sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md) are mandatory, all NOT STARTED as implementation. Their task IDs also appear in the global machine-readable backlogs.

- `SDK-I10`: Hosted feed protocol and immutable distribution; five named tasks and five designed cases in the integration plan.

These are integration packages, not a replacement for source-derived E01-E03/N01 mapping. The detailed specifications take precedence over earlier generic SDK/distribution proposals; blocked platform/language/rights features remain blocked.
