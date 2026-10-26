// SPDX-License-Identifier: MIT

package System;

/** Selected invalid-array-rank exception candidate. */
public final class IndexOutOfRangeException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Index was outside the bounds of the array.";
    public IndexOutOfRangeException() {
        super(DEFAULT_MESSAGE);
        this.set_HResult(-2146233080);
    }

    public IndexOutOfRangeException(String message) {
        super(message == null ? DEFAULT_MESSAGE : message);
        this.set_HResult(-2146233080);
    }

    public IndexOutOfRangeException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, innerException);
        this.set_HResult(-2146233080);
    }
}
