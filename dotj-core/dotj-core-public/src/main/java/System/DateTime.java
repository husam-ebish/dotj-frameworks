// SPDX-License-Identifier: MIT

package System;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.time.format.ResolverStyle;

/** Bounded immutable DateTime candidate for a calendar date and invariant text. */
public final class DateTime implements IConvertible, IComparable, ISpanFormattable {
    private static final long TICKS_PER_DAY = 864_000_000_000L;
    private static final long FILE_TIME_EPOCH_TICKS = 504_911_232_000_000_000L;
    private static final long OA_EPOCH_TICKS = 599_264_352_000_000_000L;
    private static final long OA_MIN_TICKS = 31_241_376_000_000_000L;
    private static final long MILLIS_PER_DAY = 86_400_000L;
    private static final long MAX_TICKS = 3_155_378_975_999_999_999L;
    private final LocalDateTime date;
    private final DateTimeKind kind;

    public DateTime(int year, int month, int day) {
        this.date = LocalDate.of(year, month, day).atStartOfDay();
        this.kind = DateTimeKind.Unspecified;
    }

    public DateTime(int year, int month, int day, int hourOfDay,
                    int minuteOfHour, int secondOfMinute) {
        this.date = LocalDateTime.of(year, month, day,
                hourOfDay, minuteOfHour, secondOfMinute);
        this.kind = DateTimeKind.Unspecified;
    }

    public DateTime(int year, int month, int day, int hourOfDay,
                    int minuteOfHour, int secondOfMinute, int millisecondOfSecond) {
        this.date = LocalDateTime.of(year, month, day,
                hourOfDay, minuteOfHour, secondOfMinute, millisecondOfSecond * 1_000_000);
        this.kind = DateTimeKind.Unspecified;
    }

    private DateTime(LocalDateTime date) {
        this(date, DateTimeKind.Unspecified);
    }

    private DateTime(LocalDateTime date, DateTimeKind kind) {
        this.date = date;
        this.kind = kind;
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
        if (text == null) {
            throw new ArgumentNullException("s");
        }
        try {
            LocalDateTime parsed = LocalDateTime.parse(text.strip(), DateTimeFormatter.ISO_LOCAL_DATE_TIME);
            return new DateTime(parsed);
        } catch (DateTimeParseException ignored) {
            try {
                LocalDate parsed = LocalDate.parse(text.strip(), DateTimeFormatter.ISO_LOCAL_DATE);
                return new DateTime(parsed.getYear(), parsed.getMonthValue(), parsed.getDayOfMonth());
            } catch (DateTimeParseException invalid) {
                throw new FormatException("Input string was not in a correct format");
            }
        }
    }

    public static boolean TryParse(String text, DateTime[] result) {
        result[0] = new DateTime(1, 1, 1);
        if (text == null) {
            return false;
        }
        try {
            result[0] = Parse(text);
            return true;
        } catch (FormatException expected) {
            return false;
        }
    }

    public static DateTime ParseExact(String text, String format, IFormatProvider provider) {
        if (text == null) {
            throw new ArgumentNullException("s");
        }
        if (format == null) {
            throw new ArgumentNullException("format");
        }
        try {
            return switch (format) {
                case "yyyy-MM-dd" -> new DateTime(LocalDate.parse(text,
                        DateTimeFormatter.ISO_LOCAL_DATE).atStartOfDay());
                case "yyyy-MM-dd HH:mm:ss" -> new DateTime(LocalDateTime.parse(text,
                        DateTimeFormatter.ofPattern("uuuu-MM-dd HH:mm:ss")
                                .withResolverStyle(ResolverStyle.STRICT)));
                case "yyyy-MM-ddTHH:mm:ss.fffffff" -> new DateTime(LocalDateTime.parse(text,
                        DateTimeFormatter.ofPattern("uuuu-MM-dd'T'HH:mm:ss.SSSSSSS")
                                .withResolverStyle(ResolverStyle.STRICT)));
                default -> throw new FormatException("Input string was not in a correct format");
            };
        } catch (DateTimeParseException invalid) {
            throw new FormatException("Input string was not in a correct format");
        }
    }

    public static boolean TryParseExact(String text, String format,
                                        IFormatProvider provider, DateTime[] result) {
        result[0] = new DateTime(1, 1, 1);
        if (text == null || format == null) {
            return false;
        }
        try {
            result[0] = ParseExact(text, format, provider);
            return true;
        } catch (FormatException expected) {
            return false;
        }
    }

    public static DateTime FromBinary(long dateData) {
        long ticks = dateData & 0x3fff_ffff_ffff_ffffL;
        long flags = dateData & 0xc000_0000_0000_0000L;
        if (ticks > MAX_TICKS || (flags != 0 && flags != 0x4000_0000_0000_0000L)) {
            throw new ArgumentException("Invalid binary date value", "dateData");
        }
        DateTime parsed = new DateTime(1, 1, 1).AddTicks(ticks);
        return flags == 0 ? parsed : SpecifyKind(parsed, DateTimeKind.Utc);
    }

    public static DateTime FromFileTimeUtc(long fileTime) {
        if (fileTime < 0 || fileTime > MAX_TICKS - FILE_TIME_EPOCH_TICKS) {
            throw new ArgumentOutOfRangeException("fileTime");
        }
        return SpecifyKind(new DateTime(1, 1, 1)
                .AddTicks(fileTime + FILE_TIME_EPOCH_TICKS), DateTimeKind.Utc);
    }

    public static DateTime FromFileTime(long fileTime) {
        LocalDateTime utc = FromFileTimeUtc(fileTime).date;
        LocalDateTime local = utc.atZone(ZoneOffset.UTC)
                .withZoneSameInstant(ZoneId.systemDefault()).toLocalDateTime();
        if (local.getYear() < 1 || local.getYear() > 9999) {
            throw new ArgumentOutOfRangeException("fileTime");
        }
        return new DateTime(local, DateTimeKind.Local);
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
        return new DateTime(added, this.kind);
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
        return new DateTime(added, this.kind);
    }

    public DateTime AddYears(int years) {
        if (years < -10_000 || years > 10_000) {
            throw new ArgumentOutOfRangeException("years");
        }
        LocalDateTime added = this.date.plusYears(years);
        if (added.getYear() < 1 || added.getYear() > 9999) {
            throw new ArgumentOutOfRangeException("years");
        }
        return new DateTime(added, this.kind);
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
        double ticks = java.lang.Math.rint(value * ticksPerUnit);
        if (!Double.isFinite(ticks) || ticks < Long.MIN_VALUE
                || ticks >= 0x1.0p63) {
            throw new ArgumentOutOfRangeException("value");
        }
        return AddTicks((long) ticks);
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

    public DateTime get_Date() {
        return new DateTime(this.date.toLocalDate().atStartOfDay(), this.kind);
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
        return this.get_Ticks()
                | (this.kind == DateTimeKind.Utc ? 0x4000_0000_0000_0000L : 0L);
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
        LocalDateTime utc = this.date.atZone(ZoneId.systemDefault())
                .withZoneSameInstant(ZoneOffset.UTC).toLocalDateTime();
        if (utc.getYear() < 1 || utc.getYear() > 9999) {
            throw new ArgumentOutOfRangeException("fileTime");
        }
        return new DateTime(utc).ToFileTimeUtc();
    }

    public DateTime ToUniversalTime() {
        if (this.kind == DateTimeKind.Utc) {
            return this;
        }
        LocalDateTime utc = this.date.atZone(ZoneId.systemDefault())
                .withZoneSameInstant(ZoneOffset.UTC).toLocalDateTime();
        if (utc.getYear() < 1 || utc.getYear() > 9999) {
            throw new ArgumentOutOfRangeException("value");
        }
        return new DateTime(utc, DateTimeKind.Utc);
    }

    public DateTime ToLocalTime() {
        if (this.kind == DateTimeKind.Local) {
            return this;
        }
        LocalDateTime local = this.date.atZone(ZoneOffset.UTC)
                .withZoneSameInstant(ZoneId.systemDefault()).toLocalDateTime();
        if (local.getYear() < 1 || local.getYear() > 9999) {
            throw new ArgumentOutOfRangeException("value");
        }
        return new DateTime(local, DateTimeKind.Local);
    }

    public boolean IsDaylightSavingTime() {
        if (this.kind == DateTimeKind.Utc) {
            return false;
        }
        ZoneId zone = ZoneId.systemDefault();
        return zone.getRules().isDaylightSavings(this.date.atZone(zone).toInstant());
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
        return new DateTime(this.date, this.kind);
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
            throw new ArgumentNullException("conversionType");
        }
        if (conversionType == Type.GetType("System.DateTime")) {
            return this.ToDateTime(provider);
        }
        if (conversionType == Type.GetType("System.String")) {
            return this.ToString(provider);
        }
        throw new InvalidCastException("DateTime target type is not mapped");
    }

    public String ToString(String format, IFormatProvider provider) {
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
        throw new UnsupportedOperationException("DateTime format is not mapped for this candidate");
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
            case 'd' -> new String[] {this.ToShortDateString()};
            case 'D' -> new String[] {this.ToLongDateString()};
            case 't' -> new String[] {this.ToShortTimeString()};
            case 'T' -> new String[] {this.ToLongTimeString()};
            default -> throw new FormatException("Format specifier was invalid");
        };
    }

    public String[] GetDateTimeFormats() {
        return new String[] {this.ToShortDateString(), this.ToLongDateString(),
                this.ToShortTimeString(), this.ToLongTimeString()};
    }

    @Override
    public boolean TryFormat(char[] destination, int[] charsWritten, String format,
                             IFormatProvider provider) {
        String text = format == null ? this.ToString(provider)
                : this.ToString(format, provider);
        if (destination.length < text.length()) {
            charsWritten[0] = 0;
            return false;
        }
        text.getChars(0, text.length(), destination, 0);
        charsWritten[0] = text.length();
        return true;
    }
}
