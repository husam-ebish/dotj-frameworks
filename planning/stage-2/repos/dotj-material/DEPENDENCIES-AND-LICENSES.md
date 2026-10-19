# DJ-046 .j Material: dependencies and licenses

## Proposed Java dependencies

web,validation

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: dotj-web component runtime, CSS and minimal owned browser scripts.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | Microsoft.AspNetCore.Components | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| PackageReference | Microsoft.AspNetCore.Components.Web | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| PackageReference | Microsoft.Extensions.Localization | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| PackageReference | Microsoft.AspNetCore.Components | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| PackageReference | Microsoft.AspNetCore.Components.Web | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| PackageReference | Microsoft.Extensions.Localization | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| PackageReference | Microsoft.AspNetCore.Components | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| PackageReference | Microsoft.AspNetCore.Components.Web | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| PackageReference | Microsoft.Extensions.Localization | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| PackageReference | Microsoft.CodeAnalysis.ResxSourceGenerator | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| PackageReference | NetEscapades.EnumGenerators.Generators | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| ProjectReference | ..\MudBlazor.Analyzers\MudBlazor.Analyzers.csproj | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |
| ProjectReference | ..\MudBlazor.Analyzers.CodeFixes\MudBlazor.Analyzers.CodeFixes.csproj | [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-material-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
