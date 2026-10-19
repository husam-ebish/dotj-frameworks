# DJ-023 .j JSON: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:66](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L66) | JsonConverter | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:160](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L160) | SerializationGuide | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:196](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L196) | SerializationBasics | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:223](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L223) | SerializationBasics2 | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:250](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L250) | DeserializationBasics1 | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:268](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L268) | DeserializationBasics2 | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:299](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L299) | SerializeReferencesByValue | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:345](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L345) | SerializeReferencesWithMetadata | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:408](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L408) | RoundtripTypesAndReferences | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:522](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L522) | SerializeAttributes | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:558](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L558) | MergeJson | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:601](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L601) | ArrayPooling | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:619](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L619) | SerializeDataTable | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:661](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L661) | JsonPathRegex | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:686](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L686) | AsyncDemo | yes |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:719](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L719) | Return | not confirmed |
| [Src/Newtonsoft.Json.FuzzTests/FuzzTests.cs:10](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.FuzzTests/FuzzTests.cs#L10) | FuzzDeserialization | not confirmed |
| [Src/Newtonsoft.Json.FuzzTests/FuzzTests.cs:28](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.FuzzTests/FuzzTests.cs#L28) | FuzzSerialization | not confirmed |
| [Src/Newtonsoft.Json.FuzzTests/FuzzTests.cs:44](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.FuzzTests/FuzzTests.cs#L44) | FuzzIdempotent | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-023-F01-01 | WP-01 | Split multibyte input parses correctly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F01-02 | WP-01 | malformed numbers fail at stable locations | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F01-03 | WP-01 | configured depth limits prevent exhaustion | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F02-01 | WP-02 | Recursive converter mistakes are detected | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F02-02 | WP-02 | untrusted type names cannot instantiate arbitrary classes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F02-03 | WP-02 | missing/default values follow the chosen profile | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F03-01 | WP-03 | Duplicate property policy is explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F03-02 | WP-03 | deep clones share no mutable children | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F03-03 | WP-03 | invalid query expressions fail without executing host code | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F04-01 | WP-04 | Cycles terminate under declared policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F04-02 | WP-04 | timezone/precision differences are recorded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F04-03 | WP-04 | strict output never emits nonstandard tokens silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F05-01 | WP-05 | Newtonsoft and System.Text.Json expectations are never merged | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F05-02 | WP-05 | every deviation is named | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-023-F05-03 | WP-05 | serialization memory scales with documented buffering policy | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Duplicate properties; precision; malformed Unicode; cyclic graphs; converter recursion; polymorphic type injection; streaming limits.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-023-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-023-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-023-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
