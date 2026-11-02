# Private numeric and version ordering

Task106 adds `<`, `<=`, `>` and `>=` at the existing single-comparison precedence.
An immutable ordering node keeps equality separate. Conversion tries left
numeric/version, then right numeric/version, expanding each reached scalar once.
Dispatch prefers numeric pairs, then version pairs, then both mixed directions.
Versions have two through four nonnegative Int32 components; missing components
are -1. Mixed comparison uses the version major; dotted versions exceed equal
numbers. All comparisons with NaN return false. Boolean short circuit, raw-cache
ownership, group64/node256 bounds, module-info and the no-task boundary remain.

`prepare_inputs.py` launches nothing. It copies original fixture bytes and derives
the consumer bridge from the adopted native contract at
`D:/AI/Implementation/dotj Frameworks/agents/batch2518-build-ordering-preparation-v1/frozen-native-contract-v3/contract.json`,
SHA256 `9beb122636b028f01dccbdf4988c517160abcfdfcf06d374fcab470c70732452`.
Its export preserves every native row and diagnostic. The Java consumer checks
every bridge row against the actual packaged evaluator.

Native outcomes are **222 successes/86 project errors**. Private dispositions are
**220 success comparisons/81 error mappings/seven restrictions**. Success checks
cover P/Q; ordered import owner/target/start coordinates; condition-warning
code/owner/start coordinates/raw condition; available duplicate/circular notice
code/owner/start coordinates; and Default record-list unavailability. Error
categories do not implement native exception/message/location/HResult ABI.

| Explicit restriction | Private category | Retained boundary |
| --- | --- | --- |
| `ORD-EXPAND-unicode-left` | `UNICODE_COMPARISON` | Reached scalar conversion stays ASCII-only. |
| `ORD-EXPAND-unicode-right` | `UNICODE_COMPARISON` | Reached scalar conversion stays ASCII-only. |
| `ORD-REACH-nbsp` | `UNICODE_COMPARISON` | Non-ASCII component whitespace stays excluded. |
| `ORD-REACH-unicode-digit` | `UNICODE_COMPARISON` | Non-ASCII component digits stay excluded. |
| `ORD-GRAMMAR-skipped-malformed` | `CONDITION_PROFILE` | Static validation covers skipped sites. |
| `ORD-BOUND-group65` | `CONDITION_BOUND` | Grouping limit stays 64. |
| `ORD-BOUND-node257` | `CONDITION_BOUND` | AST limit stays 256. |

Restrictions receive no native equivalence credit. Extra source-based component
controls also add no native case credit. All potentially mixed And/Or raw
conditions occur only in native part04, including the repeated owner pair and
skipped/imported owner case. One Java process preserves their captured warning
context without resetting or ignoring warnings.

`OrderingProductTest` observes MSB4130 in the actual failed State before an
ordering-conversion error, then reuses that exact raw AST with valid, false and
other-owner inputs. It checks stale warning/conversion state, non-scalar operands
without predicate/child execution, exact skipped bounds and component parsing.
`OrderingBooleanRegressionTest` allows only the exact immutable nested
`OrderingOperator` enum in the original raw-AST control. All 297 native bridge
rows remain byte-for-byte unchanged, including nine restrictions and three fault
adaptations. Of 16 private inputs, only `BOOL-BOUND-ordering` transitions to
observed P=`yes`, Q=`taken`, using identical historical/native fixture bytes.
Original consumers, contracts and transition ledgers remain intact.

Actual development evidence is retained at
`D:/AI/Implementation/dotj Frameworks/agents/batch2518-build-ordering-preparation-v1/task106-product-dev-attempt02`.
Two compilations and two JVMs exited 0: ordering308 plus its controls and
Boolean297/private16/control14. Both used JAR SHA256
`6bc95bc7ed6d702ed58f455f10fe35ed0c71389dd175034afefaee2e259e089f`,
109934 bytes, 31 class files including module-info. Product-source SHA256 is
`047af1cd4d20f870abb0965a55a140c0b2d6ff8193c2405ff66b9b5399de462c`.
Complete finite input checks ran before/after; all owned child/controller Jobs
cleaned up. The retained root-reviewed runner/plan contain exact commands.

Attempt01 remains a compiler setup failure: root's empty product-source-path
instruction caused rejection of the two named-module source files. One compiler
exited 1; no consumer compiler/JVM ran. The corrected recipe uses the exact
closed two-file product source directory, `-implicit:none`, and an empty consumer
source path. Product/consumer code did not change between attempts.

This is **development verification, not full final-JAR qualification**. Twelve
historical JVM operations, independent source/whole-branch review, integration
and push remain with root. Accepted tasks added: 0; accepted 0/1092, open 1686,
qualified 0/66. Batch2518 remains unfinished. No public facade, external product
dependency, generated/vendor/C# change or task execution is introduced.
