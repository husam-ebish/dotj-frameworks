// SPDX-License-Identifier: MIT

package System;

/** Selected ordinary System.TimeoutException construction and inherited behavior. */
public class TimeoutException extends SystemException {
    private static final String DEFAULT_MESSAGE = "The operation has timed out.";

    public TimeoutException() { this(null, null); }

    public TimeoutException(String message) { this(message, null); }

    public TimeoutException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, innerException);
        this.set_HResult(-2146233083);
    }
}
