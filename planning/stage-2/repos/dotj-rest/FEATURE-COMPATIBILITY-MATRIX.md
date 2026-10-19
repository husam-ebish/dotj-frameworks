# DJ-032 .j REST: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Preserve encoding, multipart, errors and cancellation behavior; Java transport redirect/cookie defaults must not silently replace source defaults.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Request model and URI construction | Internal planning vocabulary (verify upstream public identity): RestRequest, Parameter, ResourcePath | Reserved characters survive expected encoding; duplicate headers follow policy; concurrent calls do not mutate a shared request unexpectedly | Planned; evidence gates open |
| WP-02 | Transport and response lifecycle | Internal planning vocabulary (verify upstream public identity): RestClient, Response, ResponseBody | Non-success HTTP can retain its body; cancellation closes owned streams; response resources are released on conversion failure | Planned; evidence gates open |
| WP-03 | Serialization and multipart bodies | Internal planning vocabulary (verify upstream public identity): BodySerializer, MultipartPart, ContentType | Binary parts preserve bytes; filenames cannot inject headers; serializer failure occurs before unsafe automatic retries | Planned; evidence gates open |
| WP-04 | Authentication redirects and cookies | Internal planning vocabulary (verify upstream public identity): Authenticator, RedirectPolicy, CookieJar | Redirects cannot leak authorization across trust boundaries; expired cookies are not sent; failed auth hooks produce diagnosable outcomes | Planned; evidence gates open |
| WP-05 | Interceptors adapters and compatibility | Internal planning vocabulary (verify upstream public identity): RequestInterceptor, ClientOptions, RestCompatibilityCase | Hook order is deterministic; unsupported overload semantics are recorded; optional integration artifacts do not enter the base client | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Identify serializers/authenticator packages outside main repo; distinguish convenience wrappers around JDK from forbidden framework substitution.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
