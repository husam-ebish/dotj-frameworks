import System.Action;
import System.Action_1;
import System.Exception;
import System.IAsyncDisposable;
import System.InvalidOperationException;
import System.OperationCanceledException;
import System.Threading.Tasks.Sources.IValueTaskSource;
import System.Threading.Tasks.Sources.ValueTaskSourceOnCompletedFlags;
import System.Threading.Tasks.Sources.ValueTaskSourceStatus;
import System.Threading.Tasks.ValueTask;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.function.BiConsumer;

/** Public consumer of the selected ValueTask surface; uses only .NET names. */
public final class PublicValueTaskFixtures {
    private static final List<String> LINES = new ArrayList<>();

    private static void record(String key, Object value) { LINES.add(key + "=" + value); }

    private static String thrown(Runnable action) {
        try {
            action.run();
            return "none";
        } catch (Exception error) {
            return error.getClass().getName() + "|" + error.get_HResult() + "|" + error.get_Message();
        }
    }

    private static final class Source implements IValueTaskSource {
        final short token;
        ValueTaskSourceStatus status;
        Exception failure;
        int statusCalls, resultCalls, onCompletedCalls;
        short lastToken;
        int lastFlags = -1;
        Object lastState;
        Action_1<Object> continuation;

        Source(short token) { this(token, ValueTaskSourceStatus.Pending, null); }

        Source(short token, ValueTaskSourceStatus status, Exception failure) {
            this.token = token;
            this.status = status;
            this.failure = failure;
        }

        private void check(short supplied) {
            lastToken = supplied;
            if (supplied != token) {
                throw new InvalidOperationException("fixture token");
            }
        }

        @Override
        public ValueTaskSourceStatus GetStatus(short supplied) {
            check(supplied);
            statusCalls++;
            return status;
        }

        @Override
        public void GetResult(short supplied) {
            check(supplied);
            resultCalls++;
            if (ValueTaskSourceStatus.Pending.Equals(status)) {
                throw new InvalidOperationException("fixture pending");
            }
            if (failure != null) {
                throw failure;
            }
        }

        @Override
        public void OnCompleted(Action_1<Object> done, Object state, short supplied, ValueTaskSourceOnCompletedFlags flags) {
            check(supplied);
            onCompletedCalls++;
            lastFlags = flags.$raw();
            lastState = state;
            continuation = done;
            if (!ValueTaskSourceStatus.Pending.Equals(status)) {
                done.Invoke(state);
            }
        }

        void complete(ValueTaskSourceStatus finished) {
            status = finished;
            if (continuation != null) {
                continuation.Invoke(lastState);
            }
        }
    }

    private static final class Disposer implements IAsyncDisposable {
        int calls;
        private final ValueTask result;
        Disposer(ValueTask result) { this.result = result; }
        @Override
        public ValueTask DisposeAsync() {
            calls++;
            return result;
        }
    }

    private static void flags(String prefix, BiConsumer<Source, Action> register, Source source) {
        boolean[] ran = {false};
        Action continuation = new Action(() -> ran[0] = true);
        register.accept(source, continuation);
        record(prefix + ".calls", source.onCompletedCalls);
        record(prefix + ".flags", source.lastFlags);
        record(prefix + ".token", source.lastToken);
        record(prefix + ".stateSame", source.lastState == continuation);
        source.complete(ValueTaskSourceStatus.Succeeded);
        record(prefix + ".ran", ran[0]);
    }

    public static void main(String[] arguments) throws java.lang.Exception {
        ValueTask none = new ValueTask();
        record("default.completed", none.get_IsCompleted());
        record("default.success", none.get_IsCompletedSuccessfully());
        record("default.faulted", none.get_IsFaulted());
        record("default.canceled", none.get_IsCanceled());
        record("default.getResult", thrown(() -> none.GetAwaiter().GetResult()));
        record("default.awaiterCompleted", none.GetAwaiter().get_IsCompleted());
        record("default.equalsCompletedTask", none.Equals(ValueTask.get_CompletedTask()));
        record("default.hash", none.GetHashCode());
        record("default.operatorEqual", ValueTask.op_Equality(none, ValueTask.get_CompletedTask()));
        record("default.equalsObjectNull", none.Equals((Object) null));
        record("default.equalsObjectOther", none.Equals((Object) "x"));

        record("ctor.null", thrown(() -> new ValueTask(null, (short) 0)));

        Source pending = new Source((short) 7);
        ValueTask pendingTask = new ValueTask(pending, (short) 7);
        record("pending.completed", pendingTask.get_IsCompleted());
        record("pending.success", pendingTask.get_IsCompletedSuccessfully());
        record("pending.faulted", pendingTask.get_IsFaulted());
        record("pending.canceled", pendingTask.get_IsCanceled());
        record("pending.statusCalls", pending.statusCalls);
        record("pending.awaiterCompleted", pendingTask.GetAwaiter().get_IsCompleted());
        record("pending.getResult", thrown(() -> pendingTask.GetAwaiter().GetResult()));
        record("pending.resultCalls", pending.resultCalls);

        Source succeeded = new Source((short) -8, ValueTaskSourceStatus.Succeeded, null);
        ValueTask succeededTask = new ValueTask(succeeded, (short) -8);
        record("succeeded.completed", succeededTask.get_IsCompleted());
        record("succeeded.success", succeededTask.get_IsCompletedSuccessfully());
        record("succeeded.faulted", succeededTask.get_IsFaulted());
        record("succeeded.getResult", thrown(() -> succeededTask.GetAwaiter().GetResult()));
        record("succeeded.resultCalls", succeeded.resultCalls);
        record("succeeded.token", succeeded.lastToken);

        Exception failure = new Exception("boom");
        Source faulted = new Source((short) 3, ValueTaskSourceStatus.Faulted, failure);
        ValueTask faultedTask = new ValueTask(faulted, (short) 3);
        record("faulted.completed", faultedTask.get_IsCompleted());
        record("faulted.success", faultedTask.get_IsCompletedSuccessfully());
        record("faulted.faulted", faultedTask.get_IsFaulted());
        record("faulted.canceled", faultedTask.get_IsCanceled());
        try {
            faultedTask.GetAwaiter().GetResult();
            record("faulted.same", "none");
        } catch (Exception error) {
            record("faulted.same", error == failure);
        }
        OperationCanceledException cancel = new OperationCanceledException();
        Source canceledSource = new Source((short) 4, ValueTaskSourceStatus.Canceled, cancel);
        ValueTask canceledTask = new ValueTask(canceledSource, (short) 4);
        record("canceled.completed", canceledTask.get_IsCompleted());
        record("canceled.faulted", canceledTask.get_IsFaulted());
        record("canceled.canceled", canceledTask.get_IsCanceled());
        record("canceled.getResult", thrown(() -> canceledTask.GetAwaiter().GetResult()));
        Source unknown = new Source((short) 5, new ValueTaskSourceStatus(9), null);
        ValueTask unknownTask = new ValueTask(unknown, (short) 5);
        record("unknownStatus.completed", unknownTask.get_IsCompleted());
        record("unknownStatus.success", unknownTask.get_IsCompletedSuccessfully());
        record("unknownStatus.faulted", unknownTask.get_IsFaulted());

        record("wrongToken", thrown(() -> new ValueTask(new Source((short) 1), (short) 2).get_IsCompleted()));

        Source equalSource = new Source((short) 1);
        record("equal.sameSameToken", new ValueTask(equalSource, (short) 1).Equals(new ValueTask(equalSource, (short) 1)));
        record("equal.hash", new ValueTask(equalSource, (short) 1).GetHashCode() == new ValueTask(equalSource, (short) 1).GetHashCode());
        record("equal.differentToken", new ValueTask(equalSource, (short) 1).Equals(new ValueTask(equalSource, (short) 2)));
        record("equal.differentSource", new ValueTask(equalSource, (short) 1).Equals(new ValueTask(new Source((short) 1), (short) 1)));
        record("equal.operatorInequality", ValueTask.op_Inequality(new ValueTask(equalSource, (short) 1), new ValueTask(equalSource, (short) 2)));
        record("equal.objectSame", new ValueTask(equalSource, (short) 1).Equals((Object) new ValueTask(equalSource, (short) 1)));

        flags("await.onCompleted", (s, c) -> new ValueTask(s, s.token).GetAwaiter().OnCompleted(c), new Source((short) 11));
        flags("await.unsafe", (s, c) -> new ValueTask(s, s.token).GetAwaiter().UnsafeOnCompleted(c), new Source((short) 12));
        flags("configured.true.onCompleted", (s, c) -> new ValueTask(s, s.token).ConfigureAwait(true).GetAwaiter().OnCompleted(c), new Source((short) 13));
        flags("configured.true.unsafe", (s, c) -> new ValueTask(s, s.token).ConfigureAwait(true).GetAwaiter().UnsafeOnCompleted(c), new Source((short) 14));
        flags("configured.false.onCompleted", (s, c) -> new ValueTask(s, s.token).ConfigureAwait(false).GetAwaiter().OnCompleted(c), new Source((short) 15));
        flags("configured.false.unsafe", (s, c) -> new ValueTask(s, s.token).ConfigureAwait(false).GetAwaiter().UnsafeOnCompleted(c), new Source((short) -8));

        Source already = new Source((short) 21, ValueTaskSourceStatus.Succeeded, null);
        boolean[] alreadyRan = {false};
        new ValueTask(already, (short) 21).GetAwaiter().UnsafeOnCompleted(new Action(() -> alreadyRan[0] = true));
        record("alreadyDone.sourceRanInline", alreadyRan[0]);

        CountDownLatch completedRan = new CountDownLatch(1);
        Thread caller = Thread.currentThread();
        Thread[] callbackThread = {caller};
        none.GetAwaiter().UnsafeOnCompleted(new Action(() -> {
            callbackThread[0] = Thread.currentThread();
            completedRan.countDown();
        }));
        record("completed.unsafeRan", completedRan.await(10, TimeUnit.SECONDS));
        record("completed.otherThread", callbackThread[0] != caller);
        CountDownLatch configuredRan = new CountDownLatch(1);
        none.ConfigureAwait(false).GetAwaiter().OnCompleted(new Action(configuredRan::countDown));
        record("completed.configuredRan", configuredRan.await(10, TimeUnit.SECONDS));

        Source inner = new Source((short) 30);
        Disposer disposer = new Disposer(new ValueTask(inner, (short) 30));
        IAsyncDisposable contract = disposer;
        ValueTask first = contract.DisposeAsync(), second = contract.DisposeAsync();
        record("disposable.calls", disposer.calls);
        record("disposable.equal", first.Equals(second));
        record("disposable.completed", first.get_IsCompleted());
        record("disposable.completedDefault", new Disposer(new ValueTask()).DisposeAsync().get_IsCompletedSuccessfully());
        Files.write(Path.of(arguments[0]), LINES);
    }
}
