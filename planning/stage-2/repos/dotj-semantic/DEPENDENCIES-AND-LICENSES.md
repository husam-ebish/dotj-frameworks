# DJ-061 .j Semantic: dependencies and licenses

## Proposed Java dependencies

json,rest,extensions

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: JDK HTTP client, own JSON, reflection and async contracts.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Aspire.Azure.AI.OpenAI | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Aspire.Azure.Search.Documents | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.AppHost | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.Azure.CognitiveServices | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.NodeJs | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | CommunityToolkit.Aspire.Hosting.Dapr | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | CommunityToolkit.Aspire.Hosting.NodeJS.Extensions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.Azure.Search | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | MessagePack | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | AWSSDK.BedrockAgent | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | AWSSDK.BedrockAgentRuntime | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | AWSSDK.BedrockRuntime | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | AWSSDK.Core | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | AWS.Bedrock.MEAI | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | AWSSDK.Extensions.NETCore.Setup | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | AWSSDK.SecurityToken | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Azure.AI.Agents.Persistent | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Azure.AI.ContentSafety | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Azure.AI.OpenAI | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Azure.AI.Projects | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Azure.Identity | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Azure.Monitor.OpenTelemetry.Exporter | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Community.OData.Linq | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Dapr.Actors | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Dapr.Actors.AspNetCore | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Dapr.AspNetCore | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | EntityFramework | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | FastBertTokenizer | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Google.Apis.Auth | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Google.Apis.CustomSearchAPI.v1 | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Google.GenAI | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Google.Protobuf | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Grpc.AspNetCore | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Grpc.AspNetCore.Server | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Grpc.AspNetCore.Server.Reflection | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Grpc.AspNetCore.Web | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Grpc.Net.Client | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Grpc.Tools | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Handlebars.Net.Helpers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Handlebars.Net | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | HtmlAgilityPack | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | JmesPath.Net | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | JsonSchema.Net | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | JsonSchema.Net.Generation | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Markdig | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Agents.AI.Abstractions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Agents.AI.Foundry | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Agents.AI.OpenAI | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Agents.AI.Workflows | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Agents.CopilotStudio.Client | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.Testing | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.OData | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.OpenApi | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.SignalR.Client | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Extensions.Http | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Extensions.Http.AspNetCore | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.Extensions.Storage.Queues | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Functions.Worker.SDK | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Kusto.Data | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.WebJobs.Extensions.OpenApi | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.WebJobs.Extensions.Storage | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.HashCode | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.Memory | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.Numerics | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Common | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Identity.Client | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Identity.Client.Extensions.Msal | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityModel.JsonWebTokens | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Kiota.Abstractions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Kiota.Authentication.Azure | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Kiota.Http.HttpClientLibrary | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Kiota.Serialization.Json | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.OnnxRuntime | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.OnnxRuntime.Gpu | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.Tokenizers.Data.Cl100kBase | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.SemanticKernel.Abstractions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.SemanticKernel.Connectors.OpenAI | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.SemanticKernel.Core | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.SemanticKernel.Planners.OpenAI | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Threading | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | ModelContextProtocol | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | MSTest.TestFramework | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Npgsql | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OData2Linq | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OllamaSharp | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OpenAI | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OpenTelemetry | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Api | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Api.ProviderBuilderExtensions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.Console | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.OpenTelemetryProtocol | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Extensions.Hosting | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.AspNetCore | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.Http | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.Runtime | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | PdfPig | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Prompty.Core | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | PuppeteerSharp | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.DiagnosticSource | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.IdentityModel.Tokens.Jwt | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.IO.Packaging | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.Linq.AsyncEnumerable | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.Memory.Data | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.Net.Http | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.Numerics.Tensors | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.ValueTuple | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.Threading.Tasks.Extensions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | A2A | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | A2A.AspNetCore | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.CommandLine | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.Tokenizers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.AI | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.AI.Abstractions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.AI.AzureAIInference | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.AI.OpenAI | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Abstractions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Binder | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.EnvironmentVariables | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.FileExtensions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Json | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.UserSecrets | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Diagnostics.Testing | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http.Resilience | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.ServiceDiscovery | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Console | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Debug | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options.DataAnnotations | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options.ConfigurationExtensions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.TimeProvider | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.TimeProvider.Testing | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileProviders.Physical | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileProviders.Embedded | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.VectorData.Abstractions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Moq | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | FluentAssertions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.Text.RegularExpressions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.Threading.Channels | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | System.Threading.Tasks.Dataflow | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | xunit | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | xunit.abstractions | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | xretry | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | coverlet.collector | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Docker.DotNet | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Grpc.Net.ClientFactory | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Humanizer | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | DocumentFormat.OpenXml | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | DuckDB.NET.Data.Full | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | DuckDB.NET.Data | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Graph | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Graph.Core | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.OpenApi | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.OpenApi.Readers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.OpenApi.ApiManifest | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Plugins.Manifest | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | protobuf-net | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | protobuf-net.Reflection | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | YamlDotNet | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Fluid.Core | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Milvus.Client | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Testcontainers.Milvus | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Testcontainers.MongoDB | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | CommunityToolkit.VectorData.AzureAISearch | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | CommunityToolkit.VectorData.AzureDocumentDB | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | CommunityToolkit.VectorData.AzureCosmosDB | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | CommunityToolkit.VectorData.InMemory | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | CommunityToolkit.VectorData.PgVector | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | CommunityToolkit.VectorData.Qdrant | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | CommunityToolkit.VectorData.Redis | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | CommunityToolkit.VectorData.Weaviate | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.SourceLink.GitHub | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.Net.Compilers.Toolset | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.NetAnalyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageReference | Microsoft.CodeAnalysis.NetAnalyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Threading.Analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageReference | Microsoft.VisualStudio.Threading.Analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | xunit.analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageReference | xunit.analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Moq.Analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageReference | Moq.Analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Roslynator.Analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageReference | Roslynator.Analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Roslynator.CodeAnalysis.Analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageReference | Roslynator.CodeAnalysis.Analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Roslynator.Formatting.Analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageReference | Roslynator.Formatting.Analyzers | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.OnnxRuntimeGenAI | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.OnnxRuntimeGenAI.Cuda | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.OnnxRuntimeGenAI.DirectML | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Spectre.Console | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Spectre.Console.Cli | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | Spectre.Console.Json | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | NAudio | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| PackageVersion | WebRtcVadSharp | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-semantic-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
