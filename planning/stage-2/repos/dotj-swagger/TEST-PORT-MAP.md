# DJ-036 .j Swagger: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:11](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L11) | Can_Output_Swagger_Document_Names | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:25](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L25) | Throws_When_Startup_Assembly_Does_Not_Exist | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:35](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L35) | Error_When_OpenApiVersion_Is_Not_Supported | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:51](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L51) | Can_Generate_Swagger_Json_v2_OpenApiVersion | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:73](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L73) | Can_Generate_Swagger_Json_v3 | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:93](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L93) | Can_Generate_Swagger_Json_v3_1 | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:115](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L115) | Can_Generate_Swagger_Json_v3_OpenApiVersion | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:137](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L137) | Can_Generate_Swagger_Json_With_Async_Operation_Filters | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:163](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L163) | Overwrites_Existing_File | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:188](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L188) | CustomDocumentSerializer_Writes_Custom_V2_Document | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:207](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L207) | CustomDocumentSerializer_Writes_Custom_V3_Document | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:225](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L225) | CustomDocumentSerializer_Writes_Custom_V3_1_Document | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:245](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L245) | Can_Generate_Swagger_Json_ForTopLevelApp | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:265](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L265) | Does_Not_Run_Crashing_HostedService | yes |
| [test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs:283](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.Cli.Test/ToolTests.cs#L283) | Creates_New_Folder_Path | yes |
| [test/Swashbuckle.AspNetCore.IntegrationTests/UITests.cs:9](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.IntegrationTests/UITests.cs#L9) | Can_Load_SwaggerUI_Page_And_Make_Request | yes |
| [test/Swashbuckle.AspNetCore.IntegrationTests/UITests.cs:32](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.IntegrationTests/UITests.cs#L32) | Can_Load_Redoc_Page | yes |
| [test/Swashbuckle.AspNetCore.IntegrationTests/UITests.cs:45](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/test/Swashbuckle.AspNetCore.IntegrationTests/UITests.cs#L45) | Relative_Document_Url_Does_Not_Inherit_Query_String_From_Page_Url | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-036-F01-01 | WP-01 | Recursive types terminate via references | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F01-02 | WP-01 | same-simple-name classes do not collide silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F01-03 | WP-01 | ignored endpoints stay excluded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F02-01 | WP-02 | Filter failure identifies its source | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F02-02 | WP-02 | multiple documents do not share mutable schemas | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F02-03 | WP-02 | extensions survive serialization | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F03-01 | WP-03 | Private docs require configured access | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F03-02 | WP-03 | UI assets have provenance and pinned checksums | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F03-03 | WP-03 | untrusted document URLs cannot bypass access policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F04-01 | WP-04 | Document groups match routing version metadata | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F04-02 | WP-04 | security declarations do not masquerade as enforcement | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F04-03 | WP-04 | invalid examples are reported | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F05-01 | WP-05 | Each advertised generator behavior has fixtures | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F05-02 | WP-05 | reverse-proxy base paths remain valid | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-036-F05-03 | WP-05 | no existing Java Swagger generator replaces implementation | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Nullable schemas; recursive models; operation IDs; security definitions; filters; generated document validation and UI CSP.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-036-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-036-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-036-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
