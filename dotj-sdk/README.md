# dotj evaluation SDK seed

This source seed builds the unreleased `0.1.100-dev.1` evaluation SDK with the
locked Microsoft OpenJDK 21.0.12.1+1 installation and the operating system shell.
It needs no installed dotj, Git, Python, .NET, Maven, Gradle, or dotj-core JAR.
The JDK is an external prerequisite; no toolchain is downloaded or bundled.

On Windows PowerShell 5.1, set `JAVA_HOME` to the qualified Windows x64 JDK and
choose an absolute output directory outside this source tree whose parent already exists:

```powershell
$env:JAVA_HOME = 'D:\tools\jdk-21.0.12.1+1'
& .\dotj-sdk\seed\build.ps1 -Output 'D:\sdk builds\evaluation'
& 'D:\sdk builds\evaluation\dotj.ps1' --info
& 'D:\sdk builds\evaluation\dotj.ps1' msbuild 'D:\projects\sample.proj' '-getProperty:Probe'
```

On the qualified Linux x64 UTF-8 profile:

```sh
export JAVA_HOME=/opt/jdk-21.0.12.1+1
export LANG=C.UTF-8 LC_ALL=C.UTF-8
sh dotj-sdk/seed/build.sh '/work/sdk builds/evaluation'
sh '/work/sdk builds/evaluation/dotj' --info
sh '/work/sdk builds/evaluation/dotj' msbuild /work/sample.proj '-getProperty:Probe'
```

An admitted project can be as small as:

```xml
<Project><PropertyGroup><Probe>hello</Probe></PropertyGroup></Project>
```

One queried name prints its value and a newline; multiple names separated by
`;` or `,` print a `Properties` JSON object. `-p:Probe=value` overrides a property;
repeat overrides use the last case-insensitive name. Empty values are preserved.
Help lists the evaluation-only scope. Targets, build, restore, compilation,
SDK-style projects, implicit discovery, response files, and SDK selection are
explicitly unsupported. An unexecuted task declaration is an admission gap,
even where native MSBuild accepts its evaluation without running the task.

The launcher finds its own SDK independently of the caller's directory. Moving
the complete SDK directory preserves its identity. `DOTJ_ROOT` must be absent
or match that root. Encountering `global.json` in caller or project ancestors
is refused. Symlink/reparse aliases for entrypoints, SDK, source, output, and
JDK roots are refused. The launcher validates the selected full JDK and payload;
it does not search PATH or choose another installation.

Windows `JAVA_HOME` is limited to printable ASCII paths, including spaces and
shell metacharacters: this pinned native Java launcher cannot load its runtime
from the tested non-ASCII installation path. Source, SDK, project paths and
arguments support tested Unicode. Private UTF-8 transport preserves arguments
without changing the caller's codepage, location, or console encoding. Its
complete encoded Windows command is limited to 30000 UTF-16 units before process
creation. The common semantic bounds are 256 arguments, 32768 UTF-16 units,
64 queried names and 64 property override tokens. Other Linux locales remain
unqualified.

The seed compiles Bootstrap in memory through Java source launch, then validates
all declared inputs before product staging. It uses in-process `javac` and `jar`
providers, exactly seven staged source files, an empty classpath, disabled
processors, and fixed JAR timestamps. Retained `.dotj-stage-*` directories are
diagnostic evidence. Successful publication uses immutable version directories
and an atomic `current` pointer; prior usable payloads survive the tested
compiler failure and controlled interruption. A changed stable launcher requires
a fresh output directory. This is not an arbitrary-child process ownership or
SDK-driven self-rebuild implementation.

Qualification and source/native decisions are recorded in
[`tools/oracle/dotj-sdk/seed-v1`](../tools/oracle/dotj-sdk/seed-v1) and the
[Batch 2523 record](../planning/stage-2/implementation/batches/Batch-2523.md).
Windows functional checks ran without network isolation; the Windows offline
facet and public release/distribution remain unqualified. No framework or
accepted-task count changes follow automatically from these results.
