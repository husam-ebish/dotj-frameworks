// SPDX-License-Identifier: MIT

package System;

/** Selected invalid-format exception candidate. */
public class FormatException extends SystemException {
    public FormatException() {
        super();
        this.set_HResult(-2146233033);
    }

    public FormatException(String message) {
        super(message);
        this.set_HResult(-2146233033);
    }

    public FormatException(String message, Exception innerException) {
        super(message, innerException);
        this.set_HResult(-2146233033);
    }
}
