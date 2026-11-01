// SPDX-License-Identifier: MIT

package System.Threading.Tasks.Sources;

/** Selected System.Threading.Tasks.Sources.ValueTaskSourceOnCompletedFlags carrying the full raw Int32 value. */
public final class ValueTaskSourceOnCompletedFlags {
    public static final ValueTaskSourceOnCompletedFlags None = new ValueTaskSourceOnCompletedFlags(0);
    public static final ValueTaskSourceOnCompletedFlags UseSchedulingContext = new ValueTaskSourceOnCompletedFlags(1);
    public static final ValueTaskSourceOnCompletedFlags FlowExecutionContext = new ValueTaskSourceOnCompletedFlags(2);
    private final int code;

    public ValueTaskSourceOnCompletedFlags(int code) {
        this.code = code;
    }

    public int $raw() {
        return code;
    }

    public static ValueTaskSourceOnCompletedFlags op_BitwiseOr(ValueTaskSourceOnCompletedFlags left,
                                                               ValueTaskSourceOnCompletedFlags right) {
        return new ValueTaskSourceOnCompletedFlags(left.code | right.code);
    }

    public boolean Equals(Object other) {
        return other instanceof ValueTaskSourceOnCompletedFlags value && value.code == code;
    }

    @Override
    public boolean equals(Object other) {
        return Equals(other);
    }

    @Override
    public int hashCode() {
        return code;
    }
}
