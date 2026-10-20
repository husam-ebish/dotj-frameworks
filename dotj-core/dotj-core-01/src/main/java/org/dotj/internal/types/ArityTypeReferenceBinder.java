package org.dotj.internal.types;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Set;

/** Bounded type-reference binder for the pinned Task-family arity pairs. */
final class ArityTypeReferenceBinder {
    private static final Set<String> RESERVED = Set.of(
            "abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class",
            "const", "continue", "default", "do", "double", "else", "enum", "extends", "final",
            "finally", "float", "for", "goto", "if", "implements", "import", "instanceof", "int",
            "interface", "long", "native", "new", "package", "private", "protected", "public",
            "return", "short", "static", "strictfp", "super", "switch", "synchronized", "this",
            "throw", "throws", "transient", "try", "void", "volatile", "while", "_", "true",
            "false", "null", "record", "var", "yield", "sealed", "permits");

    private ArityTypeReferenceBinder() {
    }

    static String lower(String sourceTypeReference) {
        Parser parser = new Parser(Objects.requireNonNull(sourceTypeReference, "sourceTypeReference"));
        String result = parser.parseType();
        parser.skipWhitespace();
        if (!parser.atEnd()) {
            throw new IllegalArgumentException("Unexpected suffix at offset " + parser.position);
        }
        return result;
    }

    static boolean isSourceIdentifier(String value) {
        if (value.isEmpty() || RESERVED.contains(value) || !Character.isJavaIdentifierStart(value.charAt(0))) {
            return false;
        }
        for (int index = 1; index < value.length(); index++) {
            if (!Character.isJavaIdentifierPart(value.charAt(index))) {
                return false;
            }
        }
        return true;
    }

    private static final class Parser {
        private final String input;
        private int position;

        private Parser(String input) {
            this.input = input;
        }

        private boolean atEnd() {
            return position == input.length();
        }

        private void skipWhitespace() {
            while (!atEnd() && Character.isWhitespace(input.charAt(position))) {
                position++;
            }
        }

        private String parseType() {
            skipWhitespace();
            String name = parseQualifiedName();
            skipWhitespace();
            boolean generic = !atEnd() && input.charAt(position) == '<';
            List<String> arguments = new ArrayList<>();
            if (generic) {
                position++;
                arguments.add(parseType());
                skipWhitespace();
                while (!atEnd() && input.charAt(position) == ',') {
                    position++;
                    arguments.add(parseType());
                    skipWhitespace();
                }
                if (atEnd() || input.charAt(position) != '>') {
                    throw new IllegalArgumentException("Expected one closing > at offset " + position);
                }
                position++;
            }
            int arrayDimensions = 0;
            skipWhitespace();
            while (!atEnd() && input.charAt(position) == '[') {
                position++;
                if (atEnd() || input.charAt(position) != ']') {
                    throw new IllegalArgumentException("Expected closing array bracket at offset " + position);
                }
                position++;
                arrayDimensions++;
                skipWhitespace();
            }
            int separator = name.lastIndexOf('.');
            String namespace = name.substring(0, separator);
            String simpleName = name.substring(separator + 1);
            if (namespace.equals("System.Threading.Tasks")) {
                String backend = ArityNameMap.backendBinaryName(namespace, simpleName, arguments.size());
                return (generic ? backend + "<" + String.join(", ", arguments) + ">" : backend)
                        + "[]".repeat(arrayDimensions);
            }
            return (generic ? name + "<" + String.join(", ", arguments) + ">" : name)
                    + "[]".repeat(arrayDimensions);
        }

        private String parseQualifiedName() {
            StringBuilder name = new StringBuilder();
            boolean needSegment = true;
            while (!atEnd()) {
                char current = input.charAt(position);
                if (needSegment) {
                    if (!Character.isJavaIdentifierStart(current)) {
                        throw new IllegalArgumentException("Expected identifier at offset " + position);
                    }
                    needSegment = false;
                    name.append(current);
                    position++;
                } else if (Character.isJavaIdentifierPart(current)) {
                    name.append(current);
                    position++;
                } else if (current == '.') {
                    name.append(current);
                    position++;
                    needSegment = true;
                } else {
                    break;
                }
            }
            if (needSegment || name.indexOf(".") <= 0) {
                throw new IllegalArgumentException("A qualified type name is required at offset " + position);
            }
            for (String segment : name.toString().split("\\.")) {
                if (!isSourceIdentifier(segment)) {
                    throw new IllegalArgumentException("Type name is not a Java 21 qualified name: " + name);
                }
            }
            return name.toString();
        }
    }
}
