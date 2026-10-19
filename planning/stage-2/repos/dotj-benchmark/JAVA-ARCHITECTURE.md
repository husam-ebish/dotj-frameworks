# DJ-055 .j Benchmark: Java architecture and contracts

Provide isolated benchmark execution, parameterization, statistics and diagnostics.

Product type: JVM performance tool. Proposed Java package root: `org.dotj.benchmark`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-benchmark-01 | BenchmarkCase, ParameterSet, JobConfig | Benchmark discovery and parameterization |
| dotj-benchmark-02 | MeasurementProcess, Iteration, ClockCalibration | Process isolation warmup and measurement |
| dotj-benchmark-03 | SampleSet, StatisticalSummary, RatioEstimate | Statistics outliers and comparisons |
| dotj-benchmark-04 | Diagnoser, AllocationSample, HardwareCounterCapability | Diagnosers profilers and native tools |
| dotj-benchmark-05 | BenchmarkReport, Exporter, ValidationRule | Export configuration and regression acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

CLR JIT/GC assumptions become JVM-specific warmup, deoptimization and dead-code risks; do not claim JMH-equivalent rigor without evidence.

## Feature contracts and invariants

### WP-01: Benchmark discovery and parameterization

Contract vocabulary: `BenchmarkCase`, `ParameterSet`, `JobConfig`.

Map benchmark annotations parameters setup/cleanup and baselines. Generate deterministic workload harnesses. Separate benchmark errors from measurement results.

Required observable invariant: All parameter combinations have stable IDs; setup is outside measured interval unless configured; failed runs publish no misleading timing.

### WP-02: Process isolation warmup and measurement

Contract vocabulary: `MeasurementProcess`, `Iteration`, `ClockCalibration`.

Fork controlled JVMs with recorded flags/toolchains. Define warmup pilot workload and iteration policies. Prevent dead-code elimination through explicit result consumption.

Required observable invariant: Reports identify JVM/CPU/OS/flags; warmup and measurement data are separate; timer overhead is measured and accounted for.

### WP-03: Statistics outliers and comparisons

Contract vocabulary: `SampleSet`, `StatisticalSummary`, `RatioEstimate`.

Define aggregation confidence intervals and outlier policy. Retain raw observations for reproducibility. Avoid unsupported causal or significance claims.

Required observable invariant: Recomputed summaries match raw data; outlier removal is visible; noisy comparisons are not labeled definitive wins.

### WP-04: Diagnosers profilers and native tools

Contract vocabulary: `Diagnoser`, `AllocationSample`, `HardwareCounterCapability`.

Use JFR/JMX/JVMTI through explicit optional adapters. Gate disassembly counters and profiler dependencies per platform. Separate diagnostic runs from timing runs when perturbing.

Required observable invariant: Unsupported counters are unavailable rather than zero; profiler versions are recorded; diagnostic overhead does not contaminate primary results invisibly.

### WP-05: Export configuration and regression acceptance

Contract vocabulary: `BenchmarkReport`, `Exporter`, `ValidationRule`.

Emit machine-readable raw and summarized results. Validate benchmark configuration and suspicious harness patterns. Port discovery/config/export regressions and controlled synthetic experiments.

Required observable invariant: No JMH framework replaces the harness; exports retain units; deterministic harness tests are separate from noisy performance expectations.

## Bootstrap and dependency boundaries

ProcessBuilder, System.nanoTime, JFR and management APIs.

Proposed .j dependencies: core;diagnostics(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing BenchmarkDotNet usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `BenchmarkCase` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: All parameter combinations have stable IDs; setup is outside measured interval unless configured; failed runs publish no misleading timing. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
