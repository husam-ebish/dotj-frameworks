// SPDX-License-Identifier: MIT

package System;

/** Selected out-of-range argument exception candidate. */
public class ArgumentOutOfRangeException extends ArgumentException {
    private static final String DEFAULT_MESSAGE = "Specified argument was out of the range of valid values.";
    private final Object actualValue;

    public ArgumentOutOfRangeException() {
        this(null, null, DEFAULT_MESSAGE);
    }

    public ArgumentOutOfRangeException(String paramName) {
        this(paramName, null, DEFAULT_MESSAGE);
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
        super(message == null ? DEFAULT_MESSAGE : message, paramName);
        this.actualValue = actualValue;
        this.set_HResult(-2146233086);
    }

    public Object get_ActualValue() {
        return this.actualValue;
    }

    @Override
    public String get_Message() {
        String message = super.get_Message();
        return this.actualValue == null ? message : message + "\r\nActual value was " + this.actualValue + ".";
    }
}
