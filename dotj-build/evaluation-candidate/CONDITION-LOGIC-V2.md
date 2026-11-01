# Or conditions

Batch 2503 adds short-circuit `Or` to the internal evaluation candidate for `DJ-005-WP-01-T1`.

## Behavior

- `And` binds tighter than `Or`. Both associate left and evaluate left to right.
- Operators are case-insensitive whole words. `trueOr false` and `true Orfalse` stay refused.
- A right operand that short-circuiting skips is parsed but not evaluated, so its `Exists` path and scalar values are never read.
- Parentheses may contain `Or`. The existing 64-group and 256-node limits still apply.

## Evidence

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
