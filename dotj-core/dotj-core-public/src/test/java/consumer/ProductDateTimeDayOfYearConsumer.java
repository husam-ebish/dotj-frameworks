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
        java.lang.System.out.println("PASS external selected DateTime day of year");
    }
}
