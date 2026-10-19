# DJ-052 .j Mock: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 244 | recursive complete |
| Project-definition paths | 14 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 58 | Lexical path classification, not runnable test count |
| Sampled text files | 11 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 59 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 46 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [src/Acceptance/Dynamic/Dynamic.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Acceptance/Dynamic/Dynamic.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Acceptance/Static/Static.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Acceptance/Static/Static.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq.CodeAnalysis/Moq.CodeAnalysis.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis/Moq.CodeAnalysis.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq.CodeFixes.UnitTests/Moq.CodeFixes.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeFixes.UnitTests/Moq.CodeFixes.UnitTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq.CodeFixes/Moq.CodeFixes.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeFixes/Moq.CodeFixes.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq.DynamicProxy/Moq.DynamicProxy.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.DynamicProxy/Moq.DynamicProxy.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq.Sdk.Tests/Moq.Sdk.Tests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Sdk.Tests/Moq.Sdk.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq.Sdk/Moq.Sdk.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Sdk/Moq.Sdk.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq.StaticProxy.UnitTests/Moq.StaticProxy.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.StaticProxy.UnitTests/Moq.StaticProxy.UnitTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq.StaticProxy/Moq.StaticProxy.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.StaticProxy/Moq.StaticProxy.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq.Tests/Moq.Tests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/Moq.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq.Vsix/Moq.Vsix.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Vsix/Moq.Vsix.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Moq/Moq.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Moq.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/Moq/Arg.cs:9](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Arg.cs#L9) | `public static class Arg` |
| [src/Moq/Arg.cs:15](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Arg.cs#L15) | `public static T Any<T>() => MockSetup.Push<T>(AnyMatcher<T>.Default);` |
| [src/Moq/Arg.cs:22](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Arg.cs#L22) | `public static T Any<T>(Func<T?, bool> condition) => MockSetup.Push<T>(new ConditionalMatcher<T>(condition));` |
| [src/Moq/Arg.cs:28](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Arg.cs#L28) | `public static T Not<T>(T? value) => MockSetup.Push<T>(new NotMatcher<T>(value));` |
| [src/Moq/Arg.cs:35](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Arg.cs#L35) | `public static class Arg<T>` |
| [src/Moq/Arg.cs:40](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Arg.cs#L40) | `public static T Any => MockSetup.Push<T>(AnyMatcher<T>.Default);` |
| [src/Moq/Arg.cs:45](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Arg.cs#L45) | `public static T Not(T? value) => MockSetup.Push<T>(new NotMatcher<T>(value));` |
| [src/Moq/IMock.cs:9](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/IMock.cs#L9) | `public interface IMock : IFluentInterface` |
| [src/Moq.Tests/MoqTests.cs:12](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L12) | `public class MoqTests` |
| [src/Moq.Tests/MoqTests.cs:15](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L15) | `public void SetupDoesNotRecordCalls()` |
| [src/Moq.Tests/MoqTests.cs:25](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L25) | `public void CanRaiseEvents()` |
| [src/Moq.Tests/MoqTests.cs:52](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L52) | `public void CanRaiseEventsWithArgs()` |
| [src/Moq.Tests/MoqTests.cs:65](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L65) | `public void CanSetupPropertyViaReturns()` |
| [src/Moq.Tests/MoqTests.cs:75](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L75) | `public void CanSetupPropertyDirectly()` |
| [src/Moq.Tests/MoqTests.cs:85](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L85) | `public void CanSetupPropertyTwiceViaReturns()` |
| [src/Moq.Tests/MoqTests.cs:96](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L96) | `public void CanSetupMethodWithArgumentsViaReturns()` |
| [src/Moq.Tests/MoqTests.cs:106](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L106) | `public void CanSetupMethodWithDifferentArgumentsViaReturns()` |
| [src/Moq.Tests/MoqTests.cs:123](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L123) | `public void CanReturnFunction()` |
| [src/Moq.Tests/MoqTests.cs:132](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L132) | `public interface IAsync` |
| [src/Moq.Tests/MoqTests.cs:141](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L141) | `public async Task CanReturnAsyncFunction()` |
| [src/Moq.Tests/MoqTests.cs:151](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L151) | `public async Task CanReturnAsyncValueFunction()` |
| [src/Moq.Tests/MoqTests.cs:161](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L161) | `public async Task ThrowsAsync()` |
| [src/Moq.Tests/MoqTests.cs:171](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L171) | `public async Task ThrowsAsyncWithException()` |
| [src/Moq.Tests/MoqTests.cs:181](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L181) | `public async Task ThrowsValueAsync()` |
| [src/Moq.Tests/MoqTests.cs:191](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L191) | `public async Task ThrowsValueAsyncWithException()` |
| [src/Moq.Tests/MoqTests.cs:201](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L201) | `public async Task ThrowsVoidAsync()` |
| [src/Moq.Tests/MoqTests.cs:211](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L211) | `public async Task ThrowsVoidAsyncWithException()` |
| [src/Moq.Tests/MoqTests.cs:221](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L221) | `public async Task ThrowsValueVoidAsync()` |
| [src/Moq.Tests/MoqTests.cs:231](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L231) | `public async Task ThrowsValueVoidAsyncWithException()` |
| [src/Moq.Tests/MoqTests.cs:241](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L241) | `public void CanReturnFunctionWithArgs()` |
| [src/Moq.Tests/MoqTests.cs:252](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L252) | `public void CanReturnFunctionWithUntypedArgs()` |
| [src/Moq.Tests/MoqTests.cs:263](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L263) | `public void CanInvokeCallback()` |
| [src/Moq.Tests/MoqTests.cs:277](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L277) | `public void CanInvokeTwoCallbacks()` |
| [src/Moq.Tests/MoqTests.cs:295](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L295) | `public void CanInvokeCallbackAfterReturn()` |
| [src/Moq.Tests/MoqTests.cs:309](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L309) | `public void ThrowsWithException()` |
| [src/Moq.Tests/MoqTests.cs:319](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L319) | `public void ThrowsWithExceptionType()` |
| [src/Moq.Tests/MoqTests.cs:329](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L329) | `public void CanSetupPropertyViaReturnsForStrictMock()` |
| [src/Moq.Tests/MoqTests.cs:340](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L340) | `public void CanSetupPropertyForStrictMock()` |
| [src/Moq.Tests/MoqTests.cs:352](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L352) | `public void CanSetupVoidMethod()` |
| [src/Moq.Tests/MoqTests.cs:362](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L362) | `public void CanAccessMockInfoFromInstance()` |
| [src/Moq.Tests/MoqTests.cs:374](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L374) | `public void CanAssertInvocations()` |
| [src/Moq.Tests/MoqTests.cs:394](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L394) | `public void ChangeDefaultValue()` |
| [src/Moq.Tests/MoqTests.cs:407](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L407) | `public void ChangeBehavior()` |
| [src/Moq.Tests/MoqTests.cs:422](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs#L422) | `public void ChangingBehaviorPreservesDefaultValue()` |
| [src/Moq.Tests/MockTests.cs:12](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L12) | `public class MockTests` |
| [src/Moq.Tests/MockTests.cs:15](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L15) | `public void CreatesMockForSetup()` |
| [src/Moq.Tests/MockTests.cs:26](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L26) | `public void CreatesStrictMock()` |
| [src/Moq.Tests/MockTests.cs:38](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L38) | `public void CreatesClassMockThatCallsBase()` |
| [src/Moq.Tests/MockTests.cs:49](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L49) | `public void CreatesMockWithAdditionalInterfaces()` |
| [src/Moq.Tests/MockTests.cs:63](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L63) | `public void AsThrowsIfInterfaceIsNotImplemented()` |
| [src/Moq.Tests/MockTests.cs:67](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L67) | `public void GetsMockForImplementedInterface()` |
| [src/Moq.Tests/MockTests.cs:77](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L77) | `public void GetThrowsIfInterfaceIsNotImplemented()` |
| [src/Moq.Tests/MockTests.cs:81](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L81) | `public void GetThrowsIfNotMock()` |
| [src/Moq.Tests/MockTests.cs:85](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L85) | `public void MocksDelegates()` |
| [src/Moq.Tests/MockTests.cs:96](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L96) | `public void CustomizesCreatedMocks()` |
| [src/Moq.Tests/MockTests.cs:105](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L105) | `public void CustomizesCreatedMocksWithAdditionalInterfaces()` |
| [src/Moq.Tests/MockTests.cs:109](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L109) | `public void CustomConstructorsCreateMocks()` |
| [src/Moq.Tests/MockTests.cs:116](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L116) | `public interface ICustomized` |
| [src/Moq.Tests/MockTests.cs:128](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs#L128) | `public Mock(string name) : this() => this.Sdk.Name = name;` |

Full lexical records (59) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | Mock model and invocation recording | Mock; Invocation; MethodKey; ArgumentMatcher |
| WP-02 | Setup return callbacks and verification | Setup; Answer; Verification; Times |
| WP-03 | Proxy and instrumentation feasibility | ProxyFactory; InstrumentationCapability; ClassTransform |
| WP-04 | Lifecycle concurrency and cleanup | MockScope; InvocationStore; AgentSession |
| WP-05 | Language adaptations and conformance | MockExpression; MatchSpecification; MockCase |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
