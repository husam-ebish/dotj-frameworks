# DJ-049 .j Log: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/NLog.UnitTests/ApiTests.cs:60](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs#L60) | PublicEnumsTest | yes |
| [tests/NLog.UnitTests/ApiTests.cs:136](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs#L136) | TypesInInternalNamespaceShouldBeInternalTest | yes |
| [tests/NLog.UnitTests/ApiTests.cs:176](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs#L176) | TryGetRawValue_ThreadAgnostic_Attribute_Required | yes |
| [tests/NLog.UnitTests/ApiTests.cs:189](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs#L189) | IStringValueRenderer_AppDomainFixedOutput_Attribute_NotRequired | yes |
| [tests/NLog.UnitTests/ApiTests.cs:202](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs#L202) | SingleDefaultConfigOption | yes |
| [tests/NLog.UnitTests/ApiTests.cs:225](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs#L225) | AppDomainFixedOutput_Attribute_EnsureThreadAgnostic | yes |
| [tests/NLog.UnitTests/ApiTests.cs:239](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs#L239) | WrapperLayoutRenderer_EnsureThreadAgnostic | yes |
| [tests/NLog.UnitTests/ApiTests.cs:254](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs#L254) | ValidateLayoutRendererTypeAlias | yes |
| [tests/NLog.UnitTests/ApiTests.cs:310](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs#L310) | ValidateConfigurationItemFactory | yes |
| [tests/NLog.UnitTests/ApiTests.cs:491](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs#L491) | ShouldNotHaveExplicitStaticConstructors | yes |
| [tests/NLog.UnitTests/ApiTests.cs:592](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/ApiTests.cs#L592) | PublicPropertiesShouldDocumentDefaultValue | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:50](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L50) | TraceTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:233](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L233) | DebugTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:416](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L416) | InfoTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:599](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L599) | WarnTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:782](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L782) | ErrorTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:965](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L965) | FatalTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:1148](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L1148) | LogTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:1307](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L1307) | ConditionalTraceTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:1480](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L1480) | ConditionalTraceILogTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:1653](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L1653) | ConditionalDebugTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:1826](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L1826) | ConditionalDebugILogTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2001](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2001) | SwallowTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2069](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2069) | StringFormatWillNotCauseExceptions | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2087](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2087) | MultipleLoggersWithSameNameShouldBothReceiveMessages | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2109](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2109) | When_Logging_LogEvent_Without_Level_Defined_No_Exception_Should_Be_Thrown | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2122](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2122) | When_Logging_LogEvent_Without_Logger_Defined_UseLoggerName | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2148](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2148) | SingleTargetMessageFormatOptimizationTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2224](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2224) | MixedStructuredEventsConfigTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2254](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2254) | StructuredParametersShouldHandleDeferredCheck | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2284](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2284) | TooManyStructuredParametersShouldKeepBeInParamList | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2305](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2305) | StructuredEventsConfigTest | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2329](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2329) | StructuredEventsTest1 | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2536](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2536) | TestStructuredProperties_json | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2563](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2563) | TestStructuredProperties_json_async | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2594](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2594) | TestStructuredProperties_json_compound | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2619](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2619) | TestOptimizedBlackHoleLogger | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2702](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2702) | LogEventTemplateHandleTrickyDictionary | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2713](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2713) | LogEventTemplateShouldHaveProperties | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2723](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2723) | LogEventTemplateShouldHaveProperties_even_when_changed | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2742](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2742) | LogEventTemplateShouldOverrideProperties | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2769](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2769) | LoggerWithPropertyShouldInheritLogLevel | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2792](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2792) | LoggerSetPropertyChangesCurrentLogger | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2817](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2817) | ObsoleteILoggerExceptionMethods | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2859](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2859) | LoggerPushScopeContextUpdatesMDLC | yes |
| [tests/NLog.UnitTests/LoggerTests.cs:2880](https://github.com/NLog/NLog/blob/d9ebf823ee8ba54977c336709928a96ea58c6259/tests/NLog.UnitTests/LoggerTests.cs#L2880) | LoggerPushScopeContextUpdatesNDLC | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-049-F01-01 | WP-01 | An event follows one configuration revision | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F01-02 | WP-01 | final rules stop routing as declared | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F01-03 | WP-01 | caller context does not mutate after enqueue | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F02-01 | WP-02 | Malformed layouts fail with locations | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F02-02 | WP-02 | recursive renderers terminate | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F02-03 | WP-02 | timezone/culture rendering is explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F03-01 | WP-03 | Rotation preserves record boundaries | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F03-02 | WP-03 | flush reports failures | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F03-03 | WP-03 | bounded queues expose drops | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F03-04 | WP-03 | target failure avoids recursive logging loops | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F04-01 | WP-04 | Invalid reload leaves previous configuration active | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F04-02 | WP-04 | external XML entities are disabled | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F04-03 | WP-04 | missing extensions produce clear diagnostics | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F05-01 | WP-05 | Failure modes are observable without crashing unrelated application paths | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F05-02 | WP-05 | adapter preserves severity/context | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-049-F05-03 | WP-05 | target coverage is explicit | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Rule short-circuiting; concurrent reload; file rotation; queue overflow; recursion; process-exit flush.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-049-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-049-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-049-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
