# DJ-060 .j ML: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

C# IDataView and model archives require Java contracts; numeric similarity needs tolerances and deterministic-seed policy, not bitwise promises.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Data view schemas and pipeline model | Internal planning vocabulary (verify upstream public identity): DataView, DataSchema, Estimator, Transformer | Estimators cannot consume unavailable second passes silently; sparse vectors preserve indices; schema mismatch fails before prediction | Planned; evidence gates open |
| WP-02 | Transforms learners and evaluation | Internal planning vocabulary (verify upstream public identity): TransformSpec, Trainer, Prediction, MetricSet | Known toy datasets match accepted tolerances; metric definitions include weighting/null rules; unsupported learners remain visible | Planned; evidence gates open |
| WP-03 | Model format loading and deployment | Internal planning vocabulary (verify upstream public identity): ModelManifest, ModelComponent, PredictionEngine | Unknown component versions fail safely; models identify training schema; concurrent prediction follows documented thread-safety | Planned; evidence gates open |
| WP-04 | Native accelerators ONNX and runtime feasibility | Internal planning vocabulary (verify upstream public identity): NativeBackend, OnnxProfile, DeviceCapability | No accelerator support without executable evidence; fallback does not silently change model semantics; model format support is distinct from training parity | Planned; evidence gates open |
| WP-05 | Benchmarking reproducibility and qualification | Internal planning vocabulary (verify upstream public identity): TrainingRun, DatasetManifest, MlCompatibilityProfile | Claims name exact algorithms and tolerances; dataset rights are recorded; existing Java ML frameworks do not replace this port | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

ONNX/TensorFlow/LightGBM or other native dependencies must be confirmed per selected module; no existing Java ML framework substitution.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
