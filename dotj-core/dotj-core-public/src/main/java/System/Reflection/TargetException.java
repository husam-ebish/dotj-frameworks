// SPDX-License-Identifier: MIT

package System.Reflection;
import System.ApplicationException;
import System.Exception;
/** Selected reflection target validation exception projection. */
public class TargetException extends ApplicationException {
    public TargetException() { super((String) null); this.set_HResult(-2146232829); }
    public TargetException(String message) { super(message); this.set_HResult(-2146232829); }
    public TargetException(String message, Exception inner) { super(message, inner); this.set_HResult(-2146232829); }
}
