# DJ-025 .j Container: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Reflection, MethodHandles, AutoCloseable and ServiceLoader.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | Microsoft.CodeAnalysis.CSharp | [codegen/Autofac.CodeGen/Autofac.CodeGen.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/codegen/Autofac.CodeGen/Autofac.CodeGen.csproj) |
| PackageReference | StyleCop.Analyzers | [codegen/Autofac.CodeGen/Autofac.CodeGen.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/codegen/Autofac.CodeGen/Autofac.CodeGen.csproj) |
| ProjectReference | ../../codegen/Autofac.CodeGen/Autofac.CodeGen.csproj | [src/Autofac/Autofac.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Autofac.csproj) |
| PackageReference | Microsoft.SourceLink.GitHub | [src/Autofac/Autofac.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Autofac.csproj) |
| PackageReference | SonarAnalyzer.CSharp | [src/Autofac/Autofac.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Autofac.csproj) |
| PackageReference | StyleCop.Analyzers | [src/Autofac/Autofac.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Autofac.csproj) |
| PackageReference | System.Diagnostics.DiagnosticSource | [src/Autofac/Autofac.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Autofac.csproj) |
| PackageReference | Microsoft.Bcl.AsyncInterfaces | [src/Autofac/Autofac.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Autofac.csproj) |
| ProjectReference | ..\..\src\Autofac\Autofac.csproj | [test/Autofac.Specification.Test/Autofac.Specification.Test.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Specification.Test/Autofac.Specification.Test.csproj) |
| ProjectReference | ..\Autofac.Test.Scenarios.ScannedAssembly\Autofac.Test.Scenarios.ScannedAssembly.csproj | [test/Autofac.Specification.Test/Autofac.Specification.Test.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Specification.Test/Autofac.Specification.Test.csproj) |
| ProjectReference | ..\Autofac.Test.Scenarios.LoadContext\Autofac.Test.Scenarios.LoadContext.csproj | [test/Autofac.Specification.Test/Autofac.Specification.Test.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Specification.Test/Autofac.Specification.Test.csproj) |
| PackageReference | coverlet.collector | [test/Autofac.Specification.Test/Autofac.Specification.Test.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Specification.Test/Autofac.Specification.Test.csproj) |
| PackageReference | Microsoft.NET.Test.Sdk | [test/Autofac.Specification.Test/Autofac.Specification.Test.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Specification.Test/Autofac.Specification.Test.csproj) |
| PackageReference | SonarAnalyzer.CSharp | [test/Autofac.Specification.Test/Autofac.Specification.Test.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Specification.Test/Autofac.Specification.Test.csproj) |
| PackageReference | StyleCop.Analyzers | [test/Autofac.Specification.Test/Autofac.Specification.Test.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Specification.Test/Autofac.Specification.Test.csproj) |
| PackageReference | xunit | [test/Autofac.Specification.Test/Autofac.Specification.Test.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Specification.Test/Autofac.Specification.Test.csproj) |
| PackageReference | xunit.runner.visualstudio | [test/Autofac.Specification.Test/Autofac.Specification.Test.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Specification.Test/Autofac.Specification.Test.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-container-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
