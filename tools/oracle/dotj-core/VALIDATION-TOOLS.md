# Foundation product, validation tools and future dependencies

| Scope | Current requirement |
|---|---|
| Current dotj-core product candidate | JDK APIs, targeting Java 21. No third-party Java runtime libraries; Maven and Gradle are not required. The recorded reference JDK is Microsoft OpenJDK 21.0.12.1+1-LTS. |
| Development and reference validation | A real Python interpreter, pinned .NET SDK 10.0.401 and runtime 10.0.12. New PowerShell probes use framework-dependent PowerShell 7.6.0 on that shared runtime. These tools are excluded from the product JAR. |
| Broader project and distribution | The 66-framework resolved dependency graph remains open. Upstream PackageReference examples are not Java runtime requirements. No public .j SDK installer or package feed is documented as released. |

Read applicable AGENTS.md instructions and the current tracker before changing requirements. Old-PC installation paths are examples. This bootstrap keeps downloads and extracted tools under `D:\AI\Implementation\dotj Frameworks\toolchains`; validation builds, caches and logs also stay under the project directory on D:. It does not install globally or modify the machine PATH.

The versioned [download manifest](dependency-downloads-v1.json) records URLs actually downloaded and tested, archive hashes, verification sources and purposes. The JDK executables and .NET host/SDK/CoreLib also match the pre-existing baseline binary hashes. Python 3.13.9 is this bootstrap's reproducible selection; the project does not otherwise pin a Python version. The PowerShell archive hash matches the publisher's release checksum file. The source archive URL and hash come from the repository's existing immutable source manifest.

From the repository root:

```powershell
# Acquire and verify missing archives; retain downloads on D:.
powershell -NoProfile -ExecutionPolicy Bypass -File tools/oracle/dotj-core/bootstrap-validation-tools.ps1

# Extract verified tool archives and verify the six baseline binaries.
powershell -NoProfile -ExecutionPolicy Bypass -File tools/oracle/dotj-core/bootstrap-validation-tools.ps1 -Extract

# Offline verification of the cached archives; no downloads or extraction.
powershell -NoProfile -ExecutionPolicy Bypass -File tools/oracle/dotj-core/bootstrap-validation-tools.ps1 -VerifyOnly
```

The verification record is written to `planning/stage-2/repos/dotj-core/evidence/dependency-download-verification-v1.json`. The runtime source ZIP is retained as reference evidence; this script does not extract its full source tree. The SDK archive includes runtime 10.0.12, so a separate runtime installation is unnecessary for these selected oracles. `global.json` and `OracleBootstrap.csproj` retain the SDK and runtime pins. The selected `NuGet.Config` clears package sources.

```powershell
# Build and run the candidate in a detached worktree on D:.
powershell -NoProfile -ExecutionPolicy Bypass -File tools/oracle/dotj-core/run-isolated-foundation-gate.ps1 -RunName validation-001 -ExportEvidence

# Capture TimeSpan reference vectors; verifies actual CoreLib hash.
powershell -NoProfile -ExecutionPolicy Bypass -File tools/oracle/dotj-core/run-timespan-oracle.ps1

# Other selected reference captures use the same pinned, framework-dependent runtime profile.
powershell -NoProfile -ExecutionPolicy Bypass -File tools/oracle/dotj-core/run-pinned-contract-oracle.ps1 -Contract exception
powershell -NoProfile -ExecutionPolicy Bypass -File tools/oracle/dotj-core/run-pinned-contract-oracle.ps1 -Contract datetime
```

Each validation run needs a fresh single-component RunName so prior evidence is preserved. The isolated runner validates committed HEAD, bootstraps the compile-only IDisposable JAR, and exports only reviewed JSON evidence paths when requested. The candidate JAR exists inside that D: worktree at `dotj-core/dotj-core-public/build/foundation-v1/dotj-core-foundation-v1.jar`; it need not exist in the C: source checkout. A self-contained PowerShell package loads its bundled CoreLib and is rejected by the TimeSpan oracle; use the framework-dependent package in the manifest.

Tool availability on the default PATH is separate from availability to these explicit runners. Report `python --version`, `java -version`, `javac -version`, `jar --version`, `dotnet --list-sdks` and `dotnet --list-runtimes` from the environment actually used. Neither a successful tool bootstrap nor the bounded candidate gate closes licensing review, public API qualification or implementation acceptance.

The combined candidate runner schedules independent consumer JVMs with four Python standard-library worker threads. Compilation remains sequential and finishes before consumer execution; each consumer still has a separate JVM and its original assertions. All submitted JVM exit codes are checked before evidence is written. Set DOTJ_JAVA_WORKERS=1 for serial execution, or choose 1-8 workers for local resource limits.

The isolated gate scopes JAVA_TOOL_OPTIONS to a 16 MiB initial heap and a 256 MiB maximum per JVM, avoiding the large default initial reservations that exhausted Windows commit capacity during validation. Use -JavaHeapMiB (64-1024) to select a different validation maximum. Existing process options are retained before these heap bounds, the effective options are recorded in the isolated run manifest, and the caller's environment is restored. This is a development resource profile, with no product runtime dependency or distribution requirement.

After selecting the pinned JDK on the process PATH, run measure-foundation-consumers.py --workspace <existing-D-validation-source-directory> with the real Python interpreter to compare one and four workers. The helper keeps temporary files and Python caches beside the D: worktree. It requires identical candidate artifact evidence and JAR hashes in both modes. Timing is a local measurement, not a cross-machine performance guarantee. This changes development validation only; product runtime dependencies and qualification status stay unchanged.
