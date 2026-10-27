// SPDX-License-Identifier: MIT

package System;

import System.Runtime.Serialization.ISerializable;
import System.Runtime.Serialization.SerializationInfo;
import System.Runtime.Serialization.StreamingContext;
import System.Reflection.MethodBase;
import System.Collections.IDictionary;
import org.dotj.internal.collections.ExceptionDataDictionary;

/** Selected unchecked Java carrier for the System.Exception candidate hierarchy. */
public class Exception extends RuntimeException implements ISerializable {
    private IDictionary data;
    private int hResult = -2146233088;
    private String helpLink;
    private String source;
    private StackTraceElement targetFrame;
    private MethodBase targetSite;

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
        String message = this.getMessage();
        return message == null ? "Exception of type '" + this.getClass().getName() + "' was thrown." : message;
    }

    public final Exception get_InnerException() {
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

    public IDictionary get_Data() {
        if (this.data == null) {
            this.data = new ExceptionDataDictionary();
        }
        return this.data;
    }

    public final int get_HResult() {
        return this.hResult;
    }

    public final void set_HResult(int value) {
        this.hResult = value;
    }

    public String get_HelpLink() {
        return this.helpLink;
    }

    public void set_HelpLink(String value) {
        this.helpLink = value;
    }

    public String get_Source() {
        return this.source;
    }

    public void set_Source(String value) {
        this.source = value;
    }

    public String ToString() {
        String typeName = this.getClass().getName();
        String message = this.get_Message();
        Exception inner = this.get_InnerException();
        String innerText = inner == null ? "" : inner.ToString();
        if (innerText == null) innerText = "";
        String stackTrace = this.get_StackTrace();
        String result = message == null || message.isEmpty() ? typeName : typeName + ": " + message;
        if (inner != null) {
            result += "\r\n ---> " + innerText
                    + "\r\n   --- End of inner exception stack trace ---";
        }
        if (stackTrace != null) result += "\r\n" + stackTrace;
        return result;
    }

    public final Type GetType() {
        return Type.fromJavaClass(this.getClass());
    }

    public String get_StackTrace() {
        return org.dotj.internal.throwing.ThrowSite.stackText(this);
    }

    public final MethodBase get_TargetSite() {
        StackTraceElement frame = org.dotj.internal.throwing.ThrowSite.targetFrame(this);
        if (frame == null) {
            return null;
        }
        if (!frame.equals(this.targetFrame)) {
            this.targetFrame = frame;
            this.targetSite = Type.capturedMethod(frame);
        }
        return this.targetSite;
    }

    protected String selectedSerializationMessage() { return super.getMessage(); }

    @Override
    public void GetObjectData(SerializationInfo info, StreamingContext context) {
        if (info == null) {
            throw new ArgumentNullException("info");
        }
        info.AddValue("ClassName", this.GetType().get_FullName(), Type.GetType("System.String"));
        info.AddValue("Message", this.selectedSerializationMessage(), Type.GetType("System.String"));
        info.AddValue("Data", (Object) this.data, Type.GetType("System.Collections.IDictionary"));
        info.AddValue("InnerException", this.get_InnerException(), Type.GetType("System.Exception"));
        info.AddValue("HelpURL", this.get_HelpLink(), Type.GetType("System.String"));
        info.AddValue("StackTraceString", this.get_StackTrace(), Type.GetType("System.String"));
        info.AddValue("RemoteStackTraceString", (Object) null, Type.GetType("System.String"));
        info.AddValue("RemoteStackIndex", 0);
        info.AddValue("ExceptionMethod", (Object) null, Type.GetType("System.String"));
        info.AddValue("HResult", this.get_HResult());
        info.AddValue("Source", this.get_Source(), Type.GetType("System.String"));
        info.AddValue("WatsonBuckets", (Object) null, Type.GetType("System.Byte[]"));
    }
}
