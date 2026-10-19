# DJ-020 .j SQL: dependencies and licenses

## Proposed Java dependencies

postgresql,core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: JDBC interfaces, reflection and MethodHandles; own driver supplies database transport.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | EntityFramework | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | FastMember | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Microsoft.CSharp | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Microsoft.NETFramework.ReferenceAssemblies | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Microsoft.SourceLink.GitHub | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Microsoft.SqlServer.Types | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Nerdbank.GitVersioning | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.PublicApiAnalyzers | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | System.Reflection.Emit.Lightweight | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | System.Threading.Tasks.Extensions | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Azure.Identity | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Belgrade.Sql.Client | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Dashing | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Dapper.Contrib | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | DuckDB.NET.Data.Full | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | DevExpress.Xpo | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | FirebirdSql.Data.FirebirdClient | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | GitHubActionsTestLogger | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Iesi.Collections | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | linq2db.SqlServer | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | log4net | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.SqlClient | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.Sqlite | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.SqlServer | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Mighty | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | MySqlConnector | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | NHibernate | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Norm.net | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Npgsql | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | PetaPoco | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | RepoDb.SqlServer | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | ServiceStack.OrmLite.SqlServer | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Snowflake.Data | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | SqlMarshal | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | SubSonic | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | Susanoo.SqlServer | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | System.Data.SqlClient | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | System.Data.SQLite | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | System.Net.Http | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | System.Private.Uri | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | System.Reflection.Metadata | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Xml | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | System.Text.RegularExpressions | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | System.ValueTuple | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | xunit | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Packages.props) |
| PackageReference | Microsoft.NETFramework.ReferenceAssemblies | [Directory.Build.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Build.props) |
| PackageReference | Microsoft.SourceLink.GitHub | [Directory.Build.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Build.props) |
| PackageReference | Nerdbank.GitVersioning | [Directory.Build.props](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Directory.Build.props) |
| ProjectReference | benchmarks/**/*.csproj | [Build.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Build.csproj) |
| ProjectReference | Dapper*/*.csproj | [Build.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Build.csproj) |
| ProjectReference | tests/**/*.csproj | [Build.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Build.csproj) |
| ProjectReference | ..\Dapper.StrongName\Dapper.StrongName.csproj | [Dapper.EntityFramework.StrongName/Dapper.EntityFramework.StrongName.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper.EntityFramework.StrongName/Dapper.EntityFramework.StrongName.csproj) |
| PackageReference | EntityFramework | [Dapper.EntityFramework.StrongName/Dapper.EntityFramework.StrongName.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper.EntityFramework.StrongName/Dapper.EntityFramework.StrongName.csproj) |
| PackageReference | Microsoft.SqlServer.Types | [Dapper.EntityFramework.StrongName/Dapper.EntityFramework.StrongName.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper.EntityFramework.StrongName/Dapper.EntityFramework.StrongName.csproj) |
| PackageReference | BLToolkit | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Dashing | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Belgrade.Sql.Client | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | BenchmarkDotNet | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | DevExpress.Xpo | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | EntityFramework | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | linq2db.SqlServer | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | MySqlConnector | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | NHibernate | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Iesi.Collections | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Mighty | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | PetaPoco | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | RepoDb.SqlServer | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | ServiceStack.OrmLite.SqlServer | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | SqlMarshal | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | System.Data.SQLite | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | System.Reflection.Metadata | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | System.Data.SqlClient | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | System.Security.Cryptography.Xml | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Npgsql | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Npgsql | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | System.Text.RegularExpressions | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | System.Private.Uri | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Microsoft.Data.SqlClient | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | System.Net.Http | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Azure.Identity | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| ProjectReference | ../../Dapper.EntityFramework/Dapper.EntityFramework.csproj | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Microsoft.SqlServer.Types | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Susanoo.SqlServer | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Microsoft.EntityFrameworkCore.SqlServer | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Microsoft.EntityFrameworkCore.SqlServer | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Norm.net | [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) |
| PackageReference | Microsoft.CodeAnalysis.PublicApiAnalyzers | [Dapper/Dapper.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/Dapper.csproj) |
| PackageReference | Microsoft.Bcl.AsyncInterfaces | [Dapper/Dapper.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/Dapper.csproj) |
| PackageReference | System.Threading.Tasks.Extensions | [Dapper/Dapper.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/Dapper.csproj) |
| PackageReference | Microsoft.Bcl.AsyncInterfaces | [Dapper/Dapper.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/Dapper.csproj) |
| PackageReference | System.Reflection.Emit.Lightweight | [Dapper/Dapper.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/Dapper.csproj) |
| PackageReference | System.Threading.Tasks.Extensions | [Dapper/Dapper.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/Dapper.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `NOASSERTION`.

The inspected source has Apache license text. Logos and external Dapper extensions are not automatically covered by this source-scope decision.

| Retrieved notice/license | Immutable source |
|---|---|
| [License.txt](evidence/notices/License.txt) | [License.txt](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/License.txt) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-sql-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
