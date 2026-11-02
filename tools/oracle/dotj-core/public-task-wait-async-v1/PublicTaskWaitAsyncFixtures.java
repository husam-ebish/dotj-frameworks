// SPDX-License-Identifier: MIT
import System.Action;
import System.AggregateException;
import System.ArgumentException;
import System.Exception;
import System.InvalidOperationException;
import System.OperationCanceledException;
import System.TimeoutException;
import System.TimeSpan;
import System.Type;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskCanceledException;
import System.Threading.Tasks.TaskCompletionSource;
import System.Threading.Tasks.ValueTask;
import System.Runtime.Serialization.FormatterConverter;
import System.Runtime.Serialization.SerializationInfo;
import System.Runtime.Serialization.StreamingContext;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Base64;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/** Independently authored Java consumer of the frozen typed native matrix. */
public final class PublicTaskWaitAsyncFixtures {
    static void emit(String id,String field,String kind,Object value){java.lang.System.out.println(id+"."+field+"\t"+kind+"\t"+(value==null?"null":value));}
    static String encoded(String s){return Base64.getEncoder().encodeToString(s.getBytes(StandardCharsets.UTF_8));}
    static Throwable result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Throwable e){return e;}}
    static boolean is(String value,String...choices){for(String c:choices)if(c.equals(value))return true;return false;}
    static void waitFor(CountDownLatch gate){try{if(!gate.await(5,TimeUnit.SECONDS))throw new AssertionError("fixture gate timeout");}catch(InterruptedException e){throw new AssertionError(e);}}
    static final class Source implements AutoCloseable {
        final CancellationTokenSource cts=new CancellationTokenSource();
        final CountDownLatch entered=new CountDownLatch(1),release=new CountDownLatch(1);
        final CancellationToken token=cts.get_Token();Task task;Exception original;Runnable finish;
        Source(String kind,String terminal){
            if(is(kind,"run","run-token","run-fault","run-oce")){
                if(kind.equals("run-fault"))original=new InvalidOperationException("original");
                if(kind.equals("run-oce"))original=new OperationCanceledException("original",token);
                Action body=new Action(()->{entered.countDown();waitFor(release);if(original!=null)throw original;});
                task=kind.equals("run")?Task.Run(body):Task.Run(body,token);waitFor(entered);
                finish=()->{if(kind.equals("run-oce"))cts.Cancel();release.countDown();result(task);};return;
            }
            if(kind.equals("cancelasync")){cts.get_Token().Register(new Action(()->{entered.countDown();waitFor(release);}));task=cts.CancelAsync();waitFor(entered);finish=()->{release.countDown();result(task);};return;}
            if(kind.equals("delay")){task=Task.Delay(-1,token);finish=()->{cts.Cancel();result(task);};return;}
            if(kind.equals("from-canceled")){cts.Cancel();task=Task.FromCanceled(token);finish=()->{};return;}
            var producer=new TaskCompletionSource();task=producer.get_Task();
            String end=kind.equals("tcs-none")?"cancel-none":kind.equals("tcs-live")?"cancel-live":kind.equals("tcs-requested")?"cancel-requested":terminal;
            if(end.equals("fault"))original=new InvalidOperationException("original");
            if(end.equals("aggregate"))original=new AggregateException(new InvalidOperationException("inner"));
            if(end.equals("oce"))original=new OperationCanceledException("original",token);
            finish=()->{if(is(end,"cancel-requested","cancel")){cts.Cancel();producer.TrySetCanceled(token);}else if(end.equals("cancel-live"))producer.TrySetCanceled(token);else if(end.equals("cancel-none"))producer.TrySetCanceled();else if(original!=null)producer.TrySetException(original);else producer.TrySetResult();};
            if(is(kind,"success","fault","cancel"))finish.run();
        }
        public void close(){release.countDown();cts.Dispose();}
    }
    static Task call(Task source,String overload,long ticks,CancellationToken token){return switch(overload){case "token"->source.WaitAsync(token);case "timeout"->source.WaitAsync(new TimeSpan(ticks));default->source.WaitAsync(new TimeSpan(ticks),token);};}
    static void ordinary(String[] row){
        String id=row[0],group=row[1],kind=row[3],win=row[6];long ticks=Long.parseLong(row[5]);
        String terminal=group.equals("pending-winners")?win:kind.equals("fault")?"fault":kind.equals("cancel")?"cancel":group.equals("value-task-consumption")?win:"success";
        if(is(win,"caller","timeout","source"))terminal="success";
        try(var source=new Source(kind,terminal)){
            var caller=new CancellationTokenSource();try{
                CancellationToken token=row[4].equals("none")?CancellationToken.get_None():caller.get_Token();
                if(row[4].equals("requested"))caller.Cancel();
                if(group.equals("token-and-cause-interop")&&row[7].equals("completed"))source.finish.run();
                if(group.equals("value-task-consumption")&&row[7].equals("alias"))source.finish.run();
                Task wait=null;Throwable thrown=null;String initial="synchronous-refusal";
                try{wait=call(source.task,row[2],ticks,token);initial=wait.get_IsCompleted()?"terminal":wait==source.task?"borrowed":"WaitingForActivation";}catch(Throwable e){thrown=e;}
                if(group.equals("validation")){source.finish.run();if(wait!=null)result(wait);payload(id,source,caller,wait,thrown,"validation",false,false,false);return;}
                boolean beforeSource=wait!=null&&new TaskCanceledException(wait).get_CancellationToken().Equals(source.token);
                boolean beforeCaller=wait!=null&&new TaskCanceledException(wait).get_CancellationToken().Equals(caller.get_Token());
                if(wait!=null){
                    if(win.equals("caller")&&!row[7].equals("alias"))caller.Cancel();else if(win.equals("timeout")&&!row[7].equals("alias"))result(wait);
                    source.finish.run();thrown=result(wait);
                    if(group.equals("value-task-consumption")){
                        var value=new ValueTask(wait);if(value.AsTask()!=wait||value.Preserve().AsTask()!=wait)throw new AssertionError("ValueTask ownership");
                        Throwable v=null,p=null;try{value.GetAwaiter().GetResult();}catch(Throwable e){v=e;}try{value.ConfigureAwait(false).GetAwaiter().GetResult();}catch(Throwable e){p=e;}
                        if((thrown==null?null:thrown.getClass())!=(v==null?null:v.getClass())||(thrown==null?null:thrown.getClass())!=(p==null?null:p.getClass()))throw new AssertionError("ValueTask outcome");
                    }
                }
                payload(id,source,caller,wait,thrown,win.equals("timeout")&&!row[7].equals("alias")?"deadline-armed":initial,true,beforeSource,beforeCaller);
            }finally{caller.Dispose();}
        }
    }
    static void payload(String id,Source source,CancellationTokenSource caller,Task wait,Throwable error,String initial,boolean outcomes,boolean beforeSource,boolean beforeCaller){
        boolean valid=wait!=null;OperationCanceledException oce=error instanceof OperationCanceledException e?e:null;
        AggregateException aggregate=outcomes&&valid?wait.get_Exception():null;
        emit(id,"identity","b",valid&&wait==source.task);emit(id,"initial","s",initial);
        emit(id,"status","i",outcomes&&valid?wait.get_Status().$raw():-1);emit(id,"completed","b",outcomes&&valid&&wait.get_IsCompleted());
        emit(id,"success","b",outcomes&&valid&&wait.get_IsCompletedSuccessfully());emit(id,"faulted","b",outcomes&&valid&&wait.get_IsFaulted());emit(id,"canceled","b",outcomes&&valid&&wait.get_IsCanceled());
        emit(id,"exceptionType","s",error==null?"null":error.getClass().getName());emit(id,"exceptionNull","b",aggregate==null);emit(id,"originalIdentity","b",source.original==null||error==source.original);
        emit(id,"taskIdentity","b",!(error instanceof TaskCanceledException e)||e.get_Task()==wait);
        emit(id,"tokenSource","b",oce!=null&&oce.get_CancellationToken().Equals(source.token));emit(id,"tokenCaller","b",oce!=null&&oce.get_CancellationToken().Equals(caller.get_Token()));
        CancellationToken association=outcomes&&valid?new TaskCanceledException(wait).get_CancellationToken():CancellationToken.get_None();
        emit(id,"associatedSource","b",outcomes&&association.Equals(source.token));emit(id,"associatedCaller","b",outcomes&&association.Equals(caller.get_Token()));
        emit(id,"sourceStatus","i",source.task.get_Status().$raw());emit(id,"aggregateIdentity","b",aggregate==null||aggregate.get_InnerExceptions().length==1&&aggregate.get_InnerExceptions()[0]==error);
        emit(id,"repeatIdentity","b",!outcomes||!valid||error instanceof TaskCanceledException||error==result(wait));
        emit(id,"beforeSource","b",beforeSource);emit(id,"beforeCaller","b",beforeCaller);
        emit(id,"parameter","s",error instanceof ArgumentException e?e.get_ParamName():"null");emit(id,"hresult","i",error instanceof Exception e?e.get_HResult():0);emit(id,"message","s",error instanceof ArgumentException e?encoded(e.get_Message()):"not-observed");
    }
    static void ownership(String[] row){
        String id=row[0],extra=row[7];try(var source=new Source("pending",row[6])){
            var caller=new CancellationTokenSource();var second=new CancellationTokenSource();try{
                CancellationToken token=caller.get_Token();if(extra.equals("disposed-before-requested"))caller.Cancel();if(extra.startsWith("disposed-before"))caller.Dispose();
                Task first=source.task.WaitAsync(new TimeSpan(Long.parseLong(row[5])),token);Task other=source.task.WaitAsync(second.get_Token());
                if(extra.equals("disposed-after"))caller.Dispose();boolean nested=true;
                if(extra.equals("nested")){Task n=first.WaitAsync(second.get_Token());second.Cancel();result(n);nested=n.get_IsCanceled()&&!first.get_IsCompleted();}
                if(extra.equals("two-waiters-caller"))caller.Cancel();if(extra.equals("two-waiters-timeout"))result(first);
                boolean independent=!source.task.get_IsCompleted()&&(!other.get_IsCompleted()||extra.equals("nested"));source.finish.run();result(first);result(other);if(extra.equals("cancel-after-source"))caller.Cancel();
                emit(id,"independent","b",independent);emit(id,"borrowed","b",!source.cts.get_IsCancellationRequested()||source.task.get_IsCanceled());emit(id,"nested","b",nested);
            }finally{caller.Dispose();second.Dispose();}
        }
    }
    static void continuations(String[] row){
        String id=row[0],extra=row[7];try(var source=new Source(extra.equals("delay-async")?"delay":"pending","success")){
            var caller=new CancellationTokenSource();try{
                long completing=Thread.currentThread().threadId();boolean[] inline={false},ordered={true};boolean later=true;
                var firstEntered=new CountDownLatch(1);var firstRelease=new CountDownLatch(1);var secondDone=new CountDownLatch(1);var stage=new AtomicInteger();
                Action first=new Action(()->{if(Thread.currentThread().threadId()==completing)inline[0]=true;stage.compareAndSet(0,1);if(extra.equals("blocked-first")){firstEntered.countDown();waitFor(firstRelease);}});
                if(is(extra,"user-first","blocked-first"))source.task.GetAwaiter().OnCompleted(first);
                Task wait=source.task.WaitAsync(caller.get_Token());
                if(extra.equals("two-runtime")){Task another=source.task.WaitAsync(caller.get_Token());another.GetAwaiter().OnCompleted(new Action(()->{if(stage.get()==0)ordered[0]=false;}));}
                wait.GetAwaiter().OnCompleted(new Action(()->{if(extra.equals("user-first")&&stage.get()!=1)ordered[0]=false;if(extra.equals("runtime-first")&&stage.get()!=0)ordered[0]=false;stage.set(2);}));
                if(!is(extra,"user-first","blocked-first"))source.task.GetAwaiter().OnCompleted(first);if(extra.equals("duplicate"))source.task.GetAwaiter().OnCompleted(first);
                source.task.GetAwaiter().OnCompleted(new Action(()->{if(extra.equals("reentrant"))source.task.GetAwaiter().OnCompleted(new Action(secondDone::countDown));else secondDone.countDown();}));
                if(extra.equals("caller-inline")){caller.Cancel();inline[0]=wait.get_IsCanceled();source.finish.run();}
                else if(extra.equals("blocked-first")){Task worker=Task.Run(new Action(source.finish::run));waitFor(firstEntered);waitFor(secondDone);later=!worker.get_IsCompleted();firstRelease.countDown();result(worker);}else source.finish.run();
                result(wait);waitFor(secondDone);
                emit(id,"ordered","b",ordered[0]);emit(id,"inline","b",inline[0]);emit(id,"laterIndependent","b",later);
            }finally{caller.Dispose();}
        }
    }
    static void exceptionCase(String[] row){
        String id=row[0],kind=row[7];Exception inner=new InvalidOperationException("inner");String message=is(kind,"null","inner-null")?null:kind.equals("empty")?"":kind.contains("unicode")?"time Ω 超时":"custom";
        TimeoutException e=kind.equals("default")?new TimeoutException():kind.startsWith("inner-")?new TimeoutException(message,kind.equals("inner-null")?null:inner):new TimeoutException(message);
        emit(id,"message","s",e.get_Message());emit(id,"hresult","i",e.get_HResult());emit(id,"type","s",e.GetType().get_FullName());emit(id,"base","s",e.GetType().get_BaseType().get_FullName());
        emit(id,"inner","b",e.get_InnerException()==(is(kind,"inner-custom","inner-unicode")?inner:null));emit(id,"baseIdentity","b",e.GetBaseException()==(e.get_InnerException()==null?e:e.get_InnerException()));
        emit(id,"text","s",encoded(e.ToString()));emit(id,"lookup","b",Type.GetType("System.TimeoutException").Equals(e.GetType()));emit(id,"lookupIgnoreCase","b",Type.GetType("system.timeoutexception",false,true).Equals(e.GetType()));
        var info=new SerializationInfo(Type.GetType("System.TimeoutException"),new FormatterConverter());e.GetObjectData(info,new StreamingContext());
        emit(id,"serializationClass","s",info.GetString("ClassName"));emit(id,"serializationMessage","s",info.GetString("Message"));emit(id,"serializationHResult","i",info.GetInt32("HResult"));emit(id,"serializationInner","b",info.GetValue("InnerException",Type.GetType("System.Exception"))==e.get_InnerException());
    }
    public static void main(String[] args)throws java.lang.Exception{
        java.lang.System.setOut(new java.io.PrintStream(java.lang.System.out,true,StandardCharsets.UTF_8));
        Path jar=Path.of(args[0]).toRealPath();
        for(Class<?> type:new Class<?>[]{Task.class,TimeoutException.class,TaskCompletionSource.class,ValueTask.class,CancellationToken.class,CancellationTokenSource.class,Action.class})if(!Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar))throw new AssertionError("JAR origin "+type);
        for(String line:Files.readAllLines(Path.of(args[1]),StandardCharsets.UTF_8)){String[] row=line.split("\t",-1);switch(row[1]){case "ownership-and-independence"->ownership(row);case "continuations"->continuations(row);case "timeout-exception"->exceptionCase(row);default->ordinary(row);}}
    }
}
