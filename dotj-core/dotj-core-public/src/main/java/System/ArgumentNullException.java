// SPDX-License-Identifier: MIT

package System;

/** Selected null-argument exception candidate; message localization remains open. */
public class ArgumentNullException extends ArgumentException {
    private static final String DEFAULT_MESSAGE = "Value cannot be null.";
    public static void ThrowIfNull(Object argument) {
        ThrowIfNull(argument, null);
    }

    public static void ThrowIfNull(Object argument, String paramName) {
        if (argument == null) {
            throw new ArgumentNullException(paramName);
        }
    }

    public ArgumentNullException() {
        this((String) null);
    }

    public ArgumentNullException(String paramName) {
        super(DEFAULT_MESSAGE, paramName);
        this.set_HResult(-2147467261);
    }

    public ArgumentNullException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, null, innerException);
        this.set_HResult(-2147467261);
    }

    public ArgumentNullException(String paramName, String message) {
        super(message == null ? DEFAULT_MESSAGE : message, paramName);
        this.set_HResult(-2147467261);
    }
}
