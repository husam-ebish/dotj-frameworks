# DJ-052 .j Mock: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/devlooped/moq |
| Effective canonical source | https://github.com/devlooped/moq |
| Immutable analysis revision | `bdf16e758e8022c40cef2bfd025181f845bbd2a9` |
| Immutable tree | [bdf16e758e8022c40cef2bfd025181f845bbd2a9](https://github.com/devlooped/moq/tree/bdf16e758e8022c40cef2bfd025181f845bbd2a9) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 244 |
| New sampled source/API/test files | 4 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Moq/Arg.cs](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Arg.cs) | `45cdc8990247693d2c2c7842a08268b8de8eb5d7f2cc62364d760b99aeaa2ca9` |
| [src/Moq/IMock.cs](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/IMock.cs) | `5900786c5223b60130b1bdcc59532ce10a8d801495ce2454f3ad2b2b4b3a94a2` |
| [src/Moq.Tests/MoqTests.cs](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MoqTests.cs) | `af5ffe81dcf57ceacbb6e7562f838bfbab92bc6bf2f3d5ba725daa2c9b4bdc69` |
| [src/Moq.Tests/MockTests.cs](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.Tests/MockTests.cs) | `48806a9ac5928b39e681eabd5441cd541aa6cd3c8418e43cff0c174caf70b37b` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
