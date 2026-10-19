# DJ-060 .j ML: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/Microsoft.ML.Tests/ImagesTests.cs:29](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L29) | TestEstimatorChain | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:60](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L60) | TestEstimatorSaveLoad | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:104](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L104) | TestLoadImages | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:136](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L136) | TestSaveImages | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:171](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L171) | TestGrayscaleTransformImages | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:230](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L230) | TestGrayScaleInMemory | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:330](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L330) | TestBackAndForthConversionWithAlphaInterleave | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:405](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L405) | TestBackAndForthConversionWithoutAlphaInterleave | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:481](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L481) | TestBackAndForthConversionWithDifferentOrder | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:556](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L556) | TestBackAndForthConversionWithAlphaNoInterleave | not confirmed |
| [test/Microsoft.ML.Tests/ImagesTests.cs:631](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L631) | TestBackAndForthConversionWithoutAlphaNoInterleave | not confirmed |
| [test/Microsoft.ML.Tests/ImagesTests.cs:706](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L706) | TestBackAndForthConversionWithAlphaInterleaveNoOffset | not confirmed |
| [test/Microsoft.ML.Tests/ImagesTests.cs:782](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L782) | TestBackAndForthConversionWithoutAlphaInterleaveNoOffset | not confirmed |
| [test/Microsoft.ML.Tests/ImagesTests.cs:857](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L857) | TestBackAndForthConversionWithAlphaNoInterleaveNoOffset | not confirmed |
| [test/Microsoft.ML.Tests/ImagesTests.cs:933](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L933) | TestBackAndForthConversionWithoutAlphaNoInterleaveNoOffset | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:1007](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L1007) | ImageResizerTransformResizingModeFill | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:1083](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L1083) | TestConvertToImage | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:1175](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L1175) | ResizeInMemoryImages | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:1230](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L1230) | MLImageCreationTests | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:1262](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L1262) | MLImageCreateThrowingTest | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:1277](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L1277) | MLImageSaveTests | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:1307](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L1307) | MLImageDisposingTest | yes |
| [test/Microsoft.ML.Tests/ImagesTests.cs:1330](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/ImagesTests.cs#L1330) | MLImageSourceDisposingTest | yes |
| [test/Microsoft.ML.Tests/CachingTests.cs:41](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/CachingTests.cs#L41) | CacheCheckpointTest | yes |
| [test/Microsoft.ML.Tests/CachingTests.cs:65](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/CachingTests.cs#L65) | CacheOnEmptyEstimatorChainTest | yes |
| [test/Microsoft.ML.Tests/CachingTests.cs:81](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Tests/CachingTests.cs#L81) | CacheTest | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-060-F01-01 | WP-01 | Estimators cannot consume unavailable second passes silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F01-02 | WP-01 | sparse vectors preserve indices | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F01-03 | WP-01 | schema mismatch fails before prediction | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F02-01 | WP-02 | Known toy datasets match accepted tolerances | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F02-02 | WP-02 | metric definitions include weighting/null rules | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F02-03 | WP-02 | unsupported learners remain visible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F03-01 | WP-03 | Unknown component versions fail safely | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F03-02 | WP-03 | models identify training schema | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F03-03 | WP-03 | concurrent prediction follows documented thread-safety | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F04-01 | WP-04 | No accelerator support without executable evidence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F04-02 | WP-04 | fallback does not silently change model semantics | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F04-03 | WP-04 | model format support is distinct from training parity | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F05-01 | WP-05 | Claims name exact algorithms and tolerances | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F05-02 | WP-05 | dataset rights are recorded | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-060-F05-03 | WP-05 | existing Java ML frameworks do not replace this port | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Data cursor semantics; missing values; reproducibility; numeric tolerances; serialized model compatibility; native memory leaks.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
