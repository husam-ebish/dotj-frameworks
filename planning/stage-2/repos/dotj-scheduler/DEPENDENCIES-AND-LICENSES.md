# DJ-030 .j Scheduler: dependencies and licenses

## Proposed Java dependencies

core;postgresql(optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: java.time, monotonic timing, executors and JDBC-compatible storage.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | NUnit | [Directory.Build.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Build.props) |
| PackageReference | NUnit.Analyzers | [Directory.Build.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Build.props) |
| PackageReference | NUnit3TestAdapter | [Directory.Build.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Build.props) |
| PackageReference | Microsoft.NET.Test.Sdk | [Directory.Build.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Build.props) |
| PackageReference | coverlet.MTP | [Directory.Build.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Build.props) |
| PackageReference | GitHubActionsTestLogger | [Directory.Build.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Build.props) |
| PackageReference | Microsoft.Testing.Extensions.CrashDump | [Directory.Build.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Build.props) |
| PackageReference | Microsoft.Testing.Extensions.HangDump | [Directory.Build.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Build.props) |
| PackageReference | Microsoft.Testing.Extensions.TrxReport | [Directory.Build.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Build.props) |
| PackageVersion | Aspire.Hosting.AppHost | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.PostgreSQL | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Aspire.Npgsql | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | AwesomeAssertions | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | AwesomeAssertions.Analyzers | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | bunit | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | coverlet.MTP | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | FakeItEasy | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | FirebirdSql.Data.FirebirdClient | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | FSharp.Core | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | GitHubActionsTestLogger | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Marten | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | MELT | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | MessagePack | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.Testing | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.BannedApiAnalyzers | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.SQLite | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.SqlClient | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.Testing | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.TimeProvider.Testing | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.CrashDump | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.HangDump | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.TrxReport | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | MySqlConnector | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | NCrontab | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | NLog.Extensions.Logging | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | NSwag.AspNetCore | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | NUnit | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | NUnit.Analyzers | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | NUnit3TestAdapter | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Npgsql | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Npgsql.DependencyInjection | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.Console | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.OpenTelemetryProtocol | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.AspNetCore | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.Http | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.Runtime | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Oracle.ManagedDataAccess.Core | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | PolySharp | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | PublicApiGenerator | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Serilog | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Serilog.Extensions.Hosting | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Serilog.Extensions.Logging | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Serilog.Sinks.Console | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Spectre.Console | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | System.Data.SQLite.Core | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Testcontainers.FirebirdSql | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Testcontainers.MsSql | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Testcontainers.MySql | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Testcontainers.Oracle | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Testcontainers.PostgreSql | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Testcontainers.Redis | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Verify.NUnit | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | WolverineFx | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | WolverineFx.Postgresql | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | WolverineFx.SqlServer | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | WolverineFx.RuntimeCompilation | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.SignalR.Client | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Binder | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.HealthChecks | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting.Abstractions | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Console | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options.ConfigurationExtensions | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Extensions.Hosting | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | StackExchange.Redis | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | TimeZoneConverter | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Weasel.Core | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Weasel.Firebird | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Weasel.MySql | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Weasel.Oracle | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Weasel.Postgresql | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Weasel.Sqlite | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Weasel.SqlServer | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Hangfire.Core | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Hangfire.InMemory | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Hangfire.PostgreSql | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Sqlite | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | Npgsql.EntityFrameworkCore.PostgreSQL | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | TickerQ | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| PackageVersion | TickerQ.EntityFrameworkCore | [Directory.Packages.props](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/Directory.Packages.props) |
| ProjectReference | ../Quartz.Analyzers/Quartz.Analyzers.csproj | [src/Quartz/Quartz.csproj](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz/Quartz.csproj) |
| PackageReference | Microsoft.Extensions.DependencyInjection | [src/Quartz/Quartz.csproj](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz/Quartz.csproj) |
| PackageReference | Microsoft.Extensions.Diagnostics.HealthChecks | [src/Quartz/Quartz.csproj](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz/Quartz.csproj) |
| PackageReference | Microsoft.Extensions.Hosting.Abstractions | [src/Quartz/Quartz.csproj](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz/Quartz.csproj) |
| PackageReference | Microsoft.Extensions.Logging.Abstractions | [src/Quartz/Quartz.csproj](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz/Quartz.csproj) |
| PackageReference | Microsoft.Extensions.Options.ConfigurationExtensions | [src/Quartz/Quartz.csproj](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/src/Quartz/Quartz.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `Apache-2.0`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [license.txt](evidence/notices/license.txt) | [license.txt](https://github.com/quartznet/quartznet/blob/a94922ad3b1c2efa6d2613916fa2f386aede6681/license.txt) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-scheduler-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
