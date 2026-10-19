# DJ-052 .j Mock: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/Moq.Tests/MoqTests.cs:15](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L15) | SetupDoesNotRecordCalls | yes |
| [src/Moq.Tests/MoqTests.cs:25](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L25) | CanRaiseEvents | yes |
| [src/Moq.Tests/MoqTests.cs:52](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L52) | CanRaiseEventsWithArgs | yes |
| [src/Moq.Tests/MoqTests.cs:65](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L65) | CanSetupPropertyViaReturns | yes |
| [src/Moq.Tests/MoqTests.cs:75](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L75) | CanSetupPropertyDirectly | yes |
| [src/Moq.Tests/MoqTests.cs:85](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L85) | CanSetupPropertyTwiceViaReturns | yes |
| [src/Moq.Tests/MoqTests.cs:96](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L96) | CanSetupMethodWithArgumentsViaReturns | yes |
| [src/Moq.Tests/MoqTests.cs:106](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L106) | CanSetupMethodWithDifferentArgumentsViaReturns | yes |
| [src/Moq.Tests/MoqTests.cs:123](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L123) | CanReturnFunction | yes |
| [src/Moq.Tests/MoqTests.cs:141](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L141) | CanReturnAsyncFunction | yes |
| [src/Moq.Tests/MoqTests.cs:151](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L151) | CanReturnAsyncValueFunction | yes |
| [src/Moq.Tests/MoqTests.cs:161](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L161) | ThrowsAsync | yes |
| [src/Moq.Tests/MoqTests.cs:171](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L171) | ThrowsAsyncWithException | yes |
| [src/Moq.Tests/MoqTests.cs:181](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L181) | ThrowsValueAsync | yes |
| [src/Moq.Tests/MoqTests.cs:191](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L191) | ThrowsValueAsyncWithException | yes |
| [src/Moq.Tests/MoqTests.cs:201](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L201) | ThrowsVoidAsync | yes |
| [src/Moq.Tests/MoqTests.cs:211](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L211) | ThrowsVoidAsyncWithException | yes |
| [src/Moq.Tests/MoqTests.cs:221](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L221) | ThrowsValueVoidAsync | yes |
| [src/Moq.Tests/MoqTests.cs:231](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L231) | ThrowsValueVoidAsyncWithException | yes |
| [src/Moq.Tests/MoqTests.cs:241](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L241) | CanReturnFunctionWithArgs | yes |
| [src/Moq.Tests/MoqTests.cs:252](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L252) | CanReturnFunctionWithUntypedArgs | yes |
| [src/Moq.Tests/MoqTests.cs:263](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L263) | CanInvokeCallback | yes |
| [src/Moq.Tests/MoqTests.cs:277](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L277) | CanInvokeTwoCallbacks | yes |
| [src/Moq.Tests/MoqTests.cs:295](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L295) | CanInvokeCallbackAfterReturn | yes |
| [src/Moq.Tests/MoqTests.cs:309](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L309) | ThrowsWithException | yes |
| [src/Moq.Tests/MoqTests.cs:319](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L319) | ThrowsWithExceptionType | yes |
| [src/Moq.Tests/MoqTests.cs:329](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L329) | CanSetupPropertyViaReturnsForStrictMock | yes |
| [src/Moq.Tests/MoqTests.cs:340](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L340) | CanSetupPropertyForStrictMock | yes |
| [src/Moq.Tests/MoqTests.cs:352](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L352) | CanSetupVoidMethod | yes |
| [src/Moq.Tests/MoqTests.cs:362](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L362) | CanAccessMockInfoFromInstance | yes |
| [src/Moq.Tests/MoqTests.cs:374](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L374) | CanAssertInvocations | yes |
| [src/Moq.Tests/MoqTests.cs:394](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L394) | ChangeDefaultValue | yes |
| [src/Moq.Tests/MoqTests.cs:407](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L407) | ChangeBehavior | yes |
| [src/Moq.Tests/MoqTests.cs:422](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L422) | ChangingBehaviorPreservesDefaultValue | yes |
| [src/Moq.Tests/MockTests.cs:15](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L15) | CreatesMockForSetup | yes |
| [src/Moq.Tests/MockTests.cs:26](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L26) | CreatesStrictMock | yes |
| [src/Moq.Tests/MockTests.cs:38](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L38) | CreatesClassMockThatCallsBase | yes |
| [src/Moq.Tests/MockTests.cs:49](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L49) | CreatesMockWithAdditionalInterfaces | yes |
| [src/Moq.Tests/MockTests.cs:63](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L63) | AsThrowsIfInterfaceIsNotImplemented | yes |
| [src/Moq.Tests/MockTests.cs:67](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L67) | GetsMockForImplementedInterface | yes |
| [src/Moq.Tests/MockTests.cs:77](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L77) | GetThrowsIfInterfaceIsNotImplemented | yes |
| [src/Moq.Tests/MockTests.cs:81](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L81) | GetThrowsIfNotMock | yes |
| [src/Moq.Tests/MockTests.cs:85](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L85) | MocksDelegates | yes |
| [src/Moq.Tests/MockTests.cs:96](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L96) | CustomizesCreatedMocks | yes |
| [src/Moq.Tests/MockTests.cs:105](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L105) | CustomizesCreatedMocksWithAdditionalInterfaces | yes |
| [src/Moq.Tests/MockTests.cs:109](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L109) | CustomConstructorsCreateMocks | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-052-F01-01 | WP-01 | Overload identities do not collide | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F01-02 | WP-01 | strict unexpected calls fail immediately | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F01-03 | WP-01 | matcher state does not leak between threads | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F02-01 | WP-02 | Setup order is deterministic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F02-02 | WP-02 | failed verification shows actual calls | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F02-03 | WP-02 | callbacks throwing still record invocation according to contract | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F03-01 | WP-03 | Interface mocks work without an agent | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F03-02 | WP-03 | unsupported member interception fails clearly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F03-03 | WP-03 | instrumentation is not secretly provided by Mockito/ByteBuddy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F04-01 | WP-04 | Reset cannot corrupt active invocations | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F04-02 | WP-04 | classloader stress shows no unbounded retention | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F04-03 | WP-04 | failed transformations preserve valid classes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F05-01 | WP-05 | Setup expression representation validates the original method identity before use | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F05-02 | WP-05 | adaptations are visible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-052-F05-03 | WP-05 | upstream features without Java equivalents remain explicit coverage entries | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Overload matching; generic erasure; concurrent invocation logs; default methods; verification diagnostics; retransformation limits.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-052-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-052-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-052-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
