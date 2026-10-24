// SPDX-License-Identifier: MIT

package System;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

/** Bounded immutable DateTime candidate for a calendar date and invariant text. */
public final class DateTime implements IConvertible, IComparable {
    private final LocalDateTime date;

    public DateTime(int year, int month, int day) {
        this.date = LocalDate.of(year, month, day).atStartOfDay();
    }

    public DateTime(int year, int month, int day, int hourOfDay,
                    int minuteOfHour, int secondOfMinute) {
        this.date = LocalDateTime.of(year, month, day,
                hourOfDay, minuteOfHour, secondOfMinute);
    }

    public DateTime(int year, int month, int day, int hourOfDay,
                    int minuteOfHour, int secondOfMinute, int millisecondOfSecond) {
        this.date = LocalDateTime.of(year, month, day,
                hourOfDay, minuteOfHour, secondOfMinute, millisecondOfSecond * 1_000_000);
    }

    private DateTime(LocalDateTime date) {
        this.date = date;
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
            throw new ArgumentException("Object must be of type DateTime", "obj");
        }
        return Compare(this, other);
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
        return new DateTime(this.date.toLocalDate().atStartOfDay());
    }

    public long get_Ticks() {
        long days = this.date.toLocalDate().toEpochDay()
                - LocalDate.of(1, 1, 1).toEpochDay();
        return days * 864_000_000_000L
                + this.date.toLocalTime().toNanoOfDay() / 100L;
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
        return new DateTime(this.date);
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
}
