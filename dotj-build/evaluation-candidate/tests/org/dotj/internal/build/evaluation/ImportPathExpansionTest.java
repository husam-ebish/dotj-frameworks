package org.dotj.internal.build.evaluation;

import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Native expectations detect parse-time expansion, wrong owner, mutable globals and empty-target fiction. */
final class ImportPathExpansionTest {
    static void require(boolean ok,String why) { if(!ok)throw new AssertionError(why); }
    static Object value(Object o,String name) throws Exception { return ImportProfileTest.value(o,name); }
    static String decode(String s) {return new String(Base64.getDecoder().decode(s),StandardCharsets.UTF_8);}
    static Path target(Path directory,String name) {return name.equals("-")?null:directory.resolve(name);}
    static Map<String,String> globals(String id) {return id.equals("immutable-global-import-name")?new LinkedHashMap<>(Map.of("ImportName","one.props")):new LinkedHashMap<>();}
    public static void main(String[] args) throws Exception {
        Path fixtures=Path.of(args[1]);List<String> rows=new ArrayList<>();
        Result result=null;EvaluationFailure failure=null;Path directory=null;String id=null;
        List<?> diagnostics=List.of(),edges=List.of();int notices=0,firsts=0,cases=0,globalRows=0;Map<String,String> caller=Map.of();
        for(String line:Files.readAllLines(Path.of(args[0]),StandardCharsets.UTF_8)) {
            String[] f=line.split("\t",-1);
            switch(f[0]) {
                case "CASE" -> {
                    id=f[2];directory=fixtures.resolve(id);result=null;failure=null;notices=firsts=globalRows=0;caller=globals(id);Map<String,String> before=Map.copyOf(caller);
                    require(f[1].equals("Default"),"Only new Default semantics qualified");
                    try {result=evaluate(directory.resolve("main.proj"),directory,caller);require(f[3].equals("true"),id+" expected native failure");}
                    catch(EvaluationFailure error) {failure=error;require(f[3].equals("false"),id+" unexpected failure");}
                    require(caller.equals(before),id+" caller globals changed");
                    if(result!=null) {
                        require(result.property("P").equals(decode(f[4]))&&result.property("Q").equals(decode(f[5])),id+" properties mismatch");
                        diagnostics=result.duplicateImports();edges=result.imports();
                        require(result.importsIncludingDuplicates()==null,"Default duplicate getter unexpectedly available");
                        require(result.equals(evaluate(directory.resolve("main.proj"),directory,caller)),id+" repeated call leaked state");
                        require(result.evaluatedFiles().size()==edges.size()+1,"Unique imports/root mismatch");
                        ImportProfileTest.immutable(edges,"path edges");ImportProfileTest.immutable(result.evaluatedFiles(),"path files");
                        try {result.escapedProperties().put("P","forged");throw new AssertionError("Mutable properties");}catch(UnsupportedOperationException expected) {}
                    } else {diagnostics=failure.diagnostics;edges=List.of();}
                    ImportProfileTest.immutable(diagnostics,"path diagnostic snapshot");cases++;
                }
                case "GLOBAL" -> {require(Objects.equals(caller.get(decode(f[1])),decode(f[2])),"Manifest global transport mismatch");globalRows++;}
                case "AVAIL" -> require(f[1].equals("false")&&result!=null&&result.importsIncludingDuplicates()==null,"Getter availability mismatch");
                case "UNIQUE" -> {
                    Object edge=edges.get(firsts++);
                    require(value(edge,"owner").equals(directory.resolve(f[1]))&&value(edge,"target").equals(directory.resolve(f[2]))&&value(edge,"line").equals(Integer.valueOf(f[3]))&&value(edge,"column").equals(Integer.valueOf(f[4])),id+" native owner/target/order/site mismatch");
                }
                case "NOTICE" -> {
                    Object d=diagnostics.get(notices++);
                    require(value(d,"kind").toString().equalsIgnoreCase(f[1])&&Objects.equals(value(d,"referenceCode"),f[2].equals("NULL")?null:f[2])&&value(d,"owner").equals(directory.resolve(f[3]))&&Objects.equals(value(d,"importedProject"),target(directory,f[4])),id+" native diagnostic mismatch");
                    ImportProfileTest.position(value(d,"current"),f,5,id);
                    require(value(d,"contextKind").toString().equals(f[9]),id+" diagnostic context mismatch");
                    Object previous=value(d,"previous");require(value(d,"rootContext")==null,"Invented root context");
                    if(f[9].equals("PREVIOUS"))require(previous!=null&&value(previous,"owner").equals(directory.resolve(f[10]))&&value(previous,"line").equals(Integer.valueOf(f[11]))&&value(previous,"column").equals(Integer.valueOf(f[12])),"Previous edge mismatch");
                    else require(previous==null,"Invented previous context");
                }
                case "FAILURE" -> {
                    require(result==null&&failure!=null,"Failed evaluation exposed Result");
                    require(value(failure,"reason").toString().equals(f[1])&&Objects.equals(failure.referenceCode,f[2].equals("NULL")?null:f[2])&&failure.project.equals(directory.resolve(f[3]))&&Objects.equals(failure.importedProject,target(directory,f[4])),id+" failure identity mismatch");
                    ImportProfileTest.position(value(failure,"current"),f,5,id);
                    require(Objects.equals(failure.missingImport,f[1].equals("MISSING_IMPORT")?target(directory,f[4]):null),"Empty expression mislabelled as missing file");
                }
                case "END" -> {require(notices==diagnostics.size()&&firsts==edges.size()&&globalRows==caller.size(),id+" incomplete native rows");rows.add(id+"\tNATIVE_IMPORT_PATH_MATCH\t"+(result!=null?"SUCCESS":value(failure,"reason")));}
                default -> throw new AssertionError("Unknown bridge row");
            }
        }
        require(cases==8,"Expected eight focused cases including one legacy transition");
        Path success=fixtures.resolve("immutable-global-import-name"),invalid=fixtures.resolve("undefined-expands-empty");
        Map<String,String> snapshotCaller=globals("immutable-global-import-name");Result snapshot=evaluate(success.resolve("main.proj"),success,snapshotCaller);
        for(int i=0;i<2;i++) {
            try {evaluate(invalid.resolve("main.proj"),invalid,Map.of());throw new AssertionError("Empty expression succeeded");}catch(EvaluationFailure expected) {require(expected.missingImport==null,"Empty missing target invented");}
            require(snapshot.equals(evaluate(success.resolve("main.proj"),success,snapshotCaller)),"Success/failure/success state leak");
        }
        snapshotCaller.put("ImportName","wrong.props");require(snapshot.property("Q").equals("one.props"),"Snapshot depends on mutable caller");
        restrictions(Path.of(args[3]));
        Files.write(Path.of(args[2]),rows,StandardCharsets.UTF_8);
        System.out.println("PASS eight native Default path cases plus static/value restrictions and isolation controls; zero accepted tasks");
    }
    static void restrictions(Path root) throws Exception {
        Files.createDirectories(root);
        for(String raw:List.of("$(P","$(P.ToUpper())","$([System.IO.File]::ReadAllText('x'))","$(MSBuildThisFileDirectory)","@(I)","%(M)","one;two.props","*.props","a?.props","%3B.props","$junk","$(P$(Q))","/absolute.props","C:/x.props","https://example.invalid/x","a\\b.props")) {
            refuse(root,"<Project><ImportGroup Condition=\"false\"><Import Project=\""+raw+"\"/></ImportGroup></Project>",Map.of());
        }
        for(String injected:List.of("*.props","a?.props","a;b.props","%3B.props","$(P)","/absolute.props","C:/x.props","https://example.invalid/x","a\\b.props","../outside.props")) {
            refuse(root,"<Project><Import Project=\"$(Path)\"/></Project>",Map.of("Path",injected));
            Result skipped=evaluate(write(root,"<Project><Import Project=\"$(Path)\" Condition=\"false\"/></Project>"),root,Map.of("Path",injected));
            require(skipped.imports().isEmpty(),"False evaluated value touched target");
        }
        refuse(root,"<Project><ImportGroup Condition=\"false\"><Import Project=\"$(Path)\" Condition=\"true Or ()\"/></ImportGroup></Project>",Map.of());
        try(var files=Files.walk(root)){require(files.filter(Files::isRegularFile).count()==1,"Unqualified paths created files");}
    }
    static Path write(Path root,String xml) throws Exception {Path file=root.resolve("main.proj");Files.writeString(file,xml);return file;}
    static void refuse(Path root,String xml,Map<String,String> globals) throws Exception {
        try {evaluate(write(root,xml),root,globals);throw new AssertionError("Unqualified path accepted: "+xml+globals);}catch(ProfileRejected expected) {}
    }
}
