# DJ-009 .j Scaffold: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/Scaffolding |
| Effective canonical source | https://github.com/dotnet/Scaffolding |
| Immutable analysis revision | `107111c945bcf1264c035457a0744318b6bae3d9` |
| Immutable tree | [107111c945bcf1264c035457a0744318b6bae3d9](https://github.com/dotnet/Scaffolding/tree/107111c945bcf1264c035457a0744318b6bae3d9) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 4016 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/MSIdentityScaffolding/dotnet-msidentity/Program.cs](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/dotnet-msidentity/Program.cs) | `879db98ad0852d6f1701105285b3b60b4343ec661af327d3fc29d651842c9173` |
| [src/MSIdentityScaffolding/dotnet-msidentity/MsAADToolFactory.cs](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/dotnet-msidentity/MsAADToolFactory.cs) | `4f29153928a74edd05ead419bd8cc9c85027a0d6667379f347373c3314603677` |
| [src/Scaffolding/VS.Web.CG.Mvc/Constants.cs](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/Scaffolding/VS.Web.CG.Mvc/Constants.cs) | `1f8d3aa21cd35cc3a15e02234c6c26445ba380f1745bd143f3a38f864a7603d1` |
| [test/Scaffolding/E2E_Test/MinimalApiTests.cs](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/test/Scaffolding/E2E_Test/MinimalApiTests.cs) | `9681213e7062137ce4a96a1326509e3727a312656d812ad3ca38916ffea82d72` |
| [test/Scaffolding/E2E_Test/ViewGeneratorTests.cs](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/test/Scaffolding/E2E_Test/ViewGeneratorTests.cs) | `9f1bc5d63f899d7879fff69707c7ffd2fa8ff5e00e342a0915e58f8b63d6c643` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
