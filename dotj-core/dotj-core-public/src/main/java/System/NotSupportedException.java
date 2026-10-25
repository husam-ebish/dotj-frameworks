// SPDX-License-Identifier: MIT

package System;

/** Selected unsupported-operation exception constructors. */
public class NotSupportedException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Specified method is not supported.";

    public NotSupportedException() {
        this(DEFAULT_MESSAGE, null);
    }

    public NotSupportedException(String message) {
        this(message, null);
    }

    public NotSupportedException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, innerException);
        this.set_HResult(-2146233067);
    }
}
