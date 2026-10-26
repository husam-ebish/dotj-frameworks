// SPDX-License-Identifier: MIT

package System;

/** Selected invalid-format exception candidate. */
public class FormatException extends SystemException {
    private static final String DEFAULT_MESSAGE = "One of the identified items was in an invalid format.";
    public FormatException() {
        super(DEFAULT_MESSAGE);
        this.set_HResult(-2146233033);
    }

    public FormatException(String message) {
        super(message == null ? DEFAULT_MESSAGE : message);
        this.set_HResult(-2146233033);
    }

    public FormatException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, innerException);
        this.set_HResult(-2146233033);
    }
}
