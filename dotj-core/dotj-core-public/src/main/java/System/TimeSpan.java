// SPDX-License-Identifier: MIT

package System;

/** Immutable tick interval for the selected DateTime arithmetic candidate. */
public final class TimeSpan implements IComparable, ISpanFormattable, IUtf8SpanFormattable {
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

    public static TimeSpan FromDays(int days, int hours) {
        return FromDays(days, hours, 0L, 0L, 0L, 0L);
    }

    public static TimeSpan FromDays(int days, int hours, long minutes) {
        return FromDays(days, hours, minutes, 0L, 0L, 0L);
    }

    public static TimeSpan FromDays(int days, int hours, long minutes, long seconds) {
        return FromDays(days, hours, minutes, seconds, 0L, 0L);
    }

    public static TimeSpan FromDays(int days, int hours, long minutes, long seconds, long milliseconds) {
        return FromDays(days, hours, minutes, seconds, milliseconds, 0L);
    }

    public static TimeSpan FromDays(int days, int hours, long minutes, long seconds, long milliseconds, long microseconds) {
        return fromCompositeMicroseconds(new long[] {days, hours, minutes, seconds, milliseconds, microseconds},
                new long[] {MicrosecondsPerDay, MicrosecondsPerHour, MicrosecondsPerMinute, MicrosecondsPerSecond, MicrosecondsPerMillisecond, 1L});
    }

    public static TimeSpan FromHours(int hours, long minutes) {
        return FromHours(hours, minutes, 0L, 0L, 0L);
    }

    public static TimeSpan FromHours(int hours, long minutes, long seconds) {
        return FromHours(hours, minutes, seconds, 0L, 0L);
    }

    public static TimeSpan FromHours(int hours, long minutes, long seconds, long milliseconds) {
        return FromHours(hours, minutes, seconds, milliseconds, 0L);
    }

    public static TimeSpan FromHours(int hours, long minutes, long seconds, long milliseconds, long microseconds) {
        return fromCompositeMicroseconds(new long[] {hours, minutes, seconds, milliseconds, microseconds},
                new long[] {MicrosecondsPerHour, MicrosecondsPerMinute, MicrosecondsPerSecond, MicrosecondsPerMillisecond, 1L});
    }

    public static TimeSpan FromMinutes(long minutes, long seconds) {
        return FromMinutes(minutes, seconds, 0L, 0L);
    }

    public static TimeSpan FromMinutes(long minutes, long seconds, long milliseconds) {
        return FromMinutes(minutes, seconds, milliseconds, 0L);
    }

    public static TimeSpan FromMinutes(long minutes, long seconds, long milliseconds, long microseconds) {
        return fromCompositeMicroseconds(new long[] {minutes, seconds, milliseconds, microseconds},
                new long[] {MicrosecondsPerMinute, MicrosecondsPerSecond, MicrosecondsPerMillisecond, 1L});
    }

    public static TimeSpan FromSeconds(long seconds, long milliseconds) {
        return FromSeconds(seconds, milliseconds, 0L);
    }

    public static TimeSpan FromSeconds(long seconds, long milliseconds, long microseconds) {
        return fromCompositeMicroseconds(new long[] {seconds, milliseconds, microseconds},
                new long[] {MicrosecondsPerSecond, MicrosecondsPerMillisecond, 1L});
    }

    public static TimeSpan FromMilliseconds(long milliseconds, long microseconds) {
        return fromCompositeMicroseconds(new long[] {milliseconds, microseconds},
                new long[] {MicrosecondsPerMillisecond, 1L});
    }

    private static TimeSpan fromCompositeMicroseconds(long[] components, long[] scales) {
        java.math.BigInteger total = java.math.BigInteger.ZERO;
        for (int index = 0; index < components.length; index++) {
            total = total.add(java.math.BigInteger.valueOf(components[index])
                    .multiply(java.math.BigInteger.valueOf(scales[index])));
        }
        if (total.compareTo(java.math.BigInteger.valueOf(Long.MIN_VALUE / TicksPerMicrosecond)) < 0
                || total.compareTo(java.math.BigInteger.valueOf(Long.MAX_VALUE / TicksPerMicrosecond)) > 0) {
            throw new ArgumentOutOfRangeException(null, "TimeSpan value was out of range.");
        }
        return new TimeSpan(total.longValue() * TicksPerMicrosecond);
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
            throw new ArgumentException("Object must be of type TimeSpan.");
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
        int start = 0;
        int end = input.length();
        while (start < end && parseSpace(input.charAt(start))) { start++; }
        while (end > start && parseSpace(input.charAt(end - 1))) { end--; }
        String text = input.substring(start, end);
        boolean negative = text.startsWith("-");
        if (negative) { text = text.substring(1); }
        java.util.ArrayList<String> numbers = new java.util.ArrayList<>();
        java.util.ArrayList<String> separators = new java.util.ArrayList<>();
        java.util.regex.Matcher tokens = java.util.regex.Pattern.compile("[0-9]+|[^0-9]+").matcher(text);
        boolean expectNumber = true;
        while (tokens.find()) {
            String token = tokens.group();
            boolean number = token.charAt(0) >= '0' && token.charAt(0) <= '9';
            if (number != expectNumber) { throw new FormatException(); }
            if (number) {
                // The pinned parser bounds numeric tokens to 28 bits before component interpretation.
                if (new java.math.BigInteger(token).compareTo(java.math.BigInteger.valueOf(0x0fffffffL)) > 0) {
                    throw new OverflowException();
                }
                numbers.add(token);
                if (numbers.size() > 5) { throw new FormatException(); }
            } else {
                separators.add(token);
            }
            expectNumber = !expectNumber;
        }
        if (numbers.isEmpty() || expectNumber) { throw new FormatException(); }
        String shape = String.join("|", separators);
        java.util.ArrayList<String> layouts = new java.util.ArrayList<>();
        switch (numbers.size()) {
            case 1: layouts.add("d"); break;
            case 2: if (shape.equals(":")) { layouts.add("hm"); } break;
            case 3:
                if (shape.equals(":|:")) { layouts.add("hms"); layouts.add("dhm"); }
                if (shape.equals(".|:")) { layouts.add("dhm"); }
                if (shape.equals(":|:.")) { layouts.add("hmf"); }
                break;
            case 4:
                if (shape.equals(":|:|.")) { layouts.add("hmsf"); }
                if (shape.equals(".|:|:") || shape.equals(":|:|:")) { layouts.add("dhms"); }
                if (shape.equals(".|:|:.") || shape.equals(":|:|:.")) { layouts.add("dhmf"); }
                break;
            case 5:
                if (shape.equals(".|:|:|.") || shape.equals(":|:|:|.")) { layouts.add("dhmsf"); }
                break;
            default: break;
        }
        if (layouts.isEmpty()) { throw new FormatException(); }
        for (String layout : layouts) {
            java.math.BigInteger total = java.math.BigInteger.ZERO;
            boolean valid = true;
            for (int index = 0; index < layout.length(); index++) {
                String digits = numbers.get(index);
                long value = Long.parseLong(digits);
                long scale;
                switch (layout.charAt(index)) {
                    case 'd': valid &= value <= 10675199L; scale = TicksPerDay; break;
                    case 'h': valid &= value <= 23L; scale = TicksPerHour; break;
                    case 'm': valid &= value <= 59L; scale = TicksPerMinute; break;
                    case 's': valid &= value <= 59L; scale = TicksPerSecond; break;
                    default:
                        scale = 1L;
                        if (value == 0L) { break; }
                        int zeroes = 0;
                        while (digits.charAt(zeroes) == '0') { zeroes++; }
                        if (zeroes == 0 && value > 9999999L) { valid = false; break; }
                        if (digits.length() <= 7) {
                            value *= (long) java.lang.Math.pow(10, 7 - digits.length());
                        } else if (zeroes > 7) {
                            value = 0L;
                        } else {
                            long divisor = (long) java.lang.Math.pow(10, digits.length() - 7);
                            value = (value + divisor / 2L) / divisor;
                        }
                        break;
                }
                total = total.add(java.math.BigInteger.valueOf(value).multiply(java.math.BigInteger.valueOf(scale)));
            }
            if (negative) { total = total.negate(); }
            if (valid && total.compareTo(java.math.BigInteger.valueOf(Long.MIN_VALUE)) >= 0
                    && total.compareTo(java.math.BigInteger.valueOf(Long.MAX_VALUE)) <= 0) {
                return new TimeSpan(total.longValue());
            }
        }
        throw new OverflowException();
    }

    public static TimeSpan Parse(String input, IFormatProvider formatProvider) {
        if (formatProvider != null) { throw new UnsupportedOperationException("Only null-provider invariant parsing is mapped."); }
        return Parse(input);
    }

    public static TimeSpan Parse(ReadOnlySpan<Character> input) {
        return Parse(input, null);
    }

    public static TimeSpan Parse(ReadOnlySpan<Character> input, IFormatProvider formatProvider) {
        if (input == null) { throw new ArgumentNullException("input"); }
        return Parse(input.selectedText(), formatProvider);
    }

    private static boolean parseSpace(char value) {
        return value >= '\t' && value <= '\r' || value == '\u0085' || Character.isSpaceChar(value);
    }

    public static TimeSpan ParseExact(String input, String format, IFormatProvider formatProvider) {
        if (input == null) { throw new ArgumentNullException("input"); }
        if (format == null) { throw new ArgumentNullException("format"); }
        if (!format.equals("c") && !format.equals("t") && !format.equals("T")) {
            return parseCustomExact(input, format);
        }
        int start = 0;
        int end = input.length();
        while (start < end && (input.charAt(start) == ' ' || input.charAt(start) == '\t')) { start++; }
        while (end > start && (input.charAt(end - 1) == ' ' || input.charAt(end - 1) == '\t')) { end--; }
        String text = input.substring(start, end);
        int[] position = {0};
        boolean negative = text.startsWith("-");
        if (negative) { position[0]++; }
        long first = readConstantNumber(text, position, 10675199);
        long days = 0L, hours = 0L, minutes = 0L, seconds = 0L, fraction = 0L;
        boolean hasTime = false;
        if (position[0] < text.length() && text.charAt(position[0]) == ':') {
            hours = first;
            position[0]++;
            hasTime = true;
        } else if (position[0] < text.length() && text.charAt(position[0]) == '.') {
            days = first;
            position[0]++;
            hours = readConstantNumber(text, position, 23);
            if (position[0] == text.length() || text.charAt(position[0]++) != ':') { throw new FormatException(); }
            hasTime = true;
        } else {
            days = first;
        }
        if (hasTime) {
            if (hours > 23L) { throw new OverflowException(); }
            minutes = readConstantNumber(text, position, 59);
            if (position[0] < text.length() && text.charAt(position[0]) == ':') {
                position[0]++;
                if (position[0] == text.length() || text.charAt(position[0]) != '.') {
                    seconds = readConstantNumber(text, position, 59);
                }
                if (position[0] < text.length() && text.charAt(position[0]) == '.') {
                    position[0]++;
                    long scale = TicksPerSecond / 10L;
                    while (position[0] < text.length() && text.charAt(position[0]) >= '0' && text.charAt(position[0]) <= '9') {
                        if (scale == 0L) { throw new FormatException(); }
                        fraction += (text.charAt(position[0]++) - '0') * scale;
                        scale /= 10L;
                    }
                }
            }
        }
        if (position[0] != text.length()) { throw new FormatException(); }
        java.math.BigInteger total = java.math.BigInteger.valueOf(days).multiply(java.math.BigInteger.valueOf(TicksPerDay))
                .add(java.math.BigInteger.valueOf(hours * TicksPerHour + minutes * TicksPerMinute + seconds * TicksPerSecond + fraction));
        if (negative) { total = total.negate(); }
        if (total.compareTo(java.math.BigInteger.valueOf(Long.MIN_VALUE)) < 0
                || total.compareTo(java.math.BigInteger.valueOf(Long.MAX_VALUE)) > 0) { throw new OverflowException(); }
        return new TimeSpan(total.longValue());
    }

    private static TimeSpan parseCustomExact(String input, String format) {
        if (format.length() < 2) { throw new FormatException(); }
        long[] components = new long[5];
        boolean[] assigned = new boolean[5];
        int cursor = 0;
        for (int index = 0; index < format.length();) {
            char token = format.charAt(index++);
            if (token == '%') {
                if (index == format.length() || format.charAt(index) == '%') { throw new FormatException(); }
                continue;
            }
            if (token == '\\') {
                if (index == format.length() || cursor == input.length()
                        || input.charAt(cursor++) != format.charAt(index++)) { throw new FormatException(); }
                continue;
            }
            if (token == '\'' || token == '"') {
                boolean closed = false;
                while (index < format.length()) {
                    char literal = format.charAt(index++);
                    if (literal == token) { closed = true; break; }
                    if (literal == '\\') {
                        if (index == format.length()) { throw new FormatException(); }
                        literal = format.charAt(index++);
                    }
                    if (cursor == input.length() || input.charAt(cursor++) != literal) { throw new FormatException(); }
                }
                if (!closed) { throw new FormatException(); }
                continue;
            }
            int width = 1;
            while (index < format.length() && format.charAt(index) == token) { width++; index++; }
            int component;
            int minimum;
            int maximum;
            switch (token) {
                case 'd': component = 0; minimum = width; maximum = width == 1 ? 8 : width; break;
                case 'h': component = 1; minimum = width; maximum = width == 1 ? 2 : width; break;
                case 'm': component = 2; minimum = width; maximum = width == 1 ? 2 : width; break;
                case 's': component = 3; minimum = width; maximum = width == 1 ? 2 : width; break;
                case 'f': component = 4; minimum = width; maximum = width; break;
                case 'F': component = 4; minimum = 0; maximum = width; break;
                default: throw new FormatException();
            }
            int allowed = component == 0 ? 8 : component == 4 ? 7 : 2;
            if (width > allowed || assigned[component]) { throw new FormatException(); }
            assigned[component] = true;
            int digits = 0;
            long value = 0L;
            while (digits < maximum && cursor < input.length()) {
                char digit = input.charAt(cursor);
                if (digit < '0' || digit > '9') { break; }
                value = value * 10L + digit - '0';
                cursor++;
                digits++;
            }
            if (digits < minimum) { throw new FormatException(); }
            if (component == 4) {
                for (int padding = digits; padding < 7; padding++) { value *= 10L; }
            }
            components[component] = value;
        }
        if (cursor != input.length()) { throw new FormatException(); }
        if (components[1] > 23L || components[2] > 59L || components[3] > 59L) { throw new OverflowException(); }
        java.math.BigInteger total = java.math.BigInteger.valueOf(components[0])
                .multiply(java.math.BigInteger.valueOf(TicksPerDay))
                .add(java.math.BigInteger.valueOf(components[1] * TicksPerHour + components[2] * TicksPerMinute
                        + components[3] * TicksPerSecond + components[4]));
        if (total.compareTo(java.math.BigInteger.valueOf(Long.MAX_VALUE)) > 0) { throw new OverflowException(); }
        return new TimeSpan(total.longValue());
    }

    private static int readConstantNumber(String text, int[] position, int limit) {
        int start = position[0];
        int value = 0;
        while (position[0] < text.length()) {
            char digit = text.charAt(position[0]);
            if (digit < '0' || digit > '9') { break; }
            int next = digit - '0';
            if (value > (limit - next) / 10) { throw new OverflowException(); }
            value = value * 10 + next;
            position[0]++;
        }
        if (position[0] == start) { throw new FormatException(); }
        return value;
    }

    public static boolean TryParseExact(String input, String format, IFormatProvider formatProvider, TimeSpan[] result) {
        result[0] = Zero;
        if (input == null || format == null) { return false; }
        try {
            result[0] = ParseExact(input, format, formatProvider);
            return true;
        } catch (FormatException | OverflowException invalid) {
            return false;
        }
    }

    public static TimeSpan ParseExact(ReadOnlySpan<Character> input, ReadOnlySpan<Character> format,
            IFormatProvider formatProvider) {
        if (input == null) { throw new ArgumentNullException("input"); }
        if (format == null) { throw new ArgumentNullException("format"); }
        return ParseExact(input.selectedText(), format.selectedText(), formatProvider);
    }

    public static boolean TryParseExact(ReadOnlySpan<Character> input, ReadOnlySpan<Character> format,
            IFormatProvider formatProvider, TimeSpan[] result) {
        if (input == null) { throw new ArgumentNullException("input"); }
        if (format == null) { throw new ArgumentNullException("format"); }
        return TryParseExact(input.selectedText(), format.selectedText(), formatProvider, result);
    }

    public String ToString(String format) {
        return ToString(format, null);
    }

    @Override
    public String ToString(String format, IFormatProvider formatProvider) {
        if (format == null || format.isEmpty() || format.equals("c")
                || format.equals("t") || format.equals("T")) {
            return ToString();
        }
        if (format.length() > 1) {
            String result = customText(format);
            if (formatProvider == null) {
                return result;
            }
        }
        throw new FormatException("This candidate supports constant formats and null-provider custom formats.");
    }

    private String customText(String format) {
        return customText(format, false);
    }

    private String customText(String format, boolean byteEncoding) {
        // Components are magnitudes, including at MinValue. Custom patterns supply their own sign.
        long days = java.lang.Math.abs(this.ticks / TicksPerDay);
        long remainder = java.lang.Math.abs(this.ticks % TicksPerDay);
        String fraction = String.format(java.util.Locale.ROOT, "%07d", remainder % TicksPerSecond);
        StringBuilder output = new StringBuilder();
        for (int index = 0; index < format.length();) {
            char token = format.charAt(index++);
            if (token == '\\') {
                if (index == format.length()) {
                    throw new FormatException();
                }
                char literal = format.charAt(index++);
                output.append(byteEncoding ? (char) (literal & 0xff) : literal);
            } else if (token == '\'' || token == '"') {
                boolean closed = false;
                while (index < format.length()) {
                    char literal = format.charAt(index++);
                    if (literal == token) {
                        closed = true;
                        break;
                    }
                    if (literal == '\\') {
                        if (index == format.length()) {
                            throw new FormatException();
                        }
                        literal = format.charAt(index++);
                        output.append(byteEncoding ? (char) (literal & 0xff) : literal);
                    } else if (byteEncoding) {
                        if (Character.isSurrogate(literal)) {
                            throw new ArgumentOutOfRangeException("ch");
                        }
                        byte[] encoded = String.valueOf(literal).getBytes(java.nio.charset.StandardCharsets.UTF_8);
                        for (byte value : encoded) {
                            output.append((char) (value & 0xff));
                        }
                    } else {
                        output.append(literal);
                    }
                }
                if (!closed) {
                    throw new FormatException();
                }
            } else if (token == '%') {
                if (index == format.length() || format.charAt(index) == '%') {
                    throw new FormatException();
                }
                output.append(customText(format.substring(index, index + 1), byteEncoding));
                index++;
            } else {
                int count = 1;
                while (index < format.length() && format.charAt(index) == token) {
                    count++;
                    index++;
                }
                if (token == 'f' || token == 'F') {
                    if (count > 7) {
                        throw new FormatException();
                    }
                    String digits = fraction.substring(0, count);
                    if (token == 'F') {
                        int end = digits.length();
                        while (end > 0 && digits.charAt(end - 1) == '0') {
                            end--;
                        }
                        digits = digits.substring(0, end);
                    }
                    output.append(digits);
                } else {
                    long value;
                    switch (token) {
                        case 'd': value = days; break;
                        case 'h': value = remainder / TicksPerHour; break;
                        case 'm': value = remainder / TicksPerMinute % 60L; break;
                        case 's': value = remainder / TicksPerSecond % 60L; break;
                        default: throw new FormatException();
                    }
                    if (count > (token == 'd' ? 8 : 2)) {
                        throw new FormatException();
                    }
                    String digits = Long.toString(value);
                    output.append("0".repeat(java.lang.Math.max(0, count - digits.length()))).append(digits);
                }
            }
        }
        return output.toString();
    }

    @Override
    public boolean TryFormat(char[] destination, int[] charsWritten, String format,
            IFormatProvider provider) {
        String text = ToString(format, provider);
        if (text.length() > destination.length) {
            charsWritten[0] = 0;
            return false;
        }
        text.getChars(0, text.length(), destination, 0);
        charsWritten[0] = text.length();
        return true;
    }

    @Override
    public boolean TryFormat(byte[] destination, int[] bytesWritten, String format,
            IFormatProvider provider) {
        byte[] encoded;
        if (format != null && format.length() > 1 && provider == null) {
            // In the pinned UTF-8 formatter, quoted BMP literals are encoded while backslash
            // escapes use their low byte. Keep that distinction instead of re-encoding ToString.
            encoded = customText(format, true).getBytes(java.nio.charset.StandardCharsets.ISO_8859_1);
        } else {
            encoded = ToString(format, provider).getBytes(java.nio.charset.StandardCharsets.UTF_8);
        }
        if (encoded.length > destination.length) {
            bytesWritten[0] = 0;
            return false;
        }
        java.lang.System.arraycopy(encoded, 0, destination, 0, encoded.length);
        bytesWritten[0] = encoded.length;
        return true;
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

    public static boolean TryParse(String input, IFormatProvider formatProvider, TimeSpan[] result) {
        if (formatProvider != null) { throw new UnsupportedOperationException("Only null-provider invariant parsing is mapped."); }
        return TryParse(input, result);
    }

    public static boolean TryParse(ReadOnlySpan<Character> input, TimeSpan[] result) {
        return TryParse(input, null, result);
    }

    public static boolean TryParse(ReadOnlySpan<Character> input, IFormatProvider formatProvider, TimeSpan[] result) {
        if (input == null) { throw new ArgumentNullException("input"); }
        return TryParse(input.selectedText(), formatProvider, result);
    }

    /** One typed Java carrier for the selected CLR Char and Byte span signatures. */
    public <T> boolean TryFormat(Span<T> destination, int[] written,
            ReadOnlySpan<Character> format, IFormatProvider provider) {
        if (destination == null) { throw new ArgumentNullException("destination"); }
        if (format == null) { throw new ArgumentNullException("format"); }
        Object buffer = destination.selectedBufferCopy();
        boolean success = buffer instanceof char[] chars
                ? TryFormat(chars, written, format.selectedText(), provider)
                : TryFormat((byte[]) buffer, written, format.selectedText(), provider);
        destination.writeSelectedBuffer(buffer);
        return success;
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
