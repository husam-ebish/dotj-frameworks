package org.dotj.internal.cancellation;

/** Parent cancellation reaches the linked child; child close detaches links. */
public final class CancellationLinkedTest {
    public static void main(String[] args) {
        CancellationSource first = new CancellationSource();
        CancellationSource second = new CancellationSource();
        CancellationSource child = CancellationSource.linked(first.token(), second.token());
        if (child.isCancellationRequested()) {
            throw new AssertionError("Linked source started canceled");
        }
        second.cancel();
        if (!child.isCancellationRequested()) {
            throw new AssertionError("Parent cancellation did not propagate");
        }
        child.close();
        first.cancel();
        CancellationSource canceledParent = new CancellationSource();
        canceledParent.cancel();
        CancellationSource alreadyCanceled = CancellationSource.linked(canceledParent.token());
        if (!alreadyCanceled.isCancellationRequested()) {
            throw new AssertionError("Already canceled parent did not propagate");
        }
        alreadyCanceled.close();
        System.out.println("PASS: internal linked cancellation propagation");
    }
}
