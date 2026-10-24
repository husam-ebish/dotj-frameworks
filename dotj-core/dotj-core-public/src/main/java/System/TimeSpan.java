// SPDX-License-Identifier: MIT

package System;

/** Immutable tick interval for the selected DateTime arithmetic candidate. */
public final class TimeSpan {
    private static final long TICKS_PER_DAY = 864_000_000_000L;
    private final long ticks;

    public TimeSpan(long ticks) {
        this.ticks = ticks;
    }

    public static TimeSpan FromTicks(long ticks) {
        return new TimeSpan(ticks);
    }

    public static TimeSpan FromDays(double value) {
        return fromScaled(value, TICKS_PER_DAY);
    }

    public static TimeSpan FromHours(double value) {
        return fromScaled(value, 36_000_000_000L);
    }

    public static TimeSpan FromMinutes(double value) {
        return fromScaled(value, 600_000_000L);
    }

    public static TimeSpan FromSeconds(double value) {
        return fromScaled(value, 10_000_000L);
    }

    public static TimeSpan FromMilliseconds(double value) {
        return fromScaled(value, 10_000L);
    }

    private static TimeSpan fromScaled(double value, long ticksPerUnit) {
        double scaled = java.lang.Math.rint(value * ticksPerUnit);
        if (!Double.isFinite(scaled) || scaled < Long.MIN_VALUE
                || scaled >= 0x1.0p63) {
            throw new OverflowException("TimeSpan value was out of range.");
        }
        return new TimeSpan((long) scaled);
    }

    public long get_Ticks() {
        return this.ticks;
    }
}
