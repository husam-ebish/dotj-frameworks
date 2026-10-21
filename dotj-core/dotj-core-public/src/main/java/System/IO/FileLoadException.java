package System.IO;

import System.Exception;

/** Selected malformed-assembly exception candidate. */
public class FileLoadException extends IOException {
    private final String fileName;

    public FileLoadException() {
        this(null, null, null);
    }

    public FileLoadException(String message) {
        this(message, null, null);
    }

    public FileLoadException(String message, Exception innerException) {
        this(message, null, innerException);
    }

    public FileLoadException(String message, String fileName) {
        this(message, fileName, null);
    }

    public FileLoadException(String message, String fileName, Exception innerException) {
        super(message, innerException);
        this.fileName = fileName;
    }

    public String get_FileName() {
        return this.fileName;
    }
}
