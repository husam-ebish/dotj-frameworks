# DJ-055 .j Benchmark: dependencies and licenses

## Proposed Java dependencies

core;diagnostics(optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: ProcessBuilder, System.nanoTime, JFR and management APIs.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | Microsoft.TestPlatform.AdapterUtilities | [src/BenchmarkDotNet.TestAdapter/BenchmarkDotNet.TestAdapter.csproj](https://github.com/dotnet/BenchmarkDotNet/blob/730b8b7cc67b8d75a7478e67eaa2b10af5ec562d/src/BenchmarkDotNet.TestAdapter/BenchmarkDotNet.TestAdapter.csproj) |
| PackageReference | Microsoft.TestPlatform.ObjectModel | [src/BenchmarkDotNet.TestAdapter/BenchmarkDotNet.TestAdapter.csproj](https://github.com/dotnet/BenchmarkDotNet/blob/730b8b7cc67b8d75a7478e67eaa2b10af5ec562d/src/BenchmarkDotNet.TestAdapter/BenchmarkDotNet.TestAdapter.csproj) |
| PackageReference | Microsoft.TestPlatform.TranslationLayer | [src/BenchmarkDotNet.TestAdapter/BenchmarkDotNet.TestAdapter.csproj](https://github.com/dotnet/BenchmarkDotNet/blob/730b8b7cc67b8d75a7478e67eaa2b10af5ec562d/src/BenchmarkDotNet.TestAdapter/BenchmarkDotNet.TestAdapter.csproj) |
| ProjectReference | ..\BenchmarkDotNet\BenchmarkDotNet.csproj | [src/BenchmarkDotNet.TestAdapter/BenchmarkDotNet.TestAdapter.csproj](https://github.com/dotnet/BenchmarkDotNet/blob/730b8b7cc67b8d75a7478e67eaa2b10af5ec562d/src/BenchmarkDotNet.TestAdapter/BenchmarkDotNet.TestAdapter.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.md](evidence/notices/LICENSE.md) | [LICENSE.md](https://github.com/dotnet/BenchmarkDotNet/blob/730b8b7cc67b8d75a7478e67eaa2b10af5ec562d/LICENSE.md) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-benchmark-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
