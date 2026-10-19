# DJ-037 .j OpenAPI: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/NSwag.Core.Tests/HttpLoadingTests.cs:8](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/HttpLoadingTests.cs#L8) | When_Swagger_is_loaded_from_url_then_it_works | yes |
| [src/NSwag.Core.Tests/HttpLoadingTests.cs:21](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/HttpLoadingTests.cs#L21) | When_Swagger_is_loaded_from_url_schematype_is_Swagger2 | yes |
| [src/NSwag.Core.Tests/HttpLoadingTests.cs:34](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/HttpLoadingTests.cs#L34) | When_openapi_is_loaded_without_scopes_it_should_deserialize | yes |
| [src/NSwag.Core.Tests/HttpLoadingTests.cs:48](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/HttpLoadingTests.cs#L48) | When_OpenApi_is_loaded_from_url_schematype_is_OpenApi3 | yes |
| [src/NSwag.Core.Tests/OperationIdTests.cs:8](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/OperationIdTests.cs#L8) | When_generating_operation_ids_then_all_are_set | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-037-F01-01 | WP-01 | Round trips preserve extensions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F01-02 | WP-01 | version-specific keywords are validated | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F01-03 | WP-01 | incompatible dialect fields are not silently rewritten | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F02-01 | WP-02 | Malformed input yields path/location diagnostics | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F02-02 | WP-02 | JSON output is deterministic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F02-03 | WP-02 | YAML support is not claimed before parser evidence exists | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F03-01 | WP-03 | Recursive schemas terminate without losing references | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F03-02 | WP-03 | untrusted documents cannot fetch arbitrary local files | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F03-03 | WP-03 | changed content invalidates cache | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F04-01 | WP-04 | Duplicate/missing operation constraints are diagnosed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F04-02 | WP-04 | conversion lists dropped semantics | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F04-03 | WP-04 | validation never repairs a document invisibly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F05-01 | WP-05 | Formatting-only changes do not count as semantic breaks | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F05-02 | WP-05 | unresolved references remain visible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F05-03 | WP-05 | no Swagger UI assets are folded into this model library | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F06-01 | WP-06 | Recursive schema generation terminates | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F06-02 | WP-06 | processor errors retain source identity | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F06-03 | WP-06 | owned schema scope is not claimed to exist just because the NSwag repo references it | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F07-01 | WP-07 | Generated Java/TypeScript samples compile with locked toolchains | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F07-02 | WP-07 | unsupported C# generation capabilities remain inventoried | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F07-03 | WP-07 | runtime-specific annotations are not emitted accidentally | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F08-01 | WP-08 | CLI generation needs no desktop runtime | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F08-02 | WP-08 | configs reproduce outputs | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-037-F08-03 | WP-08 | Studio remains a visible feasibility gate rather than being omitted from scope | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Reference resolution; cyclic schemas; allOf/oneOf; enums; generated-client compilation; deterministic output.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-037-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-037-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-037-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
