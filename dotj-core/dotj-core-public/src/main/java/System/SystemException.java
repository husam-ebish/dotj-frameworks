// SPDX-License-Identifier: MIT

package System;

/** Selected System.SystemException inheritance candidate. */
public class SystemException extends Exception {
    private static final String DEFAULT_MESSAGE = "System error.";
    public SystemException() {
        super(DEFAULT_MESSAGE);
        this.set_HResult(-2146233087);
    }

    public SystemException(String message) {
        super(message);
        this.set_HResult(-2146233087);
    }

    public SystemException(String message, Exception innerException) {
        super(message, innerException);
        this.set_HResult(-2146233087);
    }
}
