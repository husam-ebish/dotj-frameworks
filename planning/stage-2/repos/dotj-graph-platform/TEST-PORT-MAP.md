# DJ-038 .j Graph Platform: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:6](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L6) | EqualsErrorValue | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:20](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L20) | EqualsDifferentError | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:34](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L34) | EqualsSameError | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:47](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L47) | EqualsDifferentValue | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:61](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L61) | EqualsSameValue | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:74](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L74) | EqualsObjectNull | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:87](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L87) | EqualsObjectNotEqual | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:101](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L101) | EqualsObjectValueNotEqual | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:115](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L115) | EqualsObjectValueEqual | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:129](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L129) | GetHashCodeEmpty | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:141](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L141) | GetHashCodeValue | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:155](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L155) | GetHashCodeError | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:169](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L169) | ImplicitRejectErrorIsNull | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:182](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L182) | ImplicitReject | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:198](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L198) | ExplicitReject | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:216](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L216) | ImplicitResolve | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:230](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L230) | ExplicitResolve | yes |
| [src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs:242](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/GreenDonut/test/GreenDonut.Tests/ResultTests.cs#L242) | ExplicitResolveList | yes |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:27](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L27) | Saga_Should_ExecuteThroughSteps | yes |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:109](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L109) | Saga_Should_Timeout | yes |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:161](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L161) | Saga_Should_TimeoutWithCustomResponse | yes |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:213](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L213) | Saga_Should_ReceiveReply_When_SendUsedWithOnAnyReply | yes |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:277](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L277) | Saga_Should_ReceiveReply_When_SendUsedWithTypedOnReply | yes |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:339](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L339) | Sagas_Should_EachOwnTheirReply_When_TwoSagasUseOnAnyReply | yes |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:402](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L402) | RpcReply_Should_NotSelectSaga_When_SameResponseTypeRequestedDirectly | yes |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:429](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L429) | Saga_Should_ReceiveFault_When_SendUsedWithOnFault | yes |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:459](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L459) | Bus_Should_RoundTripReply_When_RequestAsyncUsedDirectly | yes |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:691](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L691) | HandleAsync | not confirmed |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:700](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L700) | HandleAsync | not confirmed |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:709](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L709) | HandleAsync | not confirmed |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:718](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L718) | HandleAsync | not confirmed |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:728](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L728) | HandleAsync | not confirmed |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:741](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L741) | HandleAsync | not confirmed |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:755](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L755) | HandleAsync | not confirmed |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:776](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L776) | Record | not confirmed |
| [src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs:782](https://github.com/ChilliCream/graphql-platform/blob/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c/src/Mocha/test/Mocha.Sagas.Tests/IntegrationTests.cs#L782) | WaitAsync | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-038-F01-01 | WP-01 | Every source product family has a target owner | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F01-02 | WP-01 | independent executors do not silently share incompatible semantics | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F01-03 | WP-01 | parser errors retain source spans | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F02-01 | WP-02 | N+1 fixtures show intended batching | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F02-02 | WP-02 | loader caches do not cross users | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F02-03 | WP-02 | non-null failures propagate to the correct parent | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F03-01 | WP-03 | Unknown persisted IDs cannot bypass validation | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F03-02 | WP-03 | disconnected subscriptions release resources | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F03-03 | WP-03 | protocol-specific error behavior is tested | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F04-01 | WP-04 | Conflicting field ownership fails composition | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F04-02 | WP-04 | gateway cannot forward caller credentials beyond policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F04-03 | WP-04 | partial errors preserve service context | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F05-01 | WP-05 | Invalid operations fail generation | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F05-02 | WP-05 | union handling is exhaustive by profile | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-038-F05-03 | WP-05 | generated sources compile without reusing an existing Java GraphQL client | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

GraphQL specification cases; null bubbling; batched loading; subscription cancellation; federation plans; client cache normalization.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-038-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-038-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-038-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
