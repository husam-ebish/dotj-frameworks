# Selected compiled lifecycle inventory v1

Run from the repository with the retained Windows D: toolchain:

```powershell
& 'D:\AI\Implementation\dotj Frameworks\toolchains\python-3.13.9\python.exe' -B `
  tools/oracle/dotj-build/verify-lifecycle.py `
  --out 'D:\AI\Implementation\dotj Frameworks\validation\dotj-build-lifecycle-review1'
```

Use a new output directory. `capture-lifecycle.py --out <new-directory>` runs
one reproduction. The verification runner runs two captures, compares their
exact bytes, and exercises five pre-launch integrity refusals using isolated
copies plus a missing compiled-anchor mapping refusal. Every subprocess command,
stdout/stderr hash, resolved assembly identity and result stays under `--out`.
Failure writes `REFUSED`/`FAILED` evidence and exits unsuccessfully.

The reader uses the installed PowerShell 7.6.0 host with the existing
`powershell-oracle.runtimeconfig.json`: .NET 10.0.12, roll-forward disabled.
Its process-scoped execution policy permits this reviewed local script; no
machine policy is changed. The host loads the SDK's MetadataLoadContext library.
Microsoft.Build and its contracts are opened **only in MetadataLoadContext**.
Only reflection metadata operations execute; no reference constructors, methods,
application getters, project evaluation, tasks, source builds, restore or network
calls occur. `Add-Type -Path` loads the reader library; it does not compile C#.

The [lock](../../../planning/stage-2/repos/dotj-build/evidence/compiled-lifecycle-lock-v1.json)
pins producer bytes, Python, host/runtime files, the resolver universe, selected
source files and prior provenance evidence. All nine retained SDK archive-entry
hashes are checked against current installed files as well. Input verification
happens before and after the reader; every metadata-resolved assembly must belong
to the lock. Temporary/home paths, runtime settings and command line are retained.
The lock is a checked-in review anchor, not a security signature or protection
against concurrent hostile replacement of the machine's files. This tool never
regenerates it or accepts a different installed version automatically.

The [raw result](../../../planning/stage-2/repos/dotj-build/evidence/compiled-lifecycle-raw-v1.json)
is unedited reader JSON. Metadata tokens are local to its pinned image/MVID.
Source navigation is separately correlated in the
[mapping](../../../planning/stage-2/repos/dotj-build/evidence/compiled-lifecycle-mapping-v1.json),
with the generated type initializer and profile/closure gaps explicitly retained.
See the [bounded inventory](../../../planning/stage-2/repos/dotj-build/COMPILED-LIFECYCLE-INVENTORY.md).
No public facade, core substitute contract, task acceptance or product credit
is provided by this inventory. The existing internal candidate is unchanged.

## Explicit-import native observations

`capture-imports.py --out <new-D-directory>` compiles the owned development-only
CaptureImports.cs directly against the local pinned net10.0 reference pack and
SDK assemblies, then evaluates the immutable nine-case corpus under three
separately labeled load profiles. It preserves 128 MiB native heap / two CPUs,
the existing free-memory floors, 30-second command deadlines, D: temp/home/cache
paths and roll-forward disabled. No project Build, target/task execution,
restore, SDK fixture resolver or network call is used. The C# host has synchronous
logging and unloads/disposes a fresh collection after each success or failure.

`verify-imports.py <first-verification.json> <second-verification.json> --bridge
<checked-in-tsv> --out <new-D-json>` checks retained log hashes, compares all
ordered observations using the planned fixture-root-only substitution and
reconstructs the candidate comparison bridge. It retains native positions,
messages, null diagnostic codes, exceptions and cleanup. See the candidate's
[bounded import contract](../../../dotj-build/evaluation-candidate/IMPORT-BEHAVIOR.md)
for the supported observables and remaining gaps. The native SDK, Roslyn compiler,
reference pack and .NET runtime are development-only; they are not JAR runtime
dependencies. All new helper source is owned; no upstream implementation is copied.
