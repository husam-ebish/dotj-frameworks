# DJ-014 .j Proxy: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 1054 | recursive complete |
| Project-definition paths | 36 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 257 | Lexical path classification, not runnable test count |
| Sampled text files | 14 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 28 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 18 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [eng/common/internal/Tools.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/eng/common/internal/Tools.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [eng/yarpapppack/yarpapppack-linux-arm64.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/eng/yarpapppack/yarpapppack-linux-arm64.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [eng/yarpapppack/yarpapppack-linux-x64.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/eng/yarpapppack/yarpapppack-linux-x64.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/BasicYarpSample/BasicYarpSample.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/BasicYarpSample/BasicYarpSample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/KubernetesIngress.Sample/Combined/Yarp.Kubernetes.IngressController.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/KubernetesIngress.Sample/Combined/Yarp.Kubernetes.IngressController.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/KubernetesIngress.Sample/Ingress/Yarp.Kubernetes.Ingress.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/KubernetesIngress.Sample/Ingress/Yarp.Kubernetes.Ingress.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/KubernetesIngress.Sample/Monitor/Yarp.Kubernetes.Monitor.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/KubernetesIngress.Sample/Monitor/Yarp.Kubernetes.Monitor.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/KubernetesIngress.Sample/backend/backend.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/KubernetesIngress.Sample/backend/backend.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/Prometheus/HttpLoadApp/HttpLoadApp.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/Prometheus/HttpLoadApp/HttpLoadApp.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/Prometheus/ReverseProxy.Metrics-Prometheus.Sample/ReverseProxy.Metrics.Prometheus.Sample.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/Prometheus/ReverseProxy.Metrics-Prometheus.Sample/ReverseProxy.Metrics.Prometheus.Sample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ReverseProxy.Auth.Sample/ReverseProxy.Auth.Sample.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/ReverseProxy.Auth.Sample/ReverseProxy.Auth.Sample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ReverseProxy.Code.Sample/ReverseProxy.Code.Sample.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/ReverseProxy.Code.Sample/ReverseProxy.Code.Sample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ReverseProxy.Config.Sample/ReverseProxy.Config.Sample.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/ReverseProxy.Config.Sample/ReverseProxy.Config.Sample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ReverseProxy.ConfigFilter.Sample/ReverseProxy.ConfigFilter.Sample.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/ReverseProxy.ConfigFilter.Sample/ReverseProxy.ConfigFilter.Sample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ReverseProxy.Direct.Sample/ReverseProxy.Direct.Sample.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/ReverseProxy.Direct.Sample/ReverseProxy.Direct.Sample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ReverseProxy.HttpSysDelegation.Sample/ReverseProxy/ReverseProxy.HttpSysDelegation.Sample.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/ReverseProxy.HttpSysDelegation.Sample/ReverseProxy/ReverseProxy.HttpSysDelegation.Sample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ReverseProxy.HttpSysDelegation.Sample/SampleHttpSysServer/SampleHttpSysServer.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/ReverseProxy.HttpSysDelegation.Sample/SampleHttpSysServer/SampleHttpSysServer.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ReverseProxy.LetsEncrypt.Sample/ReverseProxy.LetsEncrypt.Sample.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/ReverseProxy.LetsEncrypt.Sample/ReverseProxy.LetsEncrypt.Sample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ReverseProxy.Metrics.Sample/ReverseProxy.Metrics.Sample.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/ReverseProxy.Metrics.Sample/ReverseProxy.Metrics.Sample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ReverseProxy.Transforms.Sample/ReverseProxy.Transforms.Sample.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/ReverseProxy.Transforms.Sample/ReverseProxy.Transforms.Sample.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/SampleServer/SampleServer.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/samples/SampleServer/SampleServer.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/Application/Yarp.Application.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Yarp.Application.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Kubernetes.Controller/Yarp.Kubernetes.Controller.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Kubernetes.Controller/Yarp.Kubernetes.Controller.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/ReverseProxy/Yarp.ReverseProxy.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/ReverseProxy/Yarp.ReverseProxy.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/TelemetryConsumption/Yarp.Telemetry.Consumption.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/TelemetryConsumption/Yarp.Telemetry.Consumption.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [test/Application.Tests/Yarp.Application.Tests.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/Yarp.Application.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Kubernetes.Tests/Yarp.Kubernetes.Tests.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Kubernetes.Tests/Yarp.Kubernetes.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/ReverseProxy.FunctionalTests/Yarp.ReverseProxy.FunctionalTests.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/ReverseProxy.FunctionalTests/Yarp.ReverseProxy.FunctionalTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/ReverseProxy.Tests/Yarp.ReverseProxy.Tests.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/ReverseProxy.Tests/Yarp.ReverseProxy.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Tests.Common/Yarp.Tests.Common.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Tests.Common/Yarp.Tests.Common.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [testassets/BenchmarkApp/BenchmarkApp.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/testassets/BenchmarkApp/BenchmarkApp.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [testassets/ReverseProxy.Code/ReverseProxy.Code.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/testassets/ReverseProxy.Code/ReverseProxy.Code.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [testassets/ReverseProxy.Config/ReverseProxy.Config.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/testassets/ReverseProxy.Config/ReverseProxy.Config.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [testassets/ReverseProxy.Direct/ReverseProxy.Direct.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/testassets/ReverseProxy.Direct/ReverseProxy.Direct.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [testassets/TestClient/TestClient.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/testassets/TestClient/TestClient.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [testassets/TestServer/TestServer.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/testassets/TestServer/TestServer.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/Application/Program.cs:78](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Program.cs#L78) | `public partial class Program { }` |
| [src/Application/Extensions.cs:18](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Extensions.cs#L18) | `public static class Extensions` |
| [src/Application/Extensions.cs:20](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Extensions.cs#L20) | `public static TBuilder AddServiceDefaults<TBuilder>(this TBuilder builder, YarpAppConfig config) where TBuilder : IHostApplicationBuilder` |
| [src/Application/Extensions.cs:31](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Extensions.cs#L31) | `public static TBuilder ConfigureOpenTelemetry<TBuilder>(this TBuilder builder, YarpAppConfig config) where TBuilder : IHostApplicationBuilder` |
| [src/Application/Extensions.cs:84](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Extensions.cs#L84) | `public static TBuilder AddDefaultHealthChecks<TBuilder>(this TBuilder builder) where TBuilder : IHostApplicationBuilder` |
| [test/Kubernetes.Tests/ReconcilerTests.cs:20](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Kubernetes.Tests/ReconcilerTests.cs#L20) | `public class ReconcilerTests` |
| [test/Kubernetes.Tests/ReconcilerTests.cs:27](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Kubernetes.Tests/ReconcilerTests.cs#L27) | `public ReconcilerTests(ITestOutputHelper output)` |
| [test/Kubernetes.Tests/ReconcilerTests.cs:34](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Kubernetes.Tests/ReconcilerTests.cs#L34) | `public async Task ReconcilerDoesNotStopOnInvalidIngress()` |
| [test/Application.Tests/SpaFallbackTests.cs:18](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L18) | `public void ConfigureConfiguration(Action<IConfigurationBuilder> configure)` |
| [test/Application.Tests/SpaFallbackTests.cs:23](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L23) | `public void Configure(YarpAppConfig config)` |
| [test/Application.Tests/SpaFallbackTests.cs:33](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L33) | `public void Configure(Dictionary<string, string?> config)` |
| [test/Application.Tests/SpaFallbackTests.cs:38](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L38) | `protected override IWebHostBuilder? CreateWebHostBuilder()` |
| [test/Application.Tests/SpaFallbackTests.cs:48](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L48) | `protected override void ConfigureWebHost(IWebHostBuilder builder)` |
| [test/Application.Tests/SpaFallbackTests.cs:54](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L54) | `public class SpaFallbackTests` |
| [test/Application.Tests/SpaFallbackTests.cs:79](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L79) | `public async Task SpaFallback_ReturnsIndexHtml_ForUnknownRoutes()` |
| [test/Application.Tests/SpaFallbackTests.cs:92](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L92) | `public async Task SpaFallback_ReturnsIndexHtml_ForDeepNestedRoutes()` |
| [test/Application.Tests/SpaFallbackTests.cs:105](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L105) | `public async Task SpaFallback_Returns404_ForMissingFileExtensions()` |
| [test/Application.Tests/SpaFallbackTests.cs:119](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L119) | `public async Task SpaFallback_ServesStaticFiles_Directly()` |
| [test/Application.Tests/SpaFallbackTests.cs:132](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L132) | `public async Task SpaFallback_DefaultDocument_ServesIndexHtml_AtRoot()` |
| [test/Application.Tests/SpaFallbackTests.cs:146](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L146) | `public async Task SpaFallback_Disabled_Returns404_ForUnknownRoutes()` |
| [test/Application.Tests/SpaFallbackTests.cs:161](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L161) | `public async Task SpaFallback_Disabled_StillServesStaticFiles()` |
| [test/Application.Tests/SpaFallbackTests.cs:178](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L178) | `public async Task StaticFiles_Disabled_Returns404_ForAll()` |
| [test/Application.Tests/SpaFallbackTests.cs:193](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L193) | `public async Task SpaFallback_CoexistsWithSpecificYarpRoutes()` |
| [test/Application.Tests/SpaFallbackTests.cs:218](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L218) | `public async Task SpaFallback_CatchAllYarpRoute_WinsOverFallback()` |
| [test/Application.Tests/SpaFallbackTests.cs:240](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L240) | `public async Task ObjectModel_StaticFilesAndFallback()` |
| [test/Application.Tests/SpaFallbackTests.cs:259](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L259) | `public async Task ObjectModel_StaticFilesWithoutFallback()` |
| [test/Application.Tests/SpaFallbackTests.cs:275](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L275) | `public async Task ObjectModel_CustomFallbackPath()` |
| [test/Application.Tests/SpaFallbackTests.cs:291](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L291) | `public async Task ObjectModel_EverythingDisabled()` |

Full lexical records (28) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | Route and cluster configuration | ProxyRoute; ClusterSnapshot; DestinationState |
| WP-02 | Streaming forwarding and transforms | ForwardingContext; HeaderTransform; DuplexTunnel |
| WP-03 | Balancing affinity and health | LoadBalancingPolicy; AffinityToken; HealthReport |
| WP-04 | Retry timeout and security boundaries | ForwardAttempt; RetryDecision; TimeoutBudget |
| WP-05 | Protocol and operational acceptance | ProxyCapabilityMatrix; RouteMetrics; FaultScenario |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
