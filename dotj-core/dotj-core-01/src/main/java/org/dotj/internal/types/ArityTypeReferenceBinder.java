package org.dotj.internal.types;

import java.util.Objects;

/** Bounded type-reference binder for the pinned Task-family arity pairs. */
final class ArityTypeReferenceBinder {
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
            String argument = null;
            if (generic) {
                position++;
                argument = parseType();
                skipWhitespace();
                if (atEnd() || input.charAt(position) != '>') {
                    throw new IllegalArgumentException("Expected one closing > at offset " + position);
                }
                position++;
            }
            int separator = name.lastIndexOf('.');
            String namespace = name.substring(0, separator);
            String simpleName = name.substring(separator + 1);
            if (namespace.equals("System.Threading.Tasks")) {
                String backend = ArityNameMap.backendBinaryName(namespace, simpleName, generic ? 1 : 0);
                return generic ? backend + "<" + argument + ">" : backend;
            }
            if (generic) {
                throw new IllegalArgumentException("Generic type is outside the bounded binder: " + name);
            }
            return name;
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
            return name.toString();
        }
    }
}
