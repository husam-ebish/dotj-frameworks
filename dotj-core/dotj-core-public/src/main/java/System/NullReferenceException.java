// SPDX-License-Identifier: MIT

package System;

/** Selected null-reference failure type. */
public class NullReferenceException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Object reference not set to an instance of an object.";
    public NullReferenceException() {
        super(DEFAULT_MESSAGE);
        this.set_HResult(-2147467261);
    }

    public NullReferenceException(String message) {
        super(message == null ? DEFAULT_MESSAGE : message);
        this.set_HResult(-2147467261);
    }

    public NullReferenceException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, innerException);
        this.set_HResult(-2147467261);
    }
}
