# Java foundation and dependency policy

## Baseline proposal

Select Java 25 as the initial portable framework language/API baseline, with no preview APIs in public contracts. This gives one coherent JDK toolchain, modern concurrency and standard JVM tooling without depending on another framework. An installed JDK suffices; neither foundation repository is a required checkout or runtime dependency.

Proposed immutable source baseline: OpenJDK `jdk25u` tag `jdk-25.0.4.1-ga`, resolving in the inspected GitHub tree page to `7b65d74bcbd7c3a0b4c1f5c5bd85e64aa2e51b4a`. Evidence: [tag listing](https://github.com/openjdk/jdk25u/tags) and [tag tree](https://github.com/openjdk/jdk25u/tree/jdk-25.0.4.1-ga), inspected 2026-10-18. This is a proposed research/source pin, not approval of a downloadable JDK distribution. A follow-up raw version-file read returned 404; verify tag contents, release applicability and vendor binary identity before making this the build lock. Do not infer a current supported binary merely from a GA-named source tag.

The separately recorded default-branch SHA in the inventory is reconnaissance evidence, not the production baseline. `jdk25u` README distinguishes its release-rampdown role from `jdk25u-dev`; the latter is a newly discovered optional reference, not a third required foundation. OpenJDK mainline is useful for source research and future-change tracking, not a production target.

The final build lock must contain vendor/distribution, exact version/build, OS/architecture, download origin, binary SHA-256, source correspondence, license/notices and update policy. These are OPEN because no build or binary selection occurred. Before implementation, validate the proposed source pin against the chosen vendor release; advance it through a recorded decision if needed. Keep the compiler/API baseline Java 25 unless a platform-specific module explicitly targets a narrower runtime.

## Runtime and platform policy

Portable modules use JDK APIs. Standard collections, sockets, TLS, cryptographic primitives, XML, ZIP, JDBC interfaces and compiler APIs should be reused. JDK APIs are not permission to equate their defaults with .NET semantics. Adapters must document differences in time, Unicode, numeric behavior, cancellation and resource ownership.

JDK class-file APIs and instrumentation are candidates for mock/coverage tooling; verify the exact API surface at the pinned JDK. Native access uses an isolated FFM/JNI adapter and explicit lifecycle/ABI checks. JVMTI agents are native components. Android and iOS are not covered by a desktop JDK support claim. Browser execution requires a separately selected JS/Wasm strategy; it cannot assume a browser JVM. Standard desktop AWT can assist bootstrapping but does not reproduce WPF or Windows Forms semantics.

## Dependency classes

| Class | Examples | Policy |
|---|---|---|
| Standard foundation | JDK compiler/runtime APIs | Allowed; document behavior and platform/version limits |
| Owned .j runtime | core contracts, JSON, data driver | Versioned module edges; avoid cycles and accidental umbrella dependencies |
| Development tools | Git, JDK CLI, shell/PowerShell | Pin versions for reproducibility; not shipped runtime dependencies |
| Reference/test tools | .NET SDK, original upstream test runners, browser automation | Keep isolated from Java runtime; record licenses and provenance |
| Runtime libraries | Any third-party Java library | Default none; require individual necessity, alternatives, license and bounded API justification |
| Native bindings/libraries | Rendering, fonts, JVMTI, platform auth | Separate artifacts, ABI/platform matrix and redistribution decision |
| Platform SDKs | Android SDK, Apple SDK/Xcode, Windows SDK | Needed only for corresponding backend; host/signing/deployment constraints explicit |
| Test/operational infrastructure | Database server, broker, container engine | Pin versions and images; infrastructure is not implementation substitution |
| Browser assets | JS interop, CSS, icons, interactive API UI | Prefer owned code; record every approved asset and its terms |

Spring, Hibernate, Netty, Vaadin, Jackson, JUnit, Mockito and analogous existing Java implementations are not foundations or substitutes. The same rule covers Java Quartz, RxJava, graphql-java, Apache POI and Testcontainers Java. Existing Java code in multi-language upstream repositories is not a shortcut for porting their C# functionality.

## Dependency decision record

For each candidate record: dependency ID, consumer module, class above, upstream URL, exact version/hash, required capability, why JDK/owned modules cannot provide it, alternatives, runtime footprint, transitive dependencies, license/notices, security/update owner and removal plan. Approval is a project decision, not implied by a package name in upstream metadata.

PackageVersion entries are version catalog evidence only. PackageReference entries confirm a declared reference in the inspected file, subject to conditions. Neither proves the complete restored closure, release applicability or a Java dependency requirement. Stage 2 resolves conditions and distinguishes build/test/runtime/native assets.

## License boundary

Using installed JDK APIs differs from copying OpenJDK implementation source. Inspect per-file GPL/ClassPath-exception applicability and additional notices before any source copying. Do not apply a repository-level label uniformly to all subcomponents. No legal clearance is asserted in this plan.
