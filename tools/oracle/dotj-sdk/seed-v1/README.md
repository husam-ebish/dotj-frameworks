# SDK seed qualification

These Python tools are validation producers and readers. The product seed and
SDK launchers do not use Python. `baseline-lock.json`, `contract.json` and
`consumed-contract-v2.json` preserve the pre-implementation source/native gate;
`implementation-profile-v3.json` records the adopted sourcepath and Windows
transport amendments. Never rewrite those frozen inputs to match a candidate.

`test_seed*`, `test_paths*`, `test_recovery*` and `qualify_commands*` retain actual
argv, streams, resource/ownership facts and failed attempts in fresh directories.
Linux attempts use an explicitly case-enabled empty parent and bounded owned
containers. A timed-out create with uncertain CID requires later independent
exact-name settlement before a fresh retry. No timeout silently increases.

`freeze_inherited.py` verifies the new SDK JAR against the complete inherited
Build semantic inventory. `freeze_proof.py` packages all selected raw objects and
the reader closure, including physically copied inherited pure readers. Original
paths in descriptors are provenance strings, never evidence fallback locations.
Run the packaged reader, whose dependencies are alongside it:

```text
python -B <bundle>/reader/proof_reader.py --proof <bundle>/proof.json --sha256 <proof-sha256> --jar <explicit-sdk-jar> --source-root <repository-root>
```

The source root must be the repository root. This is a pure read: no Java, .NET,
build, network, or original-path lookup. A proof with phase
`BASE_FOR_READER_CONTROLS` emits an explicitly nonfinal result. Only
`FINAL_QUALIFICATION` can emit `PASS_BOUNDED_SDK_PROOF`, and it requires the exact
executed reader-control inventory. `mutate_proof.py` persists 41 negative overlays
and runs a physically relocated copy; `finalize_controls.py` retains a historical
targeted native-SDK digest-control correction. Final controls include the actual
SDK executable pin mutation directly.

Counts stay separate: 64 designed S/Q/C rows, 32 native Q cohorts/68 invocations,
32 candidate Q cohorts/68 invocations, four independent builds, and 41 reader
mutation variants. Windows offline isolation and arbitrary Unicode JDK installs,
other Linux locales, full SDK selection, T4/T5, whole packages and public release
remain outside the accepted scope. No accepted-task or framework credit is
assigned by a reader result.
