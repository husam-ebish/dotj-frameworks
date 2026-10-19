# DJ-061 .j Semantic: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [dotnet/src/IntegrationTests/PromptTests.cs:40](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/IntegrationTests/PromptTests.cs#L40) | GenerateStoryTestAsync | yes |
| [dotnet/src/IntegrationTests/PromptTests.cs:69](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/IntegrationTests/PromptTests.cs#L69) | Dispose | not confirmed |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:31](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L31) | ItProvidesAccessToFunctionsViaFunctionCollection | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:45](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L45) | InvokeAsyncDoesNotRunWhenCancelledAsync | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:59](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L59) | InvokeAsyncRunsWhenNotCancelledAsync | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:75](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L75) | ItImportsPluginsNotCaseSensitive | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:88](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L88) | ItAllowsToImportTheSamePluginMultipleTimes | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:101](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L101) | ItReturnsFunctionResultsCorrectlyAsync | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:117](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L117) | ItCanFindAndRunFunctionAsync | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:134](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L134) | ItShouldBePossibleToSetAndGetCultureAssociatedWithKernel | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:149](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L149) | ItDefaultsLoggerFactoryToNullLoggerFactory | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:159](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L159) | ItDefaultsDataToEmptyDictionary | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:169](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L169) | ItDefaultsPluginsToEmptyCollection | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:179](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L179) | InvariantCultureShouldBeReturnedIfNoCultureWasAssociatedWithKernel | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:192](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L192) | ItDeepClonesAllRelevantStateInClone | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:236](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L236) | InvokeStreamingAsyncCallsConnectorStreamingApiAsync | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:262](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L262) | InvokeStreamingAsyncCallsWithMEAIContentsAndChatCompletionApiAsync | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:291](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L291) | InvokeStreamingAsyncGenericPermutationsCallsConnectorChatClientAsync | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:366](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L366) | ValidateInvokeAsync | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:381](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L381) | ValidateInvokePromptAsync | yes |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:486](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L486) | ReadFunctionCollectionAsync | not confirmed |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:495](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L495) | OnFunctionInvocationAsync | not confirmed |
| [dotnet/src/SemanticKernel.UnitTests/KernelTests.cs:503](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/src/SemanticKernel.UnitTests/KernelTests.cs#L503) | OnPromptRenderAsync | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-061-F01-01 | WP-01 | Plugin names/signatures validate before use | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F01-02 | WP-01 | C# coverage is not inferred from existing Java implementation | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F01-03 | WP-01 | invocation errors retain function context | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F02-01 | WP-02 | Partial streams retain terminal failure information | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F02-02 | WP-02 | malformed tool arguments fail validation | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F02-03 | WP-02 | unavailable provider features are explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F03-01 | WP-03 | Model output cannot grant new tool permissions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F03-02 | WP-03 | prompt rendering preserves declared encoding | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F03-03 | WP-03 | loops terminate at configured budgets | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F04-01 | WP-04 | Tenant data cannot cross query context | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F04-02 | WP-04 | process retries expose possible duplicate side effects | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F04-03 | WP-04 | successor-only features are not attributed to the inspected repo | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F05-01 | WP-05 | Offline tests require no paid provider | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F05-02 | WP-05 | live checks record model/API versions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-061-F05-03 | WP-05 | no existing Java Semantic Kernel is used as implementation foundation | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Scripted model responses; tool-call validation; cancellation; streaming; prompt injection boundaries; secret redaction.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
