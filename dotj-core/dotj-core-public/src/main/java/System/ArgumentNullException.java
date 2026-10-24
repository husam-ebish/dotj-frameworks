// SPDX-License-Identifier: MIT

package System;

/** Selected null-argument exception candidate; message localization remains open. */
public class ArgumentNullException extends ArgumentException {
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
        super("Value cannot be null.", paramName);
        this.set_HResult(-2147467261);
    }

    public ArgumentNullException(String message, Exception innerException) {
        super(message, null, innerException);
        this.set_HResult(-2147467261);
    }

    public ArgumentNullException(String paramName, String message) {
        super(message, paramName);
        this.set_HResult(-2147467261);
    }
}
