# Owned process contract v1

OP01 freezes internal semantics and expected evidence before native producers or
product code. It does not implement the helper or qualify SDK-I02-T4/F02/F04.
The binding full task/case wording is in `contract.json`; source hashes, line
anchors, rights and consumed prerequisites are in `source-map.json`. Exact case,
row, source/dependency/output and negative-control inventories are in
`fixtures.json`. No native SDK, Java, Docker or network capture ran in OP01.

All direct Process instances, including in-flight starts, must be owned and
joined. Cancellation of waiting is not killing. Descendant enumeration is an
observation, not containment; escaped descendants and forced parent death remain
unqualified. SDK diagnostics must redact the real synthetic argv/env/stdin and
failure fixtures. Raw child data, JDK TRACE/JFR and OS inspection are separate.

The planned helper ships in the existing nonexporting module and is exercised by
an SDK-owned private packaged consumer. It adds no public facade or debug CLI,
does not replace the evaluator, and leaves the provider-based seed as default.
Actual Java/javac Unicode transport stays unresolved until native observations;
required Unicode application paths cannot be excluded to manufacture a pass.

## Frozen evidence and capture protocol

The `protocol` object specifies the future `capture_reference.py` CLI, fixture
modes, exact request/result/streams/effects fields and failure behavior. Its only
arguments are `--contract`, `--platform` (`windows` or `linux`) and `--output`.
Paths must be explicit absolute paths; output must be a fresh assigned D scratch
directory. This is a declared interface, not a command reported as executed.
The separately built offline `net10.0` fixture uses native SDK10.0.401/runtime10.0.12.
SDK `dotnet run --no-build` behavior and System.Diagnostics.Process API-harness
behavior have separate engine IDs. SDK Job hard-parent-death and POSIX signal
probes are boundary observations, not API wait-cancellation equivalence.

There are 24 scenario definitions per OS (48 total), 102 fixed product rows,
eight reference cohorts per OS (16 total), four boundary groups and 60 new
negative variants (20 exact predicates times omission/content/wrong-binding).
Reference rows contain four files each plus four aggregates (68 minimum);
product rows contain four files each plus four aggregates (412 minimum).
Boundary groups, fixture binaries, controls and inherited bundles are additional.
Every mandatory dependency/output is named; future hashes are not invented.
Additional generated nested classes and inherited qualification objects require
an independently reviewed inventory freeze before capture/proof qualification.
Any unavoidable count/dependency/control expansion needs a prospective versioned
amendment, never silent producer-selected completeness.

The final JAR class inventory is variable until OP06/OP07. Its complete trusted
set must be frozen independently before OP08/OP09; `45 + N` is not an inventory.
The archived seed schema1 retains its old14-source/7-staged/45-class meaning.
Its154 controls apply only to the archived reader/base/artifact. Current affected
seed controls must be rerun against the final reader/artifact; old counts cannot
qualify the new process helper.

Caps remain unchanged: JVM128MiB/CPU2/SerialGC/codecache32MiB/perfdata off;
physical-memory floor512MiB and available-commit floor16GiB. Query20s and owned
operation120s include cleanup, with up to1s grace and <=5s cleanup reserve inside
the deadline. Linux retains network none, read-only root, cap-drop ALL, no-new-
privileges, CPU2/memory512MiB/swap512MiB/pids64/core0, inner25s, aggregate180s and
reserve40s. Split cohorts instead of raising caps. Pure Python checks and file
counts are not JVM operation caps. Outer-guard cleanup is retained as failed
capture evidence and cannot earn product cancellation credit.

## Ordered continuation

After root review, OP02A authors only `reference/Program.cs`,
`reference/Reference.csproj`, and `reference/NuGet.Config`; read the csharp-expert
skill before C#. OP02B authors only `java/ProcessProbe.java`,
`java/ProbeChild.java`, and `capture_reference.py`. OP02C authors only
`capture_windows.py`, `capture_linux.py`, and `reference-observations.json`.
All paths are relative to this directory. These three-file slices supersede the
historical unsplit OP02 allowance. Root checkpoint after OP02C precedes product.
The repeated reference acceptance bullets belong to that group checkpoint.
OP02A verifies only its native fixture/offline configuration and focused Windows
build/smoke; it does not depend on a future capture script or claim two-OS capture.
OP02B supplies JDK probes and capture protocol; OP02C performs both native captures.
The full12-task/37-distinct-file dependency graph is in `contract.json`.

OP01 verification is structural/source verification only: valid JSON, exact
unique inventories and cross-references, task DAG, case repetitions, source/tool
hashes and archive entries, clause coverage and exact four-file diff. Future
native behavior, final artifact closure and current reader controls remain open.
The full implementation report and reproducible validation script live in the
assigned D task scratch directory, outside the tracked four-file contract.

## OP01 review corrections

The corpus contains actual U+1F642 in argv, cwd and environment, with scalar and
UTF16 identities frozen. Native SDK argv probes append the payload after a second
literal `--`; the fixture parses only its five control tokens and reports its
actual received suffix independently of the request file.

Reference `request.json` retains base64 of the exact prelaunch request bytes after
capture. The request digest hashes those decoded bytes; the final envelope digest
lives only in its external descriptor, avoiding a cycle. Proof mutation pointers
operate on the explicit materialized row projection: verified retained request,
inline result and descriptor-verified inline effects. Preservation targets are
the existing `effects.after.source`, `priorSDK` and `siblings` inventories.
Pure synthetic checks exercise all60 pointer mutations and their intended binding
assertions. These checks establish contract coherence, not native behavior.

## Native fixture wire and capture ownership

The native fixture emits one UTF8 `dotj.owned-process.fixture-observation/1`
JSON object plus LF on stdout, including in exit17 mode. It reports actual Main
payload, cwd/environment and its API-child operations. It never declares capture
completion or fabricates driver streams, effects, guard, network or container
facts. The driver independently observes outer exit17 and retains the whole
stdout JSON as `stdout.bin`; API-child bytes stay in verified base64/length/SHA256
fields inside the subordinate observation. They never replace outer raw streams.
The final result retains this subordinate object and explicitly identifies the
driver, fixture and API-child actors. Parent environment snapshots belong to the
named actor. Request digests still bind exact retained prelaunch bytes.

`environment.baseline` is exactly `{values: complete string-to-string map}`.
Apply baseline to a child-local map, then remove names, then set names in ordinal
key order. Linux names are case-sensitive; Windows uses native case-insensitive
name equivalence. Preserve case-distinct request keys and record actual native
outcomes independently. Neither process changes global environment, cwd or console
encoding. The full field and merge rules are in `contract.json`.
New captures use controlled minimal environments containing only required OS/tool
settings and synthetic sentinels. Observe the actual controlled caller maps;
never copy unrelated host credentials into captures or substitute the requested
map for observed state. Historical private failed receipts remain preserved.

## OP02B executable wire supplement

ROOT task147 ruling prospectively expands OP02B to five tracked files to freeze
the previously missing JDK wire and adapter API. `ProcessProbe` uses
`--mode MODE --request ABSOLUTE_PATH -- PAYLOAD...` and emits the subordinate
`dotj.owned-process.jdk-probe-observation/1` object. Actual direct Process
observations, raw embedded child streams, independent received Unicode and
TRACE/JFR artifacts remain separate from outer driver facts. The java-argv mode
also cancels an onExit future for a separate bounded hold child, observes whether
it remains alive, then terminates and joins its owned workers. This establishes
no product or descendant guarantee. See `protocol.jdk.wire` for exact fields.

Platform modules expose `run_capture(contract, fixtures, output)`; the common
driver creates the fresh assigned D scratch output and validates the returned
structured receipt and frozen inventory. Adapters own pinned native launches,
guards, controlled caller setup and actual effects. Missing adapters retain a
failed receipt. `protocol.platformAdapter` freezes directory ownership and return
shape. Complete two-OS capture remains OP02C work.

## Qualified source portability

Preflight loads the helpers and sources from the current toolkit checkout.
Only five declared source roles permit CRLF-to-LF normalization: the reference
`Program.cs`, `Reference.csproj`, `NuGet.Config`, and Java `ProcessProbe.java`
and `ProbeChild.java`. Their qualified SHA256 values remain the reviewed LF
values. Bare CR, content changes and undeclared roles fail closed. Provenance
records the actual checkout path, physical byte length/SHA256 and qualified
LF byte length/SHA256 separately. Historical receipts and source pins remain
unchanged; retained fixture sources staged on D keep their exact qualified LF
bytes. All binary, generated configuration and other artifact checks remain
exact physical byte checks.

The fixed qualified Java compile receipt is checked before class staging. Its
two source roles bind by unique complete repository-relative suffix, independent
of the original checkout prefix. Missing, extra, ambiguous or changed bindings
are rejected. Source checks, exact class inventory and class digests pass before
copying; copied classes are checked again. Linux build reuse applies the same
finite source identity rule while retaining the pinned build and native proofs.

Pure regression checks (all scratch retained under the assigned D task directory):

```powershell
& 'D:/AI/Implementation/dotj Frameworks/toolchains/python-3.13.9/python.exe' -B ./test_portability.py -v
```

These checks and preflight provide no additional product acceptance or native
capture credit. SDK-I02-T4 remains OPEN; OP01/02A/02B/02C remains 4 of 12 and the
eight runtime steps remain pending.
