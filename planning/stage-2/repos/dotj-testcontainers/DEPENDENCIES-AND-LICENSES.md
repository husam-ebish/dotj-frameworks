# DJ-056 .j Testcontainers: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: HTTP/Unix-domain sockets, ProcessBuilder fallback and Docker-compatible engine API.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | BouncyCastle.Cryptography | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Docker.DotNet.Enhanced.X509 | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Docker.DotNet.Enhanced | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.HashCode | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | SharpZipLib | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | SSH.NET | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Cake.Frosting.Git | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Cake.Frosting | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Cake.Sonar | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.Testing | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | coverlet.collector | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Dapper | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | ReflectionMagic | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | xunit.analyzers | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | xunit | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | xunit.v3 | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | xunit.extensibility.execution | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | xunit.v3.extensibility.core | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Apache.NMS.ActiveMQ | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | ArangoDBNetStandard | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | AWSSDK.CloudWatchLogs | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | AWSSDK.DynamoDBv2 | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | AWSSDK.S3 | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | AWSSDK.SimpleNotificationService | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | AWSSDK.SQS | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Azure.Data.Tables | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Azure.Identity | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Azure.Messaging.EventHubs | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Azure.Messaging.ServiceBus | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Azure.Security.KeyVault.Certificates | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Azure.Security.KeyVault.Secrets | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Azure.Storage.Blobs | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Azure.Storage.Queues | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | CassandraCSharpDriver | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | ClickHouse.Client | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Confluent.Kafka | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Confluent.SchemaRegistry.Serdes.Json | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Confluent.SchemaRegistry | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Consul | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | CouchbaseNetClient | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | DotPulsar | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Elastic.Clients.Elasticsearch | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | EventStore.Client.Grpc.Streams | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | FirebirdSql.Data.FirebirdClient | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Google.Cloud.BigQuery.V2 | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Google.Cloud.Bigtable.Admin.V2 | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Google.Cloud.Firestore | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Google.Cloud.PubSub.V1 | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Google.Cloud.Storage.V1 | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | InfluxDB.Client | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | JanusGraph.Net | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Keycloak.Net.Core | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | KubernetesClient | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | KurrentDB.Client | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | MailKitLite | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Cosmos | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Kusto.Data | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.SqlClient | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Microsoft.Playwright | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Milvus.Client | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | MongoDB.Driver | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | MQTTnet | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | MyCouch | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | MySqlConnector | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | NATS.Client | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Neo4j.Driver | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | net-questdb-client | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Net.IBM.Data.Db2-lnx | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Net.IBM.Data.Db2-osx | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Net.IBM.Data.Db2 | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Npgsql | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | OllamaSharp | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | OpenSearch.Client | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.OpenTelemetryProtocol | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Oracle.ManagedDataAccess.Core | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Qdrant.Client | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | RabbitMQ.Client | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | RavenDB.Client | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Selenium.WebDriver | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Seq.Api | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Seq.Extensions.Logging | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | StackExchange.Redis | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | Temporalio | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageVersion | ToxiproxyNetCore | [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props) |
| PackageReference | Cake.Frosting.Git | [build/Build.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/build/Build.csproj) |
| PackageReference | Cake.Frosting | [build/Build.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/build/Build.csproj) |
| PackageReference | Cake.Sonar | [build/Build.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/build/Build.csproj) |
| PackageReference | JetBrains.Annotations | [src/Testcontainers.ActiveMq/Testcontainers.ActiveMq.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers.ActiveMq/Testcontainers.ActiveMq.csproj) |
| ProjectReference | ../Testcontainers/Testcontainers.csproj | [src/Testcontainers.ActiveMq/Testcontainers.ActiveMq.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers.ActiveMq/Testcontainers.ActiveMq.csproj) |
| PackageReference | JetBrains.Annotations | [src/Testcontainers/Testcontainers.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Testcontainers.csproj) |
| PackageReference | Docker.DotNet.Enhanced.X509 | [src/Testcontainers/Testcontainers.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Testcontainers.csproj) |
| PackageReference | Docker.DotNet.Enhanced | [src/Testcontainers/Testcontainers.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Testcontainers.csproj) |
| PackageReference | Microsoft.Extensions.Logging.Abstractions | [src/Testcontainers/Testcontainers.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Testcontainers.csproj) |
| PackageReference | SharpZipLib | [src/Testcontainers/Testcontainers.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Testcontainers.csproj) |
| PackageReference | SSH.NET | [src/Testcontainers/Testcontainers.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Testcontainers.csproj) |
| PackageReference | BouncyCastle.Cryptography | [src/Testcontainers/Testcontainers.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Testcontainers.csproj) |
| PackageReference | Microsoft.Bcl.AsyncInterfaces | [src/Testcontainers/Testcontainers.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Testcontainers.csproj) |
| PackageReference | Microsoft.Bcl.HashCode | [src/Testcontainers/Testcontainers.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Testcontainers.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-testcontainers-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
