# DJ-031 .j Mail: feature compatibility matrix

MIME composition/parsing dependency must be owned or explicitly approved; MailKit's dependency on MimeKit is outside the starting 66.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | MIME dependency and message model | Proposed Java contracts: MimeMessageContract, HeaderField, BodyPart | Binary attachments round trip; malformed header injection is rejected; MimeKit coverage is not claimed from MailKit-only inspection | Planned; evidence gates open |
| WP-02 | SMTP session and delivery outcomes | Proposed Java contracts: SmtpSession, RecipientStatus, DeliveryResult | Rejected recipients remain distinct; TLS downgrade is rejected by policy; lost final acknowledgment is reported as uncertain delivery | Planned; evidence gates open |
| WP-03 | IMAP folders synchronization and search | Proposed Java contracts: ImapCommand, FolderState, UidValidity, SearchQuery | Unsolicited updates do not corrupt command matching; UID resets invalidate caches; large literals stream with bounded memory | Planned; evidence gates open |
| WP-04 | POP3 and authentication adapters | Proposed Java contracts: Pop3Session, MessageId, SaslMechanism | Aborted sessions do not assume deletions committed; unsupported SASL fails explicitly; credentials are redacted in transcripts | Planned; evidence gates open |
| WP-05 | Protocol interoperability and resource limits | Proposed Java contracts: MailServerProfile, TranscriptFixture, MimeQuota | Each claimed extension has transcript evidence; malformed server replies fail safely; no Java mail framework replaces owned protocol processing | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

MimeKit is a newly identified source dependency candidate; DKIM/S/MIME and platform auth may require more than MailKit scope.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
