// SPDX-License-Identifier: MIT

package System;

import System.Runtime.Serialization.SerializationInfo;
import System.Runtime.Serialization.StreamingContext;

/** Selected constructor and missing-name TypeLoadException profile. */
public class TypeLoadException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Failure has occurred while loading a type.";
    private final String typeName;
    private String selectedMessage;

    public TypeLoadException() {
        this(DEFAULT_MESSAGE, null, null);
    }

    public TypeLoadException(String message) {
        this(message, null, null);
    }

    public TypeLoadException(String message, Exception inner) {
        this(message, inner, null);
    }

    TypeLoadException(String message, Exception inner, String typeName) {
        super(message, inner);
        this.typeName = typeName;
        this.selectedMessage = message;
        this.set_HResult(-2146233054);
    }

    @Override
    public String get_Message() {
        if (this.selectedMessage == null) this.selectedMessage = DEFAULT_MESSAGE;
        return this.selectedMessage;
    }

    public String get_TypeName() { return this.typeName == null ? "" : this.typeName; }

    @Override
    protected String selectedSerializationMessage() { return this.selectedMessage; }

    @Override
    public void GetObjectData(SerializationInfo info, StreamingContext context) {
        super.GetObjectData(info, context);
        info.AddValue("TypeLoadClassName", this.typeName, Type.GetType("System.String"));
        info.AddValue("TypeLoadAssemblyName", (Object)null, Type.GetType("System.String"));
        info.AddValue("TypeLoadMessageArg", (Object)null, Type.GetType("System.String"));
        info.AddValue("TypeLoadResourceID", 0);
    }
}
