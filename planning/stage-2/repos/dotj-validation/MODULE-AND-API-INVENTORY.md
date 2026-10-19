# DJ-026 .j Validation: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 296 | recursive complete |
| Project-definition paths | 4 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 80 | Lexical path classification, not runnable test count |
| Sampled text files | 9 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 70 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 47 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/FluentValidation.Tests.Benchmarks/FluentValidation.Tests.Benchmarks.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests.Benchmarks/FluentValidation.Tests.Benchmarks.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/FluentValidation.Tests/FluentValidation.Tests.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/FluentValidation.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/FluentValidation/FluentValidation.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/FluentValidation.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/FluentValidation/Enums.cs:26](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/Enums.cs#L26) | `public enum CascadeMode {` |
| [src/FluentValidation/Enums.cs:43](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/Enums.cs#L43) | `public enum ApplyConditionTo {` |
| [src/FluentValidation/Enums.cs:57](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/Enums.cs#L57) | `public enum Severity {` |
| [src/FluentValidation/Syntax.cs:29](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/Syntax.cs#L29) | `public interface IRuleBuilderInitial<T, out TProperty> : IRuleBuilder<T, TProperty> {` |
| [src/FluentValidation/Syntax.cs:37](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/Syntax.cs#L37) | `public interface IRuleBuilder<T, out TProperty> {` |
| [src/FluentValidation/Syntax.cs:82](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/Syntax.cs#L82) | `public interface IRuleBuilderOptions<T, out TProperty> : IRuleBuilder<T, TProperty> {` |
| [src/FluentValidation/Syntax.cs:94](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/Syntax.cs#L94) | `public interface IRuleBuilderOptionsConditions<T, out TProperty> : IRuleBuilder<T, TProperty> {` |
| [src/FluentValidation/Syntax.cs:106](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/Syntax.cs#L106) | `public interface IRuleBuilderInitialCollection<T, TElement> : IRuleBuilder<T, TElement> {` |
| [src/FluentValidation/Syntax.cs:113](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/Syntax.cs#L113) | `public interface IConditionBuilder {` |
| [src/FluentValidation.Tests/RulesetTests.cs:28](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L28) | `public class RulesetTests {` |
| [src/FluentValidation.Tests/RulesetTests.cs:32](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L32) | `public void Executes_rules_in_specified_ruleset() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:41](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L41) | `public void Executes_rules_not_specified_in_ruleset() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:50](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L50) | `public void Ruleset_cascades_to_child_validator() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:73](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L73) | `public void Ruleset_cascades_to_child_collection_validator() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:97](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L97) | `public void Executes_multiple_rulesets() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:111](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L111) | `public void Executes_all_rules() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:120](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L120) | `public void Executes_rules_in_default_ruleset_and_specific_ruleset() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:133](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L133) | `public void WithMessage_works_inside_rulesets() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:141](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L141) | `public void Ruleset_selection_should_not_cascade_downwards_when_set_on_property() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:149](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L149) | `public void Ruleset_selection_should_cascade_downwards_with_when_setting_child_validator_using_include_statement() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:157](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L157) | `public void Ruleset_selection_should_cascade_downwards_with_when_setting_child_validator_using_include_statement_with_lambda() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:166](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L166) | `public void Trims_spaces() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:181](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L181) | `public void Applies_multiple_rulesets_to_rule() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:205](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L205) | `public void Executes_in_rule_in_ruleset_and_default() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:225](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L225) | `public void Executes_in_rule_in_default_and_none() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:238](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L238) | `public void Combines_rulesets_and_explicit_properties() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:257](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L257) | `public async Task Combines_rulesets_and_explicit_properties_async() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:276](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L276) | `public void Includes_combination_of_rulesets() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:296](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L296) | `public async Task Includes_combination_of_rulesets_async() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:316](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L316) | `public void Includes_all_rulesets() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:334](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L334) | `public async Task Includes_all_rulesets_async() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:357](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L357) | `public TestValidator() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:369](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L369) | `public TestValidator2()` |
| [src/FluentValidation.Tests/RulesetTests.cs:380](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L380) | `public class TestValidator3 : AbstractValidator<Person> {` |
| [src/FluentValidation.Tests/RulesetTests.cs:381](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L381) | `public TestValidator3() {` |
| [src/FluentValidation.Tests/RulesetTests.cs:387](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L387) | `public class PersonContainer {` |
| [src/FluentValidation.Tests/RulesetTests.cs:388](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L388) | `public Person Person { get; set; }` |
| [src/FluentValidation.Tests/RulesetTests.cs:391](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L391) | `public class TestValidator4 : AbstractValidator<PersonContainer>` |
| [src/FluentValidation.Tests/RulesetTests.cs:393](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/RulesetTests.cs#L393) | `public TestValidator4()` |
| [src/FluentValidation.Tests/ConditionTests.cs:27](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L27) | `public class ConditionTests {` |
| [src/FluentValidation.Tests/ConditionTests.cs:29](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L29) | `public void Validation_should_succeed_when_condition_does_not_match() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:36](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L36) | `public async Task Validation_should_succeed_when_async_condition_does_not_match() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:43](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L43) | `public void Validation_should_fail_when_condition_matches() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:50](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L50) | `public async Task Validation_should_fail_when_async_condition_matches() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:57](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L57) | `public void Validation_should_succeed_when_condition_matches() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:64](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L64) | `public async Task Validation_should_succeed_when_async_condition_matches() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:71](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L71) | `public void Validation_should_fail_when_condition_does_not_match() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:78](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L78) | `public async Task Validation_should_fail_when_async_condition_does_not_match() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:85](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L85) | `public void Condition_is_applied_to_all_validators_in_the_chain() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:95](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L95) | `public async Task Async_condition_is_applied_to_all_validators_in_the_chain() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:105](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L105) | `public void Async_condition_is_applied_to_all_validators_in_the_chain_when_executed_synchronously() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:115](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L115) | `public async Task Sync_condition_is_applied_to_async_validators() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:128](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L128) | `public void Condition_is_applied_to_single_validator_in_the_chain_when_ApplyConditionTo_set_to_CurrentValidator() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:138](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L138) | `public async Task Async_condition_is_applied_to_single_validator_in_the_chain_when_ApplyConditionTo_set_to_CurrentValidator() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:148](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L148) | `public void Async_condition_throws_when_executed_synchronosuly_with_synchronous_role() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:158](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L158) | `public void Async_condition_throws_when_executed_synchronosuly_with_asynchronous_rule() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:168](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L168) | `public void Async_condition_throws_when_executed_synchronosuly_with_synchronous_collection_role() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:177](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L177) | `public void Async_condition_throws_when_invoked_synchronosuly_with_asynchronous_collection_rule() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:187](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L187) | `public void Can_access_property_value_in_custom_condition() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:201](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L201) | `public void Can_access_property_value_in_custom_condition_foreach() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:215](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L215) | `public void Can_try_access_property_value_in_custom_condition() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:235](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L235) | `public void Can_try_access_property_value_in_custom_condition_foreach() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:256](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L256) | `public void Can_access_property_path_in_condition() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:271](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L271) | `public void Can_access_nested_property_path_in_condition() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:287](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L287) | `public void Can_access_collection_item_property_path_in_condition() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:304](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L304) | `public void Can_access_property_path_in_child_rules_condition() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:335](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L335) | `public TestConditionValidator() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:341](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L341) | `public TestConditionAsyncValidator() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:347](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L347) | `public InverseConditionValidator() {` |
| [src/FluentValidation.Tests/ConditionTests.cs:353](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests/ConditionTests.cs#L353) | `public InverseConditionAsyncValidator() {` |

Full lexical records (70) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | Rule model and fluent construction | Validator; Rule; PropertyPath; RuleSet |
| WP-02 | Built-in validators and comparisons | Constraint; ComparisonContext; MessageArgument |
| WP-03 | Asynchronous and child validation | ValidationContext; AsyncRule; ChildValidator |
| WP-04 | Messages localization and extensibility | MessageCatalog; CustomValidator; FailureFormatter |
| WP-05 | Web integration and regression acceptance | ValidationAdapter; ValidationResult; RuleCoverage |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
