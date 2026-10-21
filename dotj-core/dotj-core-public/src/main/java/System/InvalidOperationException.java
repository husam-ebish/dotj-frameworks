package System;

/** Selected invalid-operation exception candidate. */
public class InvalidOperationException extends SystemException {
    public InvalidOperationException() {
        super();
        this.set_HResult(-2146233079);
    }

    public InvalidOperationException(String message) {
        super(message);
        this.set_HResult(-2146233079);
    }

    public InvalidOperationException(String message, Exception innerException) {
        super(message, innerException);
        this.set_HResult(-2146233079);
    }
}
