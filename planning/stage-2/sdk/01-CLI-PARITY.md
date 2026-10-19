# SDK command contract

Parent requirement: [DOTNET-SDK-EXPERIENCE-001](../10-SDK-AND-DISTRIBUTION-PLAN.md). The following is a target specification, not a claim of implemented commands. Command behavior must be extracted from the locked .NET SDK, not inferred from this table alone.

## Command parity inventory

Keep the command words and accepted aliases of the selected upstream version. `dotj` is the product launcher. An option listed for one command is not automatically valid for another. Preserve command-specific defaults, validation order and implicit operations through oracle fixtures.

| .NET operation | Required .j surface | Owner / observable result |
|---|---|---|
| Inspect installation | `dotj --info`, `--version`, `--list-sdks`, `--list-runtimes` | SDK; report actual selected and installed products |
| Help | `dotj --help`, `dotj <command> --help`, `dotj help <command>` | SDK; stable hierarchy and offline local help |
| Create | `dotj new console`, `classlib`, `sln`, `globaljson`, `nugetconfig`, `tool-manifest` | Templates; same template concepts and options |
| Template management | `dotj new list`, `search`, `install`, `uninstall`, `update` | Templates; discover and manage qualified templates |
| Restore | `dotj restore` | Packages/build; resolve and acquire exact dependency graph |
| Build | `dotj build` | Build; compile using the selected target and configuration |
| Run | `dotj run` | SDK; build when required, start application, forward arguments |
| Tests | `dotj test` | SDK/test adapters; discover, run and return real test status |
| Clean | `dotj clean` | Build; remove tracked outputs of the selected project/configuration |
| Pack | `dotj pack` | Packages; create the declared package archive locally |
| Publish application | `dotj publish` | SDK; create deployable application outputs |
| Build engine access | `dotj msbuild` | Build; supported MSBuild arguments/properties/targets |
| Build services | `dotj build-server shutdown` | Build; stop owned build/compiler servers |
| Solutions | `dotj sln <solution> add`, `remove`, `list` | SDK/build; preserve solution structure |
| Packages | `dotj package add`, `remove`, `list`, `search` | Packages; edit references or report package information |
| Project references | `dotj reference add`, `remove`, `list` | Build; operate on ProjectReference items |
| Familiar older forms | `dotj add <project> package`, `dotj add <project> reference`, corresponding supported list/remove forms | SDK; same behavior where the locked upstream accepts them |
| Sources | `dotj nuget add source`, `update source`, `remove source`, `list source`, `enable source`, `disable source` | Packages; edit NuGet.Config using its established concepts |
| Feed/cache actions | `dotj nuget push`, `delete`, `locals` and other source-inventoried commands | Packages; distinct local-cache and remote-feed operations |
| Tools | `dotj tool install`, `update`, `uninstall`, `list`, `restore`, `run`, `search` | SDK/packages; local, global and tool-path scopes |
| Workloads | `dotj workload install`, `restore`, `list`, `search`, `update`, `repair`, `uninstall` | SDK; versioned optional platform packs |
| SDK health | `dotj sdk check` | SDK; report update status, never update as a hidden side effect |
| Application execution | `dotj <application.jar>`, `dotj exec <application.jar>` | Runtime launcher; explicit Java payload mapping |

Inventory additional upstream commands and options, including `watch`, `format`, `dev-certs`, `user-secrets`, `store`, package auditing/signature commands and version-specific workload commands. Assign owners in diagnostics, code, web, packages or SDK. They are retained scope requiring semantic review, not silently absent from a claim of full parity. IDE commands and web tooling must not force their dependencies into the minimal console SDK.

## Required command contract records

SDK-I01 produces one record per command and supported reference version, with:

- Exact token path, aliases, positional argument cardinality, option names, short forms, value types and repetition rules.
- Default values and their dependence on target framework, configuration, project type, environment and SDK version.
- Project/solution discovery algorithm, ambiguity handling and path normalization for Windows, macOS and Linux.
- File reads/writes, possible network calls, implicit restore/build, child process ownership and cancellation behavior.
- Standard output/error routing, diagnostics, help text structure, raw exit code and machine output schema where the upstream offers one.
- Source location and immutable revision, upstream test identities, observed oracle cases, Java mapping and feature status.

Do not create a general `--json`, `--offline` or custom flag and present it as a .NET option. Where a feature needs a product extension, put it in the explicit platform decision ledger. Use established mechanisms such as local sources and `--no-restore` for qualified offline workflows.

## Daily workflow to preserve

This is a future acceptance scenario. `0.1.0` is an example .j product/package version, not an existing release or the upstream version. `java25`, `.jproj` and the generated source files are the proposed Java profile described in the decision ledger; their qualification is required before release.

```text
dotj new sln -n Store
dotj new classlib -n Store.Domain -o src/Store.Domain
dotj new console -n Store.App -o src/Store.App
dotj sln Store.slnx add src/Store.Domain/Store.Domain.jproj
dotj sln Store.slnx add src/Store.App/Store.App.jproj
dotj reference add src/Store.Domain/Store.Domain.jproj --project src/Store.App/Store.App.jproj
dotj package add Microsoft.Extensions.DependencyInjection --version 0.1.0 --project src/Store.App/Store.App.jproj
dotj restore Store.slnx
dotj build Store.slnx --no-restore --configuration Release
dotj run --project src/Store.App/Store.App.jproj --configuration Release --no-build -- customer-42
dotj pack src/Store.Domain/Store.Domain.jproj --configuration Release --output artifacts/packages
dotj publish src/Store.App/Store.App.jproj --configuration Release --runtime win-x64 --self-contained true --output artifacts/app
```

The `.slnx` example follows the selected family; legacy `.sln` support and exact template defaults are source-verified work. Do not change a user's existing solution format automatically. Package IDs follow the dedicated port feed policy; do not resolve the example against an official CLR package source.

## Parser, process and failure rules

Preserve spaces and Unicode in paths, repeated properties and the application argument delimiter. Execute subprocesses with argument arrays rather than constructing a shell command from untrusted values. Test quoting on Windows and POSIX separately. Path case behavior follows the actual filesystem; source naming remains case-exact.

An invalid command or unsupported option must fail before writing a project, installing a package or launching a compiler. A recognized but unimplemented feature must state that it is unsupported and fail. Help and version commands must work without a remote feed. A missing SDK must report the required version and detected installations without changing files.

For corresponding cases, retain raw upstream exit codes and output channels. Successful completion is zero; all failure classes must be nonzero unless the reference explicitly specifies otherwise. Do not collapse test failure, invalid arguments and restore failure into a misleading success result. Cancellation tests must verify child process cleanup and interrupted writes. Application exit propagation must be tested rather than assumed identical across hosts.

## Differential comparison rule

Run matching C# and Java-profile sample projects using the same conceptual inputs. Compare the command grammar, selected configuration, reference edits, dependency decisions, build ordering, failure category and side effects. Normalize only approved product names, temporary roots, timestamps and platform artifact representations. Never normalize away a missing warning, changed default, unresolved package or incorrect exit status. Exact wording, diagnostic codes and machine schemas must each have an explicit compatibility disposition rather than a blanket statement that all output is identical.
