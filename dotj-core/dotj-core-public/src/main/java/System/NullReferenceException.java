// SPDX-License-Identifier: MIT

package System;

/** Selected null-reference failure type. */
public class NullReferenceException extends SystemException {
    public NullReferenceException() {
        super();
        this.set_HResult(-2147467261);
    }

    public NullReferenceException(String message) {
        super(message);
        this.set_HResult(-2147467261);
    }

    public NullReferenceException(String message, Exception innerException) {
        super(message, innerException);
        this.set_HResult(-2147467261);
    }
}
