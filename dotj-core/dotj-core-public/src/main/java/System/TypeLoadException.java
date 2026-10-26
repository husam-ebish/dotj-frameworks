// SPDX-License-Identifier: MIT

package System;

/** Selected Type.GetType missing-name exception candidate. */
public class TypeLoadException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Failure has occurred while loading a type.";
    public TypeLoadException() {
        super(DEFAULT_MESSAGE);
        this.set_HResult(-2146233054);
    }

    public TypeLoadException(String message) {
        super(message == null ? DEFAULT_MESSAGE : message);
        this.set_HResult(-2146233054);
    }

    public TypeLoadException(String message, Exception inner) {
        super(message == null ? DEFAULT_MESSAGE : message, inner);
        this.set_HResult(-2146233054);
    }
}
