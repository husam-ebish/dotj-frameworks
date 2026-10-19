# DJ-008 .j Interactive: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/dotnet-interactive.Tests/HttpApiTests.cs:44](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L44) | Dispose | not confirmed |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:61](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L61) | discovery_route_is_not_registered_without_JupyterFrontedEnvironment | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:74](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L74) | FrontendEnvironment_host_is_set_via_handshake | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:89](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L89) | HttpApiTunneling_configures_frontend_environment | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:105](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L105) | HttpApiTunneling_return_bootstrapper_js_url | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:124](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L124) | HttpApiTunneling_route_serves_bootstrapper_js | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:150](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L150) | can_get_variable_value | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:167](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L167) | can_get_variable_value_when_variable_is_string | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:183](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L183) | deferred_command_produce_html_bootstrap_code | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:204](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L204) | can_get_variables_with_bulk_request | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:244](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L244) | get_variables_preserves_property_case | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:264](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L264) | bulk_variable_request_is_returned_with_application_json_content_type | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:285](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L285) | Variable_serialization_can_be_customized_using_Formatter | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:307](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L307) | variable_is_returned_with_application_json_content_type | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:323](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L323) | When_variable_does_not_exist_then_it_returns_404 | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:332](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L332) | When_subkernel_does_not_exist_then_it_returns_404 | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:341](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L341) | can_get_static_content | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:352](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L352) | can_get_static_content_from_extensions | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:372](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L372) | can_get_kernel_names | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:398](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L398) | stdio_mode_returns_javascript_api_via_http | yes |
| [src/dotnet-interactive.Tests/HttpApiTests.cs:435](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/HttpApiTests.cs#L435) | ShouldSucceed | not confirmed |
| [src/dotnet-interactive.Tests/FileProviderTests.cs:21](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/dotnet-interactive.Tests/FileProviderTests.cs#L21) | It_loads_content_from_root_provider | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-008-F01-01 | WP-01 | Every accepted command has one terminal outcome | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F01-02 | WP-01 | output cannot impersonate a protocol event | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F01-03 | WP-01 | cancellation is correlated to the right cell | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F02-01 | WP-02 | Redefinition matches documented JShell limitations | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F02-02 | WP-02 | interrupt preserves or explicitly resets state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F02-03 | WP-02 | worker failure does not kill notebook host | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F03-01 | WP-03 | Unknown metadata survives round trip | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F03-02 | WP-03 | malicious display output cannot execute in trusted host context | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F03-03 | WP-03 | binary outputs retain bytes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F04-01 | WP-04 | A package conflict leaves prior session usable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F04-02 | WP-04 | missing external kernels produce capability errors | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F04-03 | WP-04 | no existing Java notebook framework is substituted | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F05-01 | WP-05 | Malformed signatures are rejected | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F05-02 | WP-05 | heartbeat survives long cells | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F05-03 | WP-05 | shutdown removes secrets and endpoints | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-008-F05-04 | WP-05 | transport feasibility remains gated until demonstrated | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Cell execution order; interrupted evaluation; stdout isolation; notebook round trips; kernel restart and package conflicts.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
