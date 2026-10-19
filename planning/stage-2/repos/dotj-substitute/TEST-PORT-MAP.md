# DJ-053 .j Substitute: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:10](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L10) | TimeBasicOperations | yes |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:34](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L34) | TimeBasicOperationsWithGenerics | yes |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:58](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L58) | Multiple_return_configuration_dont_leak_memory_for_any_args | yes |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:73](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L73) | Muiltiple_return_configurations_dont_lead_to_memory_leak | yes |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:87](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L87) | Delegate_proxy_container_is_cached | yes |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:99](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L99) | ProxyTypeIsCached | yes |
| [tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs:10](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs#L10) | Received_LogTrace_call_using_AnyType | yes |
| [tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs:27](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs#L27) | Received_LogWarning_call_using_interfaced_types | yes |
| [tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs:44](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs#L44) | Received_LogError_call_using_messageTemplate | yes |
| [tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs:70](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs#L70) | Received_LogInformation_call_using_messageTemplate | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-053-F01-01 | WP-01 | Ambiguous matchers fail clearly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F01-02 | WP-01 | configuration does not count as an ordinary received call | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F01-03 | WP-01 | overload matching is stable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F02-01 | WP-02 | Exhausted sequences obey documented policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F02-02 | WP-02 | holder adaptation is explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F02-03 | WP-02 | recursive substitutes remain stable per configured path | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F03-01 | WP-03 | Order checks identify missing/out-of-order calls | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F03-02 | WP-03 | predicate errors are diagnosable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F03-03 | WP-03 | listener raises follow declared exception rules | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F04-01 | WP-04 | Parallel configuration cannot cross-contaminate substitutes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F04-02 | WP-04 | unsupported members fail explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F04-03 | WP-04 | no Mockito implementation is adopted | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F05-01 | WP-05 | Substitutes run independently of NUnit/xUnit ports | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F05-02 | WP-05 | reset clears only owned state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-053-F05-03 | WP-05 | instrumentation capabilities are reported accurately | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Matcher ambiguity; sequence behavior; call-order checks; async values; cross-thread recording; partial-substitute side effects.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
