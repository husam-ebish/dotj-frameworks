# Projects, solutions and build integration

Parent: [SDK plan](../10-SDK-AND-DISTRIBUTION-PLAN.md). Implementation owners: dotj-build, dotj-sdk, dotj-packages, dotj-code. This is the proposed Java-backed representation of familiar SDK-style project concepts.

## Public project model

Retain the XML concepts `Project`, `Sdk`, `PropertyGroup`, `ItemGroup`, `Import`, `Target`, property names, `PackageReference`, `ProjectReference` and `FrameworkReference`, including their upstream spelling. Preserve applicable property/item evaluation and command-line property overrides. Do not replace projects with an unrelated JSON build language or require a Maven POM or Gradle script.

The proposed native project extension is `.jproj` and the SDK ID is `Dotj.Sdk`. These identify a Java product; they do not rename source-derived framework APIs. The native target moniker `java25` is a proposed .j profile, not an existing Microsoft Target Framework Moniker. Its exact spelling and compatibility rules are frozen by SDK-I01/I05 after qualification. If a representation cannot satisfy an exact owner requirement, record the conflict and do not certify parity.

```xml
<Project Sdk="Dotj.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>java25</TargetFramework>
    <RootNamespace>Store.App</RootNamespace>
    <AssemblyName>Store.App</AssemblyName>
    <Version>0.1.0</Version>
    <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include="../Store.Domain/Store.Domain.jproj" />
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="0.1.0" />
  </ItemGroup>
</Project>
```

`AssemblyName` retains the familiar output-identity concept while mapping to a Java artifact name. It must not imply a CLR assembly exists. The example package version is illustrative. Generated source is Java and uses the source-verified .NET API facade; neither the project extension nor a template can make C# syntax valid Java automatically.

## File contracts

| File / location | Required concept and behavior |
|---|---|
| `global.json` | SDK selection, separate from target/runtime selection |
| `Directory.Build.props` / `Directory.Build.targets` | Shared build customization with established discovery/import rules |
| `Directory.Packages.props` | Central package versions using `ManagePackageVersionsCentrally` and `PackageVersion` |
| `NuGet.Config` | Sources, credentials, mappings and applicable settings |
| `packages.lock.json` | Reviewed dependency lock; deterministic locked restore |
| `.sln` / `.slnx` | Solution membership/configuration; preserve unowned entries |
| `.config/dotnet-tools.json` | Familiar local tool manifest name; runtime kind must be validated before execution |
| `obj/` | Generated restore/build state, never hand-edited as source of truth |
| `bin/<Configuration>/<TargetFramework>/` | Familiar configuration/target output separation |
| `Properties/launchSettings.json` | Applicable run profiles, arguments and environment configuration |
| `Properties/PublishProfiles/*.pubxml` | Applicable publish settings and import semantics |

Retained filenames do not prove every upstream tool can interpret Java-specific entries. Document format compatibility separately from runtime compatibility. A mixed .NET/.j tree must have independent lock/cache and build ownership where the underlying formats cannot safely share generated state; reject collisions instead of corrupting one toolchain's outputs.

## Evaluation and target execution

Implement the qualified MSBuild evaluation slice before invoking javac: ordered imports, property expansion, item inclusion/exclusion, metadata, conditions, configuration/target selection and project references. Evaluate relative paths against the correct defining file. Detect import/project cycles with a useful trace. Keep evaluation deterministic for identical inputs.

Preserve `Restore`, `Build`, `Clean`, `Rebuild`, `Pack`, `Publish` and the validated test targets as public target names. The implementation may use internal stages, but an internal stage is not a new user-facing target vocabulary. Source-derive target dependency ordering and supported extension points. Arbitrary .NET task assemblies cannot execute on the JVM; either provide the owned corresponding task or report that task as unsupported with its originating import.

Every accepted property gets a ledger entry with type, default, evaluation phase, effect and tests. Initial coverage includes `Configuration`, `TargetFramework`, `TargetFrameworks`, `RuntimeIdentifier`, `RuntimeIdentifiers`, `OutputType`, `AssemblyName`, `RootNamespace`, `Version`, `PackageId`, `PackageVersion`, `IsPackable`, `IsTestProject`, `GeneratePackageOnBuild`, `TreatWarningsAsErrors`, `NoWarn`, `Deterministic`, `ContinuousIntegrationBuild`, `OutputPath` and `IntermediateOutputPath` where applicable.

Do not accept `Nullable`, `ImplicitUsings`, `LangVersion`, analyzers, source generators, trimming or AOT properties as silent no-ops. Each requires an explicit Java mapping or a capability error. C# Roslyn analyzers/generators are not Java plugins merely because their package restores. Preserve source identities in dotj-code and qualify their own Java execution adapters.

## Compilation and incremental behavior

Translate the validated project model into javac options using an exact selected JDK. Preserve namespace/API casing, and determine JPMS module boundaries independently of public package identity. Never relocate public types solely to satisfy a packaging preference. Multiple upstream generic arities, illegal Java identifiers or namespace/type collisions remain N01 blockers until a faithful representation is settled.

Record source bytes, compiler identity, classpath/module path, generated source inputs, resource transformations, relevant properties and package content hashes in build state. Cache hits must validate the full input identity. Dependency changes, target changes and compiler upgrades invalidate affected outputs. Concurrent builds must not publish partial output trees to one another.

`--no-restore` forbids an implicit restore. `--no-build` has command-specific semantics taken from the oracle. Offline success requires complete local inputs. Missing inputs must fail explicitly. `clean` removes only build-owned outputs and respects configuration/target boundaries; arbitrary source or shared-cache deletion is forbidden.

## Project mutation and compatibility import

Package/reference/solution edit commands must preserve unrelated XML, comments, line endings and solution members where feasible. Apply edits atomically. Failed restore after an edit must follow the locked reference behavior, with clear evidence of what changed; do not invent rollback semantics under a parity claim.

Importing `.csproj` means analyzing its project/dependency/build concepts and reporting a migration mapping. It does not mean compiling unchanged C# with javac. Report unsupported imports, tasks, analyzers, frameworks, native assets and syntax before declaring a project migrated. Keep the original project intact unless the user explicitly requests a conversion operation. A language transpiler is separate scope requiring its own evidence, tests and compatibility definition.

## Required acceptance evidence

Use single-project, multi-project, central-version, conditional-reference and mixed solution fixtures. Verify configuration propagation, project-reference topological order, cycle errors, generated-file isolation, no-change incremental builds and correct rebuilds after source/package/compiler changes. Include Windows paths with spaces, Linux case distinctions, Unicode filenames and cancellation during compilation. Retain both the reference evaluation result and the .j evaluation result with all intentional representation differences enumerated.
