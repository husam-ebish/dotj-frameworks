package org.dotj.internal.build.evaluation;

import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Windows reparse-point controls complement Linux symbolic-link controls. */
public final class ItemsJunctionTest {
    public static void main(String[] args) throws Exception {
        Path root=Path.of(args[0]),jar=Path.of(args[1]);
        if(!ItemsProductCapture.hash(jar).equals(args[2]) || !ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri()))throw new AssertionError("Product identity");
        for(String name:List.of("inside","outside")) {
            Path dir=root.resolve(name),alias=dir.resolve("alias");
            BasicFileAttributes attributes=Files.readAttributes(alias,BasicFileAttributes.class,LinkOption.NOFOLLOW_LINKS);
            if(!attributes.isOther() || alias.toRealPath().equals(alias.toAbsolutePath().normalize()))throw new AssertionError("Real junction capability absent");
            Path file=dir.resolve("main.proj");Files.writeString(file,"<Project><ItemGroup><I Include=\"alias/*.cs\"/></ItemGroup></Project>");
            try { evaluate(file,dir,Map.of());throw new AssertionError("Junction admitted"); }
            catch(ProfileRejected error) { if(!error.code.equals("ITEM_GLOB_ALIAS"))throw new AssertionError(error.code); }
            System.out.println("IR08-windows-"+name+"\tPASS\tITEM_GLOB_ALIAS");
        }
        Path recovery=root.resolve("recovery");Files.createDirectory(recovery);Path file=recovery.resolve("main.proj");
        Files.writeString(file,"<Project><ItemGroup><I Include=\"a.cs\"/></ItemGroup></Project>");
        if(evaluate(file,recovery,Map.of()).items().size()!=1)throw new AssertionError("Failure recovery");
        System.out.println("IR08-windows-recovery\tPASS\tSUCCESS");
    }
}
