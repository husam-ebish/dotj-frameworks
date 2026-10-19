# DJ-027 .j Resilience: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 1026 | recursive complete |
| Project-definition paths | 22 | Files, not restored packages |
| API-definition/ref paths | 10 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 329 | Lexical path classification, not runnable test count |
| Sampled text files | 15 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 17 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 9 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [bench/Polly.Benchmarks/Polly.Benchmarks.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/bench/Polly.Benchmarks/Polly.Benchmarks.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [bench/Polly.Core.Benchmarks/Polly.Core.Benchmarks.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/bench/Polly.Core.Benchmarks/Polly.Core.Benchmarks.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/Chaos/Chaos.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/samples/Chaos/Chaos.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/DependencyInjection/DependencyInjection.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/samples/DependencyInjection/DependencyInjection.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/Extensibility/Extensibility.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/samples/Extensibility/Extensibility.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GenericPipelines/GenericPipelines.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/samples/GenericPipelines/GenericPipelines.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/Intro.FSharp/Intro.FSharp.fsproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/samples/Intro.FSharp/Intro.FSharp.fsproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/Intro/Intro.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/samples/Intro/Intro.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/Retries/Retries.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/samples/Retries/Retries.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/Polly.Core/Polly.Core.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Polly.Core.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Polly.Extensions/Polly.Extensions.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Extensions/Polly.Extensions.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Polly.RateLimiting/Polly.RateLimiting.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.RateLimiting/Polly.RateLimiting.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Polly.Testing/Polly.Testing.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Testing/Polly.Testing.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Polly/Polly.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly/Polly.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Snippets/Snippets.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Snippets/Snippets.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [test/Polly.AotTest/Polly.AotTest.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.AotTest/Polly.AotTest.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Polly.Core.Tests/Polly.Core.Tests.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/Polly.Core.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Polly.Extensions.Tests/Polly.Extensions.Tests.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Extensions.Tests/Polly.Extensions.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Polly.RateLimiting.Tests/Polly.RateLimiting.Tests.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.RateLimiting.Tests/Polly.RateLimiting.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Polly.Specs/Polly.Specs.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Specs/Polly.Specs.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Polly.TestUtils/Polly.TestUtils.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.TestUtils/Polly.TestUtils.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Polly.Testing.Tests/Polly.Testing.Tests.csproj](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Testing.Tests/Polly.Testing.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/Polly.Core/Outcome.cs:6](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Outcome.cs#L6) | `public static class Outcome` |
| [src/Polly.Core/Outcome.cs:14](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Outcome.cs#L14) | `public static Outcome<TResult> FromResult<TResult>(TResult? value) => new(value);` |
| [src/Polly.Core/Outcome.cs:22](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Outcome.cs#L22) | `public static ValueTask<Outcome<TResult>> FromResultAsValueTask<TResult>(TResult value) => new(FromResult(value));` |
| [src/Polly.Core/Outcome.cs:31](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Outcome.cs#L31) | `public static Outcome<TResult> FromException<TResult>(Exception exception)` |
| [src/Polly.Core/Outcome.cs:45](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/Outcome.cs#L45) | `public static ValueTask<Outcome<TResult>> FromExceptionAsValueTask<TResult>(Exception exception)` |
| [src/Polly.Core/VoidResult.cs:12](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/src/Polly.Core/VoidResult.cs#L12) | `public static readonly VoidResult Instance = new();` |
| [test/Shared/StrongNameTests.cs:6](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Shared/StrongNameTests.cs#L6) | `public static class StrongNameTests` |
| [test/Shared/StrongNameTests.cs:9](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Shared/StrongNameTests.cs#L9) | `public static void Tests_Are_Strong_Named()` |
| [test/Polly.Core.Tests/OutcomeTests.cs:3](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L3) | `public class OutcomeTests` |
| [test/Polly.Core.Tests/OutcomeTests.cs:6](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L6) | `public void Ctor_Result_Ok()` |
| [test/Polly.Core.Tests/OutcomeTests.cs:19](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L19) | `public void Ctor_VoidResult_Ok()` |
| [test/Polly.Core.Tests/OutcomeTests.cs:31](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L31) | `public void Ctor_Exception_Ok()` |
| [test/Polly.Core.Tests/OutcomeTests.cs:43](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L43) | `public void ToString_NullResult_ShouldBeEmpty()` |
| [test/Polly.Core.Tests/OutcomeTests.cs:50](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L50) | `public void EnsureSuccess_Result()` |
| [test/Polly.Core.Tests/OutcomeTests.cs:58](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L58) | `public void EnsureSuccess_Exception()` |
| [test/Polly.Core.Tests/OutcomeTests.cs:66](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L66) | `public void FromException_Throws_If_Null() =>` |
| [test/Polly.Core.Tests/OutcomeTests.cs:70](https://github.com/App-vNext/Polly/blob/3f3adad9d5af85658fc3585018f02a2d8c2173e8/test/Polly.Core.Tests/OutcomeTests.cs#L70) | `public async Task FromExceptionAsValueTask_Throws_If_Null() =>` |

Full lexical records (17) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | Pipeline and execution context | ResiliencePipeline; ExecutionContext; Outcome |
| WP-02 | Retry timeout and fallback | RetryDecision; TimeoutBudget; FallbackResult |
| WP-03 | Circuit breaker and concurrency limits | CircuitState; ProbeLease; PermitLease |
| WP-04 | Hedging and result disposal | HedgeAttempt; WinnerSelection; ResultDisposer |
| WP-05 | Telemetry adapters and deterministic tests | StrategyEvent; HttpResilienceAdapter; VirtualClock |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
