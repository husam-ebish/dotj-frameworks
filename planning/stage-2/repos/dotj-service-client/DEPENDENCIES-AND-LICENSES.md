# DJ-017 .j Service Client: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: XML streaming, sockets, HTTP client, JCA and optional OS bindings.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | Newtonsoft.Json | [Directory.Build.props](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/Directory.Build.props) |
| PackageReference | Microsoft.ManifestTool.CrossPlatform | [eng/common/internal/Tools.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Core | [eng/common/internal/Tools.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [eng/common/internal/Tools.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.DotNet.IBCMerge | [eng/common/internal/Tools.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/eng/common/internal/Tools.csproj) |
| PackageReference | Drop.App | [eng/common/internal/Tools.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/eng/common/internal/Tools.csproj) |
| ProjectReference | ..\CertificateGeneratorLibrary\CertificateGeneratorLibrary.csproj | [src/System.Private.ServiceModel/tools/CertificateGenerator/CertificateGenerator/CertificateGenerator.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.Private.ServiceModel/tools/CertificateGenerator/CertificateGenerator/CertificateGenerator.csproj) |
| PackageReference | System.Configuration.ConfigurationManager | [src/System.Private.ServiceModel/tools/CertificateGenerator/CertificateGenerator/CertificateGenerator.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.Private.ServiceModel/tools/CertificateGenerator/CertificateGenerator/CertificateGenerator.csproj) |
| PackageReference | Microsoft.Crank.EventSources | [src/System.Private.ServiceModel/tests/Benchmarks/WCFCorePerf/WCFCorePerf/WCFCorePerf.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.Private.ServiceModel/tests/Benchmarks/WCFCorePerf/WCFCorePerf/WCFCorePerf.csproj) |
| PackageReference | System.ServiceModel.Duplex | [src/System.Private.ServiceModel/tests/Benchmarks/WCFCorePerf/WCFCorePerf/WCFCorePerf.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.Private.ServiceModel/tests/Benchmarks/WCFCorePerf/WCFCorePerf/WCFCorePerf.csproj) |
| PackageReference | System.ServiceModel.Http | [src/System.Private.ServiceModel/tests/Benchmarks/WCFCorePerf/WCFCorePerf/WCFCorePerf.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.Private.ServiceModel/tests/Benchmarks/WCFCorePerf/WCFCorePerf/WCFCorePerf.csproj) |
| PackageReference | System.ServiceModel.NetTcp | [src/System.Private.ServiceModel/tests/Benchmarks/WCFCorePerf/WCFCorePerf/WCFCorePerf.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.Private.ServiceModel/tests/Benchmarks/WCFCorePerf/WCFCorePerf/WCFCorePerf.csproj) |
| PackageReference | System.ServiceModel.Security | [src/System.Private.ServiceModel/tests/Benchmarks/WCFCorePerf/WCFCorePerf/WCFCorePerf.csproj](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.Private.ServiceModel/tests/Benchmarks/WCFCorePerf/WCFCorePerf/WCFCorePerf.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.TXT](evidence/notices/LICENSE.TXT) | [LICENSE.TXT](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/LICENSE.TXT) |
| [THIRD-PARTY-NOTICES.TXT](evidence/notices/THIRD-PARTY-NOTICES.TXT) | [THIRD-PARTY-NOTICES.TXT](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/THIRD-PARTY-NOTICES.TXT) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-service-client-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
