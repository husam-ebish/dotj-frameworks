> Earlier source-backed foundation research retained as evidence. Current whole-core scope and readiness are in the parent directory. This sample is not whole-core completion.

# Dependencies and licenses

Status: **INCOMPLETE**. Selected project files were parsed as XML; imports, property expansion, target framework selection and restore were not executed. [Declared dependencies](evidence/declared-dependencies.json) preserves item/group conditions, paths and version expressions. It is not a resolved transitive graph.

## Observed dependency examples

| Inspected source | Observation | Consequence for the Java plan |
|---|---|---|
| Configuration.Abstractions project | References Primitives; some framework-specific references are conditional | Primitives precedes configuration; don't import every conditional .NET package into Java |
| DependencyInjection project | References abstractions conditionally, includes common/shared source and optional IL-emission files | Source inventory must follow Compile items and imports; Java activation backend is a deliberate adaptation |
| DependencyInjection project | System.Threading.Tasks.Extensions and Microsoft.Bcl.AsyncInterfaces are conditional compatibility references | Framework compatibility dependencies do not become automatic Java runtime dependencies |
| Selected global.json | Declares a prerelease SDK and Arcade/Helix/shared-framework build SDKs | C# oracle/tooling inputs require their own lock; not Java runtime dependencies |

Exact declarations and immutable source links are available in the evidence JSON. Expand all imports and conditions before claiming these examples are the complete build/runtime closure.

## Proposed target dependencies

The first core foundation modules require the JDK and owned core artifacts only. No Spring, Guice, Jackson, JUnit, Mockito or other Java framework is added. Use JDK collections, locks, executors, clocks, buffers and cryptographic primitives where appropriate; reproduce the required observable semantics through adapters.

Source-generator modules use JDK annotation-processing/compiler APIs as development dependencies. Native/OS support for the broader core inventory remains unselected. ICU/platform globalization, TLS providers, OS authentication, QUIC, COM, native libraries and runtime backends need separate dependency and feasibility records after source inspection. This list is an investigation list, not proof that every candidate is required for the initial modules.

## Provenance

The [root license](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/LICENSE.TXT) contains MIT text. [Third-party notices](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/THIRD-PARTY-NOTICES.TXT) were retrieved. This does not clear every source file, generated input, native component or test asset for reuse.

This update ships planning documents and extracted identifiers/declaration candidates, not upstream implementation files. The API candidate JSON contains reference-declaration text with source URLs and line numbers; preserve that provenance when using it. A later implementation must preserve the required source/asset notices and identify adapted tests. No legal clearance is asserted.

## Missing evidence before readiness

Resolve release baseline; inspect per-file headers and generators/shared files; evaluate target-framework conditions; inventory native/build tool versions; separate oracle test dependencies from shipped Java dependencies; pin tool binaries/checksums; record full notices in each applicable future artifact. These are gates before implementation readiness, not a reason to stop independent planning.
