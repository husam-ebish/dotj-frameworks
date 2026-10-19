# DJ-039 .j GraphQL: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/GraphQL.ApiTests/BomTests.cs:9](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.ApiTests/BomTests.cs#L9) | Files_Should_Not_Use_BOM | yes |
| [src/GraphQL.Tests/AuthorizationTests.cs:8](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L8) | Field | yes |
| [src/GraphQL.Tests/AuthorizationTests.cs:29](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L29) | NoRoles | yes |
| [src/GraphQL.Tests/AuthorizationTests.cs:40](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L40) | AllowAnonymous | yes |
| [src/GraphQL.Tests/AuthorizationTests.cs:49](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L49) | Authorize | yes |
| [src/GraphQL.Tests/AuthorizationTests.cs:58](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L58) | FieldBuilder | yes |
| [src/GraphQL.Tests/AuthorizationTests.cs:78](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L78) | ConnectionBuilder | yes |
| [src/GraphQL.Tests/AuthorizationTests.cs:98](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L98) | AutoOutputGraphType | yes |
| [src/GraphQL.Tests/AuthorizationTests.cs:124](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L124) | SchemaBuilder | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-039-F01-01 | WP-01 | Malformed documents have stable spans | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F01-02 | WP-01 | invalid schemas fail before execution | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F01-03 | WP-01 | scalar coercion is defined for literals and variables | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F02-01 | WP-02 | Omitted and explicit-null inputs differ correctly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F02-02 | WP-02 | fragment cycles fail | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F02-03 | WP-02 | stale schema plans cannot execute silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F03-01 | WP-03 | Errors retain field/index paths | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F03-02 | WP-03 | non-null violations bubble correctly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F03-03 | WP-03 | internal stack traces are hidden unless explicitly enabled | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F04-01 | WP-04 | Disconnect closes subscriptions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F04-02 | WP-04 | cache entries cannot leak across requests | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F04-03 | WP-04 | core executor needs no web framework | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F05-01 | WP-05 | Claims identify exact specification/profile | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F05-02 | WP-05 | expensive requests are bounded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-039-F05-03 | WP-05 | no graphql-java substitution implements the port | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Validation rules; variable coercion; directives; error paths; non-null propagation; query complexity and cancellation.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-039-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-039-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-039-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
