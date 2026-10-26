// SPDX-License-Identifier: MIT

package System;

/** Selected invalid-operation exception candidate. */
public class InvalidOperationException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Operation is not valid due to the current state of the object.";
    public InvalidOperationException() {
        super(DEFAULT_MESSAGE);
        this.set_HResult(-2146233079);
    }

    public InvalidOperationException(String message) {
        super(message == null ? DEFAULT_MESSAGE : message);
        this.set_HResult(-2146233079);
    }

    public InvalidOperationException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, innerException);
        this.set_HResult(-2146233079);
    }
}
