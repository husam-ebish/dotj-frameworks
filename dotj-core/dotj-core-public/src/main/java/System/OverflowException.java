// SPDX-License-Identifier: MIT

package System;

/** Selected arithmetic overflow exception candidate. */
public class OverflowException extends ArithmeticException {
    private static final String DEFAULT_MESSAGE = "Arithmetic operation resulted in an overflow.";
    public OverflowException() {
        this("Arithmetic operation resulted in an overflow.");
    }

    public OverflowException(String message) {
        this(message, null);
    }

    public OverflowException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, innerException);
        this.set_HResult(-2146233066);
    }
}
