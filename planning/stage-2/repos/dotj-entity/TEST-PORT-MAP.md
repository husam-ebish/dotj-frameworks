# DJ-019 .j Entity: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/EFCore.Proxies.Tests/ProxyTests.cs:13](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L13) | Materialization_uses_parameterless_constructor | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:28](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L28) | Materialization_uses_parameterized_constructor | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:47](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L47) | Materialization_uses_parameterized_constructor_taking_context | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:67](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L67) | CreateProxy_works_for_shared_type_entity_types | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:76](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L76) | CreateProxy_works_for_record_with_base_type_entity_types | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:85](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L85) | CreateProxy_throws_for_shared_type_entity_types_when_entity_type_name_not_known | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:103](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L103) | CreateProxy_works_for_owned_but_not_weak_entity_types | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:113](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L113) | CreateProxy_uses_parameterless_constructor | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:120](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L120) | CreateProxy_uses_parameterized_constructor | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:131](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L131) | CreateProxy_uses_parameterized_constructor_taking_context | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:143](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L143) | Proxies_only_created_if_Use_called | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:173](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L173) | Proxy_services_must_be_available | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:204](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L204) | Throws_if_type_not_available_to_Castle | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:211](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L211) | Throws_if_constructor_not_available_to_Castle | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:218](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L218) | CreateProxy_throws_if_constructor_args_do_not_match | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:225](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L225) | CreateProxy_throws_if_wrong_number_of_constructor_args | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:232](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L232) | Throws_if_create_proxy_for_non_mapped_type | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:241](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L241) | Throws_if_create_proxy_when_proxies_not_used | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:250](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L250) | Throws_if_create_proxy_when_proxies_not_enabled | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:259](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L259) | Throws_if_attempt_to_create_EntityType_based_on_proxy_class | yes |
| [test/EFCore.Proxies.Tests/ProxyTests.cs:273](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Proxies.Tests/ProxyTests.cs#L273) | Throws_if_attempt_to_add_proxy_type_to_model_builder | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:25](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L25) | Log_with_default_options | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:34](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L34) | Log_with_minimum_level | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:43](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L43) | Log_for_multiple_categories | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:57](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L57) | Log_for_single_category | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:71](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L71) | Log_for_single_category_and_minimum_level | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:97](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L97) | Log_for_single_event | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:111](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L111) | Log_for_multiple_events | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:125](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L125) | Log_for_many_events | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:146](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L146) | Log_for_single_event_and_minimum_level | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:172](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L172) | Log_with_custom_filter | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:182](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L182) | Log_with_custom_logger | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:196](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L196) | Log_with_raw_message | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:208](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L208) | Log_raw_single_line | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:220](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L220) | Log_default_single_line | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:235](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L235) | Log_only_level | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:248](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L248) | Log_only_local_time | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:261](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L261) | Log_only_UTC_time | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:274](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L274) | Log_only_ID | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:287](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L287) | Log_only_category | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:300](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L300) | Log_level_and_ID | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:314](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L314) | Log_level_and_UTC | yes |
| [test/EFCore.Tests/DbContextLoggerTests.cs:331](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Tests/DbContextLoggerTests.cs#L331) | Log_default_UTC | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-019-F01-01 | WP-01 | Ambiguous keys and unsupported mappings fail at model build | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F01-02 | WP-01 | snapshots are deterministic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F01-03 | WP-01 | Java lambda bodies are not falsely treated as inspectable expressions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F02-01 | WP-02 | Injection payloads remain parameters | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F02-02 | WP-02 | null-sensitive joins match reference cases | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F02-03 | WP-02 | unsupported operations never silently load an entire table | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F03-01 | WP-03 | One tracked key has one identity | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F03-02 | WP-03 | relationship changes yield explainable updates | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F03-03 | WP-03 | stale tokens produce conflicts without lost updates | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F04-01 | WP-04 | Failed saves preserve documented tracking state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F04-02 | WP-04 | database transactions remain caller-owned when supplied | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F04-03 | WP-04 | unknown commit outcome is not reported as safe retry | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F05-01 | WP-05 | Schema diff handles renames only with evidence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F05-02 | WP-05 | history prevents duplicate application | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F05-03 | WP-05 | failed migrations report actual transaction boundary | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F06-01 | WP-06 | N+1 patterns are visible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F06-02 | WP-06 | tools reproduce locked schema output | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-019-F06-03 | WP-06 | no Hibernate or other Java ORM replaces the planned implementation | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

SQL/null semantics; identity maps; relationship fixup; optimistic concurrency; migration diffs; transaction/savepoint rollback.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
