# DJ-013 .j Aspire: dependencies and licenses

## Proposed Java dependencies

extensions,web,containers

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: ProcessBuilder, HTTP clients and container-engine protocols; external orchestrator binaries are tool dependencies.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Azure.AI.AgentServer.AgentFramework | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.AI.Inference | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.AI.OpenAI | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.AI.Projects | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.AI.Projects.Agents | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.AI.Extensions.OpenAI | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Data.Tables | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Extensions.AspNetCore.Configuration.Secrets | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Messaging.EventHubs | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Messaging.EventHubs.Processor | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Messaging.ServiceBus | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Search.Documents | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Messaging.WebPubSub | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Security.KeyVault.Secrets | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Security.KeyVault.Certificates | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Security.KeyVault.Keys | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Storage.Blobs | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Storage.Files.DataLake | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Storage.Files.Shares | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Storage.Queues | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Cosmos | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Kusto.Data | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Kusto.Ingest | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.SignalR | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.SignalR.Management | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.StackExchangeRedis | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Azure | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.AzureAppConfiguration | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.AppConfiguration | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.AppContainers | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.AppService | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.ApplicationInsights | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.Cdn | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.ContainerRegistry | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.ContainerService | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.CognitiveServices | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.CosmosDB | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.EventHubs | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.KeyVault | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.Kusto | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.Network | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.OperationalInsights | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.PostgreSql | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.PrivateDns | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.Redis | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.RedisEnterprise | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.Search | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.ServiceBus | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.SignalR | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.Sql | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.Storage | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Provisioning.WebPubSub | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.ResourceManager.Authorization | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.ResourceManager.KeyVault | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.ResourceManager.Resources.Deployments | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.ApplicationStatus | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.Azure.Data.Tables | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.Azure.KeyVault.Secrets | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.Azure.Messaging.EventHubs | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.Azure.Storage.Blobs | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.Azure.Storage.Queues | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.AzureServiceBus | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.CosmosDb | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.Kafka | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.MongoDb | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.MySql | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.NpgSql | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.Oracle | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.Rabbitmq | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.Redis | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.SqlServer | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | AspNetCore.HealthChecks.Uris | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Utilities.Core | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.IO.Redist | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Build | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Framework | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Locator | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | NuGet.Commands | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | NuGet.ProjectModel | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | NuGet.Protocol | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | NuGet.Resolver | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Confluent.Kafka | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Dapper | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Dapper.AOT | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Deque.AxeCore.Playwright | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | DnsClient | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Google.Protobuf | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Grpc.AspNetCore | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Grpc.Net.ClientFactory | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Grpc.Tools | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Hex1b | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Hex1b.McpServer | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Hex1b.Tool | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Humanizer.Core | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | KubernetesClient | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Markdig | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | MessagePack | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.AI.Foundry.Local | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Agents.AI.OpenAI | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.SqlClient | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.SqlClient.Extensions.Azure | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.Sqlite.Core | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.FluentUI.AspNetCore.Components | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.FluentUI.AspNetCore.Components.Icons | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Milvus.Client | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | ModelContextProtocol | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | MongoDB.Driver | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | MongoDB.Driver.Core.Extensions.DiagnosticSources | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | MySqlConnector.DependencyInjection | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | MySqlConnector.Logging.Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | NATS.Net | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | NCrontab.Signed | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Npgsql.DependencyInjection | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | OpenAI | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Oracle.ManagedDataAccess.OpenTelemetry | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Polly.Core | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Polly.Extensions | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Pomelo.EntityFrameworkCore.MySql | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Qdrant.Client | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | RabbitMQ.Client | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | SQLitePCLRaw.bundle_e_sqlite3 | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Spectre.Console | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | StackExchange.Redis | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | System.IO.Hashing | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Yarp.ReverseProxy | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | YamlDotNet | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | StreamJsonRpc | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Semver | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Sigstore | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Tuf | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.DevTunnels.Connections | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Monitor.OpenTelemetry.Exporter | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Npgsql.OpenTelemetry | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.Console | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.InMemory | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.OpenTelemetryProtocol | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Extensions.Hosting | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.AspNetCore | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.GrpcNetClient | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.Http | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.Runtime | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.SqlClient | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | MicroBuild.Plugins.SwixBuild.Dotnet | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.MSBuild | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Signed.Wix | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Build.Tasks.Archives | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.GenAPI.Task | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.TemplateEngine.Edge | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.TemplateEngine.Orchestrator.RunnableProjects | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | System.CommandLine | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | xunit.v3.assert | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Orleans.Clustering.AzureStorage | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Orleans.Persistence.AzureStorage | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Orleans.Client | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Orleans.Server | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Orleans.Sdk | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.AppConfiguration.AspNetCore | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Extensions.Http.AspNetCore | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Extensions.Storage.Blobs | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Extensions.Storage.Queues | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Extensions.ServiceBus | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Extensions.EventHubs | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Extensions.CosmosDb | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.OpenTelemetry | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Sdk | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.ApplicationInsights.WorkerService | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Extensions.DurableTask | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Extensions.DurableTask.AzureManaged | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Identity.Web | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Core | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Azure.Identity | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.AI | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.AI.OpenAI | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.AI.AzureAIInference | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.AutoActivation | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.Testing | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http.Resilience | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.ServiceDiscovery | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.ServiceDiscovery.Yarp | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.TimeProvider.Testing | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.Memory | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting.Abstractions | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Abstractions | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Binder | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.EnvironmentVariables | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Caching.Memory | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileSystemGlobbing | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Primitives | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | System.Formats.Asn1 | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.Cryptography | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Cosmos | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Design | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.SqlServer | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Tools | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | MongoDB.EntityFrameworkCore | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Npgsql.EntityFrameworkCore.PostgreSQL | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Oracle.EntityFrameworkCore | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Authentication.Certificate | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Authentication.JwtBearer | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Authentication.OpenIdConnect | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.OpenApi | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.OutputCaching.StackExchangeRedis | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.TestHost | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Caching.StackExchangeRedis | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.HealthChecks.EntityFrameworkCore | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.HealthChecks | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Features | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileProviders.Embedded | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.SignalR.Client | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | NuGet.Configuration | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | NuGet.Credentials | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageVersion | NuGet.Versioning | [Directory.Packages.props](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/Directory.Packages.props) |
| PackageReference | Microsoft.Extensions.ServiceDiscovery.Yarp | [playground/TestShop/ApiGateway/ApiGateway.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/playground/TestShop/ApiGateway/ApiGateway.csproj) |
| ProjectReference | ..\TestShop.ServiceDefaults\TestShop.ServiceDefaults.csproj | [playground/TestShop/ApiGateway/ApiGateway.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/playground/TestShop/ApiGateway/ApiGateway.csproj) |
| ProjectReference | ..\..\Playground.ServiceDefaults\Playground.ServiceDefaults.csproj | [playground/AksDemo/AksDemo.ApiService/AksDemo.ApiService.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/playground/AksDemo/AksDemo.ApiService/AksDemo.ApiService.csproj) |
| ProjectReference | ..\AksDemo.ApiService\AksDemo.ApiService.csproj | [playground/AksDemo/AksDemo.AppHost/AksDemo.AppHost.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/playground/AksDemo/AksDemo.AppHost/AksDemo.AppHost.csproj) |
| PackageReference | Azure.AI.Extensions.OpenAI | [src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj) |
| PackageReference | Microsoft.Extensions.Azure | [src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj) |
| PackageReference | Microsoft.Extensions.Configuration.Binder | [src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj) |
| PackageReference | Microsoft.Extensions.Diagnostics.HealthChecks | [src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj) |
| PackageReference | Microsoft.Extensions.Hosting.Abstractions | [src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj) |
| PackageReference | OpenTelemetry.Extensions.Hosting | [src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj) |
| ProjectReference | ..\Aspire.OpenAI\Aspire.OpenAI.csproj | [src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/src/Components/Aspire.Azure.AI.Extensions.OpenAI/Aspire.Azure.AI.Extensions.OpenAI.csproj) |
| PackageReference | xunit.v3.assert | [playground/Testing/Testing.Tests/Testing.Tests.csproj](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/playground/Testing/Testing.Tests/Testing.Tests.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.TXT](evidence/notices/LICENSE.TXT) | [LICENSE.TXT](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/LICENSE.TXT) |
| [THIRD-PARTY-NOTICES.TXT](evidence/notices/THIRD-PARTY-NOTICES.TXT) | [THIRD-PARTY-NOTICES.TXT](https://github.com/microsoft/aspire/blob/118781118dddea1f7a524ab3d244fa4cee3c62cf/THIRD-PARTY-NOTICES.TXT) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-aspire-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
