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
}
