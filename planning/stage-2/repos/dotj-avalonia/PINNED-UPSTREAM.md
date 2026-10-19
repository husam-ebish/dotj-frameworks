# DJ-043 .j Avalonia: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/AvaloniaUI/Avalonia |
| Effective canonical source | https://github.com/AvaloniaUI/Avalonia |
| Immutable analysis revision | `66b7273b9a2b5ba8416feb4376b9cdc3078b8573` |
| Immutable tree | [66b7273b9a2b5ba8416feb4376b9cdc3078b8573](https://github.com/AvaloniaUI/Avalonia/tree/66b7273b9a2b5ba8416feb4376b9cdc3078b8573) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 5928 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Android/Avalonia.Android/Stubs.cs](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/src/Android/Avalonia.Android/Stubs.cs) | `176866261e0b3797a2975c7d0921c6f264716b01d05a1de0365cd359397cf96c` |
| [src/Android/Avalonia.Android/AvaloniaView.cs](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/src/Android/Avalonia.Android/AvaloniaView.cs) | `a2987d3ac9f853432ce1b61bb5cb49af006d0d8a428f692702e14208b00f3122` |
| [nukebuild/Build.cs](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/nukebuild/Build.cs) | `01a84677f2f6074c86a4805e7a9204fdf1ab32946f3228c7648ea0640e007ce3` |
| [tests/Avalonia.LeakTests/ControlTests.cs](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs) | `7b83eb123e8f974b55be3c6f73450e0fd37612dcce44389c6e58d525b99e94d0` |
| [tests/Avalonia.Base.UnitTests/RectTests.cs](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.Base.UnitTests/RectTests.cs) | `aa1ce0f1c1aa9328c655070c6f11b2cef9a210c58f4833135dd258a7e6e1f0b1` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
