# Internal project evaluation candidate

This is a checked-in, executable prerequisite for a bounded part of
`DJ-005-WP-01-T1`. It is **not a supported Microsoft.Build API or qualified
dotj-build product**. It adds no accepted task or numbered batch credit.

The module `org.dotj.build.evaluation.candidate` has no exports or opens.
Its package-private implementation lives under `org.dotj.internal.*`. Tests
patch that module solely to exercise the packaged candidate JAR. No public
`ProjectModel`, `PropertyBag`, `Project`, core, Task or cancellation stub is
introduced. Public promotion remains blocked by the source/API/eligibility
work in [prerequisites.json](prerequisites.json).

Run the complete candidate suite with the existing pinned Windows toolchain:

```powershell
& 'D:\AI\Implementation\dotj Frameworks\toolchains\python-3.13.9\python.exe' `
  'dotj-build\evaluation-candidate\verify.py' `
  --out 'D:\AI\Implementation\dotj Frameworks\validation\dotj-build-evaluation-review1'
```

Use a new output directory on each invocation. `verify.py` verifies the locked
reference reports, selected source files, native logs, original fixtures and
toolchain before launching Java. It retains exact commands, resource checks,
stdout/stderr hashes, source hashes, JAR hashes and case results in the private
output directory. A resource deferral exits unsuccessfully and preserves its
reason; it does not lower the existing memory floors. No native MSBuild command
is executed by this runner.

Schedule qualification when the host can spare at least 524288 KiB physical
and 16777216 KiB virtual memory. Before each command the runner checks both
floors immediately, with a 120-second monotonic eligibility deadline for each
command. Five seconds is the target interval between poll starts: queries and
evidence writes consume that interval, with no added sleep once they consume
five seconds. Each OS query retains its 20-second cap, limited by the remaining
eligibility budget. OS and filesystem latency may delay readings or return;
the runner rechecks the same deadline after evidence writes and immediately
before launching, so expiry cannot authorize a late command. `resources` retains
every reading and elapsed wait; `resourceWaits` records each command's wait
outcome. Expiry records `DEFERRED_RESOURCES` and `deferredBefore` without
launching that command. Failed or malformed queries record
`RESOURCE_QUERY_FAILED` with diagnostics and stop immediately. Waiting is
separate from each command's unchanged 120-second execution timeout; launched
commands are never retried. Keep each failed run and use a new output directory
when rescheduling. JVM limits remain 128 MiB heap, two processors and SerialGC.

Python-only resource tests can run with `python -B -m unittest discover -s
dotj-build/evaluation-candidate -p test_resource_guard.py -v`. They enforce a
new private directory below the Windows D: project validation root, retain case
artifacts there, and record effective temporary and bytecode paths in
`environment.json`. Real Python children also disable bytecode writes.

The suite compares 20 existing same-input Windows native observations with the
live candidate: 19 property pairs and one missing-import code/path. The prior 23
refusal inputs remain byte-identical: 21 still refuse, and the duplicate and cycle
inputs now compare captured Default once-only behavior. Nine additional import cases bring
the legacy suite to 52 cases, including three supported selected Default cycles. See
[IMPORT-BEHAVIOR.md](IMPORT-BEHAVIOR.md) for native profile and diagnostic limits. The candidate is compiled
separately and loaded from its JAR; the suite checks that runtime location and
the module's lack of exports/opens. The existing dotj-core queue is independent
and is not needed or invoked.

Runtime dependencies are JDK `java.base` and `java.xml`; the JVM runs with those
modules plus this candidate module. Python and javac are development tools. The separate native capture tool uses
the installed .NET 10.0.12 runtime, SDK 10.0.401 local toolset/reference pack and
Roslyn compiler; these are development-only inputs and are not JAR dependencies.
There are no third-party Java libraries or dotj-core binary dependencies.
No product license/distribution choice is made here; the owned predecessor
proposal is reused internally, and no upstream implementation is copied.

See [CONTRACT.md](CONTRACT.md) for the exact supported/refused profile,
normalization and remaining acceptance work.

The [source-location extension](IMPORT-LOCATIONS.md) adds ten internal location
comparisons after the 52-case legacy suite. Use `--focus-locations` for the
focused packaged comparison. The [Default-cycle extension](IMPORT-DEFAULT-CYCLES.md)
adds three same-input cycle context comparisons; use `--focus-cycles` for those.
The default verifier runs all 52 + 10 + 3 comparisons.
