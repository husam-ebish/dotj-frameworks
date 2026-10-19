# Risks and open decisions

All items remain open unless marked as an observation or provisional proposal. Owner answers are only needed when the decision actually blocks further planning. Independent analysis can continue.

| ID | Issue | Impact | Next evidence/action |
|---|---|---|---|
| CORE-R01 | Windows checkout/Azure remote not accessible | Prepared documents cannot be applied, committed or pushed here | Obtain repository clone URL and an available authorized access route; never paste credentials |
| CORE-R02 | Source snapshot uses prerelease SDK | Cannot label target as compatible with a stable .NET release | Select verified release baseline or explicitly retain prerelease reference; diff affected APIs/tests |
| CORE-R03 | JDK source/binary lock unresolved from Stage 1 | Reproducible Java toolchain unavailable | Verify chosen Java 25 vendor version, release applicability, binary hash and source correspondence |
| CORE-R04 | 218 directories, only 10 with selected file reads | Whole-core detailed plan incomplete | Finish recursive source/API/test and native inventories; sampled files are not complete modules |
| CORE-R05 | 1,061 lexical declaration candidates, not semantic symbols | Counts cannot serve as coverage claims | Use parser/build-aware extraction including conditions, type forwarding and generated source |
| CORE-R06 | Conditions/imports not evaluated | Dependency closure and exact build inputs unknown | Resolve selected framework metadata without executing unrelated repository instructions |
| CORE-R07 | Ambient execution contexts differ | Cancellation/logging behavior may diverge | Freeze explicit .j context adaptation and cross-runtime fixtures |
| CORE-R08 | Sync/async close, alias ownership and failures | Resource leaks/double-close/deadlocks | Complete state model, identity policy and failure-order tests |
| CORE-R09 | Java generic erasure and keyed DI | Incorrect service identity/resolution | Type-token/open-generic/key contract and constructor selection tests |
| CORE-R10 | Configuration reload is not an established transaction | Stage-1 snapshot wording could promise too much | Adopt compatibility behavior; any atomic snapshot extension separately named |
| CORE-R11 | New async options behavior is baseline-specific | Incorrect claims about released options semantics | Inspect startup validator/cache classes and chosen release diff |
| CORE-R12 | Logging/host implementation not fully read | Lifecycle/order/performance contracts incomplete | Inspect implementation and fixtures before freezing APIs |
| CORE-R13 | Core JSON/OPC/mail/limiter overlap with other targets | Scope loss or cyclic ownership | Keep upstream profiles distinct and approve explicit sharing boundaries |
| CORE-R14 | Native/runtime features are not JVM-library equivalents | Some capabilities may need separate platform backends | Feasibility records for VM, IL, COM, OS auth, intrinsics and browser/native execution |
| CORE-R15 | Root MIT text is not complete provenance | Source/assets/dependencies may carry separate terms | Per-file/generated/native/test-asset provenance review |

No question about licensing, Java baseline or the whole VM needs to stop this first planning increment. The immediate integration blocker is repository access. Implementation remains unauthorized even after that is resolved.
