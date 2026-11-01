// SPDX-License-Identifier: MIT

package System;

/** Selected System.ObjectDisposedException candidate. */
public class ObjectDisposedException extends InvalidOperationException {
    private final String objectName;

    public ObjectDisposedException(String objectName) {
        this(objectName, "Cannot access a disposed object.");
    }

    public ObjectDisposedException(String objectName, String message) {
        super(message);
        this.set_HResult(-2146232798);
        this.objectName = objectName;
    }

    public String get_ObjectName() {
        return objectName == null ? "" : objectName;
    }
}
