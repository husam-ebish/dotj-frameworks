# Selected DBNull singleton candidate

Batch 2063 advances `DJ-001-WP-01-T1`; no implementation task or release gate is accepted.

DBNull.ToType(Object) now returns the existing singleton, as does its DBNull self target. String conversion remains empty, and selected primitive and unsupported targets retain managed conversion errors. Static Type.GetTypeCode(DBNull) now returns DBNull, and the Type projection reports native sealed and serializable metadata flags.

The pinned CoreLib 10.0.12 oracle records 46 calls and eight assignability/instance pairs. The packaged consumer checks 64 groups: IConvertible operations, 23 targets including null, singleton identity, empty text, equality adapters, Type metadata/interfaces and null SerializationInfo behavior with two StreamingContext states. The native null-info error is NullReferenceException; the existing candidate already matches it. Java's default StreamingContext constructor is an explicit zero-state carrier adapter.

The serializable flag is metadata only. GetObjectData with non-null information remains unsupported, and serialization transport/holder representation, full exception messages, CLR boxing/language identity and release qualification remain open. Native interface names do not establish complete serialization dispatch. Runtime product dependencies remain JDK-only.
