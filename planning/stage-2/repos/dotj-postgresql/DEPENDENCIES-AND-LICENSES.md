# DJ-021 .j PostgreSQL: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Sockets/SSLEngine, JCA SCRAM primitives, ByteBuffer and java.sql; no existing JDBC driver substitution.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.API | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | NetTopologySuite | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | NetTopologySuite.IO.PostGIS | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | NodaTime | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | GeoJSON.Net | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Microsoft.SourceLink.GitHub | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.PublicApiAnalyzers | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Scriban.Signed | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | NUnit | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | NUnit.Analyzers | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Console | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | NUnit3TestAdapter | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | xunit | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | GitHubActionsTestLogger | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | AdoNet.Specification.Tests | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | OpenTelemetry | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.InMemory | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.SqlClient | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet.Diagnostics.Windows | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageVersion | Mono.Cecil | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props) |
| PackageReference | GeoJSON.Net | [src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj) |
| PackageReference | Microsoft.CodeAnalysis.PublicApiAnalyzers | [src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj) |
| ProjectReference | ../Npgsql/Npgsql.csproj | [src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj) |
| ProjectReference | ../Npgsql.SourceGenerators/Npgsql.SourceGenerators.csproj | [src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj) |
| PackageReference | Newtonsoft.Json | [src/Npgsql.Json.NET/Npgsql.Json.NET.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.Json.NET/Npgsql.Json.NET.csproj) |
| PackageReference | Microsoft.CodeAnalysis.PublicApiAnalyzers | [src/Npgsql.Json.NET/Npgsql.Json.NET.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.Json.NET/Npgsql.Json.NET.csproj) |
| ProjectReference | ..\Npgsql\Npgsql.csproj | [src/Npgsql.Json.NET/Npgsql.Json.NET.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.Json.NET/Npgsql.Json.NET.csproj) |
| PackageReference | Mono.Cecil | [test/MStatDumper/MStatDumper.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/MStatDumper/MStatDumper.csproj) |
| PackageReference | Microsoft.Extensions.Logging.Abstractions | [src/Npgsql/Npgsql.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/Npgsql.csproj) |
| PackageReference | Microsoft.Extensions.DependencyInjection.Abstractions | [src/Npgsql/Npgsql.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/Npgsql.csproj) |
| PackageReference | Microsoft.CodeAnalysis.PublicApiAnalyzers | [src/Npgsql/Npgsql.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/Npgsql.csproj) |
| ProjectReference | ../Npgsql.SourceGenerators/Npgsql.SourceGenerators.csproj | [src/Npgsql/Npgsql.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/Npgsql.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `PostgreSQL`.

The inspected project uses PostgreSQL-style terms. Preserve the exact source notices; optional authentication/native dependencies require separate records.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-postgresql-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
