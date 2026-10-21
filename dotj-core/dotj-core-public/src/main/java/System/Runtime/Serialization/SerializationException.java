// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.SystemException;
import System.Exception;

/** Selected serialization lookup and duplicate-member error. */
public class SerializationException extends SystemException {
    public SerializationException() {
        super();
    }

    public SerializationException(String message) {
        super(message);
    }

    public SerializationException(String message, Exception innerException) {
        super(message, innerException);
    }
}
