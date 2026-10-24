// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.SystemException;
import System.Exception;

/** Selected serialization lookup and duplicate-member error. */
public class SerializationException extends SystemException {
    public SerializationException() {
        super();
        this.set_HResult(-2146233076);
    }

    public SerializationException(String message) {
        super(message);
        this.set_HResult(-2146233076);
    }

    public SerializationException(String message, Exception innerException) {
        super(message, innerException);
        this.set_HResult(-2146233076);
    }
}
