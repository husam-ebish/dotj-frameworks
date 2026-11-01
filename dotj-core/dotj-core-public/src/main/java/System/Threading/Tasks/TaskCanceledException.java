// SPDX-License-Identifier: MIT
package System.Threading.Tasks;

import System.OperationCanceledException;
import System.Threading.CancellationToken;

/** Selected nullable-Task constructor and original Task identity. */
public class TaskCanceledException extends OperationCanceledException {
    private final Task task;

    public TaskCanceledException(Task task) {
        super("A task was canceled.", task == null ? CancellationToken.get_None() : task.cancellationToken());
        this.task = task;
    }

    public Task get_Task() { return task; }
}
