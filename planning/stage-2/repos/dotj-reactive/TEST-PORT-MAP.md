# DJ-028 .j Reactive: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|

No test method candidate was extracted from the sampled files. The listed test paths remain an explicit E03 mapping task.

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-028-F01-01 | WP-01 | No notification follows a terminal event | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F01-02 | WP-01 | disposal is idempotent | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F01-03 | WP-01 | synchronous errors follow the declared delivery rule | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F02-01 | WP-02 | Virtual-time traces are reproducible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F02-02 | WP-02 | cancellation removes pending work | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F02-03 | WP-02 | recursive scheduling cannot unexpectedly overflow stack | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F03-01 | WP-03 | Merge/concat/switch have distinct traces | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F03-02 | WP-03 | delayed errors preserve ordering | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F03-03 | WP-03 | unbounded operators are documented with their memory behavior | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F04-01 | WP-04 | Late subscribers see the documented terminal/replay sequence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F04-02 | WP-04 | refcount disconnects once | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F04-03 | WP-04 | concurrent observers cannot corrupt state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F05-01 | WP-05 | Push-only sources never claim native backpressure | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F05-02 | WP-05 | adapter demand is honored | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-028-F05-03 | WP-05 | every implemented operator has trace-level acceptance | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Marble/virtual-time fixtures; serialized notifications; unsubscribe races; scheduler ordering; memory retention; demand overflow.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
