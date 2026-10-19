# DJ-001 .j Core: feature compatibility matrix

Define decimal, unsigned numeric, culture, DateTime, encoding, exception and disposal semantics; Java erasure and memory-model differences preclude CLR binary compatibility.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Foundation types and ownership | Proposed Java contracts: TypeToken<T>, Outcome<T>, AsyncCloseable, explicit ContextSnapshot | Equal parameterized types share identity; different generic arguments do not; supplied resources are never closed implicitly; context values do not leak between requests | Planned; evidence gates open |
| WP-02 | Cancellation and asynchronous operations | Proposed Java contracts: CancellationToken, CancellationSource, Registration, Deadline | Late registration runs synchronously; sequential callbacks use the declared LIFO profile; self-close cannot deadlock; cancelAsync completion waits for callbacks; token identity survives source disposal as specified | Planned; evidence gates open |
| WP-03 | Default DI and configuration | Proposed Java contracts: ServiceKey<T>, ServiceDescriptor, Scope, ConfigValue, ConfigurationRoot | Concurrent singleton resolves return one published identity; aliases close once; supplied singleton stays caller-owned; empty-provider writes fail; failed reload does not acquire an invented atomic guarantee | Planned; evidence gates open |
| WP-04 | Options logging and hosting | Proposed Java contracts: OptionsFactory<T>, OptionsMonitor<T>, Logger, HostedService, Host | Invalid options never publish as valid; monitor close removes subscriptions; disabled log handling follows declared formatter behavior; partial host startup releases completed services in defined order | Planned; evidence gates open |
| WP-05 | Numeric text and time compatibility | Proposed Java contracts: DotjDecimal, DotjDateTime, EncodingProfile, CultureProfile | Decimal bit-preserving paths retain scale/sign; invalid byte sequences follow explicit modes; Turkish casing and DST ambiguity are fixture-covered; Instant conversion cannot discard unspecified Kind silently | Planned; evidence gates open |
| WP-06 | Collections LINQ and expression services | Proposed Java contracts: Sequence<T>, QueryExpression, ExpressionVisitor, CollectionAdapters | Enumerator disposal and deferred exceptions match profiles; grouping/null/equality differences are explicit; query IR round trips preserve node types and constants; provider translation has no silent client execution | Planned; evidence gates open |
| WP-07 | I/O networking and data contracts | Proposed Java contracts: OwnedStream, Pipe, HttpMessage, SocketChannelAdapter, DataRecord | Partial reads/writes and half-closes retain data; bounded buffers enforce backpressure; file handles close on failure; network cancellation does not imply rollback; unsupported distributed enlistment fails explicitly | Planned; evidence gates open |
| WP-08 | Formats serialization security and reflection | Proposed Java contracts: SystemJsonProfile, XmlModel, CryptoProvider, MetadataReader, ReflectionAdapter | System.Text.Json tests cannot be satisfied merely by Newtonsoft behavior; unsafe type activation is disabled; signature bytes and canonicalization use vectors; CLR assembly execution is never claimed from metadata parsing | Planned; evidence gates open |
| WP-09 | Native runtime and complete BCL disposition | Proposed Java contracts: PlatformCapability, NativeBinding, RuntimeCapabilityMatrix | All 218 known library directories have ownership and test routes; unsupported backend calls report capability gaps; no custom VM is assumed; a backend remains blocked until a reproducible execution experiment succeeds | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Which base APIs need adapters rather than direct JDK usage? Keep reflection emit, unsafe pointers, intrinsics and NativeAOT as explicit feasibility items.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
