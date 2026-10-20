package org.dotj.internal.types;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Stream;
import javax.tools.JavaFileObject;

public final class AritySourceCompilerTest {
    private AritySourceCompilerTest() {
    }

    public static void main(String[] args) throws Exception {
        verifyBaseCompilation();
        if (args.length < 1 || args.length > 2) {
            throw new IllegalArgumentException("Expected fixture file and optional case ID");
        }
        String selected = args.length == 2 ? args[1] : null;
        int matched = 0;
        try (Stream<String> rows = Files.lines(Path.of(args[0]))) {
            for (String row : rows.filter(line -> !line.isBlank() && !line.startsWith("#")).toList()) {
                String[] fields = row.split("\t", -1);
                if (fields.length != 6) {
                    throw new AssertionError("Fixture row must have six fields: " + row);
                }
                if (selected == null || selected.equals(fields[0])) {
                    verifyFixture(fields);
                    matched++;
                }
            }
        }
        if (matched == 0) {
            throw new AssertionError("No selected fixture: " + selected);
        }
        java.lang.System.out.println("PASS: " + matched + " Task signature compilation fixture(s)");
        java.lang.System.out.println("PASS: restricted Task signature source compilation");
    }

    private static void verifyFixture(String[] fields) throws Exception {
        String id = fields[0];
        String expectation = fields[1];
        String packageName = fields[2];
        String className = fields[3];
        List<String> signatures = fields[4].isEmpty() ? List.of() : List.of(fields[4].split("~~", -1));
        String expectedText = fields[5];
        Path output = Files.createTempDirectory("dotj-arity-case-");
        try {
            List<JavaFileObject> support = List.of(
                    AritySourceCompiler.sourceFile("System.Threading.Tasks.Task",
                            "package System.Threading.Tasks; public class Task {}"),
                    AritySourceCompiler.sourceFile("System.Threading.Tasks.Task_1",
                            "package System.Threading.Tasks; public class Task_1<T> {}"),
                    AritySourceCompiler.sourceFile("System.Threading.Tasks.ValueTask",
                            "package System.Threading.Tasks; public class ValueTask {}"),
                    AritySourceCompiler.sourceFile("System.Threading.Tasks.ValueTask_1",
                            "package System.Threading.Tasks; public class ValueTask_1<T> {}"),
                    AritySourceCompiler.sourceFile("System.Threading.Tasks.TaskCompletionSource",
                            "package System.Threading.Tasks; public class TaskCompletionSource {}"),
                    AritySourceCompiler.sourceFile("System.Threading.Tasks.TaskCompletionSource_1",
                            "package System.Threading.Tasks; public class TaskCompletionSource_1<T> {}"),
                    AritySourceCompiler.sourceFile("System.String",
                            "package System; public class String {}"),
                    AritySourceCompiler.sourceFile("System.Threading.CancellationToken",
                            "package System.Threading; public class CancellationToken {}"));
            try {
                var result = AritySourceCompiler.compile(packageName, className, signatures, support, output);
                if (expectation.equals("REJECT")) {
                    throw new AssertionError(id + ": invalid source was accepted");
                }
                if (expectation.equals("COMPILE_FAIL")) {
                    if (result.success() || result.diagnostics().stream().noneMatch(text -> text.contains(expectedText))) {
                        throw new AssertionError(id + ": expected compiler failure: " + result.diagnostics());
                    }
                } else if (expectation.equals("PASS")) {
                    if (!result.success() || !result.source().contains(expectedText)
                            || !Files.isRegularFile(output.resolve(packageName.replace('.', '/') + "/" + className + ".class"))) {
                        throw new AssertionError(id + ": compilation or source check failed: " + result.diagnostics());
                    }
                } else {
                    throw new AssertionError(id + ": unknown expectation " + expectation);
                }
            } catch (IllegalArgumentException rejected) {
                if (!expectation.equals("REJECT") || !rejected.getMessage().contains(expectedText)) {
                    throw new AssertionError(id + ": unexpected rejection: " + rejected, rejected);
                }
            }
        } finally {
            try (var paths = Files.walk(output)) {
                for (Path path : paths.sorted(Comparator.reverseOrder()).toList()) {
                    Files.delete(path);
                }
            }
        }
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
