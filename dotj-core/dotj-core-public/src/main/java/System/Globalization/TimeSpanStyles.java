// SPDX-License-Identifier: MIT

package System.Globalization;

/** Selected Int32 enum-value carrier; arbitrary values are retained for native validation. */
public final class TimeSpanStyles {
    public static final TimeSpanStyles None = new TimeSpanStyles(0);
    public static final TimeSpanStyles AssumeNegative = new TimeSpanStyles(1);
    private final int value;

    private TimeSpanStyles(int value) {
        this.value = value;
    }

    public static TimeSpanStyles FromInt32(int value) {
        return value == 0 ? None : value == 1 ? AssumeNegative : new TimeSpanStyles(value);
    }

    public int get_Value() {
        return this.value;
    }

    public String get_Name() {
        return this.value == 0 ? "None" : this.value == 1 ? "AssumeNegative" : Integer.toString(this.value);
    }

    public static TimeSpanStyles[] values() {
        return new TimeSpanStyles[] {None, AssumeNegative};
    }

    public String ToString() {
        return get_Name();
    }

    @Override
    public String toString() {
        return ToString();
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof TimeSpanStyles styles && styles.value == this.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
