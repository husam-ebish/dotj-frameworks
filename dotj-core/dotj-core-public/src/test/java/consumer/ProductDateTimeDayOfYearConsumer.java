package consumer;

import System.DateTime;

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
                || fractional.get_Ticks() != 638448068961234567L
                || withTime.get_Microsecond() != 0) {
            throw new AssertionError("DateTime microsecond changed");
        }
        java.lang.System.out.println("PASS external selected DateTime day of year");
    }
}
