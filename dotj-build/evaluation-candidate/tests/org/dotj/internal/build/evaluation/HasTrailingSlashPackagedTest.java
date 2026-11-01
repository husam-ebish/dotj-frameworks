package org.dotj.internal.build.evaluation;

import java.lang.reflect.Modifier;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import static org.dotj.internal.build.evaluation.ProjectEvaluationComponent.*;

/** Explicit JAR-only module patch consumer. Native bridge must be frozen first. */
final class HasTrailingSlashPackagedTest {
    static void require(boolean ok, String message) { if (!ok) throw new AssertionError(message); }
    static String dec(String value) { return new String(Base64.getDecoder().decode(value), StandardCharsets.UTF_8); }
    static String enc(String value) { return Base64.getEncoder().encodeToString(value.getBytes(StandardCharsets.UTF_8)); }
    static String relative(Path root, Path path) {
        require(path.startsWith(root), "path outside case root");
        return root.relativize(path).toString().replace('\\', '/');
    }
    static void immutable(Result result) {
        for (List<?> list : List.of(result.imports(), result.evaluatedFiles(), result.conditionWarnings(), result.duplicateImports())) {
            try { list.clear(); throw new AssertionError("mutable result list"); }
            catch (UnsupportedOperationException expected) { }
        }
        try { result.escapedProperties().clear(); throw new AssertionError("mutable properties"); }
        catch (UnsupportedOperationException expected) { }
    }
    public static void main(String[] args) throws Exception {
        require(args.length == 5, "bridge, fixtures, output, JAR, corpus|controls|red required");
        Path bridge = Path.of(args[0]), fixtures = Path.of(args[1]), output = Path.of(args[2]), jar = Path.of(args[3]);
        require(ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI().equals(jar.toUri()), "product not loaded from exact JAR");
        Module module = ProjectEvaluationComponent.class.getModule();
        require(module.isNamed() && module.getName().equals("org.dotj.build.evaluation.candidate") && module.getDescriptor().exports().isEmpty() && module.getDescriptor().opens().isEmpty(), "named module/API closure");
        require(!Modifier.isPublic(ProjectEvaluationComponent.class.getModifiers()), "evaluator became public");
        if (args[4].equals("controls")) { controls(fixtures, output); return; }
        require(Set.of("corpus", "red").contains(args[4]), "unknown mode");
        List<String> actual = new ArrayList<>(); Map<String,String> globals = new LinkedHashMap<>();
        Set<String> seen = new HashSet<>(); String[] expected = null;
        int matches = 0, boundaries = 0; Result retained = null; Map<String,String> retainedProperties = null;
        for (String line : Files.readAllLines(bridge, StandardCharsets.UTF_8)) {
            String[] fields = line.split("\t", -1);
            switch (fields[0]) {
                case "CASE" -> {
                    require(expected == null && fields.length >= 4, "nested/malformed case");
                    expected = Arrays.copyOfRange(fields, 1, fields.length); globals.clear();
                    require(seen.add(expected[0]), "duplicate case");
                }
                case "GLOBAL" -> {
                    require(expected != null && fields.length == 3, "malformed global");
                    require(globals.put(dec(fields[1]), dec(fields[2])) == null, "duplicate global");
                }
                case "END" -> {
                    require(expected != null && fields.length == 1, "end outside case");
                    String id = expected[0], kind = expected[1]; Path root = fixtures.resolve(id);
                    Map<String,String> caller = new LinkedHashMap<>(globals), before = Map.copyOf(caller);
                    if (kind.equals("MATCHED_EVALUATION")) {
                        require(expected.length == 6, "missing native evaluation fields");
                        Result result;
                        try { result = evaluate(root.resolve("main.proj"), root, caller); }
                        catch (ProfileRejected rejection) {
                            // Baseline RED is an actual behavior failure, never accepted refusal.
                            throw new AssertionError(id + " NATIVE_SUPPORTED_PREDICATE_REJECTED " + rejection.code, rejection);
                        }
                        require(result.property("P").equals(dec(expected[2])) && result.property("Q").equals(dec(expected[3])), id + " P/Q differ from frozen native");
                        StringJoiner imports = new StringJoiner("|"), warnings = new StringJoiner("|");
                        for (ImportEdge edge : result.imports()) imports.add(relative(root,edge.owner()) + ">" + relative(root,edge.target()) + "@" + edge.line() + ":" + edge.column());
                        for (ConditionWarning warning : result.conditionWarnings()) warnings.add(warning.referenceCode() + ":" + relative(root,warning.file()) + "@" + warning.line() + ":" + warning.column() + ":" + warning.condition());
                        require(imports.toString().equals(dec(expected[4])), id + " ordered imports differ");
                        require(warnings.toString().equals(dec(expected[5])), id + " ordered warning fields differ");
                        require(result.importsIncludingDuplicates() == null && result.duplicateImports().isEmpty(), id + " Default duplicates changed");
                        immutable(result);
                        if (id.equals("HT14-cache-first")) { retained = result; retainedProperties = Map.copyOf(result.escapedProperties()); }
                        if (id.equals("HT16-cache-third")) require(retained != null && retained.escapedProperties().equals(retainedProperties), "retained snapshot mutated");
                        actual.add(String.join("\t", id, kind, enc(result.property("P")), enc(result.property("Q")), enc(imports.toString()), enc(warnings.toString()))); matches++;
                    } else {
                        require(expected.length == 3 && Set.of("PRIVATE_NATIVE_PARSE_BOUNDARY", "PRIVATE_DECLARED_BOUNDARY").contains(kind), "unknown boundary disposition");
                        try { evaluate(root.resolve("main.proj"), root, caller); throw new AssertionError(id + " private boundary accepted"); }
                        catch (ProfileRejected rejection) {
                            require(Set.of(expected[2].split(",")).contains(rejection.code), id + " private error category " + rejection.code);
                            actual.add(id + "\t" + kind + "\t" + rejection.code);
                        }
                        boundaries++;
                    }
                    require(caller.equals(before), id + " caller map mutated");
                    try (var paths = Files.walk(root)) { require(paths.noneMatch(p -> p.getFileName().toString().equals("must-not-exist.txt")), "task marker exists"); }
                    expected = null;
                    if (args[4].equals("red")) {
                        require(id.equals("HT01-literal-separators") && matches == 1, "RED must isolate HT01");
                        Files.write(output, actual, StandardCharsets.UTF_8); return;
                    }
                }
                default -> throw new AssertionError("unknown bridge field");
            }
        }
        require(expected == null && actual.size() == 38 && matches == 32 && boundaries == 6, "38/32/6 disposition counts");
        Files.write(output, actual, StandardCharsets.UTF_8);
        System.out.println("PASS_HAS_TRAILING_SLASH rows=38 semantic=32 boundaries=6 publicAcceptance=false");
    }
    static String xml(String condition) { return condition.replace("&", "&amp;").replace("\"", "&quot;").replace("<", "&lt;"); }
    static Path fixture(Path root, String condition, boolean skipped) throws Exception {
        Files.createDirectories(root); Path file = root.resolve("main.proj");
        Files.writeString(file, "<Project><PropertyGroup" + (skipped ? " Condition=\"false\"" : "") + "><P Condition=\"" + xml(condition) + "\">yes</P></PropertyGroup></Project>"); return file;
    }
    static void rejected(Path root, String condition, boolean skipped, Map<String,String> globals, Set<String> codes) throws Exception {
        try { evaluate(fixture(root,condition,skipped),root,globals); throw new AssertionError("accepted private refusal: " + condition); }
        catch (ProfileRejected rejection) { require(codes.contains(rejection.code), "unexpected private refusal " + rejection.code); }
    }
    static void controls(Path root, Path output) throws Exception {
        List<String> results = new ArrayList<>(); int index = 0;
        Set<String> profile = Set.of("CONDITION_PROFILE");
        for (String raw : List.of("HasTrailingSlash()", "HasTrailingSlash('a','b')", "HasTrailingSlash('a/'", "HasTrailingSlash('a/')junk", "HasTrailingSlashX('a/')", "UnknownPredicate('a/')", "true And !false", "'a' != 'b'", "HasTrailingSlash(a/)", "HasTrailingSlash(\"a/\")", "HasTrailingSlash ('a/')")) {
            for (boolean skipped : List.of(false,true)) rejected(root.resolve("syntax-" + index++),raw,skipped,Map.of(),profile);
        }
        results.add("HT-STATIC-SYNTAX-AND-SKIPPED\tPRIVATE_CONTROL\t22_REFUSALS");
        for (String value : List.of("a;b/", "a/;b")) {
            Path owner = root.resolve("value-" + index++); Path file = fixture(owner,"HasTrailingSlash('$(Dynamic)')",false);
            require(evaluate(file,owner,Map.of("Dynamic","warm/")).property("P").equals("yes"),"warmup failed");
            rejected(owner,"HasTrailingSlash('$(Dynamic)')",false,Map.of("Dynamic",value),profile);
            require(evaluate(fixture(owner,"true Or HasTrailingSlash('$(Dynamic)')",false),owner,Map.of("Dynamic",value)).property("P").equals("yes"),"runtime token conversion reached skipped Or");
            require(evaluate(fixture(owner,"false And HasTrailingSlash('$(Dynamic)')",false),owner,Map.of("Dynamic",value)).property("P").isEmpty(),"runtime token conversion reached skipped And");
        }
        Path dataOwner = root.resolve("literal-data"); Path dataFile = fixture(dataOwner,"HasTrailingSlash('$(Dynamic)')",false);
        for (String value : List.of("a' Or true", "a') Or (\"x\" == \"x\")", "$(Again)", "a%252f", "a/%20", "a/\u001c"))
            require(evaluate(dataFile,dataOwner,Map.of("Dynamic",value)).property("P").isEmpty(),"expanded scalar reparsed/reexpanded/retrimmed: " + value);
        for (String value : List.of("a') Or (\"x\" == \"x\")/", "é/", "a b/", "a%2f", "a%3bb/", "; ; a/ ;;", "a/\u00a0", "a/\u0085", "https://example.invalid/", "Z:\\absent\\", "a%ZZ/"))
            require(evaluate(dataFile,dataOwner,Map.of("Dynamic",value)).property("P").equals("yes"),"ordinary scalar rejected or stale cached value: " + value);
        results.add("HT-WARM-LITERAL-DATA-AND-LAZY-TOKENIZATION\tPRIVATE_CONTROL\t17_SCALARS_2_LIST_REFUSALS");
        for (String syntax : List.of("@(Item)", "%(Meta)", "$([System.String]::Copy('a/'))")) rejected(root.resolve("static-"+index++),"HasTrailingSlash('"+syntax+"')",true,Map.of(),Set.of("PROPERTY_FUNCTION", "ASCII_PROPERTY_NAME", "CONDITION_PROFILE"));
        results.add("HT-STATIC-ITEM-METADATA-FUNCTION\tPRIVATE_CONTROL\t3_REFUSALS");
        String atom = "HasTrailingSlash('bounded/')";
        Path owner = root.resolve("budgets");
        require(evaluate(fixture(owner,"(".repeat(64)+atom+")".repeat(64),false),owner,Map.of()).property("P").equals("yes"),"64 groups rejected");
        rejected(owner,"(".repeat(65)+atom+")".repeat(65),false,Map.of(),Set.of("CONDITION_BOUND"));
        require(evaluate(fixture(owner,String.join(" And ",Collections.nCopies(128,atom)),false),owner,Map.of()).property("P").equals("yes"),"255 nodes rejected");
        rejected(owner,String.join(" And ",Collections.nCopies(129,atom)),false,Map.of(),Set.of("CONDITION_BOUND"));
        results.add("HT-EXISTING-GROUP-NODE-BUDGETS\tPRIVATE_CONTROL\t64_65_255_257");
        Files.write(output,results,StandardCharsets.UTF_8); System.out.println("PASS_HAS_TRAILING_SLASH_PRIVATE_CONTROLS groups=4 nativeParity=false");
    }
}
