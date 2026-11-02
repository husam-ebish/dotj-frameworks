// SPDX-License-Identifier: MIT
import System.Action;
import System.ArgumentException;
import System.ArgumentOutOfRangeException;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskCanceledException;
import System.TimeSpan;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.Base64;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

/** Packaged consumer of the adopted corpus. All observations come from actual calls. */
public final class PublicTaskDelayProductFixtures {
    private static final ThreadLocal<Integer> STACK = ThreadLocal.withInitial(() -> 0);
    private static final String[] STRINGS = {"kind","exceptionType","message","paramName","actualValueKind","actualValue","status","awaitType","repeatType","awaitMessage","repeatMessage","shape","winner"};
    private static final String[] INTEGERS = {"hresult","callbackCalls","lateCalls","unsafeCalls","awaitHresult","repeatHresult"};
    private static final String[] BOOLEANS = {"completed","successful","canceled","faulted","exceptionNull","completedTaskIdentity","awaitTaskIdentity","awaitTokenEqual","repeatTaskIdentity","repeatTokenEqual","tokenCanBeCanceled","tokenRequested","stateBeforeReturn","sameCallStack","secondWhileBlocked","asyncCompleted"};
    private static void need(boolean ok,String label) { if(!ok)throw new AssertionError(label); }
    private static void waitFor(CountDownLatch gate) {
        try { need(gate.await(2,TimeUnit.SECONDS),"bounded handshake"); }
        catch(InterruptedException e) { throw new AssertionError(e); }
    }
    private static void join(Thread thread) throws java.lang.Exception { thread.join(2000);need(!thread.isAlive(),"bounded join"); }
    private static void finish(Task task) { var done=new CountDownLatch(1);task.GetAwaiter().UnsafeOnCompleted(new Action(done::countDown));waitFor(done); }
    private static Map<String,Object> row() {
        var r=new TreeMap<String,Object>();for(var k:STRINGS)r.put(k,"");for(var k:INTEGERS)r.put(k,0);for(var k:BOOLEANS)r.put(k,false);return r;
    }
    private static void error(Map<String,Object> r,ArgumentOutOfRangeException e) {
        r.put("kind","argument");r.put("exceptionType",e.getClass().getName());r.put("message",e.get_Message());
        r.put("hresult",e.get_HResult());r.put("paramName",e.get_ParamName()==null?"":e.get_ParamName());
        r.put("actualValueKind",e.get_ActualValue()==null?"null":e.get_ActualValue().getClass().getName());
        r.put("actualValue",e.get_ActualValue()==null?"":e.get_ActualValue().toString());
    }
    private static void state(Map<String,Object> r,Task task,CancellationToken token) {
        String status=switch(task.get_Status().$raw()){case 1 -> "WaitingForActivation";case 5 -> "RanToCompletion";case 6 -> "Canceled";case 7 -> "Faulted";default -> throw new AssertionError("unexpected delay status carrier");};
        r.put("status",status);r.put("completed",task.get_IsCompleted());r.put("successful",task.get_IsCompletedSuccessfully());
        r.put("canceled",task.get_IsCanceled());r.put("faulted",task.get_IsFaulted());r.put("exceptionNull",task.get_Exception()==null);
        r.put("completedTaskIdentity",task==Task.get_CompletedTask());r.put("tokenCanBeCanceled",token.get_CanBeCanceled());r.put("tokenRequested",token.get_IsCancellationRequested());
        r.put("kind",task.get_IsCanceled()?"canceled":task.get_IsCompletedSuccessfully()?"success":task.get_IsFaulted()?"faulted":"pending");
        if(!task.get_IsCompleted())return;
        for(var prefix:new String[]{"await","repeat"}) {
            try { task.GetAwaiter().GetResult();r.put(prefix+"Type","returned"); }
            catch(TaskCanceledException e) {
                r.put(prefix+"Type",e.getClass().getName());r.put(prefix+"Message",e.get_Message());r.put(prefix+"Hresult",e.get_HResult());
                r.put(prefix+"TaskIdentity",e.get_Task()==task);r.put(prefix+"TokenEqual",e.get_CancellationToken().Equals(token));
            }
        }
    }
    private static Task invoke(String api,long value,CancellationToken token) {
        return switch(api) {
            case "FromCanceled" -> Task.FromCanceled(token);
            case "DelayInt" -> Task.Delay(Math.toIntExact(value));
            case "DelayIntToken" -> Task.Delay(Math.toIntExact(value),token);
            case "DelaySpan" -> Task.Delay(new TimeSpan(value));
            case "DelaySpanToken" -> Task.Delay(new TimeSpan(value),token);
            default -> throw new AssertionError("unknown API");
        };
    }
    private static void invocation(Map<String,Object> r,String api,long value,String kind) {
        var source=new CancellationTokenSource();
        var token=switch(kind) {case "none" -> CancellationToken.get_None();case "default" -> new CancellationToken();case "boolRequested" -> new CancellationToken(true);default -> source.get_Token();};
        try {
            if(kind.equals("requested")||kind.equals("disposedRequested"))source.Cancel();
            if(kind.equals("disposed")||kind.equals("disposedRequested"))source.Dispose();
            r.put("tokenCanBeCanceled",token.get_CanBeCanceled());r.put("tokenRequested",token.get_IsCancellationRequested());
            Task task;
            try { task=invoke(api,value,token); }catch(ArgumentOutOfRangeException e){error(r,e);return;}
            if(api.equals("FromCanceled"))need(task!=Task.FromCanceled(token),"distinct canceled tasks");
            long milliseconds=api.startsWith("DelaySpan")?(long)new TimeSpan(value).get_TotalMilliseconds():value;
            if(!api.equals("FromCanceled")&&kind.equals("live")&&(milliseconds==-1||milliseconds>10))source.Cancel();
            if(!task.get_IsCompleted()&&milliseconds>=0&&milliseconds<=10)finish(task);
            state(r,task,token);
        } finally { source.Dispose(); }
    }
    private static void shape(Map<String,Object> r,String api) throws java.lang.Exception {
        Class<?>[] params=switch(api) {case "FromCanceled" -> new Class<?>[]{CancellationToken.class};case "DelayInt" -> new Class<?>[]{int.class};case "DelayIntToken" -> new Class<?>[]{int.class,CancellationToken.class};case "DelaySpan" -> new Class<?>[]{TimeSpan.class};case "DelaySpanToken" -> new Class<?>[]{TimeSpan.class,CancellationToken.class};default -> throw new AssertionError();};
        var name=api.equals("FromCanceled")?api:"Delay";var method=Task.class.getMethod(name,params);
        need(method.getReturnType()==Task.class&&java.lang.reflect.Modifier.isStatic(method.getModifiers()),"exact shape");
        String parameters=switch(api) {case "FromCanceled" -> "System.Threading.CancellationToken cancellationToken";case "DelayInt" -> "System.Int32 millisecondsDelay";case "DelayIntToken" -> "System.Int32 millisecondsDelay,System.Threading.CancellationToken cancellationToken";case "DelaySpan" -> "System.TimeSpan delay";default -> "System.TimeSpan delay,System.Threading.CancellationToken cancellationToken";};
        r.put("kind","shape");r.put("shape","public static System.Threading.Tasks.Task "+name+"("+parameters+")");
    }
    private static void callbacks(Map<String,Object> r) {
        var source=new CancellationTokenSource();var first=new CountDownLatch(1);var second=new CountDownLatch(1);var late=new CountDownLatch(1);
        var a=new AtomicInteger();var b=new AtomicInteger();var c=new AtomicInteger();var task=Task.Delay(-1,source.get_Token());
        try {
            task.GetAwaiter().OnCompleted(new Action(()->{a.incrementAndGet();first.countDown();}));
            task.GetAwaiter().UnsafeOnCompleted(new Action(()->{b.incrementAndGet();second.countDown();}));source.Cancel();
            r.put("stateBeforeReturn",task.get_IsCanceled());waitFor(first);waitFor(second);
            task.GetAwaiter().OnCompleted(new Action(()->{c.incrementAndGet();late.countDown();}));waitFor(late);source.Cancel();
            r.put("callbackCalls",a.get());r.put("unsafeCalls",b.get());r.put("lateCalls",c.get());state(r,task,source.get_Token());
        } finally {source.Dispose();}
    }
    private static void shared(Map<String,Object> r,boolean async) {
        var source=new CancellationTokenSource();var token=source.get_Token();var one=Task.Delay(-1,token);var two=Task.Delay(60000,token);
        var first=new CountDownLatch(1);var second=new CountDownLatch(1);var a=new AtomicInteger();var b=new AtomicInteger();
        one.GetAwaiter().OnCompleted(new Action(()->{a.incrementAndGet();first.countDown();}));two.GetAwaiter().UnsafeOnCompleted(new Action(()->{b.incrementAndGet();second.countDown();}));
        try {
            if(async){var cancellation=source.CancelAsync();finish(cancellation);cancellation.GetAwaiter().GetResult();r.put("asyncCompleted",cancellation.get_IsCompletedSuccessfully());}else source.Cancel();
            waitFor(first);waitFor(second);need(a.get()==1&&b.get()==1&&two.get_IsCanceled(),"shared tasks");
            for(int i=0;i<2;i++){try{two.GetAwaiter().GetResult();throw new AssertionError("canceled result");}catch(TaskCanceledException e){need(e.get_Task()==two&&e.get_CancellationToken().Equals(token),"second canceled identity");}}
            r.put("callbackCalls",a.get()+b.get());state(r,one,token);
        }finally{source.Cancel();waitFor(first);waitFor(second);source.Dispose();}
    }
    private static void dispatch(Map<String,Object> r) throws java.lang.Exception {
        var source=new CancellationTokenSource();var entered=new CountDownLatch(1);var release=new CountDownLatch(1);var exited=new CountDownLatch(1);var returned=new CountDownLatch(1);
        var token=source.get_Token();var task=Task.Delay(-1,token);var inline=new AtomicBoolean();var calls=new AtomicInteger();
        task.GetAwaiter().UnsafeOnCompleted(new Action(()->{inline.set(STACK.get()==73);calls.incrementAndGet();entered.countDown();try{waitFor(release);}finally{exited.countDown();}}));
        var canceler=new Thread(()->{STACK.set(73);try{source.Cancel();}finally{STACK.remove();returned.countDown();}});canceler.setDaemon(true);canceler.start();
        try{waitFor(entered);waitFor(returned);r.put("stateBeforeReturn",task.get_IsCanceled());r.put("secondWhileBlocked",exited.getCount()!=0);}
        finally{release.countDown();join(canceler);waitFor(exited);source.Dispose();}
        r.put("sameCallStack",inline.get());r.put("callbackCalls",calls.get());state(r,task,token);
    }
    private static void isolation(Map<String,Object> r) {
        var entered=new CountDownLatch(1);var release=new CountDownLatch(1);var exited=new CountDownLatch(1);var task=Task.Delay(40);
        task.GetAwaiter().UnsafeOnCompleted(new Action(()->{entered.countDown();try{waitFor(release);}finally{exited.countDown();}}));
        try{waitFor(entered);var second=Task.Delay(1);finish(second);r.put("secondWhileBlocked",second.get_IsCompletedSuccessfully()&&exited.getCount()!=0);r.put("stateBeforeReturn",task.get_IsCompletedSuccessfully());}
        finally{release.countDown();waitFor(exited);}state(r,task,CancellationToken.get_None());
    }
    private static void race(Map<String,Object> r) {
        var source=new CancellationTokenSource();var callback=new CountDownLatch(1);var task=Task.Delay(1,source.get_Token());var calls=new AtomicInteger();var inline=new AtomicBoolean();
        task.GetAwaiter().UnsafeOnCompleted(new Action(()->{inline.set(STACK.get()==73);calls.incrementAndGet();callback.countDown();}));
        STACK.set(73);try{source.Cancel();}finally{STACK.remove();}
        waitFor(callback);state(r,task,source.get_Token());r.put("winner",task.get_IsCanceled()?"cancel":"timer");r.put("sameCallStack",inline.get());r.put("callbackCalls",calls.get());source.Dispose();
    }
    private static void origin(Path jar) throws java.lang.Exception {
        for(var name:new String[]{"System.Threading.Tasks.Task","System.TimeSpan","System.Threading.CancellationToken","System.Threading.CancellationTokenRegistration","System.Threading.CancellationTokenSource","System.Threading.Tasks.TaskCanceledException","System.Runtime.CompilerServices.TaskAwaiter","org.dotj.internal.async.TaskBridge"}) {
            var type=Class.forName(name);need(Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar.toRealPath()),"JAR-only origin: "+name);
            need(type.getModule().isNamed()&&type.getModule().getName().equals("dotj.core.foundation.v1"),"matching named module");
        }
    }
    public static void main(String[] args) throws java.lang.Exception {
        need(args.length==4,"manifest, input TSV, partition, candidate JAR");origin(Path.of(args[3]));
        String hash=java.util.HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(Path.of(args[0]))));
        java.lang.System.out.println("META\tpublic-task-delay-v1\t10.0.12\t"+hash);
        for(String line:Files.readAllLines(Path.of(args[1]),StandardCharsets.UTF_8)) {
            String[] input=line.split("\t",-1);need(input.length==7,"closed input fields");if(!input[6].equals(args[2]))continue;
            String id=input[0];java.lang.System.out.println("BEGIN\t"+id);java.lang.System.out.flush();var r=row();
            switch(input[1]){case "shape" -> shape(r,input[2]);case "invoke" -> invocation(r,input[2],Long.parseLong(input[3]),input[4]);case "callbacks" -> callbacks(r);case "shared" -> shared(r,false);case "cancelAsync" -> shared(r,true);case "dispatch" -> dispatch(r);case "isolation" -> isolation(r);case "race" -> race(r);default -> throw new AssertionError("unknown scenario");}
            for(var entry:r.entrySet()) {
                Object value=entry.getValue();String kind=value instanceof Boolean?"b":value instanceof Integer?"i":"s";
                String encoded=kind.equals("s")?Base64.getEncoder().encodeToString(((String)value).getBytes(StandardCharsets.UTF_8)):value.toString();
                java.lang.System.out.println(id+"."+entry.getKey()+"\t"+kind+"\t"+encoded);
            }
            java.lang.System.out.println("END\t"+id);java.lang.System.out.flush();
        }
    }
}
