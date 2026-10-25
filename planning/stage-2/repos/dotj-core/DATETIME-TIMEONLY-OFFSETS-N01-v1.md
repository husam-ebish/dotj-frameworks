# Paired DateTime time-only offset checks

Batch 2079 advances DJ-001-WP-05-T1 with a qualification check; no implementation task or release gate is accepted. Product Java sources and public signatures are unchanged.

Year-one time-only z formatting depends on the current local offset, including for UTC Kind. Date fields preceding z disable that branch; percent custom-token recursion selects its own time-only context. Immutable golden text cannot qualify this clock-dependent behavior.

A pinned CoreLib 10.0.12 oracle now takes native results before and after each packaged Java run. Four frames exercise 117 cases and five routes each: provider, single-format and IFormattable strings plus full Char and UTF-8 buffers. The verifier requires each Java result to match its native before or after observation exactly, compares full buffer/written state, verifies zones, source/JAR/executable hashes and bounds both monotonic and UTC frame durations to ten seconds. All 2340 paired comparisons pass. Four deliberately malformed records (wrong offset, missing route, duplicate case and expired frame) are rejected.

The fixture is compiled against the product JAR. Pinned JDK and CoreLib hashes are verified. Every process input, output, log and compiled consumer stays on D:. This check runs in the gate's serial live phase to avoid racing other shared reference-tool configuration updates.

The selected native W. Europe Standard Time/JDK Europe/Zurich current-host profile remains bounded. Historical Local/Unspecified date-first offsets, other zones, clock changes outside valid frames, complete culture/calendar/provider behavior, CLR language identity and release acceptance remain open. Native historical profiles are excluded explicitly; no full timezone equivalence is claimed. Product runtime dependencies remain JDK-only; native and Python tools are validation dependencies.
