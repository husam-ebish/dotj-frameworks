package System;

/** Selected invalid conversion exception candidate. */
public class InvalidCastException extends SystemException {
    public InvalidCastException() {
        super();
    }

    public InvalidCastException(String message) {
        super(message);
    }

    public InvalidCastException(String message, Exception innerException) {
        super(message, innerException);
    }

    public InvalidCastException(String message, int errorCode) {
        super(message);
    }
}
