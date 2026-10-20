package org.dotj.internal.types;

import java.io.IOException;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.TreeSet;
import javax.tools.DiagnosticCollector;
import javax.tools.JavaFileObject;
import javax.tools.SimpleJavaFileObject;
import javax.tools.ToolProvider;

/** Compiles a restricted abstract Java source envelope from exact-name Task signatures. */
final class AritySourceCompiler {
    private AritySourceCompiler() {
    }

    static Compilation compile(String packageName, String className, List<String> signatures,
            List<JavaFileObject> supportSources, Path outputDirectory) throws IOException {
        Objects.requireNonNull(signatures, "signatures");
        Objects.requireNonNull(supportSources, "supportSources");
        Objects.requireNonNull(outputDirectory, "outputDirectory");
        if (signatures.isEmpty()) {
            throw new IllegalArgumentException("At least one method signature is required");
        }
        String source = render(packageName, className, signatures);
        var compiler = ToolProvider.getSystemJavaCompiler();
        if (compiler == null) {
            throw new IllegalStateException("A JDK compiler is required");
        }
        Files.createDirectories(outputDirectory);
        String qualifiedName = packageName + "." + className;
        List<JavaFileObject> units = new ArrayList<>(supportSources);
        units.add(sourceFile(qualifiedName, source));
        var diagnostics = new DiagnosticCollector<JavaFileObject>();
        boolean success = Boolean.TRUE.equals(compiler.getTask(null, null, diagnostics,
                List.of("--release", "21", "-d", outputDirectory.toString()), null, units).call());
        return new Compilation(success, source,
                diagnostics.getDiagnostics().stream().map(Object::toString).toList());
    }

    static String render(String packageName, String className, List<String> signatures) {
        requireQualifiedPackage(packageName);
        requireIdentifier(className);
        Objects.requireNonNull(signatures, "signatures");
        if (signatures.isEmpty()) {
            throw new IllegalArgumentException("At least one method signature is required");
        }
        Map<String, String> simpleNames = new HashMap<>();
        TreeSet<String> imports = new TreeSet<>();
        List<String> methods = new ArrayList<>();
        for (String signature : signatures) {
            var bound = ArityJavaSourceRenderer.renderMethod(signature, Set.of(className));
            for (String qualified : bound.imports()) {
                String simple = qualified.substring(qualified.lastIndexOf('.') + 1);
                String previous = simpleNames.putIfAbsent(simple, qualified);
                if (previous != null && !previous.equals(qualified)) {
                    throw new IllegalArgumentException("Conflicting imported type " + simple);
                }
                imports.add(qualified);
            }
            methods.add("    public abstract " + bound.declaration() + ";\n");
        }
        StringBuilder source = new StringBuilder("package ").append(packageName).append(";\n");
        for (String imported : imports) {
            source.append("import ").append(imported).append(";\n");
        }
        source.append("public abstract class ").append(className).append(" {\n");
        for (String method : methods) {
            source.append(method);
        }
        return source.append("}\n").toString();
    }

    private static void requireQualifiedPackage(String packageName) {
        Objects.requireNonNull(packageName, "packageName");
        if (packageName.isEmpty()) {
            throw new IllegalArgumentException("A package name is required");
        }
        for (String part : packageName.split("\\.", -1)) {
            requireIdentifier(part);
        }
    }

    private static void requireIdentifier(String identifier) {
        Objects.requireNonNull(identifier, "identifier");
        if (!ArityTypeReferenceBinder.isSourceIdentifier(identifier)) {
            throw new IllegalArgumentException("Invalid Java identifier: " + identifier);
        }
    }

    static JavaFileObject sourceFile(String qualifiedName, String source) {
        Objects.requireNonNull(qualifiedName, "qualifiedName");
        Objects.requireNonNull(source, "source");
        URI uri = URI.create("string:///" + qualifiedName.replace('.', '/') + JavaFileObject.Kind.SOURCE.extension);
        return new SimpleJavaFileObject(uri, JavaFileObject.Kind.SOURCE) {
            @Override
            public CharSequence getCharContent(boolean ignoreEncodingErrors) {
                return source;
            }
        };
    }

    record Compilation(boolean success, String source, List<String> diagnostics) {
        Compilation {
            diagnostics = List.copyOf(diagnostics);
        }
    }
}
