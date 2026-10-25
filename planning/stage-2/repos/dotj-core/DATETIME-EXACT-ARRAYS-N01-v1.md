# Selected DateTime exact format arrays

Batch 2075 advances DJ-001-WP-05-T1; no acceptance task or release gate is accepted.

Four String/Character-view ParseExact and TryParseExact signatures accept String format arrays, provider and DateTimeStyles. The selected individual formats and style handling are shared with Batch 2074. Arrays are examined in order: the first success returns; a null/empty element encountered before success stops the search. Empty/null arrays and ordinary failure reset TryParseExact output to default. Invalid styles and malformed single-character formats throw while preserving the original output, even when an earlier candidate failed. A local candidate buffer prevents failed trials from changing caller storage before an exception. String ParseExact checks input null before formats null; styles are validated first.

The pinned native CoreLib 10.0.12 corpus has 3640 real String/span cases covering fourteen array sets, thirteen inputs and ten style values. Null and empty arrays remain distinct, as do true null and empty elements. The packaged consumer checks 10920 String and zero/offset Character-view groups, including native exception identity, HResult, parameter and output state, ticks/Kind and selected modern binary/UTC conversion. Public signatures are audited independently. The pinned upstream array loop was read directly from the verified source archive to corroborate ordering and delayed output assignment.

Arbitrary formats, providers/cultures, historical/other-zone conversion, Java/CLR array and byref language integration, complete foundation acceptance and release qualification remain open. Product runtime dependencies remain JDK-only.
