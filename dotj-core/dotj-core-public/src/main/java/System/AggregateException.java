// SPDX-License-Identifier: MIT

package System;

/** Selected System.AggregateException candidate. */
public class AggregateException extends Exception {
    private static final String DEFAULT_MESSAGE = "One or more errors occurred.";
    private final Exception[] innerExceptions;

    public AggregateException(Exception... innerExceptions) {
        super(DEFAULT_MESSAGE, innerExceptions.length == 0 ? null : innerExceptions[0]);
        this.innerExceptions = innerExceptions.clone();
        this.set_HResult(-2146233088);
    }

    public Exception[] get_InnerExceptions() {
        return innerExceptions.clone();
    }

    @Override
    public String get_Message() {
        StringBuilder message = new StringBuilder(DEFAULT_MESSAGE);
        for (Exception inner : innerExceptions) {
            message.append(" (").append(inner.get_Message()).append(')');
        }
        return message.toString();
    }
}
