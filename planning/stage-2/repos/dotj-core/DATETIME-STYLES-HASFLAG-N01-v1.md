# Selected DateTimeStyles HasFlag

Batch 2085 advances DJ-001-WP-05-T1; no implementation task or release gate is accepted.

HasFlag compares the same enum carrier using Int32 bit containment. Zero flags succeed, including on unknown values; composite and sign bits are preserved. Parsing-style validation is not applied. Null flags throw ArgumentNullException with flag; foreign enum types throw ArgumentException with no parameter name before bit testing, including foreign zero-valued flags.

The pinned CoreLib 10.0.12 reference records 3850 cases across selected signed anchors, every 0-255 flag value, additional unknown/sign-bit flags, null and twelve foreign enum types. The packaged consumer passes every group, comparing booleans, exception identity/HResult/parameters. javap checks the deliberate Java signature HasFlag(Object).

The native formal parameter is System.Enum. Object is an explicit Java carrier bridge for the selected enum argument domain while physical CLR Enum inheritance is unresolved. This is not exact public CLR parameter qualification; non-enum Java Objects are outside the captured native domain. Physical enum identity, isolated loaders/equivalent types, other Enum APIs, complete messages, language integration and full release acceptance remain open.

The local API-preview helper was corrected to route Python bytecode under D:. Its old C: repository bytecode cache was moved intact to the structured D: recovery cache; preview verification confirms the repository cache is absent. All validation intermediates remain on D:. Product runtime dependencies remain JDK-only.
