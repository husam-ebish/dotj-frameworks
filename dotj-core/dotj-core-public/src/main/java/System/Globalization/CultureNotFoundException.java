package System.Globalization;

import System.ArgumentException;
import System.Exception;

/** Selected invalid-culture exception candidate. */
public class CultureNotFoundException extends ArgumentException {
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
        super(message, paramName, innerException);
        this.invalidCultureName = invalidCultureName;
        this.invalidCultureId = invalidCultureId;
    }

    public String get_InvalidCultureName() {
        return this.invalidCultureName;
    }

    public Integer get_InvalidCultureId() {
        return this.invalidCultureId;
    }
}
