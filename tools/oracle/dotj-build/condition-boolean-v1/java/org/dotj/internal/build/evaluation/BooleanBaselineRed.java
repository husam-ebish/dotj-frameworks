package org.dotj.internal.build.evaluation;

import java.nio.file.Path;
import java.util.Map;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** JAR-only genuine red. Input must first be confirmed by the fresh native pair. */
final class BooleanBaselineRed {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new AssertionError("fixture directory and exact JAR required");
        Path root = Path.of(args[0]), jar = Path.of(args[1]);
        if (!ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri()))
            throw new AssertionError("BASELINE_JAR_IDENTITY_FAILURE");
        Module module = ProjectEvaluationComponent.class.getModule();
        if (!module.isNamed() || !module.getName().equals("org.dotj.build.evaluation.candidate") ||
            !module.getDescriptor().exports().isEmpty() || !module.getDescriptor().opens().isEmpty())
            throw new AssertionError("BASELINE_MODULE_BOUNDARY_FAILURE");
        System.out.println("BOOLEAN_BASELINE_IDENTITY_CONFIRMED");
        try {
            Result result = evaluate(root.resolve("main.proj"), root, Map.of());
            if (!result.property("P").equals("yes")) throw new AssertionError("BOOLEAN_BASELINE_WRONG_VALUE");
        } catch (ProfileRejected rejected) {
            if (!rejected.code.equals("CONDITION_PROFILE")) throw new AssertionError("UNRELATED_BASELINE_FAILURE " + rejected.code, rejected);
            System.err.println("BOOLEAN_GENUINE_RED BOOL-PREC-01 CONDITION_PROFILE");
            throw new AssertionError("NATIVE_SUPPORTED_BOOLEAN_REJECTED", rejected);
        }
        throw new AssertionError("BASELINE_UNEXPECTEDLY_ACCEPTED_NEW_BOOLEAN_BEHAVIOR");
    }
}
