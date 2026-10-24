// SPDX-License-Identifier: MIT

package System;

/** Immutable tick interval for the selected DateTime arithmetic candidate. */
public final class TimeSpan implements IComparable {
    public static final long NanosecondsPerTick = 100L;
    public static final long TicksPerMicrosecond = 10L;
    public static final long TicksPerMillisecond = 10_000L;
    public static final long TicksPerSecond = 10_000_000L;
    public static final long TicksPerMinute = 600_000_000L;
    public static final long TicksPerHour = 36_000_000_000L;
    public static final long TicksPerDay = 864_000_000_000L;
    public static final long MicrosecondsPerMillisecond = 1_000L;
    public static final long MicrosecondsPerSecond = 1_000_000L;
    public static final long MicrosecondsPerMinute = 60_000_000L;
    public static final long MicrosecondsPerHour = 3_600_000_000L;
    public static final long MicrosecondsPerDay = 86_400_000_000L;
    public static final long MillisecondsPerSecond = 1_000L;
    public static final long MillisecondsPerMinute = 60_000L;
    public static final long MillisecondsPerHour = 3_600_000L;
    public static final long MillisecondsPerDay = 86_400_000L;
    public static final long SecondsPerMinute = 60L;
    public static final long SecondsPerHour = 3_600L;
    public static final long SecondsPerDay = 86_400L;
    public static final long MinutesPerHour = 60L;
    public static final long MinutesPerDay = 1_440L;
    public static final int HoursPerDay = 24;
    public static final TimeSpan Zero = new TimeSpan(0L);
    public static final TimeSpan MaxValue = new TimeSpan(Long.MAX_VALUE);
    public static final TimeSpan MinValue = new TimeSpan(Long.MIN_VALUE);

    private static final long TICKS_PER_DAY = TicksPerDay;
    private static final java.util.regex.Pattern CONSTANT_PATTERN =
            java.util.regex.Pattern.compile("(-)?(?:(\\d+)\\.)?(\\d{1,2}):(\\d{2}):(\\d{2})(?:\\.(\\d{1,7}))?");
    private final long ticks;

    public TimeSpan() {
        this(0L);
    }

    public TimeSpan(long ticks) {
        this.ticks = ticks;
    }

    public TimeSpan(int hours, int minutes, int seconds) {
        this(0, hours, minutes, seconds, 0, 0);
    }

    public TimeSpan(int days, int hours, int minutes, int seconds) {
        this(days, hours, minutes, seconds, 0, 0);
    }

    public TimeSpan(int days, int hours, int minutes, int seconds, int milliseconds) {
        this(days, hours, minutes, seconds, milliseconds, 0);
    }

    public TimeSpan(int days, int hours, int minutes, int seconds,
            int milliseconds, int microseconds) {
        long totalMicroseconds = days * 86_400_000_000L + hours * 3_600_000_000L
                + minutes * 60_000_000L + seconds * 1_000_000L
                + milliseconds * 1_000L + microseconds;
        if (totalMicroseconds > Long.MAX_VALUE / 10L
                || totalMicroseconds < Long.MIN_VALUE / 10L) {
            throw new ArgumentOutOfRangeException(null, "TimeSpan value was out of range.");
        }
        this.ticks = totalMicroseconds * 10L;
    }

    public static TimeSpan FromTicks(long ticks) {
        return new TimeSpan(ticks);
    }

    public static TimeSpan FromDays(int days) {
        return fromUnits(days, TicksPerDay);
    }

    public static TimeSpan FromHours(int hours) {
        return fromUnits(hours, TicksPerHour);
    }

    public static TimeSpan FromMinutes(long minutes) {
        return fromUnits(minutes, TicksPerMinute);
    }

    public static TimeSpan FromSeconds(long seconds) {
        return fromUnits(seconds, TicksPerSecond);
    }

    public static TimeSpan FromMilliseconds(long milliseconds) {
        return fromUnits(milliseconds, TicksPerMillisecond);
    }

    public static TimeSpan FromMicroseconds(long microseconds) {
        return fromUnits(microseconds, TicksPerMicrosecond);
    }

    private static TimeSpan fromUnits(long value, long ticksPerUnit) {
        if (value < Long.MIN_VALUE / ticksPerUnit || value > Long.MAX_VALUE / ticksPerUnit) {
            throw new ArgumentOutOfRangeException(null, "TimeSpan value was out of range.");
        }
        return new TimeSpan(value * ticksPerUnit);
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
        if (Double.isNaN(value)) {
            throw new ArgumentException("TimeSpan does not accept floating point Not-a-Number values.");
        }
        return fromDoubleTicks(value * ticksPerUnit);
    }

    private static TimeSpan fromDoubleTicks(double ticks) {
        if (Double.isNaN(ticks) || ticks < (double) Long.MIN_VALUE
                || ticks > (double) Long.MAX_VALUE) {
            throw new OverflowException("TimeSpan value was out of range.");
        }
        if (ticks == (double) Long.MAX_VALUE) {
            return new TimeSpan(Long.MAX_VALUE);
        }
        return new TimeSpan((long) ticks);
    }

    public TimeSpan Multiply(double factor) {
        if (Double.isNaN(factor)) {
            throw new ArgumentException("TimeSpan does not accept a NaN factor.", "factor");
        }
        return fromDoubleTicks(java.lang.Math.rint(this.ticks * factor));
    }

    public TimeSpan Divide(double divisor) {
        if (Double.isNaN(divisor)) {
            throw new ArgumentException("TimeSpan does not accept a NaN divisor.", "divisor");
        }
        return fromDoubleTicks(java.lang.Math.rint(this.ticks / divisor));
    }

    public double Divide(TimeSpan ts) {
        if (ts == null) {
            throw new ArgumentNullException("ts");
        }
        return this.ticks / (double) ts.ticks;
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

    public TimeSpan Subtract(TimeSpan other) {
        if (other == null) {
            throw new ArgumentNullException("other");
        }
        try {
            return new TimeSpan(java.lang.Math.subtractExact(this.ticks, other.ticks));
        } catch (java.lang.ArithmeticException overflow) {
            throw new OverflowException("TimeSpan value was out of range.");
        }
    }

    public TimeSpan Duration() {
        if (this.ticks == Long.MIN_VALUE) {
            throw new OverflowException("TimeSpan value was out of range.");
        }
        return new TimeSpan(java.lang.Math.abs(this.ticks));
    }

    public TimeSpan Negate() {
        try {
            return new TimeSpan(java.lang.Math.negateExact(this.ticks));
        } catch (java.lang.ArithmeticException overflow) {
            throw new OverflowException("TimeSpan value was out of range.");
        }
    }

    public static int Compare(TimeSpan left, TimeSpan right) {
        if (left == null) {
            throw new ArgumentNullException("left");
        }
        if (right == null) {
            throw new ArgumentNullException("right");
        }
        return Long.compare(left.ticks, right.ticks);
    }

    public int CompareTo(TimeSpan other) {
        if (other == null) {
            throw new ArgumentNullException("other");
        }
        return Compare(this, other);
    }

    @Override
    public int CompareTo(Object obj) {
        if (obj == null) {
            return 1;
        }
        if (!(obj instanceof TimeSpan other)) {
            throw new ArgumentException("Object must be of type TimeSpan", "obj");
        }
        return Compare(this, other);
    }

    public static boolean Equals(TimeSpan left, TimeSpan right) {
        return left == right || (left != null && right != null
                && left.ticks == right.ticks);
    }

    public boolean Equals(TimeSpan other) {
        return Equals(this, other);
    }

    public boolean Equals(Object obj) {
        return obj instanceof TimeSpan other && Equals(other);
    }

    @Override
    public boolean equals(Object obj) {
        return Equals(obj);
    }

    public int GetHashCode() {
        return (int) (this.ticks ^ (this.ticks >>> 32));
    }

    @Override
    public int hashCode() {
        return GetHashCode();
    }

    public String ToString() {
        java.math.BigInteger magnitude = java.math.BigInteger.valueOf(this.ticks).abs();
        java.math.BigInteger[] dayParts = magnitude.divideAndRemainder(
                java.math.BigInteger.valueOf(TICKS_PER_DAY));
        long remainder = dayParts[1].longValue();
        long hours = remainder / 36_000_000_000L;
        remainder %= 36_000_000_000L;
        long minutes = remainder / 600_000_000L;
        remainder %= 600_000_000L;
        long seconds = remainder / 10_000_000L;
        long fractionalTicks = remainder % 10_000_000L;
        String result = String.format(java.util.Locale.ROOT, "%02d:%02d:%02d",
                hours, minutes, seconds);
        if (dayParts[0].signum() != 0) {
            result = dayParts[0] + "." + result;
        }
        if (fractionalTicks != 0L) {
            result += String.format(java.util.Locale.ROOT, ".%07d", fractionalTicks);
        }
        return this.ticks < 0L ? "-" + result : result;
    }

    public static TimeSpan Parse(String input) {
        if (input == null) {
            throw new ArgumentNullException("input");
        }
        java.util.regex.Matcher match = CONSTANT_PATTERN.matcher(input.strip());
        if (!match.matches()) {
            throw new FormatException("Input was not a valid TimeSpan constant.");
        }
        int hours = Integer.parseInt(match.group(3));
        int minutes = Integer.parseInt(match.group(4));
        int seconds = Integer.parseInt(match.group(5));
        if (hours > 23 || minutes > 59 || seconds > 59) {
            throw new FormatException("Input was not a valid TimeSpan constant.");
        }
        java.math.BigInteger days = match.group(2) == null
                ? java.math.BigInteger.ZERO : new java.math.BigInteger(match.group(2));
        java.math.BigInteger magnitude = days.multiply(
                java.math.BigInteger.valueOf(TICKS_PER_DAY));
        magnitude = magnitude.add(java.math.BigInteger.valueOf(hours * 36_000_000_000L
                + minutes * 600_000_000L + seconds * 10_000_000L));
        if (match.group(6) != null) {
            String fraction = match.group(6);
            magnitude = magnitude.add(new java.math.BigInteger(
                    fraction + "0000000".substring(fraction.length())));
        }
        if (match.group(1) != null) {
            magnitude = magnitude.negate();
        }
        if (magnitude.compareTo(java.math.BigInteger.valueOf(Long.MIN_VALUE)) < 0
                || magnitude.compareTo(java.math.BigInteger.valueOf(Long.MAX_VALUE)) > 0) {
            throw new OverflowException("TimeSpan value was out of range.");
        }
        return new TimeSpan(magnitude.longValue());
    }

    public static boolean TryParse(String input, TimeSpan[] result) {
        result[0] = new TimeSpan(0L);
        if (input == null) {
            return false;
        }
        try {
            result[0] = Parse(input);
            return true;
        } catch (FormatException | OverflowException expected) {
            return false;
        }
    }

    @Override
    public String toString() {
        return ToString();
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
        double value = (double) this.ticks / 10_000L;
        return java.lang.Math.max((double) (Long.MIN_VALUE / 10_000L),
                java.lang.Math.min(value, (double) (Long.MAX_VALUE / 10_000L)));
    }

    public double get_TotalMicroseconds() {
        return (double) this.ticks / 10L;
    }

    public double get_TotalNanoseconds() {
        return (double) this.ticks * 100L;
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
