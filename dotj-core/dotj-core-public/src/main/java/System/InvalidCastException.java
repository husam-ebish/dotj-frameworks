// SPDX-License-Identifier: MIT

package System;

/** Selected invalid conversion exception candidate. */
public class InvalidCastException extends SystemException {
    public InvalidCastException() {
        super();
        this.set_HResult(-2147467262);
    }

    public InvalidCastException(String message) {
        super(message);
        this.set_HResult(-2147467262);
    }

    public InvalidCastException(String message, Exception innerException) {
        super(message, innerException);
        this.set_HResult(-2147467262);
    }

    public InvalidCastException(String message, int errorCode) {
        super(message);
        this.set_HResult(errorCode);
    }
}
