// SPDX-License-Identifier: MIT
package System.Threading.Tasks;

import System.ArgumentNullException;
import System.Exception;
import System.InvalidOperationException;
import System.Threading.CancellationToken;

/** Default nongeneric promise producer. Only this package can publish Task completion. */
public final class TaskCompletionSource {
    private final Task task = new Task();

    public TaskCompletionSource() { }
    public Task get_Task() { return task; }
    public boolean TrySetResult() { return task.complete(TaskStatus.RanToCompletion, null, CancellationToken.get_None()); }
    public void SetResult() { requireWon(TrySetResult()); }
    public boolean TrySetException(Exception exception) {
        if (exception == null) throw new ArgumentNullException("exception");
        return task.complete(TaskStatus.Faulted, exception, CancellationToken.get_None());
    }
    public void SetException(Exception exception) { requireWon(TrySetException(exception)); }
    public boolean TrySetCanceled() { return TrySetCanceled(CancellationToken.get_None()); }
    public boolean TrySetCanceled(CancellationToken cancellationToken) {
        // Null has no native value-type counterpart; reject this Java representation input.
        if (cancellationToken == null) throw new ArgumentNullException("cancellationToken");
        return task.complete(TaskStatus.Canceled, null, cancellationToken);
    }
    public void SetCanceled() { requireWon(TrySetCanceled()); }
    public void SetCanceled(CancellationToken cancellationToken) { requireWon(TrySetCanceled(cancellationToken)); }

    private static void requireWon(boolean won) {
        if (!won) throw new InvalidOperationException(
            "An attempt was made to transition a task to a final state when it had already completed.");
    }
}
