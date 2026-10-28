// SPDX-License-Identifier: MIT

package System.IO;

import System.Exception;
import System.Type;
import System.Runtime.Serialization.SerializationInfo;
import System.Runtime.Serialization.StreamingContext;

/** Selected missing-assembly exception candidate. */
public class FileNotFoundException extends IOException {
    private static final String DEFAULT_MESSAGE = "Unable to find the specified file.";
    private final String fileName;
    private String selectedMessage;

    public FileNotFoundException() {
        this(DEFAULT_MESSAGE, null, null);
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
        this.set_HResult(-2147024894);
        this.fileName = fileName;
        this.selectedMessage = message;
    }

    @Override
    public String get_Message() {
        if (this.selectedMessage == null) {
            if (this.fileName == null && this.get_HResult() == -2146233088) {
                this.selectedMessage = DEFAULT_MESSAGE;
            } else if (this.fileName != null) {
                this.selectedMessage = "Could not load file or assembly '" + this.fileName
                        + "'. The system cannot find the file specified.";
            }
        }
        return this.selectedMessage;
    }

    public String get_FusionLog() { return null; }

    @Override
    public String ToString() {
        String message = this.get_Message();
        String result = this.getClass().getName() + ": " + (message == null ? "" : message);
        if (this.fileName != null && !this.fileName.isEmpty()) {
            result += "\r\nFile name: '" + this.fileName + "'";
        }
        Exception inner = this.get_InnerException();
        if (inner != null) {
            String text = inner.ToString();
            result += "\r\n ---> " + (text == null ? "" : text);
        }
        String stack = this.get_StackTrace();
        if (stack != null) result += "\r\n" + stack;
        String fusion = this.get_FusionLog();
        if (fusion != null) result += "\r\n\r\n" + fusion;
        return result;
    }

    @Override
    protected String selectedSerializationMessage() { return this.selectedMessage; }

    @Override
    public void GetObjectData(SerializationInfo info,
                              StreamingContext context) {
        super.GetObjectData(info, context);
        info.AddValue("FileNotFound_FileName", this.fileName, Type.GetType("System.String"));
        info.AddValue("FileNotFound_FusionLog", this.get_FusionLog(), Type.GetType("System.String"));
    }

    public String get_FileName() {
        return this.fileName;
    }
}
