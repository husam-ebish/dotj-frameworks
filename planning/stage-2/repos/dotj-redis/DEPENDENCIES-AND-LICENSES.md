# DJ-022 .j Redis: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: NIO sockets, TLS, executors and buffers.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.PerformanceCounter | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.Threading.Channels | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.Runtime.InteropServices.RuntimeInformation | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.IO.Compression | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.IO.Pipelines | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.IO.Hashing | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.Buffers | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.Memory | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | GitHubActionsTestLogger | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Analyzer.Testing | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.CodeFix.Testing | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.PublicApiAnalyzers | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Microsoft.NETFramework.ReferenceAssemblies | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Platform | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Nerdbank.GitVersioning | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | NSubstitute | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | StackExchange.Redis | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | StackExchange.Redis.StrongName | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | StyleCop.Analyzers | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.Collections.Immutable | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.Reflection.Metadata | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.Runtime.Caching | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | xunit.v3 | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | xunit.v3.runner.console | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageVersion | System.Private.Uri | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props) |
| PackageReference | Microsoft.NETFramework.ReferenceAssemblies | [Directory.Build.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Build.props) |
| ProjectReference | ..\..\eng\StackExchange.Redis.Build\StackExchange.Redis.Build.csproj | [Directory.Build.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Build.props) |
| ProjectReference | eng\**\*.csproj | [Build.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Build.csproj) |
| ProjectReference | src\**\*.csproj | [Build.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Build.csproj) |
| ProjectReference | tests\**\*.csproj | [Build.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Build.csproj) |
| ProjectReference | toys\**\*.csproj | [Build.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Build.csproj) |
| PackageReference | BenchmarkDotNet | [tests/BasicTest/BasicTest.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/BasicTest/BasicTest.csproj) |
| PackageReference | System.Collections.Immutable | [tests/BasicTest/BasicTest.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/BasicTest/BasicTest.csproj) |
| PackageReference | System.Reflection.Metadata | [tests/BasicTest/BasicTest.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/BasicTest/BasicTest.csproj) |
| ProjectReference | ..\..\src\StackExchange.Redis\StackExchange.Redis.csproj | [tests/BasicTest/BasicTest.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/BasicTest/BasicTest.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `NOASSERTION`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-redis-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
