# DJ-039 .j GraphQL: dependencies and licenses

## Proposed Java dependencies

core,json;web(optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Collections, executors, own JSON and optional web transport.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | PolySharp | [Directory.Build.props](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/Directory.Build.props) |
| PackageReference | Roslynator.Analyzers | [Directory.Build.props](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/Directory.Build.props) |
| PackageReference | Roslynator.Formatting.Analyzers | [Directory.Build.props](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/Directory.Build.props) |
| PackageReference | GraphQL-Parser | [src/GraphQL/GraphQL.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/GraphQL.csproj) |
| PackageReference | Microsoft.CSharp | [src/GraphQL/GraphQL.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/GraphQL.csproj) |
| PackageReference | Nullability.Source | [src/GraphQL/GraphQL.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/GraphQL.csproj) |
| PackageReference | System.ComponentModel.Annotations | [src/GraphQL/GraphQL.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/GraphQL.csproj) |
| PackageReference | System.Memory | [src/GraphQL/GraphQL.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/GraphQL.csproj) |
| PackageReference | Microsoft.Bcl.AsyncInterfaces | [src/GraphQL/GraphQL.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/GraphQL.csproj) |
| PackageReference | System.Runtime.CompilerServices.Unsafe | [src/GraphQL/GraphQL.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/GraphQL.csproj) |
| ProjectReference | ..\GraphQL.Analyzers.Package\GraphQL.Analyzers.Package.csproj | [src/GraphQL/GraphQL.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/GraphQL.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.md](evidence/notices/LICENSE.md) | [LICENSE.md](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/LICENSE.md) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-graphql-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
