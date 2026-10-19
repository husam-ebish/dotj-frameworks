# DJ-031 .j Mail: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [UnitTests/BodyPartTests.cs:42](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L42) | TestBodyPartBasic | yes |
| [UnitTests/BodyPartTests.cs:75](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L75) | TestNilSerialization | yes |
| [UnitTests/BodyPartTests.cs:104](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L104) | TestSimplePlainTextBody | yes |
| [UnitTests/BodyPartTests.cs:136](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L136) | TestBodyPartCollection | yes |
| [UnitTests/BodyPartTests.cs:204](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L204) | TestNestedBodyStructure | yes |
| [UnitTests/BodyPartTests.cs:226](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L226) | TestMultipartWithNoChildren | yes |
| [UnitTests/BodyPartTests.cs:342](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L342) | TestComplexPartSpecifiersExampleRfc3501 | yes |
| [UnitTests/EnvelopeTests.cs:37](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L37) | TestArgumentExceptions | yes |
| [UnitTests/EnvelopeTests.cs:43](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L43) | TestSerialization | yes |
| [UnitTests/EnvelopeTests.cs:69](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L69) | TestUnixAddressSerialization | yes |
| [UnitTests/EnvelopeTests.cs:92](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L92) | TestExampleEnvelopeRfc3501 | yes |
| [UnitTests/EnvelopeTests.cs:126](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L126) | TestEmptyEnvelope | yes |
| [UnitTests/EnvelopeTests.cs:137](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L137) | TestGroupAddress | yes |
| [UnitTests/EnvelopeTests.cs:153](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L153) | TestNestedGroupAddresses | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-031-F01-01 | WP-01 | Binary attachments round trip | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F01-02 | WP-01 | malformed header injection is rejected | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F01-03 | WP-01 | MimeKit coverage is not claimed from MailKit-only inspection | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F02-01 | WP-02 | Rejected recipients remain distinct | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F02-02 | WP-02 | TLS downgrade is rejected by policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F02-03 | WP-02 | lost final acknowledgment is reported as uncertain delivery | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F03-01 | WP-03 | Unsolicited updates do not corrupt command matching | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F03-02 | WP-03 | UID resets invalidate caches | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F03-03 | WP-03 | large literals stream with bounded memory | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F04-01 | WP-04 | Aborted sessions do not assume deletions committed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F04-02 | WP-04 | unsupported SASL fails explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F04-03 | WP-04 | credentials are redacted in transcripts | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F05-01 | WP-05 | Each claimed extension has transcript evidence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F05-02 | WP-05 | malformed server replies fail safely | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-031-F05-03 | WP-05 | no Java mail framework replaces owned protocol processing | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Protocol transcripts; STARTTLS downgrade; IMAP literals/IDLE; SMTP partial recipients; POP3 disconnect; internationalized addresses.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
