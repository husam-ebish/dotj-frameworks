# DJ-032 .j REST: feature compatibility matrix

Preserve encoding, multipart, errors and cancellation behavior; Java transport redirect/cookie defaults must not silently replace source defaults.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Request model and URI construction | Proposed Java contracts: RestRequest, Parameter, ResourcePath | Reserved characters survive expected encoding; duplicate headers follow policy; concurrent calls do not mutate a shared request unexpectedly | Planned; evidence gates open |
| WP-02 | Transport and response lifecycle | Proposed Java contracts: RestClient, Response, ResponseBody | Non-success HTTP can retain its body; cancellation closes owned streams; response resources are released on conversion failure | Planned; evidence gates open |
| WP-03 | Serialization and multipart bodies | Proposed Java contracts: BodySerializer, MultipartPart, ContentType | Binary parts preserve bytes; filenames cannot inject headers; serializer failure occurs before unsafe automatic retries | Planned; evidence gates open |
| WP-04 | Authentication redirects and cookies | Proposed Java contracts: Authenticator, RedirectPolicy, CookieJar | Redirects cannot leak authorization across trust boundaries; expired cookies are not sent; failed auth hooks produce diagnosable outcomes | Planned; evidence gates open |
| WP-05 | Interceptors adapters and compatibility | Proposed Java contracts: RequestInterceptor, ClientOptions, RestCompatibilityCase | Hook order is deterministic; unsupported overload semantics are recorded; optional integration artifacts do not enter the base client | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Identify serializers/authenticator packages outside main repo; distinguish convenience wrappers around JDK from forbidden framework substitution.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
