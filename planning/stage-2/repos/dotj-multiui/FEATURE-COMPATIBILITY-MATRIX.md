# DJ-042 .j MultiUI: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Android ART is not a Java 25 desktop JVM; iOS has no standard supported JVM deployment assumption. Shared syntax does not guarantee portable execution.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Application model and handler contracts | Internal planning vocabulary (verify upstream public identity): Application, Page, Handler, PropertyMapper | Handlers attach/detach once; navigation state survives documented lifecycle transitions; platform overrides do not mutate shared global maps | Planned; evidence gates open |
| WP-02 | Shared XAML binding and controls | Internal planning vocabulary (verify upstream public identity): XamlCompiler, BindableProperty, ResourceDictionary | Compiled and runtime XAML agree on fixtures; missing resources have source diagnostics; layout differences are recorded per backend | Planned; evidence gates open |
| WP-03 | Android backend and device services | Internal planning vocabulary (verify upstream public identity): AndroidPeer, ActivityState, PermissionRequest | Denied permissions produce explicit results; rotation does not leak peers; device APIs are tested on declared API levels | Planned; evidence gates open |
| WP-04 | Apple and desktop feasibility | Internal planning vocabulary (verify upstream public identity): PlatformBackend, NativeBridge, DeploymentProfile | No mobile platform is claimed before executable proof; native dependencies/licenses are enumerated; signing credentials remain external | Planned; evidence gates open |
| WP-05 | Workloads build and cross-platform qualification | Internal planning vocabulary (verify upstream public identity): WorkloadManifest, AppPackage, PlatformTestMatrix | Each supported target has install/launch evidence; unsupported APIs fail explicitly; shared tests do not replace device-specific validation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Select Android-compatible language/API subset and prove iOS execution strategy before claiming mobile feasibility. SDK licenses and host constraints remain blockers.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
