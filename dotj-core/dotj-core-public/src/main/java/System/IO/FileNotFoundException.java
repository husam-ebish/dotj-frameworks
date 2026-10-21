// SPDX-License-Identifier: MIT

package System.IO;

import System.Exception;

/** Selected missing-assembly exception candidate. */
public class FileNotFoundException extends IOException {
    private final String fileName;

    public FileNotFoundException() {
        this(null, null, null);
    }

    public FileNotFoundException(String message) {
        this(message, null, null);
    }

    public FileNotFoundException(String message, Exception innerException) {
        this(message, null, innerException);
    }

    public FileNotFoundException(String message, String fileName) {
        this(message, fileName, null);
    }

    public FileNotFoundException(String message, String fileName, Exception innerException) {
        super(message, innerException);
        this.fileName = fileName;
    }

    public String get_FileName() {
        return this.fileName;
    }
}
