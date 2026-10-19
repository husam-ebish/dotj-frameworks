# DJ-026 .j Validation: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/FluentValidation.Tests/RulesetTests.cs:32](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L32) | Executes_rules_in_specified_ruleset | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:41](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L41) | Executes_rules_not_specified_in_ruleset | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:50](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L50) | Ruleset_cascades_to_child_validator | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:73](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L73) | Ruleset_cascades_to_child_collection_validator | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:97](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L97) | Executes_multiple_rulesets | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:111](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L111) | Executes_all_rules | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:120](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L120) | Executes_rules_in_default_ruleset_and_specific_ruleset | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:133](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L133) | WithMessage_works_inside_rulesets | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:141](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L141) | Ruleset_selection_should_not_cascade_downwards_when_set_on_property | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:149](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L149) | Ruleset_selection_should_cascade_downwards_with_when_setting_child_validator_using_include_statement | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:157](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L157) | Ruleset_selection_should_cascade_downwards_with_when_setting_child_validator_using_include_statement_with_lambda | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:166](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L166) | Trims_spaces | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:181](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L181) | Applies_multiple_rulesets_to_rule | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:205](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L205) | Executes_in_rule_in_ruleset_and_default | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:225](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L225) | Executes_in_rule_in_default_and_none | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:238](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L238) | Combines_rulesets_and_explicit_properties | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:257](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L257) | Combines_rulesets_and_explicit_properties_async | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:276](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L276) | Includes_combination_of_rulesets | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:296](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L296) | Includes_combination_of_rulesets_async | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:316](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L316) | Includes_all_rulesets | yes |
| [src/FluentValidation.Tests/RulesetTests.cs:334](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L334) | Includes_all_rulesets_async | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:29](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L29) | Validation_should_succeed_when_condition_does_not_match | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:36](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L36) | Validation_should_succeed_when_async_condition_does_not_match | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:43](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L43) | Validation_should_fail_when_condition_matches | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:50](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L50) | Validation_should_fail_when_async_condition_matches | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:57](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L57) | Validation_should_succeed_when_condition_matches | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:64](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L64) | Validation_should_succeed_when_async_condition_matches | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:71](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L71) | Validation_should_fail_when_condition_does_not_match | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:78](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L78) | Validation_should_fail_when_async_condition_does_not_match | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:85](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L85) | Condition_is_applied_to_all_validators_in_the_chain | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:95](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L95) | Async_condition_is_applied_to_all_validators_in_the_chain | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:105](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L105) | Async_condition_is_applied_to_all_validators_in_the_chain_when_executed_synchronously | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:115](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L115) | Sync_condition_is_applied_to_async_validators | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:128](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L128) | Condition_is_applied_to_single_validator_in_the_chain_when_ApplyConditionTo_set_to_CurrentValidator | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:138](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L138) | Async_condition_is_applied_to_single_validator_in_the_chain_when_ApplyConditionTo_set_to_CurrentValidator | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:148](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L148) | Async_condition_throws_when_executed_synchronosuly_with_synchronous_role | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:158](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L158) | Async_condition_throws_when_executed_synchronosuly_with_asynchronous_rule | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:168](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L168) | Async_condition_throws_when_executed_synchronosuly_with_synchronous_collection_role | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:177](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L177) | Async_condition_throws_when_invoked_synchronosuly_with_asynchronous_collection_rule | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:187](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L187) | Can_access_property_value_in_custom_condition | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:201](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L201) | Can_access_property_value_in_custom_condition_foreach | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:215](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L215) | Can_try_access_property_value_in_custom_condition | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:235](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L235) | Can_try_access_property_value_in_custom_condition_foreach | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:256](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L256) | Can_access_property_path_in_condition | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:271](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L271) | Can_access_nested_property_path_in_condition | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:287](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L287) | Can_access_collection_item_property_path_in_condition | yes |
| [src/FluentValidation.Tests/ConditionTests.cs:304](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L304) | Can_access_property_path_in_child_rules_condition | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-026-F01-01 | WP-01 | Rule ordering is deterministic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F01-02 | WP-01 | nested paths preserve collection indices | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F01-03 | WP-01 | concurrent validations do not share mutable request state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F02-01 | WP-02 | Null-versus-empty behavior matches its profile | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F02-02 | WP-02 | locale changes do not alter invariant constraints | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F02-03 | WP-02 | pathological patterns obey declared resource limits | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F03-01 | WP-03 | Cancellation prevents later rules where promised | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F03-02 | WP-03 | child failures retain paths | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F03-03 | WP-03 | thrown application errors are not misreported as ordinary invalid input | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F04-01 | WP-04 | Missing translations use documented fallback | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F04-02 | WP-04 | custom failures preserve codes/severity | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F04-03 | WP-04 | passwords are not included in default messages | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F05-01 | WP-05 | Core validation runs without web dependencies | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F05-02 | WP-05 | API responses retain stable field paths | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-026-F05-03 | WP-05 | upstream unsupported rules remain explicit inventory entries | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Cascade ordering; nested collections; conditions; asynchronous cancellation; localized messages; error-path stability.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
