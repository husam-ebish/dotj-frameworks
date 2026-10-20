# Ownership failure policy for the first core slice

Status: **bounded decision, 2026-10-20**. Applies to the pinned .NET 10.0.12 DI scope example and the internal Java `OwnedResources` helper. It does not qualify a public .j API.

| Path | Observed or implemented behavior | Evidence |
|---|---|---|
| Pinned DI `ServiceProviderEngineScope.Dispose` | Captured resources close in reverse order. A thrown synchronous `Dispose` exception stops the loop, leaving earlier resources unclosed. An async-only object reached by this loop causes `InvalidOperationException`. | [Source windows](evidence/di-disposal-source-v10.0.12.json) and [independent executable oracle](evidence/di-disposal-oracle-v10.0.12.json). |
| DI supplied singleton instance | Provider disposal does not close the supplied singleton in the selected test and oracle. | Same evidence; upstream `SingletonServiceCreatedFromInstanceIsNotDisposedWhenContainerIsDisposed` is source-inspected, not executed here. |
| Internal Java `OwnedResources.close` | Closes each owned identity in reverse order, continues after `Exception`, throws the first observed exception and suppresses later ones. Borrowed resources remain caller-owned. | `OwnedResourcesTest` and `CallerOwnershipTest`; these are direct Java tests. |

The Java helper's continue-and-suppress policy is an **internal adaptation**. It is not a port of the DI scope's failure path. A later DI-specific compatibility implementation must use the verified fail-fast policy and its own oracle fixtures. The source method `CaptureDisposable` lists captured objects without a visible identity check, so identity deduplication cannot be attributed to that method; registration and caching paths need separate analysis.

The pinned source also has a special late-capture path after the scope has already been disposed that synchronously waits for an async-only object's disposal. This differs from the ordinary `Dispose` loop's async-only error and needs a separate fixture before any whole-scope async rule is stated. No exact `IAsyncDisposable` Java facade is approved while `ValueTask` mapping remains open.
