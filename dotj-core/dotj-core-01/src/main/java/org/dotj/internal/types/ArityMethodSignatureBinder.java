package org.dotj.internal.types;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Binds a restricted, fully qualified method declaration without changing member names. */
final class ArityMethodSignatureBinder {
    private static final int MAX_SIGNATURE_LENGTH = 8192;
    private static final int MAX_PARAMETERS = 32;

    private ArityMethodSignatureBinder() {
    }

    static String lower(String declaration) {
        Objects.requireNonNull(declaration, "declaration");
        if (declaration.length() > MAX_SIGNATURE_LENGTH) {
            throw new IllegalArgumentException("Method signature exceeds " + MAX_SIGNATURE_LENGTH + " characters");
        }
        String source = declaration.trim();
        int open = source.indexOf('(');
        int close = source.lastIndexOf(')');
        if (open < 0 || close < open || !source.substring(close + 1).trim().isEmpty()) {
            throw new IllegalArgumentException("Expected one method parameter list");
        }
        String head = source.substring(0, open).trim();
        int split = head.lastIndexOf(' ');
        if (split <= 0) {
            throw new IllegalArgumentException("Expected return type and method name");
        }
        String method = head.substring(split + 1);
        requireIdentifier(method);
        String result = ArityTypeReferenceBinder.lower(head.substring(0, split).trim()) + " " + method;
        String parameters = source.substring(open + 1, close).trim();
        if (parameters.isEmpty()) {
            return result + "()";
        }
        List<String> lowered = new ArrayList<>();
        int depth = 0;
        int start = 0;
        for (int index = 0; index <= parameters.length(); index++) {
            char current = index == parameters.length() ? ',' : parameters.charAt(index);
            if (current == '<') {
                depth++;
            } else if (current == '>') {
                depth--;
                if (depth < 0) {
                    throw new IllegalArgumentException("Unexpected closing generic bracket");
                }
            } else if (current == ',' && depth == 0) {
                lowered.add(lowerParameter(parameters.substring(start, index).trim()));
                if (lowered.size() > MAX_PARAMETERS) {
                    throw new IllegalArgumentException("Parameter count exceeds " + MAX_PARAMETERS);
                }
                start = index + 1;
            }
        }
        if (depth != 0) {
            throw new IllegalArgumentException("Unclosed generic argument");
        }
        return result + "(" + String.join(", ", lowered) + ")";
    }

    private static String lowerParameter(String parameter) {
        int split = parameter.lastIndexOf(' ');
        if (split <= 0) {
            throw new IllegalArgumentException("Expected parameter type and name");
        }
        String name = parameter.substring(split + 1);
        requireIdentifier(name);
        return ArityTypeReferenceBinder.lower(parameter.substring(0, split).trim()) + " " + name;
    }

    private static void requireIdentifier(String value) {
        if (!ArityTypeReferenceBinder.isSourceIdentifier(value)) {
            throw new IllegalArgumentException("Expected Java identifier: " + value);
        }
    }
}
