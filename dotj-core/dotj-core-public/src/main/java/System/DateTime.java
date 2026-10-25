// SPDX-License-Identifier: MIT

package System;

import java.time.LocalDate;
import System.Globalization.DateTimeStyles;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.time.format.ResolverStyle;

/** Bounded immutable DateTime candidate for a calendar date and invariant text. */
public final class DateTime implements IConvertible, IComparable, ISpanFormattable, IUtf8SpanFormattable {
    private static final long BINARY_TICK_CEILING = 0x4000_0000_0000_0000L;
    private static final long TICKS_PER_DAY = 864_000_000_000L;
    private static final long FILE_TIME_EPOCH_TICKS = 504_911_232_000_000_000L;
    private static final long OA_EPOCH_TICKS = 599_264_352_000_000_000L;
    private static final long OA_MIN_TICKS = 31_241_376_000_000_000L;
    private static final long MILLIS_PER_DAY = 86_400_000L;
    private static final long MAX_TICKS = 3_155_378_975_999_999_999L;
    private static final java.util.regex.Pattern ISO_LOCAL_PATTERN = java.util.regex.Pattern.compile(
            "([0-9]{4})-([0-9]{2})-([0-9]{2})(?:[Tt ]([0-9]{2}):([0-9]{2})(?::([0-9]{2})(?:\\.([0-9]+))?)?)?");
    public static final DateTime MinValue = new DateTime(0L);
    public static final DateTime MaxValue = new DateTime(MAX_TICKS);
    public static final DateTime UnixEpoch = new DateTime(621_355_968_000_000_000L, DateTimeKind.Utc);
    private final LocalDateTime date;
    private final DateTimeKind kind;
    private final boolean localOverlapDaylight;

    public DateTime() {
        this(0L);
    }

    public DateTime(long ticks) {
        this(ticks, DateTimeKind.Unspecified);
    }

    public DateTime(long ticks, DateTimeKind kind) {
        if (ticks < 0L || ticks > MAX_TICKS) {
            throw new ArgumentOutOfRangeException("ticks");
        }
        if (kind == null) {
            throw new ArgumentException("Invalid DateTime kind", "kind");
        }
        this.date = LocalDate.of(1, 1, 1).atStartOfDay()
                .plusDays(ticks / TICKS_PER_DAY)
                .plusNanos(ticks % TICKS_PER_DAY * 100L);
        this.kind = kind;
        this.localOverlapDaylight = false;
    }

    public DateTime(int year, int month, int day) {
        this(year, month, day, 0, 0, 0, 0, 0, DateTimeKind.Unspecified);
    }

    public DateTime(int year, int month, int day, int hourOfDay,
                    int minuteOfHour, int secondOfMinute) {
        this(year, month, day, hourOfDay, minuteOfHour, secondOfMinute, 0, 0, DateTimeKind.Unspecified);
    }

    public DateTime(int year, int month, int day, int hourOfDay,
                    int minuteOfHour, int secondOfMinute, int millisecondOfSecond) {
        this(year, month, day, hourOfDay, minuteOfHour, secondOfMinute, millisecondOfSecond, 0, DateTimeKind.Unspecified);
    }

    public DateTime(int year, int month, int day, int hour, int minute, int second, DateTimeKind kind) {
        this(year, month, day, hour, minute, second, 0, 0, kind);
    }

    public DateTime(int year, int month, int day, int hour, int minute, int second,
            int millisecond, DateTimeKind kind) {
        this(year, month, day, hour, minute, second, millisecond, 0, kind);
    }

    public DateTime(int year, int month, int day, int hour, int minute, int second,
            int millisecond, int microsecond) {
        this(year, month, day, hour, minute, second, millisecond, microsecond, DateTimeKind.Unspecified);
    }

    public DateTime(int year, int month, int day, int hour, int minute, int second,
            int millisecond, int microsecond, DateTimeKind kind) {
        if (kind == null) {
            throw new ArgumentException("Invalid DateTime kind", "kind");
        }
        LocalDateTime components;
        if (year < 1 || year > 9999) {
            throw new ArgumentOutOfRangeException(null, "Date components were out of range.");
        }
        try {
            components = LocalDate.of(year, month, day).atTime(hour, minute, second);
        } catch (java.time.DateTimeException invalid) {
            throw new ArgumentOutOfRangeException(null, "Date or time components were out of range.");
        }
        if (millisecond < 0 || millisecond > 999) {
            throw new ArgumentOutOfRangeException("millisecond");
        }
        if (microsecond < 0 || microsecond > 999) {
            throw new ArgumentOutOfRangeException("microsecond");
        }
        this.date = components.withNano(millisecond * 1_000_000 + microsecond * 1_000);
        this.kind = kind;
        this.localOverlapDaylight = false;
    }

    private DateTime(LocalDateTime date) {
        this(date, DateTimeKind.Unspecified);
    }

    private DateTime(LocalDateTime date, DateTimeKind kind) {
        this(date, kind, false);
    }

    private DateTime(LocalDateTime date, DateTimeKind kind, boolean localOverlapDaylight) {
        this.date = date;
        this.kind = kind;
        this.localOverlapDaylight = kind == DateTimeKind.Local && localOverlapDaylight;
    }

    public static DateTime SpecifyKind(DateTime value, DateTimeKind kind) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        if (kind == null) {
            throw new ArgumentException("Invalid DateTime kind", "kind");
        }
        return new DateTime(value.date, kind);
    }

    public static DateTime Parse(String text) {
        return Parse(text, null, DateTimeStyles.None);
    }

    private static DateTime selectedParseLocalIso(String text) {
        if (text == null) {
            throw new ArgumentNullException("s");
        }
        int start = 0;
        int end = text.length();
        while (start < end && parseSpace(text.charAt(start))) { start++; }
        while (end > start && parseSpace(text.charAt(end - 1))) { end--; }
        java.util.regex.Matcher match = ISO_LOCAL_PATTERN.matcher(text.substring(start, end));
        if (!match.matches()) {
            throw new FormatException("Input string was not in a correct format");
        }
        try {
            DateTime parsed = new DateTime(Integer.parseInt(match.group(1)), Integer.parseInt(match.group(2)),
                    Integer.parseInt(match.group(3)), match.group(4) == null ? 0 : Integer.parseInt(match.group(4)),
                    match.group(5) == null ? 0 : Integer.parseInt(match.group(5)),
                    match.group(6) == null ? 0 : Integer.parseInt(match.group(6)));
            String fraction = match.group(7);
            if (fraction != null) {
                int width = java.lang.Math.min(7, fraction.length());
                long ticks = Long.parseLong(fraction.substring(0, width))
                        * (long) java.lang.Math.pow(10, 7 - width);
                if (fraction.length() > 7 && fraction.charAt(7) >= '5') { ticks++; }
                parsed = parsed.AddTicks(ticks);
            }
            return parsed;
        } catch (ArgumentOutOfRangeException invalid) {
            throw new FormatException("Input string was not in a correct format");
        }
    }

    public static DateTime Parse(String s, IFormatProvider provider) {
        return Parse(s, provider, DateTimeStyles.None);
    }

    public static DateTime Parse(String s, IFormatProvider provider, DateTimeStyles styles) {
        int flags = selectedValidateStyles(styles);
        if (provider != null) throw new UnsupportedOperationException("Only null-provider invariant parsing is mapped.");
        if (s == null) throw new ArgumentNullException("s");
        int start = 0, end = s.length();
        while (start < end && parseSpace(s.charAt(start))) start++;
        while (end > start && parseSpace(s.charAt(end - 1))) end--;
        String text = s.substring(start, end);
        java.util.regex.Matcher zone = java.util.regex.Pattern.compile("([Zz]|[+-][0-9]{2}:[0-9]{2})$").matcher(text);
        String suffix = zone.find() ? zone.group(1) : null;
        DateTime parsed = selectedParseLocalIso(suffix == null ? text : text.substring(0, zone.start()));
        if (suffix != null) {
            boolean zulu = suffix.equalsIgnoreCase("Z");
            int seconds;
            try { seconds = zulu ? 0 : ZoneOffset.of(suffix).getTotalSeconds(); }
            catch (java.time.DateTimeException invalid) { throw new FormatException("Invalid date/time offset"); }
            if (Math.abs(seconds) > 14 * 3600) throw new FormatException("Invalid date/time offset");
            long utcTicks = parsed.get_Ticks() - seconds * 10_000_000L;
            if (utcTicks < 0 || utcTicks > MAX_TICKS) throw new FormatException("Date/time offset exceeds the selected range");
            DateTime utc = new DateTime(utcTicks, DateTimeKind.Utc);
            return (flags & 16) != 0 || zulu && (flags & 128) != 0 ? utc : utc.ToLocalTime();
        }
        if ((flags & 32) != 0) {
            DateTime local = new DateTime(parsed.date, DateTimeKind.Local);
            return (flags & 16) != 0 ? local.ToUniversalTime() : local;
        }
        if ((flags & 64) != 0) {
            DateTime utc = new DateTime(parsed.date, DateTimeKind.Utc);
            return (flags & 16) != 0 ? utc : utc.ToLocalTime();
        }
        return parsed;
    }

    private static int selectedValidateStyles(DateTimeStyles styles) {
        return selectedValidateStyles(styles, "styles");
    }

    private static int selectedValidateStyles(DateTimeStyles styles, String parameter) {
        if (styles == null) throw new ArgumentNullException(parameter);
        int flags = styles.get_Value();
        if ((flags & ~255) != 0 || (flags & 96) == 96 || (flags & 128) != 0 && (flags & 112) != 0) {
            throw new ArgumentException("DateTimeStyles combination is invalid", parameter);
        }
        return flags;
    }

    public static DateTime Parse(ReadOnlySpan<Character> s) {
        return Parse(s, null);
    }

    public static DateTime Parse(ReadOnlySpan<Character> s, IFormatProvider provider) {
        return Parse(s, provider, DateTimeStyles.None);
    }

    public static DateTime Parse(ReadOnlySpan<Character> s, IFormatProvider provider, DateTimeStyles styles) {
        selectedValidateStyles(styles);
        if (s == null) throw new ArgumentNullException("s");
        return Parse(s.selectedText(), provider, styles);
    }

    private static boolean parseSpace(char value) {
        return value >= '\t' && value <= '\r' || value == '\u0085' || Character.isSpaceChar(value);
    }

    public static boolean TryParse(String text, DateTime[] result) {
        return TryParse(text, null, DateTimeStyles.None, result);
    }

    public static boolean TryParse(String s, IFormatProvider provider, DateTime[] result) {
        return TryParse(s, provider, DateTimeStyles.None, result);
    }

    public static boolean TryParse(String s, IFormatProvider provider, DateTimeStyles styles, DateTime[] result) {
        selectedValidateStyles(styles);
        if (provider != null) throw new UnsupportedOperationException("Only null-provider invariant parsing is mapped.");
        result[0] = new DateTime(0L);
        if (s == null) return false;
        try { result[0] = Parse(s, provider, styles); return true; }
        catch (FormatException invalid) { return false; }
    }

    public static boolean TryParse(ReadOnlySpan<Character> s, DateTime[] result) {
        return TryParse(s, null, result);
    }

    public static boolean TryParse(ReadOnlySpan<Character> s, IFormatProvider provider, DateTime[] result) {
        return TryParse(s, provider, DateTimeStyles.None, result);
    }

    public static boolean TryParse(ReadOnlySpan<Character> s, IFormatProvider provider, DateTimeStyles styles, DateTime[] result) {
        selectedValidateStyles(styles);
        if (s == null) throw new ArgumentNullException("s");
        return TryParse(s.selectedText(), provider, styles, result);
    }

    public static DateTime ParseExact(String text, String format, IFormatProvider provider) {
        return ParseExact(text, format, provider, DateTimeStyles.None);
    }

    public static DateTime ParseExact(String text, String format, IFormatProvider provider, DateTimeStyles styles) {
        int flags = selectedValidateStyles(styles, "style");
        if (provider != null) throw new UnsupportedOperationException("Only null-provider invariant exact parsing is mapped.");
        if (text == null) throw new ArgumentNullException("s");
        if (format == null) throw new ArgumentNullException("format");
        int start = 0, end = text.length();
        if ((flags & 5) != 0) while (start < end && parseSpace(text.charAt(start))) start++;
        if ((flags & 2) != 0) while (end > start && parseSpace(text.charAt(end - 1))) end--;
        String input = text.substring(start, end);
        boolean inner = (flags & 4) != 0;
        String white = inner ? "\\s*" : "";
        String date = "([0-9]{4})" + white + "-" + white + "([0-9]{2})" + white + "-" + white + "([0-9]{2})";
        String time = "([0-9]{2})" + white + ":" + white + "([0-9]{2})" + white + ":" + white + "([0-9]{2})";
        boolean hasTime, fraction, roundTrip;
        String separator;
        switch (format) {
            case "yyyy-MM-dd" -> { hasTime = false; fraction = false; roundTrip = false; separator = ""; }
            case "yyyy-MM-dd HH:mm:ss" -> { hasTime = true; fraction = false; roundTrip = false; separator = inner ? white : (flags & 2) != 0 ? " ?" : " "; }
            case "s" -> { hasTime = true; fraction = false; roundTrip = false; separator = white + "T" + white; }
            case "yyyy-MM-ddTHH:mm:ss.fffffff" -> { hasTime = true; fraction = true; roundTrip = false; separator = white + "T" + white; }
            case "o", "O" -> { hasTime = true; fraction = true; roundTrip = true; separator = white + "T" + white; }
            default -> throw new FormatException("Format is not mapped for selected exact parsing");
        }
        String pattern = date + (hasTime ? separator + time : "")
                + (fraction ? white + "\\." + white + "([0-9]{7})" : "")
                + (roundTrip ? "(?:" + white + "(Z|[+-][0-9]{2}:[0-9]{2}))?" : "");
        java.util.regex.Matcher match = java.util.regex.Pattern.compile(pattern).matcher(input);
        if (!match.matches()) throw new FormatException("Input string was not in the selected exact format");
        String canonical = match.group(1) + "-" + match.group(2) + "-" + match.group(3);
        if (hasTime) canonical += "T" + match.group(4) + ":" + match.group(5) + ":" + match.group(6);
        if (fraction) canonical += "." + match.group(7);
        if (roundTrip && match.group(8) != null) canonical += match.group(8);
        return Parse(canonical, provider, styles);
    }

    public static boolean TryParseExact(String text, String format, IFormatProvider provider, DateTime[] result) {
        return TryParseExact(text, format, provider, DateTimeStyles.None, result);
    }

    public static boolean TryParseExact(String text, String format, IFormatProvider provider, DateTimeStyles styles, DateTime[] result) {
        selectedValidateStyles(styles, "style");
        if (provider != null) throw new UnsupportedOperationException("Only null-provider invariant exact parsing is mapped.");
        if (text != null && !text.isEmpty() && format != null && format.length() == 1
                && "dDfFgGmMoOrRstTuUyY".indexOf(format.charAt(0)) < 0) {
            throw new FormatException("Input string was not in a correct format");
        }
        result[0] = new DateTime(0L);
        if (text == null || format == null) return false;
        try { result[0] = ParseExact(text, format, provider, styles); return true; }
        catch (FormatException invalid) { return false; }
    }

    public static DateTime ParseExact(ReadOnlySpan<Character> s, ReadOnlySpan<Character> format, IFormatProvider provider) {
        return ParseExact(s, format, provider, DateTimeStyles.None);
    }

    public static DateTime ParseExact(ReadOnlySpan<Character> s, ReadOnlySpan<Character> format, IFormatProvider provider, DateTimeStyles styles) {
        selectedValidateStyles(styles, "style");
        if (s == null) throw new ArgumentNullException("s");
        if (format == null) throw new ArgumentNullException("format");
        return ParseExact(s.selectedText(), format.selectedText(), provider, styles);
    }

    public static boolean TryParseExact(ReadOnlySpan<Character> s, ReadOnlySpan<Character> format, IFormatProvider provider, DateTime[] result) {
        return TryParseExact(s, format, provider, DateTimeStyles.None, result);
    }

    public static boolean TryParseExact(ReadOnlySpan<Character> s, ReadOnlySpan<Character> format, IFormatProvider provider, DateTimeStyles styles, DateTime[] result) {
        selectedValidateStyles(styles, "style");
        if (s == null) throw new ArgumentNullException("s");
        if (format == null) throw new ArgumentNullException("format");
        return TryParseExact(s.selectedText(), format.selectedText(), provider, styles, result);
    }

    public static DateTime FromBinary(long dateData) {
        long ticks = dateData & 0x3fff_ffff_ffff_ffffL;
        if ((dateData & Long.MIN_VALUE) != 0L) {
            if (ticks > BINARY_TICK_CEILING - TICKS_PER_DAY) { ticks -= BINARY_TICK_CEILING; }
            LocalDateTime utc = LocalDate.of(1, 1, 1).atStartOfDay()
                    .plusDays(java.lang.Math.floorDiv(ticks, TICKS_PER_DAY))
                    .plusNanos(java.lang.Math.floorMod(ticks, TICKS_PER_DAY) * 100L);
            ZoneId zone = ZoneId.systemDefault();
            java.time.ZonedDateTime converted = utc.atZone(ZoneOffset.UTC).withZoneSameInstant(zone);
            LocalDateTime local = converted.toLocalDateTime();
            if (local.getYear() < 1) { local = local.plusDays(1); }
            else if (local.getYear() > 9999) { local = local.minusDays(1); }
            if (local.getYear() < 1 || local.getYear() > 9999) {
                throw new ArgumentException("Invalid binary date value", "dateData");
            }
            boolean daylightOverlap = zone.getRules().getValidOffsets(local).size() > 1
                    && zone.getRules().isDaylightSavings(converted.toInstant());
            return new DateTime(local, DateTimeKind.Local, daylightOverlap);
        }
        if (ticks > MAX_TICKS) { throw new ArgumentException("Invalid binary date value", "dateData"); }
        return new DateTime(ticks, (dateData & BINARY_TICK_CEILING) == 0L ? DateTimeKind.Unspecified : DateTimeKind.Utc);
    }

    public static DateTime FromFileTimeUtc(long fileTime) {
        if (fileTime < 0 || fileTime > MAX_TICKS - FILE_TIME_EPOCH_TICKS) {
            throw new ArgumentOutOfRangeException("fileTime");
        }
        return SpecifyKind(new DateTime(1, 1, 1)
                .AddTicks(fileTime + FILE_TIME_EPOCH_TICKS), DateTimeKind.Utc);
    }

    public static DateTime FromFileTime(long fileTime) {
        DateTime utc = FromFileTimeUtc(fileTime);
        try {
            return utc.ToLocalTime();
        } catch (ArgumentOutOfRangeException overflow) {
            throw new ArgumentOutOfRangeException("fileTime");
        }
    }

    public static DateTime FromOADate(double value) {
        if (!(value < 2_958_466.0) || !(value > -657_435.0)) {
            throw new ArgumentException("Invalid OLE Automation date");
        }
        long millis = (long) (value * MILLIS_PER_DAY
                + (value >= 0 ? 0.5 : -0.5));
        if (millis < 0) {
            millis -= (millis % MILLIS_PER_DAY) * 2;
        }
        millis += OA_EPOCH_TICKS / 10_000L;
        if (millis < 0 || millis > MAX_TICKS / 10_000L) {
            throw new ArgumentException("Invalid OLE Automation date scale");
        }
        return new DateTime(1, 1, 1).AddTicks(millis * 10_000L);
    }

    public static boolean IsLeapYear(int year) {
        if (year < 1 || year > 9999) {
            throw new ArgumentOutOfRangeException("year");
        }
        return java.time.Year.isLeap(year);
    }

    public static int DaysInMonth(int year, int month) {
        if (month < 1 || month > 12) {
            throw new ArgumentOutOfRangeException("month");
        }
        if (year < 1 || year > 9999) {
            throw new ArgumentOutOfRangeException("year");
        }
        return java.time.YearMonth.of(year, month).lengthOfMonth();
    }

    public static int Compare(DateTime left, DateTime right) {
        if (left == null) {
            throw new ArgumentNullException("left");
        }
        if (right == null) {
            throw new ArgumentNullException("right");
        }
        return Long.compare(left.get_Ticks(), right.get_Ticks());
    }

    public int CompareTo(DateTime other) {
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
        if (!(obj instanceof DateTime other)) {
            throw new ArgumentException("Object must be of type DateTime.");
        }
        return Compare(this, other);
    }

    public static boolean Equals(DateTime left, DateTime right) {
        return left == right || (left != null && right != null
                && left.get_Ticks() == right.get_Ticks());
    }

    public boolean Equals(DateTime other) {
        return Equals(this, other);
    }

    public boolean Equals(Object obj) {
        return obj instanceof DateTime other && Equals(other);
    }

    @Override
    public boolean equals(Object obj) {
        return Equals(obj);
    }

    public int GetHashCode() {
        long ticks = this.get_Ticks();
        return (int) (ticks ^ (ticks >>> 32));
    }

    @Override
    public int hashCode() {
        return GetHashCode();
    }

    public DateTime AddTicks(long value) {
        long result;
        try {
            result = java.lang.Math.addExact(this.get_Ticks(), value);
        } catch (java.lang.ArithmeticException overflow) {
            throw new ArgumentOutOfRangeException("value");
        }
        if (result < 0 || result > MAX_TICKS) {
            throw new ArgumentOutOfRangeException("value");
        }
        LocalDateTime added = LocalDate.of(1, 1, 1).atStartOfDay()
                .plusDays(result / TICKS_PER_DAY)
                .plusNanos((result % TICKS_PER_DAY) * 100L);
        return new DateTime(added, this.kind, this.localOverlapDaylight);
    }

    public DateTime Add(TimeSpan value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        return this.AddTicks(value.get_Ticks());
    }

    public DateTime Subtract(TimeSpan value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        long inverse;
        try {
            inverse = java.lang.Math.negateExact(value.get_Ticks());
        } catch (java.lang.ArithmeticException overflow) {
            throw new ArgumentOutOfRangeException("value");
        }
        return this.AddTicks(inverse);
    }

    public TimeSpan Subtract(DateTime value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        return TimeSpan.FromTicks(this.get_Ticks() - value.get_Ticks());
    }

    public DateTime AddMonths(int months) {
        if (months < -120_000 || months > 120_000) {
            throw new ArgumentOutOfRangeException("months");
        }
        LocalDateTime added = this.date.plusMonths(months);
        if (added.getYear() < 1 || added.getYear() > 9999) {
            throw new ArgumentOutOfRangeException("months");
        }
        return new DateTime(added, this.kind, this.localOverlapDaylight);
    }

    public DateTime AddYears(int value) {
        if (value < -10_000 || value > 10_000) {
            throw new ArgumentOutOfRangeException("value");
        }
        LocalDateTime added = this.date.plusYears(value);
        if (added.getYear() < 1 || added.getYear() > 9999) {
            throw new ArgumentOutOfRangeException("value");
        }
        return new DateTime(added, this.kind, this.localOverlapDaylight);
    }

    public DateTime AddDays(double value) {
        return addScaled(value, TICKS_PER_DAY);
    }

    public DateTime AddHours(double value) {
        return addScaled(value, 36_000_000_000L);
    }

    public DateTime AddMinutes(double value) {
        return addScaled(value, 600_000_000L);
    }

    public DateTime AddSeconds(double value) {
        return addScaled(value, 10_000_000L);
    }

    public DateTime AddMilliseconds(double value) {
        return addScaled(value, 10_000L);
    }

    public DateTime AddMicroseconds(double value) {
        return addScaled(value, 10L);
    }

    private DateTime addScaled(double value, long ticksPerUnit) {
        if (Double.isNaN(value)) {
            return new DateTime(this.date, this.kind);
        }
        if (java.lang.Math.abs(value) > (double) (MAX_TICKS / ticksPerUnit)) {
            throw new ArgumentOutOfRangeException("value");
        }
        long wholeUnits = (long) value;
        double remainder = value - wholeUnits;
        long offset = wholeUnits * ticksPerUnit + (long) (remainder * ticksPerUnit);
        return AddTicks(offset);
    }

    public static DateTime get_UtcNow() {
        LocalDateTime value = LocalDateTime.now(ZoneOffset.UTC);
        return new DateTime(value.withNano(value.getNano() / 100 * 100), DateTimeKind.Utc);
    }

    public static DateTime get_Now() {
        return get_UtcNow().ToLocalTime();
    }

    public static DateTime get_Today() {
        return get_Now().get_Date();
    }

    public int get_Year() {
        return this.date.getYear();
    }

    public int get_Month() {
        return this.date.getMonthValue();
    }

    public int get_Day() {
        return this.date.getDayOfMonth();
    }

    public int get_DayOfYear() {
        return this.date.getDayOfYear();
    }

    public DayOfWeek get_DayOfWeek() {
        return DayOfWeek.values()[this.date.getDayOfWeek().getValue() % 7];
    }

    public TimeSpan get_TimeOfDay() {
        return TimeSpan.FromTicks(this.date.toLocalTime().toNanoOfDay() / 100L);
    }

    public DateTime get_Date() {
        return new DateTime(this.date.toLocalDate().atStartOfDay(), this.kind, this.localOverlapDaylight);
    }

    public DateTimeKind get_Kind() {
        return this.kind;
    }

    public long get_Ticks() {
        long days = this.date.toLocalDate().toEpochDay()
                - LocalDate.of(1, 1, 1).toEpochDay();
        return days * 864_000_000_000L
                + this.date.toLocalTime().toNanoOfDay() / 100L;
    }

    public long ToBinary() {
        if (this.kind == DateTimeKind.Local) {
            long storedTicks = this.get_Ticks() - selectedLocalOffset(ZoneId.systemDefault()).getTotalSeconds() * 10_000_000L;
            if (storedTicks < 0L) { storedTicks += BINARY_TICK_CEILING; }
            return storedTicks | Long.MIN_VALUE;
        }
        return this.get_Ticks() | (this.kind == DateTimeKind.Utc ? BINARY_TICK_CEILING : 0L);
    }

    public long ToFileTimeUtc() {
        long ticks = this.kind == DateTimeKind.Local
                ? this.ToUniversalTime().get_Ticks() : this.get_Ticks();
        if (ticks < FILE_TIME_EPOCH_TICKS) {
            throw new ArgumentOutOfRangeException("fileTime");
        }
        return ticks - FILE_TIME_EPOCH_TICKS;
    }

    public long ToFileTime() {
        if (this.kind == DateTimeKind.Utc) {
            return this.ToFileTimeUtc();
        }
        ZoneId zone = ZoneId.systemDefault();
        LocalDateTime utc = LocalDateTime.ofInstant(this.date.toInstant(selectedLocalOffset(zone)), ZoneOffset.UTC);
        if (utc.getYear() < 1 || utc.getYear() > 9999) {
            throw new ArgumentOutOfRangeException("fileTime");
        }
        return new DateTime(utc).ToFileTimeUtc();
    }

    public DateTime ToUniversalTime() {
        if (this.kind == DateTimeKind.Utc) {
            return this;
        }
        ZoneId zone = ZoneId.systemDefault();
        LocalDateTime utc = LocalDateTime.ofInstant(this.date.toInstant(selectedLocalOffset(zone)), ZoneOffset.UTC);
        if (utc.getYear() < 1) { return new DateTime(0L, DateTimeKind.Utc); }
        if (utc.getYear() > 9999) { return new DateTime(MAX_TICKS, DateTimeKind.Utc); }
        return new DateTime(utc, DateTimeKind.Utc);
    }

    public DateTime ToLocalTime() {
        if (this.kind == DateTimeKind.Local) {
            return this;
        }
        ZoneId zone = ZoneId.systemDefault();
        java.time.ZonedDateTime zoned = this.date.atZone(ZoneOffset.UTC).withZoneSameInstant(zone);
        LocalDateTime local = zoned.toLocalDateTime();
        if (local.getYear() < 1) { return new DateTime(0L, DateTimeKind.Local); }
        if (local.getYear() > 9999) { return new DateTime(MAX_TICKS, DateTimeKind.Local); }
        boolean daylightOverlap = zone.getRules().getValidOffsets(local).size() > 1
                && zone.getRules().isDaylightSavings(zoned.toInstant());
        return new DateTime(local, DateTimeKind.Local, daylightOverlap);
    }

    public boolean IsDaylightSavingTime() {
        if (this.kind == DateTimeKind.Utc) {
            return false;
        }
        ZoneId zone = ZoneId.systemDefault();
        if (zone.getRules().getValidOffsets(this.date).isEmpty()) { return false; }
        return zone.getRules().isDaylightSavings(this.date.toInstant(selectedLocalOffset(zone)));
    }

    private ZoneOffset selectedLocalOffset(ZoneId zone) {
        java.time.zone.ZoneRules rules = zone.getRules();
        java.util.List<ZoneOffset> offsets = rules.getValidOffsets(this.date);
        if (offsets.isEmpty()) { return rules.getTransition(this.date).getOffsetBefore(); }
        if (offsets.size() == 1) { return offsets.get(0); }
        boolean daylight = this.kind == DateTimeKind.Local && this.localOverlapDaylight;
        for (ZoneOffset offset : offsets) {
            if (rules.isDaylightSavings(this.date.toInstant(offset)) == daylight) { return offset; }
        }
        return offsets.get(offsets.size() - 1);
    }

    public void Deconstruct(int[] year, int[] month, int[] day) {
        year[0] = this.get_Year();
        month[0] = this.get_Month();
        day[0] = this.get_Day();
    }

    public double ToOADate() {
        long ticks = this.get_Ticks();
        if (ticks == 0) {
            return 0.0;
        }
        if (ticks < TICKS_PER_DAY) {
            ticks += OA_EPOCH_TICKS;
        }
        if (ticks < OA_MIN_TICKS) {
            throw new OverflowException("Not a valid OLE Automation date.");
        }
        long millis = (ticks - OA_EPOCH_TICKS) / 10_000L;
        if (millis < 0) {
            long fraction = millis % MILLIS_PER_DAY;
            if (fraction != 0) {
                millis -= (MILLIS_PER_DAY + fraction) * 2;
            }
        }
        return (double) millis / MILLIS_PER_DAY;
    }

    public int get_Hour() {
        return this.date.getHour();
    }

    public int get_Minute() {
        return this.date.getMinute();
    }

    public int get_Second() {
        return this.date.getSecond();
    }

    public int get_Millisecond() {
        return this.date.getNano() / 1_000_000;
    }

    public int get_Microsecond() {
        return (this.date.getNano() / 1_000) % 1_000;
    }

    public int get_Nanosecond() {
        return this.date.getNano() % 1_000;
    }

    @Override
    public TypeCode GetTypeCode() {
        return TypeCode.DateTime;
    }

    @Override
    public boolean ToBoolean(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to Boolean");
    }

    @Override
    public char ToChar(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to Char");
    }

    @Override
    public byte ToSByte(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to SByte");
    }

    @Override
    public short ToByte(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to Byte");
    }

    @Override
    public short ToInt16(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to Int16");
    }

    @Override
    public int ToUInt16(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to UInt16");
    }

    @Override
    public int ToInt32(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to Int32");
    }

    @Override
    public long ToUInt32(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to UInt32");
    }

    @Override
    public long ToInt64(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to Int64");
    }

    @Override
    public java.math.BigInteger ToUInt64(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to UInt64");
    }

    @Override
    public float ToSingle(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to Single");
    }

    @Override
    public double ToDouble(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to Double");
    }

    @Override
    public Decimal ToDecimal(IFormatProvider provider) {
        throw new InvalidCastException("DateTime cannot be converted to Decimal");
    }

    @Override
    public DateTime ToDateTime(IFormatProvider provider) {
        return new DateTime(this.date, this.kind, this.localOverlapDaylight);
    }

    public String ToString() {
        return ToString((IFormatProvider) null);
    }

    public String ToString(String format) {
        return ToString(format, null);
    }

    @Override
    public String toString() {
        return ToString();
    }

    @Override
    public String ToString(IFormatProvider provider) {
        return String.format(java.util.Locale.ROOT, "%02d/%02d/%04d %02d:%02d:%02d",
                this.get_Month(), this.get_Day(), this.get_Year(),
                this.get_Hour(), this.get_Minute(), this.get_Second());
    }

    @Override
    public Object ToType(Type conversionType, IFormatProvider provider) {
        if (conversionType == null) {
            throw new ArgumentNullException("targetType");
        }
        if (conversionType == Type.GetType("System.DateTime")) {
            return this.ToDateTime(provider);
        }
        if (conversionType == Type.GetType("System.Object")) {
            return this;
        }
        if (conversionType == Type.GetType("System.String")) {
            return this.ToString(provider);
        }
        throw new InvalidCastException("DateTime target type is not mapped");
    }

    public String ToString(String format, IFormatProvider provider) {
        if (format == null || format.isEmpty()) {
            return ToString(provider);
        }
        if (format.length() == 1) {
            String text = switch (format.charAt(0)) {
                case 'd' -> ToShortDateString();
                case 'D' -> ToLongDateString();
                case 'f' -> ToLongDateString() + " " + ToShortTimeString();
                case 'F' -> ToLongDateString() + " " + ToLongTimeString();
                case 'g' -> ToShortDateString() + " " + ToShortTimeString();
                case 'G' -> ToString(provider);
                case 'm', 'M' -> this.date.format(DateTimeFormatter.ofPattern("MMMM dd", java.util.Locale.US));
                case 't' -> ToShortTimeString();
                case 'T' -> ToLongTimeString();
                case 'y', 'Y' -> this.date.format(DateTimeFormatter.ofPattern("uuuu MMMM", java.util.Locale.US));
                case 'o', 'O' -> selectedRoundTripText(provider);
                case 'r', 'R' -> this.date.format(DateTimeFormatter.ofPattern("EEE, dd MMM uuuu HH:mm:ss 'GMT'", java.util.Locale.US));
                case 'u' -> ToString("yyyy-MM-dd HH:mm:ss", provider) + "Z";
                case 'U' -> ToUniversalTime().ToString("F", provider);
                default -> null;
            };
            if (text != null) return text;
        }
        if ("yyyy-MM-dd".equals(format)) {
            return this.date.format(DateTimeFormatter.ISO_LOCAL_DATE);
        }
        if ("yyyy-MM-dd HH:mm:ss".equals(format)) {
            return this.date.format(DateTimeFormatter.ofPattern(format, java.util.Locale.ROOT));
        }
        if ("yyyy-MM-dd HH:mm:ss.fff".equals(format)) {
            return this.date.format(DateTimeFormatter.ofPattern(
                    "yyyy-MM-dd HH:mm:ss.SSS", java.util.Locale.ROOT));
        }
        if ("s".equals(format) || "yyyy-MM-dd'T'HH:mm:ss".equals(format)) {
            return this.date.format(DateTimeFormatter.ofPattern("uuuu-MM-dd'T'HH:mm:ss", java.util.Locale.ROOT));
        }
        if ("yyyy-MM-ddTHH:mm:ss.fffffff".equals(format)) {
            return this.date.format(DateTimeFormatter.ofPattern("uuuu-MM-dd'T'HH:mm:ss.SSSSSSS", java.util.Locale.ROOT));
        }
        if (format.length() == 1 && "dDfFgGmMoOrRstTuUyY".indexOf(format.charAt(0)) < 0) {
            throw new FormatException("Input string was not in a correct format");
        }
        throw new UnsupportedOperationException("DateTime format is not mapped for this candidate");
    }

    private String selectedRoundTripText(IFormatProvider provider) {
        String text = ToString("yyyy-MM-ddTHH:mm:ss.fffffff", provider);
        if (this.kind == DateTimeKind.Utc) return text + "Z";
        if (this.kind == DateTimeKind.Unspecified) return text;
        int seconds = selectedLocalOffset(ZoneId.systemDefault()).getTotalSeconds();
        int minutes = Math.abs(seconds) / 60;
        return text + String.format(java.util.Locale.ROOT, "%s%02d:%02d",
                seconds < 0 ? "-" : "+", minutes / 60, minutes % 60);
    }

    public String ToLongDateString() {
        return this.date.format(DateTimeFormatter.ofPattern(
                "EEEE, dd MMMM uuuu", java.util.Locale.US));
    }

    public String ToShortDateString() {
        return this.date.format(DateTimeFormatter.ofPattern(
                "MM/dd/uuuu", java.util.Locale.US));
    }

    public String ToLongTimeString() {
        return this.date.format(DateTimeFormatter.ofPattern(
                "HH:mm:ss", java.util.Locale.US));
    }

    public String ToShortTimeString() {
        return this.date.format(DateTimeFormatter.ofPattern(
                "HH:mm", java.util.Locale.US));
    }

    public String[] GetDateTimeFormats(char format, IFormatProvider provider) {
        return switch (format) {
            case 'd' -> new String[] {ToShortDateString(), ToString("yyyy-MM-dd", provider)};
            case 'D' -> new String[] {ToLongDateString()};
            case 't' -> new String[] {ToShortTimeString(),
                    this.date.format(DateTimeFormatter.ofPattern("hh:mm a", java.util.Locale.US)),
                    this.date.format(DateTimeFormatter.ofPattern("H:mm", java.util.Locale.US)),
                    this.date.format(DateTimeFormatter.ofPattern("h:mm a", java.util.Locale.US))};
            case 'T' -> new String[] {ToLongTimeString()};
            case 'f' -> selectedDateTimeCombinations(GetDateTimeFormats('D', provider), GetDateTimeFormats('t', provider));
            case 'F' -> selectedDateTimeCombinations(GetDateTimeFormats('D', provider), GetDateTimeFormats('T', provider));
            case 'g' -> selectedDateTimeCombinations(GetDateTimeFormats('d', provider), GetDateTimeFormats('t', provider));
            case 'G' -> selectedDateTimeCombinations(GetDateTimeFormats('d', provider), GetDateTimeFormats('T', provider));
            case 'm', 'M', 'o', 'O', 'r', 'R', 's', 'u', 'y', 'Y' -> new String[] {ToString(String.valueOf(format), provider)};
            case 'U' -> ToUniversalTime().GetDateTimeFormats('F', provider);
            default -> throw new FormatException("Format specifier was invalid");
        };
    }

    public String[] GetDateTimeFormats(char format) {
        return GetDateTimeFormats(format, null);
    }

    public String[] GetDateTimeFormats(IFormatProvider provider) {
        java.util.ArrayList<String> result = new java.util.ArrayList<>();
        for (char format : "dDfFgGmMoOrRstTuUyY".toCharArray()) {
            java.util.Collections.addAll(result, GetDateTimeFormats(format, provider));
        }
        return result.toArray(String[]::new);
    }

    public String[] GetDateTimeFormats() {
        return GetDateTimeFormats((IFormatProvider) null);
    }

    private static String[] selectedDateTimeCombinations(String[] dates, String[] times) {
        String[] result = new String[dates.length * times.length];
        int index = 0;
        for (String date : dates) {
            for (String time : times) {
                result[index++] = date + " " + time;
            }
        }
        return result;
    }

    @Override
    public boolean TryFormat(char[] destination, int[] charsWritten, String format,
                             IFormatProvider provider) {
        String text = format == null ? this.ToString(provider)
                : this.ToString(format, provider);
        int copyLength = selectedFormatCopyLength(format, text, destination.length);
        text.getChars(0, copyLength, destination, 0);
        if (destination.length < text.length()) {
            charsWritten[0] = 0;
            return false;
        }
        charsWritten[0] = text.length();
        return true;
    }

    @Override
    public boolean TryFormat(byte[] destination, int[] bytesWritten, String format,
            IFormatProvider provider) {
        String formatted = ToString(format, provider);
        byte[] text = formatted.getBytes(java.nio.charset.StandardCharsets.UTF_8);
        int copyLength = selectedFormatCopyLength(format, formatted, destination.length);
        java.lang.System.arraycopy(text, 0, destination, 0, copyLength);
        if (destination.length < text.length) {
            bytesWritten[0] = 0;
            return false;
        }
        bytesWritten[0] = text.length;
        return true;
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

    private int selectedFormatCopyLength(String format, String text, int capacity) {
        int textLength = text.length();
        if (capacity >= textLength) { return textLength; }
        if ("U".equals(format)) return ToUniversalTime().selectedFormatCopyLength("F", text, capacity);
        int[] chunks;
        if (format != null && format.length() == 1 && "dDfFgGmMtTyY".indexOf(format.charAt(0)) >= 0) {
            int month = this.date.getMonth().getDisplayName(java.time.format.TextStyle.FULL, java.util.Locale.US).length();
            int weekday = this.date.getDayOfWeek().getDisplayName(java.time.format.TextStyle.FULL, java.util.Locale.US).length();
            chunks = switch (format.charAt(0)) {
                case 'd' -> new int[] {2,1,2,1,4};
                case 'D' -> new int[] {weekday,1,1,2,1,month,1,4};
                case 'f' -> new int[] {weekday,1,1,2,1,month,1,4,1,2,1,2};
                case 'F' -> new int[] {weekday,1,1,2,1,month,1,4,1,2,1,2,1,2};
                case 'g' -> new int[] {2,1,2,1,4,1,2,1,2};
                case 'G' -> new int[] {2,1,2,1,4,1,2,1,2,1,2};
                case 'm', 'M' -> new int[] {month,1,2};
                case 't' -> new int[] {2,1,2};
                case 'T' -> new int[] {2,1,2,1,2};
                case 'y', 'Y' -> new int[] {4,1,month};
                default -> throw new AssertionError("Unknown selected standard format");
            };
        } else if ("yyyy-MM-dd".equals(format)) {
            chunks = new int[] {4,1,2,1,2};
        } else if ("yyyy-MM-dd HH:mm:ss".equals(format) || "yyyy-MM-dd'T'HH:mm:ss".equals(format)) {
            chunks = new int[] {4,1,2,1,2,1,2,1,2,1,2};
        } else if ("yyyy-MM-dd HH:mm:ss.fff".equals(format)) {
            chunks = new int[] {4,1,2,1,2,1,2,1,2,1,2,1,3};
        } else if ("yyyy-MM-ddTHH:mm:ss.fffffff".equals(format)) {
            chunks = new int[] {4,1,2,1,2,1,2,1,2,1,2,1,7};
        } else {
            return 0;
        }
        int copied = 0;
        for (int chunk : chunks) {
            if (chunk > capacity - copied) { break; }
            copied += chunk;
        }
        return copied;
    }
}
