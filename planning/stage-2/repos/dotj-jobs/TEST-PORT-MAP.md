# DJ-029 .j Jobs: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/Hangfire.Core.Tests/CronFacts.cs:9](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L9) | Minutely_ReturnsFormattedString | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:17](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L17) | Hourly_WithoutMinute_ReturnsFormattedStringWithDefaults | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:25](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L25) | Hourly_WithMinute_ReturnsFormattedStringWithMinute | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:33](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L33) | Daily_WithoutMinuteOrHour_ReturnsFormattedStringWithDefaults | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:41](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L41) | Daily_WithoutMinute_ReturnsFormattedStringWithHourAndZeroMinute | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:49](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L49) | Daily_WithMinuteAndHour_ReturnsFormattedStringWithHourAndMinute | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:57](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L57) | Weekly_WithoutDayHourMinute_ReturnsFormattedStringWithDefaults | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:65](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L65) | Weekly_WithDayWithoutHourMinute_ReturnsFormattedStringWithDay | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:74](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L74) | Weekly_WithDayHourWithoutMinute_ReturnsFormattedStringWithDayHour | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:84](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L84) | Weekly_WithDayHourMinute_ReturnsFormattedStringWithDayHourMinute | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:95](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L95) | Monthly_WithoutDayHourMinute_ReturnsFormattedStringWithDefaults | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:103](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L103) | Monthly_WithoutHourMinuteWithDay_ReturnsFormattedStringWithDay | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:112](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L112) | Monthly_WithoutMinuteWithDayHour_ReturnsFormattedStringWithDayHour | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:122](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L122) | Monthly_WithDayHourMinute_ReturnsFormattedStringWithDayHourMinute | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:133](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L133) | Yearly_WithoutMonthDayHourMinute_ReturnsFormattedStringWithDefaults | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:141](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L141) | Yearly_WithoutDayHourMinuteWithMonth_ReturnsFormattedStringWithMonth | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:150](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L150) | Yearly_WithoutHourMinuteWithMonthDay_ReturnsFormattedStringWithMonthDay | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:160](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L160) | Yearly_WithoutMinuteWithMonthDayHour_ReturnsFormattedStringWithMonthDayHour | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:171](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L171) | Yearly_WithMonthDayHourMinute_ReturnsFormattedStringWithMonthDayHourMinute | yes |
| [tests/Hangfire.Core.Tests/CronFacts.cs:183](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L183) | Never_ReturnsFormattedString | yes |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:17](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L17) | SetCurrent_DoesNotThrowAnException_WhenValueIsNull | yes |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:24](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L24) | GetCurrent_ThrowsAnException_OnUninitializedValue | yes |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:32](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L32) | GetCurrent_ReturnsCurrentValue_WhenInitialized | yes |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:41](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L41) | GetComponents_ReturnsEmptyCollectionByDefault | yes |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:47](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L47) | GetStateHandlers_ReturnsEmptyCollectionByDefault | yes |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:53](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L53) | JobExpirationTimeout_HasDefaultTimeoutFromDays1 | yes |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:59](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L59) | JobExpirationTimeout_CantAllowTimeoutLessThanOneHour | yes |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:69](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L69) | JobExpirationTimeout_CanChangeTheTimeout | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-029-F01-01 | WP-01 | Unknown method versions fail before invocation | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F01-02 | WP-01 | arbitrary type activation is disabled | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F01-03 | WP-01 | state history explains each retry | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F02-01 | WP-02 | Two workers cannot hold the same valid claim under store assumptions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F02-02 | WP-02 | crashed workers become reclaimable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F02-03 | WP-02 | guarantees are stated per provider | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F03-01 | WP-03 | A side effect followed by crash is recognized as possibly duplicated | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F03-02 | WP-03 | filter failures release resources | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F03-03 | WP-03 | shutdown leaves recoverable job state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F04-01 | WP-04 | DST/restart cases do not silently lose occurrence identity | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F04-02 | WP-04 | continuations obey terminal conditions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F04-03 | WP-04 | unlicensed extensions are not copied | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F05-01 | WP-05 | Dashboard cannot execute arbitrary methods | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F05-02 | WP-05 | retained payloads obey policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-029-F05-03 | WP-05 | at-least-once limitations are visible in documentation | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Worker crash between execution and ack; lease loss; duplicate enqueue; retry exhaustion; dashboard authorization.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-029-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-029-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-029-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
