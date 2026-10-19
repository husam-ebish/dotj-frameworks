# DJ-058 .j OpenXML: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: ZIP, XML streaming, URI and JDK signatures where sufficient.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet.Diagnostics.Windows | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | coverlet.collector | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.Memory | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.BuildTools.GenAPI | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.SourceGenerators.Testing | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.PublicApiAnalyzers | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | Microsoft.NETFramework.ReferenceAssemblies | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.CodeCoverage | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | NSubstitute | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | NuGet.Common | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | NuGet.Packaging | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | NuGet.Protocol | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | NuGet.Resolver | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | ObjectLayoutInspector | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | StyleCop.Analyzers | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | Svg | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | System.CodeDom | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | System.Collections.Immutable | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | System.Net.Http | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Algorithms | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | System.Xml.ReaderWriter | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | System.ValueTuple | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | xunit.v3.mtp-v2 | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | System.IO.Packaging | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageVersion | System.IO.Packaging | [Directory.Packages.props](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/Directory.Packages.props) |
| PackageReference | System.Text.Json | [gen/DocumentFormat.OpenXml.Generator.Models/DocumentFormat.OpenXml.Generator.Models.csproj](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/gen/DocumentFormat.OpenXml.Generator.Models/DocumentFormat.OpenXml.Generator.Models.csproj) |
| PackageReference | System.Collections.Immutable | [gen/DocumentFormat.OpenXml.Generator.Models/DocumentFormat.OpenXml.Generator.Models.csproj](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/gen/DocumentFormat.OpenXml.Generator.Models/DocumentFormat.OpenXml.Generator.Models.csproj) |
| PackageReference | BenchmarkDotNet | [test/DocumentFormat.OpenXml.Benchmarks/DocumentFormat.OpenXml.Benchmarks.csproj](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/test/DocumentFormat.OpenXml.Benchmarks/DocumentFormat.OpenXml.Benchmarks.csproj) |
| PackageReference | BenchmarkDotNet.Diagnostics.Windows | [test/DocumentFormat.OpenXml.Benchmarks/DocumentFormat.OpenXml.Benchmarks.csproj](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/test/DocumentFormat.OpenXml.Benchmarks/DocumentFormat.OpenXml.Benchmarks.csproj) |
| ProjectReference | ..\..\src\DocumentFormat.OpenXml\DocumentFormat.OpenXml.csproj | [test/DocumentFormat.OpenXml.Benchmarks/DocumentFormat.OpenXml.Benchmarks.csproj](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/test/DocumentFormat.OpenXml.Benchmarks/DocumentFormat.OpenXml.Benchmarks.csproj) |
| ProjectReference | ..\DocumentFormat.OpenXml.Tests.Assets\DocumentFormat.OpenXml.Tests.Assets.csproj | [test/DocumentFormat.OpenXml.Benchmarks/DocumentFormat.OpenXml.Benchmarks.csproj](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/test/DocumentFormat.OpenXml.Benchmarks/DocumentFormat.OpenXml.Benchmarks.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/LICENSE) |
| [NOTICE](evidence/notices/NOTICE) | [NOTICE](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/NOTICE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-openxml-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
