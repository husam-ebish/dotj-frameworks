package org.dotj.internal.types;

import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;
import java.util.List;
import java.util.Set;
import javax.tools.DiagnosticCollector;
import javax.tools.JavaFileObject;
import javax.tools.SimpleJavaFileObject;
import javax.tools.ToolProvider;

public final class ArityMethodSignatureBinderTest {
    private ArityMethodSignatureBinderTest() {
    }

    public static void main(String[] args) throws Exception {
        assertLower("System.Threading.Tasks.Task Run()", "System.Threading.Tasks.Task Run()");
        assertLower("System.Threading.Tasks.Task WaitAsync(System.Threading.CancellationToken cancellationToken)",
                "System.Threading.Tasks.Task WaitAsync(System.Threading.CancellationToken cancellationToken)");
        assertLower("System.Threading.Tasks.Task<System.String> ContinueWith(System.Threading.Tasks.Task antecedent, System.Threading.Tasks.Task<System.String> other)",
                "System.Threading.Tasks.Task_1<System.String> ContinueWith(System.Threading.Tasks.Task antecedent, System.Threading.Tasks.Task_1<System.String> other)");
        assertLower("System.Threading.Tasks.Task<System.Threading.Tasks.Task<System.String>> Unwrap(System.Threading.Tasks.ValueTask<System.String> value)",
                "System.Threading.Tasks.Task_1<System.Threading.Tasks.Task_1<System.String>> Unwrap(System.Threading.Tasks.ValueTask_1<System.String> value)");
        expectInvalid("System.Threading.Tasks.Task Run(System.String)");
        expectInvalid("System.Threading.Tasks.Task Run(System.String value,)");
        expectInvalid("System.Threading.Tasks.Task Run(System.String value");
        expectInvalid("System.Threading.Tasks.Task Run(System.String value))");
        expectInvalid("System.Threading.Tasks.Task Run(System.Threading.Tasks.Task<System.String, System.String> value)");
        expectInvalid("System.Threading.Tasks.Task run-name()");
        verifyCompilableBackendDeclaration();
        java.lang.System.out.println("PASS: bounded Task-family method signature binding");
    }

    private static void verifyCompilableBackendDeclaration() throws Exception {
        String signature = ArityMethodSignatureBinder.lower(
                "System.Threading.Tasks.Task<java.lang.String> ContinueWith(System.Threading.Tasks.Task antecedent)");
        var rendered = ArityJavaSourceRenderer.renderMethod(
                "System.Threading.Tasks.Task<java.lang.String> ContinueWith(System.Threading.Tasks.Task antecedent)");
        if (!rendered.imports().equals(List.of("System.Threading.Tasks.Task", "System.Threading.Tasks.Task_1"))
                || !rendered.declaration().equals("Task_1<java.lang.String> ContinueWith(Task antecedent)")) {
            throw new AssertionError("Unexpected Task-family import rendering: " + rendered);
        }
        try {
            ArityJavaSourceRenderer.renderMethod("System.A.Task Invoke(System.B.Task other)");
            throw new AssertionError("Conflicting simple type names were accepted");
        } catch (IllegalArgumentException expected) {
            // Java imports cannot name two distinct Task types at once.
        }
        try {
            ArityJavaSourceRenderer.renderMethod("System.Threading.Tasks.Task Run()", Set.of("Task"));
            throw new AssertionError("Declaration-scope type collision was accepted");
        } catch (IllegalArgumentException expected) {
            // A generated Task declaration cannot import another simple Task name.
        }
        Path output = Files.createTempDirectory("dotj-arity-signature-");
        try {
            var compiler = ToolProvider.getSystemJavaCompiler();
            if (compiler == null) {
                throw new AssertionError("A JDK compiler is required");
            }
            List<JavaFileObject> direct = List.of(
                    source("System.Threading.Tasks.Task", "package System.Threading.Tasks; public class Task {}"),
                    source("System.Threading.Tasks.Task_1", "package System.Threading.Tasks; public class Task_1<T> {}"),
                    source("fixture.DirectProbe", "package fixture; public abstract class DirectProbe { public abstract "
                            + signature + "; }"));
            var directDiagnostics = new DiagnosticCollector<JavaFileObject>();
            Boolean directPassed = compiler.getTask(null, null, directDiagnostics,
                    List.of("--release", "21", "-d", output.toString()), null, direct).call();
            if (Boolean.TRUE.equals(directPassed) || directDiagnostics.getDiagnostics().stream().noneMatch(
                    diagnostic -> diagnostic.toString().contains("java.lang.System"))) {
                throw new AssertionError("Expected the java.lang.System source-name collision");
            }
            var diagnostics = new DiagnosticCollector<JavaFileObject>();
            List<JavaFileObject> sources = List.of(
                    source("System.Threading.Tasks.Task", "package System.Threading.Tasks; public class Task {}"),
                    source("System.Threading.Tasks.Task_1", "package System.Threading.Tasks; public class Task_1<T> {}"),
                    source("fixture.Probe", "package fixture; "
                            + String.join("", rendered.imports().stream().map(name -> "import " + name + "; ").toList())
                            + "public abstract class Probe { public abstract " + rendered.declaration() + "; }"));
            Boolean passed = compiler.getTask(null, null, diagnostics,
                    List.of("--release", "21", "-d", output.toString()), null, sources).call();
            if (!Boolean.TRUE.equals(passed)) {
                throw new AssertionError("Bound declaration did not compile: " + diagnostics.getDiagnostics());
            }
            if (!Files.isRegularFile(output.resolve("fixture/Probe.class"))
                    || !Files.isRegularFile(output.resolve("System/Threading/Tasks/Task.class"))
                    || !Files.isRegularFile(output.resolve("System/Threading/Tasks/Task_1.class"))) {
                throw new AssertionError("Expected JVM classes were not emitted");
            }
        } finally {
            try (var paths = Files.walk(output)) {
                for (Path path : paths.sorted(Comparator.reverseOrder()).toList()) {
                    Files.delete(path);
                }
            }
        }
    }

    private static JavaFileObject source(String name, String contents) {
        URI uri = URI.create("string:///" + name.replace('.', '/') + JavaFileObject.Kind.SOURCE.extension);
        return new SimpleJavaFileObject(uri, JavaFileObject.Kind.SOURCE) {
            @Override
            public CharSequence getCharContent(boolean ignoreEncodingErrors) {
                return contents;
            }
        };
    }

    private static void assertLower(String source, String expected) {
        String actual = ArityMethodSignatureBinder.lower(source);
        if (!expected.equals(actual)) {
            throw new AssertionError("Expected " + expected + ", got " + actual);
        }
    }

    private static void expectInvalid(String source) {
        try {
            ArityMethodSignatureBinder.lower(source);
            throw new AssertionError("Invalid signature accepted: " + source);
        } catch (IllegalArgumentException expected) {
            // The bounded grammar fails closed.
        }
    }
}
