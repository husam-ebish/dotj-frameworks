# DJ-055 .j Benchmark: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

CLR JIT/GC assumptions become JVM-specific warmup, deoptimization and dead-code risks; do not claim JMH-equivalent rigor without evidence.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Benchmark discovery and parameterization | Internal planning vocabulary (verify upstream public identity): BenchmarkCase, ParameterSet, JobConfig | All parameter combinations have stable IDs; setup is outside measured interval unless configured; failed runs publish no misleading timing | Planned; evidence gates open |
| WP-02 | Process isolation warmup and measurement | Internal planning vocabulary (verify upstream public identity): MeasurementProcess, Iteration, ClockCalibration | Reports identify JVM/CPU/OS/flags; warmup and measurement data are separate; timer overhead is measured and accounted for | Planned; evidence gates open |
| WP-03 | Statistics outliers and comparisons | Internal planning vocabulary (verify upstream public identity): SampleSet, StatisticalSummary, RatioEstimate | Recomputed summaries match raw data; outlier removal is visible; noisy comparisons are not labeled definitive wins | Planned; evidence gates open |
| WP-04 | Diagnosers profilers and native tools | Internal planning vocabulary (verify upstream public identity): Diagnoser, AllocationSample, HardwareCounterCapability | Unsupported counters are unavailable rather than zero; profiler versions are recorded; diagnostic overhead does not contaminate primary results invisibly | Planned; evidence gates open |
| WP-05 | Export configuration and regression acceptance | Internal planning vocabulary (verify upstream public identity): BenchmarkReport, Exporter, ValidationRule | No JMH framework replaces the harness; exports retain units; deterministic harness tests are separate from noisy performance expectations | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Microbenchmark validity needs dedicated methodology; CPU affinity/native counters may require optional OS bindings.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
