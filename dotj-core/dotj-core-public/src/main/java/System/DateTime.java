// SPDX-License-Identifier: MIT

package System;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

/** Bounded immutable DateTime candidate for a calendar date and invariant text. */
public final class DateTime {
    private final LocalDate date;

    public DateTime(int year, int month, int day) {
        this.date = LocalDate.of(year, month, day);
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

    public String ToString(String format, IFormatProvider provider) {
        if (!"yyyy-MM-dd".equals(format)) {
            throw new UnsupportedOperationException("DateTime format is not mapped for this candidate");
        }
        return this.date.format(DateTimeFormatter.ISO_LOCAL_DATE);
    }
}
