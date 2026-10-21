package System;

/** Selected invalid-operation exception candidate. */
public class InvalidOperationException extends SystemException {
    public InvalidOperationException() {
        super();
    }

    public InvalidOperationException(String message) {
        super(message);
    }

    public InvalidOperationException(String message, Exception innerException) {
        super(message, innerException);
    }
}
