// SPDX-License-Identifier: MIT

package System;

/** Selected invalid conversion exception candidate. */
public class InvalidCastException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Specified cast is not valid.";
    public InvalidCastException() {
        super(DEFAULT_MESSAGE);
        this.set_HResult(-2147467262);
    }

    public InvalidCastException(String message) {
        super(message == null ? DEFAULT_MESSAGE : message);
        this.set_HResult(-2147467262);
    }

    public InvalidCastException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, innerException);
        this.set_HResult(-2147467262);
    }

    public InvalidCastException(String message, int errorCode) {
        super(message);
        this.set_HResult(errorCode);
    }
}
