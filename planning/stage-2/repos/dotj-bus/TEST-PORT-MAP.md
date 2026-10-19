# DJ-066 .j Bus: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/MassTransit.Tests/CronExpressionTests.cs:20](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L20) | TestIsSatisfiedBy | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:48](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L48) | TestLastDayOffset | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:75](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L75) | ExpressionToString | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:82](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L82) | CannotUseMultipleLastDayOfMonthInArray | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:97](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L97) | CanUseLastDayOfMonthInArray | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:129](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L129) | CanUse_DayOfMonth_And_DayOfWeek_Together | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:155](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L155) | LastWeekDayWithOffset | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:169](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L169) | Ensure_NthWeek_IsBetween1And5 | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:188](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L188) | Ensure_NthWeek_Day_IsBetween1And7 | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:213](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L213) | ExpressionEquality | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:223](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L223) | OffSetValue_CannontBe_GreaterThan30 | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:236](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L236) | Ensure_L_Token_CanOnlyBeUsedIn_DayOfWeek_ORDayOfMonth | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:246](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L246) | CronExpression_Throw_Error_Constructed_With_Null | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:255](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L255) | Should_Throw_Error_When_Extra_NonWhitespace_Character_After_QuestionMark | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:263](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L263) | QuestionMark_With_ExtraWhitespace_Should_Be_Valid | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:270](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L270) | TestCronExpressionPassingMidnight | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:279](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L279) | TestCronExpressionPassingYear | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:290](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L290) | TestCronExpressionWeekdaysMonFri | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:301](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L301) | TestCronExpressionWeekdaysFriday | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:314](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L314) | TestCronExpressionWeekdaysFridayEveryTwoWeeks | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:327](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L327) | TestCronExpressionWeekdaysThirsdayAndFridayEveryTwoWeeks | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:340](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L340) | TestCronExpressionLastDayOfMonth | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:350](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L350) | TestHourShift | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:359](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L359) | TestEveryMinute | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:368](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L368) | TestMonthShift | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:377](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L377) | TestYearChange | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:384](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L384) | TestCronExpressionParsingIncorrectDayOfWeek | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:400](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L400) | TestCronExpressionWithExtraWhiteSpace | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:432](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L432) | TestNthWeekDayPassingMonth | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:451](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L451) | TestNormal | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:458](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L458) | TestSecond | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:464](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L464) | TestMinute | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:470](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L470) | TestHour | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:476](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L476) | TestDayOfWeekNumber | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:482](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L482) | TestDayOfWeek | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:488](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L488) | TestDayOfMonth | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:494](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L494) | TestMonth | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:500](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L500) | TestAmbiguous | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:525](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L525) | TestQuartz640 | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:564](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L564) | TestGetTimeAfter_QRTZNET149 | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:583](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L583) | TestQRTZNET152_Nearest_Weekday_Expression_W_Does_Not_Work_In_CronTrigger | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:595](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L595) | ShouldThrowExceptionIfWParameterMakesNoSense | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:610](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L610) | TestDaylightSaving_QRTZNETZ186 | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:625](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L625) | TestDaylightSavingsDoesNotMatchAnHourBefore | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:640](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L640) | TestDaylightSavingsDoesNotMatchAnHourBefore2 | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:655](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L655) | TestSecRangeIntervalAfterSlash | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:676](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L676) | TestMinRangeIntervalAfterSlash | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:697](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L697) | TestHourRangeIntervalAfterSlash | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:717](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L717) | TestDayOfMonthRangeIntervalAfterSlash | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:737](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L737) | TestMonthRangeIntervalAfterSlash | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:757](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L757) | TestDayOfWeekRangeIntervalAfterSlash | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:777](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L777) | TestInvalidCharactersAfterAsterisk | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:794](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L794) | TestExtraCharactersAfterWeekDay | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:800](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L800) | TestHourRangeAndSlash | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:807](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L807) | PerformanceTest | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:828](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L828) | CanGetHashCode | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:836](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L836) | CanGetExpressionSummary | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:860](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L860) | GivenMonthAbbreviation_ShouldGetTimeAfter | yes |
| [tests/MassTransit.Tests/CronExpressionTests.cs:874](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.Tests/CronExpressionTests.cs#L874) | CronExpressionReturnsExpectedNextFireTime | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:34](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L34) | SendAllAsyncWritesToAllConnectionsOutput | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:72](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L72) | SendAllAsyncDoesNotWriteToDisconnectedConnectionsOutput | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:108](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L108) | SendGroupAsyncWritesToAllConnectionsInGroupOutput | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:149](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L149) | DisconnectConnectionRemovesConnectionFromGroup | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:176](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L176) | RemoveGroupFromLocalConnectionNotInGroupDoesNothing | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:194](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L194) | AddGroupAsyncForLocalConnectionAlreadyInGroupDoesNothing | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:215](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L215) | WritingToGroupWithOneConnectionFailingSecondConnectionStillReceivesMessage | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:245](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L245) | InvokeUserSendsToAllConnectionsForUser | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:268](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L268) | ConnectionShouldReceiveMessage | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:283](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L283) | ConnectionShouldNotBeReceivedIfConnectionIdCasingIsOff | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:298](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L298) | ExcludedConnectionShouldNotReceiveSendAllMessage | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:313](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L313) | ExcludedConnectionShouldReceiveSendAllMessageWhenCasingIsOff | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:328](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L328) | ExcludedConnectionShouldNotReceiveSendGroupMessage | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:347](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L347) | ExcludedConnectionShouldReceiveSendGroupMessageWhenCasingIsOff | yes |
| [tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs:367](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/tests/MassTransit.SignalR.Tests/HubLifeTimeManagerTests.cs#L367) | StillSubscribedToUserAfterOneOfMultipleConnectionsAssociatedWithUserDisconnects | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-066-F01-01 | WP-01 | Unknown message versions fail explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F01-02 | WP-01 | send and publish have distinct routing | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F01-03 | WP-01 | transport claims are scoped to tested adapters | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F02-01 | WP-02 | Acknowledge occurs at declared durability boundary | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F02-02 | WP-02 | repeated failures reach observable quarantine | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F02-03 | WP-02 | faults do not recursively create unbounded fault loops | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F03-01 | WP-03 | Concurrent events cannot silently overwrite state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F03-02 | WP-03 | unknown correlations are diagnosable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F03-03 | WP-03 | transition history explains duplicate handling | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F04-01 | WP-04 | Lost broker acknowledgment can produce duplicates but not a false exactly-once claim | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F04-02 | WP-04 | deduplication window is explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F04-03 | WP-04 | recovery replays only committed intents | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F05-01 | WP-05 | Every transport has its own guarantee matrix | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F05-02 | WP-05 | host shutdown bounds outstanding work | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-066-F05-03 | WP-05 | inspected Apache source terms are not generalized to all product versions | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Broker failover; redelivery/deduplication; outbox crash windows; saga concurrency; topology mismatch; poison messages; rolling schemas.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
