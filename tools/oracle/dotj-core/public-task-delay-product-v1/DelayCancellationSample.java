// SPDX-License-Identifier: MIT
import System.Action;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskCanceledException;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public final class DelayCancellationSample {
    public static void main(String[] args) throws java.lang.Exception {
        if(!Path.of(Task.class.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(Path.of(args[0]).toRealPath()))throw new AssertionError("packaged JAR origin");
        var finite=Task.Delay(1);var done=new CountDownLatch(1);finite.GetAwaiter().OnCompleted(new Action(done::countDown));
        if(!done.await(2,TimeUnit.SECONDS))throw new AssertionError("bounded completion");finite.GetAwaiter().GetResult();
        if(!finite.get_IsCompletedSuccessfully())throw new AssertionError("finite success");
        java.lang.System.out.println("sample.success\tb\ttrue");
        var source=new CancellationTokenSource();var token=source.get_Token();
        try {
            Task pending=Task.Delay(-1,token);source.Cancel();
            try{pending.GetAwaiter().GetResult();throw new AssertionError("cancellation required");}
            catch(TaskCanceledException canceled){if(canceled.get_Task()!=pending||!canceled.get_CancellationToken().Equals(token))throw new AssertionError("canceled identity");}
            java.lang.System.out.println("sample.canceled\tb\ttrue");
        } finally { source.Dispose(); }
    }
}
