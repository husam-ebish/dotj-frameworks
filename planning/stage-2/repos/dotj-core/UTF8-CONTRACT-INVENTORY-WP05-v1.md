# UTF-8 contract and acceptance inventory

Batch 2161 derives fourteen System.Text declarations from pinned CoreLib 10.0.12: Encoding/UTF8Encoding, both fallback hierarchies, replacement and exception fallback types, exceptions, stateful Encoder/Decoder and fallback buffers. The fixture records native signatures, constructor lists, inheritance, public properties and four UTF8Encoding constructor profiles.

UTF8Encoding constructors select identifier emission and replacement versus exception behavior. Encoding.UTF8 is read-only and emits the three-byte UTF-8 identifier through GetPreamble. The inventory checks these defaults against the native fixture and reports candidate class presence separately from behavioral implementation. Class presence is not qualification. EncodingProfile/CultureProfile are internal planning labels and are not public facade names.

WP-05-T2 remains unaccepted. Invalid-input behavior, stateful conversion and flush, buffers, unsafe pointer and span overloads, normalization/culture vectors, source identity and CLR ABI require their own evidence. E01/E02/E03/N01 remain open; no implementation task or framework is credited. The next concrete feature is selected stateless UTF-8 replacement conversion, followed by strict fallback exception payloads.

The Java product requires only the JDK. The pinned .NET runtime, Python and PowerShell are validation tools. All temporary work stays on D:.
