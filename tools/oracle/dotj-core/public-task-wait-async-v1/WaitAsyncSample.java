// SPDX-License-Identifier: MIT
import System.TimeSpan;
import System.OperationCanceledException;
import System.TimeoutException;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskCompletionSource;
import java.nio.file.Path;
public final class WaitAsyncSample {
    static void emit(String name,boolean value){java.lang.System.out.println("sample."+name+"\tb\t"+value);}
    static Throwable result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Throwable e){return e;}}
    public static void main(String[] args)throws java.lang.Exception{
        Path jar=Path.of(args[0]).toRealPath();for(Class<?> type:new Class<?>[]{Task.class,TaskCompletionSource.class,CancellationTokenSource.class,TimeoutException.class})if(!Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar))throw new AssertionError("JAR origin");
        var work=new TaskCompletionSource();var caller=new CancellationTokenSource();Task waiting=work.get_Task().WaitAsync(new TimeSpan(100000000),caller.get_Token());work.SetResult();emit("success",result(waiting)==null);caller.Cancel();emit("success-survives-late-cancel",waiting.get_IsCompletedSuccessfully());
        var borrowed=new TaskCompletionSource();var stopWaiting=new CancellationTokenSource();Task canceled=borrowed.get_Task().WaitAsync(stopWaiting.get_Token());stopWaiting.Cancel();emit("wait-canceled",result(canceled) instanceof OperationCanceledException e&&e.get_CancellationToken().Equals(stopWaiting.get_Token()));emit("work-independent",!borrowed.get_Task().get_IsCompleted());borrowed.SetResult();emit("work-completes",result(borrowed.get_Task())==null);
        var slow=new TaskCompletionSource();Task deadline=slow.get_Task().WaitAsync(new TimeSpan(0));emit("timeout",result(deadline) instanceof TimeoutException&&!slow.get_Task().get_IsCompleted());slow.SetResult();caller.Dispose();stopWaiting.Dispose();
    }
}
