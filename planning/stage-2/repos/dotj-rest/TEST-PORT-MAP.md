# DJ-032 .j REST: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/RestSharp.Tests/OptionsTests.cs:5](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/OptionsTests.cs#L5) | HttpClient_AllowAutoRedirect_Is_Always_False | yes |
| [test/RestSharp.Tests/RestClientTests.cs:18](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L18) | Execute_with_RestRequest_and_Method_overrides_previous_request_method | yes |
| [test/RestSharp.Tests/RestClientTests.cs:28](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L28) | ConfigureHttp_will_set_proxy_to_null_with_no_exceptions_When_no_proxy_can_be_found | yes |
| [test/RestSharp.Tests/RestClientTests.cs:36](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L36) | UseJson_leaves_only_json_serializer | yes |
| [test/RestSharp.Tests/RestClientTests.cs:49](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L49) | UseXml_leaves_only_json_serializer | yes |
| [test/RestSharp.Tests/RestClientTests.cs:62](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L62) | UseOnlySerializer_leaves_only_custom_serializer | yes |
| [test/RestSharp.Tests/RestClientTests.cs:75](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L75) | Should_reuse_httpClient_instance | yes |
| [test/RestSharp.Tests/RestClientTests.cs:83](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L83) | Should_use_new_httpClient_instance | yes |
| [test/RestSharp.Tests/RestClientTests.cs:91](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L91) | ConfigureDefaultParameters_sets_user_agent_new_httpClient_instance | yes |
| [test/RestSharp.Tests/RestClientTests.cs:109](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L109) | ConfigureDefaultParameters_sets_user_agent_given_httpClient_instance | yes |
| [test/RestSharp.Tests/RestClientTests.cs:128](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L128) | Should_not_set_expect_continue_on_shared_http_client_default_headers | yes |
| [test/RestSharp.Tests/RestClientTests.cs:141](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L141) | Should_not_set_expect_continue_on_new_http_client_default_headers | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-032-F01-01 | WP-01 | Reserved characters survive expected encoding | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F01-02 | WP-01 | duplicate headers follow policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F01-03 | WP-01 | concurrent calls do not mutate a shared request unexpectedly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F02-01 | WP-02 | Non-success HTTP can retain its body | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F02-02 | WP-02 | cancellation closes owned streams | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F02-03 | WP-02 | response resources are released on conversion failure | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F03-01 | WP-03 | Binary parts preserve bytes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F03-02 | WP-03 | filenames cannot inject headers | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F03-03 | WP-03 | serializer failure occurs before unsafe automatic retries | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F04-01 | WP-04 | Redirects cannot leak authorization across trust boundaries | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F04-02 | WP-04 | expired cookies are not sent | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F04-03 | WP-04 | failed auth hooks produce diagnosable outcomes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F05-01 | WP-05 | Hook order is deterministic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F05-02 | WP-05 | unsupported overload semantics are recorded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-032-F05-03 | WP-05 | optional integration artifacts do not enter the base client | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Escaping; multipart boundaries; redirects; cookies; streaming downloads; timeout classification; auth header leakage.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-032-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-032-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-032-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
