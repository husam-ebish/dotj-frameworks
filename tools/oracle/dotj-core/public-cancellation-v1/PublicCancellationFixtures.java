import System.Action;
import System.AggregateException;
import System.Exception;
import System.OperationCanceledException;
import System.ObjectDisposedException;
import System.TimeSpan;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenRegistration;
import System.Threading.CancellationTokenSource;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/** Public consumer of the selected cancellation surface; uses only .NET names. */
public final class PublicCancellationFixtures {
    private static final List<String> LINES = new ArrayList<>();

    private static void record(String key, Object value) { LINES.add(key + "=" + value); }

    private static String nativeName(java.lang.Throwable error) { return error.getClass().getName(); }

    private static String thrown(Runnable action) {
        try {
            action.run();
            return "none";
        } catch (Exception error) {
            return nativeName(error) + "|" + error.get_HResult();
        }
    }

    private static boolean finished(CompletableFuture<?> future, long milliseconds) throws java.lang.Exception {
        try {
            future.get(milliseconds, TimeUnit.MILLISECONDS);
            return true;
        } catch (java.util.concurrent.TimeoutException timeout) {
            return false;
        }
    }

    public static void main(String[] arguments) throws java.lang.Exception {
        CancellationToken none = CancellationToken.get_None(), plain = new CancellationToken();
        record("none.canBe", none.get_CanBeCanceled());
        record("none.requested", none.get_IsCancellationRequested());
        record("none.equalsDefault", CancellationToken.op_Equality(none, plain));
        boolean[] noneRan = {false};
        CancellationTokenRegistration noneRegistration = none.Register(new Action(() -> noneRan[0] = true));
        record("none.ran", noneRan[0]);
        record("none.unregister", noneRegistration.Unregister());
        record("none.throwIf", thrown(none::ThrowIfCancellationRequested));

        CancellationToken canceledToken = new CancellationToken(true);
        record("canceled.requested", canceledToken.get_IsCancellationRequested());
        record("canceled.canBe", canceledToken.get_CanBeCanceled());
        record("canceled.equal", CancellationToken.op_Equality(canceledToken, new CancellationToken(true)));
        record("uncanceled.canBe", new CancellationToken(false).get_CanBeCanceled());
        boolean[] constantRan = {false};
        canceledToken.Register(new Action(() -> constantRan[0] = true));
        record("canceled.ran", constantRan[0]);

        CancellationTokenSource source = new CancellationTokenSource();
        CancellationToken token = source.get_Token();
        record("source.sameToken", CancellationToken.op_Equality(token, source.get_Token()));
        record("source.differsFromNone", CancellationToken.op_Inequality(token, CancellationToken.get_None()));
        record("source.hash", token.GetHashCode() == source.get_Token().GetHashCode());
        List<String> order = new ArrayList<>();
        token.Register(new Action(() -> order.add("A")));
        CancellationTokenRegistration removed = token.Register(new Action(() -> order.add("B")));
        token.Register(new Action(() -> order.add("C")));
        record("registration.token", CancellationToken.op_Equality(removed.get_Token(), token));
        record("registration.first", removed.Unregister());
        record("registration.second", removed.Unregister());
        source.Cancel();
        source.Cancel();
        record("order", String.join(",", order));
        boolean[] late = {false};
        CancellationTokenRegistration lateRegistration = token.Register(new Action(() -> late[0] = true));
        record("late.ran", late[0]);
        record("late.unregister", lateRegistration.Unregister());
        record("throwIf", thrown(token::ThrowIfCancellationRequested));
        try {
            token.ThrowIfCancellationRequested();
        } catch (OperationCanceledException error) {
            record("throwIf.message", error.get_Message());
            record("throwIf.token", CancellationToken.op_Equality(error.get_CancellationToken(), token));
        }
        record("oce.default", new OperationCanceledException().get_Message());

        CancellationTokenSource failing = new CancellationTokenSource();
        failing.get_Token().Register(new Action(() -> { throw new Exception("one"); }));
        failing.get_Token().Register(new Action(() -> { throw new Exception("two"); }));
        try {
            failing.Cancel();
        } catch (AggregateException error) {
            record("aggregate.message", error.get_Message());
            record("aggregate.count", error.get_InnerExceptions().length);
            record("aggregate.first", error.get_InnerExceptions()[0].get_Message());
            record("aggregate.inner", error.get_InnerException().get_Message());
            record("aggregate.hresult", error.get_HResult());
        }
        CancellationTokenSource stop = new CancellationTokenSource();
        stop.get_Token().Register(new Action(() -> { throw new Exception("stop"); }));
        record("throwOnFirst", thrown(() -> stop.Cancel(true)));

        CancellationTokenSource reset = new CancellationTokenSource();
        boolean[] resetRan = {false};
        reset.get_Token().Register(new Action(() -> resetRan[0] = true));
        record("reset.result", reset.TryReset());
        reset.Cancel();
        record("reset.ran", resetRan[0]);
        record("reset.afterCancel", reset.TryReset());

        CancellationTokenSource disposed = new CancellationTokenSource();
        CancellationToken kept = disposed.get_Token();
        disposed.Dispose();
        disposed.Dispose();
        record("disposed.token", thrown(disposed::get_Token));
        record("disposed.cancel", thrown(disposed::Cancel));
        record("disposed.cancelAfter", thrown(() -> disposed.CancelAfter(1)));
        record("disposed.tryReset", thrown(disposed::TryReset));
        record("disposed.requested", disposed.get_IsCancellationRequested());
        boolean[] disposedRan = {false};
        CancellationTokenRegistration disposedRegistration = kept.Register(new Action(() -> disposedRan[0] = true));
        record("disposed.ran", disposedRan[0]);
        record("disposed.unregister", disposedRegistration.Unregister());

        CancellationTokenSource canceled = new CancellationTokenSource();
        CancellationToken retained = canceled.get_Token();
        canceled.Cancel();
        canceled.Dispose();
        boolean[] lateDisposed = {false};
        retained.Register(new Action(() -> lateDisposed[0] = true));
        record("canceledDisposed.ran", lateDisposed[0]);

        CancellationTokenSource first = new CancellationTokenSource(), second = new CancellationTokenSource();
        CancellationTokenSource linked = CancellationTokenSource.CreateLinkedTokenSource(first.get_Token(), second.get_Token(), CancellationToken.get_None());
        second.Cancel();
        record("linked.requested", linked.get_IsCancellationRequested());
        record("linked.otherParent", first.get_IsCancellationRequested());

        record("cancelAfter.negative", thrown(() -> new CancellationTokenSource().CancelAfter(-2)));
        CancellationTokenSource timed = new CancellationTokenSource();
        CountDownLatch fired = new CountDownLatch(1);
        timed.get_Token().Register(new Action(fired::countDown));
        timed.CancelAfter(TimeSpan.FromMilliseconds(30));
        record("cancelAfter.fired", fired.await(10, TimeUnit.SECONDS));
        CancellationTokenSource disabled = new CancellationTokenSource();
        disabled.CancelAfter(20);
        disabled.CancelAfter(-1);
        Thread.sleep(200);
        record("cancelAfter.disabled", disabled.get_IsCancellationRequested());

        CancellationTokenSource blocking = new CancellationTokenSource();
        CountDownLatch entered = new CountDownLatch(1), release = new CountDownLatch(1);
        CancellationTokenRegistration held = blocking.get_Token().Register(new Action(() -> {
            entered.countDown();
            try {
                release.await();
            } catch (InterruptedException interrupted) {
                throw new IllegalStateException(interrupted);
            }
        }));
        CompletableFuture<Void> cancel = CompletableFuture.runAsync(blocking::Cancel);
        entered.await();
        CompletableFuture<Void> closing = CompletableFuture.runAsync(held::Dispose);
        record("dispose.waited", !finished(closing, 300));
        release.countDown();
        record("dispose.finished", finished(closing, 10000) && finished(cancel, 10000));
        Files.write(Path.of(arguments[0]), LINES);
    }
}
