# Batch-2514: Computational Task and asynchronous cancellation

Status: selected implementation and targeted same-JAR verification complete. Independent task review, root full canonical gate, final-artifact qualification, whole-branch review and actual merge/push remain pending.

Task.Run(Action), Task.FromException(Exception) and CancellationTokenSource.CancelAsync add real queued/running work, original fault identity and serial LIFO cancellation callback draining. Terminal-state observation, late empty registration and ObjectDisposedException messages are included prerequisites. Only three product sources change; all other 133 source files and 178 class files retain their bytes. The canonical JAR contains 136 sources' output and 181 classes, with no new class or fixture leakage and only java.base dependency.

Candidate SHA-256: `356b4c53709a35ad3eeb79e569581b8432ebabf7b8364b9cf7afdc934e0c150d`. The same JAR passes 66 paired rows/612 fields and eight Java-only groups, old Task61/697+49, delegate34, cancellation48 and ValueTask135. The actual one-time native capture and genuine baseline compile failure are retained; no native or baseline replay occurred. All 387 native input pins remain unchanged.

The historical old Task boundary API allowlist failed on the legitimate new method. A separate successor preserves all original 49 checks and count and asserts exact new static signatures separately; full API authority is also checked by new J07. The first late-audit attempt failed because Git was absent from its explicit PATH. Its successful distribution/rights steps and failure are retained; the successor added only the installed Git command directory and resumed the remaining audits. No product change, rebuild or repeated completed behavior group was needed.

Canonical build and source/JAR binding precede distribution, rights, source provenance, pinned upstream comparison, notice queue, ThrowSite adjacency, E01 packet and differential provenance audits. Those audits pass; all three E01 decisions remain OPEN. A new verify-only gate check reparses raw frozen native and current Java results on the expected current JAR. Existing full-gate count 515 is historical; root will report the actual current count.

| Work group | Done | Remaining |
|---|---:|---|
| Selected computational Task/CancelAsync | 1/1 targeted-verified candidate | Independent reviews, root full gate, final artifact and integration |
| Historical Batch-2500 target | Complete | 0 |
| Whole project | 2514 post-integration candidate batches | Unknown batch count |

Acceptance remains 0/1092 tasks (0%), 1686 open items, 0/66 qualified frameworks, 2 in progress and 64 not started. Remaining task counts are core27/build25/other1040. Canonical master remains at 2513 until root integration; this branch's 2514 count is explicitly the post-integration candidate count.

Java-only boundaries include foreign Throwable wrapping, daemon scheduling, interruption restoration and observable asynchronous rejection fallback. Generic tasks, broader scheduler/context semantics, async builders, Task-backed ValueTask and complete API/reflection qualification remain open. Product runtime dependencies are JDK-only; Python/.NET are development/reference tools. Broader dependency relationships and a public .j installer/feed remain unresolved. All temporary outputs and evidence are under D:.

See [contract](../../repos/dotj-core/PUBLIC-WORKTASK-CANCELASYNC-N01-v1.md) and [hash-bound evidence](../../repos/dotj-core/evidence/public-worktask-cancelasync-v1.json). Root owns all remaining gates and integration; no acceptance credit is claimed.

Self-review also caught a Python default-decoding edit of two currency literals in the unexecuted canonical builder main. Exact tested builder bytes are archived; explicit UTF-8 restores the original literals, and AST comparison proves the executed artifact phase unchanged. A narrowly scoped historical-input resolver plus a strict current lock preserve original receipt integrity; three wrong-input/archive controls reject substitutions. Product sources/JAR and completed behavior results remain unchanged.
