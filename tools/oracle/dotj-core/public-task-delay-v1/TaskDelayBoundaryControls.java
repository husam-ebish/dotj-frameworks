// SPDX-License-Identifier: MIT
// Java-only successor control vocabulary; no product implementation or current execution.
// Concrete controlled schedules and assertions are in private-control-design.json.
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

final class TaskDelayBoundaryControls {
    private TaskDelayBoundaryControls() { }

    static final class Phases {
        final CountDownLatch entered = new CountDownLatch(1);
        final CountDownLatch release = new CountDownLatch(1);
        final CountDownLatch returned = new CountDownLatch(1);
        final AtomicInteger sequence = new AtomicInteger();
        volatile int releaseOrder;
        volatile int returnOrder;

        void enterAndWait() throws InterruptedException {
            entered.countDown();
            require(release.await(2, TimeUnit.SECONDS), "release envelope");
        }

        void release() {
            releaseOrder = sequence.incrementAndGet();
            release.countDown();
        }

        void returned() {
            returnOrder = sequence.incrementAndGet();
            returned.countDown();
        }

        void assertReturnedAfterRelease() {
            require(releaseOrder > 0 && returnOrder > releaseOrder, "actual return order");
        }
    }

    static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
}
