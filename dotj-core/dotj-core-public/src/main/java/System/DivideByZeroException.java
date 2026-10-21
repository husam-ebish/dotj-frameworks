// SPDX-License-Identifier: MIT

package System;

/** Selected divide-by-zero exception hierarchy carrier. */
public class DivideByZeroException extends ArithmeticException {
    public DivideByZeroException() {
        this("Attempted to divide by zero.");
    }

    public DivideByZeroException(String message) {
        this(message, null);
    }

    public DivideByZeroException(String message, Exception innerException) {
        super(message, innerException);
        this.set_HResult(-2147352558);
    }
}
