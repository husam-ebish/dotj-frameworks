// SPDX-License-Identifier: MIT
package System.Threading.Tasks;
import System.Action;
import System.Exception;
import System.OperationCanceledException;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;
public final class TaskRunTokenAssociationControls {
    static void check(boolean value,String label){if(!value)throw new AssertionError(label);}
    static void mark(String label){java.lang.System.out.println(label+"\tb\ttrue");}
    static void await(CountDownLatch gate){try{check(gate.await(5,TimeUnit.SECONDS),"bounded gate");}catch(InterruptedException error){throw new AssertionError(error);}}
    static Throwable result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Throwable error){return error;}}
    static void association(Task task,CancellationToken token){var exception=new TaskCanceledException(task);check(exception.get_Task()==task&&exception.get_CancellationToken().Equals(token),"associated Task/token");}
    public static void main(String[] args)throws java.lang.Exception {
        check(Path.of(Task.class.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(Path.of(args[0]).toRealPath()),"actual JAR");
        for(boolean canceled:new boolean[]{false,true}){
            var source=new CancellationTokenSource();var token=source.get_Token();var equal=source.get_Token();check(token!=equal&&token.Equals(equal),"equal source wrappers");
            var held=new AtomicReference<Runnable>();Task task=Task.run(new Action(()->{}),token,held::set);association(task,equal);
            check(task.get_Status()==TaskStatus.WaitingToRun&&!task.get_IsCompleted(),"queued association before entry");
            if(canceled)source.Cancel();association(task,equal);source.Dispose();association(task,equal);held.get().run();association(task,equal);
            check(task.get_IsCanceled()==canceled&&new TaskCanceledException(task).get_CancellationToken().get_IsCancellationRequested()==canceled,"lifetime requested state");
        }
        mark("A01-queued-association");mark("A02-disposed-queued-association");mark("A03-equal-source-token");
        for(int kind=0;kind<3;kind++){
            var source=new CancellationTokenSource();var token=source.get_Token();var held=new AtomicReference<Runnable>();var entered=new CountDownLatch(1);var release=new CountDownLatch(1);
            var original=kind==2?new OperationCanceledException("retained association OCE",token):new Exception("retained association fault");final int mode=kind;
            Task task=Task.run(new Action(()->{if(mode!=0)throw original;}),token,held::set,()->{entered.countDown();await(release);});
            Thread worker=new Thread(held.get(),"association-entry-control");worker.setDaemon(true);worker.start();await(entered);association(task,token);source.Cancel();source.Dispose();association(task,token);release.countDown();
            worker.join(5000);check(!worker.isAlive(),"bounded join");association(task,token);Throwable first=result(task);check(first==(kind==0?null:original)&&result(task)==first,"original/repeat identity");
            check(task.get_IsCanceled()==(kind==2)&&task.get_IsFaulted()==(kind==1),"terminal category");
        }
        mark("A04-entry-to-terminal-association");mark("A05-original-OCE-identity");
        var held=new AtomicReference<Runnable>();Task old=Task.run(new Action(()->{}),held::set);association(old,CancellationToken.get_None());held.get().run();association(old,CancellationToken.get_None());mark("A06-old-Run-None");
    }
}
