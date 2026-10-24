package consumer;

import System.DateTime;
import System.ArgumentOutOfRangeException;
import System.ArgumentNullException;
import System.ArgumentException;
import System.IComparable;
import System.FormatException;
import System.OverflowException;
import System.DateTimeKind;
import System.TimeSpan;

/** Selected Gregorian day-of-year values checked outside the product JAR. */
public final class ProductDateTimeDayOfYearConsumer {
    public static void main(String[] args) {
        DateTime firstDate = new DateTime(2024, 2, 29, 12, 0, 0);
        DateTime previousDate = new DateTime(2024, 2, 28, 12, 0, 0);
        if (firstDate.Subtract(previousDate).get_Ticks() != 864_000_000_000L
                || previousDate.Subtract(firstDate).get_Ticks() != -864_000_000_000L
                || firstDate.Subtract(firstDate).get_Ticks() != 0L) {
            throw new AssertionError("DateTime difference changed");
        }
        try {
            firstDate.Subtract((DateTime) null);
            throw new AssertionError("Null DateTime operand accepted");
        } catch (ArgumentNullException expected) {
            if (!"value".equals(expected.get_ParamName())) {
                throw new AssertionError("Null DateTime operand parameter changed");
            }
        }
        DateTime subtractOrigin = new DateTime(2024, 2, 29, 12, 0, 0);
        if (subtractOrigin.Subtract(TimeSpan.FromTicks(10_000_000L)).get_Second() != 59
                || subtractOrigin.Subtract(TimeSpan.FromTicks(-10_000_000L)).get_Second() != 1) {
            throw new AssertionError("DateTime TimeSpan subtraction changed");
        }
        try {
            subtractOrigin.Subtract((TimeSpan) null);
            throw new AssertionError("Null subtraction interval accepted");
        } catch (ArgumentNullException expected) {
            if (!"value".equals(expected.get_ParamName())) {
                throw new AssertionError("Null subtraction parameter changed");
            }
        }
        try {
            subtractOrigin.Subtract(TimeSpan.FromTicks(Long.MIN_VALUE));
            throw new AssertionError("Unnegatable subtraction interval accepted");
        } catch (ArgumentOutOfRangeException expected) {
        }
        DateTime spanOrigin = new DateTime(2024, 2, 29);
        if (spanOrigin.Add(TimeSpan.FromTicks(10_000_000L)).get_Second() != 1
                || spanOrigin.Add(new TimeSpan(-10_000_000L)).get_Day() != 28
                || TimeSpan.FromTicks(123L).get_Ticks() != 123L) {
            throw new AssertionError("DateTime TimeSpan addition changed");
        }
        try {
            spanOrigin.Add(null);
            throw new AssertionError("Null TimeSpan was accepted");
        } catch (ArgumentNullException expected) {
            if (!"value".equals(expected.get_ParamName())) {
                throw new AssertionError("Null TimeSpan parameter changed");
            }
        }
        DateTime unspecified = new DateTime(2024, 2, 29);
        DateTime specifiedUtc = DateTime.SpecifyKind(unspecified, DateTimeKind.Utc);
        DateTime specifiedLocal = DateTime.SpecifyKind(unspecified, DateTimeKind.Local);
        if (unspecified.get_Kind() != DateTimeKind.Unspecified
                || specifiedUtc.get_Kind() != DateTimeKind.Utc
                || specifiedLocal.get_Kind() != DateTimeKind.Local
                || specifiedUtc.get_Ticks() != unspecified.get_Ticks()
                || specifiedUtc.AddDays(1).get_Kind() != DateTimeKind.Utc
                || specifiedLocal.get_Date().get_Kind() != DateTimeKind.Local
                || DateTime.FromBinary(specifiedUtc.ToBinary()).get_Kind()
                    != DateTimeKind.Utc
                || DateTime.FromFileTimeUtc(0).get_Kind() != DateTimeKind.Utc) {
            throw new AssertionError("DateTime kind identity changed");
        }
        try {
            DateTime.SpecifyKind(unspecified, null);
            throw new AssertionError("Null DateTime kind accepted");
        } catch (ArgumentException expected) {
            if (!"kind".equals(expected.get_ParamName())) {
                throw new AssertionError("DateTime kind parameter changed");
            }
        }
        int[] deconstructedYear = {-1};
        int[] deconstructedMonth = {-1};
        int[] deconstructedDay = {-1};
        new DateTime(2024, 2, 29, 23, 59, 58).Deconstruct(
                deconstructedYear, deconstructedMonth, deconstructedDay);
        if (deconstructedYear[0] != 2024 || deconstructedMonth[0] != 2
                || deconstructedDay[0] != 29) {
            throw new AssertionError("DateTime date deconstruction changed");
        }
        java.util.TimeZone priorDaylightZone = java.util.TimeZone.getDefault();
        try {
            java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("America/New_York"));
            if (new DateTime(2024, 1, 15).IsDaylightSavingTime()
                    || !new DateTime(2024, 7, 15).IsDaylightSavingTime()) {
                throw new AssertionError("Local daylight-saving status changed");
            }
        } finally {
            java.util.TimeZone.setDefault(priorDaylightZone);
        }
        java.util.TimeZone priorLocalZone = java.util.TimeZone.getDefault();
        try {
            java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("America/New_York"));
            DateTime local = new DateTime(1970, 1, 1).ToLocalTime();
            if (local.get_Year() != 1969 || local.get_Month() != 12
                    || local.get_Day() != 31 || local.get_Hour() != 19) {
                throw new AssertionError("UTC to local conversion changed");
            }
        } finally {
            java.util.TimeZone.setDefault(priorLocalZone);
        }
        java.util.TimeZone priorUniversalZone = java.util.TimeZone.getDefault();
        try {
            java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("America/New_York"));
            DateTime universal = new DateTime(1969, 12, 31, 19, 0, 0)
                    .ToUniversalTime();
            if (universal.get_Ticks() != new DateTime(1970, 1, 1).get_Ticks()) {
                throw new AssertionError("Local to UTC conversion changed");
            }
        } finally {
            java.util.TimeZone.setDefault(priorUniversalZone);
        }
        java.util.TimeZone priorFileTimeZone = java.util.TimeZone.getDefault();
        try {
            java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("America/New_York"));
            if (new DateTime(1969, 12, 31, 19, 0, 0).ToFileTime()
                    != 116444736000000000L
                    || DateTime.FromFileTime(116444736000000000L).ToFileTime()
                        != 116444736000000000L) {
                throw new AssertionError("Local file-time round trip changed");
            }
        } finally {
            java.util.TimeZone.setDefault(priorFileTimeZone);
        }
        java.util.TimeZone priorZone = java.util.TimeZone.getDefault();
        try {
            java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("America/New_York"));
            DateTime localFileTime = DateTime.FromFileTime(116444736000000000L);
            if (localFileTime.get_Year() != 1969
                    || localFileTime.get_Month() != 12
                    || localFileTime.get_Day() != 31
                    || localFileTime.get_Hour() != 19) {
                throw new AssertionError("Local file-time conversion changed");
            }
        } finally {
            java.util.TimeZone.setDefault(priorZone);
        }
        DateTime formatDate = new DateTime(2024, 2, 29, 23, 59, 58);
        String[] shortDateFormats = formatDate.GetDateTimeFormats('d', null);
        String[] allDateFormats = formatDate.GetDateTimeFormats();
        if (shortDateFormats.length != 1
                || !"02/29/2024".equals(shortDateFormats[0])
                || allDateFormats.length != 4
                || !"23:59:58".equals(formatDate.GetDateTimeFormats('T', null)[0])) {
            throw new AssertionError("Selected DateTime format variants changed");
        }
        shortDateFormats[0] = "mutated";
        if (!"02/29/2024".equals(formatDate.GetDateTimeFormats('d', null)[0])) {
            throw new AssertionError("DateTime format array was shared");
        }
        try {
            formatDate.GetDateTimeFormats('?', null);
            throw new AssertionError("Unsupported DateTime format accepted");
        } catch (FormatException expected) {
        }
        DateTime formattedDate = new DateTime(2024, 2, 29, 12, 34, 56);
        char[] dateDestination = new char[12];
        int[] dateWritten = {-1};
        if (!formattedDate.TryFormat(dateDestination, dateWritten,
                    "yyyy-MM-dd", null)
                || dateWritten[0] != 10
                || !"2024-02-29".equals(new String(dateDestination, 0, 10))) {
            throw new AssertionError("DateTime TryFormat output changed");
        }
        char[] smallDateDestination = {'x', 'x'};
        dateWritten[0] = -1;
        if (formattedDate.TryFormat(smallDateDestination, dateWritten,
                    "yyyy-MM-dd", null)
                || dateWritten[0] != 0
                || smallDateDestination[0] != 'x') {
            throw new AssertionError("DateTime TryFormat small buffer changed");
        }
        if (DateTime.FromOADate(0.0).get_Ticks()
                    != new DateTime(1899, 12, 30).get_Ticks()
                || DateTime.FromOADate(2.0).get_Ticks()
                    != new DateTime(1900, 1, 1).get_Ticks()
                || DateTime.FromOADate(25569.0).get_Ticks()
                    != new DateTime(1970, 1, 1).get_Ticks()
                || DateTime.FromOADate(-1.5).get_Ticks()
                    != new DateTime(1899, 12, 29, 12, 0, 0).get_Ticks()) {
            throw new AssertionError("OLE Automation date decoding changed");
        }
        for (double invalid : new double[] {Double.NaN,
                Double.POSITIVE_INFINITY, -657435.0, 2958466.0}) {
            try {
                DateTime.FromOADate(invalid);
                throw new AssertionError("Invalid OLE date accepted");
            } catch (ArgumentException expected) {
            }
        }
        if (new DateTime(1, 1, 1).ToOADate() != 0.0
                || new DateTime(1899, 12, 30).ToOADate() != 0.0
                || new DateTime(1900, 1, 1).ToOADate() != 2.0
                || new DateTime(1970, 1, 1).ToOADate() != 25569.0
                || new DateTime(1899, 12, 29, 12, 0, 0).ToOADate() != -1.5) {
            throw new AssertionError("OLE Automation date conversion changed");
        }
        try {
            new DateTime(99, 12, 31).ToOADate();
            throw new AssertionError("Pre-OLE minimum date accepted");
        } catch (OverflowException expected) {
        }
        if (!"00:00".equals(new DateTime(1, 1, 1).ToShortTimeString())
                || !"23:59".equals(new DateTime(2024, 2, 29, 23, 59, 58)
                    .ToShortTimeString())) {
            throw new AssertionError("Invariant short-time text changed");
        }
        if (!"00:00:00".equals(new DateTime(1, 1, 1).ToLongTimeString())
                || !"23:59:58".equals(new DateTime(2024, 2, 29, 23, 59, 58)
                    .ToLongTimeString())) {
            throw new AssertionError("Invariant long-time text changed");
        }
        if (!"02/29/2024".equals(new DateTime(2024, 2, 29).ToShortDateString())
                || !"01/01/0001".equals(new DateTime(1, 1, 1).ToShortDateString())) {
            throw new AssertionError("Invariant short-date text changed");
        }
        if (!"Thursday, 29 February 2024".equals(
                    new DateTime(2024, 2, 29).ToLongDateString())
                || !"Monday, 01 January 0001".equals(
                    new DateTime(1, 1, 1).ToLongDateString())) {
            throw new AssertionError("Invariant long-date text changed");
        }
        for (long fileTime : new long[] {0L, 116444736000000000L,
                2650467743999999999L}) {
            if (DateTime.FromFileTimeUtc(fileTime).ToFileTimeUtc() != fileTime) {
                throw new AssertionError("UTC file-time round trip changed");
            }
        }
        try {
            new DateTime(1600, 12, 31).ToFileTimeUtc();
            throw new AssertionError("Pre-file-time date accepted");
        } catch (ArgumentOutOfRangeException expected) {
        }
        if (DateTime.FromFileTimeUtc(0).get_Ticks() != 504911232000000000L
                || DateTime.FromFileTimeUtc(116444736000000000L).get_Ticks()
                    != new DateTime(1970, 1, 1).get_Ticks()
                || DateTime.FromFileTimeUtc(2650467743999999999L).get_Ticks()
                    != 3155378975999999999L) {
            throw new AssertionError("UTC file-time conversion changed");
        }
        for (long invalid : new long[] {-1L, 2650467744000000000L}) {
            try {
                DateTime.FromFileTimeUtc(invalid);
                throw new AssertionError("Invalid UTC file time accepted");
            } catch (ArgumentOutOfRangeException expected) {
                if (!"fileTime".equals(expected.get_ParamName())) {
                    throw new AssertionError("UTC file-time parameter changed");
                }
            }
        }
        for (long binary : new long[] {0L, 621355968000000000L,
                638448068961234567L, 3155378975999999999L}) {
            if (DateTime.FromBinary(binary).ToBinary() != binary) {
                throw new AssertionError("Unspecified DateTime binary round trip changed");
            }
        }
        for (long invalid : new long[] {-1L, Long.MAX_VALUE}) {
            try {
                DateTime.FromBinary(invalid);
                throw new AssertionError("Invalid DateTime binary value accepted");
            } catch (ArgumentException expected) {
                if (!"dateData".equals(expected.get_ParamName())) {
                    throw new AssertionError("DateTime binary parameter changed");
                }
            }
        }
        if (new DateTime(1, 1, 1).ToBinary() != 0L
                || new DateTime(1970, 1, 1).ToBinary() != 621355968000000000L
                || DateTime.Parse("2024-02-29T12:34:56.1234567").ToBinary()
                    != 638448068961234567L) {
            throw new AssertionError("Unspecified DateTime binary representation changed");
        }
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
        double tickHour = 1.0 / 36000000000.0;
        if (dayOrigin.AddHours(-1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != -36000000000L
                || dayOrigin.AddHours(-0.5).get_Ticks() - dayOrigin.get_Ticks()
                    != -18000000000L
                || dayOrigin.AddHours(-tickHour).get_Ticks() - dayOrigin.get_Ticks() != -1L
                || dayOrigin.AddHours(tickHour / 2).get_Ticks() != dayOrigin.get_Ticks()
                || dayOrigin.AddHours(tickHour).get_Ticks() - dayOrigin.get_Ticks() != 1L
                || dayOrigin.AddHours(1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != 36000000000L
                || dayOrigin.AddHours(Double.NaN).get_Ticks() != dayOrigin.get_Ticks()) {
            throw new AssertionError("DateTime AddHours changed");
        }
        try {
            dayOrigin.AddHours(Double.POSITIVE_INFINITY);
            throw new AssertionError("Infinite hours accepted");
        } catch (ArgumentOutOfRangeException caught) {
            if (!"value".equals(caught.get_ParamName())) {
                throw new AssertionError("Hour addition parameter changed");
            }
        }
        double tickMinute = 1.0 / 600000000.0;
        if (dayOrigin.AddMinutes(-1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != -600000000L
                || dayOrigin.AddMinutes(-0.5).get_Ticks() - dayOrigin.get_Ticks()
                    != -300000000L
                || dayOrigin.AddMinutes(-tickMinute).get_Ticks()
                    - dayOrigin.get_Ticks() != -1L
                || dayOrigin.AddMinutes(tickMinute / 2).get_Ticks()
                    != dayOrigin.get_Ticks()
                || dayOrigin.AddMinutes(tickMinute).get_Ticks()
                    - dayOrigin.get_Ticks() != 1L
                || dayOrigin.AddMinutes(1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != 600000000L
                || dayOrigin.AddMinutes(Double.NaN).get_Ticks() != dayOrigin.get_Ticks()) {
            throw new AssertionError("DateTime AddMinutes changed");
        }
        try {
            dayOrigin.AddMinutes(Double.POSITIVE_INFINITY);
            throw new AssertionError("Infinite minutes accepted");
        } catch (ArgumentOutOfRangeException caught) {
            if (!"value".equals(caught.get_ParamName())) {
                throw new AssertionError("Minute addition parameter changed");
            }
        }
        double tickSecond = 1.0 / 10000000.0;
        if (dayOrigin.AddSeconds(-1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != -10000000L
                || dayOrigin.AddSeconds(-0.5).get_Ticks() - dayOrigin.get_Ticks()
                    != -5000000L
                || dayOrigin.AddSeconds(-tickSecond).get_Ticks()
                    - dayOrigin.get_Ticks() != -1L
                || dayOrigin.AddSeconds(tickSecond / 2).get_Ticks()
                    != dayOrigin.get_Ticks()
                || dayOrigin.AddSeconds(tickSecond).get_Ticks()
                    - dayOrigin.get_Ticks() != 1L
                || dayOrigin.AddSeconds(1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != 10000000L
                || dayOrigin.AddSeconds(Double.NaN).get_Ticks() != dayOrigin.get_Ticks()) {
            throw new AssertionError("DateTime AddSeconds changed");
        }
        try {
            dayOrigin.AddSeconds(Double.POSITIVE_INFINITY);
            throw new AssertionError("Infinite seconds accepted");
        } catch (ArgumentOutOfRangeException caught) {
            if (!"value".equals(caught.get_ParamName())) {
                throw new AssertionError("Second addition parameter changed");
            }
        }
        double tickMillisecond = 1.0 / 10000.0;
        if (dayOrigin.AddMilliseconds(-1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != -10000L
                || dayOrigin.AddMilliseconds(-0.5).get_Ticks() - dayOrigin.get_Ticks()
                    != -5000L
                || dayOrigin.AddMilliseconds(-tickMillisecond).get_Ticks()
                    - dayOrigin.get_Ticks() != -1L
                || dayOrigin.AddMilliseconds(tickMillisecond / 2).get_Ticks()
                    != dayOrigin.get_Ticks()
                || dayOrigin.AddMilliseconds(tickMillisecond).get_Ticks()
                    - dayOrigin.get_Ticks() != 1L
                || dayOrigin.AddMilliseconds(1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != 10000L
                || dayOrigin.AddMilliseconds(Double.NaN).get_Ticks()
                    != dayOrigin.get_Ticks()) {
            throw new AssertionError("DateTime AddMilliseconds changed");
        }
        try {
            dayOrigin.AddMilliseconds(Double.POSITIVE_INFINITY);
            throw new AssertionError("Infinite milliseconds accepted");
        } catch (ArgumentOutOfRangeException caught) {
            if (!"value".equals(caught.get_ParamName())) {
                throw new AssertionError("Millisecond addition parameter changed");
            }
        }
        if (dayOrigin.AddMicroseconds(-1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != -10L
                || dayOrigin.AddMicroseconds(-0.5).get_Ticks() - dayOrigin.get_Ticks()
                    != -5L
                || dayOrigin.AddMicroseconds(-0.1).get_Ticks() - dayOrigin.get_Ticks()
                    != -1L
                || dayOrigin.AddMicroseconds(0.05).get_Ticks()
                    != dayOrigin.get_Ticks()
                || dayOrigin.AddMicroseconds(0.1).get_Ticks() - dayOrigin.get_Ticks()
                    != 1L
                || dayOrigin.AddMicroseconds(1.0).get_Ticks() - dayOrigin.get_Ticks()
                    != 10L
                || dayOrigin.AddMicroseconds(Double.NaN).get_Ticks()
                    != dayOrigin.get_Ticks()) {
            throw new AssertionError("DateTime AddMicroseconds changed");
        }
        try {
            dayOrigin.AddMicroseconds(Double.POSITIVE_INFINITY);
            throw new AssertionError("Infinite microseconds accepted");
        } catch (ArgumentOutOfRangeException caught) {
            if (!"value".equals(caught.get_ParamName())) {
                throw new AssertionError("Microsecond addition parameter changed");
            }
        }
        DateTime[] parsed = {new DateTime(2024, 1, 1)};
        if (!DateTime.TryParse("2024-02-29T12:34:56.1234567", parsed)
                || parsed[0].get_Ticks() != 638448068961234567L
                || !DateTime.TryParse(" 2024-02-29 ", parsed)
                || parsed[0].get_DayOfYear() != 60
                || DateTime.TryParse("2023-02-29", parsed)
                || parsed[0].get_Ticks() != 0L
                || DateTime.TryParse(null, parsed)
                || parsed[0].get_Ticks() != 0L) {
            throw new AssertionError("DateTime TryParse changed");
        }
        if (DateTime.ParseExact("2024-02-29", "yyyy-MM-dd", null).get_DayOfYear() != 60
                || DateTime.ParseExact("2024-02-29 12:34:56",
                    "yyyy-MM-dd HH:mm:ss", null).get_Hour() != 12
                || DateTime.ParseExact("2024-02-29T12:34:56.1234567",
                    "yyyy-MM-ddTHH:mm:ss.fffffff", null).get_Ticks()
                    != 638448068961234567L) {
            throw new AssertionError("DateTime ParseExact changed");
        }
        String[][] invalidExact = {{" 2024-02-29 ", "yyyy-MM-dd"},
            {"2023-02-29", "yyyy-MM-dd"},
            {"2024-02-29T12:34:56.123", "yyyy-MM-ddTHH:mm:ss.fffffff"},
            {"2024-02-29", "unsupported"}};
        for (String[] row : invalidExact) {
            try {
                DateTime.ParseExact(row[0], row[1], null);
                throw new AssertionError("Invalid exact date accepted");
            } catch (FormatException expected) {
            }
        }
        DateTime[] exactResult = {new DateTime(2024, 1, 1)};
        if (!DateTime.TryParseExact("2024-02-29T12:34:56.1234567",
                    "yyyy-MM-ddTHH:mm:ss.fffffff", null, exactResult)
                || exactResult[0].get_Ticks() != 638448068961234567L
                || !DateTime.TryParseExact("2024-02-29", "yyyy-MM-dd", null,
                    exactResult)
                || exactResult[0].get_DayOfYear() != 60
                || DateTime.TryParseExact("2023-02-29", "yyyy-MM-dd", null,
                    exactResult)
                || exactResult[0].get_Ticks() != 0L
                || DateTime.TryParseExact(null, "yyyy-MM-dd", null, exactResult)
                || exactResult[0].get_Ticks() != 0L
                || DateTime.TryParseExact("2024-02-29", null, null, exactResult)
                || exactResult[0].get_Ticks() != 0L) {
            throw new AssertionError("DateTime TryParseExact changed");
        }
        java.lang.System.out.println("PASS external selected DateTime day of year");
    }
}
