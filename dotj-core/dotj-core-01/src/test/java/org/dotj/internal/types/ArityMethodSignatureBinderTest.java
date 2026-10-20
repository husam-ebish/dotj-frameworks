package org.dotj.internal.types;

public final class ArityMethodSignatureBinderTest {
    private ArityMethodSignatureBinderTest() {
    }

    public static void main(String[] args) {
        assertLower("System.Threading.Tasks.Task Run()", "System.Threading.Tasks.Task Run()");
        assertLower("System.Threading.Tasks.Task WaitAsync(System.Threading.CancellationToken cancellationToken)",
                "System.Threading.Tasks.Task WaitAsync(System.Threading.CancellationToken cancellationToken)");
        assertLower("System.Threading.Tasks.Task<System.String> ContinueWith(System.Threading.Tasks.Task antecedent, System.Threading.Tasks.Task<System.String> other)",
                "System.Threading.Tasks.Task_1<System.String> ContinueWith(System.Threading.Tasks.Task antecedent, System.Threading.Tasks.Task_1<System.String> other)");
        assertLower("System.Threading.Tasks.Task<System.Threading.Tasks.Task<System.String>> Unwrap(System.Threading.Tasks.ValueTask<System.String> value)",
                "System.Threading.Tasks.Task_1<System.Threading.Tasks.Task_1<System.String>> Unwrap(System.Threading.Tasks.ValueTask_1<System.String> value)");
        expectInvalid("System.Threading.Tasks.Task Run(System.String)");
        expectInvalid("System.Threading.Tasks.Task Run(System.String value,)");
        expectInvalid("System.Threading.Tasks.Task Run(System.String value");
        expectInvalid("System.Threading.Tasks.Task Run(System.String value))");
        expectInvalid("System.Threading.Tasks.Task Run(System.Threading.Tasks.Task<System.String, System.String> value)");
        expectInvalid("System.Threading.Tasks.Task run-name()");
        java.lang.System.out.println("PASS: bounded Task-family method signature binding");
    }

    private static void assertLower(String source, String expected) {
        String actual = ArityMethodSignatureBinder.lower(source);
        if (!expected.equals(actual)) {
            throw new AssertionError("Expected " + expected + ", got " + actual);
        }
    }

    private static void expectInvalid(String source) {
        try {
            ArityMethodSignatureBinder.lower(source);
            throw new AssertionError("Invalid signature accepted: " + source);
        } catch (IllegalArgumentException expected) {
            // The bounded grammar fails closed.
        }
    }
}
