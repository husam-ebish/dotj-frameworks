# Mandatory .NET names and concepts policy

Policy ID: DOTNET-API-EXACT-001. Owner decision: 2026-10-19. Applies to all 66 repositories, every public API, generated API, documentation example and compatibility profile.

## Product objective

C#/.NET developers must recognize and use their existing framework knowledge when working in .j on Java. Preserve the original concepts, public names, casing, roles and workflows. Do not redesign the public API to follow Java naming conventions or require a parallel framework vocabulary. The target is minimal additional learning caused by the framework. Standard Java still has language differences from C#; this policy does not claim that unchanged C# source compiles with javac.

## Binding public-surface rules

1. Preserve exact upstream class, struct/type, interface, delegate, enum and member names, including casing, `I` interface prefixes, `Async` suffixes and generic type parameter names where expressible. The selected immutable upstream profile is the authority. Preserve a struct's name and value-type concept; JVM representation and copy/equality semantics require explicit analysis.
2. Preserve exact method names and overload families. `SaveChangesAsync`, `AddSingleton`, `Where`, `Select`, `Cancel`, `Dispose` and `ThrowIfCancellationRequested` must not be converted to lowerCamelCase or renamed for taste. Retain parameter names/order/default semantics where the representation supports them; language gaps must be mapped explicitly.
3. Preserve public namespace identity and casing as Java package identity where legal and technically possible. For example a supported `System.Threading.CancellationToken` belongs to the corresponding exact public namespace/package, not an automatically renamed `org.dotj.core.CancellationToken`. Artifact coordinates, repository names, JPMS module names and product branding remain .j-owned and distinct. Conflicting package/type layouts or JPMS split-package constraints are blockers to solve, not permission to rename silently.
4. Preserve concepts and lifecycle: DbContext/DbSet/change tracking/SaveChanges, DI service registrations and scopes, middleware ordering, controllers/actions, LINQ deferred execution, Task/ValueTask, cancellation and IDisposable/IAsyncDisposable must remain recognizable with their actual upstream behavior. Matching spelling with different behavior is not compatibility.
5. Preserve the original public Task, ValueTask, collection, delegate, exception, type/reflection and disposal vocabulary wherever the selected API exposes it. JDK CompletionStage, AutoCloseable, Class/TypeToken, executors and buffers may implement internals or appear in a clearly separated Java interop module. They must not silently replace .NET public types or introduce required new framework concepts into ordinary examples. Any new compatibility facade has the same upstream public name and its own verified semantics.
6. Preserve original configuration keys, enum member values, attribute names, markup/component names, option names, command/subcommand concepts and file-format identifiers for supported features. Packaging/runtime-specific syntax is a documented boundary. The .j launcher/product name is project branding; it does not authorize arbitrary renaming of familiar operations underneath.
7. Do not add a second Java-style spelling as the canonical API. Do not strip `I`, replace `Dispose` with `close`, shorten CancellationTokenSource to CancellationSource, rename DateTime to DotjDateTime, replace DbContext with a new domain name, or advertise a helper IR/TypeToken as the normal user vocabulary. Optional bridges are not the primary learning path.
8. Existing architecture vocabulary tables were planning labels, not a verified upstream public API census. Treat unverified names as internal workstream labels only. Export only source-verified upstream public identities after N01 mapping. Internal helper names may follow Java conventions because users do not need to learn them.

## Java language boundaries

Preserve the concept and identifier first; record the smallest necessary syntax representation. These rules are default representations for planning, not invented claims that every overload already compiles.

| C#/.NET feature | Required public concept/name | Java representation or explicit gate |
|---|---|---|
| Ordinary method | Exact original name and casing | Call the same named method; no automatic lowercasing |
| Property | Exact property name, type and read/write semantics | Track as property metadata; use its actual .NET accessor names such as get_Count/set_Count where needed for standard Java syntax; never silently invent a new property concept |
| Event | Exact event/delegate names and subscription semantics | Preserve event metadata and original add_/remove_ accessor identities where a method form is necessary |
| Indexer | Exact metadata name, often Item, and overload/argument order | Original get_Item/set_Item accessor identities where applicable; verify actual source/metadata instead of assuming every indexer is Item |
| IDisposable/IAsyncDisposable | Dispose/DisposeAsync and ownership semantics | AutoCloseable.close is an optional bridge; public async result follows the original ValueTask contract |
| Task/ValueTask and async/await | Original public type/method names and async semantics | Owned compatibility types can wrap JDK machinery internally; C# await syntax requires a separate language-tooling capability and is not promised by standard javac |
| Extension methods | Original declaring class/name/signature and fluent concept | Java static-call representation may be necessary; instance-style generated facades only where semantics can be preserved; unchanged C# extension syntax is not assumed |
| LINQ and expression trees | IEnumerable/IQueryable/Expression and original operator names | Preserve familiar operators and query model; Java lambda-to-expression capture and query syntax are explicit dotj-code feasibility work, not a silent replacement with a newly named query DSL |
| Attributes/delegates/events | Original type/member names and conceptual roles | Java annotations/interfaces/adapters where representable; different language syntax is documented |
| Generics/value types/ref/out/operators | Original names, type identity and semantics | Audit erased overload collisions, generic arity, value copying, by-reference arguments and operator support. Unrepresentable exact APIs remain blocked or explicitly unsupported until resolved; never quietly rename or change meaning |
| Native/mobile/browser runtime | Original platform API names and concepts | Backend execution remains separately gated; matching names do not establish platform support |

A syntax representation is not a waiver of name or behavior fidelity. If the JVM cannot represent an API faithfully with these rules, retain the exact upstream member as blocked, investigate wrappers/generation/compiler support, and record the outcome. Any future deliberate departure must be explicit and must not be described as exact compatibility. Do not require repeated owner answers merely to apply this policy.

## N01: mandatory compatibility mapping gate

For every public symbol in the selected source profile, record: immutable source; namespace; declaring type; symbol kind; exact spelling and casing; generic arity; parameter names/types/order/modifiers/defaults; return type; overload identity; accessibility; property/event/accessor relationships; lifecycle/concept; Java representation; state/exception/ownership differences; required adapter; fixtures; status and blocking reason. Include generated APIs and sample/markup surfaces. A lexical declaration candidate is not a completed semantic mapping.

Permitted statuses: exact-name candidate pending analysis; exact mapping verified; syntax representation verified with exact metadata identity; blocked on JVM/language/backend/rights evidence; explicitly unsupported in a bounded release profile. There is no automatic 'renamed for Java style' status.

Automate case-sensitive comparison of compiler-derived upstream symbols against the proposed Java public surface. Fail on accidental changes to names, namespaces, I prefixes, Async suffixes, member ownership, defaults or enum values. Validate concept behavior with mapped oracle fixtures. Every supported feature requires paired C#/.j examples with the same workflow and names; list only unavoidable syntax differences. No public helper vocabulary may be required without a declared language necessity.

## Supersession and scope

This owner requirement supersedes earlier Stage-1/Stage-2 suggestions to use Java-style public names, put all public APIs under org.dotj, return CompletionStage universally, expose generic helper abstractions as the main API, or replace familiar framework concepts with new IR/DSL vocabulary. Narrow JDK implementation reuse remains allowed internally. Source license and eligibility gates remain unchanged. This policy is a planning correction, not a claim of completed API mapping, legal clearance or implemented compatibility.
