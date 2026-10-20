package org.dotj.internal.async;

/** Bounded state checks paired with selected .NET 10.0.12 oracle observations. */
public final class AsyncStateTest {
    public static void main(String[] args) {
        AsyncCompletion<Void> nonGeneric = new AsyncCompletion<>();
        check(nonGeneric.state() == AsyncState.PENDING, "non-generic pending");
        AsyncValue<Void> nonGenericView = AsyncValue.backedBy(nonGeneric);
        check(nonGenericView.state() == AsyncState.PENDING, "backed view pending");
        check(nonGeneric.trySetResult(null), "first non-generic result");
        check(!nonGeneric.trySetResult(null), "duplicate non-generic result");
        check(nonGeneric.state() == AsyncState.SUCCEEDED && nonGenericView.state() == AsyncState.SUCCEEDED,
                "non-generic result state");
        expectAlreadyTerminal(() -> nonGeneric.setResult(null));

        AsyncCompletion<Integer> generic = new AsyncCompletion<>();
        check(generic.state() == AsyncState.PENDING, "generic pending");
        generic.setResult(42);
        check(generic.state() == AsyncState.SUCCEEDED && generic.result() == 42,
                "generic result");
        check(!generic.trySetResult(99) && generic.result() == 42, "first generic result wins");
        AsyncValue<Integer> resultView = AsyncValue.backedBy(generic);
        check(resultView.state() == AsyncState.SUCCEEDED && resultView.result() == 42 &&
                resultView.backing() == generic, "completion-backed successful value");

        Throwable failure = new IllegalArgumentException("fault");
        AsyncCompletion<Integer> faulted = new AsyncCompletion<>();
        faulted.setFault(failure);
        check(faulted.state() == AsyncState.FAULTED && faulted.fault() == failure,
                "fault state and identity");
        check(!faulted.trySetResult(1), "fault is terminal");
        AsyncValue<Integer> faultView = AsyncValue.backedBy(faulted);
        check(faultView.state() == AsyncState.FAULTED && faultView.fault() == failure &&
                faultView.backing() == faulted, "completion-backed faulted value");
        AsyncCompletion<Void> nonGenericFault = new AsyncCompletion<>();
        nonGenericFault.setFault(failure);
        check(AsyncValue.backedBy(nonGenericFault).state() == AsyncState.FAULTED,
                "non-generic completion-backed faulted value");

        AsyncCompletion<Integer> canceled = new AsyncCompletion<>();
        canceled.setCanceled();
        check(canceled.state() == AsyncState.CANCELED && !canceled.trySetCanceled(),
                "cancellation is terminal");
        AsyncValue<Integer> canceledView = AsyncValue.backedBy(canceled);
        check(canceledView.state() == AsyncState.CANCELED && canceledView.backing() == canceled,
                "completion-backed canceled value");
        AsyncCompletion<Void> nonGenericCancel = new AsyncCompletion<>();
        nonGenericCancel.setCanceled();
        check(AsyncValue.backedBy(nonGenericCancel).state() == AsyncState.CANCELED,
                "non-generic completion-backed canceled value");

        AsyncValue<Integer> direct = AsyncValue.completed(42);
        check(direct.state() == AsyncState.SUCCEEDED && direct.result() == 42 &&
                direct.backing() == null, "direct successful value");
        System.out.println("PASS: internal async completion and value state transitions");
    }

    private static void check(boolean condition, String label) {
        if (!condition) {
            throw new AssertionError(label);
        }
    }

    private static void expectAlreadyTerminal(Runnable action) {
        try {
            action.run();
            throw new AssertionError("Duplicate completion succeeded");
        } catch (IllegalStateException expected) {
            // A second SetResult fails after the first terminal transition.
        }
    }
}
