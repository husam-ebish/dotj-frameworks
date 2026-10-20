package org.dotj.internal.types;

public final class ArityTypeReferenceBinderTest {
    private ArityTypeReferenceBinderTest() {
    }

    public static void main(String[] args) {
        assertLower("System.Threading.Tasks.Task", "System.Threading.Tasks.Task");
        assertLower("System.Threading.Tasks.Task<System.String>",
                "System.Threading.Tasks.Task_1<System.String>");
        assertLower(" System.Threading.Tasks.Task< System.Threading.Tasks.Task<System.String> > ",
                "System.Threading.Tasks.Task_1<System.Threading.Tasks.Task_1<System.String>>");
        assertLower("System.Threading.Tasks.TaskCompletionSource<System.String>",
                "System.Threading.Tasks.TaskCompletionSource_1<System.String>");
        assertLower("System.Threading.Tasks.ValueTask<System.String>",
                "System.Threading.Tasks.ValueTask_1<System.String>");
        assertLower("System.Threading.Tasks.Task<System.String>[]",
                "System.Threading.Tasks.Task_1<System.String>[]");
        assertLower("System.Threading.Tasks.Task<System.String[]>[][]",
                "System.Threading.Tasks.Task_1<System.String[]>[][]");
        assertLower("System.Collections.Generic.List<System.Threading.Tasks.Task<System.String>>",
                "System.Collections.Generic.List<System.Threading.Tasks.Task_1<System.String>>");
        assertLower("java.util.Map<System.String, System.Threading.Tasks.Task<System.String>>",
                "java.util.Map<System.String, System.Threading.Tasks.Task_1<System.String>>");
        expectInvalid("Task<System.String>");
        expectInvalid("System.Threading.Tasks.Task<>");
        expectInvalid("System.Threading.Tasks.Task<System.String");
        expectInvalid("System.Threading.Tasks.Task<System.String, System.Int32>");
        expectInvalid("System.Threading.Tasks.Task<System.String, System.Threading.Tasks.Task<System.String>>");
        expectInvalid("System.Threading.Tasks.Unknown<System.String>");
        expectInvalid("System..Threading.Tasks.Task");
        expectInvalid("System.Threading.Tasks.Task trailing");
        expectInvalid("System.Threading.Tasks.Task[");
        expectInvalid("System.Threading.Tasks.Task[ ]");
        expectInvalid("System.Threading.Tasks.Task][]");
        expectInvalid("System.class.Task");
        expectInvalid("System.Threading.void.Task");
        String nested = "System.String";
        for (int depth = 0; depth < 32; depth++) {
            nested = "System.Threading.Tasks.Task<" + nested + ">";
        }
        ArityTypeReferenceBinder.lower(nested);
        expectInvalid("System.Threading.Tasks.Task<" + nested + ">");
        expectInvalid("System." + "A".repeat(4097));
        java.lang.System.out.println("PASS: bounded source type references bind Task-family arities without JVM collisions");
    }

    private static void assertLower(String source, String expected) {
        String actual = ArityTypeReferenceBinder.lower(source);
        if (!expected.equals(actual)) {
            throw new AssertionError("Expected " + expected + ", got " + actual);
        }
    }

    private static void expectInvalid(String source) {
        try {
            ArityTypeReferenceBinder.lower(source);
            throw new AssertionError("Invalid type reference accepted: " + source);
        } catch (IllegalArgumentException expected) {
            // Unsupported or malformed syntax remains an explicit error.
        }
    }
}
