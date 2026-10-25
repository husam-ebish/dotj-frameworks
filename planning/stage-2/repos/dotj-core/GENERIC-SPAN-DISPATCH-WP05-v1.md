# Generic Encoder and Decoder count/write span adapters

Batch 2209 corrects the generic count/write heap span projections to match their native pointer-backed adapters. Decoder's generic span count calls the non-flush array overload. Generic writers receive a zero-initialized temporary destination, publish only the clamped successful prefix, and leave caller data unchanged when the callback throws. Negative callback returns remain bounded native observations. The selected UTF-8 private overrides retain their stateful flush and partial-write behavior.

The new native corpus reproduces the preceding generic mismatch: a throwing writer's temporary data was previously copied into the caller's destination. It also records exact count/write overload selection and callback array lengths. The consumer now passes 9,280 groups across 3,200 native cases: 320 count cases and 2,880 writes, with count multipliers, callback modes, view offsets and capacities. The generic Decoder count trace always selects the non-flush callback. Every observed native generic write failure leaves the caller destination unchanged.

UTF-8 NLS behavior is preserved through explicit private span overrides for Encoder writing and Decoder counting/writing. Existing 344,400 stateful span groups, 138,240 Convert span groups, generic array protocols, custom providers and stateless encoding suites remain regressions. The compiled declaration inventory remains 22/28 because these signatures already existed.

These are selected heap adapters, not direct pointer overrides, CLR ref-struct/stack/pinning lifetime, arbitrary reentrancy, full reflection/source ABI or WP-05 acceptance. The existing source-adjacency record covers Encoder.cs, Decoder.cs and UTF8Encoding.cs; E01 applicability remains open. Hash-bound differential evidence is LF-pinned. No accepted task, qualified framework or rights clearance is credited.

Next is exact custom-provider stateful span count/write/Convert qualification, including callback failures, nullable factories, overflow/reset behavior and recovery.
