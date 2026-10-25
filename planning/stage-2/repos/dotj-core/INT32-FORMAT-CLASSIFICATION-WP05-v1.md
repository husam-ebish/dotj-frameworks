# Selected Int32 standard and literal format classification

Batch 2125 advances DJ-001-WP-05-T1 without implementation acceptance credit.

Int32 recognizes lowercase bare d as decimal formatting, applies the selected negative sign to D-1/d-1/X-1/x-1 custom literal formats, throws FormatException for invalid single-letter standard formats, and supports the selected question-mark literal. Existing public signatures stay unchanged. Other custom formats and precision/culture domains remain bounded by their recorded contracts.

The pinned CoreLib 10.0.12 oracle records 1,848 rows across 21 signed anchors, including Int32 minimum/maximum, two numeric-symbol providers, standard formats and literal/invalid-specifier boundaries. The packaged Java consumer checks 5,544 groups through concrete, format-only and IFormattable routes. Compiled API and foundation gates retain the preceding signatures and regression coverage.

No full numeric API parity, task acceptance or framework qualification follows from this corpus. The product remains JDK-only; validation tools and intermediate artifacts stay on D:.
