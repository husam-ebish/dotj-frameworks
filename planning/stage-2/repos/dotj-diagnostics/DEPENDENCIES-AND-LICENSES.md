# DJ-007 .j Diagnostics: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: JFR, JMX, jcmd, jstack, java.lang.instrument and optional JVMTI native bindings.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | Microsoft.Diagnostics.NETCore.Client | [documentation/tutorial/src/triggerdump/triggerdump.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/documentation/tutorial/src/triggerdump/triggerdump.csproj) |
| PackageReference | Microsoft.Diagnostics.Tracing.TraceEvent | [documentation/tutorial/src/triggerdump/triggerdump.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/documentation/tutorial/src/triggerdump/triggerdump.csproj) |
| PackageReference | Microsoft.ManifestTool.CrossPlatform | [eng/common/internal/Tools.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Core | [eng/common/internal/Tools.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [eng/common/internal/Tools.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.DotNet.IBCMerge | [eng/common/internal/Tools.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/eng/common/internal/Tools.csproj) |
| PackageReference | Drop.App | [eng/common/internal/Tools.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.Diagnostics.Runtime | [src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj) |
| PackageReference | System.Reflection.Metadata | [src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj) |
| PackageReference | System.CommandLine | [src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj) |
| PackageReference | System.Memory | [src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj) |
| PackageReference | System.Runtime.Loader | [src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj) |
| PackageReference | System.Private.Uri | [src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj) |
| PackageReference | System.Text.Json | [src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj) |
| PackageReference | System.Threading.Tasks.Extensions | [src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj) |
| ProjectReference | $(MSBuildThisFileDirectory)..\Microsoft.Diagnostics.DebugServices\Microsoft.Diagnostics.DebugServices.csproj | [src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj) |
| ProjectReference | $(MSBuildThisFileDirectory)..\Microsoft.SymbolStore\Microsoft.SymbolStore.csproj | [src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.DebugServices.Implementation/Microsoft.Diagnostics.DebugServices.Implementation.csproj) |
| PackageReference | Microsoft.DotNet.RemoteExecutor | [src/Microsoft.Diagnostics.TestHelpers/Microsoft.Diagnostics.TestHelpers.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.TestHelpers/Microsoft.Diagnostics.TestHelpers.csproj) |
| PackageReference | xunit.v3.assert | [src/Microsoft.Diagnostics.TestHelpers/Microsoft.Diagnostics.TestHelpers.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.TestHelpers/Microsoft.Diagnostics.TestHelpers.csproj) |
| PackageReference | xunit.v3.extensibility.core | [src/Microsoft.Diagnostics.TestHelpers/Microsoft.Diagnostics.TestHelpers.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.TestHelpers/Microsoft.Diagnostics.TestHelpers.csproj) |
| ProjectReference | $(MSBuildThisFileDirectory)..\Microsoft.Diagnostics.DebugServices.Implementation\Microsoft.Diagnostics.DebugServices.Implementation.csproj | [src/Microsoft.Diagnostics.TestHelpers/Microsoft.Diagnostics.TestHelpers.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.TestHelpers/Microsoft.Diagnostics.TestHelpers.csproj) |
| ProjectReference | $(MSBuildThisFileDirectory)..\Microsoft.Diagnostics.DebugServices\Microsoft.Diagnostics.DebugServices.csproj | [src/Microsoft.Diagnostics.TestHelpers/Microsoft.Diagnostics.TestHelpers.csproj](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/src/Microsoft.Diagnostics.TestHelpers/Microsoft.Diagnostics.TestHelpers.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.TXT](evidence/notices/LICENSE.TXT) | [LICENSE.TXT](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/LICENSE.TXT) |
| [THIRD-PARTY-NOTICES.TXT](evidence/notices/THIRD-PARTY-NOTICES.TXT) | [THIRD-PARTY-NOTICES.TXT](https://github.com/dotnet/diagnostics/blob/1d95e75015fa3ccd063a59ed3d0bfe26040a6637/THIRD-PARTY-NOTICES.TXT) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-diagnostics-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
