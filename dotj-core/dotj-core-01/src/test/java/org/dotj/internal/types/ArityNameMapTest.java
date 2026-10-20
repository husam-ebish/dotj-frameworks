package org.dotj.internal.types;

import java.util.HashSet;
import java.util.Set;

public final class ArityNameMapTest {
    private ArityNameMapTest() {
    }

    public static void main(String[] args) {
        String namespace = "System.Threading.Tasks";
        Set<String> backendNames = new HashSet<>();
        for (String name : new String[]{"Task", "TaskCompletionSource", "ValueTask"}) {
            String plain = ArityNameMap.backendBinaryName(namespace, name, 0);
            String generic = ArityNameMap.backendBinaryName(namespace, name, 1);
            assertEquals(namespace + "." + name, plain);
            assertEquals(namespace + "." + name + "_1", generic);
            assertEquals(namespace + "." + name, ArityNameMap.upstreamMetadataIdentity(namespace, name, 0));
            assertEquals(namespace + "." + name + "`1", ArityNameMap.upstreamMetadataIdentity(namespace, name, 1));
            if (!backendNames.add(plain) || !backendNames.add(generic)) {
                throw new AssertionError("JVM names collided");
            }
        }
        assertEquals(6, backendNames.size());
        expectInvalid(() -> ArityNameMap.backendBinaryName(namespace, "Task", -1));
        expectInvalid(() -> ArityNameMap.backendBinaryName(namespace, "Task", 2));
        expectInvalid(() -> ArityNameMap.backendBinaryName(namespace, "Unknown", 0));
        expectInvalid(() -> ArityNameMap.backendBinaryName("org.dotj", "Task", 0));
        java.lang.System.out.println("PASS: six pinned Task-family identities lower to distinct internal JVM names");
    }

    private static void expectInvalid(Runnable action) {
        try {
            action.run();
            throw new AssertionError("Expected unsupported mapping to fail");
        } catch (IllegalArgumentException expected) {
            // Unsupported identities cannot silently become public substitutes.
        }
    }

    private static void assertEquals(Object expected, Object actual) {
        if (!expected.equals(actual)) {
            throw new AssertionError("Expected " + expected + ", got " + actual);
        }
    }
}
