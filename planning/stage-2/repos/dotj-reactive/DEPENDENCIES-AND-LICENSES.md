# DJ-028 .j Reactive: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Executors and java.util.concurrent.Flow where backpressure contracts align.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| ProjectReference | ..\System.Reactive.Async\System.Reactive.Async.csproj | [AsyncRx.NET/ApiCompare/ApiCompare.csproj](https://github.com/dotnet/reactive/blob/89e05b8730107983c3f77af54a52974ae12d37f4/AsyncRx.NET/ApiCompare/ApiCompare.csproj) |
| ProjectReference | ..\System.Reactive.Async\System.Reactive.Async.csproj | [AsyncRx.NET/Playground/Playground.csproj](https://github.com/dotnet/reactive/blob/89e05b8730107983c3f77af54a52974ae12d37f4/AsyncRx.NET/Playground/Playground.csproj) |
| PackageReference | Microsoft.Reactive.Testing | [AsyncRx.NET/Microsoft.Reactive.Testing.Async/Microsoft.Reactive.Testing.Async.csproj](https://github.com/dotnet/reactive/blob/89e05b8730107983c3f77af54a52974ae12d37f4/AsyncRx.NET/Microsoft.Reactive.Testing.Async/Microsoft.Reactive.Testing.Async.csproj) |
| ProjectReference | ..\System.Reactive.Async\System.Reactive.Async.csproj | [AsyncRx.NET/Microsoft.Reactive.Testing.Async/Microsoft.Reactive.Testing.Async.csproj](https://github.com/dotnet/reactive/blob/89e05b8730107983c3f77af54a52974ae12d37f4/AsyncRx.NET/Microsoft.Reactive.Testing.Async/Microsoft.Reactive.Testing.Async.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/dotnet/reactive/blob/89e05b8730107983c3f77af54a52974ae12d37f4/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-reactive-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
