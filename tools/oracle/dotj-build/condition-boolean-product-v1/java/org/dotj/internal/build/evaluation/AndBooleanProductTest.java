package org.dotj.internal.build.evaluation;

import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Owned packaged checks; native values come only from the independently pinned bridge. */
final class AndBooleanProductTest {
    static void require(boolean ok,String why) { if(!ok)throw new AssertionError(why); }
    static String decode(String value) { return new String(Base64.getDecoder().decode(value),StandardCharsets.UTF_8); }
    record Edge(String owner,String target,int line,int column) { }
    static Path write(Path root,String expression,String body) throws Exception {
        Path p=root.resolve("main.proj");Files.writeString(p,"<Project><PropertyGroup Condition=\""+expression+"\">"+body+"</PropertyGroup></Project>");return p;
    }
    static void refused(Path root,String id,String expression,String code,List<String> rows) throws Exception {
        try { evaluate(write(root,expression,"<P>bad</P>"),root,Map.of());throw new AssertionError(id+" unexpectedly accepted"); }
        catch(ProfileRejected e) { require(e.code.equals(code),id+" wrong refusal "+e.code);rows.add(id+"\tPRIVATE_CONTROL\t"+e.code); }
    }
    static void controls(Path root,List<String> rows) throws Exception {
        Files.createDirectories(root);
        int n=0;
        for(String expression:List.of("false And (true","true And","()","true And ()","true)","true And true trailing","trueAnd true","true Andfalse","true Orfalse"))
            refused(root,"AC-SYNTAX-"+(++n),expression,"CONDITION_PROFILE",rows);
        require(evaluate(write(root,"true And !false","<P>bad</P>"),root,Map.of()).property("P").equals("bad"),"AC-SYNTAX-10");
        rows.add("AC-SYNTAX-"+(++n)+"\tNATIVE_TYPED_SUCCESSOR\tbad");
        for(String operand:List.of("1","1.0","true","on")) {
            require(evaluate(write(root,"false And ('"+operand+"' == '"+operand+"')","<P>bad</P>"),root,Map.of()).property("P").isEmpty(),"coercion successor");
            rows.add("AC-COERCION-"+(++n)+"\tNATIVE_TYPED_SUCCESSOR\tSKIPPED");
        }
        refused(root,"AC-UNICODE","false And ('ä' == 'ä')","UNICODE_COMPARISON",rows);
        refused(root,"AC-FUNCTION","false And Exists('$([System.IO.File]::ReadAllText(x))')","PROPERTY_FUNCTION",rows);
        Path p=root.resolve("main.proj");
        for(String inner:List.of("false And (true","true And ()","true Or ()")) {
            Files.writeString(p,"<Project><PropertyGroup Condition=\"false\"><P Condition=\""+inner+"\">bad</P></PropertyGroup></Project>");
            try {evaluate(p,root,Map.of());throw new AssertionError("Skipped malformed property accepted");}
            catch(ProfileRejected e){require(e.code.equals("CONDITION_PROFILE"),"Skipped property wrong refusal");}
            Files.writeString(p,"<Project><ImportGroup Condition=\"false\"><Import Project=\"missing.props\" Condition=\""+inner+"\"/></ImportGroup></Project>");
            try {evaluate(p,root,Map.of());throw new AssertionError("Skipped malformed import accepted");}
            catch(ProfileRejected e){require(e.code.equals("CONDITION_PROFILE"),"Skipped import wrong refusal");}
        }
        rows.add("AC-SKIPPED-BRANCHES\tPRIVATE_CONTROL\tCONDITION_PROFILE");
        require(evaluate(write(root,"false And Exists('$(EmptyPath)')","<P>bad</P>"),root,Map.of("EmptyPath","")).property("P").isEmpty(),"False left evaluated empty Exists");
        try {evaluate(write(root,"true And Exists('$(EmptyPath)')","<P>bad</P>"),root,Map.of("EmptyPath",""));throw new AssertionError("Evaluated empty Exists accepted");}
        catch(ProfileRejected e){require(e.code.equals("IMPORT_PATH_PROFILE"),"Empty Exists refusal changed");}
        rows.add("AC-LAZY-EMPTY-PATH\tPRIVATE_CONTROL\tLAZY_FALSE_AND_EVALUATED_REFUSAL");
        require(evaluate(write(root,"'$(Candy)' == 'candy' And true","<P>ok</P>"),root,Map.of("Candy","Candy")).property("P").equals("ok"),"Quoted And substring became grammar");
        for(String value:List.of("alpha' And 'alpha","alpha)","true","1.0")) {
            require(evaluate(write(root,"'$(Value)' == 'alpha' And true","<P>bad</P>"),root,Map.of("Value",value)).property("P").isEmpty(),"expanded scalar injected grammar");
        }
        require(evaluate(write(root,"false And ('$(Value)' == 'alpha')","<P>bad</P>"),root,Map.of("Value","1.0")).property("P").isEmpty(),"Skipped scalar value expanded/coerced");
        rows.add("AC-EXPANSION-IS-SCALAR\tPRIVATE_CONTROL\tNO_GRAMMAR_INJECTION");
        require(evaluate(write(root,"(".repeat(64)+"true"+")".repeat(64),"<P>ok</P>"),root,Map.of()).property("P").equals("ok"),"64 groups rejected");
        refused(root,"AC-DEPTH-65","(".repeat(65)+"true"+")".repeat(65),"CONDITION_BOUND",rows);
        refused(root,"AC-DEPTH-LARGE","(".repeat(10000)+"true"+")".repeat(10000),"CONDITION_BOUND",rows);
        require(evaluate(write(root,String.join(" And ",Collections.nCopies(128,"true")),"<P>ok</P>"),root,Map.of()).property("P").equals("ok"),"255 AST nodes rejected");
        refused(root,"AC-NODES-257",String.join(" And ",Collections.nCopies(129,"true")),"CONDITION_BOUND",rows);
        refused(root,"AC-CHAIN-LARGE",String.join(" And ",Collections.nCopies(3000,"true")),"CONDITION_BOUND",rows);
        rows.add("AC-EXACT-ALLOWED-BOUNDS\tPRIVATE_CONTROL\t64_GROUPS_255_TREE_NODES");
    }
    public static void main(String[] args) throws Exception {
        String mode=args[0];Path bridge=Path.of(args[1]),fixtures=Path.of(args[2]),output=Path.of(args[3]),controlRoot=Path.of(args[4]),jar=Path.of(args[5]);
        require(ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri()),"Evaluator not loaded from actual candidate JAR");
        Module module=ProjectEvaluationComponent.class.getModule();require(module.isNamed()&&module.getDescriptor().exports().isEmpty()&&module.getDescriptor().opens().isEmpty(),"Module API exposure changed");
        require(!java.lang.reflect.Modifier.isPublic(ProjectEvaluationComponent.class.getModifiers()),"Evaluator class exposed");
        System.out.println("PACKAGED_AND_IDENTITY jar="+jar+" module="+module.getName()+" exports=0 opens=0");
        List<String> rows=new ArrayList<>();String id=null,p=null,q=null,kind=null;Map<String,String> globals=new LinkedHashMap<>();List<Edge> edges=new ArrayList<>();int diagnostics=0;
        for(String line:Files.readAllLines(bridge,StandardCharsets.UTF_8)) {
            String[] f=line.split("\t",-1);
            switch(f[0]) {
                case "CASE" -> {id=f[1];kind=f[2];p=decode(f[3]);q=decode(f[4]);diagnostics=Integer.parseInt(f[5]);globals.clear();edges.clear();}
                case "GLOBAL" -> globals.put(decode(f[1]),decode(f[2]));
                case "EDGE" -> edges.add(new Edge(f[1],f[2],Integer.parseInt(f[3]),Integer.parseInt(f[4])));
                case "END" -> {
                    Path directory=fixtures.resolve(id),project=directory.resolve("main.proj");Map<String,String> caller=new LinkedHashMap<>(globals),before=Map.copyOf(caller);
                    if(mode.equals("red")) {
                        require(id.equals("BA01-literal-truth-table"),"RED must select native-supported BA01");
                        try {evaluate(project,directory,caller);throw new AssertionError("Original evaluator unexpectedly accepts native And case");}
                        catch(ProfileRejected e){require(e.code.equals("CONDITION_PROFILE"),"Not behavioral CONDITION_PROFILE RED: "+e.code);System.err.println("PACKAGED_AND_RED CONDITION_PROFILE "+id);throw e;}
                    }
                    if(kind.equals("PRIVATE_MALFORMED")) {
                        try {evaluate(project,directory,caller);throw new AssertionError("Malformed native condition accepted");}
                        catch(ProfileRejected e){require(e.code.equals("CONDITION_PROFILE"),"Malformed condition wrong private refusal");rows.add(id+"\tPRIVATE_NATIVE_MALFORMED_BOUNDARY\tCONDITION_PROFILE");}
                    } else {
                        Result result=evaluate(project,directory,caller);
                        require(result.property("P").equals(p)&&result.property("Q").equals(q),id+" captured P/Q mismatch: "+result.property("P")+" / "+result.property("Q"));
                        require(caller.equals(before),id+" globals mutated");require(result.duplicateImports().size()==diagnostics,id+" notice count mismatch");
                        require(result.importsIncludingDuplicates()==null,id+" Default duplicate representation changed");require(result.imports().size()==edges.size(),id+" ordered import count mismatch");
                        for(int i=0;i<edges.size();i++){Edge wanted=edges.get(i);ImportEdge got=result.imports().get(i);require(got.owner().equals(directory.resolve(wanted.owner()))&&got.target().equals(directory.resolve(wanted.target()))&&got.line()==wanted.line()&&got.column()==wanted.column(),id+" import edge/location mismatch at"+i);}
                        require(result.equals(evaluate(project,directory,caller)),id+" repeated evaluation leaked state");
                        ImportProfileTest.immutable(result.imports(),id+" edges");ImportProfileTest.immutable(result.evaluatedFiles(),id+" files");
                        rows.add(id+"\tNATIVE_AND_MATCH\t"+Base64.getEncoder().encodeToString(p.getBytes(StandardCharsets.UTF_8))+"\t"+Base64.getEncoder().encodeToString(q.getBytes(StandardCharsets.UTF_8))+"\t"+edges.size());
                    }
                    require(!Files.exists(directory.resolve("must-not-exist.txt")),id+" task executed");
                }
                default -> throw new AssertionError("Unknown pinned bridge row");
            }
        }
        require(rows.stream().filter(s->s.contains("\tNATIVE_AND_MATCH\t")).count()==9,"Missing one of9 native success cases");
        require(rows.stream().filter(s->s.contains("\tPRIVATE_NATIVE_MALFORMED_BOUNDARY\t")).count()==1,"Missing BA08 boundary");
        controls(controlRoot,rows);Files.write(output,rows,StandardCharsets.UTF_8);
        System.out.println("PASS_PACKAGED_AND nativeSuccessCases=9 malformedBoundary=1 privateControlRows="+(rows.size()-10));
    }
}
