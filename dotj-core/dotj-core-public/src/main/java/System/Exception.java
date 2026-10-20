package System;

/** Selected unchecked Java carrier for the System.Exception candidate hierarchy. */
public class Exception extends RuntimeException {
    public Exception(String message) {
        super(message);
    }

    public Exception(String message, Throwable innerException) {
        super(message, innerException);
    }
}
