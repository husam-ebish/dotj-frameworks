# Batch 2523: source seed and relocatable evaluation SDK

Status: candidate implementation and qualification; independent root review,
canonical proof and source publication pending. Published count remains 2522.

The owned JDK21 seed creates SDK version `0.1.100-dev.1` from seven declared Java
sources using in-process compiler and JAR providers. The launcher validates an
explicit qualified `JAVA_HOME`, discovers its own root, reports real identity,
and exposes a bounded property-query interface over the existing evaluator.
The six inherited sources remain unchanged. The internal module exports and
opens no packages and contains one evaluator implementation.

Final JAR: `ecc7b14562a9bd2ae6108083369a32b7163864f649f233fc34b08386c9b33c2e`,
93942 bytes and 45 classes. Two independent source-only builds on each measured
OS produce the same complete JAR. Actual Windows and native Linux .NET SDK
10.0.401 captures supply 32 reference cohorts/68 invocations; the final candidate
executes the same 32 query cohorts/68 invocations under its declared capability
differences. These are observations and scenarios, not batches or task credit.

Actual final-JAR inherited replay covers 19 trace graphs × three profiles per OS,
42 item rows per OS, 14 private groups/61 rows, four supplements, raw sorting and
three boundary families per OS, ordering308/M1, Boolean297/private16/control14,
all14 history operations, stable94 with the sole NEG-items transition and ABI.
The module descriptor adds the internal resource package `dotj`; no exports,
opens or ModuleMainClass are added. Old class identity is additional provenance.

The pure proof requires exact operation, platform, cohort and output inventories
before semantic comparisons. Source/JAR/tool identities, raw channels, original
argv, immutable fixtures and retained prior payloads are bound to actual evidence.
All failed attempts remain retained, including no-CID Docker create timeouts,
native host initialization failures, initial sourcepath and transport failures,
and the interrupted Linux JDK-copy setup. No failed attempt receives pass credit.

Windows network-isolated offline execution is NOT_QUALIFIED. Windows arbitrary
Unicode JDK installation is NOT_QUALIFIED; source/output/SDK/project/argument
Unicode has separate positive evidence. Linux is case-enabled Windows-backed
Docker9p/NTFS with C.UTF-8, not generic ext4 or all locales. Native accepted
inert-target evaluation and harmless Build are explicit candidate admission/
capability gaps. T4/F04, T5/F05, full SDK-I01/I02/I03, Java25, public parity and
distribution remain open.

SDK-I01-T1 (concrete baseline lock), SDK-I02-T2 (JDK-only seed), and SDK-I02-T3
(minimal launcher) have evidence submitted for independent named-task review.
No automatic task acceptance is claimed. Accepted tasks remain 0/1092, open
acceptance items 1686, qualified frameworks 0/66, historical2500 remaining0,
project batch total/remaining UNKNOWN. Root owns all publication/counter changes.

The [exact qualification record](../../repos/dotj-sdk/evidence/sdk-seed-v1.json)
binds the Task137 round2 proof, 2640 bundled objects and 121 executed
reader variants. Initial proof v9 (2520 objects/41 variants) and round1
(2636 objects/119 variants) are retained and explicitly superseded. The repair
requires all six reader dependencies, current
reader/base scope ancestry, actual relocation invocation/summary, and semantic
outputs for all four source-build profiles. Round2 restores complete Windows
Unicode 15-file source-tree preservation, including uncompiled Ambient.java,
with two focused change/removal controls. The 14 declared-input and seven
staged-source checks remain separate. Product sources and JAR are unchanged.
FINAL_QUALIFICATION requires the complete control record; removing it fails.
Base-for-controls proofs emit an explicitly nonfinal status.
