# Batch-2515: ValueTask Task lifetime

Status: selected implementation and targeted same-JAR validation complete; independent task review, root canonical full gate, final-JAR identity, whole-branch review and integration remain pending. Completed tracker count remains 2514 until actual integration.

ValueTask(Task), AsTask and Preserve add Task backing, source-to-Task conversion and durable preservation. Task privately retains original cancellation exceptions and tokens. Only Task.java and ValueTask.java change product behavior. The candidate contains 136 sources and 182 classes, including one private SourceTask adapter; its SHA-256 is `a83c6451854a7295532fd6a300f3603db6a8b3c73d65af9823222de9caf6e4db`.

The same JAR passes 115 native-paired rows/1884 fields, eight Java-only groups, Task61/697+49, WorkTask66/612+8, delegate34/cancellation48/ValueTask135. The genuine baseline compiler RED and one-time native capture are retained; all 399 native pins are immutable. No native or RED replay occurred.

The artifact phase succeeded before an explicit source/class map rejected the new private class. Updating that map and resuming binding/distribution reused the built JAR. The initial private fixture had four Runnable-to-ActionBody compile errors. Root approved a Java-only successor changing exactly four `new Action(observe)` expressions to `new Action(observe::run)`; all controls remain unchanged. Failed attempts and raw diagnostics remain retained, and completed groups were not rerun.

Binding, distribution and ordered rights/provenance/upstream-text/notice/ThrowSite/E01/differential audits passed. The verify-only gate checks reparse raw frozen native and candidate Java evidence, bind the current gate JAR and add no captures. All three E01 decisions remain OPEN.

Acceptance remains 0/1092 tasks (0%), 1686 open items, 0/66 qualified frameworks (2 in progress, 64 not started); remaining tasks core27/build25/other1040. Historical Batch-2500 remaining work is 0; whole-project batch count is UNKNOWN. No rights, release or framework acceptance is granted.

See [stable contract](../../repos/dotj-core/PUBLIC-VALUETASK-TASK-N01-v1.md) and [hash-bound evidence](../../repos/dotj-core/evidence/public-valuetask-task-v1.json). Current status is maintained here and in STATE, never by editing the frozen contract.
