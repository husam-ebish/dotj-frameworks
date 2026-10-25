# Selected Byte character-span formatting

Batch 2140 adds ISpanFormattable projection and selected raw-array/interface/typed-view formatting. Short buffers return false with zero written and preserve storage; offset views preserve surrounding units. Invalid formats are checked before writes.

Pinned CoreLib 10.0.12 records 1,174 formatting buffers across fourteen numeric anchors and seventeen formats. Packaged consumers check 4,865 groups. The invariant profile also checks 84 selected Char/Byte span text views. Two mismatched destination/format calls must fail compilation. The UTF-8 interface remains omitted pending its separate implementation.

Other numeric APIs, formats/cultures, native generic interfaces, CLR byref lifetimes, task acceptance and release qualification remain open. The product remains JDK-only; development tools and intermediate artifacts stay on D:.
