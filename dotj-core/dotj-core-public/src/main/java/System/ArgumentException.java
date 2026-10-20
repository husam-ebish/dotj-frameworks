package System;

/** Selected System.ArgumentException parameter identity candidate. */
public class ArgumentException extends SystemException {
    private final String paramName;

    public ArgumentException(String message, String paramName) {
        super(message);
        this.paramName = paramName;
    }

    public String get_ParamName() {
        return this.paramName;
    }
}
