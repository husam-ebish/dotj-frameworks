# DJ-066 .j Bus: dependencies and licenses

## Proposed Java dependencies

core,json,resilience;postgresql(optional);scheduler(optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Sockets/HTTP, own serializers/storage and optional protocol-specific native bindings only if justified.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Apache.NMS.ActiveMQ | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Apache.NMS.AMQP | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | AWSSDK.DynamoDBv2 | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | AWSSDK.SimpleNotificationService | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | AWSSDK.S3 | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | AWSSDK.SQS | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Azure.Data.Tables | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Azure.Identity | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Azure.Messaging.EventHubs.Processor | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Azure.Messaging.ServiceBus | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Azure.Storage.Blobs | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Confluent.Kafka | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Confluent.SchemaRegistry.Serdes.Avro | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | coverlet.collector | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Dapper | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | dapper.contrib | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | EntityFramework | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Google.Protobuf | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Hangfire.AspNetCore | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Hangfire.Core | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Hangfire.MemoryStorage | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Iesi.Collections | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Ionic.Zlib.Core | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Marten | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | MathNet.Numerics | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | MediatR | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | MessagePack | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.ApplicationInsights.AspNetCore | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.SignalR.Core | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.SignalR.Protocols.MessagePack | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Cosmos | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.WebJobs.Extensions.EventHubs | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.WebJobs.Extensions.ServiceBus | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.SqlClient | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Design | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Design | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Relational | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Relational | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.SqlServer | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.SqlServer | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Caching.Memory | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Caching.Memory | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.HealthChecks | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.HealthChecks | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.HealthChecks | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.Testing | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting.Abstractions | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting.Abstractions | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting.Abstractions | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | MongoDB.Driver | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json.Bson | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | NHibernate | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Npgsql | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Npgsql.EntityFrameworkCore.PostgreSQL | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | NUnit | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | NUnit.Analyzers | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | NUnit3TestAdapter | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.Console | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.OpenTelemetryProtocol | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Extensions.Hosting | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Quartz | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | Quartz.Extensions.Hosting | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | QuikGraph | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | QuikGraph.Graphviz | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | RabbitMQ.Client | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | SharpZipLib | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | StackExchange.Redis | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Data.SqlClient | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Data.SQLite | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.DiagnosticSource | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.DiagnosticSource | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.DiagnosticSource | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Memory | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Net.Http | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Reflection.Emit | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Reflection.Emit.Lightweight | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Threading.Channels | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Threading.Channels | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Threading.Channels | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.Threading.Tasks.Extensions | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageVersion | System.ValueTuple | [Directory.Packages.props](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/Directory.Packages.props) |
| PackageReference | Microsoft.Bcl.AsyncInterfaces | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | System.Threading.Tasks.Extensions | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | System.Memory | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | System.Net.Http | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | Microsoft.Bcl.AsyncInterfaces | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | System.Reflection.Emit.Lightweight | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | System.Reflection.Emit | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | System.Threading.Tasks.Extensions | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | System.Memory | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | Microsoft.Extensions.Diagnostics.HealthChecks | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | Microsoft.Extensions.DependencyInjection.Abstractions | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | Microsoft.Extensions.Hosting.Abstractions | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | Microsoft.Extensions.Logging.Abstractions | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | Microsoft.Extensions.Options | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | System.Diagnostics.DiagnosticSource | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | System.Text.Json | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| PackageReference | System.Threading.Channels | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |
| ProjectReference | ..\MassTransit.Abstractions\MassTransit.Abstractions.csproj | [src/MassTransit/MassTransit.csproj](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/src/MassTransit/MassTransit.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

The inspected revision contains Apache license text. This observation is specific to the pin and does not establish the terms of every MassTransit release or product.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/LICENSE) |
| [NOTICE](evidence/notices/NOTICE) | [NOTICE](https://github.com/MassTransit/MassTransit/blob/d9f61f764c802785cc9a4be92547d8f5b63018d4/NOTICE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-bus-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
