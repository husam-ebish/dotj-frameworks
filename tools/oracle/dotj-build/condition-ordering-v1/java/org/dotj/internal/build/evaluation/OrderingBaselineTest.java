package org.dotj.internal.build.evaluation;

import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.jar.JarFile;

/** Fixture-only baseline consumer. Its witness comes from a later frozen native bridge. */
public final class OrderingBaselineTest {
    private static final String MODULE = "org.dotj.build.evaluation.candidate";
    private static final String BASE_SHA = "97b027c56221716cc748aa03a80d24d65a180e13fb0deb07b059c2bbdd290b1c";
    private static void require(boolean value, String why) {
        if (!value) throw new AssertionError(why);
    }
    private static String sha(Path file) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        try (var input = Files.newInputStream(file)) {
            byte[] block = new byte[65536];
            for (int read; (read = input.read(block)) != -1;) digest.update(block, 0, read);
        }
        return HexFormat.of().formatHex(digest.digest());
    }
    private static String decode(String input) {
        return new String(Base64.getDecoder().decode(input), StandardCharsets.UTF_8);
    }
    private static void productOrigins(Path jar) throws Exception {
        require(sha(jar).equals(BASE_SHA), "exact qualified baseline JAR");
        Class<?> product = ProjectEvaluationComponent.class;
        require(product.getModule().isNamed() && MODULE.equals(product.getModule().getName()), "named product module");
        Path resolved = Path.of(ModuleLayer.boot().configuration().findModule(MODULE).orElseThrow().reference().location().orElseThrow()).toRealPath();
        require(resolved.equals(jar), "module origin must be baseline JAR");
        try (JarFile archive = new JarFile(jar.toFile())) {
            var entries = archive.entries();
            int classes = 0;
            while (entries.hasMoreElements()) {
                String entry = entries.nextElement().getName();
                if (!entry.endsWith(".class") || entry.equals("module-info.class")) continue;
                Class<?> type = Class.forName(entry.substring(0,entry.length()-6).replace('/','.'),false,product.getClassLoader());
                require(type.getModule() == product.getModule(), "class module origin: " + entry);
                require(type.getProtectionDomain().getCodeSource() != null, "class origin availability: " + entry);
                Path origin = Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath();
                require(origin.equals(jar), "product class leaked from patch/source path: " + entry);
                classes++;
            }
            require(classes > 0, "product class inventory");
            System.out.println("BASELINE_ORIGIN " + jar + " " + BASE_SHA + " classes=" + classes);
        }
    }
    public static void main(String[] args) throws Exception {
        require(args.length == 4,"baseline JAR, fixture root, frozen native bridge, bridge SHA required");
        Path jar=Path.of(args[0]).toRealPath(), root=Path.of(args[1]).toRealPath(), bridge=Path.of(args[2]).toRealPath();
        productOrigins(jar);
        require(sha(bridge).equals(args[3]),"frozen independently reviewed bridge digest");
        List<String> lines=Files.readAllLines(bridge,StandardCharsets.UTF_8);
        require(!lines.isEmpty() && lines.get(0).equals("ORDERING_NATIVE_SUCCESS_BRIDGE_V1"),"native bridge version");
        Set<String> ids=new HashSet<>(); boolean witness=false;
        for (String line:lines.subList(1,lines.size())) {
            String[] fields=line.split("\t",-1);
            require(fields.length==3 && fields[0].matches("[A-Za-z0-9_-]{1,96}") && ids.add(fields[0]),"closed bridge row");
            if (!fields[0].equals("ORD-HISTORY-BOOL-BOUND-ordering")) continue;
            witness=true; Path folder=root.resolve(fields[0]).toRealPath();
            require(folder.startsWith(root),"fixture containment");
            System.out.println("ORDERING_BASELINE_BEGIN " + fields[0]);
            // No catch of ProfileRejected: baseline must fail through its real ordering refusal.
            var result=ProjectEvaluationComponent.evaluate(folder.resolve("main.proj"),folder,Map.of());
            require(result.property("P").equals(decode(fields[1])) && result.property("Q").equals(decode(fields[2])),"native-backed ordering properties");
            require(result.imports().isEmpty() && result.conditionWarnings().isEmpty(),"historical witness extra observables");
            try(var paths=Files.walk(folder)) { require(paths.noneMatch(x->x.getFileName().toString().equals("must-not-exist.txt")),"task marker"); }
            System.out.println("ORDERING_BASELINE_END " + fields[0]);
        }
        require(witness,"fresh native-observed historical ordering witness required");
    }
}
