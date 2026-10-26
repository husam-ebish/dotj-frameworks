// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.SystemException;
import System.Exception;

/** Selected serialization lookup and duplicate-member error. */
public class SerializationException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Serialization error.";
    public SerializationException() {
        super(DEFAULT_MESSAGE);
        this.set_HResult(-2146233076);
    }

    public SerializationException(String message) {
        super(message == null ? DEFAULT_MESSAGE : message);
        this.set_HResult(-2146233076);
    }

    public SerializationException(String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, innerException);
        this.set_HResult(-2146233076);
    }
}
