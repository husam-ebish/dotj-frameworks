// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

/** Bounded value-type identity for serialization method signatures. */
public final class StreamingContext {
    private final StreamingContextStates state;
    private final Object context;

    public StreamingContext() {
        this(StreamingContextStates.zero(), null);
    }

    public StreamingContext(StreamingContextStates state) {
        this(state, null);
    }

    public StreamingContext(StreamingContextStates state, Object context) {
        this.state = state;
        this.context = context;
    }

    public StreamingContextStates get_State() {
        return this.state;
    }

    public Object get_Context() {
        return this.context;
    }

    public boolean Equals(Object other) {
        return this.equals(other);
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof StreamingContext contextValue
                && this.state.equals(contextValue.state)
                && this.context == contextValue.context;
    }

    public int GetHashCode() {
        return this.hashCode();
    }

    @Override
    public int hashCode() {
        return 31 * this.state.get_Value() + java.lang.System.identityHashCode(this.context);
    }

    public String ToString() {
        return "System.Runtime.Serialization.StreamingContext";
    }

    @Override
    public String toString() {
        return this.ToString();
    }
}
