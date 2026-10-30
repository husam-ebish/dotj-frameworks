# Property-expanded single explicit import paths v1

This non-exported evaluator slice targets DJ-005-WP-01-T1 / DJ-005-F01-01.
Both remain OPEN; no implementation task, numbered batch, acceptance or product
credit is claimed. New semantic qualification is Default-only.

`Import Project` accepts literal fragments and well-formed `$(ASCII_identifier)`
references. Static validation reads neither properties nor target paths. Raw
functions, items, metadata, reserved names, malformed references, residual dollar
syntax, globs, semicolons, percent escapes, absolute/URI/backslash paths and
unsupported conditions refuse even inside skipped imports/groups. Literal-empty
`Project` remains a static restriction.

At each encounter, group and import conditions precede expansion. A true import
expands once from the current stored properties, then validates one explicit
relative slash path before loading a target. Values introducing wildcard/list/
percent/dollar/absolute/URI/backslash syntax refuse. No recursive expansion,
unescaping, globbing or list splitting occurs. Resolution uses the importing
file's directory and existing sandbox/real-path checks. Import policy, immutable
globals, per-call state and result snapshots retain their existing rules.

The eight-case manifest and fixture hashes are in
`evidence/import-path-plan-v1.json`. Two fresh native Default processes reproduced
the same complete envelopes under pinned SDK 10.0.401, runtime 10.0.12 and
MSBuild 18.9.11. The new versioned C# producer uses manifest-supplied globals and
the prior envelope shape; historical producers and observations are retained.
No Build, restore, task invocation or network request is part of capture.

| Case | Native observation |
|---|---|
| NEG-dynamic-import | P=`one.props`, Q empty, one unique import, no diagnostic |
| encounter-order-concatenation | P=`onetwo`, Q=`firstsecond`; two encounter-time targets |
| nested-owner-relative | P=`owner`, Q=`sub`; nested owner selects its sibling target |
| condition-before-path | P=`selected`, Q=`condition`; skipped empty/wildcard values do not fail |
| immutable-global-import-name | P=`once`, Q=`one.props`; one import and duplicate warning MSB4011 at (4,3,0,0) |
| undefined-expands-empty | Failed constructor, MSB4020 error at (2,3,0,0) |
| defined-empty-expands-empty | Failed constructor, MSB4020 error at (3,3,0,0) |
| expanded-missing-file | Failed constructor, MSB4019 error at (3,3,0,0) |

Empty expansion has private `INVALID_IMPORT_EXPRESSION` failure and `INVALID`
diagnostic context. Its imported/missing target is null and there is no Result.
The missing nonempty path retains `MISSING_IMPORT` and its actual target. Native
messages, HResult and public exception/logging ABI remain evidence only. Raw
nullable codes, all four coordinates, getter unavailability, ordered diagnostics,
cleanup and markers remain in the observations. Before normalization, each
embedded capture must match parsed exact retained stdout with strict JSON types
(boolean/numeric coercion is refused). The validator also rechecks the copied
manifest, complete fixture inventory and every copied fixture byte hash. Only
the exact copied fixture-root prefix is normalized in path and message fields.

The existing `NEG-dynamic-import` retains its stable ID and exact inputs:

| File | Bytes | SHA256 |
|---|---:|---|
| main.proj | 90 | 752761ce6eedf56cb4042798dd8175f46f88a67f2dac8d26786b304af57c2e3e |
| one.props | 10 | 4fd24be83f7dd636f6e2e8f456dfa559f1ca9c7346e1d10a5358db346b1300b9 |

Neither file has BOM or trailing newline. Its historical
`PROFILE_REJECT / IMPORT_PATH_PROFILE` record remains untouched. The new
native-backed disposition is `NATIVE_IMPORT_PATH_MATCH / SUCCESS` after capture
and candidate verification. All 83 prior comparison obligations remain accounted
for, with exactly this one intended transition. Seven genuinely new unique cases
produce 90 unique full-suite comparisons. The focused eight include the overlapping
legacy ID and are never counted as eight additional cases.

Remaining gates include the public API/exception/logger contract, full import
chains, dynamic cycles and profile combinations, SDK/implicit imports/resolvers,
glob/item behavior, cross-platform qualification, rights review and all broader
WP-01-T1/F01-01 acceptance criteria. No new dynamic import profile is introduced.
