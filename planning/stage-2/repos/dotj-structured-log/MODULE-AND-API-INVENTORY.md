# DJ-048 .j Structured Log: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 284 | recursive complete |
| Project-definition paths | 6 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 105 | Lexical path classification, not runnable test count |
| Sampled text files | 9 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 95 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 9 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [src/Serilog/Serilog.csproj](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Serilog.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [test/AotTestApp/AotTestApp.csproj](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/AotTestApp/AotTestApp.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Serilog.ApprovalTests/Serilog.ApprovalTests.csproj](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.ApprovalTests/Serilog.ApprovalTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Serilog.PerformanceTests/Serilog.PerformanceTests.csproj](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.PerformanceTests/Serilog.PerformanceTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Serilog.Tests/Serilog.Tests.csproj](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/Serilog.Tests/Serilog.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/TestDummies/TestDummies.csproj](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/test/TestDummies/TestDummies.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/Serilog/Log.cs:34](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L34) | `public static class Log` |
| [src/Serilog/Log.cs:42](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L42) | `public static ILogger Logger` |
| [src/Serilog/Log.cs:51](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L51) | `public static void CloseAndFlush()` |
| [src/Serilog/Log.cs:62](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L62) | `public static async ValueTask CloseAndFlushAsync()` |
| [src/Serilog/Log.cs:82](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L82) | `public static ILogger ForContext(ILogEventEnricher enricher)` |
| [src/Serilog/Log.cs:92](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L92) | `public static ILogger ForContext(ILogEventEnricher[] enrichers)` |
| [src/Serilog/Log.cs:101](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L101) | `public static ILogger ForContext(string propertyName, object? value, bool destructureObjects = false)` |
| [src/Serilog/Log.cs:112](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L112) | `public static ILogger ForContext<TSource>() => Logger.ForContext<TSource>();` |
| [src/Serilog/Log.cs:120](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L120) | `public static ILogger ForContext(Type source) => Logger.ForContext(source);` |
| [src/Serilog/Log.cs:126](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L126) | `public static void Write(LogEvent logEvent)` |
| [src/Serilog/Log.cs:137](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L137) | `public static void Write(LogEventLevel level, string messageTemplate)` |
| [src/Serilog/Log.cs:149](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L149) | `public static void Write<T>(LogEventLevel level, string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:162](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L162) | `public static void Write<T0, T1>(LogEventLevel level, string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:176](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L176) | `public static void Write<T0, T1, T2>(LogEventLevel level, string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |
| [src/Serilog/Log.cs:188](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L188) | `public static void Write(LogEventLevel level, string messageTemplate, params object?[]? propertyValues)` |
| [src/Serilog/Log.cs:200](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L200) | `public static void Write(LogEventLevel level, Exception? exception, string messageTemplate)` |
| [src/Serilog/Log.cs:213](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L213) | `public static void Write<T>(LogEventLevel level, Exception? exception, string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:227](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L227) | `public static void Write<T0, T1>(LogEventLevel level, Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:242](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L242) | `public static void Write<T0, T1, T2>(LogEventLevel level, Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |
| [src/Serilog/Log.cs:255](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L255) | `public static void Write(LogEventLevel level, Exception? exception, string messageTemplate, params object?[]? propertyValues)` |
| [src/Serilog/Log.cs:266](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L266) | `public static bool IsEnabled(LogEventLevel level) => Logger.IsEnabled(level);` |
| [src/Serilog/Log.cs:276](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L276) | `public static void Verbose(string messageTemplate)` |
| [src/Serilog/Log.cs:290](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L290) | `public static void Verbose<T>(string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:305](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L305) | `public static void Verbose<T0, T1>(string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:321](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L321) | `public static void Verbose<T0, T1, T2>(string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |
| [src/Serilog/Log.cs:335](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L335) | `public static void Verbose(string messageTemplate, params object?[]? propertyValues)` |
| [src/Serilog/Log.cs:349](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L349) | `public static void Verbose(Exception? exception, string messageTemplate)` |
| [src/Serilog/Log.cs:364](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L364) | `public static void Verbose<T>(Exception? exception, string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:380](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L380) | `public static void Verbose<T0, T1>(Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:397](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L397) | `public static void Verbose<T0, T1, T2>(Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |
| [src/Serilog/Log.cs:412](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L412) | `public static void Verbose(Exception? exception, string messageTemplate, params object?[]? propertyValues)` |
| [src/Serilog/Log.cs:425](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L425) | `public static void Debug(string messageTemplate)` |
| [src/Serilog/Log.cs:439](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L439) | `public static void Debug<T>(string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:454](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L454) | `public static void Debug<T0, T1>(string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:470](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L470) | `public static void Debug<T0, T1, T2>(string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |
| [src/Serilog/Log.cs:484](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L484) | `public static void Debug(string messageTemplate, params object?[]? propertyValues)` |
| [src/Serilog/Log.cs:498](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L498) | `public static void Debug(Exception? exception, string messageTemplate)` |
| [src/Serilog/Log.cs:513](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L513) | `public static void Debug<T>(Exception? exception, string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:529](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L529) | `public static void Debug<T0, T1>(Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:546](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L546) | `public static void Debug<T0, T1, T2>(Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |
| [src/Serilog/Log.cs:561](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L561) | `public static void Debug(Exception? exception, string messageTemplate, params object?[]? propertyValues)` |
| [src/Serilog/Log.cs:574](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L574) | `public static void Information(string messageTemplate)` |
| [src/Serilog/Log.cs:588](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L588) | `public static void Information<T>(string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:603](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L603) | `public static void Information<T0, T1>(string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:619](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L619) | `public static void Information<T0, T1, T2>(string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |
| [src/Serilog/Log.cs:633](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L633) | `public static void Information(string messageTemplate, params object?[]? propertyValues)` |
| [src/Serilog/Log.cs:647](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L647) | `public static void Information(Exception? exception, string messageTemplate)` |
| [src/Serilog/Log.cs:662](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L662) | `public static void Information<T>(Exception? exception, string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:678](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L678) | `public static void Information<T0, T1>(Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:695](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L695) | `public static void Information<T0, T1, T2>(Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |
| [src/Serilog/Log.cs:710](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L710) | `public static void Information(Exception? exception, string messageTemplate, params object?[]? propertyValues)` |
| [src/Serilog/Log.cs:723](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L723) | `public static void Warning(string messageTemplate)` |
| [src/Serilog/Log.cs:737](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L737) | `public static void Warning<T>(string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:752](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L752) | `public static void Warning<T0, T1>(string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:768](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L768) | `public static void Warning<T0, T1, T2>(string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |
| [src/Serilog/Log.cs:782](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L782) | `public static void Warning(string messageTemplate, params object?[]? propertyValues)` |
| [src/Serilog/Log.cs:796](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L796) | `public static void Warning(Exception? exception, string messageTemplate)` |
| [src/Serilog/Log.cs:811](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L811) | `public static void Warning<T>(Exception? exception, string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:827](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L827) | `public static void Warning<T0, T1>(Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:844](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L844) | `public static void Warning<T0, T1, T2>(Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |
| [src/Serilog/Log.cs:859](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L859) | `public static void Warning(Exception? exception, string messageTemplate, params object?[]? propertyValues)` |
| [src/Serilog/Log.cs:872](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L872) | `public static void Error(string messageTemplate)` |
| [src/Serilog/Log.cs:886](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L886) | `public static void Error<T>(string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:901](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L901) | `public static void Error<T0, T1>(string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:917](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L917) | `public static void Error<T0, T1, T2>(string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |
| [src/Serilog/Log.cs:931](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L931) | `public static void Error(string messageTemplate, params object?[]? propertyValues)` |
| [src/Serilog/Log.cs:945](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L945) | `public static void Error(Exception? exception, string messageTemplate)` |
| [src/Serilog/Log.cs:960](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L960) | `public static void Error<T>(Exception? exception, string messageTemplate, T propertyValue)` |
| [src/Serilog/Log.cs:976](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L976) | `public static void Error<T0, T1>(Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1)` |
| [src/Serilog/Log.cs:993](https://github.com/serilog/serilog/blob/81af75f3a5e28ec9f5be18ef74357a9914a51745/src/Serilog/Log.cs#L993) | `public static void Error<T0, T1, T2>(Exception? exception, string messageTemplate, T0 propertyValue0, T1 propertyValue1, T2 propertyValue2)` |

Full lexical records (95) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | Message templates and property values | MessageTemplate; LogEvent; PropertyValue |
| WP-02 | Logger configuration enrichment and filtering | LoggerConfig; Enricher; Filter; LevelSwitch |
| WP-03 | Sinks batching and backpressure | Sink; Batch; DeliveryPolicy |
| WP-04 | Formats integrations and configuration | EventFormatter; ConfigurationReader; LoggingBridge |
| WP-05 | Compatibility and performance corpus | TemplateCase; SinkFaultCase; AllocationReport |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
