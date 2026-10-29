// SPDX-License-Identifier: MIT

package System;
/** Selected application exception constructor projection. */
public class ApplicationException extends Exception {
    public ApplicationException() { super("Error in the application."); this.set_HResult(-2146232832); }
    public ApplicationException(String message) { super(message); this.set_HResult(-2146232832); }
    public ApplicationException(String message, Exception inner) { super(message, inner); this.set_HResult(-2146232832); }
}
