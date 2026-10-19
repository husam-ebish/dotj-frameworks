# DJ-009 .j Scaffold: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Generated Java must follow .j contracts; C# source rewriting and external identity provisioning cannot be assumed portable.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Command catalog and model discovery | Internal planning vocabulary (verify upstream public identity): ScaffoldRequest, ProjectModel, GeneratorDescriptor | Missing symbols produce source-linked diagnostics; unsupported generator families remain listed; command selection is deterministic | Planned; evidence gates open |
| WP-02 | Web and data generators | Internal planning vocabulary (verify upstream public identity): ControllerModel, EntityScaffoldModel, GeneratedFile | Each generated fixture compiles against its declared modules; relationship and nullability choices are explicit; no C# code is emitted as Java | Planned; evidence gates open |
| WP-03 | Safe project editing | Internal planning vocabulary (verify upstream public identity): EditPlan, OwnedRegion, ConflictReport | Rerunning unchanged input is idempotent; user edits cause reviewable conflicts; a failed write restores original project bytes | Planned; evidence gates open |
| WP-04 | Identity and external provisioning | Internal planning vocabulary (verify upstream public identity): IdentityScaffoldSpec, ProvisioningPlan, SecretReference | Dry runs make no remote changes; credentials never enter generated source; partial provisioning can be identified and reconciled | Planned; evidence gates open |
| WP-05 | Catalog evolution and verification | Internal planning vocabulary (verify upstream public identity): GeneratorVersion, TemplateBinding, UpgradePlan | Reproducing a generator version produces the same normalized tree; upgrades show user-facing diffs; unsupported older schemas fail with migration guidance | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Inspect external identity dependencies and whether provisioning can remain a separate authenticated CLI workflow.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
