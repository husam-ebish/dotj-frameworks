package org.dotj.internal.build.evaluation;

import java.io.IOException;
import java.lang.reflect.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Consumer-only tests. Frozen fixture expectations precede product implementation. */
public final class CycleTraceProductTest {
    private static Method traced;
    static void require(boolean value,String message) { if(!value)throw new AssertionError(message); }
    static Object invoke(Method method,Object target,Object... args) throws Exception {
        try { return method.invoke(target,args); }
        catch(InvocationTargetException e) { if(e.getCause() instanceof Exception x)throw x;throw (Error)e.getCause(); }
    }
    static Object member(Object value,String name) throws Exception {
        Method method=value.getClass().getDeclaredMethod(name);method.setAccessible(true);return invoke(method,value);
    }
    static Object evaluateTrace(Path file,Path root,Map<String,String> globals,ImportProfile profile) throws Exception {
        return invoke(traced,null,file,root,globals,profile);
    }
    static List<?> traces(Object outcome) throws Exception { return (List<?>)member(outcome,"cycleTraces"); }
    static Object wire(Object value) throws Exception {
        if(value==null||value instanceof String||value instanceof Number||value instanceof Boolean)return value;
        if(value instanceof Path p)return p.toString();
        if(value instanceof Enum<?> e)return e.name();
        if(value instanceof Map<?,?> m) { Map<String,Object> r=new LinkedHashMap<>();for(var e:m.entrySet())r.put(e.getKey().toString(),wire(e.getValue()));return r; }
        if(value instanceof Collection<?> c) { List<Object> r=new ArrayList<>();for(Object e:c)r.add(wire(e));return r; }
        if(value.getClass().isRecord()) {
            Map<String,Object> result=new LinkedHashMap<>();
            for(RecordComponent c:value.getClass().getRecordComponents()) { Method m=c.getAccessor();m.setAccessible(true);result.put(c.getName(),wire(invoke(m,value))); }
            return result;
        }
        throw new AssertionError("Unexpected wire value "+value.getClass());
    }
    static Object observation(Object outcome) throws Exception {
        Result result=(Result)member(outcome,"result");Throwable failure=(Throwable)member(outcome,"failure");
        require((result==null)!=(failure==null),"outcome XOR");
        Object evaluation;
        List<DuplicateImport> diagnostics;
        if(result!=null) {
            evaluation=ItemsJson.object("success",true,"properties",ItemsJson.object("P",result.property("P"),"Q",result.property("Q")),
                "imports",wire(result.imports()),"duplicateImports",wire(result.importsIncludingDuplicates()));
            diagnostics=result.duplicateImports();
        } else {
            require(failure instanceof IOException||failure instanceof ProfileRejected,"recoverable failure type");
            try { member(outcome,"resultOrThrow");throw new AssertionError("failure swallowed"); }
            catch(Exception same) { require(same==failure,"original failure identity changed"); }
            if(failure instanceof EvaluationFailure f) {
                evaluation=ItemsJson.object("success",false,"reason",f.reason.name(),"code",f.referenceCode,"file",f.project.toString(),
                    "target",f.importedProject==null?null:f.importedProject.toString(),"current",wire(f.current));
                diagnostics=f.diagnostics;
            } else { evaluation=ItemsJson.object("success",false,"type",failure.getClass().getName(),"code",failure instanceof ProfileRejected p?p.code:null);diagnostics=List.of(); }
        }
        return ItemsJson.object("evaluation",evaluation,"diagnostics",wire(diagnostics),"traces",wire(traces(outcome)));
    }
    static void selected(Path fixtures) throws Exception {
        List<Object> rows=new ArrayList<>();
        try(var dirs=Files.list(fixtures)) {
            for(Path dir:dirs.filter(Files::isDirectory).sorted().toList())for(ImportProfile p:ImportProfile.values()) {
                Object outcome=evaluateTrace(dir.resolve("main.proj"),dir,Map.of(),p);
                rows.add(ItemsJson.object("id",dir.getFileName().toString(),"profile",p.name(),"observation",observation(outcome)));
            }
        }
        require(rows.size()==57,"selected corpus cardinality");
        System.out.println(ItemsJson.write(ItemsJson.object("status","PASS","rows",rows)));
    }
    static Path write(Path root,String name,String xml) throws Exception {
        Path p=root.resolve(name);Files.createDirectories(p.getParent());Files.writeString(p,xml);return p;
    }
    static Path graph(Path parent,String id,String xml) throws Exception {
        Path root=parent.resolve(id);Files.createDirectories(root);write(root,"main.proj",xml);return root;
    }
    static Object eval(Path root,ImportProfile profile) throws Exception { return evaluateTrace(root.resolve("main.proj"),root,Map.of(),profile); }
    static void failure(Object value,String code,int count) throws Exception {
        Throwable f=(Throwable)member(value,"failure");require(member(value,"result")==null,"failed result present");
        String actual=f instanceof ProfileRejected p?p.code:f instanceof EvaluationFailure e?e.referenceCode:f.getClass().getSimpleName();
        require(Objects.equals(actual,code),"failure expected "+code+" got "+actual);require(traces(value).size()==count,"failure witness count");
    }
    static void immutable(List<?> list) {
        try { list.clear();throw new AssertionError("mutable published list"); }
        catch(UnsupportedOperationException expected) { }
    }
    static Path chain(Path parent,String name,int count,boolean close) throws Exception {
        Path root=parent.resolve(name);Files.createDirectories(root);
        for(int i=0;i<count;i++)write(root,i==0?"main.proj":"n"+i+".props","<Project>"+
            (i<count-1?"<Import Project=\"n"+(i+1)+".props\"/>":close?"<Import Project=\"main.proj\"/>":"")+"</Project>");
        return root;
    }
    static void interleaved(Path rootA,Path rootB,ImportProfile profileA,ImportProfile profileB) throws Exception {
        CountDownLatch entered=new CountDownLatch(1),release=new CountDownLatch(1);
        Map<String,String> paused=new AbstractMap<>() {
            public Set<Entry<String,String>> entrySet() {
                entered.countDown();try { require(release.await(5,TimeUnit.SECONDS),"interleave release timeout"); }
                catch(InterruptedException e) { Thread.currentThread().interrupt();throw new AssertionError(e); }
                return Map.of("Flag","true").entrySet();
            }
        };
        ExecutorService pool=Executors.newFixedThreadPool(2);
        try {
            Future<Object> a=pool.submit(()->evaluateTrace(rootA.resolve("main.proj"),rootA,paused,profileA));
            require(entered.await(5,TimeUnit.SECONDS),"interleave entry timeout");
            Future<Object> b=pool.submit(()->evaluateTrace(rootB.resolve("main.proj"),rootB,Map.of("Flag","true"),profileB));
            Object before=b.get(5,TimeUnit.SECONDS);Object snapshot=wire(traces(before));release.countDown();
            Object after=a.get(5,TimeUnit.SECONDS);
            require(ItemsJson.write(snapshot).equals(ItemsJson.write(wire(traces(before)))),"other thread changed published snapshot");
            require(traces(before).size()==1&&traces(after).size()==1,"thread trace counts");
            require(((List<?>)member(traces(before).getFirst(),"nodes")).getFirst().equals(rootB.resolve("main.proj").toRealPath()),"B root contamination");
            require(((List<?>)member(traces(after).getFirst(),"nodes")).getFirst().equals(rootA.resolve("main.proj").toRealPath()),"A root contamination");
            require((member(after,"failure")!=null)==(profileA==ImportProfile.REJECT_CIRCULAR),"A profile contamination");
        } finally { release.countDown();pool.shutdownNow();require(pool.awaitTermination(5,TimeUnit.SECONDS),"thread cleanup"); }
    }
    static void controls(Path parent,Path fixtures,String platform) throws Exception {
        Files.createDirectories(parent);List<String> groups=new ArrayList<>();
        Object acyclic=eval(chain(parent,"chain16",16,false),ImportProfile.DEFAULT);
        require(member(acyclic,"result")!=null&&traces(acyclic).isEmpty(),"acyclic limit");groups.add("CC01-no-cycle-16");
        failure(eval(chain(parent,"chain17",17,false),ImportProfile.DEFAULT),"INPUT_BOUND",0);groups.add("CC02-file17");
        for(int size:new int[]{65536,65537}) {
            String base="<Project><!--"+"x".repeat(size-26)+"--></Project>";require(base.length()==size,"size fixture");
            Object out=eval(graph(parent,"size"+size,base),ImportProfile.DEFAULT);
            if(size==65536)require(member(out,"result")!=null,"65536 refused");else failure(out,"INPUT_BOUND",0);
        }groups.add("CC03-size");
        Path root=graph(parent,"immutable","<Project><Import Project=\"main.proj\"/></Project>");
        Object outcome=eval(root,ImportProfile.DEFAULT);Object trace=traces(outcome).getFirst();
        immutable(traces(outcome));immutable((List<?>)member(trace,"nodes"));immutable((List<?>)member(trace,"edges"));immutable((List<?>)member(trace,"diagnosticIndices"));
        var ctor=trace.getClass().getDeclaredConstructors()[0];ctor.setAccessible(true);
        List<Object> nodes=new ArrayList<>((List<?>)member(trace,"nodes")),edges=new ArrayList<>((List<?>)member(trace,"edges")),links=new ArrayList<>((List<?>)member(trace,"diagnosticIndices"));
        Object copy=ctor.newInstance(nodes,edges,0,ImportProfile.DEFAULT,links);nodes.clear();edges.clear();links.clear();
        require(((List<?>)member(copy,"nodes")).size()==2&&((List<?>)member(copy,"edges")).size()==1&&((List<?>)member(copy,"diagnosticIndices")).size()==1,"constructor defensive copy");
        Object snapshot=wire(trace);eval(chain(parent,"other",3,true),ImportProfile.DEFAULT);require(snapshot.equals(wire(trace)),"snapshot changed");groups.add("CC04-immutable");
        Path nonroot=graph(parent,"nonroot","<Project><Import Project=\"a.props\" Condition=\"'$(Flag)' != 'false'\"/></Project>");
        write(nonroot,"a.props","<Project><Import Project=\"a.props\" Condition=\"'$(Flag)' != 'false'\"/></Project>");
        failure(eval(nonroot,ImportProfile.REJECT_CIRCULAR),null,1);
        require(traces(eval(chain(parent,"recovered",2,false),ImportProfile.DEFAULT)).isEmpty(),"recovery contamination");
        for(String tail:List.of("missing.props","bad.props","item.props","xml.props")) {
            Path later=graph(parent,"later-"+tail,"<Project><Import Project=\"main.proj\"/><Import Project=\""+tail+"\"/></Project>");
            if(tail.equals("bad.props"))write(later,tail,"<Project><Unknown/></Project>");
            if(tail.equals("item.props"))write(later,tail,"<Project><ItemGroup><Compile Include=\"a.cs\" Condition=\"'notbool'\"/></ItemGroup></Project>");
            if(tail.equals("xml.props"))write(later,tail,"<Project>");
            Object result=eval(later,ImportProfile.DEFAULT);require(member(result,"failure")!=null&&traces(result).size()==1,"later failure lost trace "+tail);
        }
        interleaved(nonroot,root,ImportProfile.REJECT_CIRCULAR,ImportProfile.DEFAULT);groups.add("CC05-recovery");
        // Original compiled consumer and javap equality are separate driver obligations.
        groups.add("CC06-abi");
        Path boundary=graph(parent,"boundary","<Project><Import Project=\"../outside.props\"/></Project>");
        write(parent,"outside.props","<Project/>");failure(eval(boundary,ImportProfile.DEFAULT),"IMPORT_BOUNDARY",0);
        for(String kind:List.of("inside","outside")) {
            Path dir=parent.resolve("links/"+kind);
            require(Files.exists(dir.resolve("alias")),"driver must provide controlled link");
            write(dir,"main.proj","<Project><Import Project=\"alias/one.props\"/></Project>");
            if(kind.equals("outside"))failure(eval(dir,ImportProfile.DEFAULT),"IMPORT_BOUNDARY",0);
            else require(member(eval(dir,ImportProfile.DEFAULT),"result")!=null,"inside import alias refused");
        }groups.add("CC07-boundaries");
        failure(evaluateTrace(root.resolve("main.proj"),root,Map.of(),null),"IMPORT_PROFILE",0);
        Path empty=graph(parent,"empty","<Project><Import Project=\"$(Missing)\"/></Project>");failure(eval(empty,ImportProfile.DEFAULT),"MSB4020",0);
        for(String expr:List.of("a;b","*.props","/absolute","a\\b","$(Missing)$")) {
            Path invalid=graph(parent,"invalid"+groups.size()+"-"+Integer.toHexString(expr.hashCode()),"<Project><Import Project=\""+expr+"\"/></Project>");
            failure(eval(invalid,ImportProfile.DEFAULT),"IMPORT_PATH_PROFILE",0);
        }
        Path skipped=graph(parent,"skipped","<Project><Import Project=\"main.proj\" Condition=\"false\"/></Project>");require(traces(eval(skipped,ImportProfile.DEFAULT)).isEmpty(),"false closure traced");
        AtomicInteger calls=new AtomicInteger();ProfileRejected sentinel=new ProfileRejected("sentinel","original");
        Map<String,String> once=new AbstractMap<>() { public Set<Entry<String,String>> entrySet(){calls.incrementAndGet();throw sentinel;} };
        Object captured=evaluateTrace(root.resolve("main.proj"),root,once,ImportProfile.DEFAULT);require(member(captured,"failure")==sentinel&&calls.get()==1,"single execution capture");
        try { evaluate(root.resolve("main.proj"),root,once);throw new AssertionError("legacy swallowed"); }catch(ProfileRejected e){require(e==sentinel&&calls.get()==2,"legacy identity/single execution");}
        try { evaluateTrace(null,root,Map.of(),ImportProfile.DEFAULT);throw new AssertionError("unchecked swallowed"); }catch(NullPointerException expected) { }
        Object missingSandbox=evaluateTrace(root.resolve("main.proj"),parent.resolve("absent-sandbox"),Map.of(),ImportProfile.DEFAULT);
        require(member(missingSandbox,"failure") instanceof IOException&&traces(missingSandbox).isEmpty(),"pre-state IOException");
        OutOfMemoryError fatalSentinel=new OutOfMemoryError("deliberately thrown test sentinel");
        Map<String,String> fatal=new AbstractMap<>() {public Set<Entry<String,String>> entrySet(){throw fatalSentinel;}};
        try { evaluateTrace(root.resolve("main.proj"),root,fatal,ImportProfile.DEFAULT);throw new Exception("fatal swallowed"); }catch(OutOfMemoryError e){require(e==fatalSentinel,"fatal identity changed");}
        groups.add("CC08-invalid-profile-and-path");
        try(var dirs=Files.list(fixtures)) {
            for(Path dir:dirs.filter(Files::isDirectory).sorted().toList()) {
                Path variant=parent.resolve("markers/"+dir.getFileName());
                try(var files=Files.walk(dir)) {for(Path f:files.filter(Files::isRegularFile).toList()) {Path dest=variant.resolve(dir.relativize(f));Files.createDirectories(dest.getParent());Files.copy(f,dest);}}
                Path main=variant.resolve("main.proj");String xml=Files.readString(main);String marker="<Target Name=\"TraceMarker\"><WriteLinesToFile File=\"must-not-exist.txt\" Lines=\"executed\" Overwrite=\"true\"/></Target>";
                Files.writeString(main,xml.replace("</Project>",marker+"</Project>"));
                for(ImportProfile p:ImportProfile.values())eval(variant,p);
                try(var files=Files.walk(variant)){require(files.noneMatch(f->f.getFileName().toString().equals("must-not-exist.txt")),"target executed");}
            }
        }groups.add("CC09-inert-target");
        Path twice=graph(parent,"twice","<Project>\n <Import Project=\"main.proj\"/>\n <Import Project=\"main.proj\"/>\n</Project>");
        Object repeated=eval(twice,ImportProfile.DEFAULT);require(traces(repeated).size()==2,"repeated closures collapsed");
        require(member(traces(repeated).get(0),"diagnosticIndices").equals(List.of(0))&&member(traces(repeated).get(1),"diagnosticIndices").equals(List.of(1)),"diagnostic occurrence order");
        require(member(traces(eval(nonroot,ImportProfile.REJECT_CIRCULAR)).getFirst(),"diagnosticIndices").equals(List.of(0,1)),"reject pair linkage");groups.add("CC10-order-and-owner");
        interleaved(nonroot,root,ImportProfile.RECORD_DUPLICATES,ImportProfile.REJECT_CIRCULAR);
        for(ImportProfile p:ImportProfile.values())require(traces(eval(nonroot,p)).size()==1,"cache/profile lost cycle");groups.add("CC11-cache-isolation");
        Path caseRoot=graph(parent,"case","<Project><Import Project=\"MAIN.PROJ\"/></Project>");Object caseValue=eval(caseRoot,ImportProfile.DEFAULT);
        if(platform.equals("windows"))require(traces(caseValue).size()==1,"Windows case observation changed");else failure(caseValue,"MSB4019",0);
        groups.add("CC14-case-and-alias-profile");
        System.out.println(ItemsJson.write(ItemsJson.object("status","PASS","groups",groups,"proofControls","CC12/CC13 executed by Python reader controls")));
    }
    public static void main(String[] args) throws Exception {
        Path expected=Path.of(args[args.length-2]).toRealPath();
        Path actual=Path.of(ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath();
        require(actual.equals(expected),"product origin differs");
        byte[] digest=java.security.MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(actual));
        require(HexFormat.of().formatHex(digest).equals(args[args.length-1]),"product hash differs");
        System.err.println("PRODUCT_ORIGIN\t"+actual+"\t"+HexFormat.of().formatHex(digest));
        try { traced=ProjectEvaluationComponent.class.getDeclaredMethod("evaluateWithTraces",Path.class,Path.class,Map.class,ImportProfile.class); }
        catch(NoSuchMethodException absent) { throw new AssertionError("FEATURE_RED: required trace-aware sidecar absent",absent); }
        traced.setAccessible(true);
        if(args[0].equals("selected"))selected(Path.of(args[1]));
        else controls(Path.of(args[1]),Path.of(args[2]),args[3]);
    }
}
