// SPDX-License-Identifier: MIT
import System.Action;
import System.Exception;
import System.ArgumentNullException;
import System.InvalidOperationException;
import System.OperationCanceledException;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskStatus;
import System.Threading.Tasks.TaskCanceledException;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public final class PublicTaskRunTokenFixtures {
    static final String[] CASES={"null-none","null-live","null-requested","none","default","live","precanceled","disposed-live","disposed-requested","running-return","running-ordinary","matching-requested","equal-source-token","matching-unrequested","foreign-requested","foreign-unrequested","default-oce","none-oce-requested","old-run-oce","disposed-matching","cancel-then-ordinary"};
    static void emit(String id,String field,String type,Object value) { java.lang.System.out.println(id+"."+field+"\t"+type+"\t"+value); }
    static Throwable result(Task task) { try { task.GetAwaiter().GetResult();return null; }catch(Throwable error){return error;} }
    static void waitFor(CountDownLatch gate) {try {if(!gate.await(5,TimeUnit.SECONDS))throw new AssertionError("fixture gate timeout");}catch(InterruptedException error){throw new AssertionError(error);} }
    static boolean is(String id,String... values) {for(String value:values)if(id.equals(value))return true;return false;}
    static void run(String id) {
        var source=new CancellationTokenSource();var other=new CancellationTokenSource();
        var entered=new CountDownLatch(1);var release=new CountDownLatch(1);
        CancellationToken token=source.get_Token();
        if(is(id,"none","null-none"))token=CancellationToken.get_None();
        if(id.equals("default"))token=new CancellationToken();
        final CancellationToken associated=token;
        if(is(id,"precanceled","disposed-requested","null-requested"))source.Cancel();
        if(id.startsWith("disposed-")&&!id.equals("disposed-matching"))source.Dispose();
        try {
            if(id.startsWith("null-")) {
                try {Task.Run(null,associated);throw new AssertionError("null action accepted");}
                catch(ArgumentNullException error){emit(id,"parameter","s",error.get_ParamName());emit(id,"hresult","i",error.get_HResult());}
                return;
            }
            var calls=new AtomicInteger();Exception error=null;
            if(is(id,"running-ordinary","cancel-then-ordinary"))error=new InvalidOperationException("ordinary");
            CancellationToken thrownToken=associated;
            if(id.equals("equal-source-token")) {thrownToken=source.get_Token();if(thrownToken==associated||!thrownToken.Equals(associated))throw new AssertionError("distinct equal token objects");}
            if(id.startsWith("foreign-"))thrownToken=other.get_Token();
            if(id.equals("foreign-requested"))other.Cancel();
            if(is(id,"default-oce","none-oce-requested"))thrownToken=new CancellationToken();
            if(id.contains("oce")||is(id,"matching-requested","matching-unrequested","equal-source-token","foreign-requested","foreign-unrequested","disposed-matching"))error=new OperationCanceledException("original",thrownToken);
            final Exception original=error;
            boolean cancel=is(id,"running-return","running-ordinary","matching-requested","equal-source-token","none-oce-requested","old-run-oce","disposed-matching","cancel-then-ordinary");
            Action action=new Action(()->{calls.incrementAndGet();entered.countDown();waitFor(release);if(original!=null)throw original;});
            Task task=id.equals("old-run-oce")?Task.Run(action):Task.Run(action,associated);
            if(!is(id,"precanceled","disposed-requested")) {
                waitFor(entered);if(cancel)source.Cancel();if(id.equals("disposed-matching"))source.Dispose();
                emit(id,"heldRunning","b",task.get_Status()==TaskStatus.Running&&!task.get_IsCompleted());release.countDown();
            }
            Throwable first=result(task),second=result(task);
            emit(id,"calls","i",calls.get());emit(id,"status","i",task.get_Status().$raw());
            emit(id,"completed","b",task.get_IsCompleted());emit(id,"success","b",task.get_IsCompletedSuccessfully());
            emit(id,"canceled","b",task.get_IsCanceled());emit(id,"faulted","b",task.get_IsFaulted());
            emit(id,"exceptionType","s",first==null?"null":first.getClass().getName());
            emit(id,"originalIdentity","b",original==null||first==original);
            emit(id,"repeatIdentity","b",first instanceof TaskCanceledException&&original==null||first==second);
            emit(id,"taskIdentity","b",!(first instanceof TaskCanceledException canceled)||canceled.get_Task()==task);
            emit(id,"tokenEquals","b",!(first instanceof OperationCanceledException oce)||oce.get_CancellationToken().Equals(associated));
            emit(id,"exceptionNull","b",task.get_Exception()==null);
            emit(id,"aggregateOriginal","b",task.get_Exception()==null||task.get_Exception().get_InnerExceptions().length==1&&task.get_Exception().get_InnerExceptions()[0]==original);
        } finally {release.countDown();source.Dispose();other.Dispose();}
    }
    public static void main(String[] args)throws java.lang.Exception {
        Path jar=Path.of(args[0]).toRealPath();
        for(Class<?> type:new Class<?>[]{Task.class,Action.class,CancellationToken.class,CancellationTokenSource.class,OperationCanceledException.class,TaskCanceledException.class})
            if(!Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar))throw new AssertionError("JAR origin "+type);
        for(String id:CASES)run(id);
    }
}
