// SPDX-License-Identifier: MIT

package System;

/** Selected System.ObjectDisposedException candidate. */
public class ObjectDisposedException extends InvalidOperationException {
    private final String objectName;

    public ObjectDisposedException(String objectName) {
        this(objectName, "Cannot access a disposed object.");
    }

    public ObjectDisposedException(String objectName, String message) {
        super(message == null ? "Cannot access a disposed object." : message);
        this.set_HResult(-2146232798);
        this.objectName = objectName;
    }

    public String get_ObjectName() {
        return objectName == null ? "" : objectName;
    }

    @Override
    public String get_Message() {
        String message = super.get_Message();
        return get_ObjectName().isEmpty() ? message : message + java.lang.System.lineSeparator()
                + "Object name: '" + objectName + "'.";
    }
}
