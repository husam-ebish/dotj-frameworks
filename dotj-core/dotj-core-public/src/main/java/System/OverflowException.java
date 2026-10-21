// SPDX-License-Identifier: MIT

package System;

/** Selected arithmetic overflow exception candidate. */
public class OverflowException extends SystemException {
    public OverflowException() {
        super();
    }

    public OverflowException(String message) {
        super(message);
    }

    public OverflowException(String message, Exception innerException) {
        super(message, innerException);
    }
}
