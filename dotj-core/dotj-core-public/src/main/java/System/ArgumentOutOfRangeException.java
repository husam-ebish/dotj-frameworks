// SPDX-License-Identifier: MIT

package System;

/** Selected out-of-range argument exception candidate. */
public class ArgumentOutOfRangeException extends ArgumentException {
    private final Object actualValue;

    public ArgumentOutOfRangeException() {
        this(null, null, "Specified argument was out of range.");
    }

    public ArgumentOutOfRangeException(String paramName) {
        this(paramName, null, "Specified argument was out of range.");
    }

    public ArgumentOutOfRangeException(String paramName, String message) {
        this(paramName, null, message);
    }

    public ArgumentOutOfRangeException(String message, Exception innerException) {
        super(message, innerException);
        this.actualValue = null;
        this.set_HResult(-2146233086);
    }

    public ArgumentOutOfRangeException(String paramName, Object actualValue, String message) {
        super(message, paramName);
        this.actualValue = actualValue;
        this.set_HResult(-2146233086);
    }

    public Object get_ActualValue() {
        return this.actualValue;
    }
}
