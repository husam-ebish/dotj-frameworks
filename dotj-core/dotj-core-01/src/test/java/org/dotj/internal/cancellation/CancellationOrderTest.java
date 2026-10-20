package org.dotj.internal.cancellation;

import java.util.ArrayList;
import java.util.List;

/** Designed internal counterpart for the pinned LIFO callback observation. */
public final class CancellationOrderTest {
    public static void main(String[] args) {
        CancellationSource source = new CancellationSource();
        List<Integer> calls = new ArrayList<>();
        source.token().register(() -> calls.add(1));
        source.token().register(() -> calls.add(2));
        source.token().register(() -> calls.add(3));
        source.cancel();
        if (!calls.equals(List.of(3, 2, 1))) {
            throw new AssertionError("Expected LIFO callbacks: " + calls);
        }
        source.cancel();
        if (calls.size() != 3) {
            throw new AssertionError("Repeated cancellation invoked callbacks again");
        }
        System.out.println("PASS: internal LIFO cancellation callbacks");
    }
}
