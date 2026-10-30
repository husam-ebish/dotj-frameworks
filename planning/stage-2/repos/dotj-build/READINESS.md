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
| Java implementation tests | Existing current-master receipt: 94 unique packaged comparisons; reused with unchanged product/runner/input hashes; no task/product acceptance |
| Selected compiled lifecycle evidence | [Installed metadata inventory v1](COMPILED-LIFECYCLE-INVENTORY.md): twelve anchors and complete selected overload families; full E02/N01 closure remains OPEN |
| Selected lifecycle/representation qualification | [Finite qualification v1](LIFECYCLE-REPRESENTATION-QUALIFICATION.md): all 47 retained callables, two properties and 24 identities accounted for; eight designed native scenarios agree across two fresh passes; exact representations remain BLOCKED |
| Release readiness | NOT READY |
| Applied to repository | Internal candidate unchanged from synchronized base a1ef50ef; bounded lifecycle/representation evidence added; no qualified public product |

## What you can do next

Use the [bounded lifecycle contract and representation dispositions](LIFECYCLE-REPRESENTATION-QUALIFICATION.md)
to resolve the consumed shared-core/.j representations and remaining E01-E03/N01
gates before public promotion. The reference observations cover selected file-based
Project/ProjectCollection behavior; the internal candidate still has no approved
public facade for that contract. Its existing 94-comparison receipt is reused with
unchanged product, module, tests, runner and fixture hashes. These eight lifecycle
scenarios are a separate evidence set and add no candidate comparison, accepted
task or numbered batch credit. Rights, recursive dependency closure, paired compiled
C#/.j examples and broader SDK/platform behavior remain OPEN.

## Exact-name requirement

Owner decision: fixed for all public API/concept surfaces. N01 semantic name mapping and language-gap closure: OPEN per slice. Exact-name implementation/conformance: NOT STARTED. This policy update does not pretend all upstream declarations have already been mapped or compiled.

## Detailed SDK integration requirement

[DOTNET-SDK-EXPERIENCE-001](../../10-SDK-AND-DISTRIBUTION-PLAN.md) supplements this repository's existing feature work. The detailed [integration tasks and acceptance cases](../../sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md) are mandatory, all NOT STARTED as implementation. Their task IDs also appear in the global machine-readable backlogs.

- `SDK-I02`: Independent JDK bootstrap and minimal launcher; five named tasks and five designed cases in the integration plan.
- `SDK-I03`: SDK-style project evaluation and solutions; five named tasks and five designed cases in the integration plan.

These are integration packages, not a replacement for source-derived E01-E03/N01 mapping. The detailed specifications take precedence over earlier generic SDK/distribution proposals; blocked platform/language/rights features remain blocked.
