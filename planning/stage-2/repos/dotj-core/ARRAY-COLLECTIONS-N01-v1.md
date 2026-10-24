# Selected array collection projection

Batch 2069 advances `DJ-001-WP-01-T1`; no implementation task is accepted.

System.Array and selected array shapes now enumerate and resolve the logical ICollection/IEnumerable subset, and those interfaces recognize selected array types and storage through assignability/instance predicates. System.Array now reports the pinned serializable metadata flag. Direct Java collection-interface dispatch and serialization are separate open adaptations.

Native rank-one compatibility is directional: an Int32[*] target accepts Int32[] type/storage, while an Int32[] type target rejects Int32[*]. The previous requirement that vector flags always match is corrected. Higher-rank runtime storage remains outside the selected Java carrier profile.

The pinned CoreLib 10.0.12 reference records eight base/vector/non-vector/matrix/jagged/pointer-array profiles, 256 lookups, 104 type-relation pairs and 78 instance queries. The packaged consumer passes 454 groups, including selected metadata/interface lists and vector/jagged/reference storage. Native generic, IList, clone and structural interfaces are retained as omitted scope.

These checks do not qualify omitted interface lookup/dispatch, rectangular allocation/storage, pointer values, all array conversions, physical Java interface adaptation, serialization transport or full language/release behavior. Product runtime dependencies remain JDK-only.
