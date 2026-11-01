// SPDX-License-Identifier: MIT
package System.Threading.Tasks;

/** Native TaskStatus values carried as raw Int32 data, including unknown values. */
public final class TaskStatus {
    public static final TaskStatus Created = new TaskStatus(0);
    public static final TaskStatus WaitingForActivation = new TaskStatus(1);
    public static final TaskStatus WaitingToRun = new TaskStatus(2);
    public static final TaskStatus Running = new TaskStatus(3);
    public static final TaskStatus WaitingForChildrenToComplete = new TaskStatus(4);
    public static final TaskStatus RanToCompletion = new TaskStatus(5);
    public static final TaskStatus Canceled = new TaskStatus(6);
    public static final TaskStatus Faulted = new TaskStatus(7);
    private final int code;

    public TaskStatus(int code) { this.code = code; }
    public int $raw() { return code; }
    public boolean Equals(Object other) { return other instanceof TaskStatus value && value.code == code; }
    @Override public boolean equals(Object other) { return Equals(other); }
    @Override public int hashCode() { return code; }
}
