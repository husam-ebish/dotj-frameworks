// SPDX-License-Identifier: MIT
import System.Action;
import System.OperationCanceledException;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskStatus;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
public final class SupplementRunTokenFixtures {
    static void emit(String id,String field,String kind,Object value){java.lang.System.out.println(id+"."+field+"\t"+kind+"\t"+value);}
    static Throwable result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Throwable error){return error;}}
    static void await(CountDownLatch gate){try{if(!gate.await(5,TimeUnit.SECONDS))throw new AssertionError("gate timeout");}catch(InterruptedException error){throw new AssertionError(error);}}
    public static void main(String[] args)throws java.lang.Exception {
        Path jar=Path.of(args[0]).toRealPath();for(Class<?> type:new Class<?>[]{Task.class,CancellationToken.class,OperationCanceledException.class})if(!Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar))throw new AssertionError("actual JAR");
        for(String id:new String[]{"foreign-both-requested","foreign-unrequested-associated-requested","none-token-oce","default-token-oce"}) {
            var source=new CancellationTokenSource();var other=new CancellationTokenSource();var entered=new CountDownLatch(1);var release=new CountDownLatch(1);
            var associated=id.equals("none-token-oce")?CancellationToken.get_None():id.equals("default-token-oce")?new CancellationToken():source.get_Token();
            var thrown=id.startsWith("foreign-")?other.get_Token():new CancellationToken();if(id.equals("foreign-both-requested"))other.Cancel();
            var original=new OperationCanceledException("supplement original",thrown);var calls=new AtomicInteger();
            Action action=new Action(()->{calls.incrementAndGet();entered.countDown();await(release);throw original;});Task task=Task.Run(action,associated);
            try {
                await(entered);if(id.startsWith("foreign-"))source.Cancel();emit(id,"heldRunning","b",task.get_Status()==TaskStatus.Running&&!task.get_IsCompleted());release.countDown();
                Throwable first=result(task),second=result(task);
                emit(id,"calls","i",calls.get());emit(id,"status","i",task.get_Status().$raw());emit(id,"canceled","b",task.get_IsCanceled());
                emit(id,"associatedRequested","b",associated.get_IsCancellationRequested());emit(id,"thrownRequested","b",thrown.get_IsCancellationRequested());
                emit(id,"tokenEquals","b",associated.Equals(thrown));emit(id,"exceptionType","s",first==null?"null":first.getClass().getName());
                emit(id,"originalIdentity","b",first==original);emit(id,"repeatIdentity","b",first==second);
                emit(id,"aggregateOriginal","b",task.get_Exception()!=null&&task.get_Exception().get_InnerExceptions().length==1&&task.get_Exception().get_InnerExceptions()[0]==original);
            }finally{release.countDown();source.Dispose();other.Dispose();}
        }
    }
}
