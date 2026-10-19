# DJ-042 .j MultiUI: feature compatibility matrix

Android ART is not a Java 25 desktop JVM; iOS has no standard supported JVM deployment assumption. Shared syntax does not guarantee portable execution.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Application model and handler contracts | Proposed Java contracts: Application, Page, Handler, PropertyMapper | Handlers attach/detach once; navigation state survives documented lifecycle transitions; platform overrides do not mutate shared global maps | Planned; evidence gates open |
| WP-02 | Shared XAML binding and controls | Proposed Java contracts: XamlCompiler, BindableProperty, ResourceDictionary | Compiled and runtime XAML agree on fixtures; missing resources have source diagnostics; layout differences are recorded per backend | Planned; evidence gates open |
| WP-03 | Android backend and device services | Proposed Java contracts: AndroidPeer, ActivityState, PermissionRequest | Denied permissions produce explicit results; rotation does not leak peers; device APIs are tested on declared API levels | Planned; evidence gates open |
| WP-04 | Apple and desktop feasibility | Proposed Java contracts: PlatformBackend, NativeBridge, DeploymentProfile | No mobile platform is claimed before executable proof; native dependencies/licenses are enumerated; signing credentials remain external | Planned; evidence gates open |
| WP-05 | Workloads build and cross-platform qualification | Proposed Java contracts: WorkloadManifest, AppPackage, PlatformTestMatrix | Each supported target has install/launch evidence; unsupported APIs fail explicitly; shared tests do not replace device-specific validation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Select Android-compatible language/API subset and prove iOS execution strategy before claiming mobile feasibility. SDK licenses and host constraints remain blockers.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
