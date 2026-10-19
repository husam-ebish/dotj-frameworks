# DJ-065 .j Mediator: dependencies and licenses

## Proposed Java dependencies

core;container(optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Functional interfaces, type tokens, CompletionStage and Flow where explicit.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | IsExternalInit | [src/MediatR/MediatR.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/MediatR.csproj) |
| PackageReference | MediatR.Contracts | [src/MediatR/MediatR.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/MediatR.csproj) |
| PackageReference | Microsoft.Bcl.AsyncInterfaces | [src/MediatR/MediatR.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/MediatR.csproj) |
| PackageReference | Microsoft.Extensions.DependencyInjection.Abstractions | [src/MediatR/MediatR.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/MediatR.csproj) |
| PackageReference | Microsoft.Extensions.Logging.Abstractions | [src/MediatR/MediatR.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/MediatR.csproj) |
| PackageReference | Microsoft.IdentityModel.JsonWebTokens | [src/MediatR/MediatR.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/MediatR.csproj) |
| PackageReference | Microsoft.SourceLink.GitHub | [src/MediatR/MediatR.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/MediatR.csproj) |
| PackageReference | MinVer | [src/MediatR/MediatR.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/MediatR.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

The inspected LICENSE.md offers RPL 1.5 terms or a separate agreement. Do not assume historical MIT terms apply to the inspected revision. Resolve rights before source reuse.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.md](evidence/notices/LICENSE.md) | [LICENSE.md](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/LICENSE.md) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-mediator-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
