// SPDX-License-Identifier: MIT

package System;

/** Selected managed allocation exception projection; host JVM exhaustion remains distinct. */
public class OutOfMemoryException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Insufficient memory to continue the execution of the program.";

    public OutOfMemoryException() {
        this(DEFAULT_MESSAGE, null);
    }

    public OutOfMemoryException(String message) {
        this(message, null);
    }

    public OutOfMemoryException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, innerException);
        this.set_HResult(-2147024882);
    }
}
