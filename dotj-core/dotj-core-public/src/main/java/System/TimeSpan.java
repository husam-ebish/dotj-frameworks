// SPDX-License-Identifier: MIT

package System;

/** Immutable tick interval for the selected DateTime arithmetic candidate. */
public final class TimeSpan {
    private final long ticks;

    public TimeSpan(long ticks) {
        this.ticks = ticks;
    }

    public static TimeSpan FromTicks(long ticks) {
        return new TimeSpan(ticks);
    }

    public long get_Ticks() {
        return this.ticks;
    }
}
