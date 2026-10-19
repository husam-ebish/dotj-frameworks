# DJ-042 .j MultiUI: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/maui |
| Effective canonical source | https://github.com/dotnet/maui |
| Immutable analysis revision | `3a7d72870b9c2ed006de7268a6257ae039cb7f99` |
| Immutable tree | [3a7d72870b9c2ed006de7268a6257ae039cb7f99](https://github.com/dotnet/maui/tree/3a7d72870b9c2ed006de7268a6257ae039cb7f99) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 26423 |
| New sampled source/API/test files | 6 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/BlazorWebView/src/Maui/PublicAPI/net-android/PublicAPI.Shipped.txt](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/BlazorWebView/src/Maui/PublicAPI/net-android/PublicAPI.Shipped.txt) | `55b4711dff6ee12c2f658c16a724ab22453d6d87b7637f4eb66556662adaccdf` |
| [src/BlazorWebView/src/Maui/PublicAPI/net-ios/PublicAPI.Shipped.txt](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/BlazorWebView/src/Maui/PublicAPI/net-ios/PublicAPI.Shipped.txt) | `a10bfaea27f1691624c0e652b4e3b2933c2fcc92b01425b664687f3a3ba3ba05` |
| [src/Core/src/IFlyout.cs](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/IFlyout.cs) | `99ccbe779c1f12fc7ebaaf70fe2c334136c4e5fe014424113a12a654a7551a87` |
| [src/Core/src/WeakList.cs](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/WeakList.cs) | `7d5d2ea1c931d7f4a5c781f57b30098b3cf067334ae8bb9acb6b0da333634781` |
| [src/Core/tests/UnitTests/BrushTests.cs](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/tests/UnitTests/BrushTests.cs) | `3908f829cea12a366e8b0d2046513ad897970d5edf1d885924a8b4be72d6c1a2` |
| [src/Core/tests/UnitTests/PaintTests.cs](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/tests/UnitTests/PaintTests.cs) | `4724c80b88b10a97c709b88d10a303f692b44197f10407f07ff83fbe474ec67c` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
