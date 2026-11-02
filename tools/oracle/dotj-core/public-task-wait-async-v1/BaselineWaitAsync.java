import System.Threading.Tasks.Task;
import System.Threading.CancellationToken;
import System.TimeSpan;
class BaselineWaitAsync {
    void missing(Task task) {
        task.WaitAsync(CancellationToken.get_None());
        task.WaitAsync(new TimeSpan(0));
        task.WaitAsync(new TimeSpan(0),CancellationToken.get_None());
        new System.TimeoutException();
    }
}
