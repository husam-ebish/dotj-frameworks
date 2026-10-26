// SPDX-License-Identifier: MIT

package System;

/** Selected arithmetic exception hierarchy carrier. */
public class ArithmeticException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Overflow or underflow in the arithmetic operation.";
    public ArithmeticException() {
        this("Overflow or underflow in the arithmetic operation.");
    }

    public ArithmeticException(String message) {
        this(message, null);
    }

    public ArithmeticException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, innerException);
        this.set_HResult(-2147024362);
    }
}
