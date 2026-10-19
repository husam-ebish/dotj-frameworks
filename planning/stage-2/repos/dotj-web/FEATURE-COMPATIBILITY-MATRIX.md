# DJ-012 .j Web: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Server rendering and persistent component circuits are plausible JVM tracks. Browser execution needs a separately justified JS/Wasm compilation/runtime design; browsers do not supply a JVM.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Server transport and HTTP lifecycle | Internal planning vocabulary (verify upstream public identity): ConnectionContext, HttpExchange, BodyPipe, ProtocolCapability | Conflicting framing is rejected; slow consumers bound buffers; abort terminates body reads; unsupported protocols are advertised honestly | Planned; evidence gates open |
| WP-02 | Middleware routing and APIs | Internal planning vocabulary (verify upstream public identity): RequestDelegate, RoutePattern, EndpointMetadata, BindingResult | Ambiguous routes fail deterministically; middleware can observe unwind order; malformed payloads have stable status/problem responses | Planned; evidence gates open |
| WP-03 | MVC and Razor Pages | Internal planning vocabulary (verify upstream public identity): ActionDescriptor, ModelState, PageHandler, ViewResult | Filters execute in documented nesting; validation errors preserve field paths; generated pages render escaped output and source-linked errors | Planned; evidence gates open |
| WP-04 | Components and Blazor execution profiles | Internal planning vocabulary (verify upstream public identity): ComponentDescriptor, RenderBatch, CircuitId, HydrationState | Disconnected circuits expire and release state; duplicate events are handled explicitly; browser execution is not advertised before a runnable backend exists | Planned; evidence gates open |
| WP-05 | Identity authentication and authorization | Internal planning vocabulary (verify upstream public identity): Principal, AuthenticationScheme, AuthorizationPolicy, IdentityStore | Scheme confusion tests fail closed; password/reset secrets are protected; lockout and concurrent updates behave predictably; auth store adapters are optional | Planned; evidence gates open |
| WP-06 | Application security and data protection | Internal planning vocabulary (verify upstream public identity): AntiforgeryToken, ProtectionKeyRing, CorsPolicy, SecurityHeaders | Cross-site requests cannot bypass token checks; old keys decrypt only under declared retention; untrusted redirects and markup are rejected or escaped | Planned; evidence gates open |
| WP-07 | SignalR and real-time messaging | Internal planning vocabulary (verify upstream public identity): HubConnection, InvocationId, HubProtocol, GroupMembership | Invocation completion is correlated once; stream cancellation releases producers; reconnect behavior is documented under lost responses and node changes | Planned; evidence gates open |
| WP-08 | Hosting diagnostics and integrated acceptance | Internal planning vocabulary (verify upstream public identity): WebHost, HealthEndpoint, RequestActivity, ServerOptions | Draining stops admission then bounds in-flight work; logs exclude credentials by default; claimed capabilities have per-protocol and per-platform evidence | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

HTTP/2 and HTTP/3, QUIC bindings, browser runtime and Identity stores require feasibility and threat reviews. Maintain all listed subsystems visibly.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
