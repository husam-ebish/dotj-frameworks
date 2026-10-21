package System;

/** Selected invalid-format exception candidate. */
public class FormatException extends SystemException {
    public FormatException() {
        super();
    }

    public FormatException(String message) {
        super(message);
    }

    public FormatException(String message, Exception innerException) {
        super(message, innerException);
    }
}
