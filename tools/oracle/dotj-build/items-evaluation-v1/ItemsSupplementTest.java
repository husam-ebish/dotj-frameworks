package org.dotj.internal.build.evaluation;

import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Exact frozen supplemental inputs; private mappings do not claim native exception ABI. */
public final class ItemsSupplementTest {
    public static void main(String[] args) throws Exception {
        Path root=Path.of(args[0]),jar=Path.of(args[1]);
        if(!ItemsProductCapture.hash(jar).equals(args[2]) || !ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri()))throw new AssertionError("Product identity");
        var expected=new LinkedHashMap<String,String>();
        expected.put("NEG-items","SUCCESS");expected.put("IR03-definition-vector","ITEM_REFERENCE_CONTEXT");
        expected.put("IR03-property-condition","PROPERTY_FUNCTION");expected.put("IR05-built-in-assignment","METADATA_RESERVED");
        for(var entry:expected.entrySet()) {
            Path dir=root.resolve(entry.getKey());
            try {
                Result result=evaluate(dir.resolve("main.proj"),dir,Map.of());
                if(!entry.getValue().equals("SUCCESS") || !result.items().isEmpty())throw new AssertionError(entry.getKey());
            }catch(ProfileRejected error) { if(!error.code.equals(entry.getValue()))throw new AssertionError(entry.getKey()+" "+error.code); }
            System.out.println(entry.getKey()+"\tPASS\t"+entry.getValue());
        }
    }
}
