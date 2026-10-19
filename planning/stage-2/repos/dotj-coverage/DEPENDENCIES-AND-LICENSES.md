# DJ-054 .j Coverage: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: java.lang.instrument, standard class-file API and classloaders.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet.TestAdapter | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet.Diagnostics.Windows | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.DiagnosticsHub.BenchmarkDotNetDiagnosers | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.DiagnosticsHub.BenchmarkDotNetDiagnosers | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | DotNetConfig | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Utilities.Core | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Framework | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Locator | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.BannedApiAnalyzers | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyModel | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Json | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileSystemGlobbing | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Sbom.Targets | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.TestPlatform.ObjectModel | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Platform | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.TrxReport.Abstractions | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.HangDump | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.CrashDump | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Platform.MSBuild | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.TrxReport | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.AzureDevOpsReport | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | MSTest | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | MSTest.TestFramework | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | NuGet.Frameworks | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | NuGet.Packaging | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | NuGet.Versioning | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Mono.Cecil | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | ReportGenerator.Core | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | ReportGenerator.Core | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | LinqKit.Microsoft.EntityFrameworkCore | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.CommandLine | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | xunit.v3 | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | xunit.v3.mtp-v2 | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | xunit.v3.runner.msbuild | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Buffers | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Collections.Immutable | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Configuration.ConfigurationManager | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.EventLog | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Formats.Asn1 | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.IO.Pipelines | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Linq.Async | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Memory | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Net.Http | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Reflection.Metadata | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Runtime.CompilerServices.Unsafe | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Security.AccessControl | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Text.Encoding.CodePages | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Text.RegularExpressions | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageVersion | System.Threading.Tasks.Extensions | [Directory.Packages.props](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/Directory.Packages.props) |
| PackageReference | System.CommandLine | [src/coverlet.console/coverlet.console.csproj](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/src/coverlet.console/coverlet.console.csproj) |
| PackageReference | Microsoft.Extensions.DependencyInjection | [src/coverlet.console/coverlet.console.csproj](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/src/coverlet.console/coverlet.console.csproj) |
| PackageReference | Microsoft.Sbom.Targets | [src/coverlet.console/coverlet.console.csproj](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/src/coverlet.console/coverlet.console.csproj) |
| ProjectReference | $(MSBuildThisFileDirectory)..\coverlet.core\coverlet.core.csproj | [src/coverlet.console/coverlet.console.csproj](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/src/coverlet.console/coverlet.console.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/LICENSE) |
| [THIRD-PARTY-NOTICES.txt](evidence/notices/THIRD-PARTY-NOTICES.txt) | [THIRD-PARTY-NOTICES.txt](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/THIRD-PARTY-NOTICES.txt) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-coverage-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
