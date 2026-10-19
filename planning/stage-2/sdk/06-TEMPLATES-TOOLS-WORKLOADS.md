# Templates, tools, workloads and IDE integration

Parent: [SDK plan](../10-SDK-AND-DISTRIBUTION-PLAN.md). Owners: dotj-templates, dotj-scaffold, dotj-sdk, dotj-packages, dotj-code and individual platform products.

## Templates and generated examples

Keep familiar template short names for corresponding capabilities: `console`, `classlib`, `sln`, `globaljson`, `nugetconfig`, `tool-manifest`, and qualified test/web templates as their products become available. Every default must be tied to the selected .NET reference profile and a Java representation decision. Do not advertise an unavailable framework by generating an application that cannot restore/build.

Preserve template concepts such as identities, short names, symbols, parameters, constraints, source transforms, rename rules and post-actions. Use the source-derived `.template.config/template.json` schema where its semantics are retained. A Java template advertises its language honestly; `--language C#` must not produce Java while claiming success for a C# request.

Generated code must demonstrate exact public framework naming: for example, qualified `IServiceCollection`, `AddSingleton`, `BuildServiceProvider`, `ILogger`, `IConfiguration`, `Host.CreateApplicationBuilder` and source-verified related APIs where those APIs are actually implemented. Java syntax may require static extension-method invocation or metadata accessor forms; explain those exact mappings in paired C#/.j examples. Never publish noncompiling pseudocode as a successful template acceptance result.

The initial console template uses only the qualified core surface; the class library has no invented external dependencies. Add an xUnit or NUnit style template only after its package and runner adapter are usable. Web/worker/desktop templates depend on their actual framework slices and remain clearly pending until then.

`new --dry-run` previews all intended paths without writes or restores. Overwrite handling follows the reference. Path traversal and transformations outside the declared output root fail. Post-actions need a declared operation and noninteractive behavior; a downloaded template must not silently execute arbitrary scripts merely because its archive was inspected or listed.

## Local and global tools

Preserve `tool install/update/uninstall/list/restore/run/search`, global scope, local manifests and tool-path concepts, including the exact qualified options. Tool packages contain Java executables and explicit command names/runtime requirements; ordinary .NET tool DLLs are incompatible until an actual execution bridge exists.

Retain `.config/dotnet-tools.json` as the familiar manifest name for the selected compatibility profile. Validate runtime kind from the resolved package and isolate installation stores/shims. Mixed CLR and Java tool manifests require per-tool runtime qualification; one toolchain must not overwrite another's binaries. If format semantics cannot safely coexist, record the conflict rather than silently change manifest discovery.

On installation, resolve and validate the package, stage payloads, verify declared executable entry points, then publish shims atomically. Tool name collisions require an explicit failure or the source-qualified behavior. Local tool restore must respect the repository manifest and pinned version; global installation must not modify project dependencies. Removal deletes only that tool's owned shim and content.

Tool process execution preserves arguments, current directory, environment and exit code under the qualified contract. Cancellation must not leave owned child processes running. Tool restore and package restore are related services with separate command semantics, not synonyms.

## Workload manifests and installation

Workloads group optional platform packs and tooling; they are not another name for every package reference. Source-derive manifest fields, workload IDs, pack dependencies, SDK band compatibility, update sets and command options. Preserve known workload IDs for corresponding implemented capabilities where identity and rights allow; the runtime assets remain .j-specific and clearly identified.

The base SDK must create/build a console app without installing every mobile/UI/browser toolchain. A workload is installable only when its OS/architecture requirements, external toolchain prerequisites, licenses, pack content and runtime backend are qualified. An unimplemented mobile runtime cannot pass because its manifest downloads correctly.

Record the exact installed workload/pack versions and SDK association. Install/update is a transaction: resolve complete closure, stage, validate, commit, retain rollback data. Repair verifies content; uninstall respects shared packs. Workload restore inspects project requirements without silently changing unrelated workloads. Source-derive interactive permission behavior and provide clear failures in unattended CI.

Offline workload bundles include all selected manifests, packs and required external tools whose redistribution is permitted. A download pointer is not an offline dependency. Document prerequisites that cannot be bundled and fail before pretending installation completed.

## Test, diagnostics and development loops

`dotj test` is the single familiar entry point. It integrates real dotj-xtest/dotj-test adapters and qualified runner protocols, preserves test filtering/result/logging concepts and distinguishes no tests, failed tests, invalid configuration and crashed runners according to the selected reference. A Java main method printing success is not a substitute for the requested test framework behavior.

Qualify the .NET 10 runner selection boundary explicitly: VSTest and Microsoft.Testing.Platform modes have different contracts. Do not combine their option sets into an invented common CLI. Pin the intended initial mode, preserve that mode's configuration and add the other through its own adapter/tests.

`watch`, formatting, diagnostics, coverage, benchmarking, code generation and hot reload belong to their real product owners. Inventory their upstream command/protocol contracts and maintain their place in the backlog. A file watcher that restarts the application must not be advertised as semantic hot reload unless that capability is implemented.

## IDE integration

First deliver a terminal workflow that works in any editor. Then provide thin IDE integrations which invoke the same SDK/project services for restore/build/test/debug, rather than duplicating project resolution. A language server or debug adapter must report Java execution accurately while exposing familiar .NET framework symbols and project concepts.

Keep project discovery, launch configurations, diagnostics, completion, navigation and test discovery linked to the compiled public API and the selected SDK. An IDE extension does not make Microsoft's C# compiler understand Java or guarantee official Visual Studio/Rider C# tooling compatibility. Qualify each supported integration and plugin distribution mechanism separately.

## Acceptance

For every advertised template, create in an empty directory, restore from the designated feed, build, run/test and publish where applicable. Test repeated installation, version update, rollback, tool name collision, corrupt template, path traversal, incompatible SDK/workload band, missing external compiler, offline closure and removal of shared packs. Store paired C#/.j examples and exact platform differences with the evidence.
