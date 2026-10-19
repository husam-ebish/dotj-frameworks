# DJ-060 .j ML: feature compatibility matrix

C# IDataView and model archives require Java contracts; numeric similarity needs tolerances and deterministic-seed policy, not bitwise promises.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Data view schemas and pipeline model | Proposed Java contracts: DataView, DataSchema, Estimator, Transformer | Estimators cannot consume unavailable second passes silently; sparse vectors preserve indices; schema mismatch fails before prediction | Planned; evidence gates open |
| WP-02 | Transforms learners and evaluation | Proposed Java contracts: TransformSpec, Trainer, Prediction, MetricSet | Known toy datasets match accepted tolerances; metric definitions include weighting/null rules; unsupported learners remain visible | Planned; evidence gates open |
| WP-03 | Model format loading and deployment | Proposed Java contracts: ModelManifest, ModelComponent, PredictionEngine | Unknown component versions fail safely; models identify training schema; concurrent prediction follows documented thread-safety | Planned; evidence gates open |
| WP-04 | Native accelerators ONNX and runtime feasibility | Proposed Java contracts: NativeBackend, OnnxProfile, DeviceCapability | No accelerator support without executable evidence; fallback does not silently change model semantics; model format support is distinct from training parity | Planned; evidence gates open |
| WP-05 | Benchmarking reproducibility and qualification | Proposed Java contracts: TrainingRun, DatasetManifest, MlCompatibilityProfile | Claims name exact algorithms and tolerances; dataset rights are recorded; existing Java ML frameworks do not replace this port | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

ONNX/TensorFlow/LightGBM or other native dependencies must be confirmed per selected module; no existing Java ML framework substitution.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
