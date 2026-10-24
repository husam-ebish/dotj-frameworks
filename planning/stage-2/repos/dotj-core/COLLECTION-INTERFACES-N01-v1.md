# Selected non-generic collection interface relations

Batch 2067 advances `DJ-001-WP-01-T1`; no task acceptance is claimed.

The common selected interface lookup now includes IEnumerable, IEnumerator, ICollection, IDictionary, IDictionaryEnumerator, DictionaryEntry, SerializationInfoEnumerator and IFormatterConverter. Parent lists use the existing selected collection interfaces; IEnumerator and IFormatterConverter have no parents. IEnumerator assignability now follows its declared Java interface inheritance, including IDictionaryEnumerator, alongside the existing SerializationInfoEnumerator mapping.

ValueType instance classification now consults the logical Type value flag rather than an incomplete carrier list. The new runtime corpus specifically checks DictionaryEntry membership. Broader carrier membership remains separate qualification work.

The pinned CoreLib 10.0.12 reference records eight profiles, 124 lookups, 80 assignability/subclass pairs and 50 instance queries. The packaged consumer passes 262 groups, using exception Data dictionaries and their enumerators, DictionaryEntry, Object and null. Query shape and true-null guards are retained from the selected core lookup profile.

This qualifies selected non-generic relationships and instances. Full collection behavior, generic interfaces, arbitrary carriers, formatter implementations from other assemblies, serialization transport and language/release qualification remain open. No product runtime dependency changes.
