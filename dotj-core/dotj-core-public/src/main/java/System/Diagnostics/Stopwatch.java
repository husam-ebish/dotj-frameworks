// SPDX-License-Identifier: MIT

package System.Diagnostics;

import System.TimeSpan;

/** Selected 100 ns monotonic counter profile; its origin is unrelated to DateTime ticks. */
public class Stopwatch {
    private static final long ORIGIN_NANOS = java.lang.System.nanoTime();
    public static final long Frequency = counterFrequency();
    public static final boolean IsHighResolution = Frequency > 0L;
    private long accumulated;
    private long started;
    private boolean running;

    public Stopwatch() {
    }

    private static long counterFrequency() {
        return 10_000_000L;
    }

    public static long GetTimestamp() {
        return (java.lang.System.nanoTime() - ORIGIN_NANOS) / 100L;
    }

    public static TimeSpan GetElapsedTime(long startingTimestamp) {
        return GetElapsedTime(startingTimestamp, GetTimestamp());
    }

    public static TimeSpan GetElapsedTime(long startingTimestamp, long endingTimestamp) {
        double tickScale = (double) TimeSpan.TicksPerSecond / Frequency;
        return TimeSpan.FromTicks((long) ((endingTimestamp - startingTimestamp) * tickScale));
    }

    public static Stopwatch StartNew() {
        Stopwatch result = new Stopwatch();
        result.Start();
        return result;
    }

    public final void Start() {
        if (!this.running) {
            this.started = GetTimestamp();
            this.running = true;
        }
    }

    public final void Stop() {
        if (this.running) {
            this.accumulated += GetTimestamp() - this.started;
            this.running = false;
        }
    }

    public final void Reset() {
        this.accumulated = 0L;
        this.started = 0L;
        this.running = false;
    }

    public final void Restart() {
        this.accumulated = 0L;
        this.started = GetTimestamp();
        this.running = true;
    }

    public final boolean get_IsRunning() {
        return this.running;
    }

    public final long get_ElapsedTicks() {
        return this.accumulated + (this.running ? GetTimestamp() - this.started : 0L);
    }

    public final TimeSpan get_Elapsed() {
        return GetElapsedTime(0L, get_ElapsedTicks());
    }

    public final long get_ElapsedMilliseconds() {
        return get_Elapsed().get_Ticks() / TimeSpan.TicksPerMillisecond;
    }

    public String ToString() {
        return get_Elapsed().ToString();
    }

    @Override
    public String toString() {
        return ToString();
    }
}
