package System;

/** Test-only bootstrap until .j typeof lowering supplies public Type instances. */
public final class TypeCandidateFactory {
    private TypeCandidateFactory() {
    }

    public static Type Of(Class<?> definition) {
        return Type.fromJavaClass(definition);
    }
}
