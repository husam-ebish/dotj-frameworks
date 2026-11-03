package org.dotj.internal.build.evaluation;

import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Private admission, limits and ownership controls; no native parity credit. */
public final class ItemsPrivateTest {
    static Path root;
    static final List<String> rows=new ArrayList<>();
    static void require(boolean value,String why) { if(!value)throw new AssertionError(why); }
    static String project(String body) { return "<Project>"+body+"</Project>"; }
    static String item(String spec) { return project("<ItemGroup><I Include=\""+spec+"\"/></ItemGroup>"); }
    static Result evaluate(String id,String xml) throws Exception {
        Path dir=root.resolve(id);Files.createDirectories(dir);Path path=dir.resolve("main.proj");Files.writeString(path,xml);
        return ProjectEvaluationComponent.evaluate(path,dir,Map.of());
    }
    static void ok(String id,String xml,int count) throws Exception {
        require(evaluate(id,xml).items().size()==count,id+" count");rows.add(id+"\tPASS\tSUCCESS");
    }
    static void reject(String id,String xml,String code) throws Exception {
        try { evaluate(id,xml);throw new AssertionError(id+" unexpectedly accepted"); }
        catch(ProfileRejected ex) { require(ex.code.equals(code),id+" expected "+code+" got "+ex.code);rows.add(id+"\tPASS\t"+code); }
    }
    static void immutable(Runnable action) {
        try { action.run();throw new AssertionError("Mutable snapshot"); }catch(UnsupportedOperationException expected) { }
    }
    static String metadata(int count) {
        StringBuilder xml=new StringBuilder();for(int i=0;i<count;i++)xml.append("<M"+i+">v</M"+i+">");return xml.toString();
    }
    static void windows() throws Exception {
        for(String expression:List.of("@(I->'%(Filename)')","@(I->Count())","@(I, ',')"))reject("IR01-"+rows.size(),item(expression),"ITEM_NAME");
        reject("IR02-mixed",item("prefix@(I)"),"ITEM_MIXED_VECTOR");
        reject("IR02-qualified",project("<ItemGroup><I Include=\"a\"><M>%(Other.M)</M></I></ItemGroup>"),"METADATA_QUALIFIER");
        reject("IR03-definition-value",project("<ItemDefinitionGroup><I><M>@(I)</M></I></ItemDefinitionGroup>"),"ITEM_REFERENCE_CONTEXT");
        reject("IR03-definition-condition",project("<ItemDefinitionGroup Condition=\"'@(I)' == ''\"><I/></ItemDefinitionGroup>"),"ITEM_REFERENCE_CONTEXT");
        reject("IR03-property",project("<PropertyGroup Condition=\"'@(I)' == ''\"><P>x</P></PropertyGroup>"),"PROPERTY_FUNCTION");
        reject("IR03-import",project("<Import Project=\"@(I)\"/>"),"PROPERTY_FUNCTION");
        for(String attr:List.of("MatchOnMetadata","KeepMetadata","RemoveMetadata","KeepDuplicates","M"))reject("IR04-"+attr,project("<ItemGroup><I Include=\"a\" "+attr+"=\"x\"/></ItemGroup>"),"UNSUPPORTED_ATTRIBUTE");
        reject("IR05-reserved",project("<ItemGroup><I Include=\"a\"><Filename>x</Filename></I></ItemGroup>"),"METADATA_RESERVED");
        reject("IR05-timestamp",project("<ItemGroup><I Include=\"a\"><M>%(ModifiedTime)</M></I></ItemGroup>"),"METADATA_TIMESTAMP");
        reject("IR06-unclosed",item("@(I"),"ITEM_REFERENCE");
        reject("IR06-escape",item("a%41"),"ITEM_ESCAPE");
        reject("IR06-unicode",item("\u03bb"),"ITEM_ASCII");
        reject("IR06-skipped",project("<ItemGroup Condition=\"false\"><I Include=\"@(I\"/></ItemGroup>"),"ITEM_REFERENCE");
        ok("IR06-skipped-data",project("<ItemGroup Condition=\"false\"><I Include=\"\u03bb\"/></ItemGroup>"),0);
        for(String glob:List.of("/*.cs","C:/*.cs","//server/*.cs","https://host/*.cs","dir\\*.cs","../*.cs"))reject("IR07-"+rows.size(),item(glob),"ITEM_GLOB_PATH");
        ok("IR09-512",project("<ItemGroup>"+"<I Include=\"a\"/>".repeat(512)+"</ItemGroup>"),512);
        reject("IR09-513",project("<ItemGroup>"+"<I Include=\"a\"/>".repeat(513)+"</ItemGroup>"),"ITEM_OPERATION_BOUND");
        ok("IR09-definitions512",project("<ItemDefinitionGroup>"+"<I/>".repeat(512)+"</ItemDefinitionGroup>"),0);
        reject("IR09-definitions513",project("<ItemDefinitionGroup>"+"<I/>".repeat(513)+"</ItemDefinitionGroup>"),"ITEM_OPERATION_BOUND");
        ok("IR10-live1024",item("a;".repeat(1024)),1024);
        reject("IR10-live1025",item("a;".repeat(1025)),"ITEM_LIVE_BOUND");
        ok("IR10-metadata64",project("<ItemGroup><I Include=\"a\">"+metadata(64)+"</I></ItemGroup>"),1);
        reject("IR10-metadata65",project("<ItemGroup><I Include=\"a\">"+metadata(65)+"</I></ItemGroup>"),"ITEM_METADATA_BOUND");
        ok("IR10-defaults64",project("<ItemDefinitionGroup><I>"+metadata(64)+"</I></ItemDefinitionGroup>"),0);
        reject("IR10-defaults65",project("<ItemDefinitionGroup><I>"+metadata(65)+"</I></ItemDefinitionGroup>"),"ITEM_METADATA_BOUND");
        Path entries=root.resolve("IR11-entries/entries");Files.createDirectories(entries);
        for(int i=0;i<4096;i++)Files.writeString(entries.resolve("f"+i+".txt"),"");
        ok("IR11-entries",item("entries/*.zz"),0);
        Files.writeString(entries.resolve("f4096.txt"),"");
        reject("IR11-entries",item("entries/*.zz"),"ITEM_TRAVERSAL_BOUND");
        Path depth=root.resolve("IR11-depth");Files.createDirectories(depth);
        for(int i=0;i<32;i++){depth=depth.resolve("d");Files.createDirectory(depth);}
        ok("IR11-depth",item("d/**/*.zz"),0);Files.createDirectory(depth.resolve("d"));
        reject("IR11-depth",item("d/**/*.zz"),"ITEM_DEPTH_BOUND");
        ok("IR11-segments64",item("d/".repeat(63)+"*.zz"),0);
        reject("IR11-segments65",item("d/".repeat(64)+"*.zz"),"ITEM_PATTERN_BOUND");
        reject("IR12-shape",item("a**b/*.cs"),"ITEM_GLOB_SHAPE");
        reject("IR13-task",project("<UsingTask TaskName=\"T\" AssemblyFile=\"x.dll\"/>"),"UNSUPPORTED_ELEMENT");
        reject("IR13-factory",project("<UsingTask TaskName=\"T\" TaskFactory=\"F\" AssemblyFile=\"x.dll\"/>"),"UNSUPPORTED_ELEMENT");
        reject("IR13-target",project("<Target Name=\"T\"><ItemGroup><I Include=\"a\"/></ItemGroup></Target>"),"TARGET_DECLARATION_PROFILE");
        reject("IR13-sdk","<Project Sdk=\"Never\"/>","UNSUPPORTED_ATTRIBUTE");
        String condition="'@(I)' == ''";
        ok("IR14-warm",project("<ItemGroup Condition=\""+condition+"\"><I Include=\"a\"/></ItemGroup>"),1);
        reject("IR14-forbidden",project("<PropertyGroup Condition=\""+condition+"\"><P>x</P></PropertyGroup>"),"PROPERTY_FUNCTION");
        ok("IR14-reuse",project("<ItemGroup><I Include=\"x\"/></ItemGroup><ItemGroup Condition=\""+condition+"\"><I Include=\"a\"/></ItemGroup>"),1);
        reject("IR14-tree",project("<ItemGroup Condition=\""+"true Or ".repeat(256)+"true\"><I Include=\"a\"/></ItemGroup>"),"CONDITION_BOUND");
        String nested="(".repeat(65)+"true"+")".repeat(65);
        reject("IR14-depth",project("<ItemGroup Condition=\""+nested+"\"><I Include=\"a\"/></ItemGroup>"),"CONDITION_BOUND");
        Result result=evaluate("ownership",project("<ItemDefinitionGroup><I><D>v</D></I></ItemDefinitionGroup><ItemGroup><I Include=\"a\"><M>x</M></I></ItemGroup>"));
        ItemSnapshot first=result.items().getFirst();
        immutable(()->result.items().clear());immutable(()->result.itemDefinitions().clear());immutable(()->first.metadata().clear());
        immutable(()->first.direct.clear());immutable(()->first.defaults.clear());immutable(()->first.inherited.clear());
        immutable(()->result.itemDefinitions().get("I").metadata().clear());
        evaluate("ownership-other",item("b"));require(first.evaluatedInclude().equals("a")&&first.metadataValue("M").equals("x"),"Snapshot changed");
        Result legacy=new Result(Map.of("P","v"),List.of(),List.of(),List.of(),null,List.of());
        require(legacy.property("P").equals("v")&&legacy.items().isEmpty()&&legacy.importsIncludingDuplicates()==null,"Six argument ABI");
        rows.add("OWNERSHIP-ABI\tPASS\tIMMUTABLE");
    }
    static void linux() throws Exception {
        for(String kind:List.of("inside","outside")) {
            Path dir=root.resolve("IR08-"+kind);Files.createDirectories(dir);
            Path target=kind.equals("inside")?dir.resolve("target"):root.resolve("outside-target");Files.createDirectories(target);Files.writeString(target.resolve("a.cs"),"");
            Files.createSymbolicLink(dir.resolve("alias"),target);
            require(Files.isSymbolicLink(dir.resolve("alias")),"Symlink capability absent");
            reject("IR08-"+kind,item("alias/*.cs"),"ITEM_GLOB_ALIAS");
        }
        Path collision=root.resolve("IR12-collision");Files.createDirectories(collision);
        Files.writeString(collision.resolve("a.cs"),"lower");Files.writeString(collision.resolve("A.cs"),"upper");
        require(!Files.isSameFile(collision.resolve("a.cs"),collision.resolve("A.cs")),"Case-distinct capability absent");
        reject("IR12-collision",item("*.cs"),"ITEM_CASE_COLLISION");
        ok("IR08-recovery",item("a.cs"),1);
    }
    public static void main(String[] args) throws Exception {
        root=Path.of(args[0]).toAbsolutePath();Files.createDirectories(root);
        Path jar=Path.of(args[2]);
        require(ItemsProductCapture.hash(jar).equals(args[3]),"Wrong JAR bytes");
        for(Class<?> type:List.of(ProjectEvaluationComponent.class,ItemEvaluator.class,ItemExpressions.class,ItemGlobs.class,ItemSnapshot.class))
            require(type.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri()),"Product origin "+type);
        if(args[1].equals("linux"))linux();else windows();
        Files.write(root.resolve("results.tsv"),rows);
        System.out.println("PASS "+args[1]+" private controls "+rows.size()+" rows; jar "+args[3]);
    }
}
