# DJ-018 .j Services: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/CoreWCF.Http/tests/ByRefTests.cs:24](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Http/tests/ByRefTests.cs#L24) | ByRefParams | yes |
| [src/CoreWCF.Http/tests/ByRefTests.cs:105](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Http/tests/ByRefTests.cs#L105) | ConfigureServices | not confirmed |
| [src/CoreWCF.Http/tests/ByRefTests.cs:110](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Http/tests/ByRefTests.cs#L110) | Configure | not confirmed |
| [src/CoreWCF.WebHttp/tests/SslTests.cs:25](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.WebHttp/tests/SslTests.cs#L25) | SslWorks | yes |
| [src/CoreWCF.WebHttp/tests/SslTests.cs:44](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.WebHttp/tests/SslTests.cs#L44) | ConfigureServices | not confirmed |
| [src/CoreWCF.WebHttp/tests/SslTests.cs:49](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.WebHttp/tests/SslTests.cs#L49) | Configure | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-018-F01-01 | WP-01 | Ambiguous operations fail at host startup | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F01-02 | WP-01 | per-call instances are disposed once | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F01-03 | WP-01 | unhandled exceptions do not disclose stack traces by default | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F02-01 | WP-02 | Stopping a host rejects new work and bounds draining | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F02-02 | WP-02 | binding limits are enforced before deserialization | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F02-03 | WP-02 | client codecs do not depend on server dispatch | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F03-01 | WP-03 | Exported metadata reimports into reference clients | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F03-02 | WP-03 | inspector failures have defined cleanup | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F03-03 | WP-03 | behavior order is deterministic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F04-01 | WP-04 | Unauthorized operations never invoke service code | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F04-02 | WP-04 | unavailable impersonation fails explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F04-03 | WP-04 | timeouts do not claim a committed transaction was rolled back | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F05-01 | WP-05 | Every supported binding has bidirectional fault/streaming evidence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F05-02 | WP-05 | resource use remains bounded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-018-F05-03 | WP-05 | unsupported WS-* profiles remain enumerated | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

.NET clients against Java hosts; concurrent instances; SOAP faults; WSDL import; channel abort and authorization.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
