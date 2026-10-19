# DJ-014 .j Proxy: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/Kubernetes.Tests/ReconcilerTests.cs:34](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Kubernetes.Tests/ReconcilerTests.cs#L34) | ReconcilerDoesNotStopOnInvalidIngress | yes |
| [test/Application.Tests/SpaFallbackTests.cs:18](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L18) | ConfigureConfiguration | not confirmed |
| [test/Application.Tests/SpaFallbackTests.cs:23](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L23) | Configure | not confirmed |
| [test/Application.Tests/SpaFallbackTests.cs:33](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L33) | Configure | not confirmed |
| [test/Application.Tests/SpaFallbackTests.cs:79](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L79) | SpaFallback_ReturnsIndexHtml_ForUnknownRoutes | yes |
| [test/Application.Tests/SpaFallbackTests.cs:92](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L92) | SpaFallback_ReturnsIndexHtml_ForDeepNestedRoutes | yes |
| [test/Application.Tests/SpaFallbackTests.cs:105](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L105) | SpaFallback_Returns404_ForMissingFileExtensions | yes |
| [test/Application.Tests/SpaFallbackTests.cs:119](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L119) | SpaFallback_ServesStaticFiles_Directly | yes |
| [test/Application.Tests/SpaFallbackTests.cs:132](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L132) | SpaFallback_DefaultDocument_ServesIndexHtml_AtRoot | yes |
| [test/Application.Tests/SpaFallbackTests.cs:146](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L146) | SpaFallback_Disabled_Returns404_ForUnknownRoutes | yes |
| [test/Application.Tests/SpaFallbackTests.cs:161](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L161) | SpaFallback_Disabled_StillServesStaticFiles | yes |
| [test/Application.Tests/SpaFallbackTests.cs:178](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L178) | StaticFiles_Disabled_Returns404_ForAll | yes |
| [test/Application.Tests/SpaFallbackTests.cs:193](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L193) | SpaFallback_CoexistsWithSpecificYarpRoutes | yes |
| [test/Application.Tests/SpaFallbackTests.cs:218](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L218) | SpaFallback_CatchAllYarpRoute_WinsOverFallback | yes |
| [test/Application.Tests/SpaFallbackTests.cs:240](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L240) | ObjectModel_StaticFilesAndFallback | yes |
| [test/Application.Tests/SpaFallbackTests.cs:259](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L259) | ObjectModel_StaticFilesWithoutFallback | yes |
| [test/Application.Tests/SpaFallbackTests.cs:275](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L275) | ObjectModel_CustomFallbackPath | yes |
| [test/Application.Tests/SpaFallbackTests.cs:291](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/SpaFallbackTests.cs#L291) | ObjectModel_EverythingDisabled | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-014-F01-01 | WP-01 | Invalid reload preserves last good snapshot | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F01-02 | WP-01 | each request sees one revision | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F01-03 | WP-01 | removed backends stop receiving new work | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F02-01 | WP-02 | Request/response bodies are not fully buffered by default | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F02-02 | WP-02 | smuggling cases are rejected | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F02-03 | WP-02 | tunnel disconnect closes both owned halves | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F03-01 | WP-03 | Unhealthy destinations are excluded as configured | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F03-02 | WP-03 | stale affinity cannot cross clusters | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F03-03 | WP-03 | health flapping obeys explicit recovery policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F04-01 | WP-04 | Non-replayable requests are not silently retried | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F04-02 | WP-04 | cancellation stops all attempts | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F04-03 | WP-04 | untrusted forwarded headers cannot change authenticated origin | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F05-01 | WP-05 | Each advertised forwarding feature has wire evidence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F05-02 | WP-05 | active drain has a bounded outcome | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-014-F05-03 | WP-05 | diagnostic labels do not contain unbounded URLs | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Request smuggling; hop-by-hop headers; slow clients; retry safety; health flapping; streaming backpressure.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
