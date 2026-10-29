// SPDX-License-Identifier: MIT

package System;

/** Selected MemberAccessException constructors and literal-field failure projection. */
public class MemberAccessException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Cannot access member.";
    public MemberAccessException() { super(DEFAULT_MESSAGE); this.set_HResult(-2146233062); }
    public MemberAccessException(String message) { super(message == null ? DEFAULT_MESSAGE : message); this.set_HResult(-2146233062); }
    public MemberAccessException(String message, Exception innerException) { super(message == null ? DEFAULT_MESSAGE : message, innerException); this.set_HResult(-2146233062); }
}
