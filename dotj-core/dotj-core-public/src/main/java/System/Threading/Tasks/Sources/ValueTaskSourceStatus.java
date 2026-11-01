// SPDX-License-Identifier: MIT

package System.Threading.Tasks.Sources;

/** Selected System.Threading.Tasks.Sources.ValueTaskSourceStatus carrying the full raw Int32 value. */
public final class ValueTaskSourceStatus {
    public static final ValueTaskSourceStatus Pending = new ValueTaskSourceStatus(0);
    public static final ValueTaskSourceStatus Succeeded = new ValueTaskSourceStatus(1);
    public static final ValueTaskSourceStatus Faulted = new ValueTaskSourceStatus(2);
    public static final ValueTaskSourceStatus Canceled = new ValueTaskSourceStatus(3);
    private final int code;

    public ValueTaskSourceStatus(int code) {
        this.code = code;
    }

    public int $raw() {
        return code;
    }

    public boolean Equals(Object other) {
        return other instanceof ValueTaskSourceStatus value && value.code == code;
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
