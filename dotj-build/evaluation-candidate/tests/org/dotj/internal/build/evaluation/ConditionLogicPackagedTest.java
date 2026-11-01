package org.dotj.internal.build.evaluation;

import java.lang.reflect.Modifier;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Fixture-only named-module consumer; expected values derive from externally pinned raw observations. */
final class ConditionLogicPackagedTest {
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
        require(args.length == 4, "bridge, fixtures, output and actual candidate JAR required");
        Path bridge = Path.of(args[0]), fixtures = Path.of(args[1]), output = Path.of(args[2]), jar = Path.of(args[3]);
        require(ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri()),
                "Evaluator not loaded from actual candidate JAR");
        Module module = ProjectEvaluationComponent.class.getModule();
        require(module.isNamed() && module.getName().equals("org.dotj.build.evaluation.candidate") &&
                module.getDescriptor().exports().isEmpty() && module.getDescriptor().opens().isEmpty(), "Module identity/API exposure changed");
        require(!Modifier.isPublic(ProjectEvaluationComponent.class.getModifiers()), "Evaluator class exposed");
        System.out.println("PACKAGED_CONDITION_IDENTITY jar=" + jar + " module=" + module.getName() + " exports=0 opens=0");
        List<String> results = new ArrayList<>();
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
                        require(warnings.toString().equals(decode(expected[5])), id + " warning code/file/line/column/raw-condition mismatch");
                        require(result.importsIncludingDuplicates() == null && result.duplicateImports().isEmpty(), id + " Default duplicate contract changed");
                        require(result.equals(evaluate(project, root, caller)), id + " repeated evaluation leaked state");
                        ImportProfileTest.immutable(result.imports(), id + " imports");
                        ImportProfileTest.immutable(result.evaluatedFiles(), id + " evaluated files");
                        ImportProfileTest.immutable(result.conditionWarnings(), id + " warnings");
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
        require(expected == null && results.size() == 35 && evaluations == 26 && nativeParseBoundaries == 5 && declaredBoundaries == 4 && warningFields == 4,
                "Corpus categories or four warning fields missing");
        Files.write(output, results, StandardCharsets.UTF_8);
        System.out.println("PASS_PACKAGED_CONDITION evaluations=26 nativeParseBoundaries=5 declaredBoundaries=4 warningFields=4");
    }
}
