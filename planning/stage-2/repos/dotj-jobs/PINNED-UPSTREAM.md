# DJ-029 .j Jobs: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/HangfireIO/Hangfire |
| Effective canonical source | https://github.com/HangfireIO/Hangfire |
| Immutable analysis revision | `c35077110cc8364b06ea30d39947bd5f688b2e8b` |
| Immutable tree | [c35077110cc8364b06ea30d39947bd5f688b2e8b](https://github.com/HangfireIO/Hangfire/tree/c35077110cc8364b06ea30d39947bd5f688b2e8b) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 611 |
| New sampled source/API/test files | 4 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Hangfire.Core/Cron.cs](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Cron.cs) | `b239453715e3ebad75b37c2b176378b37023c988bf49acb1c368a9db8ae64efa` |
| [src/Hangfire.Core/JobStorage.cs](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/JobStorage.cs) | `643bc88f13d749b5c65b2853811e69d8330abe9cdf0dcad8d99cdb70dafef90f` |
| [tests/Hangfire.Core.Tests/CronFacts.cs](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/CronFacts.cs) | `19aab302ab9ee78f6260d5ffa1d904c86812dc989863edc30328e5120efe8850` |
| [tests/Hangfire.Core.Tests/JobStorageFacts.cs](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/JobStorageFacts.cs) | `a9746b79c826c623ab9696096aee646e9c2bfe531cf45803635db5d43ab555a8` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
