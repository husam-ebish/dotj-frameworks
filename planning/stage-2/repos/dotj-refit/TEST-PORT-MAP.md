# DJ-033 .j Refit: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/tests/Refit.Tests/ResponseTests.cs:97](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/ResponseTests.cs#L97) | JsonPropertyCanBeUsedToAliasFieldNamesInResponses | yes |
| [src/tests/Refit.Tests/ResponseTests.cs:113](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/ResponseTests.cs#L113) | AliasAsCannotBeUsedToAliasFieldNamesInResponses | yes |
| [src/tests/Refit.Tests/ResponseTests.cs:126](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/ResponseTests.cs#L126) | ThrowsValidationException | yes |
| [src/tests/Refit.Tests/ResponseTests.cs:160](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/ResponseTests.cs#L160) | ValidationApiExceptionPropagatesContentHeaders | yes |
| [src/tests/Refit.Tests/ResponseTests.cs:185](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/ResponseTests.cs#L185) | ValidationApiExceptionUsesConfiguredContentSerializer | yes |
| [src/tests/Refit.Tests/ResponseTests.cs:205](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/ResponseTests.cs#L205) | When_BadRequest_EnsureSuccessStatusCodeAsync_ThrowsValidationException | yes |
| [src/tests/Refit.Tests/ResponseTests.cs:240](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/ResponseTests.cs#L240) | WhenProblemDetailsResponseContainsExtensions_ShouldHydrateExtensions | yes |
| [src/tests/Refit.Tests/ResponseTests.cs:277](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/ResponseTests.cs#L277) | WithNonSeekableStream_UsingSystemTextJsonContentSerializer | yes |
| [src/tests/Refit.Tests/ResponseTests.cs:320](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/ResponseTests.cs#L320) | DeserializationFailureWithNonSeekableStream_PopulatesApiExceptionContent | yes |
| [src/tests/Refit.Tests/ResponseTests.cs:353](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/ResponseTests.cs#L353) | XmlDeserializationWithNonSeekableStream_DoesNotThrowStreamConsumed | yes |
| [src/tests/Refit.Tests/ResponseTests.cs:384](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/ResponseTests.cs#L384) | ValidationApiException_HydratesBaseContent | yes |
| [src/tests/Refit.Tests/MultipartTests.cs:76](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/MultipartTests.cs#L76) | MultipartUploadShouldWorkWithStream | yes |
| [src/tests/Refit.Tests/MultipartTests.cs:105](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/MultipartTests.cs#L105) | MultipartUploadShouldWorkWithStreamAndCustomBoundary | yes |
| [src/tests/Refit.Tests/MultipartTests.cs:142](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/MultipartTests.cs#L142) | MultipartUploadShouldWorkWithByteArray | yes |
| [src/tests/Refit.Tests/MultipartTests.cs:174](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/MultipartTests.cs#L174) | MultipartUploadShouldWorkWithFileInfo | yes |
| [src/tests/Refit.Tests/MultipartTests.cs:242](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/MultipartTests.cs#L242) | MultipartUploadShouldWorkWithString | yes |
| [src/tests/Refit.Tests/MultipartTests.cs:272](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/MultipartTests.cs#L272) | MultipartUploadShouldWorkWithFormattableValues | yes |
| [src/tests/Refit.Tests/MultipartTests.cs:308](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/MultipartTests.cs#L308) | MultipartFormattableValueWithNullFormatterIsEmpty | yes |
| [src/tests/Refit.Tests/MultipartTests.cs:329](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests/Refit.Tests/MultipartTests.cs#L329) | MultipartUploadShouldWorkWithHeaderAndRequestProperty | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-033-F01-01 | WP-01 | Conflicting bindings fail with member location | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F01-02 | WP-01 | inherited methods retain metadata | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F01-03 | WP-01 | unsupported signatures never produce runtime surprises | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F02-01 | WP-02 | Generated and proxy paths produce equivalent requests | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F02-02 | WP-02 | no runtime C# expression/codegen dependency is assumed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F03-01 | WP-03 | Deserialization failure retains HTTP context | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F03-02 | WP-03 | streams close on cancellation | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F03-03 | WP-03 | generic response types remain resolvable after erasure | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F04-01 | WP-04 | Concurrent users cannot share credentials accidentally | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F04-02 | WP-04 | caller transport is not closed by generated clients | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F04-03 | WP-04 | handler failures release request resources | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F05-01 | WP-05 | Base generated clients need only accepted transport contracts | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F05-02 | WP-05 | URI/header fixtures match profile | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-033-F05-03 | WP-05 | no Retrofit replacement supplies the implementation | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Generated request equivalence; inherited interfaces; generic models; multipart; cancellation; status-error decoding.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
