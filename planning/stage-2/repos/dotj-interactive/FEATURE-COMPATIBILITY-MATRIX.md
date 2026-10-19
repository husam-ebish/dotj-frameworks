# DJ-008 .j Interactive: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

JShell state and class redefinition differ from C# scripting. Jupyter transport dependencies and notebook format support need separate decisions.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Kernel command and event protocol | Internal planning vocabulary (verify upstream public identity): KernelCommand, CommandToken, KernelEvent | Every accepted command has one terminal outcome; output cannot impersonate a protocol event; cancellation is correlated to the right cell | Planned; evidence gates open |
| WP-02 | Java execution state | Internal planning vocabulary (verify upstream public identity): JavaKernel, CellState, ValueHandle | Redefinition matches documented JShell limitations; interrupt preserves or explicitly resets state; worker failure does not kill notebook host | Planned; evidence gates open |
| WP-03 | Notebook and display formats | Internal planning vocabulary (verify upstream public identity): NotebookDocument, CellOutput, MimeBundle | Unknown metadata survives round trip; malicious display output cannot execute in trusted host context; binary outputs retain bytes | Planned; evidence gates open |
| WP-04 | Package and multi-language integration | Internal planning vocabulary (verify upstream public identity): KernelPackageReference, ExternalKernelAdapter, SessionLock | A package conflict leaves prior session usable; missing external kernels produce capability errors; no existing Java notebook framework is substituted | Planned; evidence gates open |
| WP-05 | Jupyter transport and lifecycle | Internal planning vocabulary (verify upstream public identity): ConnectionFile, MessageAuthenticator, TransportAdapter | Malformed signatures are rejected; heartbeat survives long cells; shutdown removes secrets and endpoints; transport feasibility remains gated until demonstrated | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

ZeroMQ/Jupyter transport is not supplied by standard JDK. Investigate own transport versus narrowly justified native binding without importing a notebook framework.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
