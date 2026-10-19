# DJ-025 .j Container: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/Autofac.Test/ModuleTests.cs:22](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L22) | LoadsRegistrations | yes |
| [test/Autofac.Test/ModuleTests.cs:32](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L32) | DetectsNullComponentRegistryArgument | yes |
| [test/Autofac.Test/ModuleTests.cs:49](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L49) | AttachesToRegistrations | yes |
| [test/Autofac.Test/ModuleTests.cs:65](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L65) | AttachesToRegistrationsInScope | yes |
| [test/Autofac.Test/ModuleTests.cs:82](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L82) | AttachesToRegistrationsInNestedScope | yes |
| [test/Autofac.Test/ModuleTests.cs:101](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L101) | ModifiedScopesHaveTheirOwnDelegate | yes |
| [test/Autofac.Test/ModuleTests.cs:159](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L159) | TheAssemblyExposedByThisAssemblyIsTheOneContainingTheConcreteModuleClass | yes |
| [test/Autofac.Test/ModuleTests.cs:170](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L170) | IndirectlyDerivedModulesCannotUseThisAssembly | yes |
| [test/Autofac.Test/ModuleTests.cs:194](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L194) | CanUseBuilderPropertyBag | yes |
| [test/Autofac.Test/ModuleTests.cs:220](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L220) | ModuleWithoutHookDoesNotSubscribeToRegisteredEvent | yes |
| [test/Autofac.Test/ModuleTests.cs:236](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L236) | ModuleWithoutHookDoesNotSubscribeToRegistrationSourceAddedEvent | yes |
| [test/Autofac.Test/ModuleTests.cs:265](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L265) | ModuleOverridingComponentRegistrationHookSubscribesToRegisteredEvent | yes |
| [test/Autofac.Test/ModuleTests.cs:280](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L280) | ModuleOverridingComponentRegistrationHookStillReceivesRegistrations | yes |
| [test/Autofac.Test/ModuleTests.cs:294](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L294) | ModuleOverridingOnlyComponentRegistrationHookDoesNotSubscribeToRegistrationSourceAddedEvent | yes |
| [test/Autofac.Test/ModuleTests.cs:323](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L323) | ModuleOverridingRegistrationSourceHookSubscribesToRegistrationSourceAddedEvent | yes |
| [test/Autofac.Test/ModuleTests.cs:338](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L338) | ModuleOverridingOnlyRegistrationSourceHookDoesNotSubscribeToRegisteredEvent | yes |
| [test/Autofac.Test/ModuleTests.cs:364](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L364) | ModuleOverridingRegistrationSourceHookStillReceivesSources | yes |
| [test/Autofac.Test/ModuleTests.cs:400](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L400) | ModuleInheritingHookFromIntermediateBaseStillReceivesRegistrations | yes |
| [test/Autofac.Test/ModuleTests.cs:415](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L415) | ModuleInheritingHookFromIntermediateBaseSubscribesToRegisteredEvent | yes |
| [test/Autofac.Test/NamedParameterTests.cs:26](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/NamedParameterTests.cs#L26) | MatchesIdenticallyNamedParameter | yes |
| [test/Autofac.Test/NamedParameterTests.cs:47](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/NamedParameterTests.cs#L47) | DoesNotMatchDifferentlyNamedParameter | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-025-F01-01 | WP-01 | Ambiguous constructors fail deterministically | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F01-02 | WP-01 | generic constraints are enforced | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F01-03 | WP-01 | circular resolution errors identify the cycle | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F02-01 | WP-02 | Externally supplied objects remain untouched | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F02-02 | WP-02 | alias registrations dispose once | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F02-03 | WP-02 | failed activation cleans partially constructed owned dependencies | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F03-01 | WP-03 | Scanning executes no static application initialization | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F03-02 | WP-03 | activation hook failures do not leak instances | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F03-03 | WP-03 | module precedence is reproducible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F04-01 | WP-04 | Lazy/factory values respect originating scope | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F04-02 | WP-04 | metadata does not force instantiation | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F04-03 | WP-04 | unsupported final-class interception is explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F05-01 | WP-05 | Bridge differences are documented | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F05-02 | WP-05 | a disposed scope cannot admit new resolutions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-025-F05-03 | WP-05 | optional adapter creates no core-to-container dependency | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Captive dependencies; circular graphs; concurrent singleton creation; decorator ordering; async disposal adaptation.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
