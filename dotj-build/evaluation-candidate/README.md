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

The suite compares 20 existing same-input Windows native observations with the
live candidate: 19 property pairs and one missing-import code/path. Another 23
cases verify explicit candidate-profile refusals. The candidate is compiled
separately and loaded from its JAR; the suite checks that runtime location and
the module's lack of exports/opens. The existing dotj-core queue is independent
and is not needed or invoked.

Runtime dependencies are JDK `java.base` and `java.xml`; the JVM runs with those
modules plus this candidate module. Python and javac are development tools.
There are no third-party Java libraries or dotj-core binary dependencies.
No product license/distribution choice is made here; the owned predecessor
proposal is reused internally, and no upstream implementation is copied.

See [CONTRACT.md](CONTRACT.md) for the exact supported/refused profile,
normalization and remaining acceptance work.
