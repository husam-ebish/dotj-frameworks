package org.dotj.internal.build.evaluation;

import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ItemsJson.*;

/** T129-IMPORTANT-01: raw ASCII order, before escaping; separate from the frozen42. */
public final class ItemsRawGlobOrderTest {
    static void require(boolean value,String why) { if(!value)throw new AssertionError(why); }
    public static void main(String[] args) throws Exception {
        Path root=Path.of(args[0]),jar=Path.of(args[1]);Files.createDirectories(root);
        require(ItemsProductCapture.hash(jar).equals(args[2]),"Wrong JAR bytes");
        for(Class<?> type:List.of(ProjectEvaluationComponent.class,ItemGlobs.class,ItemSnapshot.class))
            require(type.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri()),"Wrong product origin");
        Files.writeString(root.resolve("a0.cs"),"");Files.writeString(root.resolve("a@.cs"),"");
        Path project=root.resolve("main.proj");
        Files.writeString(project,"<Project><ItemGroup><I Include=\"*.cs\"/></ItemGroup></Project>");
        var first=ProjectEvaluationComponent.evaluate(project,root,Map.of());
        var pair=first.items().stream().map(ItemSnapshot::evaluatedInclude).toList();
        require(pair.equals(List.of("a0.cs","a@.cs")),"Raw pair order: "+pair);
        // Literal percent sequences must survive exactly one decode of stored escaping.
        Files.writeString(root.resolve("a%40.cs"),"");
        Files.writeString(project,"<Project><ItemGroup><I Include=\"a@.cs;*.cs;*.cs\"/><J Include=\"@(I)\"/></ItemGroup></Project>");
        var result=ProjectEvaluationComponent.evaluate(project,root,Map.of());
        var expected=List.of("a@.cs","a%40.cs","a0.cs","a@.cs","a%40.cs","a0.cs","a@.cs");
        var actual=result.items("I").stream().map(ItemSnapshot::evaluatedInclude).toList();
        require(actual.equals(expected),"Fragment order/duplicates/raw percent: "+actual);
        require(result.items("J").stream().map(ItemSnapshot::evaluatedInclude).toList().equals(expected),"Vector order changed");
        for(var item:result.items())require(item.metadataValue("Identity").equals(item.evaluatedInclude()),"Identity escaping changed");
        require(first.items().stream().map(ItemSnapshot::evaluatedInclude).toList().equals(pair),"Prior snapshot changed");
        System.out.println(write(object("id","T129-IMPORTANT-01","status","PASS","pair",pair,
            "fragmentsAndDuplicates",actual,"vectorOrder",expected,"identityEscaping",true,"retainedSnapshot",true,"jarSha256",args[2])));
    }
}
