// SPDX-License-Identifier: MIT
import System.Action;
import System.InvalidOperationException;
import System.OperationCanceledException;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskCanceledException;
import System.Threading.Tasks.TaskCompletionSource;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

public final class WaitAsyncDepthFixtures {
    static final int DEPTH=8192;
    static final AtomicReference<String> UNCAUGHT=new AtomicReference<>("none");
    static void check(boolean value,String message){if(!value)throw new AssertionError(message);}
    static void await(CountDownLatch gate){try{check(gate.await(10,TimeUnit.SECONDS),"bounded tail completion");}catch(InterruptedException e){throw new AssertionError(e);}}
    static void emit(String id,String name,String kind,Object value){java.lang.System.out.println(id+"."+name+"\t"+kind+"\t"+value);}
    static Throwable result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Throwable e){return e;}}
    static void run(String id,String outcome){
        var source=new TaskCompletionSource();var caller=new CancellationTokenSource();var sourceCts=new CancellationTokenSource();
        CancellationToken callerToken=caller.get_Token(),sourceToken=sourceCts.get_Token();var fault=new InvalidOperationException("deep stored fault");
        var tasks=new Task[DEPTH];Task previous=source.get_Task();boolean distinct=true;
        try{
            for(int i=0;i<DEPTH;i++){tasks[i]=previous.WaitAsync(callerToken);distinct&=tasks[i]!=previous;previous=tasks[i];}
            var tailDone=new CountDownLatch(1);var callbacks=new AtomicInteger();previous.GetAwaiter().OnCompleted(new Action(()->{callbacks.incrementAndGet();tailDone.countDown();}));
            Throwable rootFailure=null;String borrowed="not-applicable";
            try{
                if(outcome.equals("caller-cancel")){caller.Cancel();borrowed=source.get_Task().get_IsCompleted()?"completed":"pending";}
                else if(outcome.equals("source-cancel")){sourceCts.Cancel();source.SetCanceled(sourceToken);}
                else if(outcome.equals("fault"))source.SetException(fault);
                else source.SetResult();
            }catch(Throwable e){rootFailure=e;}
            check(rootFailure==null,"root completion must not throw "+rootFailure);await(tailDone);
            int completed=0,successful=0,faulted=0,canceled=0;boolean payloadMatches=true;
            for(Task task:tasks){
                if(task.get_IsCompleted())completed++;if(task.get_IsCompletedSuccessfully())successful++;if(task.get_IsFaulted())faulted++;if(task.get_IsCanceled())canceled++;
                check(task.get_IsCompleted(),"all wrappers terminal before result observation");Throwable error=result(task);
                payloadMatches&=outcome.equals("success")?error==null:outcome.equals("fault")?error==fault:error instanceof TaskCanceledException e&&e.get_Task()==task&&e.get_CancellationToken().Equals(outcome.equals("source-cancel")?sourceToken:callerToken);
            }
            check(completed==DEPTH&&payloadMatches&&distinct,"complete chain with original payload ownership");
            boolean usable=caller.get_Token().Equals(callerToken)&&sourceCts.get_Token().Equals(sourceToken);
            if(outcome.equals("caller-cancel")){check(borrowed.equals("pending"),"caller cancellation borrows source");source.SetResult();}
            boolean callerRequestedBeforeDispose=callerToken.get_IsCancellationRequested(),sourceRequestedBeforeDispose=sourceToken.get_IsCancellationRequested();
            caller.Dispose();sourceCts.Dispose();
            emit(id,"depth","i",DEPTH);emit(id,"completed","i",completed);emit(id,"successful","i",successful);emit(id,"faulted","i",faulted);emit(id,"canceled","i",canceled);
            emit(id,"tailCompleted","b",previous.get_IsCompleted());emit(id,"tailStatus","i",previous.get_Status().$raw());emit(id,"tailCallbacks","i",callbacks.get());emit(id,"allPayloadsMatch","b",payloadMatches);
            emit(id,"rootFailure","s",rootFailure==null?"null":rootFailure.getClass().getName());emit(id,"uncaughtFailure","s",UNCAUGHT.get());emit(id,"rootCompleted","b",source.get_Task().get_IsCompleted());
            emit(id,"callerRequested","b",callerToken.get_IsCancellationRequested());emit(id,"sourceRequested","b",sourceToken.get_IsCancellationRequested());emit(id,"distinctWrappers","b",distinct);
            emit(id,"borrowedSourceAfterCallerCancel","s",borrowed);emit(id,"callerAndSourceUsableAfterCompletion","b",usable);emit(id,"tokensStableAfterDispose","b",callerRequestedBeforeDispose==callerToken.get_IsCancellationRequested()&&sourceRequestedBeforeDispose==sourceToken.get_IsCancellationRequested()&&callerToken.get_CanBeCanceled()&&sourceToken.get_CanBeCanceled());
            check(UNCAUGHT.get().equals("none"),"no unhandled continuation failure");
        }finally{caller.Dispose();sourceCts.Dispose();}
    }
    public static void main(String[] args)throws java.lang.Exception{
        Path jar=Path.of(args[0]).toRealPath();for(Class<?> type:new Class<?>[]{Task.class,TaskCompletionSource.class,CancellationTokenSource.class,TaskCanceledException.class,OperationCanceledException.class})check(Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar),"same packaged JAR");
        Thread.setDefaultUncaughtExceptionHandler((thread,error)->UNCAUGHT.compareAndSet("none",error.getClass().getName()));int n=1;for(String outcome:new String[]{"success","fault","source-cancel","caller-cancel"})run("D00"+n++,outcome);
    }
}
