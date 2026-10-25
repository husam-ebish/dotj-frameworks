# Selected UTF-8 whole-character-array and capacity overloads

Batch 2167 adds GetBytes(Char[]) and GetByteCount(Char[]) through the selected range implementation. Native null array parameter identity is preserved. It also adds overflow-safe GetMaxByteCount and GetMaxCharCount. Pinned default fallback profiles require (charCount + 1) * 3 and byteCount + 1 respectively, with native ArgumentOutOfRangeException on negative inputs or Int32 overflow. These are capacity bounds, not allocation requests.

Four emit/strict profiles produce 6,784 whole-array reference controls from the existing 847 UTF-16 vectors and null inputs. Another 112 controls cover zero, ordinary counts, the maximum valid byte bound, the next invalid value, Int32 extrema and the maximum valid character bound. The packaged consumer verifies 13,792 output/error and source-preservation groups.

The count formulas are qualified only for the selected default fallback profiles. Configurable fallback objects may change bounds and remain open, along with stateful conversion, span/pointer overloads, logical type identity, native source/value/array ABI and WP-05-T2 acceptance. No accepted task or framework qualification is credited. The next concrete task is native Encoding/UTF8Encoding/fallback-exception logical type lookup and metadata.
