# DJ-041 .j Forms: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/winforms |
| Effective canonical source | https://github.com/dotnet/winforms |
| Immutable analysis revision | `c4891de0851184dcbe95d16ca543969fe2540245` |
| Immutable tree | [c4891de0851184dcbe95d16ca543969fe2540245](https://github.com/dotnet/winforms/tree/c4891de0851184dcbe95d16ca543969fe2540245) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 6147 |
| New sampled source/API/test files | 6 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Microsoft.VisualBasic.Forms/src/PublicAPI.Shipped.txt](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/Microsoft.VisualBasic.Forms/src/PublicAPI.Shipped.txt) | `bc400d50a3a75c32e46a0c6320f4abff73fe273591682d290c0fde6af798ec43` |
| [src/System.Windows.Forms.Design/src/PublicAPI.Shipped.txt](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/System.Windows.Forms.Design/src/PublicAPI.Shipped.txt) | `5e725901e37b8870263b98a63ab0ea294fdcbca033edfce5de6849d87f06bc6e` |
| [src/System.Windows.Forms/GlobalSuppressions.cs](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/System.Windows.Forms/GlobalSuppressions.cs) | `37bd81e62157473e38c3528f24267830faad570e30d7f7574dc7575e4f50599b` |
| [src/System.Windows.Forms/SRCategoryAttribute.cs](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/System.Windows.Forms/SRCategoryAttribute.cs) | `b7d35dee46c927a99c12ab8d691f1bf8c6487c85e0aa46e50b139f9c41a0de32` |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs) | `c3ccd13cc9db7f7ec1e9c52517b1fc237eeb5a75addfdba3e9eb10a598fc05e6` |
| [src/test/integration/UIIntegrationTests/MDITests.cs](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/UIIntegrationTests/MDITests.cs) | `97d196d68b2e3cd593c46f441b76e3451a997cd1b7c087d438b466f9860c12c9` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
