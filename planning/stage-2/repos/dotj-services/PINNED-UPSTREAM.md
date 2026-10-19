# DJ-018 .j Services: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/CoreWCF/CoreWCF |
| Effective canonical source | https://github.com/CoreWCF/CoreWCF |
| Immutable analysis revision | `6e2cce88349fe41056fe8afda0dbbdf98d54bb00` |
| Immutable tree | [6e2cce88349fe41056fe8afda0dbbdf98d54bb00](https://github.com/CoreWCF/CoreWCF/tree/6e2cce88349fe41056fe8afda0dbbdf98d54bb00) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 2264 |
| New sampled source/API/test files | 4 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/CoreWCF.BuildTools/src/Indentor.cs](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Indentor.cs) | `f2eb71877b6b0101a316bec111fd28433c23b780731de569fedbdefeeeaa881b` |
| [src/CoreWCF.BuildTools/src/Extensions.cs](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/Extensions.cs) | `c2564a977c261d7f250f9a3678b251395d836cf0f9bd03bb719c4f337783015f` |
| [src/CoreWCF.Http/tests/ByRefTests.cs](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.Http/tests/ByRefTests.cs) | `3a58c6c2df836d88ac42e26854e6de92bab3ae3e1edaadc3277b4944689087d9` |
| [src/CoreWCF.WebHttp/tests/SslTests.cs](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.WebHttp/tests/SslTests.cs) | `e162f3d9ae6e5c92008aa2a766057a7c0275e90956510307c739e31301887574` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
