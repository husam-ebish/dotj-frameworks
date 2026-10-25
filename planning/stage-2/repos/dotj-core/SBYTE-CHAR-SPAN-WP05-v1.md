# Selected SByte character-span formatting

Batch 2138 adds ISpanFormattable and raw/typed Char buffer routes for the selected SByte formatting profile. Formats are validated before writes; short destinations return false and zero written without modifying storage. Typed offset views preserve surrounding characters. The selected interface projection grows to IComparable/IConvertible/ISpanFormattable/IFormattable; the native UTF-8 interface remains omitted pending its own implementation.

Pinned CoreLib 10.0.12 records 1,218 buffer cases across fourteen signed-byte anchors and selected standard/invalid formats, plus 84 span text cases. Packaged consumers check 5,041 groups through raw arrays, interface calls and offset views. Two mismatched Byte/Char calls must fail compilation. Oracle provenance retains the native JSON fixture rather than a later compile-negative probe path.

The corpus uses invariant numeric symbols. Other culture/precision domains, native generic interfaces, CLR byref lifetimes, full numeric API and release qualification remain open. Product dependencies remain JDK-only; validation tools and intermediate artifacts stay on D:.
