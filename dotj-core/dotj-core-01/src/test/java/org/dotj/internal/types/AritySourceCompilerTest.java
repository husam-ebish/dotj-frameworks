package org.dotj.internal.types;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;
import java.util.List;
import javax.tools.JavaFileObject;

public final class AritySourceCompilerTest {
    private AritySourceCompilerTest() {
    }

    public static void main(String[] args) throws Exception {
        verifyBaseCompilation();
        java.lang.System.out.println("PASS: restricted Task signature source compilation");
    }

    private static void verifyBaseCompilation() throws Exception {
        Path output = Files.createTempDirectory("dotj-arity-source-");
        try {
            List<JavaFileObject> support = List.of(
                    AritySourceCompiler.sourceFile("System.Threading.Tasks.Task",
                            "package System.Threading.Tasks; public class Task {}"),
                    AritySourceCompiler.sourceFile("System.Threading.Tasks.Task_1",
                            "package System.Threading.Tasks; public class Task_1<T> {}"));
            var result = AritySourceCompiler.compile("fixture", "Probe",
                    List.of("System.Threading.Tasks.Task<java.lang.String> ContinueWith(System.Threading.Tasks.Task antecedent)"),
                    support, output);
            if (!result.success()) {
                throw new AssertionError("Compilation failed: " + result.diagnostics());
            }
            if (!result.source().contains("Task_1<java.lang.String> ContinueWith(Task antecedent)")) {
                throw new AssertionError("Task arity was not lowered");
            }
            if (!Files.isRegularFile(output.resolve("fixture/Probe.class"))) {
                throw new AssertionError("No compiled class was emitted");
            }
        } finally {
            try (var paths = Files.walk(output)) {
                for (Path path : paths.sorted(Comparator.reverseOrder()).toList()) {
                    Files.delete(path);
                }
            }
        }
    }
}
