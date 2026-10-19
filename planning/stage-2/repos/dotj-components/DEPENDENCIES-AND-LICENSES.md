# DJ-047 .j Components: dependencies and licenses

## Proposed Java dependencies

web

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Owned component runtime, SVG/canvas/DOM and CSS.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | Microsoft.AspNetCore.Components | [Radzen.Blazor/Radzen.Blazor.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/Radzen.Blazor.csproj) |
| PackageReference | Microsoft.AspNetCore.Components.Web | [Radzen.Blazor/Radzen.Blazor.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/Radzen.Blazor.csproj) |
| PackageReference | Microsoft.AspNetCore.Components | [Radzen.Blazor/Radzen.Blazor.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/Radzen.Blazor.csproj) |
| PackageReference | Microsoft.AspNetCore.Components.Web | [Radzen.Blazor/Radzen.Blazor.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/Radzen.Blazor.csproj) |
| PackageReference | Microsoft.AspNetCore.Components | [Radzen.Blazor/Radzen.Blazor.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/Radzen.Blazor.csproj) |
| PackageReference | Microsoft.AspNetCore.Components.Web | [Radzen.Blazor/Radzen.Blazor.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/Radzen.Blazor.csproj) |
| PackageReference | Microsoft.Extensions.AI | [Radzen.Blazor/Radzen.Blazor.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/Radzen.Blazor.csproj) |
| PackageReference | Radzen.MSBuild | [Radzen.Blazor/Radzen.Blazor.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/Radzen.Blazor.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-components-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
