# DJ-008 .j Interactive: feature compatibility matrix

JShell state and class redefinition differ from C# scripting. Jupyter transport dependencies and notebook format support need separate decisions.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Kernel command and event protocol | Proposed Java contracts: KernelCommand, CommandToken, KernelEvent | Every accepted command has one terminal outcome; output cannot impersonate a protocol event; cancellation is correlated to the right cell | Planned; evidence gates open |
| WP-02 | Java execution state | Proposed Java contracts: JavaKernel, CellState, ValueHandle | Redefinition matches documented JShell limitations; interrupt preserves or explicitly resets state; worker failure does not kill notebook host | Planned; evidence gates open |
| WP-03 | Notebook and display formats | Proposed Java contracts: NotebookDocument, CellOutput, MimeBundle | Unknown metadata survives round trip; malicious display output cannot execute in trusted host context; binary outputs retain bytes | Planned; evidence gates open |
| WP-04 | Package and multi-language integration | Proposed Java contracts: KernelPackageReference, ExternalKernelAdapter, SessionLock | A package conflict leaves prior session usable; missing external kernels produce capability errors; no existing Java notebook framework is substituted | Planned; evidence gates open |
| WP-05 | Jupyter transport and lifecycle | Proposed Java contracts: ConnectionFile, MessageAuthenticator, TransportAdapter | Malformed signatures are rejected; heartbeat survives long cells; shutdown removes secrets and endpoints; transport feasibility remains gated until demonstrated | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

ZeroMQ/Jupyter transport is not supplied by standard JDK. Investigate own transport versus narrowly justified native binding without importing a notebook framework.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
