# Or conditions

Batch 2503 adds short-circuit `Or` to the internal evaluation candidate for `DJ-005-WP-01-T1`.

## Behavior

- `And` binds tighter than `Or`. Both associate left and evaluate left to right.
- Operators are case-insensitive whole words. `trueOr false` and `true Orfalse` stay refused.
- A right operand that short-circuiting skips is parsed but not evaluated, so its `Exists` path and scalar values are never read.
- Parentheses may contain `Or`. The existing 64-group and 256-node limits still apply.

## Evidence

Batch 2510 adds the current packaged reproduction command below. It executes the unchanged current 94-row runner, then the existing And consumer (9 native successes, 1 private malformed boundary, 24 actual current controls) and the new 35-case condition consumer against the same emitted candidate JAR. Its fixture-only compiler uses an empty source path and `-implicit:none`; both consumers verify the private named module and actual evaluator JAR location. The four MSB4130 occurrences compare code, file, line, column and raw condition within the 26 semantic matches, and add no unique cases.

From the repository root, using a fresh output directory and an independently frozen checkpoint:

```powershell
& 'D:/AI/Implementation/dotj Frameworks/toolchains/python-3.13.9/python.exe' -B tools/oracle/dotj-build/condition-product-v3/verify.py --out 'D:/AI/Implementation/dotj Frameworks/validation/<fresh-run>' --checkpoint '<frozen-checkpoint.json>' --checkpoint-sha256 '<independently-observed-sha256>'
```

Prepare a checkpoint with `verify.py --freeze-checkpoint <new-checkpoint.json>` after the source/tool/fixture closure is final. Independently observe its SHA256 before the qualification command. Independently revalidate the result with `verify.py --check-receipt <run>/verification.json --candidate-lock <run>/candidate-lock.json --candidate-lock-sha256 <independently-observed-lock-sha256>`. The versioned contract is `condition-product-v3/CONTRACT.json`. All temporary, home and cache paths must stay under the D: implementation root; execution retains the existing 128 MiB / two-processor / SerialGC resource floors and deadlines.

The native 35 rows reuse the externally pinned original/revised raw pair; this command performs no native capture and grants no new native-case credit. The reference lock's historical `NOT_IMPLEMENTED` warning disposition describes its original validation stage. The current packaged consumer actually compares all four warning occurrences. The 94 current rows match the retained current baseline, with 91 historical rows unchanged and 3 explicit Or input transitions. All six exact predecessor documents, including three changed And subcases, remain separately compared within the existing 35 cases; the original 24 aggregate controls are not claimed byte-identical.

The following classpath comparison command and native capture instructions in `condition-logic-v2` are historical evidence paths, not the current package qualification command:

`tools/oracle/dotj-build/condition-logic-v2/compare-candidate.py <new-run-id>` compares the Java candidate with the retained MSBuild 10.0.401 native capture in `condition-logic-v2/evidence/native-pass2-capture.json`.

| Result | Cases |
|---|---|
| Same P, Q and import edges | 26 |
| Native failure, candidate refusal | 5 |
| Declared candidate refusal where native succeeds | 4 |
| **Total** | **35** |

The four refusals were declared in the fixture manifest before native capture:

| Case | Reason |
|---|---|
| `CL04-lazy-exists-2` | Evaluated empty `Exists` path |
| `CL05-scalar-2` | Evaluated numeric coercion |
| `CL05-scalar-4` | Expanded value contains quote syntax |
| `CL08-skipped-malformed` | The candidate validates skipped conditions statically |

`verify.py` still passes its 94 packaged comparisons. The three legacy rows in `predecessor-transitions.json` now test a malformed `Or` input, so they are transitions, not unchanged results. Their exact old documents are native-compared as `CL09-legacy-*`.

## MSB4130

Batch 2506 reports MSB4130 for evaluated conditions that mix `And` and `Or` at one expression level, following `Parser.cs`: each `Expr` level, including a parenthesized group, consumes its own marks, so `(true Or false) And false` does not warn. `Result.conditionWarnings` carries the code, file, line, column and condition text, and the native comparison covers all five fields. Skipped conditions are not evaluated, so they do not warn.

## Limits

- Repeated identical conditions each report MSB4130 here; native parse caching for repeats is not captured.
- Native failure text and positions are not compared.
- `!=`, `!`, relational operators, items, globs and property functions stay outside the profile.
- This is internal candidate work. `DJ-005-WP-01-T1` stays open and no acceptance credit is granted.
