import System.Action;
import System.Threading.CancellationToken;
import System.Threading.Tasks.Task;
public final class BaselineRunToken {
    public static void main(String[] args) { Task.Run(new Action(()->{}),CancellationToken.get_None()); }
}
