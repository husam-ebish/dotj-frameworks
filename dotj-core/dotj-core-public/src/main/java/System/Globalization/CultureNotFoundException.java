// SPDX-License-Identifier: MIT

package System.Globalization;

import System.ArgumentException;
import System.Type;
import System.Runtime.Serialization.SerializationInfo;
import System.Runtime.Serialization.StreamingContext;
import System.Exception;
import System.InvalidOperationException;

/** Selected invalid-culture exception candidate. */
public class CultureNotFoundException extends ArgumentException {
    private static final String DEFAULT_MESSAGE = "Culture is not supported.";
    private final String invalidCultureName;
    private final Integer invalidCultureId;

    public CultureNotFoundException() {
        this(null, null, null, null, null);
    }

    public CultureNotFoundException(String message) {
        this(null, null, null, message, null);
    }

    public CultureNotFoundException(String paramName, String message) {
        this(paramName, null, null, message, null);
    }

    public CultureNotFoundException(String message, Exception innerException) {
        this(null, null, null, message, innerException);
    }

    public CultureNotFoundException(String paramName, String invalidCultureName, String message) {
        this(paramName, invalidCultureName, null, message, null);
    }

    public CultureNotFoundException(String message, String invalidCultureName, Exception innerException) {
        this(null, invalidCultureName, null, message, innerException);
    }

    public CultureNotFoundException(String message, int invalidCultureId, Exception innerException) {
        this(null, null, invalidCultureId, message, innerException);
    }

    public CultureNotFoundException(String paramName, int invalidCultureId, String message) {
        this(paramName, null, invalidCultureId, message, null);
    }

    private CultureNotFoundException(String paramName, String invalidCultureName,
                                     Integer invalidCultureId, String message, Exception innerException) {
        super(message == null ? DEFAULT_MESSAGE : message, paramName, innerException);
        this.invalidCultureName = invalidCultureName;
        this.invalidCultureId = invalidCultureId;
    }

    @Override
    public void GetObjectData(SerializationInfo info, StreamingContext context) {
        super.GetObjectData(info, context);
        info.AddValue("InvalidCultureId", this.invalidCultureId, Type.GetType("System.Nullable`1[System.Int32]"));
        info.AddValue("InvalidCultureName", this.invalidCultureName, Type.GetType("System.String"));
    }

    public String get_InvalidCultureName() {
        return this.invalidCultureName;
    }

    public Integer get_InvalidCultureId() {
        return this.invalidCultureId;
    }
    @Override
    public String get_Message() {
        String message = super.get_Message();
        if (this.invalidCultureId != null || this.invalidCultureName != null) {
            String identifier;
            if (get_InvalidCultureId() != null) {
                Integer value = get_InvalidCultureId();
                if (value == null) throw new InvalidOperationException("Nullable object must have a value.");
                String hex = Integer.toHexString(value);
                identifier = value + " (0x" + "0".repeat(Math.max(0, 4 - hex.length())) + hex + ")";
            } else {
                identifier = get_InvalidCultureName();
            }
            message += "\r\n" + (identifier == null ? "" : identifier) + " is an invalid culture identifier.";
        }
        return message;
    }
}
