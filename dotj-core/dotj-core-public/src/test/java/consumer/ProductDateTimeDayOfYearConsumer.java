package consumer;

import System.DateTime;
import System.ArgumentOutOfRangeException;
import System.ArgumentNullException;
import System.ArgumentException;
import System.IComparable;

/** Selected Gregorian day-of-year values checked outside the product JAR. */
public final class ProductDateTimeDayOfYearConsumer {
    public static void main(String[] args) {
        int[][] cases = {
            {1, 1, 1, 1},
            {2000, 2, 29, 60},
            {2000, 12, 31, 366},
            {2001, 3, 1, 60},
            {2024, 3, 1, 61},
            {9999, 12, 31, 365},
        };
        for (int[] row : cases) {
            DateTime date = new DateTime(row[0], row[1], row[2]);
            if (date.get_DayOfYear() != row[3]) {
                throw new AssertionError("DateTime day of year changed: "
                        + row[0] + "-" + row[1] + "-" + row[2]);
            }
        }
        DateTime withTime = new DateTime(2024, 2, 29, 23, 59, 58, 999);
        DateTime date = withTime.get_Date();
        if (date == withTime || date.get_Year() != 2024
                || date.get_Month() != 2 || date.get_Day() != 29
                || date.get_DayOfYear() != 60 || date.get_Hour() != 0
                || date.get_Minute() != 0 || date.get_Second() != 0
                || date.get_Millisecond() != 0) {
            throw new AssertionError("DateTime Date did not truncate the time");
        }
        if (date.get_Date().get_Hour() != 0) {
            throw new AssertionError("DateTime Date changed after a second access");
        }
        if (new DateTime(1, 1, 1).get_Ticks() != 0L
                || new DateTime(1970, 1, 1).get_Ticks() != 621355968000000000L
                || new DateTime(2000, 2, 29, 12, 34, 56, 789).get_Ticks()
                    != 630874244967890000L
                || new DateTime(9999, 12, 31, 23, 59, 59, 999).get_Ticks()
                    != 3155378975999990000L
                || withTime.get_Date().get_Ticks()
                    != new DateTime(2024, 2, 29).get_Ticks()) {
            throw new AssertionError("DateTime ticks changed");
        }
        DateTime fractional = DateTime.Parse("2024-02-29T12:34:56.1234567");
        if (fractional.get_Millisecond() != 123
                || fractional.get_Microsecond() != 456
                || fractional.get_Nanosecond() != 700
                || fractional.get_Ticks() != 638448068961234567L
                || withTime.get_Microsecond() != 0
                || withTime.get_Nanosecond() != 0) {
            throw new AssertionError("DateTime microsecond changed");
        }
        int[] leapYears = {4, 400, 2000, 2024};
        int[] commonYears = {1, 100, 1900, 2001, 9999};
        for (int year : leapYears) {
            if (!DateTime.IsLeapYear(year)) {
                throw new AssertionError("Leap year rejected: " + year);
            }
        }
        for (int year : commonYears) {
            if (DateTime.IsLeapYear(year)) {
                throw new AssertionError("Common year accepted: " + year);
            }
        }
        for (int year : new int[] {0, -1, 10000}) {
            try {
                DateTime.IsLeapYear(year);
                throw new AssertionError("Invalid year accepted: " + year);
            } catch (ArgumentOutOfRangeException caught) {
                if (!"year".equals(caught.get_ParamName())) {
                    throw new AssertionError("Invalid year parameter changed");
                }
            }
        }
        int[][] monthDays = {
            {1, 2, 28}, {1900, 2, 28}, {2000, 2, 29},
            {2024, 2, 29}, {2024, 4, 30}, {2024, 12, 31},
            {9999, 12, 31},
        };
        for (int[] row : monthDays) {
            if (DateTime.DaysInMonth(row[0], row[1]) != row[2]) {
                throw new AssertionError("Month days changed: " + row[0] + "-" + row[1]);
            }
        }
        int[][] invalidMonths = {{2024, 0}, {2024, 13}, {0, 0}};
        for (int[] row : invalidMonths) {
            try {
                DateTime.DaysInMonth(row[0], row[1]);
                throw new AssertionError("Invalid month accepted");
            } catch (ArgumentOutOfRangeException caught) {
                if (!"month".equals(caught.get_ParamName())) {
                    throw new AssertionError("Invalid month parameter changed");
                }
            }
        }
        for (int year : new int[] {0, 10000}) {
            try {
                DateTime.DaysInMonth(year, 1);
                throw new AssertionError("Invalid year accepted");
            } catch (ArgumentOutOfRangeException caught) {
                if (!"year".equals(caught.get_ParamName())) {
                    throw new AssertionError("Invalid year parameter changed");
                }
            }
        }
        DateTime earlier = new DateTime(2024, 2, 29, 12, 0, 0);
        DateTime later = new DateTime(2024, 2, 29, 12, 0, 1);
        if (DateTime.Compare(earlier, later) != -1
                || DateTime.Compare(later, earlier) != 1
                || DateTime.Compare(earlier, new DateTime(2024, 2, 29, 12, 0, 0)) != 0
                || DateTime.Compare(new DateTime(1, 1, 1), new DateTime(9999, 12, 31)) != -1) {
            throw new AssertionError("DateTime Compare changed");
        }
        try {
            DateTime.Compare(null, later);
            throw new AssertionError("Null left DateTime accepted");
        } catch (ArgumentNullException caught) {
            if (!"left".equals(caught.get_ParamName())) {
                throw new AssertionError("Left parameter changed");
            }
        }
        try {
            DateTime.Compare(earlier, null);
            throw new AssertionError("Null right DateTime accepted");
        } catch (ArgumentNullException caught) {
            if (!"right".equals(caught.get_ParamName())) {
                throw new AssertionError("Right parameter changed");
            }
        }
        if (earlier.CompareTo(later) != -1
                || later.CompareTo(earlier) != 1
                || earlier.CompareTo(new DateTime(2024, 2, 29, 12, 0, 0)) != 0
                || ((IComparable) earlier).CompareTo(later) != -1
                || ((IComparable) later).CompareTo(null) != 1) {
            throw new AssertionError("DateTime CompareTo changed");
        }
        try {
            earlier.CompareTo((DateTime) null);
            throw new AssertionError("Null typed DateTime accepted");
        } catch (ArgumentNullException caught) {
            if (!"other".equals(caught.get_ParamName())) {
                throw new AssertionError("Typed parameter changed");
            }
        }
        try {
            ((IComparable) earlier).CompareTo("2024-02-29");
            throw new AssertionError("Wrong comparison type accepted");
        } catch (ArgumentException caught) {
            if (!"obj".equals(caught.get_ParamName())) {
                throw new AssertionError("Object parameter changed");
            }
        }
        DateTime equalDate = new DateTime(2024, 2, 29, 12, 0, 0);
        if (!DateTime.Equals(earlier, equalDate)
                || !earlier.Equals(equalDate)
                || !earlier.Equals((Object) equalDate)
                || !earlier.equals(equalDate)
                || DateTime.Equals(earlier, later)
                || earlier.Equals((Object) "2024-02-29")
                || earlier.Equals((DateTime) null)
                || earlier.GetHashCode() != -62334691
                || earlier.GetHashCode() != equalDate.GetHashCode()
                || earlier.hashCode() != earlier.GetHashCode()) {
            throw new AssertionError("DateTime equality or hash changed");
        }
        DateTime minimum = new DateTime(1, 1, 1);
        DateTime maximumMillisecond = new DateTime(9999, 12, 31, 23, 59, 59, 999);
        if (minimum.AddTicks(1).get_Ticks() != 1L
                || minimum.AddTicks(1).AddTicks(-1).get_Ticks() != 0L
                || maximumMillisecond.AddTicks(9999).get_Ticks()
                    != 3155378975999999999L
                || new DateTime(2024, 2, 29).AddTicks(864000000000L)
                    .get_DayOfYear() != 61) {
            throw new AssertionError("DateTime AddTicks changed");
        }
        long[][] invalidTicks = {{0L, -1L}, {1L, 10000L}, {0L, Long.MAX_VALUE}};
        for (long[] row : invalidTicks) {
            DateTime target = row[0] == 0L ? minimum : maximumMillisecond;
            try {
                target.AddTicks(row[1]);
                throw new AssertionError("Out-of-range ticks accepted");
            } catch (ArgumentOutOfRangeException caught) {
                if (!"value".equals(caught.get_ParamName())) {
                    throw new AssertionError("Tick parameter changed");
                }
            }
        }
        DateTime januaryEnd = new DateTime(2024, 1, 31, 12, 34, 56, 789);
        DateTime leapEnd = januaryEnd.AddMonths(1);
        DateTime commonEnd = new DateTime(2023, 1, 31).AddMonths(1);
        if (leapEnd.get_Year() != 2024 || leapEnd.get_Month() != 2
                || leapEnd.get_Day() != 29 || leapEnd.get_Hour() != 12
                || leapEnd.get_Millisecond() != 789
                || commonEnd.get_Day() != 28
                || new DateTime(2024, 3, 31).AddMonths(-1).get_Day() != 29
                || januaryEnd.AddMonths(0).get_Ticks() != januaryEnd.get_Ticks()) {
            throw new AssertionError("DateTime AddMonths changed");
        }
        int[][] invalidMonthsDelta = {{1, -1}, {9999, 1}, {2024, -120001},
            {2024, 120001}};
        for (int[] row : invalidMonthsDelta) {
            DateTime target = new DateTime(row[0], row[0] == 9999 ? 12 : 1, 1);
            try {
                target.AddMonths(row[1]);
                throw new AssertionError("Out-of-range month addition accepted");
            } catch (ArgumentOutOfRangeException caught) {
                if (!"months".equals(caught.get_ParamName())) {
                    throw new AssertionError("Month addition parameter changed");
                }
            }
        }
        DateTime leapDay = new DateTime(2024, 2, 29, 12, 34, 56, 789);
        if (leapDay.AddYears(-1).get_Day() != 28
                || leapDay.AddYears(1).get_Day() != 28
                || leapDay.AddYears(4).get_Day() != 29
                || leapDay.AddYears(1).get_Hour() != 12
                || leapDay.AddYears(1).get_Millisecond() != 789
                || leapDay.AddYears(0).get_Ticks() != leapDay.get_Ticks()) {
            throw new AssertionError("DateTime AddYears changed");
        }
        int[][] invalidYearsDelta = {{1, -1}, {9999, 1}, {2024, -10001},
            {2024, 10001}};
        for (int[] row : invalidYearsDelta) {
            try {
                new DateTime(row[0], 1, 1).AddYears(row[1]);
                throw new AssertionError("Out-of-range year addition accepted");
            } catch (ArgumentOutOfRangeException caught) {
                if (!"years".equals(caught.get_ParamName())) {
                    throw new AssertionError("Year addition parameter changed");
                }
            }
        }
        DateTime dayOrigin = new DateTime(2024, 2, 29, 12, 0, 0);
        double tickDay = 1.0 / 864000000000.0;
        if (dayOrigin.AddDays(-1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != -864000000000L
                || dayOrigin.AddDays(-0.5).get_Ticks() - dayOrigin.get_Ticks()
                    != -432000000000L
                || dayOrigin.AddDays(-tickDay).get_Ticks() - dayOrigin.get_Ticks() != -1L
                || dayOrigin.AddDays(-tickDay / 2).get_Ticks() != dayOrigin.get_Ticks()
                || dayOrigin.AddDays(tickDay / 2).get_Ticks() != dayOrigin.get_Ticks()
                || dayOrigin.AddDays(tickDay).get_Ticks() - dayOrigin.get_Ticks() != 1L
                || dayOrigin.AddDays(0.5).get_Ticks() - dayOrigin.get_Ticks()
                    != 432000000000L
                || dayOrigin.AddDays(1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != 864000000000L
                || dayOrigin.AddDays(Double.NaN).get_Ticks() != dayOrigin.get_Ticks()) {
            throw new AssertionError("DateTime AddDays changed");
        }
        for (double days : new double[] {Double.POSITIVE_INFINITY,
                Double.NEGATIVE_INFINITY, Double.MAX_VALUE}) {
            try {
                dayOrigin.AddDays(days);
                throw new AssertionError("Out-of-range day addition accepted");
            } catch (ArgumentOutOfRangeException caught) {
                if (!"value".equals(caught.get_ParamName())) {
                    throw new AssertionError("Day addition parameter changed");
                }
            }
        }
        java.lang.System.out.println("PASS external selected DateTime day of year");
    }
}
