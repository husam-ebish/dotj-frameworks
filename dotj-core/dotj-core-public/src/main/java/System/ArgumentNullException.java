package System;

/** Selected null-argument exception candidate; message localization remains open. */
public class ArgumentNullException extends ArgumentException {
    public ArgumentNullException(String paramName) {
        super("Value cannot be null.", paramName);
    }
}
