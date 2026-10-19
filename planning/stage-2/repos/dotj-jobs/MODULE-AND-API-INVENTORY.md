# DJ-029 .j Jobs: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 611 | recursive complete |
| Project-definition paths | 10 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 138 | Lexical path classification, not runnable test count |
| Sampled text files | 15 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 70 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 28 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [samples/ConsoleSample/ConsoleSample.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/samples/ConsoleSample/ConsoleSample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/NetCoreSample/NetCoreSample.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/samples/NetCoreSample/NetCoreSample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Hangfire.NetCore/Hangfire.NetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.NetCore/Hangfire.NetCore.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Hangfire.SqlServer.Msmq/Hangfire.SqlServer.Msmq.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.SqlServer.Msmq/Hangfire.SqlServer.Msmq.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Hangfire.SqlServer/Hangfire.SqlServer.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.SqlServer/Hangfire.SqlServer.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [tests/Hangfire.SqlServer.Msmq.Tests/Hangfire.SqlServer.Msmq.Tests.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.SqlServer.Msmq.Tests/Hangfire.SqlServer.Msmq.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [tests/Hangfire.SqlServer.Tests/Hangfire.SqlServer.Tests.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.SqlServer.Tests/Hangfire.SqlServer.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/Hangfire.Core/Cron.cs:23](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L23) | `public static class Cron` |
| [src/Hangfire.Core/Cron.cs:28](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L28) | `public static string Minutely()` |
| [src/Hangfire.Core/Cron.cs:36](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L36) | `public static string Hourly()` |
| [src/Hangfire.Core/Cron.cs:45](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L45) | `public static string Hourly(int minute)` |
| [src/Hangfire.Core/Cron.cs:53](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L53) | `public static string Daily()` |
| [src/Hangfire.Core/Cron.cs:63](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L63) | `public static string Daily(int hour)` |
| [src/Hangfire.Core/Cron.cs:74](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L74) | `public static string Daily(int hour, int minute)` |
| [src/Hangfire.Core/Cron.cs:82](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L82) | `public static string Weekly()` |
| [src/Hangfire.Core/Cron.cs:92](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L92) | `public static string Weekly(DayOfWeek dayOfWeek)` |
| [src/Hangfire.Core/Cron.cs:103](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L103) | `public static string Weekly(DayOfWeek dayOfWeek, int hour)` |
| [src/Hangfire.Core/Cron.cs:115](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L115) | `public static string Weekly(DayOfWeek dayOfWeek, int hour, int minute)` |
| [src/Hangfire.Core/Cron.cs:124](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L124) | `public static string Monthly()` |
| [src/Hangfire.Core/Cron.cs:134](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L134) | `public static string Monthly(int day)` |
| [src/Hangfire.Core/Cron.cs:145](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L145) | `public static string Monthly(int day, int hour)` |
| [src/Hangfire.Core/Cron.cs:157](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L157) | `public static string Monthly(int day, int hour, int minute)` |
| [src/Hangfire.Core/Cron.cs:165](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L165) | `public static string Yearly()` |
| [src/Hangfire.Core/Cron.cs:175](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L175) | `public static string Yearly(int month)` |
| [src/Hangfire.Core/Cron.cs:186](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L186) | `public static string Yearly(int month, int day)` |
| [src/Hangfire.Core/Cron.cs:198](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L198) | `public static string Yearly(int month, int day, int hour)` |
| [src/Hangfire.Core/Cron.cs:211](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L211) | `public static string Yearly(int month, int day, int hour, int minute)` |
| [src/Hangfire.Core/Cron.cs:219](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L219) | `public static string Never()` |
| [src/Hangfire.Core/Cron.cs:233](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L233) | `public static string MinuteInterval(int interval)` |
| [src/Hangfire.Core/Cron.cs:247](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L247) | `public static string HourInterval(int interval)` |
| [src/Hangfire.Core/Cron.cs:262](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L262) | `public static string DayInterval(int interval)` |
| [src/Hangfire.Core/Cron.cs:275](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L275) | `public static string MonthInterval(int interval)` |
| [src/Hangfire.Core/Cron.cs:287](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs#L287) | `public static string GetDescription(string cronExpression)` |
| [src/Hangfire.Core/JobStorage.cs:27](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L27) | `public abstract class JobStorage` |
| [src/Hangfire.Core/JobStorage.cs:34](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L34) | `public static JobStorage Current` |
| [src/Hangfire.Core/JobStorage.cs:64](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L64) | `public TimeSpan JobExpirationTimeout` |
| [src/Hangfire.Core/JobStorage.cs:81](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L81) | `public virtual bool LinearizableReads => false;` |
| [src/Hangfire.Core/JobStorage.cs:83](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L83) | `public abstract IMonitoringApi GetMonitoringApi();` |
| [src/Hangfire.Core/JobStorage.cs:85](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L85) | `public abstract IStorageConnection GetConnection();` |
| [src/Hangfire.Core/JobStorage.cs:87](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L87) | `public virtual IStorageConnection GetReadOnlyConnection()` |
| [src/Hangfire.Core/JobStorage.cs:94](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L94) | `public virtual IEnumerable<IServerComponent> GetComponents()` |
| [src/Hangfire.Core/JobStorage.cs:100](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L100) | `public virtual IEnumerable<IBackgroundProcess> GetServerRequiredProcesses()` |
| [src/Hangfire.Core/JobStorage.cs:105](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L105) | `public virtual IEnumerable<IBackgroundProcess> GetStorageWideProcesses()` |
| [src/Hangfire.Core/JobStorage.cs:110](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L110) | `public virtual IEnumerable<IStateHandler> GetStateHandlers()` |
| [src/Hangfire.Core/JobStorage.cs:115](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L115) | `public virtual void WriteOptionsToLog(ILog logger)` |
| [src/Hangfire.Core/JobStorage.cs:119](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs#L119) | `public virtual bool HasFeature([NotNull] string featureId)` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:6](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L6) | `public class CronFacts` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:9](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L9) | `public void Minutely_ReturnsFormattedString()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:17](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L17) | `public void Hourly_WithoutMinute_ReturnsFormattedStringWithDefaults()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:25](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L25) | `public void Hourly_WithMinute_ReturnsFormattedStringWithMinute()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:33](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L33) | `public void Daily_WithoutMinuteOrHour_ReturnsFormattedStringWithDefaults()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:41](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L41) | `public void Daily_WithoutMinute_ReturnsFormattedStringWithHourAndZeroMinute()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:49](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L49) | `public void Daily_WithMinuteAndHour_ReturnsFormattedStringWithHourAndMinute()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:57](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L57) | `public void Weekly_WithoutDayHourMinute_ReturnsFormattedStringWithDefaults()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:65](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L65) | `public void Weekly_WithDayWithoutHourMinute_ReturnsFormattedStringWithDay()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:74](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L74) | `public void Weekly_WithDayHourWithoutMinute_ReturnsFormattedStringWithDayHour()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:84](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L84) | `public void Weekly_WithDayHourMinute_ReturnsFormattedStringWithDayHourMinute()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:95](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L95) | `public void Monthly_WithoutDayHourMinute_ReturnsFormattedStringWithDefaults()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:103](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L103) | `public void Monthly_WithoutHourMinuteWithDay_ReturnsFormattedStringWithDay()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:112](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L112) | `public void Monthly_WithoutMinuteWithDayHour_ReturnsFormattedStringWithDayHour()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:122](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L122) | `public void Monthly_WithDayHourMinute_ReturnsFormattedStringWithDayHourMinute()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:133](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L133) | `public void Yearly_WithoutMonthDayHourMinute_ReturnsFormattedStringWithDefaults()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:141](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L141) | `public void Yearly_WithoutDayHourMinuteWithMonth_ReturnsFormattedStringWithMonth()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:150](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L150) | `public void Yearly_WithoutHourMinuteWithMonthDay_ReturnsFormattedStringWithMonthDay()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:160](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L160) | `public void Yearly_WithoutMinuteWithMonthDayHour_ReturnsFormattedStringWithMonthDayHour()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:171](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L171) | `public void Yearly_WithMonthDayHourMinute_ReturnsFormattedStringWithMonthDayHourMinute()` |
| [tests/Hangfire.Core.Tests/CronFacts.cs:183](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs#L183) | `public void Never_ReturnsFormattedString()` |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:7](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L7) | `public class JobStorageFacts` |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:11](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L11) | `public JobStorageFacts()` |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:17](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L17) | `public void SetCurrent_DoesNotThrowAnException_WhenValueIsNull()` |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:24](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L24) | `public void GetCurrent_ThrowsAnException_OnUninitializedValue()` |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:32](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L32) | `public void GetCurrent_ReturnsCurrentValue_WhenInitialized()` |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:41](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L41) | `public void GetComponents_ReturnsEmptyCollectionByDefault()` |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:47](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L47) | `public void GetStateHandlers_ReturnsEmptyCollectionByDefault()` |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:53](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L53) | `public void JobExpirationTimeout_HasDefaultTimeoutFromDays1()` |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:59](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L59) | `public void JobExpirationTimeout_CantAllowTimeoutLessThanOneHour()` |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs:69](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs#L69) | `public void JobExpirationTimeout_CanChangeTheTimeout()` |

Full lexical records (70) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | Job representation and state machine | JobDescriptor; JobState; StateTransition |
| WP-02 | Persistent storage and atomic claims | JobStore; WorkerLease; QueueRecord |
| WP-03 | Worker execution filters and cancellation | JobContext; JobFilter; WorkerPool |
| WP-04 | Recurring jobs continuations and batches | RecurringDefinition; Continuation; ScheduleOccurrence |
| WP-05 | Dashboard and operational acceptance | JobDashboard; QueueMetrics; RetentionPolicy |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
