// SPDX-License-Identifier: MIT

package System;
/** Selected default exception used by inherited reflection metadata guards. */
public class NotImplementedException extends SystemException {
    public NotImplementedException() { super("The method or operation is not implemented."); this.set_HResult(-2147467263); }
}
