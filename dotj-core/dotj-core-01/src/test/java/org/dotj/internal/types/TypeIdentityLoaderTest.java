package org.dotj.internal.types;

import java.io.IOException;
import java.io.InputStream;

public final class TypeIdentityLoaderTest {
    private TypeIdentityLoaderTest() {
    }

    public static void main(String[] args) throws IOException, ClassNotFoundException {
        String name = "org.dotj.internal.types.LoadableType";
        String resource = name.replace('.', '/') + ".class";
        byte[] bytes;
        try (InputStream stream = TypeIdentityLoaderTest.class.getClassLoader().getResourceAsStream(resource)) {
            if (stream == null) {
                throw new AssertionError("test class bytes unavailable");
            }
            bytes = stream.readAllBytes();
        }

        Class<?> first = new IsolatedLoader(name, bytes).loadClass(name);
        Class<?> second = new IsolatedLoader(name, bytes).loadClass(name);
        if (!first.getName().equals(second.getName()) || first == second
                || TypeIdentity.of(first).equals(TypeIdentity.of(second))) {
            throw new AssertionError("same-name classes from distinct loaders share type identity");
        }
        System.out.println("PASS: same-name classes from isolated loaders remain distinct");
    }

    private static final class IsolatedLoader extends ClassLoader {
        private final String targetName;
        private final byte[] bytes;

        private IsolatedLoader(String targetName, byte[] bytes) {
            super(null);
            this.targetName = targetName;
            this.bytes = bytes;
        }

        @Override
        protected Class<?> findClass(String name) throws ClassNotFoundException {
            if (!name.equals(targetName)) {
                throw new ClassNotFoundException(name);
            }
            return defineClass(name, bytes, 0, bytes.length);
        }
    }
}
