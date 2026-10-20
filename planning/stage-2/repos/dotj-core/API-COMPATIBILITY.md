# DJ-001 dotj-core: exact API and concept compatibility

Policy: [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md). This is the required public API direction for .NET runtime and base libraries; generic workstream names in earlier architecture drafts are internal only.

## Required behavior

Use the selected upstream profile's exact class/interface/member names and casing, preserve namespace identity and generic/overload families, and keep the same concepts and lifecycle. Do not replace this product's API with Java-style names or a newly designed facade vocabulary. JDK primitives remain implementation details or optional interop. Examples must remain recognizable to developers who already know .NET runtime and base libraries.

## Source identity and ledger

Source: https://github.com/dotnet/runtime

Revision: `9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819`

The [naming ledger](evidence/naming-ledger.json) retains 187 lexical production declaration candidates. These are source navigation anchors, not a completed or semantically verified API map. E02 and N01 must resolve generated/conditional APIs, namespaces, declaring types, overloads, generic arities, accessors and behavior before any public symbol is frozen. No type is renamed because the sample did not contain its full declaration.

The original lexical inventory above uses the analysis revision. The bounded release-profile [N01 selected-method ledger](evidence/n01-selected-methods-v10.0.12.json) instead checks 99 distinct declared-public method signatures across nine async and cancellation types against installed .NET 10.0.12 CoreLib metadata (SHA-256 `1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678`) and owning source-file hashes at commit `4271d88e0aebf3d04f188f1334c2220d80555ef6`. This is a selected metadata inventory: it does not attribute each member to a source line, establish all inherited or conditional APIs, decide the Java generic-arity collision, or qualify public behavior. [The 100-point schedule](../../implementation/N01-100-POINTS.json) and [series audit](../../implementation/batches/Batch-400.md) retain the bounded scope.

## N01 tasks

1. `DJ-001-N01-T1`: Extract the complete semantic upstream public surface for the selected slice, preserving exact namespace/type/member spelling, casing, overloads, generic arity, parameter identities and property/event metadata.
1. `DJ-001-N01-T2`: Map each symbol and concept to a faithful Java representation; move invented helper vocabulary behind the public facade; record Java language/JVM conflicts without silently renaming or changing behavior.
1. `DJ-001-N01-T3`: Add automated case-sensitive public API comparison and concept-behavior fixtures, including I prefixes, Async suffixes, enum values, configuration/markup names and generated members.
1. `DJ-001-N01-T4`: Provide paired C# and .j usage examples with the same public names, lifecycle and workflow; identify unavoidable syntax differences and keep unsupported exact APIs explicitly blocked.

## Acceptance cases

- `DJ-001-NF01`: Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced.
- `DJ-001-NF02`: Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts.
- `DJ-001-NF03`: Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility.

## Integration gate

Prerequisites: the applicable E01 eligibility and E02 semantic source slice. N01 contract mapping and proposed API validation must be complete before implementation of that public slice; the compiled-surface comparison and behavior tests must pass before merging or advertising it. N01 does not require all other repositories to be finished first. The exact-name intent is decided; only source mapping and technical feasibility remain open.

CLI/image-only workstreams apply the rule to command/options/configuration concepts and generated public surfaces where present; do not invent a Java class API solely to satisfy this gate.
