package org.dotj.internal.ownership;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public final class OwnedResourcesReentrancyTest {
    private OwnedResourcesReentrancyTest() {
    }

    public static void main(String[] args) throws Exception {
        ExecutorService worker = Executors.newSingleThreadExecutor();
        try {
            OwnedResources scope = new OwnedResources();
            AtomicInteger callbackCount = new AtomicInteger();
            AtomicInteger rejectedCloseCount = new AtomicInteger();
            scope.addOwned(() -> {
                callbackCount.incrementAndGet();
                scope.close();
                Future<Boolean> registration = worker.submit(() -> {
                    try {
                        scope.addOwned(rejectedCloseCount::incrementAndGet);
                        return false;
                    } catch (IllegalStateException expected) {
                        return true;
                    }
                });
                if (!registration.get(5, TimeUnit.SECONDS)) {
                    throw new AssertionError("closed scope accepted registration from callback");
                }
            });
            scope.close();
            scope.close();
            if (callbackCount.get() != 1 || rejectedCloseCount.get() != 0) {
                throw new AssertionError("reentrant close repeated callback or took rejected ownership");
            }
            System.out.println("PASS: close callback reentrancy and unlocked rejection");
        } finally {
            worker.shutdownNow();
            worker.awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}
