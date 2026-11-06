# Batch 2525: qualified reference toolkit checkout portability

Source feature commit: `55dfe0c168f7dff2fd7c8e170d1a94d0b5fdebf8`. Evidence: `D:\AI\Implementation\dotj Frameworks\agents\task156-toolkit-portability-v1\review-report.json` (SHA-256 `ab7a8e3e5d3275fbfc356d801b5e2dffd0ce21de400b549b302ed5cd6d749d55`). Publication is complete only after the reviewed feature is merged and master/feature remote refs are verified; the controller publication receipt records that outcome.

The existing toolkit failed before any native launch from the canonical Windows checkout because fixed LF source hashes were compared to CRLF physical files and qualified class receipt keys referenced an old absolute worktree. This feature repairs source identity and staging across checkout line endings and source-root relocation. Normalization is limited to the finite qualified source allowlist; original fixed binary, class and receipt integrity checks remain required. Historical failed preflight evidence and all raw reference captures are preserved.

Verification evidence is in the implementation report. This tooling repair adds no runtime capability or accepted implementation task. The following work starts with the two bounded strict-startup transport diagnostics, then a source-backed runtime strategy and the remaining product/packaged qualification steps. Diagnostic operations alone are not new numbered batches.

| Measure | Done | Remaining |
| --- | --- | --- |
| Numbered batches | 2525 | 75 to milestone2600 |
| Project-wide batches | Total unknown | Unknown |
| Toolkit portability feature | Complete upon verified publication | 0 after publication |
| Parent SDK process plan | 4/12 | 8 runtime/product steps |
| Accepted implementation tasks | 3/1092 (0.275%) | 1089 |
| Open acceptance items | No new closure credit | 1683 |
| Qualified frameworks | 0/66 | 66 |
| Git | Feature branch; no-ff merge and verified push required | Publication receipt records actual refs |

Product candidate: JDK APIs, no third-party Java runtime library, Maven or Gradle requirement. Development/reference tools: real D Python, pinned JDK21, SDK10.0.401/runtime10.0.12; no new download required for this fix. Broader66-framework dependency resolution and public .j installer/feed remain open.
