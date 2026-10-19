# DJ-027 .j Resilience: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Executors, ScheduledExecutorService, atomic state and monotonic clocks.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Cake.FileHelpers | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Flurl.Http.Signed | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | FsCheck.Xunit.v3 | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | FSharp.Core | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | GitHubActionsTestLogger | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | IcedTasks | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.BannedApiAnalyzers | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.PublicApiAnalyzers | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Caching.Memory | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http.Resilience | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Console | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options.ConfigurationExtensions | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.TimeProvider.Testing | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.CodeCoverage | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Platform | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | MinVer | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | NSubstitute | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Polly | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Polly.Contrib.WaitAndRetry | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Polly.Core | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Polly.Extensions | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Polly.RateLimiting | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Polly.Testing | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Refit.HttpClientFactory | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | RestSharp | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Shouldly | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | SonarAnalyzer.CSharp | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | StyleCop.Analyzers | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | System.ComponentModel.Annotations | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | System.Memory | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | System.Threading.Tasks.Extensions | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | System.ValueTuple | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | xunit.v3.assert | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | xunit.v3.mtp-v2 | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.TimeProvider | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.DiagnosticSource | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageVersion | System.Threading.RateLimiting | [Directory.Packages.props](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/Directory.Packages.props) |
| PackageReference | Microsoft.Bcl.AsyncInterfaces | [src/Polly.Core/Polly.Core.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Polly.Core.csproj) |
| PackageReference | Microsoft.Bcl.TimeProvider | [src/Polly.Core/Polly.Core.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Polly.Core.csproj) |
| PackageReference | System.Threading.Tasks.Extensions | [src/Polly.Core/Polly.Core.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Polly.Core.csproj) |
| PackageReference | System.ValueTuple | [src/Polly.Core/Polly.Core.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Polly.Core.csproj) |
| PackageReference | System.ComponentModel.Annotations | [src/Polly.Core/Polly.Core.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Polly.Core.csproj) |
| ProjectReference | ..\Polly.Core\Polly.Core.csproj | [src/Polly.Extensions/Polly.Extensions.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Extensions/Polly.Extensions.csproj) |
| PackageReference | Microsoft.Extensions.Options | [src/Polly.Extensions/Polly.Extensions.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Extensions/Polly.Extensions.csproj) |
| PackageReference | Microsoft.Extensions.Logging.Abstractions | [src/Polly.Extensions/Polly.Extensions.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Extensions/Polly.Extensions.csproj) |
| PackageReference | System.Diagnostics.DiagnosticSource | [src/Polly.Extensions/Polly.Extensions.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Extensions/Polly.Extensions.csproj) |
| ProjectReference | ..\Polly.Core\Polly.Core.csproj | [src/Polly.Testing/Polly.Testing.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Testing/Polly.Testing.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `BSD-3-Clause`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-resilience-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
