# DJ-005 .j Build: readiness

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Dimension | Status |
|---|---|
| Stage-1 plan | Previously written; retained as historical input |
| Stage-2 written plan | WRITTEN: architecture, capability breakdown, tasks, acceptance, tests and blockers |
| Capability and integration work packages | 7: 5 existing + 2 SDK integration |
| Pinned source evidence | Retrieved tree and sampled source/API/test files |
| Exhaustive semantic upstream analysis | OPEN: E02/E03 closure remains required |
| Eligible release and licensing | OPEN: E01; see repository-specific evidence |
| Implementation eligibility | Conditional per slice; not blanket approval for every capability |
| Implementation | Merged non-exported [internal evaluation candidate](../../../../dotj-build/evaluation-candidate/README.md); public product implementation remains unqualified |
| Java implementation tests | Existing candidate evidence: 20 native comparisons + 23 profile refusals (43 cases); no task/product acceptance |
| Selected compiled lifecycle evidence | [Installed metadata inventory v1](COMPILED-LIFECYCLE-INVENTORY.md): twelve anchors and complete selected overload families; full E02/N01 closure remains OPEN |
| Release readiness | NOT READY |
| Applied to repository | Internal candidate merged at b872dce7; bounded reference evidence retained; no qualified public product |

## What you can do next

Review the bounded compiled lifecycle mapping, then resolve the selected public
dependency/representation and lifecycle gaps alongside E01-E03/N01 before public
promotion. The merged candidate is internal evidence for selected property/import
behavior. Its existing 43-case evidence is reused because this inventory changes
no candidate source, runtime or runner. No accepted task or numbered batch credit
is added. Native/mobile/browser and rights-dependent packages remain gated where
specified.

## Exact-name requirement

Owner decision: fixed for all public API/concept surfaces. N01 semantic name mapping and language-gap closure: OPEN per slice. Exact-name implementation/conformance: NOT STARTED. This policy update does not pretend all upstream declarations have already been mapped or compiled.

## Detailed SDK integration requirement

[DOTNET-SDK-EXPERIENCE-001](../../10-SDK-AND-DISTRIBUTION-PLAN.md) supplements this repository's existing feature work. The detailed [integration tasks and acceptance cases](../../sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md) are mandatory, all NOT STARTED as implementation. Their task IDs also appear in the global machine-readable backlogs.

- `SDK-I02`: Independent JDK bootstrap and minimal launcher; five named tasks and five designed cases in the integration plan.
- `SDK-I03`: SDK-style project evaluation and solutions; five named tasks and five designed cases in the integration plan.

These are integration packages, not a replacement for source-derived E01-E03/N01 mapping. The detailed specifications take precedence over earlier generic SDK/distribution proposals; blocked platform/language/rights features remain blocked.
