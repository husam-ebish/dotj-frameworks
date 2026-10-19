# Decisions and blockers

Planning is complete across all targets without requiring another round of owner questions. The following defaults let work proceed while preserving the gates that cannot honestly be assumed resolved.

| Decision | Planning default | Evidence required before affected implementation |
|---|---|---|
| Java baseline | Java 25 non-preview for portable server/desktop work | Exact approved binary/vendor/platform lock |
| Compiler scope | Java tooling first; retain C#, VB and translation as separate tracks | Language grammar/semantic ownership and feasibility report |
| Build project format | Own Java model with explicit MSBuild compatibility importer/profile | Evaluation ordering and supported task semantics |
| Browser components | Server/runtime contracts first; browser execution separately investigated | Runnable JS/Wasm/backend choice; no browser JVM assumption |
| Mobile | Separate Android-compatible subset and Apple runtime/AOT investigation | Device install/launch, SDK/license/ABI evidence |
| Native desktop | Windows-first WPF/Forms profile; other backends individually scoped | Rendering/input/accessibility/native ownership proof |
| JSON and DI | Core profile and independent third-party product ports | Behavior-specific fixtures and adapter boundaries |
| ORM queries | Explicit typed query IR/generated metamodel | SQL/null semantics and unsupported-expression diagnostics |
| PostgreSQL | Owned wire driver; JDBC coverage method-by-method | Protocol/server matrix and JDBC capability evidence |
| Instrumentation | Interface proxies first; owned classfile/agent research separately gated | Verifier/semantic equivalence and agent compatibility |
| Packages | Native Java artifacts distinct from NuGet protocol compatibility | Artifact identity, resolver and format fixtures |
| Licenses | Preserve evidence; no blanket clearance | Exact source/version/dependency eligibility and notices |
| Source audits | Sampled evidence available; close semantic inventory per slice | E02/E03 output before each claimed capability |

## Do not confuse these states

Written plan complete does not mean exhaustive upstream audit complete. Implementation requested does not clear license/platform gates. Passing a sample does not imply whole-product compatibility. A source directory inventory is not an API census. A designed test is not an executed test. A library interface compiled on Java is not proof that its native/mobile/browser backend exists.

## Gate ownership

Repository maintainers own baseline and source/API closure. Compatibility maintainers own fixtures and deviations. Platform maintainers own native/device/browser proofs. Dependency/licensing reviewers own eligibility records. Product maintainers own explicit scope changes. These are roles, not invented assigned people. Independent packages proceed while a specific gate remains blocked.
