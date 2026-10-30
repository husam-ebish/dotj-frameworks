package org.dotj.internal.build.evaluation;

import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Native expectations detect parse-time expansion, wrong owner, mutable globals and empty-target fiction. */
final class ImportPathWhitespaceTest {
    static void require(boolean ok,String why) { if(!ok)throw new AssertionError(why); }
    static Object value(Object o,String name) throws Exception { return ImportProfileTest.value(o,name); }
    static String decode(String s) {return new String(Base64.getDecoder().decode(s),StandardCharsets.UTF_8);}
    static Path target(Path directory,String name) {return name.equals("-")?null:directory.resolve(name);}
    static Map<String,String> globals(String id) {
        String value=switch(id) {
            case "BW01-ascii-whitespace-only" -> " \t\r\n";
            case "BW02-ascii-padded-path" -> " \t\r\none.props \t\r\n";
            case "BW03-nbsp-whitespace-only" -> "\u00a0";
            case "BW04-nbsp-padded-path" -> "\u00a0one.props\u00a0";
            default -> throw new AssertionError("Unknown whitespace case");
        };
        return new LinkedHashMap<>(Map.of("ImportName",value));
    }
    public static void main(String[] args) throws Exception {
        Path fixtures=Path.of(args[1]);List<String> rows=new ArrayList<>();Set<Integer> nativeWhitespace=new TreeSet<>();
        Result result=null;EvaluationFailure failure=null;Path directory=null;String id=null;
        List<?> diagnostics=List.of(),edges=List.of();int notices=0,firsts=0,cases=0,globalRows=0;Map<String,String> caller=Map.of();
        for(String line:Files.readAllLines(Path.of(args[0]),StandardCharsets.UTF_8)) {
            String[] f=line.split("\t",-1);
            switch(f[0]) {
                case "WHITESPACE" -> {for(String cp:f[1].split(","))nativeWhitespace.add(Integer.parseInt(cp));}
                case "CASE" -> {
                    id=f[2];directory=fixtures.resolve(id);result=null;failure=null;notices=firsts=globalRows=0;caller=globals(id);Map<String,String> before=Map.copyOf(caller);
                    require(f[1].equals("Default"),"Only new Default semantics qualified");
                    try {result=evaluate(directory.resolve("main.proj"),directory,caller);require(f[3].equals("true"),id+" expected native failure");}
                    catch(EvaluationFailure error) {failure=error;require(f[3].equals("false"),id+" unexpected failure");}
                    require(caller.equals(before),id+" caller globals changed");
                    if(result!=null) {
                        require(result.property("P").equals(decode(f[4]))&&result.property("Q").equals(decode(f[5])),id+" untrimmed properties mismatch");
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
                case "END" -> {require(notices==diagnostics.size()&&firsts==edges.size()&&globalRows==caller.size(),id+" incomplete native rows");rows.add(id+"\tNATIVE_IMPORT_PATH_WHITESPACE_MATCH\t"+(result!=null?"SUCCESS":value(failure,"reason")));}
                default -> throw new AssertionError("Unknown bridge row");
            }
        }
        require(cases==4&&!nativeWhitespace.isEmpty(),"Expected four native whitespace cases and actual classifier observations");
        whitespaceControls(fixtures,Path.of(args[3]),nativeWhitespace);
        ImportPathExpansionTest.restrictions(Path.of(args[3]).resolve("original-restrictions"));
        Files.write(Path.of(args[2]),rows,StandardCharsets.UTF_8);
        System.out.println("PASS four native whitespace cases, native-classifier functional controls and preserved refusals; zero accepted tasks");
    }
    static void whitespaceControls(Path fixtures,Path out,Set<Integer> nativeWhitespace) throws Exception {
        Path success=fixtures.resolve("BW02-ascii-padded-path");
        for(int cp:nativeWhitespace) {
            String padding=String.valueOf((char)cp),original=padding+"one.props"+padding;
            Map<String,String> caller=new LinkedHashMap<>(Map.of("ImportName",original));
            Result result=evaluate(success.resolve("main.proj"),success,caller);
            require(result.imports().size()==1&&result.imports().getFirst().target().equals(success.resolve("one.props")),"Native whitespace U+"+Integer.toHexString(cp)+" did not select one target");
            require(result.property("Q").equals(original)&&result.property("ImportName").equals(original)&&caller.get("ImportName").equals(original),"Path trimming changed property/global value");
        }
        require(nativeWhitespace.contains(0xa0)&&!nativeWhitespace.contains(0x1c),"Native NBSP versus JDK whitespace distinction missing");
        for(int cp:List.of(0x1c,0x200b,0xfeff)) {
            require(!nativeWhitespace.contains(cp),"Negative control became native whitespace");
            String padding=String.valueOf((char)cp);
            try {evaluate(success.resolve("main.proj"),success,Map.of("ImportName",padding+"one.props"+padding));throw new AssertionError("Unqualified character silently trimmed: "+cp);}
            catch(java.io.IOException|IllegalArgumentException expected) { /* No exception ABI/code qualification for these negative controls. */ }
        }
        Files.createDirectories(out);Path file=out.resolve("main.proj");
        Files.writeString(file,"<Project><ImportGroup Condition=\"false\"><Import Project=\"$(ImportName)\"/></ImportGroup><Import Project=\"$(ImportName)\" Condition=\"false\"/></Project>",StandardCharsets.UTF_8);
        for(String v:List.of(" \t\r\n","\u00a0","\u00a0one.props\u00a0"))require(evaluate(file,out,Map.of("ImportName",v)).imports().isEmpty(),"False condition/group touched whitespace-expanded path");
        Files.writeString(file,"<Project><Import Project=\"$(ImportName)\"/></Project>",StandardCharsets.UTF_8);
        for(String v:List.of(" *.props ","\u00a0%3B.props\u00a0"," /outside.props "," ../outside.props "," $(P) ")) {
            try {evaluate(file,out,Map.of("ImportName",v));throw new AssertionError("Padded unqualified path accepted: "+v);}catch(ProfileRejected expected) {}
        }
    }
}
