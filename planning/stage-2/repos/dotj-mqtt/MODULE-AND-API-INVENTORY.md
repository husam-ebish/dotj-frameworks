# DJ-034 .j MQTT: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 499 | recursive complete |
| Project-definition paths | 12 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 113 | Lexical path classification, not runnable test count |
| Sampled text files | 12 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 36 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 3 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [Samples/MQTTnet.Samples.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Samples/MQTTnet.Samples.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [Source/MQTTnet.AspTestApp/MQTTnet.AspTestApp.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspTestApp/MQTTnet.AspTestApp.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [Source/MQTTnet.AspnetCore/MQTTnet.AspNetCore.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/MQTTnet.AspNetCore.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Source/MQTTnet.Benchmarks/MQTTnet.Benchmarks.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Benchmarks/MQTTnet.Benchmarks.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [Source/MQTTnet.Extensions.Rpc/MQTTnet.Extensions.Rpc.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Extensions.Rpc/MQTTnet.Extensions.Rpc.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Source/MQTTnet.Extensions.Socks5/MQTTnet.Extensions.Socks5.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Extensions.Socks5/MQTTnet.Extensions.Socks5.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Source/MQTTnet.Extensions.TopicTemplate/MQTTnet.Extensions.TopicTemplate.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Extensions.TopicTemplate/MQTTnet.Extensions.TopicTemplate.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Source/MQTTnet.Server/MQTTnet.Server.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Server/MQTTnet.Server.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Source/MQTTnet.TestApp/MQTTnet.TestApp.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.TestApp/MQTTnet.TestApp.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [Source/MQTTnet.Tests.Extensions.Socks5/MQTTnet.Tests.Extensions.Socks5.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests.Extensions.Socks5/MQTTnet.Tests.Extensions.Socks5.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [Source/MQTTnet.Tests/MQTTnet.Tests.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/MQTTnet.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [Source/MQTTnet/MQTTnet.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MQTTnet.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [Source/MQTTnet.AspnetCore/DuplexPipe.cs:9](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/DuplexPipe.cs#L9) | `public class DuplexPipe : IDuplexPipe` |
| [Source/MQTTnet.AspnetCore/DuplexPipe.cs:11](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/DuplexPipe.cs#L11) | `public DuplexPipe(PipeReader reader, PipeWriter writer)` |
| [Source/MQTTnet.AspnetCore/DuplexPipe.cs:17](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/DuplexPipe.cs#L17) | `public PipeReader Input { get; }` |
| [Source/MQTTnet.AspnetCore/DuplexPipe.cs:19](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/DuplexPipe.cs#L19) | `public PipeWriter Output { get; }` |
| [Source/MQTTnet.AspnetCore/DuplexPipe.cs:21](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/DuplexPipe.cs#L21) | `public static DuplexPipePair CreateConnectionPair(PipeOptions inputOptions, PipeOptions outputOptions)` |
| [Source/MQTTnet.AspnetCore/DuplexPipe.cs:33](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/DuplexPipe.cs#L33) | `public readonly struct DuplexPipePair` |
| [Source/MQTTnet.AspnetCore/DuplexPipe.cs:35](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/DuplexPipe.cs#L35) | `public IDuplexPipe Transport { get; }` |
| [Source/MQTTnet.AspnetCore/DuplexPipe.cs:36](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/DuplexPipe.cs#L36) | `public IDuplexPipe Application { get; }` |
| [Source/MQTTnet.AspnetCore/DuplexPipe.cs:38](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/DuplexPipe.cs#L38) | `public DuplexPipePair(IDuplexPipe transport, IDuplexPipe application)` |
| [Source/MQTTnet.AspnetCore/SocketSender.cs:13](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/SocketSender.cs#L13) | `public sealed class SocketSender : IDisposable` |
| [Source/MQTTnet.AspnetCore/SocketSender.cs:21](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/SocketSender.cs#L21) | `public SocketSender(Socket socket, PipeScheduler scheduler)` |
| [Source/MQTTnet.AspnetCore/SocketSender.cs:29](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/SocketSender.cs#L29) | `public void Dispose()` |
| [Source/MQTTnet.AspnetCore/SocketSender.cs:34](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/SocketSender.cs#L34) | `public SocketAwaitable SendAsync(in ReadOnlySequence<byte> buffers)` |
| [Source/MQTTnet/MqttClient.cs:17](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L17) | `public sealed class MqttClient : Disposable, IMqttClient` |
| [Source/MQTTnet/MqttClient.cs:49](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L49) | `public MqttClient(IMqttClientAdapterFactory channelFactory, IMqttNetLogger logger)` |
| [Source/MQTTnet/MqttClient.cs:56](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L56) | `public event Func<MqttApplicationMessageReceivedEventArgs, Task> ApplicationMessageReceivedAsync` |
| [Source/MQTTnet/MqttClient.cs:62](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L62) | `public event Func<MqttClientConnectedEventArgs, Task> ConnectedAsync` |
| [Source/MQTTnet/MqttClient.cs:68](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L68) | `public event Func<MqttClientConnectingEventArgs, Task> ConnectingAsync` |
| [Source/MQTTnet/MqttClient.cs:74](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L74) | `public event Func<MqttClientDisconnectedEventArgs, Task> DisconnectedAsync` |
| [Source/MQTTnet/MqttClient.cs:80](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L80) | `public event Func<InspectMqttPacketEventArgs, Task> InspectPacketAsync` |
| [Source/MQTTnet/MqttClient.cs:86](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L86) | `public bool IsConnected => (MqttClientConnectionStatus)_connectionStatus == MqttClientConnectionStatus.Connected;` |
| [Source/MQTTnet/MqttClient.cs:88](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L88) | `public MqttClientOptions Options { get; private set; }` |
| [Source/MQTTnet/MqttClient.cs:90](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L90) | `public async Task<MqttClientConnectResult> ConnectAsync(MqttClientOptions options, CancellationToken cancellationToken = default)` |
| [Source/MQTTnet/MqttClient.cs:178](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L178) | `public async Task DisconnectAsync(MqttClientDisconnectOptions options, CancellationToken cancellationToken = default)` |
| [Source/MQTTnet/MqttClient.cs:226](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L226) | `public async Task PingAsync(CancellationToken cancellationToken = default)` |
| [Source/MQTTnet/MqttClient.cs:244](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L244) | `public Task<MqttClientPublishResult> PublishAsync(MqttApplicationMessage applicationMessage, CancellationToken cancellationToken = default)` |
| [Source/MQTTnet/MqttClient.cs:281](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L281) | `public Task SendEnhancedAuthenticationExchangeDataAsync(MqttEnhancedAuthenticationExchangeData data, CancellationToken cancellationToken = default)` |
| [Source/MQTTnet/MqttClient.cs:301](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L301) | `public async Task<MqttClientSubscribeResult> SubscribeAsync(MqttClientSubscribeOptions options, CancellationToken cancellationToken = default)` |
| [Source/MQTTnet/MqttClient.cs:335](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L335) | `public async Task<MqttClientUnsubscribeResult> UnsubscribeAsync(MqttClientUnsubscribeOptions options, CancellationToken cancellationToken = default)` |
| [Source/MQTTnet/MqttClient.cs:369](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs#L369) | `protected override void Dispose(bool disposing)` |
| [Source/MQTTnet.Tests/Protocol_Tests.cs:11](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/Protocol_Tests.cs#L11) | `public sealed class Protocol_Tests` |
| [Source/MQTTnet.Tests/Protocol_Tests.cs:14](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/Protocol_Tests.cs#L14) | `public void Encode_Four_Byte_Integer()` |
| [Source/MQTTnet.Tests/Protocol_Tests.cs:35](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/Protocol_Tests.cs#L35) | `public void Encode_Two_Byte_Integer()` |
| [Source/MQTTnet.Tests/RoundtripTime_Tests.cs:14](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/RoundtripTime_Tests.cs#L14) | `public class RoundtripTime_Tests` |
| [Source/MQTTnet.Tests/RoundtripTime_Tests.cs:16](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/RoundtripTime_Tests.cs#L16) | `public TestContext TestContext { get; set; }` |
| [Source/MQTTnet.Tests/RoundtripTime_Tests.cs:19](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/RoundtripTime_Tests.cs#L19) | `public async Task Round_Trip_Time()` |

Full lexical records (36) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | Packet codecs and negotiation | MqttPacket; ProtocolVersion; PropertySet |
| WP-02 | Client connection and session state | ClientSession; SessionExpiry; KeepAliveState |
| WP-03 | QoS inflight and retained delivery | PacketIdentifier; InflightRecord; DeliveryState |
| WP-04 | Broker subscriptions and routing | SubscriptionFilter; BrokerSession; RetainedMessage |
| WP-05 | Extensions transports and conformance | MqttCapability; TransportAdapter; ProtocolTrace |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
