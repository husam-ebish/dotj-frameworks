// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

/** Pinned streaming-context state flags and unnamed zero value. */
public final class StreamingContextStates {
    public static final StreamingContextStates CrossProcess = new StreamingContextStates("CrossProcess", 1);
    public static final StreamingContextStates CrossMachine = new StreamingContextStates("CrossMachine", 2);
    public static final StreamingContextStates File = new StreamingContextStates("File", 4);
    public static final StreamingContextStates Persistence = new StreamingContextStates("Persistence", 8);
    public static final StreamingContextStates Remoting = new StreamingContextStates("Remoting", 16);
    public static final StreamingContextStates Other = new StreamingContextStates("Other", 32);
    public static final StreamingContextStates Clone = new StreamingContextStates("Clone", 64);
    public static final StreamingContextStates CrossAppDomain = new StreamingContextStates("CrossAppDomain", 128);
    public static final StreamingContextStates All = new StreamingContextStates("All", 255);

    private static final StreamingContextStates unnamedZero = new StreamingContextStates(null, 0);
    private static final StreamingContextStates[] named = {
        CrossProcess, CrossMachine, File, Persistence, Remoting, Other,
        Clone, CrossAppDomain, All
    };

    private final String name;
    private final int value;

    private StreamingContextStates(String name, int value) {
        this.name = name;
        this.value = value;
    }

    static StreamingContextStates zero() {
        return unnamedZero;
    }

    public String get_Name() {
        return this.name;
    }

    public int get_Value() {
        return this.value;
    }

    public static StreamingContextStates[] values() {
        return named.clone();
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof StreamingContextStates state && this.value == state.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
