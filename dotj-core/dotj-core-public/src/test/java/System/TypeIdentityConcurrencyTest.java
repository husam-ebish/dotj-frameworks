package System;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/** Checks selected loader separation and concurrent canonical Type construction. */
public final class TypeIdentityConcurrencyTest {
    public static void main(String[] args) throws java.lang.Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected fixture class-file path");
        }
        byte[] bytes = Files.readAllBytes(Path.of(args[0]));
        Class<?> firstClass = loadIsolated(bytes);
        Class<?> secondClass = loadIsolated(bytes);
        Type first = Type.fromJavaClass(firstClass);
        Type second = Type.fromJavaClass(secondClass);
        if (firstClass == secondClass || first == second || first.Equals(second)
                || Type.fromJavaClass(firstClass) != first) {
            throw new AssertionError("Distinct loader identities collapsed");
        }
        Type list = Type.fromJavaClass(List.class);
        if (list.MakeGenericType(new Type[] {first})
                == list.MakeGenericType(new Type[] {second})) {
            throw new AssertionError("Generic arguments from distinct loaders collapsed");
        }

        var pool = Executors.newFixedThreadPool(8);
        var ready = new CountDownLatch(8);
        var start = new CountDownLatch(1);
        try {
            List<Callable<Type>> tasks = new ArrayList<>();
            for (int index = 0; index < 8; index++) {
                tasks.add(() -> {
                    ready.countDown();
                    if (!start.await(10, TimeUnit.SECONDS)) {
                        throw new AssertionError("Concurrent start timed out");
                    }
                    Type result = null;
                    for (int iteration = 0; iteration < 200; iteration++) {
                        Type next = list.MakeGenericType(new Type[] {first});
                        if (result != null && result != next) {
                            throw new AssertionError("Canonical Type changed within worker");
                        }
                        result = next;
                    }
                    return result;
                });
            }
            var futures = new ArrayList<java.util.concurrent.Future<Type>>();
            for (var task : tasks) {
                futures.add(pool.submit(task));
            }
            if (!ready.await(10, TimeUnit.SECONDS)) {
                throw new AssertionError("Workers did not become ready");
            }
            start.countDown();
            Type expected = list.MakeGenericType(new Type[] {first});
            for (var future : futures) {
                if (future.get(10, TimeUnit.SECONDS) != expected) {
                    throw new AssertionError("Concurrent Type construction lost canonical identity");
                }
            }
        } finally {
            start.countDown();
            pool.shutdownNow();
        }
        java.lang.System.out.println("PASS System.Type isolated loader and 1600 concurrent canonical constructions");
    }

    private static Class<?> loadIsolated(byte[] bytes) throws ClassNotFoundException {
        ClassLoader loader = new ClassLoader(TypeIdentityConcurrencyTest.class.getClassLoader()) {
            @Override
            protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
                if (!name.equals("fixture.LoadableType")) {
                    return super.loadClass(name, resolve);
                }
                synchronized (getClassLoadingLock(name)) {
                    Class<?> existing = findLoadedClass(name);
                    if (existing == null) {
                        existing = defineClass(name, bytes, 0, bytes.length);
                    }
                    if (resolve) {
                        resolveClass(existing);
                    }
                    return existing;
                }
            }
        };
        return loader.loadClass("fixture.LoadableType");
    }
}
