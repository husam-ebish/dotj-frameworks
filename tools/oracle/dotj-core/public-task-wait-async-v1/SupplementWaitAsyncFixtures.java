// SPDX-License-Identifier: MIT
import System.Action;
import System.Exception;
import System.InvalidOperationException;
import System.OperationCanceledException;
import System.TimeSpan;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskCanceledException;
import System.Threading.Tasks.TaskCompletionSource;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
public final class SupplementWaitAsyncFixtures {
    static final String[] CASES={"tcs-none-before","tcs-live-before","tcs-requested-before","tcs-none-after","tcs-live-after","tcs-requested-after","from-canceled-before","delay-disposed-before","delay-disposed-after","run-before","run-token-before","run-token-after","run-fault-before","run-oce-before","run-oce-after","cancelasync-before","cancelasync-after"};
    static void emit(String id,String name,String kind,Object value){java.lang.System.out.println(id+"."+name+"\t"+kind+"\t"+value);}
    static Throwable result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Throwable e){return e;}}
    static void await(CountDownLatch gate){try{if(!gate.await(5,TimeUnit.SECONDS))throw new AssertionError("supplement gate timeout");}catch(InterruptedException e){throw new AssertionError(e);}}
    static void run(String id){
        var source=new CancellationTokenSource();var caller=new CancellationTokenSource();var entered=new CountDownLatch(1);var release=new CountDownLatch(1);CancellationToken token=source.get_Token();boolean delay=id.startsWith("delay-"),before=id.endsWith("-before");
        try{
            Task original;Runnable finish;Exception errorCause=null;
            if(id.startsWith("tcs-")){var producer=new TaskCompletionSource();original=producer.get_Task();if(id.contains("requested"))source.Cancel();finish=()->{if(id.contains("-none-"))producer.SetCanceled();else producer.SetCanceled(token);};}
            else if(id.startsWith("from-")){source.Cancel();original=Task.FromCanceled(token);finish=()->{};}
            else if(delay){original=Task.Delay(-1,token);finish=caller::Cancel;}
            else if(id.startsWith("cancelasync-")){token.Register(new Action(()->{entered.countDown();await(release);}));original=source.CancelAsync();await(entered);finish=release::countDown;}
            else{
                if(id.startsWith("run-fault-"))errorCause=new InvalidOperationException("original");if(id.startsWith("run-oce-"))errorCause=new OperationCanceledException("original",token);final Exception cause=errorCause;
                Action action=new Action(()->{entered.countDown();await(release);if(cause!=null)throw cause;});original=id.equals("run-before")?Task.Run(action):Task.Run(action,token);await(entered);if(id.startsWith("run-oce-"))source.Cancel();finish=release::countDown;
            }
            Exception cause=errorCause;boolean requested=token.get_IsCancellationRequested();CancellationToken equalCopy=token;if(before)source.Dispose();
            CancellationToken originalBefore=new TaskCanceledException(original).get_CancellationToken();Task wait=original.WaitAsync(new TimeSpan(100000000),caller.get_Token());CancellationToken waitBefore=new TaskCanceledException(wait).get_CancellationToken();if(!before)source.Dispose();
            finish.run();Throwable error=result(wait);if(!delay)result(original);CancellationToken originalAfter=new TaskCanceledException(original).get_CancellationToken(),waitAfter=new TaskCanceledException(wait).get_CancellationToken();
            emit(id,"originalBeforeSource","b",originalBefore.Equals(token));emit(id,"originalBeforeNone","b",originalBefore.Equals(CancellationToken.get_None()));emit(id,"waitBeforeSource","b",waitBefore.Equals(token));emit(id,"waitBeforeNone","b",waitBefore.Equals(CancellationToken.get_None()));
            emit(id,"originalAfterSource","b",originalAfter.Equals(token));emit(id,"originalAfterNone","b",originalAfter.Equals(CancellationToken.get_None()));emit(id,"waitAfterSource","b",waitAfter.Equals(token));emit(id,"waitAfterNone","b",waitAfter.Equals(CancellationToken.get_None()));
            emit(id,"identity","b",original==wait);emit(id,"sourcePending","b",!original.get_IsCompleted());emit(id,"sourceStatus","i",original.get_Status().$raw());emit(id,"waitStatus","i",wait.get_Status().$raw());emit(id,"outcome","s",error==null?"null":error.getClass().getName());
            emit(id,"resultSourceToken","b",error instanceof OperationCanceledException e&&e.get_CancellationToken().Equals(token));emit(id,"resultCallerToken","b",error instanceof OperationCanceledException e&&e.get_CancellationToken().Equals(caller.get_Token()));emit(id,"causeIdentity","b",cause==null||error==cause);emit(id,"syntheticNamesWait","b",!(error instanceof TaskCanceledException e)||e.get_Task()==wait);
            emit(id,"sourceRequested","b",token.get_IsCancellationRequested());emit(id,"callerRequested","b",caller.get_IsCancellationRequested());emit(id,"tokenStableAfterDispose","b",token.Equals(equalCopy)&&token.get_CanBeCanceled()&&token.get_IsCancellationRequested()==requested);
        }finally{release.countDown();source.Dispose();caller.Dispose();}
    }
    public static void main(String[] args)throws java.lang.Exception{
        Path jar=Path.of(args[0]).toRealPath();for(Class<?> type:new Class<?>[]{Task.class,TaskCompletionSource.class,CancellationTokenSource.class,TaskCanceledException.class,OperationCanceledException.class})if(!Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar))throw new AssertionError("JAR origin");for(String id:CASES)run(id);
    }
}
