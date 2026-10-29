// SPDX-License-Identifier: MIT

package System;
/** Selected default exception used by inherited reflection metadata guards. */
public class NotImplementedException extends SystemException {
    public NotImplementedException() { super("The method or operation is not implemented."); this.set_HResult(-2147467263); }
    public NotImplementedException(String message) { super(message == null ? "The method or operation is not implemented." : message); this.set_HResult(-2147467263); }
    public NotImplementedException(String message, Exception inner) { super(message == null ? "The method or operation is not implemented." : message, inner); this.set_HResult(-2147467263); }
}
