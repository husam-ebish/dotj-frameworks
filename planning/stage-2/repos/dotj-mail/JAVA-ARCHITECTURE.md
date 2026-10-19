# DJ-031 .j Mail: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Implement IMAP, POP3 and SMTP client behavior including authentication and message transport.

Product type: JVM messaging/protocol library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-mail-01 | MimeMessageContract, HeaderField, BodyPart | MIME dependency and message model |
| dotj-mail-02 | SmtpSession, RecipientStatus, DeliveryResult | SMTP session and delivery outcomes |
| dotj-mail-03 | ImapCommand, FolderState, UidValidity, SearchQuery | IMAP folders synchronization and search |
| dotj-mail-04 | Pop3Session, MessageId, SaslMechanism | POP3 and authentication adapters |
| dotj-mail-05 | MailServerProfile, TranscriptFixture, MimeQuota | Protocol interoperability and resource limits |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

MIME composition/parsing dependency must be owned or explicitly approved; MailKit's dependency on MimeKit is outside the starting 66.

## Feature contracts and invariants

### WP-01: MIME dependency and message model

Internal analysis vocabulary (not permission to rename the public API): `MimeMessageContract`, `HeaderField`, `BodyPart`.

Inventory MimeKit as a separately owned missing dependency. Define headers encodings multipart boundaries and streaming ownership. Separate raw preservation from normalized message generation.

Required observable invariant: Binary attachments round trip; malformed header injection is rejected; MimeKit coverage is not claimed from MailKit-only inspection.

### WP-02: SMTP session and delivery outcomes

Internal analysis vocabulary (not permission to rename the public API): `SmtpSession`, `RecipientStatus`, `DeliveryResult`.

Model greeting EHLO STARTTLS authentication and DATA states. Preserve per-recipient partial acceptance and final server replies. Specify cancellation and ambiguous delivery after connection loss.

Required observable invariant: Rejected recipients remain distinct; TLS downgrade is rejected by policy; lost final acknowledgment is reported as uncertain delivery.

### WP-03: IMAP folders synchronization and search

Internal analysis vocabulary (not permission to rename the public API): `ImapCommand`, `FolderState`, `UidValidity`, `SearchQuery`.

Handle tagged replies unsolicited updates literals and capabilities. Track UIDVALIDITY and incremental synchronization state. Define IDLE cancellation and command serialization.

Required observable invariant: Unsolicited updates do not corrupt command matching; UID resets invalidate caches; large literals stream with bounded memory.

### WP-04: POP3 and authentication adapters

Internal analysis vocabulary (not permission to rename the public API): `Pop3Session`, `MessageId`, `SaslMechanism`.

Implement POP3 state and deferred deletion semantics. Use explicit SASL mechanism negotiation and credential handling. Isolate platform-specific authentication dependencies.

Required observable invariant: Aborted sessions do not assume deletions committed; unsupported SASL fails explicitly; credentials are redacted in transcripts.

### WP-05: Protocol interoperability and resource limits

Internal analysis vocabulary (not permission to rename the public API): `MailServerProfile`, `TranscriptFixture`, `MimeQuota`.

Run controlled SMTP IMAP POP3 reference servers. Test fragmented responses oversized messages and timeout races. Verify disposal of messages streams and pooled connections.

Required observable invariant: Each claimed extension has transcript evidence; malformed server replies fail safely; no Java mail framework replaces owned protocol processing.

## Bootstrap and dependency boundaries

Sockets, SSLEngine, JCA and streaming I/O.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing MailKit usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `MimeMessageContract` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Binary attachments round trip; malformed header injection is rejected; MimeKit coverage is not claimed from MailKit-only inspection. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
