package consumer;

import System.IDisposable;

/** Separate compile-only consumer of the candidate JAR. */
public final class IndependentDisposableConsumer {
    private static final class Resource implements IDisposable {
        private int calls;

        @Override
        public void Dispose() {
            this.calls++;
        }
    }

    public static void main(String[] args) {
        Resource resource = new Resource();
        IDisposable contract = resource;
        contract.Dispose();
        if (resource.calls != 1) {
            throw new AssertionError("Interface dispatch did not reach the consumer implementation");
        }
        System.out.println("PASS: independent IDisposable candidate consumer");
    }
}
