// SPDX-License-Identifier: MIT

package System.IO;

import System.SystemException;
import System.Exception;

/** Selected I/O exception hierarchy candidate. */
public class IOException extends SystemException {
    private static final String DEFAULT_MESSAGE = "I/O error occurred.";
    public IOException() {
        super(DEFAULT_MESSAGE);
        this.set_HResult(-2146232800);
    }

    public IOException(String message) {
        super(message);
        this.set_HResult(-2146232800);
    }

    public IOException(String message, int hresult) {
        super(message);
        this.set_HResult(hresult);
    }

    public IOException(String message, Exception innerException) {
        super(message, innerException);
        this.set_HResult(-2146232800);
    }
}
