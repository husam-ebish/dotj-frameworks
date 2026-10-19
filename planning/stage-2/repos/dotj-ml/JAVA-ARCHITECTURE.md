# DJ-060 .j ML: Java architecture and contracts

Reproduce data pipelines, transformations, training, inference and model persistence.

Product type: JVM/native ML framework. Proposed Java package root: `org.dotj.ml`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-ml-01 | DataView, DataSchema, Estimator, Transformer | Data view schemas and pipeline model |
| dotj-ml-02 | TransformSpec, Trainer, Prediction, MetricSet | Transforms learners and evaluation |
| dotj-ml-03 | ModelManifest, ModelComponent, PredictionEngine | Model format loading and deployment |
| dotj-ml-04 | NativeBackend, OnnxProfile, DeviceCapability | Native accelerators ONNX and runtime feasibility |
| dotj-ml-05 | TrainingRun, DatasetManifest, MlCompatibilityProfile | Benchmarking reproducibility and qualification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

C# IDataView and model archives require Java contracts; numeric similarity needs tolerances and deterministic-seed policy, not bitwise promises.

## Feature contracts and invariants

### WP-01: Data view schemas and pipeline model

Contract vocabulary: `DataView`, `DataSchema`, `Estimator`, `Transformer`.

Define row cursors column types vector sparsity and missing values. Specify fit/transform separation and schema propagation. Support replayable and one-pass data sources explicitly.

Required observable invariant: Estimators cannot consume unavailable second passes silently; sparse vectors preserve indices; schema mismatch fails before prediction.

### WP-02: Transforms learners and evaluation

Contract vocabulary: `TransformSpec`, `Trainer`, `Prediction`, `MetricSet`.

Inventory trainer/transform/evaluator families individually. Define deterministic seed and floating-point policies. Implement reference algorithms before optimization.

Required observable invariant: Known toy datasets match accepted tolerances; metric definitions include weighting/null rules; unsupported learners remain visible.

### WP-03: Model format loading and deployment

Contract vocabulary: `ModelManifest`, `ModelComponent`, `PredictionEngine`.

Version serialized components and dependencies. Reject unsafe type activation from model files. Separate batch streaming and low-latency prediction ownership.

Required observable invariant: Unknown component versions fail safely; models identify training schema; concurrent prediction follows documented thread-safety.

### WP-04: Native accelerators ONNX and runtime feasibility

Contract vocabulary: `NativeBackend`, `OnnxProfile`, `DeviceCapability`.

Inventory native math TensorFlow/ONNX and platform dependencies. Choose narrow bindings only after ownership/license review. Define CPU fallback and supported architecture matrix.

Required observable invariant: No accelerator support without executable evidence; fallback does not silently change model semantics; model format support is distinct from training parity.

### WP-05: Benchmarking reproducibility and qualification

Contract vocabulary: `TrainingRun`, `DatasetManifest`, `MlCompatibilityProfile`.

Port data/transform/trainer/regression tests by family. Record dataset provenance seeds hardware and precision. Test corrupted models resource limits and reproducibility.

Required observable invariant: Claims name exact algorithms and tolerances; dataset rights are recorded; existing Java ML frameworks do not replace this port.

## Bootstrap and dependency boundaries

Arrays/buffers, concurrency and optional FFM/JNI bindings to identified native engines.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing ML.NET usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `DataView` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Estimators cannot consume unavailable second passes silently; sparse vectors preserve indices; schema mismatch fails before prediction. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
