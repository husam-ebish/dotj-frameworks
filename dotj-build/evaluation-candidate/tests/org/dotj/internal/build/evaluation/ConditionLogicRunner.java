package org.dotj.internal.build.evaluation;

import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Evaluates each logic-v2 fixture once; one tab-separated Base64 row per case. */
final class ConditionLogicRunner {
    static String encode(String value) {
        return Base64.getEncoder().encodeToString(value.getBytes(StandardCharsets.UTF_8));
    }
    public static void main(String[] args) throws Exception {
        Path fixtures=Path.of(args[0]).toAbsolutePath().normalize();
        for(String line:Files.readAllLines(Path.of(args[1]),StandardCharsets.UTF_8)) {
            String[] columns=line.split("\t",-1);
            Map<String,String> globals=new HashMap<>();
            for(int i=1;i+1<columns.length;i+=2) {
                globals.put(new String(Base64.getDecoder().decode(columns[i]),StandardCharsets.UTF_8),
                            new String(Base64.getDecoder().decode(columns[i+1]),StandardCharsets.UTF_8));
            }
            Path root=fixtures.resolve(columns[0]);
            try {
                Result result=evaluate(root.resolve("main.proj"),root,globals);
                StringJoiner imports=new StringJoiner("|");
                for(ImportEdge edge:result.imports())
                    imports.add(root.relativize(edge.owner())+">"+root.relativize(edge.target())+"@"+edge.line()+":"+edge.column());
                StringJoiner warnings=new StringJoiner("|");
                for(ConditionWarning warning:result.conditionWarnings())
                    warnings.add(warning.referenceCode()+":"+root.relativize(warning.file())+"@"+warning.line()+":"+warning.column()+":"+warning.condition());
                System.out.println(columns[0]+"\tOK\t"+encode(result.property("P"))+"\t"+encode(result.property("Q"))+"\t"+encode(imports.toString())+"\t"+encode(warnings.toString()));
            } catch(ProfileRejected rejected) {
                System.out.println(columns[0]+"\tREJECT\t"+rejected.code);
            }
        }
    }
}
