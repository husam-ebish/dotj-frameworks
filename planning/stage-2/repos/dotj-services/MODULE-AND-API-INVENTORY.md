# DJ-018 .j Services: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 2264 | recursive complete |
| Project-definition paths | 35 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 655 | Lexical path classification, not runnable test count |
| Sampled text files | 11 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 22 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 6 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [src/Common/UnitTests.Common/UnitTests.Common.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/Common/UnitTests.Common/UnitTests.Common.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn3.11.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn3.11.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn4.0.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn4.0.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.BuildTools/tests/CoreWCF.BuildTools.Roslyn3.11.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/tests/CoreWCF.BuildTools.Roslyn3.11.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.BuildTools/tests/CoreWCF.BuildTools.Roslyn4.0.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/tests/CoreWCF.BuildTools.Roslyn4.0.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.ConfigurationManager/src/CoreWCF.ConfigurationManager.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.ConfigurationManager/src/CoreWCF.ConfigurationManager.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.ConfigurationManager/tests/CoreWCF.ConfigurationManager.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.ConfigurationManager/tests/CoreWCF.ConfigurationManager.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Http/src/CoreWCF.Http.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Http/src/CoreWCF.Http.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Http/tests/CoreWCF.Http.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Http/tests/CoreWCF.Http.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Kafka.Client/src/CoreWCF.Kafka.Client.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Kafka.Client/src/CoreWCF.Kafka.Client.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Kafka/src/CoreWCF.Kafka.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Kafka/src/CoreWCF.Kafka.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Kafka/tests/CoreWCF.Kafka.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Kafka/tests/CoreWCF.Kafka.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.MSMQ/src/CoreWCF.MSMQ.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.MSMQ/src/CoreWCF.MSMQ.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.MSMQ/tests/CoreWCF.MSMQ.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.MSMQ/tests/CoreWCF.MSMQ.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Metadata/tests/CoreWCF.Metadata.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Metadata/tests/CoreWCF.Metadata.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.NetFramingBase/src/CoreWCF.NetFramingBase.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.NetFramingBase/src/CoreWCF.NetFramingBase.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.NetNamedPipe/src/CoreWCF.NetNamedPipe.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.NetNamedPipe/src/CoreWCF.NetNamedPipe.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.NetNamedPipe/tests/CoreWCF.NetNamedPipe.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.NetNamedPipe/tests/CoreWCF.NetNamedPipe.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.NetTcp/src/CoreWCF.NetTcp.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.NetTcp/src/CoreWCF.NetTcp.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.NetTcp/tests/CoreWCF.NetTcp.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.NetTcp/tests/CoreWCF.NetTcp.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Primitives/src/CoreWCF.Primitives.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Primitives/src/CoreWCF.Primitives.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Primitives/tests/CoreWCF.Primitives.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Primitives/tests/CoreWCF.Primitives.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Queue/src/CoreWCF.Queue.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Queue/src/CoreWCF.Queue.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Queue/tests/CoreWCF.Queue.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Queue/tests/CoreWCF.Queue.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.RabbitMQ.Client/src/CoreWCF.RabbitMQ.Client.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.RabbitMQ.Client/src/CoreWCF.RabbitMQ.Client.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.RabbitMQ/src/CoreWCF.RabbitMQ.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.RabbitMQ/src/CoreWCF.RabbitMQ.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.RabbitMQ/tests/CoreWCF.RabbitMQ.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.RabbitMQ/tests/CoreWCF.RabbitMQ.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Templates/src/CoreWCF.Templates.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Templates/src/CoreWCF.Templates.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Templates/src/templates/CoreWCFService/CoreWCFService.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Templates/src/templates/CoreWCFService/CoreWCFService.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.Templates/tests/CoreWCF.Templates.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Templates/tests/CoreWCF.Templates.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.UnixDomainSocket/src/CoreWCF.UnixDomainSocket.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.UnixDomainSocket/src/CoreWCF.UnixDomainSocket.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.UnixDomainSocket/tests/CoreWCF.UnixDomainSocket.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.UnixDomainSocket/tests/CoreWCF.UnixDomainSocket.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.WebHttp/src/CoreWCF.WebHttp.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.WebHttp/src/CoreWCF.WebHttp.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/CoreWCF.WebHttp/tests/CoreWCF.WebHttp.Tests.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.WebHttp/tests/CoreWCF.WebHttp.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/SourceWebsite/SourceWebsite.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/SourceWebsite/SourceWebsite.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/CoreWCF.BuildTools/src/Indentor.cs:18](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Indentor.cs#L18) | `public int Level { get; private set; } = 0;` |
| [src/CoreWCF.BuildTools/src/Indentor.cs:19](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Indentor.cs#L19) | `public void Increment()` |
| [src/CoreWCF.BuildTools/src/Indentor.cs:24](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Indentor.cs#L24) | `public void Decrement()` |
| [src/CoreWCF.BuildTools/src/Extensions.cs:13](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Extensions.cs#L13) | `public static bool? IsGeneratedCode(this IMethodSymbol methodSymbol)` |
| [src/CoreWCF.BuildTools/src/Extensions.cs:16](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Extensions.cs#L16) | `public static bool IsMatchingUserProvidedMethod(this IMethodSymbol methodSymbol, IMethodSymbol userProvidedMethodSymbol, INamedTypeSymbol? coreWCFInjectedAttribute, INamedTypeSymbol? fromServicesAttribute)` |
| [src/CoreWCF.BuildTools/src/Extensions.cs:47](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Extensions.cs#L47) | `public static bool IsMatchingParameter(this IParameterSymbol symbol, IParameterSymbol parameterSymbol)` |
| [src/CoreWCF.BuildTools/src/Extensions.cs:53](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Extensions.cs#L53) | `public static AttributeData? GetOneAttributeOf(this ISymbol symbol, params INamedTypeSymbol?[] attributeTypeSymbols)` |
| [src/CoreWCF.BuildTools/src/Extensions.cs:74](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Extensions.cs#L74) | `public static bool HasOneAttributeInheritFrom(this ISymbol symbol, params INamedTypeSymbol?[] attributeTypeSymbols)` |
| [src/CoreWCF.BuildTools/src/Extensions.cs:98](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Extensions.cs#L98) | `public static bool IsPrivate(this ISymbol symbol)` |
| [src/CoreWCF.BuildTools/src/Extensions.cs:111](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Extensions.cs#L111) | `public static bool IsPartial(this INamedTypeSymbol namedTypeSymbol, out INamedTypeSymbol parentType)` |
| [src/CoreWCF.BuildTools/src/Extensions.cs:125](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Extensions.cs#L125) | `public static string ToSafeCSharpString(this TypedConstant typedConstant)` |
| [src/CoreWCF.BuildTools/src/Extensions.cs:139](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Extensions.cs#L139) | `public static string ToMessagePropertyVariableName(this string propertyName)` |
| [src/CoreWCF.Http/tests/ByRefTests.cs:14](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Http/tests/ByRefTests.cs#L14) | `public class ByRefTests` |
| [src/CoreWCF.Http/tests/ByRefTests.cs:18](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Http/tests/ByRefTests.cs#L18) | `public ByRefTests(ITestOutputHelper output)` |
| [src/CoreWCF.Http/tests/ByRefTests.cs:24](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Http/tests/ByRefTests.cs#L24) | `public void ByRefParams()` |
| [src/CoreWCF.Http/tests/ByRefTests.cs:105](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Http/tests/ByRefTests.cs#L105) | `public void ConfigureServices(IServiceCollection services)` |
| [src/CoreWCF.Http/tests/ByRefTests.cs:110](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Http/tests/ByRefTests.cs#L110) | `public void Configure(IApplicationBuilder app)` |
| [src/CoreWCF.WebHttp/tests/SslTests.cs:15](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.WebHttp/tests/SslTests.cs#L15) | `public class SslTests` |
| [src/CoreWCF.WebHttp/tests/SslTests.cs:19](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.WebHttp/tests/SslTests.cs#L19) | `public SslTests(ITestOutputHelper output)` |
| [src/CoreWCF.WebHttp/tests/SslTests.cs:25](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.WebHttp/tests/SslTests.cs#L25) | `public async Task SslWorks()` |
| [src/CoreWCF.WebHttp/tests/SslTests.cs:44](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.WebHttp/tests/SslTests.cs#L44) | `public void ConfigureServices(IServiceCollection services)` |
| [src/CoreWCF.WebHttp/tests/SslTests.cs:49](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.WebHttp/tests/SslTests.cs#L49) | `public void Configure(IApplicationBuilder app)` |

Full lexical records (22) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | Dispatch and operation selection | DispatchTable; OperationInvoker; ServiceInstance |
| WP-02 | Host and transport bindings | ServiceHost; ListenerBinding; RequestChannel |
| WP-03 | Behaviors middleware and metadata | ServiceBehavior; MessageInspector; MetadataExporter |
| WP-04 | Authentication authorization and transactions | CallerIdentity; AuthorizationDecision; TransactionContext |
| WP-05 | Server interoperability and hosting acceptance | ServiceCompatibilityProfile; DotnetClientFixture; LoadScenario |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
