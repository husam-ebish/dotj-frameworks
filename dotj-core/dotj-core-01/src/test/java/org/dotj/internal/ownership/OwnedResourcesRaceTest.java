package org.dotj.internal.ownership;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public final class OwnedResourcesRaceTest {
    private OwnedResourcesRaceTest() {
    }

    public static void main(String[] args) throws Exception {
        ExecutorService workers = Executors.newFixedThreadPool(2);
        try {
            for (int attempt = 0; attempt < 200; attempt++) {
                OwnedResources scope = new OwnedResources();
                AtomicInteger closeCount = new AtomicInteger();
                CountDownLatch start = new CountDownLatch(1);
                Future<Boolean> registration = workers.submit(() -> {
                    start.await();
                    try {
                        scope.addOwned(closeCount::incrementAndGet);
                        return true;
                    } catch (IllegalStateException expected) {
                        return false;
                    }
                });
                Future<?> closing = workers.submit(() -> {
                    start.await();
                    scope.close();
                    return null;
                });
                start.countDown();
                boolean accepted = registration.get(5, TimeUnit.SECONDS);
                closing.get(5, TimeUnit.SECONDS);
                scope.close();
                if (closeCount.get() != (accepted ? 1 : 0)) {
                    throw new AssertionError("ownership race lost or double-closed a resource");
                }
            }
            System.out.println("PASS: 200 registration/close races preserve accepted ownership");
        } finally {
            workers.shutdownNow();
            workers.awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}
