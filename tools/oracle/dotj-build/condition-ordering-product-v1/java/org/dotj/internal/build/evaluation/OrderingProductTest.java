package org.dotj.internal.build.evaluation;

import java.lang.reflect.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.jar.JarFile;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Fixture-only consumer of the exact adopted 308-row native bridge. */
public final class OrderingProductTest {
    private static final String MODULE="org.dotj.build.evaluation.candidate";
    static void require(boolean ok,String why) { if(!ok)throw new AssertionError(why); }
    static String dec(String value) { return new String(Base64.getDecoder().decode(value),StandardCharsets.UTF_8); }
    static String enc(String value) { return Base64.getEncoder().encodeToString(value.getBytes(StandardCharsets.UTF_8)); }
    static String sha(Path file) throws Exception {
        MessageDigest digest=MessageDigest.getInstance("SHA-256");
        try(var input=Files.newInputStream(file)) {
            byte[] block=new byte[65536];
            for(int n;(n=input.read(block))!=-1;)digest.update(block,0,n);
        }
        return HexFormat.of().formatHex(digest.digest());
    }
    static String rel(Path root,Path file) {
        require(file.startsWith(root),"path outside fixture");
        return root.relativize(file).toString().replace('\\','/');
    }
    static void origins(Path jar) throws Exception {
        Class<?> product=ProjectEvaluationComponent.class;
        Module module=product.getModule();
        require(module.isNamed()&&module.getName().equals(MODULE),"named product module");
        require(module.getDescriptor().exports().isEmpty()&&module.getDescriptor().opens().isEmpty(),"private module");
        require(module.getDescriptor().requires().stream().map(x->x.name()).collect(java.util.stream.Collectors.toSet()).equals(Set.of("java.base","java.xml")),"exact dependencies");
        require(!Modifier.isPublic(product.getModifiers()),"private evaluator");
        Path resolved=Path.of(ModuleLayer.boot().configuration().findModule(MODULE).orElseThrow().reference().location().orElseThrow()).toRealPath();
        require(resolved.equals(jar),"module JAR origin");
        int count=0;
        try(JarFile archive=new JarFile(jar.toFile())) {
            var entries=archive.entries();
            while(entries.hasMoreElements()) {
                String entry=entries.nextElement().getName();
                if(!entry.endsWith(".class")||entry.equals("module-info.class"))continue;
                Class<?> type=Class.forName(entry.substring(0,entry.length()-6).replace('/','.'),false,product.getClassLoader());
                require(type.getModule()==module,"class module origin "+entry);
                require(type.getProtectionDomain().getCodeSource()!=null,"class code source "+entry);
                require(Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar),"product class leaked from patch "+entry);
                count++;
            }
        }
        require(count>0,"product class inventory");
        System.out.println("ORDERING_PRODUCT_ORIGIN "+jar+" sha256="+sha(jar)+" classes="+count);
    }
    static void immutable(Result result) {
        for(List<?> value:List.of(result.imports(),result.evaluatedFiles(),result.duplicateImports(),result.conditionWarnings()))
            try { value.clear();throw new AssertionError("mutable snapshot"); } catch(UnsupportedOperationException expected) { }
        try { result.escapedProperties().clear();throw new AssertionError("mutable properties"); } catch(UnsupportedOperationException expected) { }
    }
    static List<String> observations(Result result,Path root) {
        StringJoiner imports=new StringJoiner("|"),warnings=new StringJoiner("|"),notices=new StringJoiner("|");
        for(ImportEdge edge:result.imports())imports.add(rel(root,edge.owner())+">"+rel(root,edge.target())+"@"+edge.line()+":"+edge.column());
        for(ConditionWarning warning:result.conditionWarnings())warnings.add(warning.referenceCode()+":"+rel(root,warning.file())+"@"+warning.line()+":"+warning.column()+":"+warning.condition());
        for(DuplicateImport notice:result.duplicateImports()) {
            // WarningPosition is a private record; the notice exposes no new public facade.
            try {
                Object position=notice.current();
                Method line=position.getClass().getDeclaredMethod("line"),column=position.getClass().getDeclaredMethod("column");
                line.setAccessible(true);column.setAccessible(true);
                notices.add(notice.referenceCode()+":"+rel(root,notice.owner())+"@"+line.invoke(position)+":"+column.invoke(position));
            } catch(ReflectiveOperationException error) { throw new AssertionError(error); }
        }
        require(result.importsIncludingDuplicates()==null,"Default record list is unavailable");
        return List.of(result.property("P"),result.property("Q"),imports.toString(),warnings.toString(),notices.toString());
    }
    static void corpus(Path fixtures,Path bridge,Path output) throws Exception {
        String[] expected=null;
        Map<String,String> globals=new LinkedHashMap<>();
        Set<String> ids=new HashSet<>();List<String> results=new ArrayList<>();
        int success=0,mapped=0,restricted=0;
        Result retained=null;Map<String,String> retainedProperties=null;
        for(String raw:Files.readAllLines(bridge,StandardCharsets.UTF_8)) {
            String[] f=raw.split("\t",-1);
            switch(f[0]) {
                case "CASE" -> {
                    require(expected==null&&f.length>=4&&ids.add(f[1]),"closed CASE schema");
                    expected=Arrays.copyOfRange(f,1,f.length);globals.clear();
                }
                case "GLOBAL" -> { require(expected!=null&&f.length==3&&globals.put(dec(f[1]),dec(f[2]))==null,"closed global"); }
                case "FILE" -> {
                    require(expected!=null&&f.length==4,"closed file row");
                    Path root=fixtures.resolve(expected[0]).toRealPath(),file=root.resolve(dec(f[1])).toRealPath();
                    require(file.startsWith(root)&&sha(file).equals(f[2])&&Files.size(file)==Long.parseLong(f[3]),"fixture bytes "+expected[0]);
                }
                case "END" -> {
                    require(expected!=null&&f.length==1,"closed END");
                    String id=expected[0],kind=expected[1];Path root=fixtures.resolve(id).toRealPath();
                    Map<String,String> caller=new LinkedHashMap<>(globals),before=Map.copyOf(caller);
                    System.out.println("ORDERING_CASE_BEGIN "+id+" "+kind);
                    if(kind.equals("NATIVE_SUCCESS")) {
                        require(expected.length==7,"five native success fields");
                        Result result=evaluate(root.resolve("main.proj"),root,caller);
                        List<String> actual=observations(result,root),wanted=new ArrayList<>();
                        for(int i=2;i<7;i++)wanted.add(dec(expected[i]));
                        require(actual.equals(wanted),id+" differs actual="+actual+" expected="+wanted);
                        immutable(result);success++;
                        if(retained==null) { retained=result;retainedProperties=Map.copyOf(result.escapedProperties()); }
                        results.add(id+"\t"+kind+"\t"+String.join("\t",actual.stream().map(OrderingProductTest::enc).toList()));
                    } else {
                        require(expected.length==3&&Set.of("PRIVATE_ERROR_MAPPING","PRIVATE_RESTRICTION").contains(kind),"reviewed failure disposition");
                        String code=dec(expected[2]);
                        try { evaluate(root.resolve("main.proj"),root,caller);throw new AssertionError(id+" expected "+code); }
                        catch(ProfileRejected error) {
                            require(error.code.equals(code),id+" expected "+code+" actual "+error.code);
                            if(id.equals("ORD-ERROR-source-error-side"))require(error.getMessage().contains("\"6.0.0\" evaluates to \"6.0.0\""),"numeric-left-based error side");
                        }
                        catch(EvaluationFailure error) {
                            require(code.equals("MSB4019")&&error.referenceCode.equals(code)&&error.project.equals(root.resolve("main.proj")),id+" missing import mapping");
                        }
                        if(kind.equals("PRIVATE_RESTRICTION"))restricted++;else mapped++;
                        results.add(id+"\t"+kind+"\t"+code);
                    }
                    require(caller.equals(before),id+" caller globals mutated");
                    if(retained!=null)require(retained.escapedProperties().equals(retainedProperties),"retained snapshot changed");
                    try(var paths=Files.walk(root)) { require(paths.noneMatch(x->x.getFileName().toString().equals("must-not-exist.txt")),id+" tasks executed"); }
                    System.out.println("ORDERING_CASE_END "+id);expected=null;
                }
                default -> throw new AssertionError("unknown bridge record");
            }
        }
        require(expected==null&&results.size()==308&&success==220&&mapped==81&&restricted==7,"complete308 classified rows: "+success+"/"+mapped+"/"+restricted);
        Files.write(output,results,StandardCharsets.UTF_8);
        System.out.println("PASS_ORDERING_308 nativeSuccess=220 mappedErrors=81 restrictions=7");
    }
    static Class<?> stateType() {
        return Arrays.stream(ProjectEvaluationComponent.class.getDeclaredClasses()).filter(x->x.getSimpleName().equals("State")).findFirst().orElseThrow();
    }
    static Map<?,?> cache() throws Exception {
        Field field=stateType().getDeclaredField("CONDITIONS");field.setAccessible(true);return (Map<?,?>)field.get(null);
    }
    static Path fixture(Path root,String raw) throws Exception {
        Files.createDirectories(root);Path file=root.resolve("main.proj");
        String xml=raw.replace("&","&amp;").replace("<","&lt;").replace("\"","&quot;");
        Files.writeString(file,"<Project><PropertyGroup Condition=\""+xml+"\"><P>yes</P></PropertyGroup></Project>",StandardCharsets.UTF_8);
        return file;
    }
    static void controls(Path root) throws Exception {
        // M1 observes the warning at the actual failure point without adding an evaluator API.
        String raw="'$(M1Left)'<'$(M1Right)' And true Or false";
        Path file=fixture(root.resolve("failure"),raw).toRealPath();Path sandbox=file.getParent();
        require(!cache().containsKey(raw),"M1 must start cold");
        Constructor<?> constructor=stateType().getDeclaredConstructor(Path.class,Map.class,ImportProfile.class);
        constructor.setAccessible(true);
        Object state=constructor.newInstance(sandbox,Map.of("M1Left","bad","M1Right","2"),ImportProfile.DEFAULT);
        Method read=stateType().getDeclaredMethod("read",Path.class,boolean.class);read.setAccessible(true);
        try { read.invoke(state,file,true);throw new AssertionError("M1 expected ordering conversion failure"); }
        catch(InvocationTargetException error) {
            require(error.getCause() instanceof ProfileRejected&&((ProfileRejected)error.getCause()).code.equals("CONDITION_NON_NUMERIC"),"M1 conversion failure category");
        }
        Field warnings=stateType().getDeclaredField("conditionWarnings");warnings.setAccessible(true);
        List<?> failedWarnings=List.copyOf((List<?>)warnings.get(state));
        require(failedWarnings.size()==1,"M1 warning must precede conversion error");
        ConditionWarning warning=(ConditionWarning)failedWarnings.get(0);
        require(warning.referenceCode().equals("MSB4130")&&warning.file().equals(file)&&warning.line()==1&&warning.column()==25&&warning.condition().equals(raw),"M1 original warning owner/position/raw");
        Object tree=cache().get(raw);require(tree!=null,"M1 raw AST retained after conversion failure");
        Result valid=evaluate(file,sandbox,Map.of("M1Left","1","M1Right","2"));
        require(valid.property("P").equals("yes")&&valid.conditionWarnings().isEmpty(),"M1 exact raw valid reuse has no stale failure/warning");
        Result falseResult=evaluate(file,sandbox,Map.of("M1Left","9","M1Right","2"));
        require(falseResult.property("P").isEmpty()&&falseResult.conditionWarnings().isEmpty(),"M1 converted values are evaluation-local");
        Path second=fixture(root.resolve("second-owner"),raw).toRealPath();
        Result other=evaluate(second,second.getParent(),Map.of("M1Left","1","M1Right","2"));
        require(other.property("P").equals("yes")&&other.conditionWarnings().isEmpty()&&cache().get(raw)==tree,"M1 raw identity across owners");
        require(((List<?>)warnings.get(state)).equals(failedWarnings),"M1 failed state warning changed during later evaluation");
        immutable(valid);immutable(other);
        // Non-scalar conversion must not execute predicates, Not or their children.
        for(String operand:List.of("Exists('C:bad')","HasTrailingSlash('a;b')","!Exists('C:bad')","(Exists('C:bad')==true)")) {
            Path f=fixture(root.resolve("non-scalar"),operand+"<2");
            try { evaluate(f,f.getParent(),Map.of());throw new AssertionError("non-scalar accepted"); }
            catch(ProfileRejected error) { require(error.code.equals("CONDITION_NON_NUMERIC"),"non-scalar child executed: "+operand+" "+error.code); }
        }
        // Native308 covers reached group64/node256 and refused65/257. Repeat exact skipped boundaries.
        // 63 comparisons +62 And +3 Not +true +Or =256 nodes; parentheses add no nodes.
        for(String skipped:List.of("(".repeat(64)+"1<2"+")".repeat(64),"(!!!1<2"+" And 1<2".repeat(62)+")")) {
            Path f=fixture(root.resolve("skipped-bound"),"true Or "+skipped);
            require(evaluate(f,f.getParent(),Map.of()).property("P").equals("yes"),"exact skipped boundary refused");
        }
        for(String skipped:List.of("(".repeat(65)+"1<2"+")".repeat(65),"(!!!!1<2"+" And 1<2".repeat(62)+")")) {
            Path f=fixture(root.resolve("skipped-bound"),"true Or "+skipped);
            try { evaluate(f,f.getParent(),Map.of());throw new AssertionError("skipped bound accepted"); }
            catch(ProfileRejected error) { require(error.code.equals("CONDITION_BOUND"),"skipped bound category"); }
        }
        // Source-based component boundaries; zero extra native parity credit.
        Path componentFile=fixture(root.resolve("components"),"'$(Version)'<'7.0.0'");
        for(String value:List.of("+6.-0.0","6.0.0 \0","6.\t0.0","0000000000006.0.0"))
            require(evaluate(componentFile,componentFile.getParent(),Map.of("Version",value)).property("P").equals("yes"),"component accepted "+enc(value));
        for(String value:List.of("6.0.0\0 ","6.+ 0.0","6.2147483648.0","6.-1.0","6..0","6.0.0.0.0"))
            try { evaluate(componentFile,componentFile.getParent(),Map.of("Version",value));throw new AssertionError("component accepted "+enc(value)); }
            catch(ProfileRejected error) { require(error.code.equals("CONDITION_NON_NUMERIC"),"component refusal"); }
        System.out.println("PASS_ORDERING_CONTROLS M1-warning-before-error exact-raw-reuse local-conversions non-scalar-no-evaluation skipped-bounds version-components");
    }
    public static void main(String[] args) throws Exception {
        require(args.length==6,"JAR, fixtures, bridge, bridgeSHA, controls, result output required");
        Path jar=Path.of(args[0]).toRealPath(),fixtures=Path.of(args[1]).toRealPath(),bridge=Path.of(args[2]).toRealPath();
        origins(jar);require(sha(bridge).equals(args[3]),"reviewed native-derived bridge identity");
        corpus(fixtures,bridge,Path.of(args[5]));controls(Path.of(args[4]));
    }
}
