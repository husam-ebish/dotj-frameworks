# DJ-053 .j Substitute: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 491 | recursive complete |
| Project-definition paths | 6 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 248 | Lexical path classification, not runnable test count |
| Sampled text files | 9 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 39 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 10 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [src/NSubstitute/NSubstitute.csproj](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/NSubstitute.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [tests/NSubstitute.Acceptance.Specs/NSubstitute.Acceptance.Specs.csproj](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/NSubstitute.Acceptance.Specs.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [tests/NSubstitute.Benchmarks/NSubstitute.Benchmarks.csproj](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Benchmarks/NSubstitute.Benchmarks.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [tests/NSubstitute.Documentation.Tests.Generator/NSubstitute.Documentation.Tests.Generator.csproj](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Documentation.Tests.Generator/NSubstitute.Documentation.Tests.Generator.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [tests/NSubstitute.Documentation.Tests/NSubstitute.Documentation.Tests.csproj](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Documentation.Tests/NSubstitute.Documentation.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [tests/NSubstitute.Specs/NSubstitute.Specs.csproj](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Specs/NSubstitute.Specs.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/NSubstitute/Arg.cs:13](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L13) | `public static partial class Arg` |
| [src/NSubstitute/Arg.cs:22](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L22) | `public interface AnyType` |
| [src/NSubstitute/Arg.cs:29](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L29) | `public static ref T Any<T>()` |
| [src/NSubstitute/Arg.cs:37](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L37) | `public static ref T Is<T>(T value)` |
| [src/NSubstitute/Arg.cs:46](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L46) | `public static ref T Is<T>(Expression<Predicate<T>> predicate)` |
| [src/NSubstitute/Arg.cs:55](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L55) | `public static ref T Is<T>(Expression<Predicate<object>> predicate) where T : AnyType` |
| [src/NSubstitute/Arg.cs:63](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L63) | `public static ref T Is<T>(IArgumentMatcher matcher) =>` |
| [src/NSubstitute/Arg.cs:69](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L69) | `public static ref T Is<T>(IArgumentMatcher<T> matcher) =>` |
| [src/NSubstitute/Arg.cs:75](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L75) | `public static ref T Same<T>(T value)` |
| [src/NSubstitute/Arg.cs:84](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L84) | `public static ref Action Invoke()` |
| [src/NSubstitute/Arg.cs:92](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L92) | `public static ref Action<T> Invoke<T>(T arg)` |
| [src/NSubstitute/Arg.cs:100](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L100) | `public static ref Action<T1, T2> Invoke<T1, T2>(T1 arg1, T2 arg2)` |
| [src/NSubstitute/Arg.cs:108](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L108) | `public static ref Action<T1, T2, T3> Invoke<T1, T2, T3>(T1 arg1, T2 arg2, T3 arg3)` |
| [src/NSubstitute/Arg.cs:116](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L116) | `public static ref Action<T1, T2, T3, T4> Invoke<T1, T2, T3, T4>(T1 arg1, T2 arg2, T3 arg3, T4 arg4)` |
| [src/NSubstitute/Arg.cs:125](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L125) | `public static ref TDelegate InvokeDelegate<TDelegate>(params object[] arguments)` |
| [src/NSubstitute/Arg.cs:134](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L134) | `public static ref T Do<T>(Action<T> useArgument)` |
| [src/NSubstitute/Arg.cs:143](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Arg.cs#L143) | `public static ref T Do<T>(Action<object> useArgument) where T : AnyType` |
| [src/NSubstitute/Raise.cs:10](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Raise.cs#L10) | `public static class Raise` |
| [src/NSubstitute/Raise.cs:15](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Raise.cs#L15) | `public static EventHandlerWrapper<TEventArgs> EventWith<TEventArgs>(object sender, TEventArgs eventArgs) where TEventArgs : EventArgs` |
| [src/NSubstitute/Raise.cs:23](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Raise.cs#L23) | `public static EventHandlerWrapper<TEventArgs> EventWith<TEventArgs>(TEventArgs eventArgs) where TEventArgs : EventArgs` |
| [src/NSubstitute/Raise.cs:32](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Raise.cs#L32) | `public static EventHandlerWrapper<TEventArgs> EventWith<TEventArgs>() where TEventArgs : EventArgs` |
| [src/NSubstitute/Raise.cs:41](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Raise.cs#L41) | `public static EventHandlerWrapper<EventArgs> Event()` |
| [src/NSubstitute/Raise.cs:50](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/src/NSubstitute/Raise.cs#L50) | `public static DelegateEventWrapper<THandler> Event<THandler>(params object[] arguments)` |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:6](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L6) | `public class PerfTests` |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:10](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L10) | `public void TimeBasicOperations()` |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:34](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L34) | `public void TimeBasicOperationsWithGenerics()` |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:58](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L58) | `public void Multiple_return_configuration_dont_leak_memory_for_any_args()` |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:73](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L73) | `public void Muiltiple_return_configurations_dont_lead_to_memory_leak()` |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:87](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L87) | `public void Delegate_proxy_container_is_cached()` |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:99](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L99) | `public void ProxyTypeIsCached()` |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:110](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L110) | `public interface IFoo { int GetInt(string s); }` |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:111](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L111) | `public interface IBar { int GetInt<T>(T t); }` |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:112](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L112) | `public interface IByteArraySource { byte[] GetArray(); }` |
| [tests/NSubstitute.Acceptance.Specs/PerfTests.cs:113](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/PerfTests.cs#L113) | `public interface IByteArrayConsumer { bool ConsumeArray(byte[] array); }` |
| [tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs:7](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs#L7) | `public class ILoggerTests` |
| [tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs:10](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs#L10) | `public void Received_LogTrace_call_using_AnyType()` |
| [tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs:27](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs#L27) | `public void Received_LogWarning_call_using_interfaced_types()` |
| [tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs:44](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs#L44) | `public void Received_LogError_call_using_messageTemplate()` |
| [tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs:70](https://github.com/nsubstitute/NSubstitute/blob/f2b623d762fc28fc1a2fe3932b3b360d113c734d/tests/NSubstitute.Acceptance.Specs/ILoggerTests.cs#L70) | `public void Received_LogInformation_call_using_messageTemplate()` |

Full lexical records (39) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | Substitution and call specification | Substitute; CallSpecification; ArgumentSpecification |
| WP-02 | Returns callbacks and recursive values | ReturnSequence; CallAction; AutoValueProvider |
| WP-03 | Received calls order and events | ReceivedCheck; CallOrder; EventAdapter |
| WP-04 | Proxy instrumentation and thread state | SubstituteFactory; InterceptionCapability; ConfigurationScope |
| WP-05 | Integration and regression acceptance | SubstituteCase; AssertionAdapter; CleanupRecord |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
