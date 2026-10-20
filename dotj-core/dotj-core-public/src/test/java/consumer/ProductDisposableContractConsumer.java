package consumer;

import System.IDisposable;
import java.lang.reflect.Method;

/** Runs against the packaged public interface, with no product classes on the source path. */
public final class ProductDisposableContractConsumer {
    private static final class Counting implements IDisposable {
        private int count;

        @Override
        public void Dispose() {
            this.count++;
        }
    }

    private static final class Failing implements IDisposable {
        private final RuntimeException failure = new RuntimeException("dispose failed");

        @Override
        public void Dispose() {
            throw this.failure;
        }
    }

    private static void observeBorrowed(IDisposable resource) {
        if (resource == null) {
            throw new AssertionError("Missing resource");
        }
    }

    public static void main(String[] args) {
        Method[] methods = IDisposable.class.getDeclaredMethods();
        if (methods.length != 1 || !methods[0].getName().equals("Dispose")
                || methods[0].getReturnType() != void.class
                || methods[0].getParameterCount() != 0) {
            throw new AssertionError("Public interface shape changed");
        }
        if (AutoCloseable.class.isAssignableFrom(IDisposable.class)) {
            throw new AssertionError("AutoCloseable must remain an optional bridge");
        }

        Counting resource = new Counting();
        observeBorrowed(resource);
        if (resource.count != 0) {
            throw new AssertionError("Borrowed observation disposed the resource");
        }
        IDisposable contract = resource;
        contract.Dispose();
        if (resource.count != 1) {
            throw new AssertionError("Explicit Dispose did not dispatch exactly once");
        }

        Failing failing = new Failing();
        try {
            failing.Dispose();
            throw new AssertionError("Expected failure");
        } catch (RuntimeException caught) {
            if (caught != failing.failure) {
                throw new AssertionError("Dispose replaced the implementation failure", caught);
            }
        }
        java.lang.System.out.println("PASS: product IDisposable shape, explicit dispatch, borrowed ownership and failure propagation");
    }
}
