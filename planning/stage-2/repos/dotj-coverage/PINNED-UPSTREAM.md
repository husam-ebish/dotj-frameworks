# DJ-054 .j Coverage: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/coverlet-coverage/coverlet |
| Effective canonical source | https://github.com/coverlet-coverage/coverlet |
| Immutable analysis revision | `b5ba9197f032e22627836d899aa3956a50cd5017` |
| Immutable tree | [b5ba9197f032e22627836d899aa3956a50cd5017](https://github.com/coverlet-coverage/coverlet/tree/b5ba9197f032e22627836d899aa3956a50cd5017) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 483 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/coverlet.console/Program.cs](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/src/coverlet.console/Program.cs) | `40cdf3b06b8f90d3fc1560c155b3d176ef50927c2a36ec9a68a7e9454143983a` |
| [src/coverlet.console/ExitCodes.cs](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/src/coverlet.console/ExitCodes.cs) | `fecee199457cdc547a9bf666eb9df47d5b74b58c4eb1a5980fc31511f1e79a09` |
| [src/coverlet.core/Coverage.cs](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/src/coverlet.core/Coverage.cs) | `a49b28b67ec5a1c994c33399661257fc8f055c6a742f1b638e74213afdb214f6` |
| [test/coverlet.core.tests/CoverageResultTests.cs](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/test/coverlet.core.tests/CoverageResultTests.cs) | `7d6277134bff86a4947271b32a011554e2ad82126871e4f65a0fd9ecc57f17ea` |
| [test/coverlet.integration.tests/WpfResolverTests.cs](https://github.com/coverlet-coverage/coverlet/blob/b5ba9197f032e22627836d899aa3956a50cd5017/test/coverlet.integration.tests/WpfResolverTests.cs) | `bfc30ce558bbcd136773952a629aa94a2d16d3c47bd13bdc701bdfc27cbd4368` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
