# DJ-027 .j Resilience: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/Shared/StrongNameTests.cs:9](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Shared/StrongNameTests.cs#L9) | Tests_Are_Strong_Named | yes |
| [test/Polly.Core.Tests/OutcomeTests.cs:6](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L6) | Ctor_Result_Ok | yes |
| [test/Polly.Core.Tests/OutcomeTests.cs:19](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L19) | Ctor_VoidResult_Ok | yes |
| [test/Polly.Core.Tests/OutcomeTests.cs:31](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L31) | Ctor_Exception_Ok | yes |
| [test/Polly.Core.Tests/OutcomeTests.cs:43](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L43) | ToString_NullResult_ShouldBeEmpty | yes |
| [test/Polly.Core.Tests/OutcomeTests.cs:50](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L50) | EnsureSuccess_Result | yes |
| [test/Polly.Core.Tests/OutcomeTests.cs:58](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L58) | EnsureSuccess_Exception | yes |
| [test/Polly.Core.Tests/OutcomeTests.cs:66](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L66) | FromException_Throws_If_Null | yes |
| [test/Polly.Core.Tests/OutcomeTests.cs:70](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L70) | FromExceptionAsValueTask_Throws_If_Null | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-027-F01-01 | WP-01 | Concurrent calls do not share attempt counters | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F01-02 | WP-01 | context cleanup runs on every outcome | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F01-03 | WP-01 | caller cancellation remains distinguishable from timeout | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F02-01 | WP-02 | Deterministic fake time reproduces attempts | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F02-02 | WP-02 | retry-after handling is bounded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F02-03 | WP-02 | non-replayable operations require explicit caller policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F03-01 | WP-03 | Only allowed probes enter half-open state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F03-02 | WP-03 | cancellation returns permits once | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F03-03 | WP-03 | rejected work reports strategy-specific outcomes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F04-01 | WP-04 | No hedge occurs for ineligible requests | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F04-02 | WP-04 | losing response bodies are closed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F04-03 | WP-04 | simultaneous completions yield one returned result | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F05-01 | WP-05 | Telemetry excludes payload secrets | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F05-02 | WP-05 | retry fixtures are reproducible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-027-F05-03 | WP-05 | composition order has explicit examples and acceptance outcomes | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Virtual-clock retry schedules; half-open contention; retry storms; cancellation races; permit leaks and jitter distribution.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
