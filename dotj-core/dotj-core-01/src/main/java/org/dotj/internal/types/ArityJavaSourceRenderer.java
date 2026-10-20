package org.dotj.internal.types;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Internal Java source rendering for bounded, arity-bound method signatures. */
final class ArityJavaSourceRenderer {
    private static final Pattern SYSTEM_TYPE = Pattern.compile(
            "(?<![A-Za-z0-9_$.])System(?:\\.[A-Za-z_$][A-Za-z0-9_$]*)+");

    private ArityJavaSourceRenderer() {
    }

    static BoundMethod renderMethod(String sourceSignature) {
        String bound = ArityMethodSignatureBinder.lower(sourceSignature);
        Matcher matcher = SYSTEM_TYPE.matcher(bound);
        StringBuilder declaration = new StringBuilder();
        Map<String, String> names = new HashMap<>();
        TreeSet<String> imports = new TreeSet<>();
        while (matcher.find()) {
            String qualified = matcher.group();
            String simple = qualified.substring(qualified.lastIndexOf('.') + 1);
            String previous = names.putIfAbsent(simple, qualified);
            if (previous != null && !previous.equals(qualified)) {
                throw new IllegalArgumentException("Conflicting simple type name " + simple
                        + ": " + previous + " and " + qualified);
            }
            imports.add(qualified);
            matcher.appendReplacement(declaration, Matcher.quoteReplacement(simple));
        }
        matcher.appendTail(declaration);
        return new BoundMethod(new ArrayList<>(imports), declaration.toString());
    }

    record BoundMethod(List<String> imports, String declaration) {
        BoundMethod {
            imports = List.copyOf(imports);
        }
    }
}
