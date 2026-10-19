# DJ-010 .j Templates: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Template conditions, symbol replacement and post-actions need precise ordering; shell execution must be an explicit opt-in operation.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Template schema and discovery | Internal planning vocabulary (verify upstream public identity): TemplateManifest, SymbolDefinition, CatalogEntry | Duplicate identities are diagnosed; malformed manifests do not enter catalog; discovery executes no post-actions | Planned; evidence gates open |
| WP-02 | Symbols conditions and transforms | Internal planning vocabulary (verify upstream public identity): SymbolTable, ConditionNode, FileTransform | Circular symbols fail with a path; conditional renames are deterministic; binary fixture checksums stay identical | Planned; evidence gates open |
| WP-03 | Filesystem planning and application | Internal planning vocabulary (verify upstream public identity): CreationPlan, DestinationPath, ConflictPolicy | Archives cannot escape destination; case-insensitive collisions are caught before writes; interruption leaves original user files intact | Planned; evidence gates open |
| WP-04 | Install update and post-actions | Internal planning vocabulary (verify upstream public identity): TemplatePackageLock, InstallTransaction, PostActionRequest | Corrupt packages never become selectable; uninstall preserves generated projects; unattended creation does not silently run arbitrary shell commands | Planned; evidence gates open |
| WP-05 | SDK and legacy package integration | Internal planning vocabulary (verify upstream public identity): TemplateEngine, NuGetTemplateAdapter, CreationResult | Same locked template and inputs produce equivalent trees; adapter rejects CLR-only post-actions; SDK receives structured conflicts and exit status | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Pin relocated SDK source and inspect historical tags if needed. NuGet-packaged templates need an adapter, not mandatory NuGet runtime semantics.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
