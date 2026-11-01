# Internal parsed-condition cache qualification

The externally approved native reference is
`D:/AI/Implementation/dotj Frameworks/validation/Batch-2511-cache-native-pair-v1/observation-lock.json`,
SHA-256 `9612d662aa80501614b04475236169d7bb839ef5e0d41b932e2964bd0d2d688c`.
It records eight ordered evaluations in each of two fresh native processes. All
eight rows therefore run in one fresh Java VM, preserving the original order.
The 35-condition corpus, And corpus and private cache controls each run in their
own VM, as separate datasets; they do not warm the eight-row cache.

The existing packaged JAR (`253a22a247695295fe6eea07d34fbb71f9b5f059715fde75ac75eb4a2ceba941`)
was tested before the product change. Its values and imports matched all eight
native rows, but warnings were `[2,2,2,7,2,2,0,1]` (18), versus the observed
`[1,0,0,1,1,1,0,1]` (5). The genuine assertion failure, all eight actual rows,
compiler output and exact source staging remain in
`validation/Batch-2511-cache-product-red-run1`. Later runs never overwrite it.

## Representation and source basis

Pinned MSBuild revision `b44cdcec4c79c50c67560876707d57d4f635fa3b`:

- `src/Build/Evaluation/ConditionEvaluator.cs:240–300` selects a cache by parser
  options, then an ordinal raw-condition pool. A cache miss invokes the parser;
  each evaluation receives a new context, and mutable node state is reset.
- `ConditionEvaluator.cs:306–340` flushes before lookup when the optimistic
  entry count exceeds 3000. The Java owned map uses that same threshold and
  timing as a bounded retention rule, without claiming native eviction parity.
- `src/Build/Evaluation/Conditionals/Parser.cs:134–145` emits MSB4130 during parsing.
- `src/Build/Evaluation/Evaluator.cs:1002,1320,1446,1620` uses AllowProperties
  for the four supported sites: PropertyGroup, property, ImportGroup and Import.

Java retains immutable syntax and a mixed-And/Or flag in an exact-string map
for the named module's classloader lifetime. Lookup/parse is synchronized;
evaluation and file access occur outside the lock in a fresh State. No State,
expanded values, booleans, globals, owner path or result is cached. Whole-XML
validation parses independently and cannot warm the map or consume a warning.
This preserves fail-closed validation of skipped malformed branches.

The native source pools mutable nodes; this implementation safely shares
immutable syntax. The selected observations establish sequential warning and
value behavior, not equivalent pool internals. Native concurrency, eviction,
multiple classloaders, alternate ParserOptions, same-live-Project reevaluation
and full cache parity remain unqualified. Four extra Java-only controls exercise
fresh values and owner-relative Exists on cache hits, immutable snapshots,
scalar-injection rejection after warmup, and malformed skipped syntax after
warmup. They add no native acceptance claims.

## Qualification

`tools/oracle/dotj-build/condition-cache-product-v1/verify.py` is the narrow
successor. It reuses preserved v3 validation primitives without changing or
rebinding the v3 product-source pin, and invokes the unchanged canonical
94-row runner. It compiles only the explicit new consumer and unchanged And
consumer against the actual newly built named-module JAR, using an empty
sourcepath and `-implicit:none`. Every green consumer uses that same JAR.
It verifies CodeSource, zero exports/opens, the nonpublic evaluator class,
caller-map preservation, immutable results and task-marker absence.

The preserved historical `ConditionLogicPackagedTest` compared complete Result
equality on a repeat, including parse-time warnings. That assertion belongs to
the pre-cache stage. The successor keeps all 35 first-evaluation expectations
(26 evaluations, five native parse boundaries, four declared boundaries, four
warning events), and separately compares repeat values/files/imports/duplicate
information while requiring no new parse warnings. It also preserves the 94
rows and unchanged And 9 successes / 1 malformed boundary / 24 private controls,
including the 64-group and 256-node private limits. The three historical legacy
transitions are unchanged; no unique-acceptance counts are added.

Use the pinned Python 3.13.9 executable with `-B`. Freeze a fresh external
checkpoint with `--freeze-checkpoint <path>`, then run with
`--checkpoint <path> --checkpoint-sha256 <external hash> --out <fresh D: path>`.
Add `--red` to test the immutable baseline JAR. Check a completed receipt with
`--check-receipt <verification.json> --candidate-lock <candidate-lock.json>
--candidate-lock-sha256 <external hash>`. All inputs and raw results are retained.

Each Java/compiler launch uses 128 MiB, two processors, SerialGC and a 120-second
timeout after a fresh memory check (512 MiB physical / 16 GiB virtual; 20-second
query, 120-second wait, five-second polling). The canonical runner's owned outer
helper has a 600-second ceiling and uses the frozen cleanup adapter with an
absolute pinned executable and D: environment. No native observer or SDK build
is launched. Native preparation and its 29 pure Python controls remain unchanged.

Accepted task credit and numbered batch credit are both zero. Overall framework
completion is not inferred from this private qualification.
