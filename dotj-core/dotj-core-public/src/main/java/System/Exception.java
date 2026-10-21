package System;

/** Selected unchecked Java carrier for the System.Exception candidate hierarchy. */
public class Exception extends RuntimeException {
    private java.util.Map<Object, Object> data;
    private int hResult = -2146233088;

    public Exception() {
        super();
    }

    public Exception(String message) {
        super(message);
    }

    public Exception(String message, Exception innerException) {
        super(message, innerException);
    }

    public String get_Message() {
        return this.getMessage();
    }

    public Exception get_InnerException() {
        return this.getCause() instanceof Exception innerException ? innerException : null;
    }

    public Exception GetBaseException() {
        java.util.IdentityHashMap<Exception, Boolean> visited = new java.util.IdentityHashMap<>();
        Exception current = this;
        while (current.get_InnerException() != null && visited.put(current, Boolean.TRUE) == null) {
            current = current.get_InnerException();
        }
        return current;
    }

    public java.util.Map<Object, Object> get_Data() {
        if (this.data == null) {
            this.data = new java.util.HashMap<>();
        }
        return this.data;
    }

    public int get_HResult() {
        return this.hResult;
    }

    protected void set_HResult(int value) {
        this.hResult = value;
    }
}
