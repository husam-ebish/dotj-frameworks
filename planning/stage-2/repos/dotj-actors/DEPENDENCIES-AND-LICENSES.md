# DJ-015 .j Actors: dependencies and licenses

## Proposed Java dependencies

core,json,extensions

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Executors, sockets, timers and own serializers; no Akka substitute.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Aspire.Azure.Data.Tables | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Aspire.Azure.Storage.Blobs | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Aspire.Azure.Storage.Queues | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.AppHost | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.Orleans | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.Redis | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Aspire.StackExchange.Redis | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Autofac.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | AwesomeAssertions | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | AWSSDK.DynamoDBv2 | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | AWSSDK.Kinesis | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | AWSSDK.S3 | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | AWSSDK.SQS | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Azure.Core | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Azure.Data.Tables | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Azure.Identity | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Azure.Messaging.EventHubs | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Azure.Security.KeyVault.Secrets | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Azure.Storage.Blobs | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Azure.Storage.Queues | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet.Diagnostics.Windows | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | CassandraCSharpDriver | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Consul | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | CsCheck | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | FSharp.Core | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Google.Cloud.Firestore | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Google.Cloud.PubSub.V1 | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Google.Cloud.Storage.V1 | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Google.Protobuf | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Grpc.Tools | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Hyperion | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | KubernetesClient | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | MessagePack | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.StringTools | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Accordant | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Cosmos | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Build | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.BannedApiAnalyzers | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Common | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Features | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.Common | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Crank.EventSources | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.CSharp | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.SqlClient | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.Sqlite | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.GenAPI.Task | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.PlatformAbstractions | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Abstractions | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.AzureKeyVault | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Binder | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Json | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyModel | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.Testing | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting.Abstractions | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http.Resilience | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Console | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Debug | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.ObjectPool | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options.ConfigurationExtensions | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.ServiceDiscovery | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.TimeProvider.Testing | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.NETFramework.ReferenceAssemblies | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.SourceLink.AzureRepos.Git | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.SourceLink.GitHub | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.CrashDump | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.HangDump | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.TrxReport | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Platform | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Platform.MSBuild | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | MySql.Data | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | NATS.Net | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | NodaTime | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Npgsql | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | NSubstitute.Analyzers.CSharp | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | NSubstitute | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | OpenTelemetry | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.OpenTelemetryProtocol | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Extensions.Hosting | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.AspNetCore | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.Http | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.Runtime | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Polly | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Polly.Extensions | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | protobuf-net | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | SSH.NET | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | SpanJson | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | SQLitePCLRaw.bundle_e_sqlite3 | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | StackExchange.Redis | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | StructureMap.Microsoft.DependencyInjection | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | System.CodeDom | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | System.Collections.Immutable | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | System.CommandLine | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.PerformanceCounter | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | System.Drawing.Common | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | System.IO.Hashing | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | System.IO.Pipelines | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | System.Memory.Data | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | System.Reactive | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Testcontainers | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Testcontainers.Consul | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Utf8Json | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Verify.XunitV3 | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | xunit.v3.assert | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | xunit.v3.core.mtp-v2 | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | xunit.v3.extensibility.core | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | xunit.v3.mtp-v2 | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | ZeroFormatter | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | ZooKeeperNetEx | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.Azure.EventHubs | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.Azure.Storage | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.Testing | [Directory.Packages.props](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/Directory.Packages.props) |
| PackageReference | Microsoft.Orleans.Dashboard | [docs/site/src/content/docs/dashboard/snippets/secure-dashboard/SecureDashboard.csproj](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/docs/site/src/content/docs/dashboard/snippets/secure-dashboard/SecureDashboard.csproj) |
| PackageReference | Microsoft.Orleans.Server | [docs/site/src/content/docs/dashboard/snippets/secure-dashboard/SecureDashboard.csproj](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/docs/site/src/content/docs/dashboard/snippets/secure-dashboard/SecureDashboard.csproj) |
| PackageReference | Azure.Identity | [docs/site/src/content/docs/deployment/snippets/service-fabric/ServiceFabricSilo/ServiceFabricSilo.csproj](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/docs/site/src/content/docs/deployment/snippets/service-fabric/ServiceFabricSilo/ServiceFabricSilo.csproj) |
| PackageReference | Microsoft.Orleans.Clustering.AzureStorage | [docs/site/src/content/docs/deployment/snippets/service-fabric/ServiceFabricSilo/ServiceFabricSilo.csproj](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/docs/site/src/content/docs/deployment/snippets/service-fabric/ServiceFabricSilo/ServiceFabricSilo.csproj) |
| PackageReference | Microsoft.Orleans.Server | [docs/site/src/content/docs/deployment/snippets/service-fabric/ServiceFabricSilo/ServiceFabricSilo.csproj](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/docs/site/src/content/docs/deployment/snippets/service-fabric/ServiceFabricSilo/ServiceFabricSilo.csproj) |
| PackageReference | Microsoft.ServiceFabric.Services | [docs/site/src/content/docs/deployment/snippets/service-fabric/ServiceFabricSilo/ServiceFabricSilo.csproj](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/docs/site/src/content/docs/deployment/snippets/service-fabric/ServiceFabricSilo/ServiceFabricSilo.csproj) |
| PackageReference | Microsoft.Orleans.TestingHost | [docs/site/src/content/docs/grains/snippets/testing/orleans-testing/Sample.OrleansTesting.MSTest/Sample.OrleansTesting.MSTest.csproj](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/docs/site/src/content/docs/grains/snippets/testing/orleans-testing/Sample.OrleansTesting.MSTest/Sample.OrleansTesting.MSTest.csproj) |
| PackageReference | MSTest.TestAdapter | [docs/site/src/content/docs/grains/snippets/testing/orleans-testing/Sample.OrleansTesting.MSTest/Sample.OrleansTesting.MSTest.csproj](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/docs/site/src/content/docs/grains/snippets/testing/orleans-testing/Sample.OrleansTesting.MSTest/Sample.OrleansTesting.MSTest.csproj) |
| PackageReference | MSTest.TestFramework | [docs/site/src/content/docs/grains/snippets/testing/orleans-testing/Sample.OrleansTesting.MSTest/Sample.OrleansTesting.MSTest.csproj](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/docs/site/src/content/docs/grains/snippets/testing/orleans-testing/Sample.OrleansTesting.MSTest/Sample.OrleansTesting.MSTest.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/dotnet/orleans/blob/9f8310cb6e5bbe35cd3bbb0752052993578eb083/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-actors-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
