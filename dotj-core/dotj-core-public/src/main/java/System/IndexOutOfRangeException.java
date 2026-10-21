// SPDX-License-Identifier: MIT

package System;

/** Selected invalid-array-rank exception candidate. */
public class IndexOutOfRangeException extends SystemException {
    public IndexOutOfRangeException() {
        super();
    }

    public IndexOutOfRangeException(String message) {
        super(message);
    }

    public IndexOutOfRangeException(String message, Exception innerException) {
        super(message, innerException);
    }
}
