package org.dotj.internal.types;

public final class ErasureMethodNameMapTest {
    private ErasureMethodNameMapTest() {
    }

    public static void main(String[] args) {
        String owner = "System.Threading.Tasks.Task";
        String plain = ErasureMethodNameMap.backendName(owner, "FromException",
                "System.Threading.Tasks.Task FromException(System.Exception)");
        String generic = ErasureMethodNameMap.backendName(owner, "FromException",
                "System.Threading.Tasks.Task`1[TResult] FromException[TResult](System.Exception)");
        if (!plain.equals("FromException__dotj_c42000a95d67")
                || !generic.equals("FromException__dotj_d8530b802ffd")) {
            throw new AssertionError("Pinned overloads did not receive distinct Java backend names");
        }
        if (!plain.equals(ErasureMethodNameMap.backendName(owner, "FromException",
                "System.Threading.Tasks.Task FromException(System.Exception)"))) {
            throw new AssertionError("Backend name changed between calls");
        }
        expectInvalid(() -> ErasureMethodNameMap.backendName("System.Unknown", "FromException",
                "System.Threading.Tasks.Task FromException(System.Exception)"));
        expectInvalid(() -> ErasureMethodNameMap.backendName(owner, "FromException",
                "System.Threading.Tasks.Task Run(System.Exception)"));
        java.lang.System.out.println("PASS: pinned erased overloads map to distinct deterministic JVM names");
    }

    private static void expectInvalid(Runnable action) {
        try {
            action.run();
            throw new AssertionError("Expected invalid mapping to fail");
        } catch (IllegalArgumentException expected) {
            // Invalid identities must not enter the backend name map.
        }
    }
}
