package org.dotj.internal.types;

import java.util.Objects;

/** Internal JVM binary-name mapping for the pinned Task-family arity collisions. */
final class ArityNameMap {
    private static final String NAMESPACE = "System.Threading.Tasks";

    private ArityNameMap() {
    }

    static String backendBinaryName(String namespace, String simpleName, int genericArity) {
        Objects.requireNonNull(namespace, "namespace");
        Objects.requireNonNull(simpleName, "simpleName");
        if (!NAMESPACE.equals(namespace)) {
            throw new IllegalArgumentException("Unsupported namespace: " + namespace);
        }
        if (!simpleName.equals("Task") && !simpleName.equals("TaskCompletionSource")
                && !simpleName.equals("ValueTask")) {
            throw new IllegalArgumentException("Unsupported type: " + simpleName);
        }
        if (genericArity != 0 && genericArity != 1) {
            throw new IllegalArgumentException("Unsupported generic arity: " + genericArity);
        }
        return namespace + "." + simpleName + (genericArity == 0 ? "" : "_1");
    }

    static String upstreamMetadataIdentity(String namespace, String simpleName, int genericArity) {
        backendBinaryName(namespace, simpleName, genericArity);
        return namespace + "." + simpleName + (genericArity == 0 ? "" : "`1");
    }
}
