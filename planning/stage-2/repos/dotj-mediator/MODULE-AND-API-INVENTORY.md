# DJ-065 .j Mediator: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 192 | recursive complete |
| Project-definition paths | 15 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 71 | Lexical path classification, not runnable test count |
| Sampled text files | 8 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 85 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 29 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [samples/MediatR.Examples.AspNetCore/MediatR.Examples.AspNetCore.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/samples/MediatR.Examples.AspNetCore/MediatR.Examples.AspNetCore.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MediatR.Examples.Autofac/MediatR.Examples.Autofac.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/samples/MediatR.Examples.Autofac/MediatR.Examples.Autofac.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MediatR.Examples.DryIoc/MediatR.Examples.DryIoc.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/samples/MediatR.Examples.DryIoc/MediatR.Examples.DryIoc.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MediatR.Examples.Lamar/MediatR.Examples.Lamar.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/samples/MediatR.Examples.Lamar/MediatR.Examples.Lamar.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MediatR.Examples.LightInject/MediatR.Examples.LightInject.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/samples/MediatR.Examples.LightInject/MediatR.Examples.LightInject.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MediatR.Examples.PublishStrategies/MediatR.Examples.PublishStrategies.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/samples/MediatR.Examples.PublishStrategies/MediatR.Examples.PublishStrategies.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MediatR.Examples.SimpleInjector/MediatR.Examples.SimpleInjector.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/samples/MediatR.Examples.SimpleInjector/MediatR.Examples.SimpleInjector.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MediatR.Examples.Stashbox/MediatR.Examples.Stashbox.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/samples/MediatR.Examples.Stashbox/MediatR.Examples.Stashbox.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MediatR.Examples.Windsor/MediatR.Examples.Windsor.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/samples/MediatR.Examples.Windsor/MediatR.Examples.Windsor.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MediatR.Examples/MediatR.Examples.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/samples/MediatR.Examples/MediatR.Examples.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/MediatR.Contracts/MediatR.Contracts.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR.Contracts/MediatR.Contracts.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/MediatR/MediatR.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/MediatR.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [test/MediatR.Benchmarks/MediatR.Benchmarks.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Benchmarks/MediatR.Benchmarks.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/MediatR.DependencyInjectionTests/MediatR.DependencyInjectionTests.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.DependencyInjectionTests/MediatR.DependencyInjectionTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/MediatR.Tests/MediatR.Tests.csproj](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/MediatR.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/MediatR/ISender.cs:10](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/ISender.cs#L10) | `public interface ISender` |
| [src/MediatR/Mediator.cs:17](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L17) | `public class Mediator : IMediator` |
| [src/MediatR/Mediator.cs:29](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L29) | `public Mediator(IServiceProvider serviceProvider)` |
| [src/MediatR/Mediator.cs:37](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L37) | `public Mediator(IServiceProvider serviceProvider, INotificationPublisher publisher)` |
| [src/MediatR/Mediator.cs:48](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L48) | `public static string? LicenseKey { get; set; }` |
| [src/MediatR/Mediator.cs:50](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L50) | `public Task<TResponse> Send<TResponse>(IRequest<TResponse> request, CancellationToken cancellationToken = default)` |
| [src/MediatR/Mediator.cs:67](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L67) | `public Task Send<TRequest>(TRequest request, CancellationToken cancellationToken = default)` |
| [src/MediatR/Mediator.cs:85](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L85) | `public Task<object?> Send(object request, CancellationToken cancellationToken = default)` |
| [src/MediatR/Mediator.cs:121](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L121) | `public Task Publish<TNotification>(TNotification notification, CancellationToken cancellationToken = default)` |
| [src/MediatR/Mediator.cs:132](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L132) | `public Task Publish(object notification, CancellationToken cancellationToken = default) =>` |
| [src/MediatR/Mediator.cs:147](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L147) | `protected virtual Task PublishCore(IEnumerable<NotificationHandlerExecutor> handlerExecutors, INotification notification, CancellationToken cancellationToken)` |
| [src/MediatR/Mediator.cs:163](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L163) | `public IAsyncEnumerable<TResponse> CreateStream<TResponse>(IStreamRequest<TResponse> request, CancellationToken cancellationToken = default)` |
| [src/MediatR/Mediator.cs:183](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/src/MediatR/Mediator.cs#L183) | `public IAsyncEnumerable<object?> CreateStream(object request, CancellationToken cancellationToken = default)` |
| [test/MediatR.Tests/SendTests.cs:12](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L12) | `public class SendTests` |
| [test/MediatR.Tests/SendTests.cs:18](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L18) | `public SendTests()` |
| [test/MediatR.Tests/SendTests.cs:34](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L34) | `public class Ping : IRequest<Pong>` |
| [test/MediatR.Tests/SendTests.cs:36](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L36) | `public string? Message { get; set; }` |
| [test/MediatR.Tests/SendTests.cs:39](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L39) | `public class VoidPing : IRequest` |
| [test/MediatR.Tests/SendTests.cs:43](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L43) | `public class Pong` |
| [test/MediatR.Tests/SendTests.cs:45](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L45) | `public string? Message { get; set; }` |
| [test/MediatR.Tests/SendTests.cs:48](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L48) | `public class PingHandler : IRequestHandler<Ping, Pong>` |
| [test/MediatR.Tests/SendTests.cs:50](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L50) | `public Task<Pong> Handle(Ping request, CancellationToken cancellationToken)` |
| [test/MediatR.Tests/SendTests.cs:56](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L56) | `public class Dependency` |
| [test/MediatR.Tests/SendTests.cs:58](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L58) | `public bool Called { get; set; }` |
| [test/MediatR.Tests/SendTests.cs:59](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L59) | `public bool CalledSpecific { get; set; }` |
| [test/MediatR.Tests/SendTests.cs:62](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L62) | `public class VoidPingHandler : IRequestHandler<VoidPing>` |
| [test/MediatR.Tests/SendTests.cs:66](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L66) | `public VoidPingHandler(Dependency dependency) => _dependency = dependency;` |
| [test/MediatR.Tests/SendTests.cs:68](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L68) | `public Task Handle(VoidPing request, CancellationToken cancellationToken)` |
| [test/MediatR.Tests/SendTests.cs:76](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L76) | `public class GenericPing<T> : IRequest<T>` |
| [test/MediatR.Tests/SendTests.cs:79](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L79) | `public T? Pong { get; set; }` |
| [test/MediatR.Tests/SendTests.cs:82](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L82) | `public class GenericPingHandler<T> : IRequestHandler<GenericPing<T>, T>` |
| [test/MediatR.Tests/SendTests.cs:87](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L87) | `public GenericPingHandler(Dependency dependency) => _dependency = dependency;` |
| [test/MediatR.Tests/SendTests.cs:89](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L89) | `public Task<T> Handle(GenericPing<T> request, CancellationToken cancellationToken)` |
| [test/MediatR.Tests/SendTests.cs:97](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L97) | `public class VoidGenericPing<T> : IRequest` |
| [test/MediatR.Tests/SendTests.cs:101](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L101) | `public class VoidGenericPingHandler<T> : IRequestHandler<VoidGenericPing<T>>` |
| [test/MediatR.Tests/SendTests.cs:105](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L105) | `public VoidGenericPingHandler(Dependency dependency) => _dependency = dependency;` |
| [test/MediatR.Tests/SendTests.cs:107](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L107) | `public Task Handle(VoidGenericPing<T> request, CancellationToken cancellationToken)` |
| [test/MediatR.Tests/SendTests.cs:115](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L115) | `public class PongExtension : Pong` |
| [test/MediatR.Tests/SendTests.cs:120](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L120) | `public class TestClass1PingRequestHandler : IRequestHandler<VoidGenericPing<PongExtension>>` |
| [test/MediatR.Tests/SendTests.cs:124](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L124) | `public TestClass1PingRequestHandler(Dependency dependency) => _dependency = dependency;` |
| [test/MediatR.Tests/SendTests.cs:126](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L126) | `public Task Handle(VoidGenericPing<PongExtension> request, CancellationToken cancellationToken)` |
| [test/MediatR.Tests/SendTests.cs:133](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L133) | `public interface ITestInterface1 { }` |
| [test/MediatR.Tests/SendTests.cs:134](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L134) | `public interface ITestInterface2 { }` |
| [test/MediatR.Tests/SendTests.cs:135](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L135) | `public interface ITestInterface3 { }` |
| [test/MediatR.Tests/SendTests.cs:137](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L137) | `public class TestClass1 : ITestInterface1 { }` |
| [test/MediatR.Tests/SendTests.cs:138](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L138) | `public class TestClass2 : ITestInterface2 { }` |
| [test/MediatR.Tests/SendTests.cs:139](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L139) | `public class TestClass3 : ITestInterface3 { }` |
| [test/MediatR.Tests/SendTests.cs:141](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L141) | `public class MultipleGenericTypeParameterRequest<T1, T2, T3> : IRequest<int>` |
| [test/MediatR.Tests/SendTests.cs:146](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L146) | `public int Foo { get; set; }` |
| [test/MediatR.Tests/SendTests.cs:149](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L149) | `public class MultipleGenericTypeParameterRequestHandler<T1, T2, T3> : IRequestHandler<MultipleGenericTypeParameterRequest<T1, T2, T3>, int>` |
| [test/MediatR.Tests/SendTests.cs:156](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L156) | `public MultipleGenericTypeParameterRequestHandler(Dependency dependency) => _dependency = dependency;` |
| [test/MediatR.Tests/SendTests.cs:158](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L158) | `public Task<int> Handle(MultipleGenericTypeParameterRequest<T1, T2, T3> request, CancellationToken cancellationToken)` |
| [test/MediatR.Tests/SendTests.cs:165](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L165) | `public class TimeoutBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>` |
| [test/MediatR.Tests/SendTests.cs:168](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L168) | `public async Task<TResponse> Handle(TRequest request, RequestHandlerDelegate<TResponse> next, CancellationToken cancellationToken)` |
| [test/MediatR.Tests/SendTests.cs:177](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L177) | `public class TimeoutRequest : IRequest` |
| [test/MediatR.Tests/SendTests.cs:181](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L181) | `public class TimeoutRequest2 : IRequest<int>` |
| [test/MediatR.Tests/SendTests.cs:185](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L185) | `public class TimeoutRequestHandler : IRequestHandler<TimeoutRequest>` |
| [test/MediatR.Tests/SendTests.cs:189](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L189) | `public TimeoutRequestHandler(Dependency dependency) => _dependency = dependency;` |
| [test/MediatR.Tests/SendTests.cs:191](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L191) | `public async Task Handle(TimeoutRequest request, CancellationToken cancellationToken)` |
| [test/MediatR.Tests/SendTests.cs:199](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L199) | `public class TimeoutRequest2Handler : IRequestHandler<TimeoutRequest2, int>` |
| [test/MediatR.Tests/SendTests.cs:203](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L203) | `public TimeoutRequest2Handler(Dependency dependency) => _dependency = dependency;` |
| [test/MediatR.Tests/SendTests.cs:205](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L205) | `public async Task<int> Handle(TimeoutRequest2 request, CancellationToken cancellationToken)` |
| [test/MediatR.Tests/SendTests.cs:215](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L215) | `public async Task Should_resolve_main_handler()` |
| [test/MediatR.Tests/SendTests.cs:223](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L223) | `public async Task Should_resolve_main_void_handler()` |
| [test/MediatR.Tests/SendTests.cs:231](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L231) | `public async Task Should_resolve_main_handler_via_dynamic_dispatch()` |
| [test/MediatR.Tests/SendTests.cs:241](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L241) | `public async Task Should_resolve_main_void_handler_via_dynamic_dispatch()` |
| [test/MediatR.Tests/SendTests.cs:252](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L252) | `public async Task Should_resolve_main_handler_by_specific_interface()` |
| [test/MediatR.Tests/SendTests.cs:260](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L260) | `public async Task Should_resolve_main_handler_by_given_interface()` |
| [test/MediatR.Tests/SendTests.cs:270](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L270) | `public Task Should_raise_execption_on_null_request() => Should.ThrowAsync<ArgumentNullException>(async () => await _mediator.Send(default!));` |
| [test/MediatR.Tests/SendTests.cs:273](https://github.com/LuckyPennySoftware/MediatR/blob/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5/test/MediatR.Tests/SendTests.cs#L273) | `public async Task Should_resolve_generic_handler()` |

Full lexical records (85) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | License baseline requests and handlers | MediatorLicenseRecord; Request; Handler; Response |
| WP-02 | Pipeline behaviors and exception handling | PipelineBehavior; RequestContext; ExceptionHandler |
| WP-03 | Notifications publishing and concurrency | Notification; NotificationHandler; PublishStrategy |
| WP-04 | Streaming requests and lifecycle | StreamRequest; StreamHandler; StreamBehavior |
| WP-05 | Registration adapters and verification | MediatorRegistry; CoreDiAdapter; MediatorCase |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
