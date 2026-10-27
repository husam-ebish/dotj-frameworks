// SPDX-License-Identifier: MIT

package System;

/** Selected constructor and missing-name TypeLoadException profile. */
public class TypeLoadException extends SystemException {
    private static final String DEFAULT_MESSAGE = "Failure has occurred while loading a type.";
    private final String typeName;

    public TypeLoadException() {
        this(DEFAULT_MESSAGE, null, "");
    }

    public TypeLoadException(String message) {
        this(message, null, "");
    }

    public TypeLoadException(String message, Exception inner) {
        this(message, inner, "");
    }

    TypeLoadException(String message, Exception inner, String typeName) {
        super(message == null ? DEFAULT_MESSAGE : message, inner);
        this.typeName = typeName == null ? "" : typeName;
        this.set_HResult(-2146233054);
    }

    @Override
    public String get_Message() { return super.get_Message(); }

    public String get_TypeName() { return this.typeName; }
}
