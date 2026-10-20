package org.dotj.internal.cancellation;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

/** Registration close waits for a callback running on another thread. */
public final class CancellationCloseWaitTest {
    public static void main(String[] args) throws Exception {
        CancellationSource source = new CancellationSource();
        CountDownLatch entered = new CountDownLatch(1);
        CountDownLatch release = new CountDownLatch(1);
        CancellationRegistration registration = source.token().register(() -> {
            entered.countDown();
            try {
                if (!release.await(10, TimeUnit.SECONDS)) {
                    throw new AssertionError("Callback release timed out");
                }
            } catch (InterruptedException exception) {
                Thread.currentThread().interrupt();
                throw new AssertionError(exception);
            }
        });
        Thread cancel = new Thread(source::cancel);
        cancel.start();
        if (!entered.await(10, TimeUnit.SECONDS)) {
            throw new AssertionError("Callback did not start");
        }
        CountDownLatch closeStarted = new CountDownLatch(1);
        CountDownLatch closeDone = new CountDownLatch(1);
        AtomicBoolean closeReturned = new AtomicBoolean();
        Thread close = new Thread(() -> {
            closeStarted.countDown();
            registration.close();
            closeReturned.set(true);
            closeDone.countDown();
        });
        close.start();
        if (!closeStarted.await(10, TimeUnit.SECONDS) || closeDone.await(100, TimeUnit.MILLISECONDS)) {
            throw new AssertionError("Close returned before running callback completed");
        }
        release.countDown();
        cancel.join(10_000);
        close.join(10_000);
        if (cancel.isAlive() || close.isAlive() || !closeReturned.get()) {
            throw new AssertionError("Callback/close did not finish");
        }
        System.out.println("PASS: internal registration close waits for callback");
    }
}
