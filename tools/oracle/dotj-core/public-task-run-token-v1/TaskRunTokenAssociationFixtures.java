// SPDX-License-Identifier: MIT
import System.Action;
import System.Exception;
import System.InvalidOperationException;
import System.OperationCanceledException;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskCanceledException;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
public final class TaskRunTokenAssociationFixtures {
    static void emit(String id,String field,String kind,Object value){java.lang.System.out.println(id+"."+field+"\t"+kind+"\t"+value);}
    static Throwable result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Throwable error){return error;}}
    static void await(CountDownLatch gate){try{if(!gate.await(5,TimeUnit.SECONDS))throw new AssertionError("association gate timeout");}catch(InterruptedException error){throw new AssertionError(error);}}
    static void observe(String id,String stage,Task task,CancellationToken associated,CancellationToken equal){
        var exception=new TaskCanceledException(task);var found=exception.get_CancellationToken();
        emit(id,stage+".taskIdentity","b",exception.get_Task()==task);emit(id,stage+".associatedEquals","b",found.Equals(associated));
        emit(id,stage+".equalSourceEquals","b",found.Equals(equal));emit(id,stage+".requested","b",found.get_IsCancellationRequested());
        emit(id,stage+".cancelable","b",found.get_CanBeCanceled());emit(id,stage+".status","i",task.get_Status().$raw());
        if(exception.get_Task()!=task||!found.Equals(associated)||!found.Equals(equal))throw new AssertionError("Run association lost: "+id+"/"+stage);
    }
    public static void main(String[] args)throws java.lang.Exception {
        Path jar=Path.of(args[0]).toRealPath();for(Class<?> type:new Class<?>[]{Task.class,TaskCanceledException.class,CancellationToken.class})if(!Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar))throw new AssertionError("association JAR origin");
        for(String id:new String[]{"none","default","live-success","live-fault","request-success","request-fault","equal-source-success","equal-source-fault","disposed-before-entry","dispose-after-entry","request-dispose-success","request-dispose-fault","matching-oce","old-run-action"}){
            var source=new CancellationTokenSource();var entered=new CountDownLatch(1);var release=new CountDownLatch(1);
            CancellationToken supplied=source.get_Token(),equal=source.get_Token();
            if(id.equals("none"))supplied=equal=CancellationToken.get_None();if(id.equals("default"))supplied=equal=new CancellationToken();
            var associated=id.equals("old-run-action")?CancellationToken.get_None():supplied;if(id.equals("old-run-action"))equal=CancellationToken.get_None();
            if(id.startsWith("equal-source")&&(supplied==equal||!supplied.Equals(equal)))throw new AssertionError("distinct equal source tokens required");
            if(id.equals("disposed-before-entry"))source.Dispose();
            final Exception original=id.contains("fault")?new InvalidOperationException("association fault"):id.equals("matching-oce")?new OperationCanceledException("association original",supplied):null;
            Action action=new Action(()->{entered.countDown();await(release);if(original!=null)throw original;});Task task=id.equals("old-run-action")?Task.Run(action):Task.Run(action,supplied);
            try{
                await(entered);if(id.startsWith("request")||id.equals("matching-oce"))source.Cancel();
                if(id.equals("dispose-after-entry")||id.equals("request-dispose-success")||id.equals("request-dispose-fault"))source.Dispose();
                observe(id,"running",task,associated,equal);release.countDown();Throwable first=result(task),second=result(task);
                observe(id,"completed",task,associated,equal);emit(id,"originalIdentity","b",first==original);emit(id,"repeatIdentity","b",first==second);
                emit(id,"exceptionNull","b",task.get_Exception()==null);emit(id,"aggregateOriginal","b",task.get_Exception()==null||task.get_Exception().get_InnerExceptions().length==1&&task.get_Exception().get_InnerExceptions()[0]==original);
            }finally{release.countDown();source.Dispose();}
        }
    }
}
