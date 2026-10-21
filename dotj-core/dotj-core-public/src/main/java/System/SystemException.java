// SPDX-License-Identifier: MIT

package System;

/** Selected System.SystemException inheritance candidate. */
public class SystemException extends Exception {
    public SystemException() {
        super();
    }

    public SystemException(String message) {
        super(message);
    }

    public SystemException(String message, Exception innerException) {
        super(message, innerException);
    }
}
