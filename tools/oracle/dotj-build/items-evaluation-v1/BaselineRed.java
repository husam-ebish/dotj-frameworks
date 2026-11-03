package org.dotj.internal.build.evaluation;

import java.nio.file.Path;
import java.util.Map;

/** Calls only the retained evaluator entrypoint, against native-success inputs. */
public final class BaselineRed {
    public static void main(String[] args) throws Exception {
        Path jar = Path.of(args[2]);
        if (!ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri()))
            throw new AssertionError("Wrong retained artifact origin");
        int failures = 0;
        for (int i = 0; i < 2; i++) {
            String id = i == 0 ? "IP01" : "NEG-items";
            Path root = Path.of(args[i]);
            try {
                ProjectEvaluationComponent.evaluate(root.resolve("main.proj"), root, Map.of());
                System.out.println(id + "\tSUCCESS");
            } catch (ProjectEvaluationComponent.ProfileRejected error) {
                System.out.println(id + "\t" + error.code);
                if (!error.code.equals("UNSUPPORTED_ELEMENT")) throw error;
                failures++;
            }
        }
        if (failures != 0)
            throw new AssertionError("Required native-success item evaluation failed on retained artifact: " + failures);
    }
}
