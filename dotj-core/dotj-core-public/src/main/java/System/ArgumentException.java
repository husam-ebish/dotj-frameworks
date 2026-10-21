// SPDX-License-Identifier: MIT

package System;

/** Selected System.ArgumentException parameter identity candidate. */
public class ArgumentException extends SystemException {
    private final String paramName;

    public ArgumentException() {
        this(null, null, null);
    }

    public ArgumentException(String message) {
        this(message, null, null);
    }

    public ArgumentException(String message, Exception innerException) {
        this(message, null, innerException);
    }

    public ArgumentException(String message, String paramName) {
        this(message, paramName, null);
    }

    public ArgumentException(String message, String paramName, Exception innerException) {
        super(message, innerException);
        this.paramName = paramName;
        this.set_HResult(-2147024809);
    }

    public String get_ParamName() {
        return this.paramName;
    }

    @Override
    public String get_Message() {
        String message = super.get_Message();
        return this.paramName == null ? message : message + " (Parameter '" + this.paramName + "')";
    }
}
