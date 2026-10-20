package System;

/** Selected Type.GetType missing-name exception candidate. */
public class TypeLoadException extends SystemException {
    public TypeLoadException() {
        super();
    }

    public TypeLoadException(String message) {
        super(message);
    }

    public TypeLoadException(String message, Exception inner) {
        super(message, inner);
    }
}
