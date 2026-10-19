# DJ-065 .j Mediator: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/MediatR.Tests/SendTests.cs:50](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L50) | Handle | not confirmed |
| [test/MediatR.Tests/SendTests.cs:68](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L68) | Handle | not confirmed |
| [test/MediatR.Tests/SendTests.cs:89](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L89) | Handle | not confirmed |
| [test/MediatR.Tests/SendTests.cs:107](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L107) | Handle | not confirmed |
| [test/MediatR.Tests/SendTests.cs:126](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L126) | Handle | not confirmed |
| [test/MediatR.Tests/SendTests.cs:158](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L158) | Handle | not confirmed |
| [test/MediatR.Tests/SendTests.cs:168](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L168) | Handle | not confirmed |
| [test/MediatR.Tests/SendTests.cs:191](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L191) | Handle | not confirmed |
| [test/MediatR.Tests/SendTests.cs:205](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L205) | Handle | not confirmed |
| [test/MediatR.Tests/SendTests.cs:215](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L215) | Should_resolve_main_handler | yes |
| [test/MediatR.Tests/SendTests.cs:223](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L223) | Should_resolve_main_void_handler | yes |
| [test/MediatR.Tests/SendTests.cs:231](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L231) | Should_resolve_main_handler_via_dynamic_dispatch | yes |
| [test/MediatR.Tests/SendTests.cs:241](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L241) | Should_resolve_main_void_handler_via_dynamic_dispatch | yes |
| [test/MediatR.Tests/SendTests.cs:252](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L252) | Should_resolve_main_handler_by_specific_interface | yes |
| [test/MediatR.Tests/SendTests.cs:260](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L260) | Should_resolve_main_handler_by_given_interface | yes |
| [test/MediatR.Tests/SendTests.cs:270](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L270) | Should_raise_execption_on_null_request | yes |
| [test/MediatR.Tests/SendTests.cs:273](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L273) | Should_resolve_generic_handler | yes |
| [test/MediatR.Tests/SendTests.cs:285](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L285) | Should_resolve_generic_void_handler | yes |
| [test/MediatR.Tests/SendTests.cs:294](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L294) | Should_resolve_multiple_type_parameter_generic_handler | yes |
| [test/MediatR.Tests/SendTests.cs:303](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L303) | Should_resolve_closed_handler_if_defined | yes |
| [test/MediatR.Tests/SendTests.cs:327](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L327) | Should_resolve_open_handler_if_not_defined | yes |
| [test/MediatR.Tests/SendTests.cs:350](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L350) | TimeoutBehavior_Void_Should_Cancel_Long_Running_Task_And_Throw_Exception | yes |
| [test/MediatR.Tests/SendTests.cs:362](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L362) | TimeoutBehavior_NonVoid_Should_Cancel_Long_Running_Task_And_Throw_Exception | yes |
| [test/MediatR.Tests/UnitTests.cs:12](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/UnitTests.cs#L12) | Should_be_equal_to_each_other | yes |
| [test/MediatR.Tests/UnitTests.cs:23](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/UnitTests.cs#L23) | Should_be_equitable | yes |
| [test/MediatR.Tests/UnitTests.cs:34](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/UnitTests.cs#L34) | Should_tostring | yes |
| [test/MediatR.Tests/UnitTests.cs:41](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/UnitTests.cs#L41) | Should_compareto_as_zero | yes |
| [test/MediatR.Tests/UnitTests.cs:70](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/UnitTests.cs#L70) | Should_be_equal | yes |
| [test/MediatR.Tests/UnitTests.cs:82](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/UnitTests.cs#L82) | Should_compareto_value_as_zero | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-065-F01-01 | WP-01 | Source reuse waits for rights resolution | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F01-02 | WP-01 | missing/multiple handlers fail explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F01-03 | WP-01 | generic request identity survives erasure through tokens | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F02-01 | WP-02 | Behavior order is deterministic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F02-02 | WP-02 | cleanup runs on failure | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F02-03 | WP-02 | exception handling cannot accidentally invoke the request twice | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F03-01 | WP-03 | Parallel failures are not lost | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F03-02 | WP-03 | sequential strategy has stable ordering | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F03-03 | WP-03 | scoped handlers are disposed after completion | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F04-01 | WP-04 | Early termination closes owned resources | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F04-02 | WP-04 | exceptions preserve stream context | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F04-03 | WP-04 | no hidden unbounded buffering is introduced | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F05-01 | WP-05 | Base mediator works with explicit factories | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F05-02 | WP-05 | no event bus is substituted | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-065-F05-03 | WP-05 | rights status and compatibility evidence remain separate | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Single handler resolution; nested sends; pipeline ordering; notification failures; cancellation; stream termination.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
