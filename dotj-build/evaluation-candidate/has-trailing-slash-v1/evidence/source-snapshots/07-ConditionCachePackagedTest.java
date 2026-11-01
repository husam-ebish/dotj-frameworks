package org.dotj.internal.build.evaluation;

import java.lang.reflect.Modifier;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Fixture-only named-module consumer; expected values derive from externally pinned raw observations. */
final class ConditionCachePackagedTest {
    static void require(boolean value, String reason) {
        if (!value) throw new AssertionError(reason);
    }

    static String decode(String value) {
        return new String(Base64.getDecoder().decode(value), StandardCharsets.UTF_8);
    }

    static String encode(String value) {
        return Base64.getEncoder().encodeToString(value.getBytes(StandardCharsets.UTF_8));
    }

    static String relative(Path root, Path path) {
        require(path.startsWith(root), "Result path escaped fixture root");
        return root.relativize(path).toString().replace('\\', '/');
    }

    public static void main(String[] args) throws Exception {
        require(args.length == 5, "bridge, fixtures, output and actual candidate JAR and corpus mode required");
        Path bridge = Path.of(args[0]), fixtures = Path.of(args[1]), output = Path.of(args[2]), jar = Path.of(args[3]);
        require(ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri()),
                "Evaluator not loaded from actual candidate JAR");
        Module module = ProjectEvaluationComponent.class.getModule();
        require(module.isNamed() && module.getName().equals("org.dotj.build.evaluation.candidate") &&
                module.getDescriptor().exports().isEmpty() && module.getDescriptor().opens().isEmpty(), "Module identity/API exposure changed");
        require(!Modifier.isPublic(ProjectEvaluationComponent.class.getModifiers()), "Evaluator class exposed");
        System.out.println("PACKAGED_CONDITION_IDENTITY jar=" + jar + " module=" + module.getName() + " exports=0 opens=0");
        if (args[4].equals("controls")) {
            controls(fixtures, output);
            return;
        }
        List<String> results = new ArrayList<>(); List<String> failures = new ArrayList<>();
        Set<String> seen = new HashSet<>();
        String[] expected = null;
        Map<String, String> globals = new LinkedHashMap<>();
        int evaluations = 0, nativeParseBoundaries = 0, declaredBoundaries = 0, warningFields = 0;
        for (String line : Files.readAllLines(bridge, StandardCharsets.UTF_8)) {
            String[] fields = line.split("\t", -1);
            switch (fields[0]) {
                case "CASE" -> {
                    require(expected == null && fields.length >= 4, "Malformed or nested case");
                    expected = Arrays.copyOfRange(fields, 1, fields.length);
                    require(seen.add(expected[0]), "Duplicate case ID");
                    globals.clear();
                }
                case "GLOBAL" -> {
                    require(expected != null && fields.length == 3, "Global outside case");
                    require(globals.put(decode(fields[1]), decode(fields[2])) == null, "Duplicate global");
                }
                case "END" -> {
                    require(expected != null && fields.length == 1, "End outside case");
                    String id = expected[0], kind = expected[1];
                    Path root = fixtures.resolve(id), project = root.resolve("main.proj");
                    Map<String, String> caller = new LinkedHashMap<>(globals), before = Map.copyOf(caller);
                    if (kind.equals("MATCHED_EVALUATION")) {
                        require(expected.length == 6, "Evaluation fields missing");
                        Result result = evaluate(project, root, caller);
                        require(result.property("P").equals(decode(expected[2])) && result.property("Q").equals(decode(expected[3])), id + " P/Q mismatch");
                        StringJoiner imports = new StringJoiner("|");
                        for (ImportEdge edge : result.imports()) {
                            imports.add(relative(root, edge.owner()) + ">" + relative(root, edge.target()) + "@" + edge.line() + ":" + edge.column());
                        }
                        StringJoiner warnings = new StringJoiner("|");
                        for (ConditionWarning warning : result.conditionWarnings()) {
                            warnings.add(warning.referenceCode() + ":" + relative(root, warning.file()) + "@" + warning.line() + ":" + warning.column() + ":" + warning.condition());
                            warningFields++;
                        }
                        require(imports.toString().equals(decode(expected[4])), id + " ordered import owner/target/location mismatch");
                        if (!warnings.toString().equals(decode(expected[5]))) failures.add(id + " warning mismatch: expected=" + decode(expected[5]) + " actual=" + warnings);
                        require(result.importsIncludingDuplicates() == null && result.duplicateImports().isEmpty(), id + " Default duplicate contract changed");
                        if (args[4].equals("condition")) {
                            Result repeated = evaluate(project, root, caller);
                            require(result.escapedProperties().equals(repeated.escapedProperties()) && result.evaluatedFiles().equals(repeated.evaluatedFiles()) && result.imports().equals(repeated.imports()) && result.duplicateImports().equals(repeated.duplicateImports()) && Objects.equals(result.importsIncludingDuplicates(), repeated.importsIncludingDuplicates()), id + " repeated evaluation changed values/imports");
                            require(repeated.conditionWarnings().isEmpty(), id + " repeated parse warning");
                            immutable(repeated.imports()); immutable(repeated.evaluatedFiles()); immutable(repeated.conditionWarnings());
                        }
                        immutable(result.imports());
                        immutable(result.evaluatedFiles());
                        immutable(result.conditionWarnings());
                        results.add(String.join("\t", id, kind, encode(result.property("P")), encode(result.property("Q")), encode(imports.toString()), encode(warnings.toString())));
                        evaluations++;
                    } else {
                        require(expected.length == 3 && Set.of("PRIVATE_NATIVE_PARSE_BOUNDARY", "PRIVATE_DECLARED_BOUNDARY").contains(kind), "Unknown private boundary");
                        try {
                            evaluate(project, root, caller);
                            throw new AssertionError(id + " unexpectedly accepted private boundary");
                        } catch (ProfileRejected rejected) {
                            require(rejected.code.equals(expected[2]), id + " wrong private boundary code: " + rejected.code);
                            results.add(id + "\t" + kind + "\t" + rejected.code);
                        }
                        if (kind.equals("PRIVATE_NATIVE_PARSE_BOUNDARY")) nativeParseBoundaries++;
                        else declaredBoundaries++;
                    }
                    require(caller.equals(before), id + " caller globals mutated");
                    try (var paths = Files.walk(root)) {
                        require(paths.noneMatch(path -> path.getFileName().toString().equals("must-not-exist.txt")), id + " task marker created");
                    }
                    expected = null;
                }
                default -> throw new AssertionError("Unknown bridge row");
            }
        }
        require(expected == null && !results.isEmpty(), "Incomplete or empty bridge");
        if (args[4].equals("condition")) require(results.size() == 35 && evaluations == 26 && nativeParseBoundaries == 5 && declaredBoundaries == 4 && warningFields == 4, "Original 35 categories/four warning fields missing");
        else require(args[4].equals("cache") && results.size() == 8 && evaluations == 8 && nativeParseBoundaries == 0 && declaredBoundaries == 0, "Eight cache evaluations missing");
        Files.write(output, results, StandardCharsets.UTF_8);
        System.out.println("OBSERVED rows=" + results.size() + " evaluations=" + evaluations + " nativeParseBoundaries=" + nativeParseBoundaries + " declaredBoundaries=" + declaredBoundaries + " warnings=" + warningFields);
        require(failures.isEmpty(), String.join("\n", failures));
        System.out.println("PASS_PACKAGED_CACHE_COMPARISON");
    }
    static void immutable(List<?> values) {
        try { values.clear(); throw new AssertionError("Mutable result list"); }
        catch (UnsupportedOperationException expected) { }
    }
    static Path project(Path root, String condition) throws Exception {
        Files.createDirectories(root);
        Path file = root.resolve("main.proj");
        Files.writeString(file, "<Project><PropertyGroup><P Condition=\"" + condition + "\">$(Dynamic)</P></PropertyGroup></Project>");
        return file;
    }
    static void controls(Path root, Path output) throws Exception {
        List<String> rows = new ArrayList<>();
        String raw = "'$(Dynamic)' == 'Alpha' Or '$(Dynamic)' == 'Beta' And Exists('present.marker')";
        String[] values = {"Alpha", "Gamma", "Beta", "Beta"};
        String[] expected = {"Alpha", "", "Beta", ""};
        Result first = null;
        for (int index = 0; index < values.length; index++) {
            Path owner = root.resolve("owner-" + index);
            Path file = project(owner, raw);
            if (index == 2) Files.writeString(owner.resolve("present.marker"), "exists only here");
            Map<String,String> caller = new LinkedHashMap<>(Map.of("Dynamic", values[index]));
            Map<String,String> before = Map.copyOf(caller);
            Result result = evaluate(file, owner, caller);
            require(result.property("P").equals(expected[index]), "cached value or Exists owner leaked at " + index);
            require(result.conditionWarnings().size() == (index == 0 ? 1 : 0), "cache warning lifetime differs");
            require(caller.equals(before), "caller globals mutated on cache hit");
            immutable(result.imports()); immutable(result.evaluatedFiles()); immutable(result.conditionWarnings());
            try { result.escapedProperties().clear(); throw new AssertionError("Mutable properties"); }
            catch (UnsupportedOperationException immutable) { }
            if (index == 0) first = result;
        }
        require(first.property("P").equals("Alpha"), "retained result mutated by later evaluation");
        rows.add("CC-OWNER-AND-VALUE-FRESHNESS\tPRIVATE_CONTROL\tTRUE_FALSE_TRUE_FALSE");
        rows.add("CC-IMMUTABLE-SNAPSHOTS\tPRIVATE_CONTROL\tUNCHANGED");
        Path scalar = root.resolve("scalar");
        Path scalarFile = project(scalar, "'$(Dynamic)' == 'Alpha'");
        require(evaluate(scalarFile, scalar, Map.of("Dynamic", "Alpha")).property("P").equals("Alpha"), "scalar warmup failed");
        try {
            evaluate(scalarFile, scalar, Map.of("Dynamic", "Alpha' Or 'x' == 'x"));
            throw new AssertionError("cache hit accepted scalar grammar injection");
        } catch (ProfileRejected rejected) {
            require(Set.of("CONDITION_PROFILE", "CONDITION_COERCION").contains(rejected.code), "wrong scalar boundary");
        }
        rows.add("CC-WARM-SCALAR-INJECTION\tPRIVATE_CONTROL\tREJECTED");
        Files.writeString(scalarFile, "<Project><PropertyGroup Condition=\"false\"><P Condition=\"true Or (\">bad</P></PropertyGroup></Project>");
        try { evaluate(scalarFile, scalar, Map.of()); throw new AssertionError("skipped malformed condition accepted after warmup"); }
        catch (ProfileRejected rejected) { require(rejected.code.equals("CONDITION_PROFILE"), "wrong skipped syntax boundary"); }
        rows.add("CC-WARM-SKIPPED-MALFORMED\tPRIVATE_CONTROL\tREJECTED");
        Files.write(output, rows, StandardCharsets.UTF_8);
        System.out.println("PASS_PRIVATE_CACHE_CONTROLS count=4 nativeParity=false");
    }
}
