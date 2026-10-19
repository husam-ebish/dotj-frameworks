# DJ-033 .j Refit: dependencies and licenses

## Proposed Java dependencies

rest,json;code(dev-optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Annotation processing, reflection fallback and JDK HTTP client via own REST transport.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | ReactiveUI.Primitives | [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj) |
| PackageReference | System.Text.Json | [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj) |
| PackageReference | System.Net.Http.Json | [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj) |
| PackageReference | System.Net.ServerSentEvents | [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj) |
| PackageVersion | Microsoft.NETFramework.ReferenceAssemblies | [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj) |
| PackageReference | Microsoft.NETFramework.ReferenceAssemblies | [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj) |
| ProjectReference | ..\InterfaceStubGenerator.Roslyn48\InterfaceStubGenerator.Roslyn48.csproj | [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj) |
| ProjectReference | ..\Refit.Analyzers.Roslyn48\Refit.Analyzers.Roslyn48.csproj | [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj) |
| ProjectReference | ..\Refit.CodeFixes.Roslyn48\Refit.CodeFixes.Roslyn48.csproj | [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj) |
| PackageVersion | Newtonsoft.Json | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | ReactiveUI.Primitives | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | MinVer | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.SourceLink.GitHub | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | StyleSharp.Analyzers | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | PerformanceSharp.Analyzers | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | SecuritySharp.Analyzers | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | PublicApiSharp.Analyzers | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.SourceGenerators.Testing | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | TUnit | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.CodeCoverage | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.TimeProvider.Testing | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Serilog | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Serilog.Sinks.Console | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http.Resilience | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | OpenTelemetry | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.InMemory | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.Http | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | System.Net.Http | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | System.Text.RegularExpressions | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | System.Net.Http.Json | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | System.Net.ServerSentEvents | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | System.Net.Http.Json | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | System.Net.ServerSentEvents | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Components.WebAssembly | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Components.WebAssembly.DevServer | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.WebUtilities | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Components.WebAssembly | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Components.WebAssembly.DevServer | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.WebUtilities | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Components.WebAssembly | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Components.WebAssembly.DevServer | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.WebUtilities | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Components.WebAssembly | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Components.WebAssembly.DevServer | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.WebUtilities | [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |


## License evidence and eligibility gate

Observed metadata hint: `NOASSERTION`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-refit-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
