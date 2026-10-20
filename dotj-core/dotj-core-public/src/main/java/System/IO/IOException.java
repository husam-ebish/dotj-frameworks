package System.IO;

import System.SystemException;
import System.Exception;

/** Selected I/O exception hierarchy candidate. */
public class IOException extends SystemException {
    public IOException() {
        super();
    }

    public IOException(String message) {
        super(message);
    }

    public IOException(String message, int hresult) {
        super(message);
    }

    public IOException(String message, Exception innerException) {
        super(message, innerException);
    }
}
