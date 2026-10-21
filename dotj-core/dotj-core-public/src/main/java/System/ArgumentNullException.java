// SPDX-License-Identifier: MIT

package System;

/** Selected null-argument exception candidate; message localization remains open. */
public class ArgumentNullException extends ArgumentException {
    public ArgumentNullException() {
        this((String) null);
    }

    public ArgumentNullException(String paramName) {
        super("Value cannot be null.", paramName);
    }

    public ArgumentNullException(String message, Exception innerException) {
        super(message, null, innerException);
    }

    public ArgumentNullException(String paramName, String message) {
        super(message, paramName);
    }
}
