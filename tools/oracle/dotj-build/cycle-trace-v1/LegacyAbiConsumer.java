package org.dotj.internal.build.evaluation;

import java.nio.file.Path;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Compiled against the retained original artifact, then run without recompilation. */
public final class LegacyAbiConsumer {
    public static void main(String[] args) throws Exception {
        Path actual=Path.of(ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath();
        if(!actual.equals(Path.of(args[0]).toRealPath()))throw new AssertionError("ABI consumer product origin");
        Result six=new Result(Map.of("P","value"),List.of(Path.of("main.proj")),List.of(),List.of(),null,List.of());
        Result seven=new Result(Map.of("P","value"),List.of(Path.of("main.proj")),List.of(),List.of(),null,List.of(),ItemEvaluator.Output.empty());
        if(!six.equals(seven)||six.hashCode()!=seven.hashCode()||!six.toString().equals(seven.toString()))throw new AssertionError("Result value ABI");
        if(!Arrays.stream(Result.class.getRecordComponents()).map(java.lang.reflect.RecordComponent::getName).toList().equals(
            List.of("escapedProperties","evaluatedFiles","duplicateImports","imports","importsIncludingDuplicates","conditionWarnings","itemState")))throw new AssertionError("Result record shape");
        DuplicateImport diagnostic=new DuplicateImport("MSB4011",Path.of("owner"),Path.of("target"),null,null,null,DiagnosticKind.WARNING,ContextKind.PREVIOUS);
        if(!diagnostic.referenceCode().equals("MSB4011")||diagnostic.kind()!=DiagnosticKind.WARNING||diagnostic.contextKind()!=ContextKind.PREVIOUS)throw new AssertionError("DuplicateImport descriptor");
        EvaluationFailure failure=new EvaluationFailure(Path.of("owner"),Path.of("missing"));
        if(!failure.referenceCode.equals("MSB4019")||failure.reason!=FailureReason.MISSING_IMPORT||!failure.missingImport.equals(Path.of("missing")))throw new AssertionError("Failure ABI");
        System.out.println("PASS\tCC06-abi\told-compiled-consumer-six-seven-record-failure");
    }
}
