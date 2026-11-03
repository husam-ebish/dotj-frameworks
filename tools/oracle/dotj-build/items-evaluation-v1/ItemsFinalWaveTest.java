package org.dotj.internal.build.evaluation;

import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ItemsJson.*;

/** Three separately reported Task130 boundary families; frozen native42 remains unchanged. */
public final class ItemsFinalWaveTest {
    static Path root,project;
    static String jarSha,platform;
    static void require(boolean value,String why) { if(!value)throw new AssertionError(why); }
    static ProjectEvaluationComponent.Result evaluate(String body) throws Exception {
        Files.writeString(project,"<Project><ItemGroup>"+body+"</ItemGroup></Project>");
        return ProjectEvaluationComponent.evaluate(project,root,Map.of());
    }
    static List<String> identities(ProjectEvaluationComponent.Result value,String type) {
        return value.items(type).stream().map(ItemSnapshot::evaluatedInclude).toList();
    }
    static void row(String id,Map<String,Object> values) {
        values.put("id",id);values.put("status","PASS");values.put("jarSha256",jarSha);values.put("platform",platform);
        System.out.println(write(values));
    }
    public static void main(String[] args) throws Exception {
        root=Path.of(args[0]);Path jar=Path.of(args[1]);jarSha=args[2];Files.createDirectories(root);
        platform=root.getFileSystem().getSeparator().equals("\\")?"windows":"linux";
        require(ItemsProductCapture.hash(jar).equals(jarSha),"Wrong JAR bytes");
        for(Class<?> type:List.of(ProjectEvaluationComponent.class,ItemGlobs.class,ItemSnapshot.class,ItemEvaluator.class))
            require(type.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri()),"Wrong product origin");
        project=root.resolve("main.proj");
        prefix();selectors();extensions();
    }
    static void prefix() throws Exception {
        for(String dir:List.of("a@","a%40")) {
            Files.createDirectory(root.resolve(dir));Files.writeString(root.resolve(dir).resolve("x.cs"),"");
        }
        var value=evaluate("<I Include=\"a%40/*.cs;a%2540/*.cs;a%40/*.cs\"><Seen>%(Identity)</Seen><Leaf>%(Filename)</Leaf></I>"
            +"<I Update=\"a%40/x.cs\"><M>at</M></I><I Update=\"a%2540/x.cs\"><M>percent</M></I>"
            +"<J Include=\"@(I)\"/><E Include=\"a%40/*.cs;a%2540/*.cs\" Exclude=\"a%40/x.cs\"/>"
            +"<R Include=\"@(I)\"/><R Remove=\"a%2540/x.cs\"/>");
        String sep=root.getFileSystem().getSeparator();
        var expected=List.of("a@"+sep+"x.cs","a%40"+sep+"x.cs","a@"+sep+"x.cs");
        require(identities(value,"I").equals(expected),"Prefix single escaping/duplicates");
        require(identities(value,"J").equals(expected),"Prefix vector copy");
        var metadata=value.items("I").stream().map(i->i.metadataValue("M")).toList();
        require(metadata.equals(List.of("at","percent","at")),"Prefix literal selection");
        require(value.items("J").stream().map(i->i.metadataValue("M")).toList().equals(metadata),"Copied metadata");
        for(var i:value.items("I"))require(i.metadataValue("Seen").equals(i.evaluatedInclude())&&i.metadataValue("Leaf").equals("x"),"Prefix inline metadata");
        require(identities(value,"E").equals(List.of(expected.get(1))),"Prefix Exclude single decode");
        require(identities(value,"R").equals(List.of(expected.get(0),expected.get(2))),"Prefix Remove single decode");
        row("T130-IMPORTANT-01",object("identities",expected,"copy",identities(value,"J"),"metadata",metadata,
            "exclude",identities(value,"E"),"remove",identities(value,"R"),"inlineIdentity",true));
    }
    static void selectors() throws Exception {
        String abs=root.resolve("a.cs").toString().replace("&","&amp;").replace("\"","&quot;");
        String specs="./a.cs;a.cs;d/../a.cs;missing/../a.cs;other.cs;p%2540.cs;p%40.cs";
        var value=evaluate("<S Include=\"./unused/../a.cs\"/><U Include=\""+specs+"\"/>"
            +"<Before Include=\"@(U)\"/><U Update=\"none;@(S)\"><M>updated</M></U>"
            +"<U Update=\"p%2540.cs\"><M>percent</M></U><U Update=\"p%40.cs\"><M>at</M></U>"
            +"<E Include=\"./a.cs;a.cs;d/../a.cs\" Exclude=\"z;./q/../a.cs\"/>"
            +"<R Include=\"./a.cs;a.cs;d/../a.cs;other.cs\"/><R Remove=\"@(S)\"/>"
            +"<A Include=\"./a.cs\"/><A Update=\""+abs+"\"><M>absolute</M></A>"
            +"<B Include=\"./a.cs\"/><B Update=\"d\\..\\a.cs\"><M>slashes</M></B>"
            +"<T Include=\"a.cs/\"/><T Update=\"a.cs\"><M>trailing</M></T>"
            +"<Invalid Include=\"./a|b\"/><Invalid Update=\"a|b\"><M>wrong</M></Invalid>");
        var expected=List.of("./a.cs","a.cs","d/../a.cs","missing/../a.cs","other.cs","p%40.cs","p@.cs");
        var metadata=value.items("U").stream().map(i->i.metadataValue("M")).toList();
        require(identities(value,"U").equals(expected),"Stored spelling/duplicates changed");
        require(metadata.equals(List.of("updated","updated","updated","updated","","percent","at")),"List/vector lexical selection");
        require(identities(value,"Before").equals(expected)&&value.items("Before").stream().allMatch(i->i.metadataValue("M").isEmpty()),"Copy changed after update");
        require(value.items("E").isEmpty()&&identities(value,"R").equals(List.of("other.cs")),"Normalized Exclude/Remove");
        require(value.items("A").getFirst().metadataValue("M").equals("absolute"),"Absolute selector");
        require(value.items("B").getFirst().metadataValue("M").equals("slashes"),"Mixed separators");
        require(value.items("T").getFirst().metadataValue("M").equals("trailing"),"Trailing separator");
        require(value.items("Invalid").getFirst().metadataValue("M").isEmpty(),"Native invalid-path fallback");
        require(!Files.exists(root.resolve("a.cs"))&&!Files.exists(root.resolve("missing")),"Literal matching consulted existing files");
        row("T130-IMPORTANT-02",object("identities",expected,"metadata",metadata,"excludeCount",value.items("E").size(),
            "remove",identities(value,"R"),"absolute",true,"mixedSeparators",true,"nonexistentPaths",true,"copyUnchanged",true,"invalidFallback",true,"trailingSeparator",true));
    }
    static void extensions() throws Exception {
        var value=evaluate("<I Include=\"name.;plain;file.cs;.hidden;multi.part.\"><E>%(Extension)</E></I>");
        var expected=List.of("","",".cs",".hidden","");
        var direct=value.items("I").stream().map(i->i.metadataValue("Extension")).toList();
        var inline=value.items("I").stream().map(i->i.metadataValue("E")).toList();
        require(direct.equals(expected)&&inline.equals(expected),"Direct/inline extension");
        var original=value.items("I").getFirst();
        require(original.metadataValue("Filename").equals("name"),"Trailing dot filename");
        require(original.metadataValue("DefiningProjectExtension").equals(".proj"),"Ordinary project extension");
        require(original.copy("J",root.resolve("owner."),Map.of()).metadataValue("DefiningProjectExtension").isEmpty(),"Trailing-dot project extension");
        require(!Files.exists(root.resolve("name.")),"Literal unexpectedly exists");
        row("T130-IMPORTANT-03",object("identities",identities(value,"I"),"direct",direct,"inline",inline,"definingProject",true,"nonexistentLiteral",true));
    }
}
