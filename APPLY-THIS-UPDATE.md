# Historical planning-package handoff

This file describes a 19 October 2026 planning package and its original copy/commit instructions. That package is already present in this repository. For the current implementation and review status, start with [README.md](README.md) and [REVIEW.md](REVIEW.md). Do not run the historical copy or commit steps below as a setup procedure for this checkout.

# Full Stage-2 plan for .j Frameworks

**Updated owner requirement:** all 66 plans now require exact upstream .NET public names, casing and concepts. See [the mandatory policy](planning/stage-2/08-DOTNET-API-COMPATIBILITY-POLICY.md). This version supersedes the earlier Java-style naming proposals. Merge/replace the included Stage-2 files in your repository; do not modify immutable source evidence.

The complete written package covers all 66 repositories with 356 feature and integration work packages, 1,356 named tasks and 1,311 designed acceptance cases.

**New in this revision:** detailed SDK installation, exact .NET command/workflow contracts, packages/feeds, hosting, publishing, templates/tools/workloads and AI execution instructions. Start with [10-SDK-AND-DISTRIBUTION-PLAN.md](planning/stage-2/10-SDK-AND-DISTRIBUTION-PLAN.md). The existing 66 plans and immutable evidence are retained.

Open [planning/stage-2/README.md](planning/stage-2/README.md), then [07-IMPLEMENTATION-START.md](planning/stage-2/07-IMPLEMENTATION-START.md).

Copy the included `planning/stage-2` directory into your repository at `C:\source\repos\dotj Frameworks`. Merge the directory and replace matching Stage-2 files from the earlier core increment. Your existing Stage-1 plans remain in place. Review the resulting Git diff before committing. This package was not applied to your Windows repository automatically.

In PowerShell, after copying:

```powershell
Set-Location 'C:\source\repos\dotj Frameworks'
git status --short
git diff --stat
git add -- planning/stage-2
git diff --cached --stat
git commit -m "docs: specify dotnet-style SDK and distribution plan"
```

Add a link to `planning/stage-2/README.md` from your existing planning README when convenient. The archive contains no application source implementation. Rights, full source audit and native feasibility gates are explicitly marked; complete written plans do not certify every repository ready for implementation or release.
