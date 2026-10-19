# DJ-056 .j Testcontainers: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/Testcontainers/Logger.cs:94](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logger.cs#L94) | Dispose | not confirmed |
| [src/Testcontainers/Logging.cs:170](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L170) | IgnorePatternAdded | not confirmed |
| [src/Testcontainers/Logging.cs:175](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L175) | DockerContainerCreated | not confirmed |
| [src/Testcontainers/Logging.cs:180](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L180) | StartDockerContainer | not confirmed |
| [src/Testcontainers/Logging.cs:185](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L185) | StopDockerContainer | not confirmed |
| [src/Testcontainers/Logging.cs:190](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L190) | PauseDockerContainer | not confirmed |
| [src/Testcontainers/Logging.cs:195](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L195) | UnpauseDockerContainer | not confirmed |
| [src/Testcontainers/Logging.cs:200](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L200) | DeleteDockerContainer | not confirmed |
| [src/Testcontainers/Logging.cs:205](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L205) | StartReadinessCheck | not confirmed |
| [src/Testcontainers/Logging.cs:210](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L210) | CompleteReadinessCheck | not confirmed |
| [src/Testcontainers/Logging.cs:215](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L215) | CopyArchiveToDockerContainer | not confirmed |
| [src/Testcontainers/Logging.cs:220](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L220) | ReadArchiveFromDockerContainer | not confirmed |
| [src/Testcontainers/Logging.cs:225](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L225) | AttachToDockerContainer | not confirmed |
| [src/Testcontainers/Logging.cs:230](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L230) | CanNotReadDockerContainerOutput | not confirmed |
| [src/Testcontainers/Logging.cs:235](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L235) | ConnectToDockerNetwork | not confirmed |
| [src/Testcontainers/Logging.cs:240](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L240) | ExecuteCommandInDockerContainer | not confirmed |
| [src/Testcontainers/Logging.cs:246](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L246) | DockerImageCreated | not confirmed |
| [src/Testcontainers/Logging.cs:251](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L251) | RetryCreateDockerImage | not confirmed |
| [src/Testcontainers/Logging.cs:256](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L256) | DockerImageBuilt | not confirmed |
| [src/Testcontainers/Logging.cs:261](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L261) | BuildDockerImage | not confirmed |
| [src/Testcontainers/Logging.cs:270](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L270) | DockerImageBuildOutput | not confirmed |
| [src/Testcontainers/Logging.cs:279](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L279) | ImageBuildParameterNotSupported | not confirmed |
| [src/Testcontainers/Logging.cs:284](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L284) | DeleteDockerImage | not confirmed |
| [src/Testcontainers/Logging.cs:289](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L289) | DockerNetworkCreated | not confirmed |
| [src/Testcontainers/Logging.cs:294](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L294) | DeleteDockerNetwork | not confirmed |
| [src/Testcontainers/Logging.cs:299](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L299) | DockerVolumeCreated | not confirmed |
| [src/Testcontainers/Logging.cs:304](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L304) | DeleteDockerVolume | not confirmed |
| [src/Testcontainers/Logging.cs:309](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L309) | DockerRuntimeInfo | not confirmed |
| [src/Testcontainers/Logging.cs:314](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L314) | AddFileToTarArchive | not confirmed |
| [src/Testcontainers/Logging.cs:319](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L319) | AddFileToTarArchive | not confirmed |
| [src/Testcontainers/Logging.cs:324](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L324) | CanNotResolveComposeServiceImages | not confirmed |
| [src/Testcontainers/Logging.cs:329](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L329) | CanNotPullComposeServiceImage | not confirmed |
| [src/Testcontainers/Logging.cs:334](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L334) | CanNotCleanUpComposeProject | not confirmed |
| [src/Testcontainers/Logging.cs:339](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L339) | CanNotGetResourceReaperEndpoint | not confirmed |
| [src/Testcontainers/Logging.cs:344](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L344) | CanNotConnectToResourceReaper | not confirmed |
| [src/Testcontainers/Logging.cs:350](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L350) | LostConnectionToResourceReaper | not confirmed |
| [src/Testcontainers/Logging.cs:356](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L356) | DockerConfigFileNotFound | not confirmed |
| [src/Testcontainers/Logging.cs:361](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L361) | SearchingDockerRegistryCredential | not confirmed |
| [src/Testcontainers/Logging.cs:366](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L366) | DockerRegistryAuthPropertyValueKindInvalid | not confirmed |
| [src/Testcontainers/Logging.cs:371](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L371) | DockerRegistryAuthPropertyValueNotFound | not confirmed |
| [src/Testcontainers/Logging.cs:376](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L376) | DockerRegistryAuthPropertyValueInvalidBase64 | not confirmed |
| [src/Testcontainers/Logging.cs:381](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L381) | DockerRegistryAuthPropertyValueInvalidBasicAuthenticationFormat | not confirmed |
| [src/Testcontainers/Logging.cs:386](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L386) | DockerRegistryCredentialNotFound | not confirmed |
| [src/Testcontainers/Logging.cs:391](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L391) | DockerRegistryCredentialFound | not confirmed |
| [src/Testcontainers/Logging.cs:396](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L396) | ReusableExperimentalFeature | not confirmed |
| [src/Testcontainers/Logging.cs:401](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L401) | ReusableResourceFound | not confirmed |
| [src/Testcontainers/Logging.cs:406](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers/Logging.cs#L406) | ReusableResourceNotFound | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-056-F01-01 | WP-01 | Unsupported engine versions fail explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F01-02 | WP-01 | registry credentials are redacted | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F01-03 | WP-01 | images used for reproducibility have immutable identity | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F02-01 | WP-02 | Failed readiness produces useful logs | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F02-02 | WP-02 | cleanup runs after partial creation | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F02-03 | WP-02 | a passing port-open check is not claimed as application readiness | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F03-01 | WP-03 | Caller-owned volumes remain | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F03-02 | WP-03 | mismatched reuse settings do not attach silently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F03-03 | WP-03 | Windows/Linux path cases are tested independently | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F04-01 | WP-04 | Cleanup never targets unlabeled foreign resources | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F04-02 | WP-04 | reaper failure is visible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F04-03 | WP-04 | remote configuration cannot silently expose daemon credentials | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F05-01 | WP-05 | Modules expose mapped endpoints only after readiness | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F05-02 | WP-05 | each image profile has evidence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-056-F05-03 | WP-05 | no existing Java Testcontainers implementation is reused | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Daemon disconnect; failed start; health timeout; port races; network cleanup; credential redaction; orphan recovery.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
