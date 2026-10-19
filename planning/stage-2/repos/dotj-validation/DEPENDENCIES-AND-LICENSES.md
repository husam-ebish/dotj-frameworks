# DJ-026 .j Validation: dependencies and licenses

## Proposed Java dependencies

core;web(optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Functional interfaces, regex, resource bundles and CompletionStage.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | Microsoft.Extensions.DependencyInjection.Abstractions | [src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj) |
| ProjectReference | ..\FluentValidation\FluentValidation.csproj | [src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj) |
| PackageReference | Zomp.SyncMethodGenerator | [src/FluentValidation/FluentValidation.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/FluentValidation.csproj) |
| PackageReference | BenchmarkDotNet | [src/FluentValidation.Tests.Benchmarks/FluentValidation.Tests.Benchmarks.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests.Benchmarks/FluentValidation.Tests.Benchmarks.csproj) |
| PackageReference | Bogus | [src/FluentValidation.Tests.Benchmarks/FluentValidation.Tests.Benchmarks.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests.Benchmarks/FluentValidation.Tests.Benchmarks.csproj) |
| ProjectReference | ..\FluentValidation\FluentValidation.csproj | [src/FluentValidation.Tests.Benchmarks/FluentValidation.Tests.Benchmarks.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests.Benchmarks/FluentValidation.Tests.Benchmarks.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `Apache-2.0`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [License.txt](evidence/notices/License.txt) | [License.txt](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/License.txt) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-validation-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
