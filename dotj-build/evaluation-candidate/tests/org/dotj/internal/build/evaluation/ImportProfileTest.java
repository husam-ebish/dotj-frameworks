package org.dotj.internal.build.evaluation;

import java.io.IOException;
import java.lang.reflect.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Same-profile native assertions catch wrong branch order, null coercion and duplicate replay. */
final class ImportProfileTest {
    static void require(boolean ok,String why) { if(!ok)throw new AssertionError(why); }
    static Object value(Object o,String name) throws Exception {
        try { return o.getClass().getDeclaredMethod(name).invoke(o); }
        catch(NoSuchMethodException absent) { return o.getClass().getDeclaredField(name).get(o); }
    }
    static Class<?> selector() {
        return Arrays.stream(ProjectEvaluationComponent.class.getDeclaredClasses()).filter(c->c.getSimpleName().equals("ImportProfile")).findFirst()
            .orElseThrow(()->new AssertionError("Missing internal selected import-policy behavior"));
    }
    @SuppressWarnings({"unchecked","rawtypes"})
    static Result call(Path file,Path root,String profile) throws Exception {
        Class<?> type=selector();Object selected=profile==null?null:Enum.valueOf((Class)type,profile.equals("RecordDuplicateButNotCircularImports")?"RECORD_DUPLICATES":profile.equals("RejectCircularImports")?"REJECT_CIRCULAR":"DEFAULT");
        try { return (Result)ProjectEvaluationComponent.class.getDeclaredMethod("evaluate",Path.class,Path.class,Map.class,type).invoke(null,file,root,Map.of(),selected); }
        catch(InvocationTargetException error) { if(error.getCause() instanceof Exception e)throw e;throw error; }
    }
    static String decode(String s) { return new String(Base64.getDecoder().decode(s),StandardCharsets.UTF_8); }
    static void immutable(List<?> list,String name) {try {list.clear();throw new AssertionError("Mutable "+name);}catch(UnsupportedOperationException expected) {}}
    static void position(Object p,String[] f,int offset,String label) throws Exception {
        for(int i=0;i<4;i++)require(value(p,List.of("line","column","endLine","endColumn").get(i)).equals(Integer.valueOf(f[offset+i])),label+" coordinate mismatch");
    }
    public static void main(String[] args) throws Exception {
        Path fixtures=Path.of(args[1]);List<String> rows=new ArrayList<>();
        selector();
        Path absent=fixtures.resolve("never-exists");
        try {call(absent,absent,null);throw new AssertionError("Null import profile accepted");}
        catch(ProfileRejected refused) {require(refused.code.equals("IMPORT_PROFILE"),"Null profile must refuse before filesystem access");}
        Result result=null;EvaluationFailure failure=null;Path directory=null;String id=null,profile=null;
        List<?> diagnostics=List.of(),unique=List.of(),recorded=null;int notices=0,firsts=0,repeats=0,cases=0;
        for(String line:Files.readAllLines(Path.of(args[0]),StandardCharsets.UTF_8)) {
            String[] f=line.split("\t",-1);
            switch(f[0]) {
                case "CASE" -> {
                    profile=f[1];id=f[2];directory=fixtures.resolve(id);result=null;failure=null;notices=firsts=repeats=0;
                    try {result=call(directory.resolve("main.proj"),directory,profile);require(f[3].equals("true"),id+" expected failure");}
                    catch(EvaluationFailure error) {failure=error;require(f[3].equals("false"),id+" unexpected failure");}
                    if(result!=null) {
                        require(result.property("P").equals(decode(f[4]))&&result.property("Q").equals(decode(f[5])),id+" properties/replay mismatch");
                        unique=(List<?>)value(result,"imports");recorded=(List<?>)value(result,"importsIncludingDuplicates");diagnostics=result.duplicateImports();
                        immutable(unique,"unique imports");if(recorded!=null)immutable(recorded,"recorded imports");
                        require(result.equals(call(directory.resolve("main.proj"),directory,profile)),id+" repeat state leaked");
                        require(result.evaluatedFiles().size()==unique.size()+1,"Root must be excluded from unique imports");
                    } else {diagnostics=(List<?>)value(failure,"diagnostics");unique=List.of();recorded=null;}
                    immutable(diagnostics,"diagnostic snapshot");cases++;
                }
                case "AVAIL" -> require((recorded!=null)==Boolean.parseBoolean(f[1]),id+" getter availability mismatch");
                case "UNIQUE", "RECORDED" -> {
                    Object edge=f[0].equals("UNIQUE")?unique.get(firsts++):recorded.get(repeats++);
                    require(value(edge,"owner").equals(directory.resolve(f[1]))&&value(edge,"target").equals(directory.resolve(f[2]))&&value(edge,"line").equals(Integer.valueOf(f[3]))&&value(edge,"column").equals(Integer.valueOf(f[4])),id+" native edge order/site mismatch");
                }
                case "NOTICE" -> {
                    Object d=diagnostics.get(notices++);String code=f[2].equals("NULL")?null:f[2];
                    require(value(d,"kind").toString().equalsIgnoreCase(f[1])&&Objects.equals(value(d,"referenceCode"),code)&&value(d,"owner").equals(directory.resolve(f[3]))&&value(d,"importedProject").equals(directory.resolve(f[4])),id+" native diagnostic order/null/identity mismatch");
                    position(value(d,"current"),f,5,id);require(value(d,"contextKind").toString().equals(f[9]),id+" context kind mismatch");
                    Object previous=value(d,"previous"),root=value(d,"rootContext");
                    if(f[9].equals("ROOT"))require(previous==null&&root.equals(directory.resolve("main.proj")),"Root precedence/context mismatch");
                    else if(f[9].equals("PREVIOUS"))require(root==null&&previous!=null&&value(previous,"owner").equals(directory.resolve(f[10]))&&value(previous,"line").equals(Integer.valueOf(f[11]))&&value(previous,"column").equals(Integer.valueOf(f[12])),"Previous import context mismatch");
                    else require(previous==null&&root==null,"Invented circular/missing ancestor context");
                }
                case "FAILURE" -> {
                    require(result==null&&failure!=null,"Failure exposed successful Result");
                    require(value(failure,"reason").toString().equals(f[1])&&Objects.equals(failure.referenceCode,f[2].equals("NULL")?null:f[2])&&failure.project.equals(directory.resolve(f[3]))&&value(failure,"importedProject").equals(directory.resolve(f[4])),id+" typed failure mismatch");
                    position(value(failure,"current"),f,5,id);require((failure.missingImport==null)==f[1].equals("CIRCULAR_IMPORT"),"Circular target mislabelled missing");
                }
                case "END" -> {require(notices==diagnostics.size()&&firsts==unique.size()&&(recorded==null||repeats==recorded.size()),id+" incomplete native observations");rows.add(id+"\t"+profile+"\tNATIVE_PROFILE_MATCH");}
                default -> throw new AssertionError("Malformed profile bridge");
            }
        }
        require(cases==18,"Incomplete selected profile corpus");
        Path repeat=fixtures.resolve("BI01-repeat"),cycle=fixtures.resolve("BI08-nonroot-cycle");
        Result baseline=evaluate(repeat.resolve("main.proj"),repeat,Map.of()),before=call(repeat.resolve("main.proj"),repeat,"RecordDuplicateButNotCircularImports");
        List<?> failedSnapshot=null;
        for(int i=0;i<2;i++) {
            try {call(cycle.resolve("main.proj"),cycle,"RejectCircularImports");throw new AssertionError("Circular reject returned Result");}
            catch(EvaluationFailure expected) {failedSnapshot=(List<?>)value(expected,"diagnostics");require(failedSnapshot.size()==2,"Reject must preserve warning then error");}
            require(before.equals(call(repeat.resolve("main.proj"),repeat,"RecordDuplicateButNotCircularImports"))&&baseline.equals(evaluate(repeat.resolve("main.proj"),repeat,Map.of())),"Success/failure state leaked across calls");
        }
        require(failedSnapshot!=null&&failedSnapshot.size()==2&&((List<?>)value(before,"imports")).size()==1&&((List<?>)value(before,"importsIncludingDuplicates")).size()==2,"Historical snapshots changed after other calls");
        try(var files=Files.walk(fixtures)) {require(files.noneMatch(p->p.getFileName().toString().equals("must-not-exist.txt")),"Task marker executed");}
        Files.write(Path.of(args[2]),rows,StandardCharsets.UTF_8);
        System.out.println("PASS 18 same-profile comparisons; null/refusal/immutable/state controls; no public ABI qualification");
    }
}
