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

    public static TimeSpan FromMicroseconds(double value) {
        return fromScaled(value, 10L);
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

    public TimeSpan Add(TimeSpan other) {
        if (other == null) {
            throw new ArgumentNullException("other");
        }
        try {
            return new TimeSpan(java.lang.Math.addExact(this.ticks, other.ticks));
        } catch (java.lang.ArithmeticException overflow) {
            throw new OverflowException("TimeSpan value was out of range.");
        }
    }

    public double get_TotalDays() {
        return (double) this.ticks / TICKS_PER_DAY;
    }

    public double get_TotalHours() {
        return (double) this.ticks / 36_000_000_000L;
    }

    public double get_TotalMinutes() {
        return (double) this.ticks / 600_000_000L;
    }

    public double get_TotalSeconds() {
        return (double) this.ticks / 10_000_000L;
    }

    public double get_TotalMilliseconds() {
        return (double) this.ticks / 10_000L;
    }

    public double get_TotalMicroseconds() {
        return (double) this.ticks / 10L;
    }

    public int get_Days() {
        return (int) (this.ticks / TICKS_PER_DAY);
    }

    public int get_Hours() {
        return (int) ((this.ticks / 36_000_000_000L) % 24L);
    }

    public int get_Minutes() {
        return (int) ((this.ticks / 600_000_000L) % 60L);
    }

    public int get_Seconds() {
        return (int) ((this.ticks / 10_000_000L) % 60L);
    }

    public int get_Milliseconds() {
        return (int) ((this.ticks / 10_000L) % 1_000L);
    }

    public int get_Microseconds() {
        return (int) ((this.ticks / 10L) % 1_000L);
    }

    public int get_Nanoseconds() {
        return (int) (this.ticks % 10L) * 100;
    }
}
