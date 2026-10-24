// SPDX-License-Identifier: MIT

package System;

/** Selected Type.GetType missing-name exception candidate. */
public class TypeLoadException extends SystemException {
    public TypeLoadException() {
        super();
        this.set_HResult(-2146233054);
    }

    public TypeLoadException(String message) {
        super(message);
        this.set_HResult(-2146233054);
    }

    public TypeLoadException(String message, Exception inner) {
        super(message, inner);
        this.set_HResult(-2146233054);
    }
}
