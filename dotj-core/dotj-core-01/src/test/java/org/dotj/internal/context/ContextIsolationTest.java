package org.dotj.internal.context;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;

/** Independent Java fixture for designed DJ-001-F01-04. */
public final class ContextIsolationTest {
    private ContextIsolationTest() {
    }

    public static void main(String[] args) throws InterruptedException {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        ThreadLocal<String> ambient = new ThreadLocal<>();
        CountDownLatch completed = new CountDownLatch(2);
        AtomicReference<String> firstRequest = new AtomicReference<>();
        AtomicReference<String> secondRequest = new AtomicReference<>();
        AtomicReference<String> staleAmbient = new AtomicReference<>();
        try {
            ContextTransfer.execute(executor, ContextSnapshot.empty().with("request", "A"), snapshot -> {
                firstRequest.set(snapshot.get("request"));
                ambient.set("ambient-A");
                completed.countDown();
            });
            ContextTransfer.execute(executor, ContextSnapshot.empty().with("request", "B"), snapshot -> {
                staleAmbient.set(ambient.get());
                secondRequest.set(snapshot.get("request"));
                ambient.remove();
                completed.countDown();
            });
            if (!completed.await(5, TimeUnit.SECONDS)) {
                throw new AssertionError("request work did not complete");
            }
            if (!"A".equals(firstRequest.get()) || !"B".equals(secondRequest.get())
                    || !"ambient-A".equals(staleAmbient.get())) {
                throw new AssertionError("explicit context leaked or worker was not reused");
            }
            System.out.println("PASS: DJ-001-F01-04 explicit context isolated on reused worker");
        } finally {
            executor.shutdownNow();
            executor.awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}
