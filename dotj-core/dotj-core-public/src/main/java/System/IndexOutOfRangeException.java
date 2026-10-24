// SPDX-License-Identifier: MIT

package System;

/** Selected invalid-array-rank exception candidate. */
public class IndexOutOfRangeException extends SystemException {
    public IndexOutOfRangeException() {
        super();
        this.set_HResult(-2146233080);
    }

    public IndexOutOfRangeException(String message) {
        super(message);
        this.set_HResult(-2146233080);
    }

    public IndexOutOfRangeException(String message, Exception innerException) {
        super(message, innerException);
        this.set_HResult(-2146233080);
    }
}
