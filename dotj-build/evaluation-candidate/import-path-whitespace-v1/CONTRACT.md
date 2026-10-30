# FR-18-01: whitespace in a single expanded import path

This separate extension preserves every v1 producer, fixture, plan, observation,
lock, raw log and qualification artifact. It targets the sole final-review finding
FR-18-01; no task, acceptance, numbered batch or product credit is added.

The new manifest has four Default project cases: ASCII whitespace-only, ASCII
padding around `one.props`, NBSP-only, and NBSP padding around `one.props`.
The selected path must follow the pinned evaluator/tokenizer whitespace behavior,
while stored properties, captured Q and caller globals retain their original
whitespace. Empty-after-normalization has no filesystem target or Result.
Actual native error codes and coordinates must be observed before product mapping.

The versioned producer also emits the runtime's `System.Char.IsWhiteSpace` result
for every BMP code unit. This is a separate classifier observable, not an extra
project-case count. It supplies the finite native definition used by functional
controls and distinguishes NBSP from Java `trim`, `strip` and `isBlank` shortcuts.
Negative controls prevent silently trimming characters absent from that definition;
their public exception or error-code behavior is not qualified.

Conditions still precede all expansion/normalization/target access. One-pass
expansion, immutable properties/globals/snapshots, importing-file-relative
resolution, syntax refusals and sandbox/import policy remain unchanged.

The full suite must retain all 90 preceding comparison outcomes without a
disposition transition and add four new unique comparison keys, for 94 total.
Existing v1 evidence continues to reproduce its original 90-case result. The
additional classifier/condition/refusal assertions are controls, not invented
capture cases or acceptance credit. Default-only qualification and all previously
open public ABI, profile-combination, SDK, rights and task gates remain open.

The two fresh qualified native-v2 passes reproduced all four project cases and
the same 25-code-unit BMP whitespace definition. Both whitespace-only cases
failed with MSB4020 and an error at (2,3,0,0), without a successful Result or
selected import target. Both padded cases selected `one.props`, P=`selected`,
and Q retained the exact ASCII/NBSP padding supplied by the caller.

The captured native whitespace set is U+0009-U+000D, U+0020, U+0085, U+00A0,
U+1680, U+2000-U+200A, U+2028, U+2029, U+202F, U+205F and U+3000.
The evaluator trims this set only at the boundaries of the expanded path,
after conditions and before the empty-expression guard or filesystem resolution.
It neither trims stored property/global values nor recursively expands the result.
The consumer tests every observed whitespace code unit with a real path and
property-preservation assertion, plus negative U+001C/U+200B/U+FEFF controls
whose exception ABI is unqualified. These controls add no capture-case credit.

The first native-v1 attempt compiled and completed one pass, then its unchanged
512MiB resource guard refused pass2 before launch. That whole failed attempt is
preserved and contributes no qualified two-pass observation. The replacement
native-v2 used identical locked producer/input bytes and retained the same guards.
