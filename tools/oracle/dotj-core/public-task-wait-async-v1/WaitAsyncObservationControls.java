// SPDX-License-Identifier: MIT
import System.Action;
import System.InvalidOperationException;
import System.TimeSpan;
import System.TimeoutException;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskCompletionSource;
import System.Threading.Tasks.ValueTask;
import java.util.concurrent.atomic.AtomicReference;

public final class WaitAsyncObservationControls {
    static void check(String name,boolean value){WaitAsyncObservationFixtures.require(value,name);java.lang.System.out.println(name+"\tb\ttrue");}
    static void queued(){
        var caller=new CancellationTokenSource();var o=new WaitAsyncObservationFixtures.CancelObservation();
        try{
            // Cancellation registrations execute LIFO. This earlier blocker keeps Cancel
            // active until the later Delay cancellation's queued callback is observed.
            caller.get_Token().Register(new Action(()->WaitAsyncObservationFixtures.await(o.waitDone)));
            Task queued=Task.Delay(-1,caller.get_Token());queued.GetAwaiter().OnCompleted(new Action(()->o.observeWait(queued)));
            o.begin();try{caller.Cancel();}finally{o.end();}
            WaitAsyncObservationFixtures.await(o.waitDone);
            check("queued-published-canceled",o.waitSawCanceled&&queued.get_IsCanceled());
            check("queued-before-return-not-inline",o.waitCount==1&&o.waitInCancel&&!o.waitSameThread&&!o.inline());
            String before=o.snapshot();var source=new TaskCompletionSource();source.get_Task().GetAwaiter().OnCompleted(new Action(o::observeSource));
            o.begin();try{source.SetResult();}finally{o.end();}WaitAsyncObservationFixtures.await(o.sourceDone);
            check("source-inline-cannot-overwrite-queued-wait",o.sourceSameThread&&o.sourceInCancel&&before.equals(o.snapshot())&&!o.inline());
        }finally{caller.Dispose();}
    }
    static void late(){
        var caller=new CancellationTokenSource();var source=new TaskCompletionSource();var o=new WaitAsyncObservationFixtures.CancelObservation();var held=new AtomicReference<Runnable>();
        try{
            Task wait=source.get_Task().WaitAsync(caller.get_Token());wait.GetAwaiter().OnCompleted(new Action(()->held.set(()->o.observeWait(wait))));
            o.begin();try{caller.Cancel();}finally{o.end();}
            check("late-published-before-observation",wait.get_IsCanceled()&&o.waitCount==0&&held.get()!=null);
            held.get().run();WaitAsyncObservationFixtures.await(o.waitDone);
            check("same-thread-after-return-not-inline",o.waitSameThread&&!o.waitInCancel&&o.waitSawCanceled&&!o.inline());
            String before=o.snapshot();source.get_Task().GetAwaiter().OnCompleted(new Action(o::observeSource));source.SetResult();WaitAsyncObservationFixtures.await(o.sourceDone);
            check("source-cannot-overwrite-late-wait",before.equals(o.snapshot())&&!o.inline());
        }finally{caller.Dispose();}
    }
    static void results(){
        var a=new CancellationTokenSource();var b=new CancellationTokenSource();a.Cancel();b.Cancel();
        try{
            Task ta=Task.FromCanceled(a.get_Token()),tb=Task.FromCanceled(b.get_Token()),ta2=Task.FromCanceled(a.get_Token());
            Throwable eb=WaitAsyncObservationFixtures.result(tb),ea2=WaitAsyncObservationFixtures.result(ta2);
            check("wrong-token-rejected",!new WaitAsyncObservationFixtures.ResultObservation("source-cancel",eb,null,a.get_Token(),tb).matches);
            check("wrong-task-rejected",!new WaitAsyncObservationFixtures.ResultObservation("caller-cancel",ea2,null,a.get_Token(),ta).matches);
            var fault=new InvalidOperationException("stored");var other=new InvalidOperationException("same type wrong object");
            var producer=new TaskCompletionSource();producer.SetException(fault);var value=new ValueTask(producer.get_Task());Throwable actual=null;
            try{value.GetAwaiter().GetResult();}catch(Throwable e){actual=e;}
            check("actual-valuetask-stored-fault-accepted",new WaitAsyncObservationFixtures.ResultObservation("fault",actual,fault,a.get_Token(),producer.get_Task()).matches);
            check("same-class-wrong-fault-object-rejected",!new WaitAsyncObservationFixtures.ResultObservation("fault",actual,other,a.get_Token(),producer.get_Task()).matches);
            Task timeout=new TaskCompletionSource().get_Task().WaitAsync(TimeSpan.Zero);Throwable timeoutError=WaitAsyncObservationFixtures.result(timeout);
            check("wrong-timeout-object-rejected",!new WaitAsyncObservationFixtures.ResultObservation("timeout",timeoutError,new TimeoutException(),a.get_Token(),timeout).matches);
            check("success-with-error-rejected",!new WaitAsyncObservationFixtures.ResultObservation("success",actual,null,a.get_Token(),producer.get_Task()).matches);
            var success=new WaitAsyncObservationFixtures.ResultObservation("success",null,null,a.get_Token(),producer.get_Task());
            check("nonapplicable-facets-explicit",success.matches&&success.storedIdentity.equals("not-applicable")&&success.tokenMatch.equals("not-applicable")&&success.taskMatch.equals("not-applicable"));
        }finally{a.Dispose();b.Dispose();}
    }
    public static void main(String[] args)throws java.lang.Exception{WaitAsyncObservationFixtures.origin(args[0]);WaitAsyncObservationFixtures.callbackProbe();check("actual-positive-shared-observer",true);queued();late();results();}
}
