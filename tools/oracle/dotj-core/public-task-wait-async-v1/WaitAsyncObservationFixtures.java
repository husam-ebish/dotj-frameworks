// SPDX-License-Identifier: MIT
import System.Action;
import System.InvalidOperationException;
import System.OperationCanceledException;
import System.TimeSpan;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskCanceledException;
import System.Threading.Tasks.TaskCompletionSource;
import System.Threading.Tasks.ValueTask;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public final class WaitAsyncObservationFixtures {
    static void require(boolean value,String message){if(!value)throw new AssertionError(message);}
    static void await(CountDownLatch gate){try{require(gate.await(5,TimeUnit.SECONDS),"bounded observation");}catch(InterruptedException e){throw new AssertionError(e);}}
    static void emit(String id,String name,String kind,Object value){java.lang.System.out.println(id+"."+name+"\t"+kind+"\t"+value);}
    static Throwable result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Throwable e){return e;}}
    // The controls use this exact observer and predicate, not a copied model.
    static final class CancelObservation {
        final Thread cancellationThread=Thread.currentThread();
        final CountDownLatch waitDone=new CountDownLatch(1),sourceDone=new CountDownLatch(1);
        volatile boolean inCancel,waitSameThread,waitInCancel,waitSawCanceled,sourceSameThread,sourceInCancel;
        volatile int waitCount,sourceCount;
        void begin(){inCancel=true;}
        void end(){inCancel=false;}
        void observeWait(Task wait){waitSameThread=Thread.currentThread()==cancellationThread;waitInCancel=inCancel;waitSawCanceled=wait.get_IsCanceled();waitCount++;waitDone.countDown();}
        void observeSource(){sourceSameThread=Thread.currentThread()==cancellationThread;sourceInCancel=inCancel;sourceCount++;sourceDone.countDown();}
        boolean inline(){return waitCount==1&&waitSameThread&&waitInCancel;}
        String snapshot(){return waitCount+":"+waitSameThread+":"+waitInCancel+":"+waitSawCanceled+":"+inline();}
    }
    static void callbackProbe(){
        var caller=new CancellationTokenSource();var source=new TaskCompletionSource();var observation=new CancelObservation();
        try{
            Task wait=source.get_Task().WaitAsync(caller.get_Token());
            wait.GetAwaiter().OnCompleted(new Action(()->observation.observeWait(wait)));
            source.get_Task().GetAwaiter().OnCompleted(new Action(observation::observeSource));
            observation.begin();try{caller.Cancel();}finally{observation.end();}
            await(observation.waitDone);String before=observation.snapshot();
            require(observation.inline()&&observation.waitSawCanceled,"actual wait callback inline during Cancel");
            require(observation.sourceCount==0,"borrowed source independent");
            source.SetResult();await(observation.sourceDone);
            emit("O001","waitCallbacks","i",observation.waitCount);emit("O001","waitSameThread","b",observation.waitSameThread);
            emit("O001","waitInCancel","b",observation.waitInCancel);emit("O001","waitInline","b",observation.inline());emit("O001","waitSawCanceled","b",observation.waitSawCanceled);
            emit("O001","sourceCallbacks","i",observation.sourceCount);emit("O001","sourceSameThread","b",observation.sourceSameThread);emit("O001","sourceInCancel","b",observation.sourceInCancel);
            emit("O001","waitUnaffectedBySource","b",before.equals(observation.snapshot()));
        }finally{caller.Dispose();}
    }
    static final class ResultObservation {
        final String type,storedIdentity,tokenMatch,taskMatch;final boolean succeeded,matches;
        ResultObservation(String outcome,Throwable error,Throwable stored,CancellationToken token,Task wait){
            succeeded=error==null;type=error==null?"null":error.getClass().getName();
            boolean identity=outcome.equals("fault")||outcome.equals("timeout"),canceled=outcome.endsWith("cancel");
            storedIdentity=identity?(error==stored?"same":"different"):"not-applicable";
            tokenMatch=canceled?(error instanceof OperationCanceledException e&&e.get_CancellationToken().Equals(token)?"equal":"different"):"not-applicable";
            taskMatch=canceled?(error instanceof TaskCanceledException e&&e.get_Task()==wait?"same":"different"):"not-applicable";
            matches=outcome.equals("success")?succeeded:identity?error!=null&&error==stored:!succeeded&&tokenMatch.equals("equal")&&taskMatch.equals("same");
        }
        void emitFields(String id,String prefix){emit(id,prefix+"Type","s",type);emit(id,prefix+"Succeeded","b",succeeded);emit(id,prefix+"StoredIdentity","s",storedIdentity);emit(id,prefix+"TokenMatch","s",tokenMatch);emit(id,prefix+"TaskMatch","s",taskMatch);emit(id,prefix+"Matches","b",matches);}
    }
    static void valueProbe(String id,String shape,String outcome){
        var source=new TaskCompletionSource();var sourceCts=new CancellationTokenSource();var caller=new CancellationTokenSource();
        try{
            var fault=new InvalidOperationException("stored observation fault");CancellationToken token=outcome.equals("source-cancel")?sourceCts.get_Token():caller.get_Token();
            Task receiver=source.get_Task();boolean alias=shape.equals("alias");
            if(alias&&(outcome.equals("caller-cancel")||outcome.equals("timeout"))){receiver=receiver.WaitAsync(outcome.equals("timeout")?TimeSpan.Zero:new TimeSpan(100000000),caller.get_Token());if(outcome.equals("caller-cancel"))caller.Cancel();}
            else if(alias){finish(source,sourceCts,fault,outcome);}
            Task wait=receiver.WaitAsync(outcome.equals("timeout")&&!alias?TimeSpan.Zero:new TimeSpan(100000000),caller.get_Token());
            if(!alias){if(outcome.equals("caller-cancel"))caller.Cancel();else if(!outcome.equals("timeout"))finish(source,sourceCts,fault,outcome);}
            Throwable stored=outcome.equals("fault")?fault:outcome.equals("timeout")?wait.get_Exception().get_InnerExceptions()[0]:null;
            var value=new ValueTask(wait);Throwable normal=null,configured=null;
            try{value.GetAwaiter().GetResult();}catch(Throwable e){normal=e;}
            try{value.ConfigureAwait(false).GetAwaiter().GetResult();}catch(Throwable e){configured=e;}
            var first=new ResultObservation(outcome,normal,stored,token,wait);var second=new ResultObservation(outcome,configured,stored,token,wait);
            require(first.matches&&second.matches,"actual ValueTask awaiter facets");
            emit(id,"receiverAlias","b",wait==receiver);emit(id,"asTaskIdentity","b",value.AsTask()==wait);emit(id,"preserveIdentity","b",value.Preserve().AsTask()==wait);
            first.emitFields(id,"normal");second.emitFields(id,"configured");
            if(!source.get_Task().get_IsCompleted())source.SetResult();
        }finally{sourceCts.Dispose();caller.Dispose();}
    }
    static void finish(TaskCompletionSource source,CancellationTokenSource cts,InvalidOperationException fault,String outcome){if(outcome.equals("fault"))source.SetException(fault);else if(outcome.equals("source-cancel")){cts.Cancel();source.SetCanceled(cts.get_Token());}else source.SetResult();}
    static void origin(String path)throws java.lang.Exception{Path jar=Path.of(path).toRealPath();for(Class<?> type:new Class<?>[]{Task.class,TaskCompletionSource.class,ValueTask.class,TaskCanceledException.class,CancellationTokenSource.class})require(Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar),"same JAR origin");}
    public static void main(String[] args)throws java.lang.Exception{origin(args[0]);callbackProbe();int n=2;for(String shape:new String[]{"alias","wrapper"})for(String outcome:new String[]{"success","fault","source-cancel","caller-cancel","timeout"})valueProbe(String.format("O%03d",n++),shape,outcome);}
}
