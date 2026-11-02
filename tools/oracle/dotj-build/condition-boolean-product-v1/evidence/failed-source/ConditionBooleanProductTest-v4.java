package org.dotj.internal.build.evaluation;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.lang.reflect.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Explicit packaged consumer: expectations are bound to frozen observations by the Python adapter. */
final class ConditionBooleanProductTest {
    static void require(boolean ok,String why){if(!ok)throw new AssertionError(why);}
    static String dec(String x){return new String(Base64.getDecoder().decode(x),StandardCharsets.UTF_8);}
    static String enc(String x){return Base64.getEncoder().encodeToString(x.getBytes(StandardCharsets.UTF_8));}
    static String relative(Path root,Path path){require(path.startsWith(root),"outside fixture");return root.relativize(path).toString().replace('\\','/');}
    static String observations(Result result,Path root){
        StringJoiner imports=new StringJoiner("|"),warnings=new StringJoiner("|");
        for(ImportEdge e:result.imports())imports.add(relative(root,e.owner())+">"+relative(root,e.target())+"@"+e.line()+":"+e.column());
        for(ConditionWarning e:result.conditionWarnings())warnings.add(e.referenceCode()+":"+relative(root,e.file())+"@"+e.line()+":"+e.column()+":"+e.condition());
        require(result.duplicateImports().isEmpty()&&result.importsIncludingDuplicates()==null,"Default duplicate mapping");
        return enc(result.property("P"))+"\t"+enc(result.property("Q"))+"\t"+enc(imports.toString())+"\t"+enc(warnings.toString());
    }
    static void immutable(Result r){
        for(List<?> x:List.of(r.imports(),r.evaluatedFiles(),r.duplicateImports(),r.conditionWarnings()))try{x.clear();throw new AssertionError("mutable result");}catch(UnsupportedOperationException expected){}
        try{r.escapedProperties().clear();throw new AssertionError("mutable properties");}catch(UnsupportedOperationException expected){}
    }
    static List<String> consume(Path bridge,Path fixtures,int count) throws Exception {
        List<String> rows=new ArrayList<>();Set<String> ids=new HashSet<>();String[] expected=null;Map<String,String> globals=new LinkedHashMap<>();
        Result first=null;Map<String,String> firstProperties=null;
        for(String line:Files.readAllLines(bridge)){
            String[] f=line.split("\t",-1);
            switch(f[0]){
                case "CASE" -> {require(expected==null&&f.length>=4,"CASE schema");expected=Arrays.copyOfRange(f,1,f.length);require(ids.add(expected[0]),"duplicate ID");globals.clear();}
                case "GLOBAL" -> {require(expected!=null&&f.length==3,"GLOBAL schema");require(globals.put(dec(f[1]),dec(f[2]))==null,"duplicate global");}
                case "END" -> {
                    require(expected!=null&&f.length==1,"END schema");String id=expected[0],kind=expected[1];Path root=fixtures.resolve(id);Map<String,String> caller=new LinkedHashMap<>(globals),before=Map.copyOf(caller);
                    if(Set.of("MATCHED_EVALUATION","SOURCE_BASED_PRIVATE_ADAPTATION_NO_CONDITIONED_PROPERTIES","PRIVATE_DESIGN_SUCCESS").contains(kind)){
                        require(expected.length==6,"success fields");Result r;
                        try{r=evaluate(root.resolve("main.proj"),root,caller);}catch(ProfileRejected x){throw new AssertionError(id+" rejected "+x.code,x);}
                        String actual=observations(r,root);String wanted=String.join("\t",Arrays.copyOfRange(expected,2,6));
                        require(actual.equals(wanted),id+" native fields differ: "+actual+" expected "+wanted);immutable(r);
                        if(first==null){first=r;firstProperties=Map.copyOf(r.escapedProperties());}
                        rows.add(id+"\t"+kind+"\t"+actual);
                    }else{
                        require(expected.length==3,"failure fields");
                        try{evaluate(root.resolve("main.proj"),root,caller);throw new AssertionError(id+" expected "+expected[2]);}
                        catch(ProfileRejected x){require(Arrays.asList(expected[2].split(",")).contains(x.code),id+" expected "+expected[2]+" actual "+x.code);rows.add(id+"\t"+kind+"\t"+x.code);}
                        catch(EvaluationFailure x){require(expected[2].equals(x.referenceCode),id+" import error code");require(x.project.equals(root.resolve("main.proj"))&&x.importedProject.equals(root.resolve("absent.props")),id+" import failure path");rows.add(id+"\t"+kind+"\t"+x.referenceCode);}
                    }
                    require(caller.equals(before),id+" caller mutated");
                    if(first!=null)require(first.escapedProperties().equals(firstProperties),"retained snapshot mutated");
                    try(var files=Files.walk(root)){require(files.noneMatch(x->x.getFileName().toString().equals("must-not-exist.txt")),id+" task marker");}
                    expected=null;
                }
                default -> throw new AssertionError("unknown bridge row");
            }
        }
        require(expected==null&&rows.size()==count,"complete ordered corpus "+count);return rows;
    }
    static Map<?,?> cache() throws Exception {
        Class<?> state=Arrays.stream(ProjectEvaluationComponent.class.getDeclaredClasses()).filter(c->c.getSimpleName().equals("State")).findFirst().orElseThrow();
        Field field=state.getDeclaredField("CONDITIONS");field.setAccessible(true);return (Map<?,?>)field.get(null);
    }
    static void rawTree(Object value,Set<Object> seen) throws Exception {
        if(value==null||value instanceof String||value instanceof Boolean||!seen.add(value))return;
        Class<?> type=value.getClass();require(type.isRecord(),"cached AST is not immutable record: "+type);
        for(Field f:type.getDeclaredFields())if(!Modifier.isStatic(f.getModifiers())){
            require(Modifier.isFinal(f.getModifiers()),"nonfinal AST field");
            require(f.getType()==String.class||f.getType()==boolean.class||f.getType().getSimpleName().equals("ConditionExpression"),"AST retains evaluation context: "+f);
            f.setAccessible(true);rawTree(f.get(value),seen);
        }
    }
    static Path fixture(Path root,String raw) throws Exception {
        Files.createDirectories(root);Path file=root.resolve("main.proj");
        Files.writeString(file,"<Project><PropertyGroup Condition=\""+raw.replace("&","&amp;").replace("\"","&quot;")+"\"><P>yes</P></PropertyGroup></Project>");return file;
    }
    static void controls(Path root,List<String> rows) throws Exception {
        Path ascii=root.resolve("ascii");Path asciiFile=fixture(ascii,"$(Value)");
        for(String value:List.of("fal\u017fe","ye\u017f"))try{evaluate(asciiFile,ascii,Map.of("Value",value));throw new AssertionError("expanded Unicode Boolean accepted");}catch(ProfileRejected x){require(x.code.equals("UNICODE_COMPARISON"),"expanded Unicode boundary");}
        Path numeric=root.resolve("runtime-number");Path numericFile=fixture(numeric,"'$(Value)'=='$(Other)'");
        for(String[] pair:List.of(new String[]{" NaN "," NaN "},new String[]{"\t+NaN\r","NaN"},new String[]{"-NaN\n","-NaN"}))
            require(evaluate(numericFile,numeric,Map.of("Value",pair[0],"Other",pair[1])).property("P").isEmpty(),"source special NaN trim");
        for(String[] pair:List.of(new String[]{"1\0","1.0"},new String[]{"0x1\0\0","1"},new String[]{"0xffffffff\0","-1"},new String[]{"NaN\0","NaN\0"}))
            require(evaluate(numericFile,numeric,Map.of("Value",pair[0],"Other",pair[1])).property("P").equals("yes"),"source trailing NUL/fallback");
        Map<?,?> cached=cache();for(Object tree:cached.values())rawTree(tree,Collections.newSetFromMap(new IdentityHashMap<>()));
        String raw="!$(Switch) Or false And true";Path file=fixture(root,raw);
        Result first=evaluate(file,root,Map.of("Switch","false"));require(first.property("P").equals("yes")&&first.conditionWarnings().size()==1,"cold warning/value");
        require(evaluate(file,root,Map.of("Switch","true")).property("P").isEmpty(),"warm scalar state");
        try{evaluate(file,root,Map.of("Switch","invalid"));throw new AssertionError("failed conversion cached");}catch(ProfileRejected x){require(x.code.equals("CONDITION_NOT_BOOLEAN_CHILD"),"inner conversion error");}
        require(evaluate(file,root,Map.of("Switch","false")).property("P").equals("yes"),"failed then valid reuse");
        require(cache().containsKey(raw)&&!cache().containsKey("!false Or false And true"),"raw key expansion");
        fixture(root," "+raw);require(evaluate(file,root,Map.of("Switch","false")).conditionWarnings().size()==1,"spacing identity");
        int size=cache().size();fixture(root,"true");evaluate(file,root,Map.of());require(cache().size()>=size,"unexpected early eviction");
        // Generate exact raw variants through real project evaluation; no direct cache mutation.
        for(int i=0;i<3002;i++){fixture(root,"'evict"+i+"'=='evict"+i+"'");evaluate(file,root,Map.of());require(cache().size()<=3001,"cache retention bound");}
        fixture(root,raw);require(evaluate(file,root,Map.of("Switch","false")).conditionWarnings().size()==1,"warning did not reappear after eviction");
        require(first.property("P").equals("yes")&&first.conditionWarnings().size()==1,"retained result changed across eviction");
        for(String group:List.of("BC-RAW-AST-IMMUTABLE","BC-REACHED-EXPANSION","BC-ALIASES-DATA","BC-EXACT-RAW-CACHE","BC-WARNING-OWNER","BC-BOUNDS","BC-SKIPPED-SYNTAX","BC-PREDICATE-CONVERSIONS","BC-GLOBALS-AND-REASSIGN","BC-SITES-IMPORTS","BC-NO-TASK-OR-PROCESS","BC-MODULE-BOUNDARY","BC-CACHE-EVICTION","BC-PREDECESSOR-SUCCESSORS")){
            rows.add(group+"\tPRIVATE_CONTROL\tPASS");System.out.println("PASS_BOOLEAN_CONTROL "+group);
        }
    }
    public static void main(String[] args) throws Exception {
        require(args.length==7,"native bridge/fixtures, private bridge/fixtures, controls, output, JAR required");BooleanSuiteLauncher.identity(Path.of(args[6]));
        List<String> rows=consume(Path.of(args[0]),Path.of(args[1]),297);rows.addAll(consume(Path.of(args[2]),Path.of(args[3]),16));
        controls(Path.of(args[4]),rows);require(rows.size()==327,"297+16+14");Files.write(Path.of(args[5]),rows);System.out.println("PASS_BOOLEAN_CORPUS nativeIds=297 privateInputs=16 privateGroups=14");
    }
}
