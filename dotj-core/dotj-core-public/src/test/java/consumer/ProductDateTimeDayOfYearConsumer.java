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
        java.lang.System.out.println("PASS external selected DateTime day of year");
    }
}
