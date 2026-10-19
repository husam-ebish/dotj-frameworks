# DJ-031 .j Mail: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 1230 | recursive complete |
| Project-definition paths | 7 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 565 | Lexical path classification, not runnable test count |
| Sampled text files | 9 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 40 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 14 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [AotCompatibility/AotCompatibility.csproj](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/AotCompatibility/AotCompatibility.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [MailKit/MailKit.csproj](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/MailKit.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [UnitTests/UnitTests.csproj](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/UnitTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ImapClientDemo.Android/ImapClientDemo.Android/ImapClientDemo.Android.csproj](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/samples/ImapClientDemo.Android/ImapClientDemo.Android/ImapClientDemo.Android.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ImapClientDemo.iOS/ImapClientDemo.iOS/ImapClientDemo.iOS.csproj](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/samples/ImapClientDemo.iOS/ImapClientDemo.iOS/ImapClientDemo.iOS.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ImapClientDemo/ImapClientDemo/ImapClientDemo.csproj](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/samples/ImapClientDemo/ImapClientDemo/ImapClientDemo.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ImapIdle/ImapIdle/ImapIdle.csproj](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/samples/ImapIdle/ImapIdle/ImapIdle.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [MailKit/BodyPart.cs:48](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/BodyPart.cs#L48) | `public abstract class BodyPart` |
| [MailKit/BodyPart.cs:63](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/BodyPart.cs#L63) | `protected BodyPart (ContentType contentType, string partSpecifier)` |
| [MailKit/BodyPart.cs:82](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/BodyPart.cs#L82) | `public ContentType ContentType {` |
| [MailKit/BodyPart.cs:96](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/BodyPart.cs#L96) | `public string PartSpecifier {` |
| [MailKit/BodyPart.cs:115](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/BodyPart.cs#L115) | `public abstract void Accept (BodyPartVisitor visitor);` |
| [MailKit/BodyPart.cs:251](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/BodyPart.cs#L251) | `protected abstract void Encode (StringBuilder builder);` |
| [MailKit/BodyPart.cs:764](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/BodyPart.cs#L764) | `public static bool TryParse (string text, out BodyPart? part)` |
| [MailKit/Envelope.cs:48](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L48) | `public class Envelope` |
| [MailKit/Envelope.cs:56](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L56) | `public Envelope ()` |
| [MailKit/Envelope.cs:73](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L73) | `public InternetAddressList From {` |
| [MailKit/Envelope.cs:85](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L85) | `public InternetAddressList Sender {` |
| [MailKit/Envelope.cs:97](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L97) | `public InternetAddressList ReplyTo {` |
| [MailKit/Envelope.cs:108](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L108) | `public InternetAddressList To {` |
| [MailKit/Envelope.cs:119](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L119) | `public InternetAddressList Cc {` |
| [MailKit/Envelope.cs:130](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L130) | `public InternetAddressList Bcc {` |
| [MailKit/Envelope.cs:141](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L141) | `public string? InReplyTo {` |
| [MailKit/Envelope.cs:152](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L152) | `public DateTimeOffset? Date {` |
| [MailKit/Envelope.cs:163](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L163) | `public string? MessageId {` |
| [MailKit/Envelope.cs:174](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L174) | `public string? Subject {` |
| [MailKit/Envelope.cs:620](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/MailKit/Envelope.cs#L620) | `public static bool TryParse (string text, out Envelope? envelope)` |
| [UnitTests/BodyPartTests.cs:39](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L39) | `public class BodyPartTests` |
| [UnitTests/BodyPartTests.cs:42](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L42) | `public void TestBodyPartBasic ()` |
| [UnitTests/BodyPartTests.cs:75](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L75) | `public void TestNilSerialization ()` |
| [UnitTests/BodyPartTests.cs:104](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L104) | `public void TestSimplePlainTextBody ()` |
| [UnitTests/BodyPartTests.cs:136](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L136) | `public void TestBodyPartCollection ()` |
| [UnitTests/BodyPartTests.cs:204](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L204) | `public void TestNestedBodyStructure ()` |
| [UnitTests/BodyPartTests.cs:226](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L226) | `public void TestMultipartWithNoChildren ()` |
| [UnitTests/BodyPartTests.cs:304](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L304) | `public override void Visit (BodyPart body)` |
| [UnitTests/BodyPartTests.cs:312](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L312) | `protected internal override void VisitBodyPart (BodyPart entity)` |
| [UnitTests/BodyPartTests.cs:321](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L321) | `protected override void VisitMessage (BodyPart message)` |
| [UnitTests/BodyPartTests.cs:328](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L328) | `protected override void VisitChildren (BodyPartMultipart multipart)` |
| [UnitTests/BodyPartTests.cs:342](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/BodyPartTests.cs#L342) | `public void TestComplexPartSpecifiersExampleRfc3501 ()` |
| [UnitTests/EnvelopeTests.cs:34](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L34) | `public class EnvelopeTests` |
| [UnitTests/EnvelopeTests.cs:37](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L37) | `public void TestArgumentExceptions ()` |
| [UnitTests/EnvelopeTests.cs:43](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L43) | `public void TestSerialization ()` |
| [UnitTests/EnvelopeTests.cs:69](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L69) | `public void TestUnixAddressSerialization ()` |
| [UnitTests/EnvelopeTests.cs:92](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L92) | `public void TestExampleEnvelopeRfc3501 ()` |
| [UnitTests/EnvelopeTests.cs:126](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L126) | `public void TestEmptyEnvelope ()` |
| [UnitTests/EnvelopeTests.cs:137](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L137) | `public void TestGroupAddress ()` |
| [UnitTests/EnvelopeTests.cs:153](https://github.com/jstedfast/MailKit/blob/7418d38dc27a47d8db9108d8fa994b2b784f1578/UnitTests/EnvelopeTests.cs#L153) | `public void TestNestedGroupAddresses ()` |

Full lexical records (40) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | MIME dependency and message model | MimeMessageContract; HeaderField; BodyPart |
| WP-02 | SMTP session and delivery outcomes | SmtpSession; RecipientStatus; DeliveryResult |
| WP-03 | IMAP folders synchronization and search | ImapCommand; FolderState; UidValidity; SearchQuery |
| WP-04 | POP3 and authentication adapters | Pop3Session; MessageId; SaslMechanism |
| WP-05 | Protocol interoperability and resource limits | MailServerProfile; TranscriptFixture; MimeQuota |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
