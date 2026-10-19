# DJ-030 .j Scheduler: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/Quartz.Tests.Unit/SimpleTriggerDstTests.cs:46](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/SimpleTriggerDstTests.cs#L46) | HourlySimpleTrigger_FallBackLocalDayHas25Fires_SpringDay23 | yes |
| [src/Quartz.Tests.Unit/SimpleTriggerDstTests.cs:77](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/SimpleTriggerDstTests.cs#L77) | FinalFireTimeUtc_IsPureTickArithmetic_AcrossTransition | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:109](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L109) | GetTimeAfter_FixedTimeInsideGap_FiresOnceAtTheEndOfTheGap | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:143](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L143) | GetTimeAfter_DailyFixedTime_FallBackDay_FiresOnlyOnce_AtDaylightOccurrence | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:174](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L174) | SequentialWalk_MinutelyCron_SpringForwardDay_FireCountAndNoLocalGapHour | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:229](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L229) | GetPreviousValidTimeBefore_RoundTripsWithGetTimeAfter_AroundTransitions | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:264](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L264) | IsSatisfiedBy_MinutelyCron_TrueForInstantsInsideGapHourUtc | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:287](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L287) | SequentialWalk_MinutelyCron_FallBackDay_FiresThroughBothPassesOfRepeatedHour | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:314](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L314) | IsSatisfiedBy_RepeatedHourStandardPass_AgreesWithSequentialWalk | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:348](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L348) | HasIntervalSemantics_SetForWildcardStepAndRangeInTimeFields | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:360](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L360) | SequentialWalk_HourlyCron_FallBackDay_FiresEveryRealHour | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:382](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L382) | FixedTimeCommaList_FallBackDay_FiresOnlyFirstPass | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:404](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L404) | SequentialWalk_MinutelyCron_LordHoweFallBack_FiresBothHalfHourPasses | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:443](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L443) | IsSatisfiedBy_InstantReturnedForInGapFixedTime_IsTrue | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:470](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L470) | GetTimeAfter_SeveralMatchesInsideOneGap_FireOnceAtTheGapsEnd | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:493](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L493) | GetTimeAfter_MatchBetweenGapEndAndTheOldDeltaShift_IsNoLongerSwallowed | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:524](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L524) | GetTimeAfter_HourlyAtHalfPast_FiresAtTheGapsEndAndAgainAtTheNextHalfHour | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:561](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L561) | GetTimeAfter_AcrossSpringForward_MakesStrictProgressAndStaysMonotone | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:597](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L597) | GetTimeAfter_ProbeAtTheMinimumInstant_DoesNotThrow | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:619](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L619) | GetTimeAfter_SubSecondInstantInsideRepeatedHour_ReturnsSameFireAsWholeSecond | yes |
| [src/Quartz.Tests.Unit/CronExpressionDstTests.cs:650](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz.Tests.Unit/CronExpressionDstTests.cs#L650) | GetPreviousValidTimeBefore_ProbeJustAfterFireTimeInRepeatedHour_ReturnsRealPrecedingFire | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-030-F01-01 | WP-01 | DST gaps/overlaps have fixture-backed outcomes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F01-02 | WP-01 | invalid cron fails with location | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F01-03 | WP-01 | calendars do not silently change timezone | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F02-01 | WP-02 | Restart after downtime produces the documented firing sequence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F02-02 | WP-02 | clock adjustments do not spin indefinitely | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F02-03 | WP-02 | pause/resume retains policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F03-01 | WP-03 | Concurrent nodes do not acquire one occurrence twice under declared store guarantees | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F03-02 | WP-03 | recovery does not claim exactly-once side effects | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F04-01 | WP-04 | Listener failure cannot leak a worker | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F04-02 | WP-04 | nonconcurrent jobs serialize correctly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F04-03 | WP-04 | interrupt remains cooperative and observable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F05-01 | WP-05 | Core schedule calculation works without a database | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F05-02 | WP-05 | test traces identify timezone data version | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-030-F05-03 | WP-05 | every claimed store has recovery evidence | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

DST gaps/overlaps; leap dates; misfire modes; clock changes; trigger acquisition races; cluster failover.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-030-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-030-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-030-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
