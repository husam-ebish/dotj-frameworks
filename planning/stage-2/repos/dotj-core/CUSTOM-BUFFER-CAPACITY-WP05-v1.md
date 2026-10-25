# Selected custom fallback small-destination behavior

Batch 2180 preserves custom fallback behavior when a UTF-8 destination has insufficient space. Entering the native fallback path on valid input can create a buffer even though no Fallback method is called. Encoder overflow attempts MovePrevious once per UTF-16 unit of the pending scalar and evaluates pending input/buffer state. Decoder overflow resets the fallback buffer before reporting insufficient capacity. Exceptions thrown by MovePrevious or Reset propagate.

An intentionally nonconforming encoder buffer which refuses rewind or reports zero Remaining can cause a native partial success. The bounded candidate reproduces those recorded outcomes without presenting the buffer as well behaved. Astral scalars remain atomic. Earlier output persists in destinations when later consumption or capacity checks fail.

Thirty-six native emitted profiles combine four replacement outputs and nine behaviors, including honest/refused/throwing rewind and throwing Reset. Seven capacities and two destination offsets across twelve UTF-16 and twenty byte inputs produce 16,128 native operations. The packaged consumer passes 64,584 groups, including exact factory/GetNextChar/Fallback/Remaining/MovePrevious/Reset calls, return values, failures and destination contents. The earlier fallback and UTF-8 suites remain regressions.

This is selected candidate evidence, not complete arbitrary-provider or stateful encoding qualification. Providers changing across count/write passes, custom reentrancy, complete metadata/source ABI, broader encoding families and WP-05-T2 acceptance remain open. No accepted task or qualified framework is credited. Next is provider changes between allocation passes and buffer reuse/reference observations.
