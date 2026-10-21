// SPDX-License-Identifier: MIT

package System;

/** Selected arithmetic exception hierarchy carrier. */
public class ArithmeticException extends SystemException {
    public ArithmeticException() {
        this("Overflow or underflow in the arithmetic operation.");
    }

    public ArithmeticException(String message) {
        this(message, null);
    }

    public ArithmeticException(String message, Exception innerException) {
        super(message, innerException);
        this.set_HResult(-2147024362);
    }
}
