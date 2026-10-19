# DJ-032 .j REST: dependencies and licenses

## Proposed Java dependencies

json,core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: java.net.http.HttpClient and own JSON serializer.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Microsoft.Extensions.Http | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | CsvHelper | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | MinVer | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | Nullable | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | Microsoft.NETFramework.ReferenceAssemblies.net472 | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | Microsoft.SourceLink.GitHub | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | JetBrains.Annotations | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | HttpMultipartParser | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | PolySharp | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | AutoFixture | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | coverlet.collector | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | FluentAssertions | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.TestHost | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | Polly | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | rest-mock-core | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | RichardSzalay.MockHttp | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | System.Net.Http.Json | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | Xunit.Extensions.Logging | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | xunit | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | WireMock.Net | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageVersion | WireMock.Net.FluentAssertions | [Directory.Packages.props](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/Directory.Packages.props) |
| PackageReference | Nullable | [src/RestSharp/RestSharp.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/RestSharp.csproj) |
| ProjectReference | $(RepoRoot)\gen\SourceGenerator\SourceGenerator.csproj | [src/RestSharp/RestSharp.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/RestSharp.csproj) |
| PackageReference | System.Text.Json | [src/RestSharp/RestSharp.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/RestSharp.csproj) |
| PackageReference | System.Text.Json | [src/RestSharp/RestSharp.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/RestSharp.csproj) |
| PackageReference | System.Text.Json | [src/RestSharp/RestSharp.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/RestSharp.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `Apache-2.0`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.txt](evidence/notices/LICENSE.txt) | [LICENSE.txt](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/LICENSE.txt) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-rest-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
