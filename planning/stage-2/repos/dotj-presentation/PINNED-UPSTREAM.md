# DJ-040 .j Presentation: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/wpf |
| Effective canonical source | https://github.com/dotnet/wpf |
| Immutable analysis revision | `65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9` |
| Immutable tree | [65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9](https://github.com/dotnet/wpf/tree/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 7373 |
| New sampled source/API/test files | 7 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Microsoft.DotNet.Wpf/src/PresentationCore/ref/PresentationCore.cs](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/src/PresentationCore/ref/PresentationCore.cs) | `5ec4de4a6575a96263c3aa05ccac444e7fde76337be6e3099bf4ff231b412f6a` |
| [src/Microsoft.DotNet.Wpf/src/PresentationFramework/ref/PresentationFramework.cs](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/src/PresentationFramework/ref/PresentationFramework.cs) | `0168bc28c5c8d658438f3f2bbacb6f7bf8624ff1dc307b8ad81dbb970bdc0995` |
| [src/Microsoft.DotNet.Wpf/src/System.Xaml/GlobalSuppressions.cs](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/src/System.Xaml/GlobalSuppressions.cs) | `788bdd2cac71b43aa9cd7326cb12ddc5029d27a272e396021845ebef97c5b3b1` |
| [src/Microsoft.DotNet.Wpf/src/System.Xaml/OtherAssemblyAttrs.cs](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/src/System.Xaml/OtherAssemblyAttrs.cs) | `b50f0717d687c1dc9640765886143e26840178766755077210c2845400a81b34` |
| [src/Microsoft.DotNet.Wpf/src/WindowsBase/SR.cs](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/src/WindowsBase/SR.cs) | `44cdd01445bfd8be395c3f6bb3f37050263568027236564cc6159e47fbcc8071` |
| [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationFramework.Fluent.Tests/ResourceTests/FluentResourceDictionaryTests.cs](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationFramework.Fluent.Tests/ResourceTests/FluentResourceDictionaryTests.cs) | `a239dd17e7424c3fdf552bda97a21493c80d340fd3a0baed8554fd010093c733` |
| [src/Microsoft.DotNet.Wpf/tests/UnitTests/WindowsBase.Tests/System/Windows/RectTests.cs](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/WindowsBase.Tests/System/Windows/RectTests.cs) | `7a19ae735df2ad8d0517e0a841a4dda6be45c978e3f59da2dd501c5fba8bf50c` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
