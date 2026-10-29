// SPDX-License-Identifier: MIT

package System;

/** Selected FieldAccessException constructors and literal-field failure projection. */
public class FieldAccessException extends MemberAccessException {
    private static final String DEFAULT_MESSAGE = "Attempted to access a field that is not accessible by the caller.";
    public FieldAccessException() { super(DEFAULT_MESSAGE); this.set_HResult(-2146233081); }
    public FieldAccessException(String message) { super(message == null ? DEFAULT_MESSAGE : message); this.set_HResult(-2146233081); }
    public FieldAccessException(String message, Exception innerException) { super(message == null ? DEFAULT_MESSAGE : message, innerException); this.set_HResult(-2146233081); }
}
