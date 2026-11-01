# DJ-005 dotj-build: exact API and concept compatibility

Policy: [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md). This is the required public API direction for MSBuild; generic workstream names in earlier architecture drafts are internal only.

## Required behavior

Use the selected upstream profile's exact class/interface/member names and casing, preserve namespace identity and generic/overload families, and keep the same concepts and lifecycle. Do not replace this product's API with Java-style names or a newly designed facade vocabulary. JDK primitives remain implementation details or optional interop. Examples must remain recognizable to developers who already know MSBuild.

## Source identity and ledger

Source: https://github.com/dotnet/msbuild

Revision: `6348d0c087aeec18c323b01a2c77da089ddafea0`

The [naming ledger](evidence/naming-ledger.json) retains 155 lexical production declaration candidates. These are source navigation anchors, not a completed or semantically verified API map. E02 and N01 must resolve generated/conditional APIs, namespaces, declaring types, overloads, generic arities, accessors and behavior before any public symbol is frozen. No type is renamed because the sample did not contain its full declaration.

## N01 tasks

The [selected compiled lifecycle inventory](COMPILED-LIFECYCLE-INVENTORY.md)
adds installed SDK 10.0.401 / MSBuild 18.9.11 metadata evidence for the twelve
Project/ProjectCollection prerequisite anchors and their overload families.
Its component pin is retained separately from the historical analysis revision
above. The separate [lifecycle/representation qualification](LIFECYCLE-REPRESENTATION-QUALIFICATION.md)
retains all 45 method/constructor records plus two separate accessors, two property
descriptors and 24 direct identities. Every row has an explicit profile disposition
and BLOCKED exact representation; nonpublic/internal records remain nonpublic.
Eight independently designed file-based scenarios agree across two fresh native
passes under the pinned installed profile. This establishes that finite reference
contract, while broader lifecycle/configuration coverage, recursive dependency
closure, actual Java/core/.j representations and the full N01 tasks remain OPEN.
No public facade, paired compiled .j examples, task acceptance or numbered credit
is supplied by this prerequisite evidence.

1. `DJ-005-N01-T1`: Extract the complete semantic upstream public surface for the selected slice, preserving exact namespace/type/member spelling, casing, overloads, generic arity, parameter identities and property/event metadata.
1. `DJ-005-N01-T2`: Map each symbol and concept to a faithful Java representation; move invented helper vocabulary behind the public facade; record Java language/JVM conflicts without silently renaming or changing behavior.
1. `DJ-005-N01-T3`: Add automated case-sensitive public API comparison and concept-behavior fixtures, including I prefixes, Async suffixes, enum values, configuration/markup names and generated members.
1. `DJ-005-N01-T4`: Provide paired C# and .j usage examples with the same public names, lifecycle and workflow; identify unavoidable syntax differences and keep unsupported exact APIs explicitly blocked.

## Acceptance cases

- `DJ-005-NF01`: Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced.
- `DJ-005-NF02`: Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts.
- `DJ-005-NF03`: Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility.

## Integration gate

Prerequisites: the applicable E01 eligibility and E02 semantic source slice. N01 contract mapping and proposed API validation must be complete before implementation of that public slice; the compiled-surface comparison and behavior tests must pass before merging or advertising it. N01 does not require all other repositories to be finished first. The exact-name intent is decided; only source mapping and technical feasibility remain open.

CLI/image-only workstreams apply the rule to command/options/configuration concepts and generated public surfaces where present; do not invent a Java class API solely to satisfy this gate.
