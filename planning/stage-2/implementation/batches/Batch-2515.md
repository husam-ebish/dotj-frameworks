# Batch-2515: ValueTask Task lifetime

Status: selected group 1/1 implemented and verified in the Batch-2515 integration candidate. Independent task review approved; root canonical gate passed 517/517 checks and independently verified the identical final JAR. Whole-branch review and root integration/merge/push remain pending. The branch tracker records post-integration CANDIDATE count/list length 2515; canonical master remains 2514 until actual root merge.

ValueTask(Task), AsTask and Preserve add Task backing, source-to-Task conversion and durable preservation. Task privately retains original cancellation exceptions and tokens. Only Task.java and ValueTask.java change product behavior. The candidate contains 136 sources and 182 classes, including one private SourceTask adapter; its SHA-256 is `a83c6451854a7295532fd6a300f3603db6a8b3c73d65af9823222de9caf6e4db`.

The same JAR passes 115 native-paired rows/1884 fields, eight Java-only groups, Task61/697+49, WorkTask66/612+8, delegate34/cancellation48/ValueTask135. The genuine baseline compiler RED and one-time native capture are retained; all 399 native pins are immutable. No native or RED replay occurred.

The artifact phase succeeded before an explicit source/class map rejected the new private class. Updating that map and resuming binding/distribution reused the built JAR. The initial private fixture had four Runnable-to-ActionBody compile errors. Root approved a Java-only successor changing exactly four `new Action(observe)` expressions to `new Action(observe::run)`; all controls remain unchanged. Failed attempts and raw diagnostics remain retained, and completed groups were not rerun.

Binding, distribution and ordered rights/provenance/upstream-text/notice/ThrowSite/E01/differential audits passed. The verify-only gate checks reparse raw frozen native and candidate Java evidence, bind the current gate JAR and add no captures. All three E01 decisions remain OPEN.

Acceptance remains 0/1092 tasks (0%), 1686 open items, 0/66 qualified frameworks (2 in progress, 64 not started); remaining tasks core27/build25/other1040. Historical Batch-2500 remaining work is 0; whole-project batch count is UNKNOWN. No rights, release or framework acceptance is granted.

See [stable contract](../../repos/dotj-core/PUBLIC-VALUETASK-TASK-N01-v1.md) and [hash-bound evidence](../../repos/dotj-core/evidence/public-valuetask-task-v1.json). Current status is maintained here and in STATE, never by editing the frozen contract.

Root proof: `batch2515-root-full-gate1-verification-v1.json`, SHA-256 `07aa1d9cd105bcfa559798a664e7d74ba0ee9d3dcba926e857ebbd6afee82243`, binds input HEAD `7d8a1c4f4b163250a1a9f44054f14873b56c9445` / tree `b352524c079d6ab1681d11fcfa1d092b2bc7c9f0`. The actual isolated gate executed 517 checks with 136 sources/182 classes, verified 977 aggregate evidence hashes and found zero source newline differences. Its final JAR is byte-identical to the selected 115/1884+8, Task61/697+49, WorkTask66/612+8, delegate34/cancellation48/ValueTask135 qualification. All 399 native pins, 115 rows/1884 fields plus one metadata row, old observations and twelve frozen native Git blobs remain unchanged. The 499 exported JSON records are retained exactly.

Review finding B2515-STYLE-01 is retained: the captured/tested Java fixture and native oracle contain 98 trailing-whitespace lines each. Their exact bytes remain frozen; a global diff check is not clean. Bookkeeping and nonfrozen changes are checked separately with these two explicit exclusions. No runtime behavior is replayed for finalization.

The broader dependency graph and public .jinstaller feed remain unresolved. The product is JDK-only; Python and .NET are development/reference tools. Generic/value-copy/context/scheduler and wider API qualification remain open. No current merge/push, whole-branch approval, task acceptance or release qualification is claimed.
